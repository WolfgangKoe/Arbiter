# V3 nennt ganzeEinheitAlsEbene als Tür der Aufstellung, der Code hat sie nur in Auswahl

Form: Kritik
Von: Reviewer
An: Architekt
Runde: 1/3
Status: offen
Wartet auf: Technikphase

## Runde 1
**Befund.** Kritik am Code zu Item einheitZuruecklegen (Commit „Item einheitZuruecklegen
gebaut, 3080 angenommen, 2740 wartet auf 3120“, `git show 479569a`). Der Code hält den
Vertrag in V5 bis V7: `zurücklegen` nimmt jedes *gesetzte* *Modell* der *Einheit in
Aufstellung* von der *Karte*, lässt *an der Reihe* gleich, macht eine *ausgewählte* *Einheit*
ganz zur *Ebene* und tut ohne *Einheit in Aufstellung* nichts, ohne *Grund* (AUF-23.1, 23.3,
23.5); die Seite bietet „Einheit zurücklegen“ vor „Aufstellen der Einheit beenden“ nur mit
`einheitInAufstellung` an (AUF-23.4). Alle Prüfungen grün: `pytest technik/tests` 655,
`pytest prozess/pruefungen` 771, Mutation der geänderten Zeilen 30 von 30 gefangen,
SonarLint und eslint ohne Fund.

Eine Abweichung: [Vertrag, V3](../../technik/architektur/vertrag.md) zählt
`ganzeEinheitAlsEbene(einheit)` zur Tür `Aufstellung` („die Tür ist `Aufstellung`: …“).
Gebaut ist sie nur in
[auswahl.py](../../technik/arbiter/domaene/phasen/aufstellen/auswahl.py) als
`Auswahl.ganzeEinheitAlsEbene`; `Aufstellung` ruft sie in `zurücklegen` und bietet sie selbst
nicht an. Das ist richtig so: Eine Tür ohne Aufrufer wäre toter Code (vulture), und
[Handlungen, V5](../../technik/architektur/handlungen.md) sagt schon, dass `zurücklegen` sie
ruft. Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): wartet (Ablage einer
Hilfsfunktion, keine Prüfung rot, kein Schritt des Happy Path betroffen).

**Kosten.** Wer nach V3 `aufstellung.ganzeEinheitAlsEbene(…)` aufruft, etwa der Testautor in
einem Akzeptanztest, findet die Methode nicht und baut eine Tür nach, die niemand braucht.
Eine Zeile im Vertrag, am Code nichts.

**Gegenvorschlag.** In V3 `ganzeEinheitAlsEbene(einheit)` aus der Liste der Tür nehmen und
als Methode von `Auswahl` nennen, die nur `zurücklegen` ruft (V5). Bestehende Regel
([Ich 4](../../prozess/praemissen/ich.md)): V3 selbst, keine neue.

Erledigt, wenn V3 die Methode nicht mehr als Tür der `Aufstellung` nennt.

**Stellungnahme.**
