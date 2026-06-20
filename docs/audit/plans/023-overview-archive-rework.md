# Plan 023 — Overview-/Session-Archiv-Rework

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in "STOP conditions" occurs, stop and report — do not
> improvise. When done, update the status row in `docs/audit/plans/README.md`.
>
> **Drift check (run first)**:
> `grep -n "_render_subagents\|_render_subagent_archive\|subagent_archive" tools/token_report.py`
> Erwartet: beide Render-Funktionen + `_ARCHIVE_FILE = .../subagent_archive.json`
> vorhanden. Wenn `_render_session_archive` o. Ä. bereits existiert → STOP,
> unbekannte Drift melden.

## Status

- **Priority**: P0 (HÖCHSTE — Stakeholder zieht vor 022, 2026-06-21)
- **Effort**: M
- **Risk**: MEDIUM (reiner Tooling-/Report-Code, kein Spiel-/Render-Pfad;
  aber Schema-Migration der Archiv-JSON)
- **Depends on**: —
- **Category**: refactor + bugfix (S72-Duplikat-Tabellen) + feature (Archiv-Auslagerung)
- **Planned at**: 2026-06-21

## Why this matters

`docs/metrics/overview.md` ist heute **zu lang und dupliziert**: `render_markdown`
schreibt ZWEI breite Subagent-Tabellen in dieselbe Datei — `_render_subagents`
("## Subagenten — wer wurde wofür gestartet") und `_render_subagent_archive`
("## Subagent-Archiv (je Session)"). Das ist der S72-Befund, der den Stakeholder
beim Lesen stört. Konzept-Vorlage: `Refinement/overview_concept.md`.

Ziel (Stakeholder-Entscheid 2026-06-21):
1. **Auslagern:** Die akkumulierte Sessions-Historie wandert in eine **separate,
   auto-generierte** Datei `docs/metrics/session_archive.md`. `overview.md` bleibt
   kurz und verlinkt nur darauf.
2. **Dedup:** Der Generator wird pro Session mehrfach angestoßen → derselbe
   Session-Eintrag darf **nie doppelt** ins Archiv. Idempotent je Session-ID.
   (Datenpfad-Dedup existiert bereits in `merge_session_into_archive`; auf das
   neue, session-weite Schema erweitern.)
3. **Auto:** Beides entsteht über `python tools/token_report.py --write` (läuft
   im pytest-Hook). Keine Handpflege. Anzahl der Auslösungen wird NICHT
   dokumentiert (Stakeholder 2026-06-21).

## Ziel-Layout (verbindlich)

### `overview.md` — Reihenfolge exakt nach Konzept (Restruktur)

1. Header (`# Token-Report — Effizienz statt Menge`, Stand, Korridor-Intro) — unverändert
2. `## Verlauf (letzte 6 Sessions)` — heutiges `_render_history`, **an den Anfang**
3. `## Jüngste Session` — heutiges `_render_focus`, aber **nur** der Stats-Block
   (Aufgabe/Modelle/Tokens/Peak/cache_read). Heading „Fokus: letzte Session" →
   „Jüngste Session".
4. `## (Retro-)Hinweise` — heutiges `_render_hints`, Heading umbenannt.
5. `## 150k-Korridor für Subagenten` — heutiges `_render_subagent_corridor`,
   Heading umbenannt (nur jüngste Session).
6. `## Zusammensetzung der Antworten` — der Balken-Block **+ Legende**, aus
   `_render_focus` **herausgelöst** in einen eigenen Renderer.
7. `## Vergangene Sessions` — **nur ein Link**:
   `→ vollständige Historie: [session_archive.md](session_archive.md)`
8. `Σ über N Sessions: …` — unverändert.

**Entfällt komplett aus overview.md:** `_render_subagents` (breite Tabelle) und
die in-line `_render_subagent_archive`-Tabelle.

### `session_archive.md` — NEUE separate Datei (auto, dedup, wachsend)

Block „Vergangene Sessions" nach Konzept §„Vergangene Sessions": je Session eine
Hauptzeile (Label · Peak-Balken+Status+Trend · Subagent-Anteil · Modell-Mix),
darunter **Inline-Subzeilen** je Subagent (`SA_1·  30k ✅  <Aufgabe>`), Sessions
durch `---`-Trenner separiert, jüngste zuerst.

```text
# Session-Archiv

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: <ts>

Jüngste zuerst. Akkumuliert über alle Sessions (dedup je Session-ID).
Modell-Mix: `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix
----------------- ---------------------- -------------- ------------
06-20 11:42 7e13  ██████████░░ 131k ✅↓  ██░░░░  30% ↓  ████████····
         SA_1·    ██░░░░░░░░░░  30k ✅    Fix setup-phase a…
         SA_2·    ███░░░░░░░░░  41k ✅    Generic-src quick…
----------------- ---------------------- -------------- ------------
06-20 11:04 5abd  ███████████░ 138k ✅↓  ██░░░░  35% ↑  ████████····
…
```
```

## Datenmodell — Archiv-JSON erweitern

Heute: `subagent_archive.json` = `{session_id: [subagent_records]}` (nur Subagenten).
Für die Hauptzeilen fehlen Peak/Anteil/Mix. **Schema auf session-weit erweitern**
und Datei umbenennen → `docs/metrics/session_archive.json`:

```json
{
  "<session_id>": {
    "started_at": "2026-06-20T11:42:…",
    "task": "start next session",
    "peak_context": 131000,
    "subagent_share": 30.0,
    "by_tier": {"opus": 8345688, "sonnet": 3587245},
    "subagents": [
      {"agent_type": "general-purpose", "description": "…",
       "tier": "sonnet", "peak_context": 30000}
    ]
  }
}
```

- **Dedup:** `merge_session_into_archive` schreibt `updated[session_id] = {…}`
  (Upsert) — mehrfaches `--write` je Session ist idempotent.
- **Rückwärtskompatibilität (Migration):** `load_session_archive` erkennt das
  alte Listen-Format (`value` ist `list`) und hüllt es in
  `{"subagents": value, "started_at": <aus erstem Record>, "peak_context": null,
   "subagent_share": null, "by_tier": {}, "task": null}`. Fehlende Hauptzeilen-
  Werte → Render zeigt `—` / leere Balken. So geht nichts verloren.

## Affected files

- `tools/token_report.py` — Render-Reihenfolge, neue Renderer, Schema, main()
- `docs/metrics/overview.md` — wird neu generiert (kein Handgriff)
- `docs/metrics/session_archive.md` — **neu**, generiert
- `docs/metrics/session_archive.json` — **neu** (ersetzt `subagent_archive.json`;
  Migration aus Altdatei beim ersten Lauf)
- `tests/tools/test_token_report.py` — neue/angepasste Tests

## Steps

### Step 1: Renderer aufteilen + umbenennen (overview.md-Struktur)

In `tools/token_report.py`:
- `_render_focus` aufteilen: Stats-Block bleibt (Heading → „## Jüngste Session"),
  Balken+Legende in neuen `_render_composition(session)` (Heading
  „## Zusammensetzung der Antworten") auslagern.
- `_render_hints`: Heading „## Hinweise" → „## (Retro-)Hinweise".
- `_render_subagent_corridor`: Heading → „## 150k-Korridor für Subagenten".
- `render_markdown`: Reihenfolge gemäß Ziel-Layout; `_render_subagents` und
  `_render_subagent_archive` **aus overview.md entfernen**, durch Link-Abschnitt
  „## Vergangene Sessions" ersetzen.

**Verify:** `python -m pytest tests/tools/test_token_report.py -q` (zunächst evtl.
rot wegen Heading-Asserts — in Step 4 mitziehen). Kein `## Subagenten — wer wurde
wofür gestartet` mehr in `render_markdown`-Output.

### Step 2: Archiv-Schema session-weit + Migration

- `load_subagent_archive` → `load_session_archive` (neuer Pfad
  `_ARCHIVE_FILE = docs/metrics/session_archive.json`); Alt-Listen-Format migrieren.
- `merge_session_into_archive`: speichert jetzt das **volle** Session-Dict
  (started_at, task, peak_context, subagent_share, by_tier, subagents). Upsert
  je session_id (Dedup bleibt).
- `save_subagent_archive` → `save_session_archive`.
- Einmalige Migration: liegt nur `subagent_archive.json` vor, beim ersten `--write`
  einlesen, ins neue Schema heben, als `session_archive.json` schreiben. Altdatei
  **nicht** löschen (Sicherheitsnetz; Stakeholder entscheidet später).

### Step 3: `session_archive.md` rendern + schreiben

- Neuer `render_session_archive_md(archive, *, generated_at)` → vollständiges
  Markdown wie Ziel-Layout (Hauptzeile + SA-Subzeilen + `---`-Trenner, jüngste
  zuerst). Wiederverwendung von `bar`, `model_mix_bar`, `_short_label`,
  `_context_status`, `trend`.
- `main()`: nach overview.md zusätzlich `session_archive.md` schreiben
  (`_ARCHIVE_MD = docs/metrics/session_archive.md`).

### Step 4: Tests (PFLICHT — Sicherheitsnetz)

`tests/tools/test_token_report.py` erweitern:

| Test | Prüft |
|------|-------|
| `test_overview_has_no_wide_subagent_table` | `## Subagenten — wer wurde wofür gestartet` NICHT in overview-Output |
| `test_overview_section_order` | Reihenfolge Verlauf→Jüngste→Hinweise→Korridor→Zusammensetzung→Vergangene |
| `test_overview_links_to_session_archive` | overview enthält Link `session_archive.md` |
| `test_composition_section_present` | „## Zusammensetzung der Antworten" + 4 Balken |
| `test_session_archive_md_has_main_and_sa_rows` | Archiv-MD: Hauptzeile + `SA_1` Subzeile |
| `test_merge_session_idempotent` | zweimal dieselbe session_id → genau 1 Eintrag |
| `test_load_archive_migrates_old_list_schema` | altes `{sid: [list]}` → neues Dict-Schema |

**Verify:** `python -m pytest tests/tools/test_token_report.py -q` grün.

### Step 5: Vollsuite + Lint + Doku + Backlog

- `pytest --tb=short` grün, Coverage ≥ 90 %.
- `ruff check tools/ && black --check tools/ && isort --check-only tools/` passt.
- `python tools/token_report.py --write` ausführen → overview.md kurz + neue
  session_archive.md erzeugt; **manuell sichten** (Stakeholder-Abnahme).
- Backlog-Eintrag (`docs/goals/backlog.md` ~Z. 171) auf ✅ setzen + kurzer Verweis.
- Statuszeile in `docs/audit/plans/README.md` aktualisieren.

## Test plan (Pflicht-Tests)

Siehe Step-4-Tabelle. Jeder ist HTML-/Text-Output-orientiert (Render-Code → der
Generator IST hier die Business-Logik und wird direkt getestet, nicht
ausgeschlossen — `token_report.py` ist Tool-Code, kein Streamlit-Render).

## Done criteria

ALLE müssen gelten:

- [ ] overview.md folgt Ziel-Layout, keine breite Subagent-Tabelle mehr
- [ ] „Zusammensetzung der Antworten" eigener Abschnitt
- [ ] overview.md verlinkt auf session_archive.md
- [ ] session_archive.md wird auto generiert (Hauptzeile + SA-Subzeilen, dedup)
- [ ] Schema-Migration aus altem subagent_archive.json verlustfrei
- [ ] mehrfaches `--write` je Session bleibt idempotent (Dedup-Test grün)
- [ ] `pytest --tb=short` grün, Coverage ≥ 90 %
- [ ] Lint sauber (ruff/black/isort)
- [ ] Backlog + plans/README aktualisiert

## STOP conditions

- Migration verliert Subagent-Daten aus der Altdatei → STOP, nicht überschreiben,
  melden.
- Vorher grüne Tests werden rot, die NICHT zu erwartenden Heading-/Struktur-
  Änderungen gehören → STOP, Nutzer fragen (war das Verhalten gewollt?).
- session_archive.md würde > ~400 Zeilen pro Lauf (unbegrenztes Wachstum ohne
  Rotation) → Scope-Frage an Stakeholder (Rotations-Policy nötig?).

## Maintenance notes

- `Refinement/overview_concept.md` ist die Layout-Vorlage; bei Abweichung gilt das
  Konzept, außer bewusste Entscheidung mit Kommentar.
- Das JSON-Archiv ist die Datenquelle, die `.md`-Dateien sind reine Sichten —
  niemals von Hand pflegen.
- Wenn das Archiv zu groß wird: separater Rotations-Plan (analog
  `tools/rotate_history.py`), nicht hier.
