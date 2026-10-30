# Dienst wählt „ohne Ebene“: Name widerspricht Kriterium und Glossar

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Kritik an den Tests zu Item anhaltenUndAuswahl (Schnittstelle, Lesbarkeit).
Hält auf nach [Kritik](../../prozess/ablauf/kritik.md): ein Name, der das Gegenteil seines
Kriteriums sagt ([Es](../../prozess/praemissen/es.md), Lesbarkeit; [Wir 2](../../prozess/praemissen/wir.md)).

`testAuf30_1DerDienstWähltDieAufgestellteEinheitOhneEbene` in
[aufgestellteEinheitAuswaehlenTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/aufgestellteEinheitAuswaehlenTest.py)
prüft AUF-30.1: „ausgewählt mit der ganzen *Einheit* als *Ebene*“. Das
[Glossar](../../domaene/glossar.md) sagt: Jede *ausgewählte* *Einheit* hat eine *Ebene*.
„ohne Ebene“ meint hier nur, dass im Spielstand kein *Modell* `ebene` trägt
([Vertrag V1, Aufstellen · Auswahl](../../technik/architektur/vertrag/aufstellen/auswahl.md)).
Wer den Namen liest, versteht eine *Auswahl* ohne *Ebene*, die es nicht gibt; der Test der
Domäne daneben heißt richtig `…MitDerGanzenEinheitAlsEbene`.

Geprüft ohne weiteren Befund: Aufrufe nach V14, V16, V19 (`modellAnklicken`,
`stellenBeimLoslassen`, `karteAnklicken`), `übergehen=` benannt in BEW-2.8. Die Schleife in
`aufeinanderZuZiehen` und die zwei Quellen der *Bewegungsweite* stehen schon in Anliegen 7072.
Die Tests zu BEW-10 sind ohne neuen Code grün, weil `Schlacht.stellenBeimLoslassen` fremde
*Modelle* schon heute stehen lässt; sie prüfen echtes Verhalten.

**Kosten.** Ein Name, am Bildschirm nichts.

**Gegenvorschlag.** Umbenennen in
`testAuf30_1DerDienstWähltDieAufgestellteEinheitMitDerGanzenEinheitAlsEbene`; die Annahme
`ebenenIm(spielstand) == frozenset()` bleibt, sie zeigt im Spielstand genau das.

**Stellungnahme.** Umgesetzt wie vorgeschlagen: Der Test in
[aufgestellteEinheitAuswaehlenTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/aufgestellteEinheitAuswaehlenTest.py)
heißt jetzt `testAuf30_1DerDienstWähltDieAufgestellteEinheitMitDerGanzenEinheitAlsEbene`.
Die Prüfung `ebenenIm(spielstand) == frozenset()` bleibt unverändert. Sonst nennt niemand den
alten Namen.
