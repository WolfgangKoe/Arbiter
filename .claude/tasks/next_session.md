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

## Aktueller Stand (nach Session 15, 2026-06-05)

### Was funktioniert ✅
- Ziel 1–5 (Grundgerüst, Phasen, Setup, Daten) — vollständig
- Ziel 6a–6e, 6g, 6h — committed
- 6d-v2 Attackensequenz: Deklaration + Resolution-Tabs, Wound-Tabelle, RP-Block, Cover-Dropdown
- AUFGABE 2 ✅: alle hardcodierten Fraktionsreferenzen entfernt
- AUFGABE 3 ✅: 6. Protokoll + Dynastiebonus implementiert
- 456 Tests grün

### Was diese Session erledigt wurde ✅
- Pending-Commit von Session 14: shot/fought-Flags, resolved damage, scenario mapping, weapon multiselect
- AUFGABE 2 komplett: `_OVERLORD_ID` → Keyword-Check, `is_necron_faction()` gelöscht,
  `resurrection_orb_used` aus init, `auto_round_1` aus Code (YAML war bereits sauber),
  Protocol-Assignment Range 1–5, `_render_command_protocols` aus commandPhase.py entfernt
- AUFGABE 3 Bug 2: `_get_extra_protocol_id` + `_render_extra_protocol` + auto-activate aus Assignments
- AUFGABE 3 Bug 3: `dynasty`-Feld in Roster-YAML + `p1/p2_dynasty` in session state
- AUFGABE 1 Necrons: Tesseract Ark Waffen korrigiert (C'tan-Powers particle_hurricane/seismic_lash/solar_fire)
- AUFGABE 1 Necrons: Waffen-Profile verifiziert (Chronomancer ✅, Doomstalker ✅, Wound-Tracks ✅)
- AUFGABE 1 Orks: Aktive Roster-Einheiten ergänzt (Warboss Mega Armour, Big Mek, Warbikers)

---

## Offene Aufgaben (priorisiert)

### AUFGABE 1 — Datengrundlage vollständig fixen (laufend)

**Necrons ✅ weitgehend erledigt:**
- Waffen verifiziert, Wound-Tracks korrekt
- Noch offen: weitere Einheiten nach Bedarf

**Orks — aktive Roster-Einheiten ergänzt ✅:**
- Noch offen: 71 weitere Einheiten haben fehlende Abilities (niedrig-prio, nach Bedarf ergänzen)

**Custodes — kein aktiver Roster:**
- Noch kein `unit_abilities.yaml` — erst anlegen wenn Custodes-Roster erstellt wird

---

### AUFGABE 2 ✅ ERLEDIGT (2026-06-05, Commit 564deb8)

---

### AUFGABE 3 ✅ ERLEDIGT (2026-06-05, Commits 42b49ce + 2cd8357)

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
