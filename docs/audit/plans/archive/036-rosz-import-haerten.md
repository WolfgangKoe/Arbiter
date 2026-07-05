# Plan 036: `.rosz`-Import härten — Stored-XSS über Roster-Namen unterbinden + Zip-Bomb-Cap

> **Executor instructions**: Schritt für Schritt folgen, jede Verifikation
> ausführen. Bei STOP-Bedingung: stoppen und berichten. Am Ende Status-Zeile in
> `docs/audit/plans/README.md` aktualisieren. Keine Exploit-Payloads über die
> Testfälle hinaus erzeugen.
>
> **Drift check (zuerst ausführen)**:
> `git diff --stat f6c464a..HEAD -- src/gameObjects/rosz_importer.py src/uiLayout/gameHeader.py tests/gameObjects/test_rosz_importer.py`
> Bei Änderungen: Exzerpte gegen Live-Code prüfen; Abweichung → STOP.

## Status

- **Priority**: P1
- **Effort**: S
- **Risk**: LOW
- **Depends on**: none
- **Category**: security
- **Planned at**: commit `f6c464a`, 2026-07-05

## Why this matters

Der BattleScribe-Import ist die **einzige** Freitext-Quelle der App (kein
`st.text_input`/`st.text_area` existiert in `src/`). Zwei Lücken:

1. **Stored XSS**: Das `name`-Attribut der hochgeladenen Roster-XML wird
   unverändert als `display_name` ins Roster-YAML persistiert, beim Spielstart
   zum Spielernamen und in `gameHeader.py` per f-String in
   `unsafe_allow_html`-Markup interpoliert. Ein präparierter Roster-Name (z. B.
   `<img src=x onerror=…>`) führt Script im Browser aus — und weil Roster
   serverseitig unter `data/rosters/` liegen, trifft das auf einem geteilten
   Deployment (Dockerfile/HF Spaces, Port 7860, `0.0.0.0`) auch **spätere
   Besucher**, die das Roster aus dem Dropdown wählen.
2. **Zip-Bomb-DoS**: Der 5-MB-Check prüft nur die **komprimierte** Größe;
   `zf.read()` liest die dekomprimierte Datei ohne Limit in den Speicher — ein
   kleines, hochkomprimiertes Archiv kann den Streamlit-Prozess (alle Sessions)
   lahmlegen.

## Current state

**Quelle** — `src/gameObjects/rosz_importer.py:155-177`:

```python
def parse_rosz_bytes(data: bytes) -> tuple[str, ET.Element]:
    if len(data) > _MAX_SIZE_BYTES:                       # nur komprimierte Größe
        raise ValueError(f"File too large ({len(data):,} bytes; max 5 MB)")
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as zf:
            ros_files = [n for n in zf.namelist() if n.endswith(".ros")]
            if not ros_files:
                raise ValueError("No .ros file found inside the .rosz archive")
            xml_bytes = zf.read(ros_files[0])             # ← kein Dekompressions-Limit
    except zipfile.BadZipFile as exc:
        raise ValueError(f"Invalid .rosz file (not a ZIP archive): {exc}") from exc
    root = _validate_and_parse_xml(xml_bytes)
    return root.attrib.get("name", "imported_roster"), root   # ← Name ungefiltert
```

(`parse_ros_bytes`, Zeile ~171-177, gibt den Namen ebenso ungefiltert zurück.
`_MAX_SIZE_BYTES = 5 * 1024 * 1024` steht in Zeile 20. `defusedxml` schützt nur
das Parsen, nicht den Attribut-Inhalt.)

**Persistenz** — `rosz_importer.py:228-239` (`import_roster`): Der *Dateiname*
wird sanitisiert (`safe_name = re.sub(...)`), der **Inhalt** nicht:

```python
        yaml.dump(
            {"display_name": roster_name, "faction_dir": faction_dir, "units": matched},
```

**Senke** — `src/uiLayout/gameHeader.py:266-271` (`display_name` → via
`game_state.py:89` und `:409-412` als `active`/`first`/`second` im Session-State):

```python
    st.markdown(
        f'<div style="text-align:center;font-size:1.0rem;font-weight:600;'
        f'letter-spacing:0.1em;color:#fbbf24;text-transform:uppercase;margin-bottom:6px;">'
        f"{phase_name} · {active}</div>",
        unsafe_allow_html=True,
    )
```

## Commands you will need

| Purpose | Command | Expected on success |
|---|---|---|
| Vollsuite + Coverage | `pytest --tb=short` | exit 0, Coverage ≥ 99 % |
| Importer-Tests | `pytest tests/gameObjects/test_rosz_importer.py --no-cov -q` | all pass |
| Sink-Suche | `grep -rn "unsafe_allow_html" src/uiLayout/ \| wc -l` | Basis für Step 3 |
| Lint | `ruff check src/ && black --check src/ && isort --check-only src/` | exit 0 |

## Scope

**In scope:**
- `src/gameObjects/rosz_importer.py` (Sanitisierung + Dekompressions-Cap)
- `src/uiLayout/gameHeader.py` (Escaping an der Senke)
- `tests/gameObjects/test_rosz_importer.py` (neue Tests)

**Out of scope:**
- `data/rosters/*.yaml` — bestehende, vertrauenswürdige Roster nicht umschreiben.
- Andere `unsafe_allow_html`-Stellen, die **keine** nutzergesteuerten Strings
  interpolieren (dice_html, badges mit YAML-Katalogdaten) — nur inventarisieren
  (Step 3), nicht umbauen.
- Der XML-Parse-Pfad (`_validate_and_parse_xml`) — bereits defusedxml-gehärtet.

## Git workflow

- Branch: `fix/036-rosz-import-hardening`
- Commits z. B. `Sanitize imported roster names against HTML injection`,
  `Cap decompressed size of rosz archive members`
- Nicht pushen ohne Anweisung.

## Steps

### Step 1: Roster-Namen an der Quelle sanitisieren

In `rosz_importer.py` einen Modul-Helper einführen und in **beiden**
Parse-Funktionen auf den zurückgegebenen Namen anwenden:

```python
_NAME_STRIP_RE = re.compile(r"[<>&\"']")

def _sanitize_roster_name(raw: str) -> str:
    """Remove HTML-active characters from an imported roster name."""
    cleaned = _NAME_STRIP_RE.sub("", raw).strip()
    return cleaned or "imported_roster"
```

Rückgabe: `_sanitize_roster_name(root.attrib.get("name", "imported_roster"))`.
Damit ist auch der persistierte `display_name` in `import_roster` sauber
(er erhält den bereits sanitisierten Namen als Parameter).

**Verify**: `pytest tests/gameObjects/test_rosz_importer.py --no-cov -q` → all pass
(bestehende Tests nutzen harmlose Namen; wird einer rot, weil er Sonderzeichen
im Namen erwartet → STOP, siehe unten).

### Step 2: Dekompressions-Cap

In `parse_rosz_bytes`, vor `zf.read(...)`:

```python
_MAX_DECOMPRESSED_BYTES = 20 * 1024 * 1024  # .ros-XML sind < 1 MB; 20 MB ist großzügig

            info = zf.getinfo(ros_files[0])
            if info.file_size > _MAX_DECOMPRESSED_BYTES:
                raise ValueError(
                    f"Roster XML too large when decompressed "
                    f"({info.file_size:,} bytes; max 20 MB)"
                )
```

**Verify**: `pytest tests/gameObjects/test_rosz_importer.py --no-cov -q` → all pass.

### Step 3: Escaping an der Render-Senke (Defense-in-depth)

`grep -rn "unsafe_allow_html" src/uiLayout/` ausführen und jede Stelle
klassifizieren: interpoliert sie einen String, der aus `display_name` /
`first_player` / `second_player` / `active` stammt? Nach dem Audit-Stand ist das
nur `gameHeader.py:266-271`. Dort:

```python
import html
        f"{phase_name} · {html.escape(active)}</div>",
```

Findet der grep **weitere** Spielernamen-Senken, diese ebenfalls mit
`html.escape(...)` versehen und im Abschlussbericht auflisten.

**Verify**: `pytest --tb=short` → exit 0 (gameHeader ist coverage-ausgenommen;
Suite darf nicht brechen).

### Step 4: Tests + Vollsuite + Lint (siehe Test plan)

**Verify**: `pytest --tb=short` → exit 0, Coverage ≥ 99 %; Lint-Dreier → exit 0.

## Test plan

Neue Tests in `tests/gameObjects/test_rosz_importer.py` (strukturell an den
bestehenden Tests der Datei orientieren — sie bauen `.ros`-XML-Bytes bzw.
In-Memory-Zips):

1. `test_roster_name_html_chars_stripped` — XML mit
   `name='<script>alert(1)</script>Necrons'` → `parse_ros_bytes` liefert einen
   Namen ohne `<`, `>`, `&`, `"`, `'` (z. B. `scriptalert(1)/scriptNecrons`).
2. `test_roster_name_only_html_chars_falls_back` — `name='<>'` → Fallback
   `imported_roster`.
3. `test_display_name_sanitized_in_written_yaml` — `import_roster` mit
   präpariertem Namen → geschriebenes YAML enthält keine HTML-aktiven Zeichen
   in `display_name`.
4. `test_rosz_decompression_bomb_rejected` — In-Memory-Zip, dessen `.ros`-Member
   > 20 MB dekomprimiert (z. B. `b"0" * (21*1024*1024)` mit `ZIP_DEFLATED`
   geschrieben — komprimiert winzig) → `ValueError` mit „too large".
5. `test_rosz_normal_size_still_parses` — Regressionsschutz: normales kleines
   Archiv parst weiterhin.

**Manuelle UI-Verifikation** (Render-Code, im Abschlussbericht nennen): App
starten, Spiel mit beliebigem Roster beginnen → Header zeigt Namen unverändert
an (Escaping darf legitime Namen nicht sichtbar verändern).

## Done criteria

- [ ] `pytest --tb=short` exit 0, Coverage ≥ 99 %; 5 neue Tests grün
- [ ] `parse_rosz_bytes`/`parse_ros_bytes` geben nur sanitisierte Namen zurück
- [ ] Dekompressions-Cap aktiv (Test 4 grün)
- [ ] `gameHeader.py` escaped `active` an der HTML-Senke
- [ ] `git status`: nur In-Scope-Dateien geändert
- [ ] Status-Zeile in `docs/audit/plans/README.md` aktualisiert

## STOP conditions

- Ein bestehender Importer-Test erwartet Sonderzeichen-Erhalt im Namen →
  Verhaltensbruch bestätigen lassen (Sicherheitsnetz-Regel).
- Der grep in Step 3 findet Spielernamen-Interpolation in mehr als 3 weiteren
  Dateien → Umfang meldepflichtig, nicht eigenmächtig flächig umbauen.
- `import_roster` erhält den Namen inzwischen aus anderer Quelle als den beiden
  Parse-Funktionen (Drift) → Sanitisierungspunkt neu bewerten, berichten.

## Maintenance notes

- Regel für künftige Features: **Jeder** String, der je aus Nutzereingaben oder
  importierten Dateien stammen kann, wird an `unsafe_allow_html`-Senken durch
  `html.escape()` geführt. Reviewer sollten bei neuen `unsafe_allow_html`-Aufrufen
  die Herkunft jeder Interpolation prüfen.
- Bereits vorhandene Roster-YAMLs unter `data/rosters/` wurden lokal erzeugt und
  gelten als vertrauenswürdig; wer dem Misstraut, kann die YAML-`display_name`s
  einmalig durch `_sanitize_roster_name` ziehen (bewusst nicht Teil dieses Plans).
- Das 20-MB-Cap ist bewusst großzügig; reale `.ros`-Dateien liegen unter 1 MB.
