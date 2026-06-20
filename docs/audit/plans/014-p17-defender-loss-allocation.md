# Plan 014: P17 — Interaktive Schadenszuweisung auf Subgruppen (Defender Loss Allocation)

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `docs/audit/plans/README.md`.
>
> **Drift check (run first)**:
> - Plan 013 MUSS DONE sein (`docs/audit/plans/README.md`); `grep -rn
>   "render_attack_declaration" src/` → 0 Call-Sites (Beweis, dass 013 lief).
> - `grep -n "def apply_damage\|def _apply_group_wound_damage\|def
>   _recompute_from_group_wounds\|def _front_group_hp\|group_wounds" \
>   src/gameMechanic/unit_mutations.py` → die genannten Funktionen + der
>   `group_wounds`-Branch existieren. Stimmt das nicht: STOP, Neuabgleich.
> - `grep -n "has_per_group_wounds\|group_wound_value" src/gameObjects/unit.py`
>   und `grep -n "group_wounds" src/gameMechanic/game_state.py` → vorhanden.

## Status

- **Priority**: P1-HOCH (ziel6.md §6n P17, neu geplant Refinement 2026-06-21)
- **Effort**: M–L (Schadenspfad-Vereinheitlichung berührt alle Gruppen-Einheiten)
- **Risk**: HIGH (greift in den zentralen Schadenspfad ein; Regressionsfläche groß)
- **Depends on**: 013 (zwingend — ein Code-Pfad, beide ändern `_common.py`);
  019 (empfohlen vorher — `pending_target_request`-Pattern)
- **Category**: feature (Regelkonformität Verlust-Zuweisung) + Refactor (Schadenspfad)
- **Planned at**: Refinement 2026-06-21 (Neuplanung; ersetzt die Fassung vom 2026-06-20)
- **Branch**: `feature/014-defender-loss-allocation`

## Warum diese Neuplanung (Lektion aus der alten Fassung)

Die alte Fassung dieses Plans hatte **zwei tödliche Designfehler**, die beim
Code-Abgleich (Refinement 2026-06-21) auffielen:

1. **`group_wounds`-Namenskollision.** Die alte Fassung wollte ein neues Feld
   `group_wounds[gid]` = „Wunden des Frontmodells je Gruppe" einführen. Dieses
   Feld **existiert bereits** in `game_state.py`/`unit_mutations.py` mit anderer
   Bedeutung: der **HP-Pool einer Gruppe** — und wird heute **nur** für Einheiten
   mit unterschiedlichen Wundenwerten je Gruppe befüllt (`has_per_group_wounds()`,
   z. B. Szarekh 16 + Triarchal Menhirs 7). Eine Umdefinition hätte den
   Szarekh-Pfad zerstört.
2. **Selbstwiderspruch.** Die alte Fassung erklärte „Frontmodell-Tracking" für
   *out of scope*, der Lock-Mechanismus (s. u.) **braucht** dieses Tracking aber
   zwingend. Das Leitbeispiel Nobz (alle 3 LP, nur gemischte Waffen) wäre damit
   nicht baubar gewesen.

**Konsens-Entscheidung (Stakeholder, 2026-06-21):** `group_wounds` wird zum
**einen kanonischen Per-Gruppen-HP-Pool für ALLE Gruppen-Einheiten** gemacht
(nicht mehr nur bei gemischten Wundenwerten). Damit verschmelzen die zwei
heutigen Pfade in `apply_damage` zu einem. Der Lock und die freie Wahl ergeben
sich direkt aus den Pool-Ständen. Der triviale Fall (homogene Einheit, eine
Subgruppe) geht als Spezialfall in derselben Struktur auf.

## Warum das fachlich nötig ist

Regel (9E): Der **Verteidiger** bestimmt, welche Modelle Schaden erhalten.
Heute verteilt die App automatisch priority-aufsteigend — falsch bei gemischten
Subgruppen (Nobz mit verschiedenen Waffen: WELCHER Nob fällt, bestimmt die
verfügbaren Waffen der Folgerunden).

**Lock-Regel (9E):** Ist ein Modell angeschlagen (hat Wunden verloren, lebt aber
noch), MÜSSEN alle weiteren Wunden dieses Turns auf dieses Modell — also dessen
Subgruppe — gelenkt werden. Andere Subgruppen sind gesperrt. Erst nach
Zerstörung des angeschlagenen Modells ist freie Wahl wieder möglich.

**Fähigkeitsverlust:** Fällt eine Subgruppe komplett (letztes Modell zerstört),
verliert die Einheit deren Ausrüstung/Fähigkeit — die App zeigt das als Warnung.

**Mortal Wounds (Overflow):** `mortal=True` erlaubt Overflow über Modell-Grenzen
hinaus und ignoriert den Lock (Schaden „läuft durch"). Bestehendes Verhalten —
muss erhalten bleiben (Regressionstest).

**Lethal Hits:** OUT OF SCOPE (eigener Plan nach 014, siehe backlog.md §2).

## Datenmodell (Konsens-Entscheidung umsetzen)

### `group_wounds` universell befüllen

`game_state._unit_state` befüllt `group_wounds` heute nur, wenn
`u.has_per_group_wounds()`. **Neu:** für JEDE Einheit mit `model_groups`:

```
group_wounds = {g.id: g.count * u.group_wound_value(g) for g in u.model_groups}
current_wounds = sum(group_wounds.values())
```

`group_wound_value(g)` liefert für homogene Gruppen `unit.wounds` — die Summe
bleibt also identisch zum alten `unit.wounds * count`. **`current_wounds` ändert
sich für homogene Gruppen-Einheiten nicht** (nur die interne Repräsentation).

### Lock + freie Wahl ergeben sich aus den Pools

Für eine Gruppe `gid` mit `pool = group_wounds[gid]` und `wval =
group_wound_value(group)`:

- **angeschlagenes Frontmodell vorhanden** ⇔ `pool % wval != 0` (Pool ist kein
  ganzzahliges Vielfaches der Modell-LP → ein Modell steht teilbeschädigt).
- **Lock aktiv** ⇔ irgendeine Gruppe hat `pool % wval != 0`. `get_locked_group`
  liefert deren `gid` (es kann pro Einheit höchstens **eine** angeschlagene
  Gruppe geben — der Lock verhindert ein zweites angeschlagenes Modell).
- **Freie Wahl** ⇔ keine Gruppe angeschlagen → Verteidiger wählt
  `damage_active_group_id`.

### Neue/erweiterte State-Felder (in der `units_key_for`-State der Einheit)

- `damage_active_group_id: str | None` — vom Verteidiger gewählte Zielgruppe für
  den nächsten Schaden. Persistiert zwischen Reruns bis zur nächsten Änderung.
- `group_wounds: dict[str, int]` — jetzt für alle Gruppen-Einheiten befüllt
  (kanonischer Per-Gruppen-HP-Pool).

## 3 Zustände der Subgruppen-Auswahl (UI — vom Stakeholder freigegeben)

### Zustand A — Freie Wahl (kein angeschlagenes Modell)

```
SCHADENSZUWEISUNG — Nobz          (Verteidiger wählt · Zustand wird gespeichert)
   Subgruppe            lebt   LP je Modell    Ausrüstung
   ────────────────────────────────────────────────────────────────
 ○ Nob – Power Klaw      2     ●●● ●●●         Power Klaw, Big Choppa
 ◉ Nob – 2× Kill Saw     2     ●●● ●●●         Kill Saw ×2
 ○ Nob – Slugga          1     ●●●             Slugga, Choppa
   ────────────────────────────────────────────────────────────────
   Schaden (2) →  [ Nob – 2× Kill Saw ▾ ]            [ Anwenden ]
```

### Zustand B — Gesperrt (angeschlagenes Modell, lebt noch)

```
SCHADENSZUWEISUNG — Nobz     ⚠ Angeschlagenes Modell zuerst abhandeln
   Subgruppe            lebt   LP je Modell
   ──────────────────────────────────────────────────────
   Nob – Power Klaw      2     ●●● ●●●     [—]  (gesperrt)
 ► Nob – 2× Kill Saw     2     ●●● ●○○     [▶]  ← 1 LP verbleibend
   Nob – Slugga          1     ●●●         [—]  (gesperrt)
   ──────────────────────────────────────────────────────
   Weiterer Schaden geht zwingend an:  Nob – 2× Kill Saw   [ Anwenden ]
```

### Zustand C — Modell zerstört (Lock fällt, freie Wahl zurück)

```
 ✕ Nob – 2× Kill Saw: 1 Modell zerstört  →  freie Wahl wiederhergestellt (Zustand A)
   (nur falls letztes Modell der Subgruppe:)
 ⚠ Subgruppe verloren — Kill Saw ×2 nicht mehr verfügbar
```

### Trivialer Fall (homogene Einheit, z. B. Warriors)

Eine Subgruppe → keine Auswahl sichtbar, Schaden geht automatisch dorthin. Die
Lock-Mechanik ist unsichtbar (es gibt nichts zu wählen). UI-Bedingung:
interaktives UI nur bei `len(aktive Subgruppen) > 1`.

## Commands you will need

| Zweck | Befehl | Erwartet |
|-------|--------|----------|
| venv | `source .venv/bin/activate` | `(.venv)` |
| Mutations-Tests | `python -m pytest tests/gameMechanic/test_unit_mutations.py -q` | grün |
| Gruppen-Tests | `python -m pytest tests/uiLayout/test_group_flow.py -q` | grün |
| State-Tests | `python -m pytest tests/gameMechanic/test_game_state.py -q` | grün |
| Vollsuite | `pytest --tb=short` | grün, ≥ 90 % |
| Lint | `ruff check src/ && black --check src/ && isort --check-only src/` | passt |
| App | `streamlit run src/app.py` | Port 8501 |

## Scope

**In scope**:
- `src/gameMechanic/game_state.py` — `_unit_state`: `group_wounds` für ALLE
  Gruppen-Einheiten befüllen (Vereinheitlichung).
- `src/gameMechanic/unit_mutations.py` — neue Funktionen
  `select_damage_target_group()`, `get_locked_group()`; `apply_damage` lenkt
  Schaden auf `damage_active_group_id` statt priority-spill; Lock-Check.
- `src/uiLayout/_common.py` — `_render_damage_block()`: Subgruppen-Auswahl
  (Zustand A/B/C) VOR dem Apply-Button; Mortal-Overflow korrekt weiterreichen.
- Tests: PFLICHT auf 4 Schichten (siehe Test plan).

**Out of scope** (NICHT anfassen):
- Lethal Hits Overflow → eigener Plan nach 014.
- Angreifer-seitige Sicht auf Verteidiger-Gruppen (bleibt verborgen).
- Morale-/Flee-Pfad (`fled_models_this_turn` ohne Gruppen-Reduktion — falls
  auffällig: NUR melden, nicht beheben).
- YAML-Daten — keine Änderungen.

## Regressionsfläche (HIGH RISK — vor Step 1 lesen)

Das Universell-Machen von `group_wounds` berührt **alle** heutigen Konsumenten.
Diese MÜSSEN nach Step 1 unverändert grün bleiben (oder bewusst angepasst +
getestet werden):

- `unit_mutations.unit_max_hp` (liest `group_wounds`)
- `unit_mutations._recompute_from_group_wounds`, `_front_group_hp`,
  `_apply_group_wound_damage`, `_heal_group_wounds` (Heal-Pfad!)
- `unit_mutations.heal_*` / Revive-Pfad (`_restore_group_models`)
- `src/uiLayout/unitCard.py:194` (`state.get("group_wounds")`)
- `src/uiLayout/_common.py:608+`, `:1061+`, `:1084+` (Anzeige der Pools)
- Szarekh/Menhir-Roster (gemischte Wundenwerte) — muss identisch funktionieren.

**Wenn ein vorher grüner Test rot wird, der NICHT in der erwarteten
Migrationsliste (Step 1) steht: STOP, Nutzer fragen.** (CLAUDE.md-Sicherheitsnetz.)

## Steps

### Step 1: `group_wounds` universell befüllen (`game_state.py`)

`_unit_state`: den `if u.has_per_group_wounds()`-Zweig so erweitern, dass
`group_wounds` für **jede** Einheit mit `model_groups` befüllt wird. Für
Einheiten ohne `model_groups` bleibt `group_wounds = {}` (uniformer Alt-Pfad).

**Erwartete Test-Migrationen** (diese dürfen sich ändern, alles andere = STOP):
- Tests in `test_game_state.py`, die `group_wounds == {}` für homogene
  Gruppen-Einheiten erwarteten → erwarten jetzt befüllte Pools.

**Verify**:
```
python -m pytest tests/gameMechanic/test_game_state.py tests/gameMechanic/test_unit_mutations.py -q
pytest --tb=short          # Szarekh/Menhir + alle Heal-/Damage-Tests grün
```
→ `current_wounds` für homogene Einheiten unverändert (Summe identisch).

### Step 2: Lock-Logik + gerichteter Schaden (`unit_mutations.py`)

Zwei neue Funktionen:

```python
def select_damage_target_group(uid: str, faction: str, group_id: str) -> None:
    """Defender's choice: set damage_active_group_id for the next application.
    Raises ValueError if group_id is not a known group of this unit."""

def get_locked_group(uid: str, faction: str) -> str | None:
    """Return the group_id whose front model is wounded-but-alive
    (group_wounds[gid] % group_wound_value != 0), or None if free choice."""
```

`apply_damage` (group_wounds-Pfad):
- Wenn `get_locked_group()` einen `gid` liefert UND `damage_active_group_id !=
  gid` → **ValueError** (UI verhindert das; Defensiv-Check für Tests/direkte
  Aufrufe).
- Schaden wird auf `damage_active_group_id`s Pool angewendet (nicht mehr
  priority-spill). Ist `damage_active_group_id` None und keine Sperre aktiv →
  Default = erste Gruppe nach `priority` (deterministisch, für direkte Aufrufe).
- `mortal=True`: Overflow über Gruppengrenzen bleibt erhalten, ignoriert den
  Lock (Regressionstest).
- Nach Anwendung `_recompute_from_group_wounds` (vorhanden) hält `group_models`
  / `models` / `destroyed` konsistent.

**Verify**: `python -m pytest tests/gameMechanic/test_unit_mutations.py -q` grün.

### Step 3: UI in `_common.py` — Auswahl VOR Apply-Button

In `_render_damage_block()`, VOR dem Apply-Button, NUR bei `len(aktive Gruppen)
> 1` (Gruppen mit `group_models[gid] > 0`):

- **Zustand A** (`get_locked_group() is None`): Auswahl (radio/selectbox) der
  aktiven Subgruppen; Key z. B. `dmg_target_grp_{tab_key}`; Default = erste nach
  `priority`; Caption je Option = Gruppenname + Waffennamen. Auswahl ruft
  `select_damage_target_group()` beim nächsten Apply.
- **Zustand B** (`get_locked_group()` liefert `gid`): alle Gruppen anzeigen,
  gesperrte hervorgehoben (`►`), andere `[—]`; verbleibende LP des Frontmodells
  (`group_wounds[gid] % wval`); Apply-Button nur auf die gesperrte Gruppe;
  Warntext „Angeschlagenes Modell muss zuerst abgehandelt werden."
- **Zustand C** (letzter Apply hatte `models_lost > 0`): Zerstörungsmeldung
  `✕ <Gruppenname>: <n> Modell(e) zerstört.`; wenn `group_models[gid] == 0`:
  `st.warning("Subgruppe verloren — <Waffenliste> nicht mehr verfügbar")`; danach
  freie Wahl (zurück zu Zustand A).

Pattern an `pending_target_request` (Plan 019) orientieren, sonst an
bestehenden `st.radio`-Patterns in `_common.py`.

**Verify**: bestehende Tests grün (UI-Erweiterung vor dem Button).

### Step 4: Tests (PFLICHT — 4 Schichten)

**Schicht 1 — Unit `tests/gameMechanic/test_unit_mutations.py`:**
- `test_select_damage_target_group_sets_state`
- `test_select_damage_target_group_invalid_group_raises`
- `test_get_locked_group_returns_none_when_no_wounded`
- `test_get_locked_group_returns_wounded_group` (Pool nicht ganzzahlig-Vielfaches)
- `test_lock_invariante_apply_damage_wrong_group_raises`
- `test_mortal_wound_overflow_ignores_lock` (Regression — Overflow über Grenzen)
- `test_homogeneous_unit_group_wounds_sum_unchanged` (current_wounds identisch)
- `test_single_group_unit_no_interactive_ui_needed` (`len(active)==1`)

**Schicht 1b — State `tests/gameMechanic/test_game_state.py`:**
- `test_group_wounds_populated_for_all_group_units`
- `test_mixed_wound_unit_group_wounds_unchanged` (Szarekh/Menhir-Regression)

**Schicht 2 — Acceptance `tests/uiLayout/test_group_flow.py`:**
- `test_zustand_a_b_c_transition_nobz`: Schaden auf Kill-Saw-Gruppe → Lock (B);
  weiterer Schaden zerstört Modell → C (Warnung); danach A (freie Wahl).
- `test_regressionstest_nobz_killsaw_group_destroyed`: Kill-Saw auf 0 →
  `group_models["kill_saw"] == 0`; Warnung enthält „Kill Saw".

**Schicht 3 — Architektur (bestehend):**
`pytest tests/architecture/ --no-cov -q` grün; kein neuer Fraktions-String:
`grep -rn "necron\|ork\|custodes" src/gameMechanic/unit_mutations.py` → leer.

**Schicht 4 — Manuelle UI-Verifikation (Nobz-Roster):**

| Schritt | Erwartetes Verhalten |
|---|---|
| Schaden auf Kill-Saw-Gruppe wählen | Zustand A zeigt Auswahl |
| Ersten Schaden anwenden (Modell lebt) | Lock → Zustand B; andere gesperrt |
| Weiteren Schaden anwenden (Modell stirbt) | Zustand C: Vernichtungsmeldung |
| Kill-Saw letztes Modell stirbt | Warnung „Kill Saw ×2 nicht mehr verfügbar" |
| Nächste Schadensrunde | Zustand A: freie Wahl zurück |
| Warriors (homogen) | keine Subgruppen-Auswahl |
| Szarekh + Menhirs | Pools unverändert, Schaden korrekt |

**Verify**: `pytest --tb=short` grün.

### Step 5: Vollsuite + Lint + Doku

- `pytest --tb=short` grün, Coverage ≥ 90 %; kein neuer uncovered Pfad.
- `ruff check src/ && black --check src/ && isort --check-only src/` passt.
- Abschlussbericht in `next_session.md`: manuelle Verifikationspunkte + Hinweis,
  dass `group_wounds` jetzt universell ist (Doku-Drift in `architecture.md` §
  session_state-Schema nachziehen lassen — backlog.md §4b).

## Test plan (Zusammenfassung)

| Test | Datei | Typ |
|---|---|---|
| `select_damage_target_group` Happy/Invalid | `test_unit_mutations.py` | Unit |
| `get_locked_group` none / wounded | `test_unit_mutations.py` | Unit |
| Lock-Invariante: falscher gid → ValueError | `test_unit_mutations.py` | Unit |
| Mortal-Overflow ignoriert Lock (Regression) | `test_unit_mutations.py` | Unit |
| Homogene Einheit: current_wounds unverändert | `test_unit_mutations.py` | Unit |
| Einzelgruppe: kein interaktives UI | `test_unit_mutations.py` | Unit |
| group_wounds universell befüllt | `test_game_state.py` | State |
| Szarekh/Menhir Pools unverändert (Regression) | `test_game_state.py` | State |
| Zustand A→B→C Transition (Nobz) | `test_group_flow.py` | AC |
| Kill-Saw-Gruppe zerstört → Warnung | `test_group_flow.py` | AC |
| Kein Fraktions-String in src/ | `tests/architecture/` | Architektur |
| Nobz-Roster alle 3 Zustände | manuell | Manuell |
| Warriors ohne UI / Szarekh-Pools | manuell | Manuell |

## Done criteria

ALLE müssen gelten:

- [ ] `group_wounds` für alle Gruppen-Einheiten befüllt; `current_wounds`
      homogener Einheiten unverändert (getestet)
- [ ] Szarekh/Menhir-Pfad unverändert grün (Regression)
- [ ] `select_damage_target_group()` + `get_locked_group()` implementiert + getestet
- [ ] Lock-Check in `apply_damage`: falscher `group_id` bei Lock → ValueError
- [ ] Mortal-Overflow ignoriert Lock korrekt (Regressionstest grün)
- [ ] Zustand A/B/C korrekt gerendert; `damage_active_group_id` persistiert
- [ ] Einzelgruppen-Einheiten: kein interaktives UI (`len > 1`)
- [ ] `pytest --tb=short` grün, Coverage ≥ 90 %; Lint sauber; Architektur-Gate grün
- [ ] Manuell verifiziert: Nobz alle 3 Zustände + Fähigkeitswarnung; Warriors
      ohne UI; Szarekh-Pools korrekt
- [ ] Status-Zeile in `docs/audit/plans/README.md` aktualisiert

## STOP conditions

- Plan 013 nicht DONE → STOP (falscher Ausgangszustand).
- Ein vorher grüner Test wird rot und steht NICHT in der erwarteten
  Migrationsliste (Step 1) → STOP, Nutzer fragen (CLAUDE.md-Sicherheitsnetz).
- Universell-Machen von `group_wounds` bricht den Heal-/Revive-Pfad strukturell
  (mehr als die erwarteten Anpassungen) → STOP, Neuabgleich.
- Lethal Hits Overflow wird für Korrektheit nötig → STOP, eigener Plan nach 014.

## Maintenance notes

- `select_damage_target_group` / `get_locked_group` sind UI-unabhängig — bei
  Undo/Redo ganzer Angriffe dieselben State-Felder nutzen.
- `group_wounds` ist nach diesem Plan der **einzige** kanonische Per-Gruppen-
  HP-Pool. Der alte uniforme `current_wounds`-Pfad bleibt nur für Einheiten
  OHNE `model_groups`. Mittelfristig prüfen, ob auch die letzten group-losen
  Einheiten Gruppen bekommen (dann ein einziger Pfad).
- Doku-Drift: `architecture.md` §session_state-Schema nennt `group_wounds` als
  Sonderfall — nach diesem Plan ist es Normalfall (backlog.md §4b).
