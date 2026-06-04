# Startprompt — Nächste Session
<!-- Kanonische Planung. Nicht durch separate Plan-Dateien ersetzen — immer hier ergänzen. -->

## ⚠️ Session-Regeln (immer beachten)

**Zu Beginn jeder Session lesen:**
- `CLAUDE.md` — Workflow, Freigabe-Pflicht, **Unklarheiten IMMER zuerst fragen**, Branch-Strategie
- `docs/goals/ziel6.md` — aktueller Ziel-6-Stand

**Am Ende jeder Session:**
- `docs/goals/ziel6.md` aktualisieren: Checkboxen abhaken, neue Erkenntnisse ergänzen

---

## Was ist Arbiter?

**Arbiter** ist ein digitaler Spielbegleiter für Warhammer 40.000 9. Edition, gebaut in Streamlit (Python).
Starten: `streamlit run src/app.py` (Port fest: 8501)
Branch: `dev` (Entwicklung), `main` (stabiler Stand, nur per PR)

---

## Aktueller Stand (nach Session 12, 2026-06-04)

### Was funktioniert ✅
- Ziel 1–5 (Grundgerüst, Phasen, Setup, Daten) — vollständig
- Ziel 6a–6c, 6e, 6g, 6h — committed
- 6d-v2 Attackensequenz: Deklaration + Resolution-Tabs, Wound-Tabelle, RP-Block, Cover-Dropdown
- 461 Tests grün

### Was diese Session erledigt wurde ✅
- CLAUDE.md verschlankt: Flask entfernt, Arbiter-Projektkontext ergänzt, Freigabe-Regeln präzisiert
- Dead Code `_render_stratagem_hints()` aus `gameActionsArea.py` gelöscht
- Memory bereinigt: veraltete Flask/Ziel-3-Einträge entfernt
- `.claude/settings.json` verschlankt: von 55 spezifischen Einträgen auf 18 allgemeine Patterns

---

## Offene Aufgaben (priorisiert)

### AUFGABE 1 — Wahapedia-Daten lokal speichern (Voraussetzung für Aufgabe 2)

**Plan liegt vor, Freigabe noch ausstehend.** Permissions in `settings.json` sind bereits eingetragen.

Schritte (alle bereits beschrieben, warten auf „ja"):
1. `mkdir -p data/wahapedia_reference/necrons data/wahapedia_reference/orks`
2. `.venv/bin/python tools/wahapedia_scraper.py necrons --all > data/wahapedia_reference/necrons/units_all.txt`
3. `.venv/bin/python tools/wahapedia_scraper.py necrons --stratagems > data/wahapedia_reference/necrons/stratagems.txt`
4. Gleiches für Orks
5. Vergleichsreport `data/wahapedia_reference/VERIFICATION_REPORT.md` schreiben

**Ziel:** Daten lokal haben, um YAML-Fehler bei Einheiten (Silent King etc.) zu finden.

---

### AUFGABE 2 — Stratagems-Visibility Redesign (kritisch)

**Code-Review ist fertig** (aus Session 12). Ursachen sind vollständig verstanden:

**Bug A — `timing: phase_reactive` wird ignoriert:**
`stratagem_visibility()` liest das `timing`-Feld nie → reaktive GOs erscheinen immer wenn Phase + Stage passen.
Fix: `if stratagem.timing == "phase_reactive": return "hidden"` in `stratagem_visibility()`.

**Bug B — Nur aktive Fraktion geladen:**
`load_stratagems(faction_dir_for(active_faction))` lädt nur Necron-Stratagems, aber zeigt manche als "für Orks" an.
Fix: Beide Fraktionen laden, sauber filtern nach `player`.

**Bug C — Condition-Fallback zu permissiv:**
`_conditions_met()` ohne selected_unit → prüft alle Einheiten → fast immer True.
Fix: Kein Fallback. Ohne selected_unit + mit Conditions → hidden.

**Dateien die sich ändern:**
- `src/gameObjects/stratagem.py` — `stratagem_visibility()` um timing-Check erweitern
- `src/uiLayout/gameProtocoll.py` — `_conditions_met()` Fallback entfernen + beide Fraktionen laden

**Alle Änderungen gegen Wahapedia-Daten verifizieren** (erst Aufgabe 1 abschließen).

---

### AUFGABE 3 — Silent King + weitere Einheiten-Fähigkeiten (Datenproblem)

**Symptom:** Command-Phase-Fähigkeiten des Silent King (Will of the Triarch etc.) erscheinen nicht.
**Vermutung:** Einträge fehlen oder sind falsch in `data/wh40k_9e/necrons/unit_abilities.yaml`.
**Vorgehensweise:** Nach Aufgabe 1 gegen Wahapedia-Daten vergleichen → gezielte YAML-Korrekturen.
**Wahrscheinlich betrifft es weitere Einheiten** — nicht nur Silent King.

---

### AUFGABE 4 — Command Protocols regelkonform machen

**Problem:** Reihenfolge der Protokolle sollte vor Spielbeginn festgelegt werden (in Setup), nicht frei in jeder Befehlsphase wählbar. Außerdem: `active_directive` (primary/secondary) wird in `ability_engine.py` abgefragt, aber nirgends gesetzt.

**Dateien:**
- `src/gameMechanic/commandPhase.py` — `_render_command_protocols()` überarbeiten
- `src/uiLayout/gameActionsArea.py` — Setup-Phase um Protokoll-Reihenfolge erweitern

---

## Weitere offene Punkte (nachrangig)

| Punkt | Priorität |
|---|---|
| Weapon-Ability-Badges (Tesla, Dakka) im Hit-Block | mittel |
| Stratagem Reset-Button (reaktive GOs rückgängig) | mittel |
| `once_per_battle` enforcement | niedrig |
| subfaction_affinity UI | niedrig |
| load_powers() verdrahten (Psychic Phase) | niedrig |

---

## Wichtige Constraints (unverändert)

- **Freigabe vor Umsetzung** — Plan + Dateiliste zeigen, auf „ja" warten
- **Planergänzung ≠ Freigabe** — Plan neu zeigen, nochmal warten
- **Kein Memory/Subagent/Skill ohne Freigabe**
- dev-Branch, kein direktes Committen auf main
- Seitenleisten: first_player links, second_player rechts (unveränderlich)
- Keywords immer `UPPERCASE` in YAML
- `_parse_strength()` für Waffenstärke, nie `int(strength)` direkt

---

## Historische Sessions (Kurzfassung)

| Session | Datum | Inhalt |
|---|---|---|
| 1–5 | 2026-06-03/04 | Grundgerüst, Datenkorrektur, Fähigkeitssystem |
| 6–7 | 2026-06-04 | GO-Daten vollständig, render_attack_form neu (2-Spalten) |
| 8 | 2026-06-04 | Design 6d-v2 abgestimmt |
| 9–10 | 2026-06-04 | 6d-v2 Kern implementiert (Deklaration + Resolution + RP) |
| 11 | 2026-06-04 | Bug-Fixes: Scenario-KeyError, shot/fought-Flags, apply_damage(resolved), Stratagems-Hint entfernt |
| 12 | 2026-06-04 | CLAUDE.md + Memory + settings.json bereinigt; Stratagem-Bugs analysiert; Wahapedia-Plan vorbereitet |
