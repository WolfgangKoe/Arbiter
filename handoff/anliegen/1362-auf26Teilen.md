# AUF-26 teilen: Die Testdatei liegt über dem Höchstmaß

Form: Kritik
Von: Architekt
An: Planer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Die Akzeptanztests zu [AUF-26](../../domaene/anforderungen/phasen/aufstellen/anhaltenAnEinerBase.md)
(`technik/tests/akzeptanz/phasen/aufstellen/anhaltenAnEinerBaseTest.py`) haben mit Item
[anhaltenAnBases](../../domaene/items/anhaltenAnBases.md) 22.825 Zeichen, über dem Höchstmaß
20.000 einer Akzeptanztest-Datei. Nach [Kennzahlen](../../prozess/kennzahlen.md) wird daraus
ein Item bis zum Kürzungsmaß 12.000, darüber wird die Anforderung geteilt (eine Testdatei je
Anforderung, [Architektur, T1](../../technik/architektur.md)). Nach
[Ich 3](../../prozess/praemissen/ich.md) wartet das: keine Prüfung ist rot, das Kriterium
hat seinen Test. Die Zeichen je Kriterium: 26.1 rund 5.300, 26.2 rund 6.500, 26.3 rund 4.700,
26.4 rund 3.200, dazu 3.100 Tabellen der Züge. Räumt der Testautor die Hilfen auf
(Anliegen 1361), bleiben für 26.2 bis 26.4 noch über
12.000, ohne die Fälle aus Anliegen 1352.

**Kosten.** Bis zur Teilung wächst die Datei nicht; die Fälle aus 1352 brauchen die Teilung
oder warten. Wer einen Test zum Anhalten sucht, liest 600 Zeilen.

**Gegenvorschlag.** Ein Item im nächsten Plan, Umfang AUF-26: Der Anforderungsautor teilt
nach dem, was der Spieler erlebt, etwa
1. Hineinrücken in die *Aufstellungszone* (26.1),
2. ein *Modell* hält an einer *Base* an, auch beim Halten (26.2, 26.4),
3. der Block kürzt seinen Weg vor einer fremden *Base* (26.3);

danach folgen Testdateien und Prüfung `formregeln/spiegel.py` von selbst (T1). Den Schnitt
entscheidet die Domäne; die Kennungen bleiben, wenn die Domäne das so regelt.

**Stellungnahme.** Umgesetzt ohne eigenes Item: Der Anforderungsautor hat AUF-26 geteilt
(Anliegen 2090). AUF-26 hat nur noch 26.1 und 26.5, das Anhalten vor fremden *Bases* steht in
[AUF-29](../../domaene/anforderungen/phasen/aufstellen/anhaltenAufDemWeg.md).
`anhaltenAnEinerBaseTest.py` hat jetzt 8.243 Zeichen, unter dem Kürzungsmaß.
