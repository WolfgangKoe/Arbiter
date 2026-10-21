# Spiegel rot: Tests zu AUF-25.1 stehen hinter denen zu 25.2

1560 · Kritik · von Fachkritiker → Testautor · Runde 1/3 · erledigt

## Runde 1
**Befund.** Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): hält auf, denn eine
Prüfung ist rot. Hinter der Abnahme von Item einheitVerschieben steht also ein Hindernis.
`python3 -m pytest prozess/pruefungen/formregeln/spiegelTest.py` meldet:
`modellPerKlickTest.py: Zeile 205: AUF-25.1 nach AUF-25.2`. Die zwei Tests aus
[1300](1300-luekenTestsZuEinheitVerschieben.md),
`testAuf25_1NachDemZiehenDerEinheitIstDieEbeneDieGanzeEinheit` und
`testAuf25_1NachDemZiehenDesModellsDasDieEbeneIstBleibtEsDieEbene`, stehen in
[modellPerKlickTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/modellPerKlickTest.py)
hinter den Tests zu 25.2. Fachlich sind sie in Ordnung. Alle 622 Akzeptanztests sind grün,
die anderen Prüfungen in `prozess/pruefungen` auch.

**Kosten.** Solange der Spiegel rot ist, kann niemand committen und Item einheitVerschieben
nicht abnehmen. Die Behebung kostet nur das Verschieben von zwei Funktionen.

**Gegenvorschlag.** Die zwei Tests unverändert vor
`testAuf25_2EinKlickAufDasModellDerEbeneMachtWiederDieGanzeEinheitZurEbene` stellen, direkt
hinter die übrigen Tests zu 25.1. Erledigt, wenn `spiegelTest` grün ist und die
Akzeptanztests grün bleiben.

**Stellungnahme.** Angenommen. Die zwei Tests zu AUF-25.1 stehen unverändert direkt hinter den
übrigen Tests zu 25.1 und vor denen zu 25.2.

Nachgeprüft (Fachkritiker): in Ordnung. Die beiden Tests sind inhaltlich unverändert,
`spiegelTest` ist grün, alle 622 Akzeptanztests sind grün.
