STATUS: ANSWERED

**Entscheidung (Stakeholder, S130): Option (c) — nicht-blockierendes Inline-Wiring.**
Nach jedem regelerlaubten Wurf erscheint neben dem Wurfergebnis ein Inline-Button
`↻ Command Re-Roll (1 CP)` (kein Use/Pass-Dialog, Flow läuft weiter). Sichtbar nur wenn
CP ≥ 1, in dieser Phase noch nicht eingesetzt und der Wurf noch der letzte ist; Klick =
1 CP, Wurf ersetzen, Folgeberechnung ab dort neu. Umsetzung als eigener Auftrag (Effort M,
gesplittet nach Auftragsgrößen-Gate) nach Paket 2; Datei löschen, sobald umgesetzt.

# Command Re-Roll — reactive wiring deliberately deferred (S130, Plan 015)

**Lebensdauer:** temporär — löschen, sobald die Entscheidung getroffen und (falls "wire it")
umgesetzt ist, oder sobald R-CMD-12 explizit als dauerhaft-manuell dokumentiert wurde.

## Kontext

S130 setzte Plan 015 (reaktive Stratagem-UI) für 4 der 5 allgemeinen reaktiven Stratagems aus
`data/wh40k_9e/_shared/stratagems.yaml` um: **Fire Overwatch**, **Counter-Offensive**,
**Cut Them Down**, **Emergency Disembarkation** sind jetzt im richtigen Moment kontextuell
anwählbar (CP-Abzug, `used_stratagem_ids`/`used_stratagem_battle_ids`, `active_modifiers`).

**Command Re-Roll** bleibt wie zuvor unconditionally hidden (`stratagem_visibility()` mit
`reactive_trigger_active=False`, dem Default) — hier wurde bewusst NICHT gewired.

## Warum

Command Re-Roll (`event: after_roll`) triggert nach JEDEM Würfelwurf-Typ: Hit-, Wound-,
Damage-, Save-Wurf, Advance-Wurf, Charge-Wurf, Psychic Test, Deny the Witch, oder der
Anzahl-Attacken-Wurf (core_rules.txt Z. 3124-3130). Diese Wurf-Arten verteilen sich auf:

- `_common.py` (Hit/Wound/Save/Damage/Attacken-Wurf) — **im S130-Dateiscope**
- `chargephase.py` (Charge-Wurf), `movementPhase.py` (Advance-Wurf) — **im S130-Dateiscope**
- `psychicPhase.py` (Psychic Test, Deny the Witch) — **AUSSERHALB des S130-Dateiscopes**
  (Auftrag listete `psychicPhase.py` nicht unter den erlaubten Phase-Handlern)

Eine Teil-Wiring (nur die Wurf-Arten in den erlaubten Dateien) hätte eine inkonsistente UX
erzeugt: Command Re-Roll wäre nach einem Hit-Wurf anwählbar, aber nicht nach einem Deny-the-
Witch-Wurf — ohne erkennbaren Grund für den Spieler am Tisch.

Zusätzlich dokumentiert `docs/spec/acceptance/rules.md` R-CMD-12 bereits eine **bewusste,
getestete Entscheidung**: „als `phase_reactive` klassifiziert wird es in der UI nicht proaktiv
angeboten (reaktiver Einsatz nach einem Würfelwurf am Tisch)" — d.h. Command Re-Roll war schon
vor S130 als *dauerhaft manuell/table-tracked* eingestuft, nicht nur als „noch nicht gebaut".
Diesen Status ohne Rückfrage zu ändern hätte gegen die Freigabe-Pflicht verstoßen (S130-Auftrag
nannte Command Re-Roll zwar unter den „5 allgemeinen reaktiven Stratagems", aber die
Dateiliste schloss `psychicPhase.py` aus — ein Widerspruch, der laut Auftrag zu melden statt
still zu entscheiden ist).

## Entscheidungsfrage

Wie soll mit Command Re-Roll weiterverfahren werden?

**a) Vollständig wiren** — neuer Plan/Step, der `psychicPhase.py` mit ins Dateiscope aufnimmt,
   damit alle 9 Wurf-Arten konsistent abgedeckt sind. Aufwand: mittel (die generische
   Infrastruktur aus S130 — `reactive_stratagems_for`, `render_reactive_stratagem_box`,
   `spend_stratagem` — trägt bereits; es fehlen nur die Trigger-Hooks je Wurf-Stelle).

**b) Dauerhaft manuell belassen** — R-CMD-12 in `docs/spec/acceptance/rules.md` explizit auf
   „bewusst nicht App-verwaltet, Tisch-Tracking" umformulieren (Klasse bleibt A, da die
   *Klassifizierung* selbst App-Logik ist), damit künftige Sessions nicht wieder über denselben
   Punkt stolpern.

Rückfrage: Was bedeutet denn "vollständig verdrahten"? Ich stelle es mir so vor, dass man diese GO für jeden "erlaubten" Wurf (s. Regeln) einsetzen können sollte. Entsprechend muss diese auch in der Phase angezeigt werden. Jede GO kann zwar nur einmal pro Phase, aber dieses hier ja dann in jeder Phase eingesetzt werden, wo ein entsprechender Würfelwurf getätigt wird. Also "bewusst nicht App-verwaltet" wäre irgendwie falsch, aber wenn es bei jedem Klick in der App den Flow unterbricht, wäre es zu viel. Ich hoffe, du verstehst, was ich meine, und kommst mit einem guten Plan oder Vorschlag um die Ecke. Ansonsten frage mich nochmal. 

## Betroffene Dateien bei Option (a)

`src/gameMechanic/psychicPhase.py`, ggf. `src/uiLayout/_common.py` (Hit/Wound/Save/Damage-Rolls
sind dort schon instrumentiert für die anderen 4 Stratagems — Command Re-Roll bräuchte denselben
Trigger-Mechanismus, nur mit `event="after_roll"`).
