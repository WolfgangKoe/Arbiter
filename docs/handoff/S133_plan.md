STATUS: ANSWERED

# S133 — Planungsentwurf v2 (Stakeholder-Kommentare eingearbeitet)

## Vorbemerkung Working Tree

Ungeprüfte K1/K4-Diffs (`_common.py`, `dice_html.py`, `go_card.py` + Tests). Task 1 konsumiert
sie: Marker prüfen (beide DONE), EINE Vollsuite als Baseline, manuelle UI-Checkliste (7 Punkte
next_session.md + 5 K1-Prüfpunkte), beide Handoffs löschen. K4-Folgekommentar ist jetzt fester
Task 7 (Stakeholder-Entscheid), damit ist der Handoff nach Task 1 konsumierbar.

## Neues Defekt-Paket S133-D (Screenshots Desperate-Breakout-GO-Karte, Orks)

1. **Button-Label:** Soll nur `Use` / `↺ Undo` (CP stehen im Header). Spec-Befund: `design_system.md`
   §6.1 (Z. 163/178–180) zeigt in den Mockups bereits das nackte `[Use]`, §6.4 verlangt aber die
   Familie `Use (N CP)` / `↺ Undo (+N CP)` — spec-interner Widerspruch. Stakeholder-Entscheid löst
   ihn Richtung §6.1; §6.4 wird im selben Task nachgezogen.
2. **Kein Inline-Offer:** Rule-Text, Number-Input, Confirm stehen losgelöst UNTER der Karte statt
   im Kartenrahmen. Bestätigt: `movementPhase.py:150-201` (`_render_desperate_breakout`) rendert
   `st.divider` + Widgets frei in den Phasen-Flow, nicht in der GO-Karte; §6.1-Mockup verlangt
   expandierten Inhalt innerhalb des Rahmens. Abweichung gegen Spec, kein Ermessensspielraum.
3. **Number-Input-Max + Einheitenbindung:** Code setzt `max_value=unit_state["models"]`
   (`movementPhase.py:181`) — Max 1 im Screenshot deutet auf falsche Einheitenbindung:
   `gameProtocoll.py:194` bucht auf `_selected_state_key_for(player)` (aktuell selektierte
   Einheit), ohne dass die Karte zeigt, WELCHE Einheit gemeint ist. Root Cause im Task verifizieren
   (Selektions-Key vs. `models`-Zählung bei Gruppen) + Einheit sichtbar machen.
4. **Aktivierungsbedingung (Regel belegt, `rules_appendix.txt:2618-2625`):** „Use this Stratagem in
   your Movement phase. Select one unit … that has not been selected to move this phase and which
   is in Engagement Range …" — Stakeholder-Vermutung bestätigt. Wirkung: 1 D6 je Modell, je 1 ein
   Modell zerstört; danach Fall Back durch Feindmodelle hindurch; Einheit kann diesen Zug NICHTS
   mehr (auch nicht mit Post-Fall-Back-Sonderregeln). Soll: Karte nur „bereit", wenn selektierte
   Einheit in ER + noch nicht bewegt; nach Anwendung Zustand „retreated" (deckt Code via
   `resolve_desperate_breakout` bereits ab — nur das Gating fehlt).

## Aufgabenliste + Parallelisierungs-Wellen

| # | Aufgabe | Effort | Tier | Token | Dateien (Kollisions-Check) |
|---|---|---|---|---|---|
| 1 | K1/K4 konsumieren (Vollsuite, UI-Checkliste, Handoffs löschen) | XS | Sonnet | ~10k | nur `docs/handoff/` |
| 2 | K3: `orks/stratagems.yaml` `[BOYZ, BEAST SNAGGA]` + Regressionstest | XS | Haiku | ~5k | `data/`, `tests/` |
| 3 | Beobachtung ④: doppeltes `""` Bewegungswert + Profilwert-Reihenfolge | XS–S | Sonnet | ~8k | Setup-/unitCard-Bereich |
| 4 | S133-D: Befunde 1–4 + Spec-Sync §6.4 | M | Sonnet | ~30k | `go_card.py`, `_common.py`, `movementPhase.py`, `gameProtocoll.py`, `design_system.md` |
| 5 | K2: Bewegungsphasen-Umbau (State-Modell lt. Entscheid, s. u.) | S–M | Sonnet | ~30k | `movementPhase.py`, `chargephase.py`, `_common.py` |
| 6 | Paket 3a: Reaktiv-Box → GO-Karte + mypy `_common.py` (75→64) | M | Sonnet | ~35k | `_common.py`, 3 Phase-Dateien, `mypy_gate.py` |
| 7 | K4-Umbau: Dakka an Attackenzuweisung (Default niedriger Wert, Max wenn alle in halber Reichweite; Badge raus). Regel: `wahapedia_orks/faction_overview.txt:626` | S | Sonnet | ~12k | `dice_html.py`, `_common.py` (Attackenzuweisung) |
| 8 | Paket 3b: `before_battle` in `PHASES` + ArmySetup-Liste | S | Sonnet | ~15k | `stratagem.py`/Setup-UI |

**Welle 1 (parallel):** Task 1 + Task 2 + Task 3 — disjunkte Dateimengen (Handoff/Daten/Setup-UI).
Parallele Vollsuiten unkritisch; jede Suite im Vordergrund, `run_in_background` VERBOTEN.
**Welle 2 (sequenziell — `_common.py`-Cluster kollidiert):** Task 4 → 5 → 6. Alle drei fassen
`_common.py` und Phase-Dateien an; keine Parallelisierung möglich.
**Welle 3 (parallel):** Task 7 + Task 8 — Dakka (`dice_html.py` + Attackenzuweisungs-Abschnitt)
vs. `before_battle` (Stratagem-Matching + Setup) sind disjunkt; Vorsicht: Task 7 berührt
`_common.py` — falls Task 8 doch dorthin oder nach `gameProtocoll.py` greift, sequenzialisieren.
Korridor-Regel: bei ~135k nach der laufenden Welle geordnet beenden; Welle 3 ist der erste
Verschiebe-Kandidat (→ S134).

## mypy-Baseline (Entscheid 3 eingearbeitet)

Kopplung an Task 6 (`_common.py`, 11 Fehler → Baseline 75→64), da dort ohnehin der größte Diff
entsteht; `tools/mypy_gate.py` im selben Commit senken (Ratchet). Fällt Welle 2 dem Korridor zum
Opfer: Fallback `movementPhase.py` (7 Fehler) an Task 5 koppeln.

## K2-Regelbefund + State-Modell (Entscheid 1 eingearbeitet)

`core_rules.txt:709-839`: außer ER = Normal/Advance/Stationary; in ER = nur Fall Back oder Remain
Stationary (Z. 724/739); Reinforcements als eigener Schritt NACH allen Bewegungen, im Ankunfts-Zug
keine Bewegungsart, zählen als „moved" (Z. 800-836). Stakeholder-Modell konform. Entscheid:
KEIN eigener Remain-Stationary-Pfad für in-melee — Hintergrund-Verhalten bleibt exakt; Retreat +
Reset („Stay Stationary") ⇒ wieder „stationary", „in melee"-Anzeige + vorige Abhängigkeit
wiederhergestellt; kein Übergang Retreated→Move/Advance.

## Stale Checks / Doku-Drift

ziel7.md gegen `git log --oneline -30`: Stufe-B-Häkchen durch `f6c464a`/`5827ea4` belegt — nicht
stale. Neu (S133-D Befund 1): §6.1↔§6.4-Widerspruch in `design_system.md`, wird in Task 4 bereinigt.

## Offene Entscheidungsfragen

Keine — Fragen 1–3 aus v1 sind entschieden und oben eingearbeitet. Einziger Vorbehalt: Task-8-
Dateiüberlappung mit Task 7 wird vor Welle 3 vom Koordinator per `git diff --stat` verifiziert.
