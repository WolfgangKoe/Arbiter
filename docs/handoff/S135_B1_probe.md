STATUS: NEEDS-DECISION

# S135 — B1 Scroll-Sprung: Probe-Patch zur Hypothesen-Verifikation

Bezug: B1 (Scroll-Sprung beim Ändern eines Command-Protocol-Slots im Setup),
`docs/goals/backlog.md` §2. Patch: `docs/handoff/S135_B1_probe.patch`
(NUR Diagnose — KEIN Fix, NICHT committen; Koordinator wendet ihn per
`git apply docs/handoff/S135_B1_probe.patch` an und nimmt ihn per
`git apply -R docs/handoff/S135_B1_probe.patch` wieder zurück).

## Hypothesen (3 Sätze)

**H1 (Fokus-Autoscroll):** Der Browser scrollt beim Rerun automatisch zum zuletzt
fokussierten Widget (der geänderten Selectbox), d. h. der Sprung entsteht
client-seitig durch Fokus-Wiederherstellung, unabhängig davon, was der Python-Code
in `session_state` schreibt. **H2 (DOM-Remount durch Sechsfach-Key-Rewrite):** Der
`on_change`-Callback `_swap_round_choice_slot` schreibt bei JEDER Slot-Änderung
alle sechs Widget-Keys (`proto_slot_<faction>_<slot>`) neu, was Streamlit als
Zustandsänderung aller sechs Selectboxes wertet und Teile des DOM neu aufbaut —
der Browser verliert dadurch die Scroll-Position. Der Patch schaltet exakt diesen
Sechsfach-Key-Rewrite ab (die Swap-Map `proto_slots_<faction>` wird weiterhin
gepflegt; einzige Probe-Nebenwirkung: der Partner-Slot eines Swaps zeigt bis zum
nächsten Rerun einen veralteten Anzeigewert — für den Scroll-Test irrelevant).

## Test-Ansage (zwei Stufen, exakt so ausführen)

**Stufe 1 — OHNE Patch (nur der B6-Stand aus dieser Session):**
App neu laden → Setup-Phase → einen Command-Protocol-Slot ändern
(einen der sechs Zuweisungs-Dropdowns, NICHT das „Read directive"-Dropdown)
→ **springt der Screen? Ja/Nein** notieren. - Ja. der Screen springt.

**Stufe 2 — MIT Patch (Koordinator wendet `S135_B1_probe.patch` an, App neu laden):**
gleicher Test: Setup-Phase → einen Command-Protocol-Slot ändern
→ **springt der Screen? Ja/Nein** notieren. 
Danach Patch zurücknehmen (`git apply -R`). - Wie wende ich den Patch an?

## Interpretationstabelle

| Stufe 1 (ohne Patch) | Stufe 2 (mit Patch) | Bedeutung |
|---|---|---|
| Ja | Nein | **H2 bestätigt** — der Sechsfach-Key-Rewrite ist die Ursache; Fix = Rewrite vermeiden/entschärfen (eigener Executor-Auftrag). |
| Ja | Ja | **H2 widerlegt** — Ursache ist H1 (Fokus-Autoscroll) oder etwas Drittes (z. B. Layout-Shift durch `st.columns`); nächster Schritt: H1-Probe (Fokus/Anchor-Verhalten). |
| Nein | — | B1 tritt auf dem neuen B6-Stand (Nebeneinander-Layout) gar nicht mehr auf — Stufe 2 entfällt, B1 als „durch B6 miterledigt" schließen (mit kurzer Beobachtungsnotiz). |
| Nein | Ja | Unerwartet (Probe verschlimmert) — Befund melden, keine der Hypothesen sauber bestätigt; neu analysieren. |

## Entscheidung erbeten

1. Stufe-1-Ergebnis (Ja/Nein), 2. falls nötig Stufe-2-Ergebnis (Ja/Nein) —
danach Fix-Auftrag gemäß Tabelle planen.
