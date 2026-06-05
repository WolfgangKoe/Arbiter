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

## Aktueller Stand (nach Session 16, 2026-06-05)

### Was funktioniert ✅
- Ziel 1–5 (Grundgerüst, Phasen, Setup, Daten) — vollständig
- Ziel 6a–6i — committed
- 6d-v2 Attackensequenz: Deklaration + Resolution-Tabs, Wound-Tabelle, RP-Block, Cover-Dropdown
- Weapon-Ability-Badges (Tesla, Dakka, Auto-Hit, Power Klaw) im Hit-Block
- Stratagem Undo-Button (CP-Erstattung + Modifier-Rollback)
- Auto-Advance: abgehandelte Einheiten rutschen ans Ende der Armeeliste
- 456 Tests grün

### Was Session 16 erledigt hat ✅
- Weapon-Ability-Badges im Hit-Block (Tesla, Dakka, Auto-Hit, Power Klaw)
- Stratagem Reset-Button (Undo mit CP-Erstattung)
- Auto-Advance in Armeeliste: `movement_chosen`-Flag + stabile Sortierung in `detachmentCard.py`
- Bugfix: `movement_choice == "stationary"` war Initialwert → `movement_chosen: bool` als separates Flag
- Skizzen für Attackensequenz-Redesign analysiert (Fotos/IMG_4038–4042)

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

## Nächste Session — AUFGABE 5: Attackensequenz-Redesign (Würfel-UI)

Design-Skizzen in `Fotos/IMG_4038–4042`. Ziel: visuelle Würfelfaces statt Text.

**Schritt 1 — Würfel-Komponente:**
- SVG-Würfelface für Werte 1–6, inline via `st.markdown(unsafe_allow_html=True)`
- Farbcodierung: grün (3+), gelb (4+), orange (5+), rot (6+), dunkelrot (immer miss)
- Highlight-Rahmen für aktive Schwelle
- Hilfsfunktion `dice_face_svg(value, color, highlighted) -> str`
- Hilfsfunktion `dice_row_html(threshold, stack) -> str` — rendert 2+…6+ als Reihe

**Schritt 2 — Treffer-Block neu:**
- Würfelreihe 2+…6+, aktive Schwelle highlighted + farbig
- Modifier verschieben den Highlight (nicht den Text)
- Badges darunter: MWBD, Tesla, Dakka, faction ability etc.

**Schritt 3 — Verwundungs-Block neu:**
- Dieselbe Würfelkomponente
- Nur aktive S-vs-T-Zeile anzeigen (nicht Tabelle)

**Schritt 4 — Rettungswurf-Block neu:**
- Rüstung + Invuln je als Würfelreihe
- AP und Cover als Modifier-Würfel die den Effektivwert zeigen

**Schritt 5 — Schaden-Block:**
- Würfel-Icon für Schadenswert (D3, D6 als Text im Würfel)
- FNP als Würfel-Icon
- `[−1][+1]` Buttons bleiben

Betroffene Dateien: `uiLayout/_common.py` (neue Hilfsfunktionen + Render-Blöcke ersetzen)

---

## Weitere offene Punkte (nachrangig)

| Punkt | Priorität |
|---|---|
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
