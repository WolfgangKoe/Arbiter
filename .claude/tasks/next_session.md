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

## Aktueller Stand (nach Session 18, 2026-06-06)

### Was funktioniert ✅
- Ziel 1–5 vollständig abgeschlossen
- Ziel 6a–6i (Basis) committed
- 6d-v3 Würfel-UI vollständig: Schwellenwert-Kopfzeile, Modifier-Paare (korrekte Reihenfolge), 7+-Handling
- Cover: 3 phasengebundene Checkboxen (Dense nach HIT, Light/Heavy nach SAVE)
- Damage-Block: MW-Bedingung + Einzelmodell-Fix
- 456 Tests grün

### Session 18 (2026-06-06) ✅
- Regelrecherche: Resurrection Orb, WAAAGH!, Skarabäen → Ergebnisse in next_session.md
- 6d-v3 Würfel-UI Fixes: `threshold_header_html`, Modifier-Dimming-Fix, Blau für positive Mods, SAVE-Überarbeitung, 7+
- Cover: Dropdown → 3 Checkboxen + Phasenbindung + Dense nach HIT-Block
- Damage-Block: `has_mortal_wounds`-Flag + `is_single_model`-Fix

---

## Session-Start — Empfohlene Reihenfolge

1. Diese Datei + `docs/goals/ziel6.md` lesen
2. Regelrecherche (s.u.) erledigen — entsperrt mehrere Tasks
3. Schritt aus "Nächste Schritte" auswählen → Plan zeigen → Freigabe einholen

---

## Nächste Schritte (priorisiert)

### Schritt 1 — Regelrecherche (~15 min, vor allem anderen)

Lokale Wahapedia-Dateien lesen, Ergebnisse in diese Datei eintragen:

- `docs/work/wahapedia_necrons/` → Resurrection Orb (KERN-Einschränkung?), Command Protocols (6. Protokoll Setup-Zeitpunkt, Dynastiebonus, Effekte auf Living Metal/RP), Skarabäen (6=auto-wound)
- `docs/work/wahapedia_orks/` → WAAAGH! (welche Einheiten ausgenommen?)

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

### Schritt 5 — Fight Phase (eigene Session, komplex)

Struktureller Regelfehler — inaktiver Spieler kämpft mit, CHARGED-Reihenfolge.
Betrifft `gameMechanic/fightPhase.py` + `game_state.py`. Braucht detaillierten Plan.

---

## Offene Tasks — Ziel 6 (Fokus nächste Session)

Kanonische Checkboxen: `docs/goals/ziel6.md § Testsession-Fixes`
Hier stehen die Tasks mit Beobachtungsdetail als Kontext.

### 🔴 KRITISCH — Fight Phase (`gameMechanic/fightPhase.py`, `game_state.py`)

- [ ] Inaktiver Spieler kann in Fight Phase Einheiten auswählen und kämpfen (aktuell geblockt)
- [ ] `charged` / `in_melee` / `fought` als separate Flags korrekt setzen und auswerten
- [ ] Ablauf 9E: zuerst alle CHARGED-Einheiten aller Spieler → dann abwechselnd (Startspieler: inaktiv)
- [ ] Counterattack GO einsetzbar (reaktive Unterbrechung)

### 🔴 HOCH — 6d-v3 Würfel-UI Fixes (`uiLayout/_common.py`)

**HIT + WOUND:**
- [ ] Schwellenwert-Zeile über Würfeln: `2+  3+  4+  5+  6+`, aktive Schwelle mit Rahmen hervorgehoben
- [ ] Senkrechte Ausrichtungslinie bei aktiver Schwelle (durchgezogen); gestrichelte Linie zwischen Würfel 1 (immer miss) und Würfel 2
- [ ] Modifier-Reihenfolge: linker Würfel = Ausgangsschwelle, rechter = neue Schwelle (aktuell vertauscht)
- [ ] MWBD-Farbe: **blau** (wie unitCard-Badges), nicht grün

**SAVE:**
- [ ] Waagerechte Schwellenwert-Reihe + senkrechte Ausrichtungslinie (wie HIT/WOUND)
- [ ] Vertikales Alignment: Würfelreihen und Modifier-Effekte tabellenartig ausgerichtet
- [ ] Effective Save als Würfelreihe mit farbigem Rahmen (kein statischer Zahlenwert)
- [ ] Invuln-Zeile: ebenfalls Schwellenwert-Reihe + senkrechte Linie nötig

**7+ / unmöglicher Save:**
- [ ] Roter `[×]`-Würfel rechts neben 6er-Würfel wenn Schwelle 7+ (z.B. Gretchin, Warboss)
- [ ] Effective Save 7+: 6 rote `[×]`-Würfel statt Zahlenwert

### 🟡 HOCH — Damage-Block (`uiLayout/_common.py`)

- [ ] Mortal Wounds: Eingabe nur anzeigen wenn Waffe MW-Fähigkeit hat (aktuell immer sichtbar)
- [ ] Einzelmodell-Einheit (z.B. Warboss): nur Wunden-Eingabe, kein Modellverlust-Counter

### 🟡 HOCH — Heroic Intervention (`gameMechanic/chargePhase.py`, `game_state.py`)

- [ ] Intervene-Button erst sichtbar nach erfolgreichem Charge (Step 2 Charge Phase, nicht bei Zielauswahl)
- [ ] Nur CHARACTER-Einheiten dürfen intervenieren — Prüfung fehlt
- [ ] INTERVENED-Badge auf unitCard; `in_melee`-Ergänzung korrekt
- [ ] Intervention = Charge-Bewegung: Spieler wählt welche feindlichen Einheiten in Engagement Range landen

### 🟡 MITTEL — Cover-Überarbeitung (`uiLayout/_common.py`)

- [ ] Dropdown → Checkboxen/Buttons (mehrere Cover-Typen gleichzeitig möglich — Entweder-Oder ist regelfalsch)
- [ ] Phasenbindung: Dense + Light Cover → nur Shooting Phase; Heavy Cover → nur Fight Phase
- [ ] Dense Cover in HIT-Block verschieben (−1 Trefferwurf), nicht im Save-Block
- [ ] Heavy Cover: Effekt korrekt anzeigen; erscheint fälschlicherweise in gegnerischer Phase

### 🟡 MITTEL — GOs in gameActionArea

- [ ] GO-Buttons kontextuell direkt in gameActionArea (aktiver + inaktiver Spieler), nicht als Liste unten
- [ ] Overwatch als reaktive GO in Charge Phase

### 🟡 MITTEL — Necron Command Phase (`gameMechanic/commandPhase.py`, `uiLayout/armyCard.py`)

- [ ] Living Metal: einmalig pro Phase (aktuell mehrfach anwendbar)
- [ ] 6. Protokoll: einmalig im Setup für das gesamte Spiel festgelegt (nicht jede Runde neu wählbar)
- [ ] Protokoll-Effekte auf Living Metal / RP-Verbesserungen abbilden (Interaktion fehlt)
- [ ] Dynastiebonus: wenn Direktive durch Dynastiezugehörigkeit gilt → Effekt anzeigen
- [ ] Anzeigereihenfolge: Regelkasten immer ganz oben in allen Phasen

### 🟡 MITTEL — WAAAGH! + Sonstiges

- [ ] WAAAGH!-Badge auf unitCards der betroffenen Einheiten
- [ ] Ork-Regeln prüfen: welche Einheiten ausgenommen? → unitCard-Logik anpassen
- [ ] Resurrection Orb: Regel lesen (nur KERN-Einheiten?) → Implementierung prüfen
- [ ] Skarabäen: 6=auto-wound — YAML-Lücke oder Code fehlt?

### 🟢 NIEDRIG — Moralphase

- [ ] Gretchin Cowardly: −1 auf Combat Attrition Tests wenn kein RUNTHERD in 6" (Ld 4 — kritisch!)

### Weitere offene Tasks (nachrangig — Details in ziel6.md §6e–6h)

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
