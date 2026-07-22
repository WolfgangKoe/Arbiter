STATUS: NEEDS-DECISION

# S178 — B-113 UI-Verifikation (Stakeholder) + Folge-Befunde

**Kontext:** B-113 (Reroll-Fähigkeiten verdrahten), umgesetzt in zwei Teil-Briefs —
A: Skorpekh-Destroyer Hit-Reroll (self, „Hardwired for Destruction"); B: Destroyer-Lord
Wound-Reroll-Aura (`reroll_wound_1`, `friendly_destroyer_cult_aura`) + Roster-Prep
(Skorpekh Lord in `necrons_test.yaml`). Verifikationsroster: `necrons_test.yaml`.

## Verifikationsergebnis: **POSITIV**

Manuelle Sichtprüfung (localhost:8501), Roster `necrons_test.yaml`:
- **HIT-Block (Brief A):** Reroll-Marker-Zeile (↺) unter Slot 1 erscheint beim
  Skorpekh-Destroyer-Angriff (Hardwired for Destruction). ✅
- **WOUND-Block (Brief B):** Reroll-Marker-Zeile (↺) unter Slot 1 erscheint, solange der
  Skorpekh Lord im Roster (Aura-Quelle) vorhanden/nicht zerstört ist; Gegenprobe (Lord
  entfernt/zerstört → Zeile verschwindet) bestätigt. ✅

Stakeholder-Wortlaut: „Der Befund ist positiv. […] Ansonsten gute Arbeit."

## Folge-Befunde (Stakeholder, zur Retro-Triage → Backlog-Items)

1. **Destroyer-Lord Hit-Reroll-von-1 fehlt.** Der Destroyer/Skorpekh Lord besitzt (laut
   Stakeholder) ebenfalls die Fähigkeit, einen **Treffer**wurf von 1 zu wiederholen — das ist
   aktuell nirgends verdrahtet. Regelrecherche (`docs/work/wahapedia_necrons/`) + Verdrahtung
   nötig (Lord-eigener Hit-Reroll, ggf. self analog Brief A). Fachlichkeit Ziel 7.

2. **Reroll-Marker-Farbe: Buff → Grün.** Die Reroll-Marker-Zeilen sind Buffs und müssen nach
   unserer Farb-Konvention **grün** eingefärbt sein (aktuell fixes Reroll-Orange,
   `_REROLL_COLOR` in `src/uiLayout/diceCompose.py`). Abgleich mit `docs/spec/design_colors.md`
   + `design_system.md` §4.3/§4.4; ggf. perspektiv-abhängig wie `always_fail_marker_row_html`
   (color_hint). Fachlichkeit Ziel 7 / Design.

3. **Aura-Reichweiten-Hinweis fehlt bei den normalen Zerstörern.** Die App misst keine
   Distanzen (bewusst) — muss aber **informieren**: bei den Destroyer-Cult-Einheiten ein
   Hinweis, dass der Wound-Reroll-von-1 nur gilt, wenn sie sich in der Aura eines Destroyer
   Lords (6″) befinden, damit der Nutzer es am Tisch prüfen kann. Klasse-B-Hinweis-Muster
   (st.info-Block, verwandt B-127 RP-Hinweise). Fachlichkeit Ziel 7.

## Stakeholder-Prozesswunsch

UI-Verifikationen sollen als Datei im Handoff dokumentiert werden (diese Datei erfüllt das
für S178). Abgrenzung zur transitory-Hygiene (DoD-7 + `test_handoff_hygiene`) in der Retro klären.
