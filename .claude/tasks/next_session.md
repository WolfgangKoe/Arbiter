# Startprompt — Nächste Session
<!-- Kanonisch: .claude/tasks/next_session.md — nie ins Root-Verzeichnis anlegen. -->

## ⚠️ Session-Regeln (immer beachten)

**Zu Beginn jeder Session lesen:**
- `CLAUDE.md` — Workflow, Freigabe-Pflicht, **Unklarheiten IMMER zuerst fragen**
- `docs/goals/ziel6.md` — vollständige Aufgabenliste mit allen Checkboxen

**Am Ende jeder Session:**
- Checkboxen in `docs/goals/ziel6.md` abhaken
- Diese Datei aktualisieren: Stand + nächster Schritt + neue Erkenntnisse (ZUERST lesen, dann ergänzen)

---

## Was ist Arbiter?

**Arbiter** ist ein digitaler Spielbegleiter für Warhammer 40.000 9. Edition, gebaut in Streamlit (Python).
Start: `streamlit run src/app.py` (Port 8501)
Branch: `dev` (Entwicklung), `main` (stabiler Stand, nur per PR)

---

## Aktueller Stand (nach Session 20, 2026-06-06)

### Was funktioniert ✅
- Ziel 1–5 vollständig abgeschlossen
- Ziel 6a–6i (Basis) committed
- 6d-v3 Würfel-UI: Schwellenwert-Kopfzeile, Modifier-Paare, SAVE-Würfelreihen, 7+-Handling
- Cover: 3 phasengebundene Checkboxen (Dense → HIT, Light/Heavy → SAVE)
- Damage-Block: MW-Bedingung + Einzelmodell-Fix
- Fight Phase: beide Spieler alternieren korrekt; CHARGED-Priorität; inaktiver Spieler startet
- 456 Tests grün

### Session 18 (2026-06-06) ✅
- Regelrecherche: Resurrection Orb, WAAAGH!, Skarabäen → Ergebnisse in next_session.md
- 6d-v3 Würfel-UI Fixes: `threshold_header_html`, Modifier-Dimming-Fix, Blau für positive Mods, SAVE-Überarbeitung, 7+
- Cover: Dropdown → 3 Checkboxen + Phasenbindung + Dense nach HIT-Block
- Damage-Block: `has_mortal_wounds`-Flag + `is_single_model`-Fix

### Session 19 (2026-06-06) ✅
- Fight Phase Strukturfehler behoben: `fight_current_player` in `game_state.py`
- `can_fight_now()` + `_any_charged_remain()`: CHARGED-Priorität nach Regeltext
- `_advance_fight_turn_if_needed()`: automatischer Spielerwechsel + Auto-Skip
- `_render_fight_column()`: beide Spalten können aktiv sein (ersetzt `render_player_column`)

### Session 20 (2026-06-06) ✅
- 6d-v3 Würfel-UI Restfixes: Ausrichtungslinien (dashed/solid), Modifier-Richtung korrigiert, SAVE-Alignment
- Fight Phase Root Cause: `unitCard.py` `is_active` nutzte `st.session_state.active` statt `fight_current_player` → inaktiver Spieler konnte nie Einheiten für Angriff auswählen

### Session 21 (2026-06-07) ✅
- Heroic Intervention: Step-2-Timing (`charge_phase_step`), "All Charges Done →"-Button, CHARACTER-Check, HEROIC INT.-Badge, Feind-Zielauswahl via `pending_hi` + `hi_targets`
- Beobachtungen gesammelt: SAVE Würfel-Bug, HI GO-Extension, Gloom-Prism-Hardcodierung → in ziel6.md eingetragen

---

## Session-Start — Empfohlene Reihenfolge

1. Diese Datei + `docs/goals/ziel6.md` lesen
2. Schritt aus "Nächste Schritte" auswählen → Plan zeigen → Freigabe einholen

---

## Nächste Schritte (priorisiert)

### ✅ Schritt 1 — Regelrecherche (2026-06-06, erledigt)

### ✅ Schritt 2 — 6d-v3 Würfel-UI Fixes (2026-06-06)

- Schwellenwert-Zeile (`threshold_header_html`) über allen Würfelreihen
- Modifier-Paar: linker Würfel neutral, rechter farbig (kein miss-Dimming mehr)
- Positive Modifier-Farbe: blau (#3b82f6) statt grün
- SAVE: Würfelreihe für Rüstung + Invuln + Effective Save
- 7+/unmöglicher Save: grauer Würfelblock + rotes `×`-Marker

### ✅ Schritt 3 — Cover-Überarbeitung (2026-06-06)

- Dropdown → 3 separate Checkboxen (Dense/Light/Heavy)
- Phasenbindung: Dense+Light nur Shooting, Heavy nur Fight
- Dense Cover Checkbox direkt nach HIT-Block
- `_COVER_OPTIONS` Liste entfernt

### ✅ Schritt 4 — Damage-Block Fixes (2026-06-06)

- `has_mortal_wounds` in `_detect_weapon_special`: MW-Input nur wenn `"mortal wound"` in abilities
- `is_single_model = models_max ≤ 1`: kein Model-Counter, nur Wunden-Input

### ✅ Schritt 5 — Fight Phase (2026-06-06)

- `fight_current_player` State in `game_state.py` (init + reset)
- Inaktiver Spieler startet: `priority = second if active == first else first`
- Beide Spieler alternieren: `_advance_fight_turn_if_needed()` wechselt nach jedem Fight
- CHARGED-Priorität: `can_fight_now()` + `_any_charged_remain()` blockieren nicht-gechargede Einheiten
- Auto-Skip wenn ein Spieler keine eligible Units hat
- Counterattack GO (reaktive Unterbrechung) → Teil von 6e, noch offen

---

## Offene Tasks — Ziel 6 (Fokus nächste Session)

Kanonische Checkboxen: `docs/goals/ziel6.md § Testsession-Fixes`

### ✅ 6d-v3 Würfel-UI Restfixes — erledigt Session 20

- [x] Ausrichtungslinien: gestrichelte Linie nach Würfel 1, solide Linie vor Erfolgs-Frame
- [x] Modifier-Richtung: positive Modifier zeigen `[neuer Würfel] →+1→ [alter Würfel]` (MWBD: 2→3 ✓)
- [x] AP: negativer Wert → `←` Pfeil statt `→`
- [x] SAVE: Flex-Tabellen-Layout (Label-Spalte 68px, Würfelinhalt immer bündig)

### 🔴 HOCH — Nahkampf: Attacken auf Ziele verteilen, nicht Modelle (`uiLayout/_common.py` Declaration-Block)

**Bug:** Im Declaration-Block der Nahkampfphase kann der Spieler seine Attacken aktuell NUR auf Modelle eines Ziels verteilen. Regelkonform müssen Attacken auf **Zieleinheiten** verteilt werden — beliebig aufgeteilt. Ein Overlord mit 4 Attacken darf 2+2 auf zwei verschiedene Einheiten aufteilen.

- Hinweis: Der Declaration-Block wird ohnehin noch überarbeitet (6d-v3 Layout). Diesen Fix **im Zuge der Überarbeitung** umsetzen, nicht vorher als Einzelfix.
- Betrifft: `uiLayout/_common.py` → `render_attack_declaration()`, Fight-Phase-Integration

### 🔴 HOCH — Heroic Intervention (`gameMechanic/chargephase.py`, `game_state.py`)

### ✅ Heroic Intervention — erledigt Session 21

- [x] Step-2-Timing: `charge_phase_step` in `game_state.py`; "All Charges Done →"-Button
- [x] CHARACTER-Check korrekt; HEROIC INT.-Badge auf unitCard
- [x] Feind-Zielauswahl via `pending_hi` + `hi_targets` → `enter_melee()`
- [ ] **Offen:** GOs die Non-CHARACTER HI erlauben (z.B. `enslaved_protectors`) → HI-Eligibility erweiterbar machen

### 🟡 MITTEL — GOs in gameActionArea

- [ ] GO-Buttons kontextuell direkt in gameActionArea (aktiver + inaktiver Spieler), nicht als Liste
- [ ] Overwatch als reaktive GO in Charge Phase
- [ ] Counterattack GO in Fight Phase (reaktive Unterbrechung) — Teil von 6e

### 🟡 MITTEL — Necron Command Phase (`gameMechanic/commandPhase.py`, `uiLayout/armyCard.py`)

- [ ] Living Metal: einmalig pro Phase (aktuell mehrfach anwendbar)
- [ ] MWBD: nach erstmaligem Setzen in Command Phase zurücksetzbar
- [ ] Protokoll-Effekte auf Living Metal / RP-Verbesserungen abbilden (Interaktion fehlt)
- [ ] Dynastiebonus: wenn Direktive durch Dynastiezugehörigkeit gilt → Effekt anzeigen
- [ ] Anzeigereihenfolge: Regelkasten immer ganz oben in allen Phasen

### 🟡 MITTEL — WAAAGH!

- [ ] WAAAGH!-Badge auf unitCards der betroffenen Einheiten (alle ORKS — keine Ausnahmen laut Regeltext)

### 🟢 NIEDRIG — Moralphase

- [ ] Gretchin Cowardly: −1 auf Combat Attrition Tests wenn kein RUNTHERD in 6" (Ld 4)

### 🔴 HOCH — SAVE Würfel-UI Bugs (`uiLayout/_common.py`)

Befunde Session 21 (noch nicht implementiert):

- [ ] Grauer Miss-Würfel links vom Rahmen: muss `threshold − 1` zeigen (bei 6+ Save: Würfel-5, nicht Würfel-6)
- [ ] Modifier-Paare im SAVE-Block: beide Würfel zeigen `threshold − 1` des jeweiligen Zustands
  - Richtung: `Basis(neutral) ←-N← Effektiv(rot)` für AP; `Basis(neutral) →+N→ Effektiv(blau)` für Cover
  - Beispiel AP-2 auf 4+: `Würfel-3 ←-2← Würfel-5(rot)`
- [ ] Fähigkeit + AP kombiniert als eine Badge: z.B. `Enslaved AP-1` statt zwei separater Paare

### 🔴 HOCH — Psiphase: Gloom Prism hardcoded (`gameMechanic/psychicPhase.py:58`)

- [ ] `can_deny()` prüft `"gloom_prism" in u.rules` direkt — gehört in generisches Wargear-System
- [ ] Lösung: `deny: true`-Flag in `wargear.yaml`; `can_deny()` liest Wargear-Fähigkeiten generisch

### Nachrangig (Details in ziel6.md §6e–6h)

- [ ] Fight Phase Declaration-Block: noch nicht 6d-v3-Layout
- [ ] CP-Doppelvergabe-Fix + `collect_modifiers_for_phase()` (6e)
- [ ] Ability-Badges auf unitCard (6f)
- [ ] Nach Reset keine alten Einträge im Battle Log (6g)
- [ ] Hardcoded Fraktionslogik herauslösen (6h)

---

## Regelerkenntnisse (2026-06-06)

### Fight Phase — exakter Ablauf (core_rules.txt Z. 1941–1973)
- **Startet mit dem inaktiven Spieler** — beide Spieler wechseln sich ab beim Auswählen eligibler Einheiten
- **Charged Units Fight First:** Nicht-gechargede Einheiten erst wenn ALLE gechargeden Einheiten aller Spieler gekämpft haben
- Eligible = innerhalb Engagement Range ODER hat diese Runde einen Charge Move gemacht
- Wenn ein Spieler keine eligible Einheiten mehr hat, kämpft der andere alleine weiter
- Nach Consolidation können neue Einheiten eligible werden

### Heroic Intervention — Timing (core_rules.txt Z. 1824–1848)
- **Schritt 2 der Charge Phase** — erst NACHDEM alle Charges abgeschlossen sind
- Nur **CHARACTER**-Einheiten
- Bedingung: nicht in Engagement Range, aber ≤3" horizontal + ≤5" vertikal von einer feindlichen Einheit
- Bewegung: bis zu 3", muss näher zum nächsten feindlichen Modell enden

### Cover (core_rules.txt Z. 3791–3858)
- **Dense Cover:** −1 Trefferwurf bei Fernkampfwaffen (Terrain ≥3" hoch zwischen Schütze und Ziel) → gehört in HIT-Block
- **Light Cover:** +1 Rüstungswurf gegen Fernkampfwaffen — nur Shooting Phase
- **Heavy Cover:** +1 Rüstungswurf gegen Nahkampfwaffen, außer wenn Angreifer diese Runde charged — nur Fight Phase
- Alle drei können gleichzeitig aktiv sein → Dropdown falsch, Checkboxen nötig

### FNP (rules_appendix.txt Z. 2214–2219)
- Gilt für alle Wunden — normale UND tödliche Verwundungen
- Pro Wunde nur eine Ignore-Regel verwendbar

### Gretchin (units_all.txt Z. 417)
- **Cowardly:** −1 auf alle Combat Attrition Tests solange kein RUNTHERD in 6"
- Ld 4 — sehr niedrig, Tests schon bei kleinen Verlusten kritisch

---

## Regelerkenntnisse (2026-06-06, Session 18)

- **Resurrection Orb**: Keine KERN-Einschränkung — gilt für alle `<DYNASTY>`-Einheiten. Bedingung: nicht bei Starting Strength + RP noch nicht ausgelöst diese Phase. Einmalig pro Kampf. Aktuelle Implementierung ist korrekt (keine falsche KERN-Prüfung).
- **WAAAGH!**: Keine Einheiten-Ausnahmen — alle ORKS-Modelle profitieren (Stage 1: ORKS CORE+CHARACTER dürfen nach Advance chargen; alle ORKS: +1 Str/A, 5+/6+ Invuln). GRETCHIN-Ausnahme gilt nur für "Waaagh! Energy"-Zählung, nicht für WAAAGH! selbst.
- **Skarabäen**: Feeder Mandibles "Unmodified hit roll of 6 = auto-wounds." BEREITS in `data/wh40k_9e/necrons/weapons.yaml` als `abilities` Text. Kein Code-Feature nötig; nur als Abilities-Text angezeigt (gleich wie Tesla/Dakka).
- **Command Protocols 6. Protokoll**: Bereits in Session 17 gefixt ✅.

---

## Noch nachzuschlagen (vor Umsetzung der betroffenen Tasks)

_(leer — alle offenen Recherchepunkte abgearbeitet)_

---

## Wichtige Constraints (unveränderlich)

- **Freigabe vor Umsetzung** — Plan + Dateiliste zeigen, auf „ja" warten
- **Planergänzung ≠ Freigabe** — Plan neu zeigen, nochmal warten
- **Kein Memory/Subagent/Skill ohne Freigabe**
- dev-Branch, kein direktes Committen auf main
- Seitenleisten: `first_player` links, `second_player` rechts (unveränderlich)
- Keywords immer `UPPERCASE` in YAML
- `_parse_strength()` für Waffenstärke, nie `int(strength)` direkt
- Regelreferenz: Immer erst lokal nachschlagen (`docs/work/wahapedia_*/`), nie Nutzer fragen

---

## Historische Sessions

| Session | Datum | Inhalt |
|---|---|---|
| 1–5 | 2026-06-03/04 | Grundgerüst, Datenkorrektur, Fähigkeitssystem |
| 6–7 | 2026-06-04 | GO-Daten vollständig, render_attack_form neu (2-Spalten) |
| 8 | 2026-06-04 | Design 6d-v2 abgestimmt |
| 9–10 | 2026-06-04 | 6d-v2 Kern implementiert (Deklaration + Resolution + RP) |
| 11 | 2026-06-04 | Bug-Fixes: Scenario-KeyError, shot/fought-Flags, apply_damage(resolved), Stratagems-Hint |
| 12 | 2026-06-04 | CLAUDE.md + Memory bereinigt; Stratagem-Bugs; Wahapedia-Plan |
| 13–14 | 2026-06-04/05 | Wahapedia-Scraper, Daten-Review (Necrons/Orks), Custodes Ka'tah |
| 15–16 | 2026-06-05 | Weapon-Ability-Badges, Stratagem Undo, Auto-Advance, 6d-v3 Skizzen |
| 17 | 2026-06-06 | 6d-v3 SVG-Würfel-UI; Testsession: 21 Abweichungen + Regelrecherche |
| 18 | 2026-06-06 | 6d-v3 Fixes (Schwellenwert, Modifier, SAVE, 7+), Cover-Checkboxen, Damage-Block |
| 19 | 2026-06-06 | Fight Phase: beide Spieler alternieren, CHARGED-Priorität, fight_current_player |
