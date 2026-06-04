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

## Aktueller Stand (nach Session 13, 2026-06-04)

### Was funktioniert ✅
- Ziel 1–5 (Grundgerüst, Phasen, Setup, Daten) — vollständig
- Ziel 6a–6e, 6g, 6h — committed
- 6d-v2 Attackensequenz: Deklaration + Resolution-Tabs, Wound-Tabelle, RP-Block, Cover-Dropdown
- 461 Tests grün

### Was diese Session erledigt wurde ✅
- Wahapedia-Scraper: Truncation entfernt, alle Unit-Slugs (Necrons 67, Orks 80+, Custodes 33)
- Neues Tool `wahapedia_page_scraper.py`: faction_overview + Core Rules lokal gespeichert
- Stratagem-Visibility: 3 Bugs gefixt (phase_reactive, dual-faction load, condition fallback)
- Silent King: 8 fehlende Abilities in `unit_abilities.yaml` eingetragen
- Command Protocols: regelkonform (Setup-Zuweisung, Auto-Aktivierung, active_directive gesetzt)

---

## Offene Aufgaben (priorisiert)

### AUFGABE 1 — Wahapedia-Daten lokal (erledigt)

Gespeichert in `docs/work/`:
- `wahapedia_necrons/`: units_all.txt (67 Einheiten), stratagems.txt, faction_overview.txt (344K)
- `wahapedia_orks/`: units_all.txt (80+ Einheiten), stratagems.txt, faction_overview.txt (343K)
- `wahapedia_adeptus_custodes/`: units_all.txt (33 Einheiten), faction_overview.txt (262K)
- `wahapedia_core_rules/`: 6 Dateien (741K gesamt)

Noch offen: Vergleichsreport YAML vs. Wahapedia (weitere Einheiten nach Silent King)

---

### AUFGABE 2 — Stratagems-Visibility ✅ ERLEDIGT (fb5d39c)

---

### AUFGABE 3 — Einheiten-Abilities (laufend)

Silent King ✅ — 8 Abilities eingetragen (149029d)

Noch offen: Imotekh, Chronomancer, Plasmancer, Psychomancer, Lychguard, Flayed Ones,
Canoptek Wraiths u.v.m. — gegen `docs/work/wahapedia_necrons/units_all.txt` prüfen.

---

### AUFGABE 4 — Command Protocols ✅ ERLEDIGT (58ebc0b)

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
