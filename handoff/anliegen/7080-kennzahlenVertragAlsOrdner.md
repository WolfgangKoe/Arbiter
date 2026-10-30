# Kennzahlen: Architektur ohne Summe, Vertrag einer Phase als Ordner

Form: Kritik
Von: Architekt
An: Organisationsentwickler
Runde: 1/3
Status: offen
Wartet auf: Prozessphase

## Runde 1
**Befund.** Zwei Entscheidungen des Stakeholders ändern denselben Satz der
[Kennzahlen](../../prozess/kennzahlen.md#höchstmaße), Höchstmaße der Architektur:
1. [7022](7022-vertragEinerPhaseUeberDemHoechstmass.md) F1 A: Eine volle Vertragsdatei wird
   ein Ordner, darin je Abschnitt eine Datei zu 6.000, ohne Summe. Umgesetzt für die
   *Aufstellung*, die *Schlacht* und die *Bewegungsphase*: `technik/architektur/vertrag/aufstellen/`,
   `…/schlacht/`, `…/bewegung/` ([Übersicht](../../technik/architektur.md#schichten)). Die
   Kennzahlen sagen noch „Vertrag je Phase eine Datei … zu je 6.000“.
2. Anliegen 7090 F1, Antwort: „Wir machen erst A und dann B. Ich möchte dass Redundanzen
   reduziert werden.“ A ist umgesetzt: Die Regeln der Architektur sind gekürzt, ohne
   Wiederholung, und haben zusammen rund 23.000 Zeichen. B: Die Summe von 24.000 für die
   Regeln fällt, je Datei bleiben 6.000, wie beim Vertrag.

Einordnung: wartet, kein Schritt des Happy Path hängt daran; die Regeln liegen unter der
Summe, die Messung im Dashboard (`rollenregeln/architekturMessung.py`) zählt die Unterordner
schon mit und prüft keine Summe.

**Kosten.** Bleibt der Satz, liest eine Rolle „eine Datei je Phase“ und legt die Ordner
wieder zusammen (Anliegen 5000), und die nächste Regel der Architektur stößt an eine Summe,
die der Stakeholder abgeschafft hat. Umsetzen: ein Satz, kein Mechanismus.

**Gegenvorschlag.** In den Kennzahlen ersetzt den Teil ab „Architektur:“ bis „(Anliegen
2570);“: „Architektur: Regeln (`technik/architektur.md` und je Datei in
`technik/architektur/`) je 6.000, ohne Summe (Anliegen 159, 211, 7090); Vertrag je Phase
eine Datei in `technik/architektur/vertrag/` zu je 6.000; wird sie voll, ein Ordner gleichen
Namens mit je Abschnitt einer Datei zu je 6.000; ohne Summe (Anliegen 2570, 7022);“

**Stellungnahme.**
