NEEDS-DECISION

# Review S113 — Abschluss-Review (Reviewer-SA, Opus)

Ganzheitliches DoD-Review der Session S113. Read-only am Code. Kern: die Logik ist
regelkonform, generisch und voll getestet — aber die **UI-Render-Schicht** (coverage-
ausgeschlossen) hat zwei zusammenhängende Lücken im Undo-/Label-Pfad, die eine
Stakeholder-Entscheidung brauchen (Fix jetzt vs. als Backlog-Eintrag).

## DoD-Punkte 1–7

1. **Regelkonform — ERFÜLLT.** T2b: „once per battle" ist im Core-Glossar battle-scoped
   (z. B. `_shared/stratagems.yaml:104` Insane Bravery, rule_text „once per battle";
   `rules_appendix` bestätigt per-battle-Semantik). Das neue `used_stratagem_battle_ids`-Set
   überlebt Phasen-/Spieler-/Rundenwechsel → korrekt. T1: Direktiv-Befund korrekt zitiert —
   `faction_overview.txt` Z. ~574/579 belegt wörtlich „select which directive … at the start
   of each battle round" für BEIDE Direktiven (Haupt + Extra). Eintrag in `rules_insights.md`
   trifft den Text. Voice-of-the-Triarch-Ausnahme korrekt abgegrenzt (schaltet aktives
   Protokoll, nicht die Direktiv-Wahl).

2. **Generisch — ERFÜLLT.** Entscheidung hängt am `stratagem.once_per_battle`-Flag, das der
   Loader (`loader.py:638`) aus YAML liest — kein Fraktions-String in `src/`. grep: keine neuen
   Fraktions-Checks in den geänderten Dateien. INV-4b-Ratchet unverändert (11 Tokens — kein
   Anstieg).

3. **Tests grün — ERFÜLLT.** Selbst nachgemessen: `tests/gameObjects/` + `test_game_state.py`
   + `test_faction_abilities_orks.py` 146 passed. Architektur 8/8. Regressionstests decken das
   RICHTIGE Verhalten: battle-greyed über Phasenwechsel (`used_this_phase` leer, `used_in_battle`
   voll), Normal-Stratagem unberührt vom battle-Set, Legacy-Fallback (`used_in_battle=None`),
   und `_reset_phase_state()` lässt das battle-Set stehen. Gute Abdeckung der reinen Funktion.

4. **Architektur-Gate — ERFÜLLT.** 8/8 grün (selbst gemessen). Änderung ist additiv in
   gameObjects (Streamlit-frei) + UI-Schicht — keine Layer-Verletzung plausibel.

5. **Clean Code — ERFÜLLT.** `used_in_battle: set[str] | None = None` am Ende mit Default →
   abwärtskompatibel, Docstring erklärt das Warum. Type Hints vollständig, kein magischer String.
   Call-Site positional an 7. Stelle korrekt verdrahtet, einziger Aufrufer in `src/`.

6. **UI manuell verifiziert — OFFEN (Render-Code, nicht test-gedeckt).** Kein toter Code:
   echte once_per_battle-Stratagems existieren im Datensatz (Necron `stratagems.yaml`
   Z. 29/43/56/638/772; `_shared` Insane Bravery Z. 104; Orks). Mechanik ist am echten
   Datensatz aktiv. ABER zwei Render-Lücken (s. Blocker/Befunde) — manuelle Prüfung Pflicht.

7. **Artefakte — TEILWEISE.** `rules_insights.md` + Prio-1-Block sauber. **Drift NOCH OFFEN:**
   `next_session.md` Z. 54 nennt „Fix B WAAAGH! generisch — active_text-Feld im YAML fehlt noch"
   als offen, obwohl T2a belegt hat, dass active_text bereits geladen/gerendert wird und der
   Inhaltstest (S1+S2) grün ist. Muss im Abschluss korrigiert werden. `next_session.md` steht
   bei 77/120 Zeilen (Gate ok, aber Ziel ≤70 beim nächsten Reißen).

## Blocker / Befunde

**Kein harter Blocker** — die Logik ist korrekt und getestet. Zwei UI-Befunde zur Entscheidung:

**B1 (funktional, mittel) — Undo eines battle-Stratagems nach Phasenwechsel unmöglich.**
`gameProtocoll.py:193` zeigt den Undo-Button nur bei `strat.id in used_ids` (phase-scoped).
Wird ein once_per_battle-Stratagem in Phase X eingesetzt, ist es ab Phase X+1 zwar korrekt
greyed (via `used_battle_ids`), aber `used_ids` ist beim Phasenwechsel geleert → kein
Undo-Button mehr. Folge: Ein versehentlicher battle-Einsatz lässt sich nach Phasenende NICHT
mehr rückgängig machen (nur Spielreset hilft). Wurzel: Undo-Sichtbarkeit prüft nur das
phase-Set, nicht das battle-Set.

**B2 (Anzeige, klein) — irreführendes Label nach Phasenwechsel.** `gameProtocoll.py:185-189`:
Ein in einer Vorphase verbrauchtes once_per_battle-Stratagem ist greyed, fällt aber in den
`else`-Zweig und trägt das Label *(CP insufficient)* statt *(used)*, weil `strat.id in used_ids`
dann False ist. Falsche Begründung für den Spieler.

Beide haben dieselbe Wurzel: Render-/Undo-Pfad unterscheidet phase- vs. battle-scope nicht
(nur `stratagem_visibility()` tut das). Empfehlung: in beiden Stellen zusätzlich
`strat.id in used_battle_ids` berücksichtigen — kleiner, lokaler Fix in einer Datei.

**Entscheidung gefragt:** B1+B2 jetzt im Abschluss mitfixen (kleiner UI-Patch + manuelle
Prüfung), ODER als Backlog-Eintrag „once_per_battle UI: Undo/Label battle-scope" für eine
Folge-Session festhalten? (Reine Logik ist unabhängig davon korrekt.)

## Manuelle UI-Prüfliste (Render-Code, nicht test-gedeckt)

Mit echtem once_per_battle-Stratagem (z. B. Insane Bravery in Morale-Phase, oder ein Necron-
Stratagem):
1. Einsatz: Stratagem klicken → CP sinkt, Button wird *(used)*/greyed.
2. **Phasenwechsel weiter, dann zurückblättern/neue Phase:** Stratagem bleibt greyed (battle-
   scope hält) — der eigentliche Fix von S113.
3. **Spielerwechsel:** Beim Gegner-Zug bleibt das Stratagem ebenfalls battle-greyed.
4. **Undo im SELBEN Phasenfenster:** „↺ Rückgängig" gibt CP zurück und macht wieder clickable.
5. **Undo NACH Phasenwechsel (B1):** prüfen, ob ein Undo überhaupt noch angeboten wird — laut
   Code NICHT. Bewerten, ob das akzeptabel ist.
6. **Label-Text (B2):** greyed-once_per_battle in späterer Phase — zeigt es *(used)* oder
   irreführend *(CP insufficient)*?
7. **Spielreset:** Nach „Neues Spiel" ist das Stratagem wieder clickable (battle-Set geleert via
   `reset_game()`).

## Was der Abschluss noch nachziehen muss

1. **`next_session.md` Z. 54 Drift korrigieren:** „Fix B WAAAGH! generisch — active_text fehlt"
   ist erledigt (active_text geladen+gerendert, Test grün). Punkt 2(a) entfernen/als erledigt
   markieren; Prio 2 ggf. auf den verbleibenden Ziel6-Rest reduzieren.
2. **Entscheidung zu B1/B2** eintragen: entweder gefixt (+ manuelle Prüfung dokumentiert) oder
   neuer Backlog-Eintrag in `docs/goals/backlog.md`.
3. **Manuelle UI-Verifikation** (obige Liste) durchführen und Ergebnis vermerken — DoD-Punkt 6
   ist sonst nicht abgeschlossen.
4. `next_session.md` perspektivisch auf ≤70 Zeilen kürzen (aktuell 77, Gate 120 noch ok).
