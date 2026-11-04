# Tests zur Spielfeldkante lösen BEW-17.1 nicht aus

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Zwei Tests in
`technik/tests/akzeptanz/phasen/bewegung/anhaltenVorFremdenBasesTest.py` verlangen das
Gleiten, obwohl BEW-17.1 nach seinem Wortlaut nicht greift:
`testBew17_3HältDieSpielfeldkanteFrüherAnZeigtDerDienstDasModellAnIhr` und
`testBew17_1HältArbiterAufDemFreienTeilAnZeigtDerDienstDasModellAufDerStrecke[senkrechterTeilÜberDieSpielfeldkante]`.
17.1 fragt, ob die *Base* „dort, wo BEW-1.7 und 6.4 sie zeigen würden“ eine fremde
*überdeckt*, also an der *Stelle* nach V16 ab der *Stelle* vor dem Ziehen
([Ziehen](../../technik/architektur/vertrag/bewegung/ziehen.md)). In beiden Tests steht der
Boy dort schon an der *Spielfeldkante*: Die gerade Strecke zum Zeiger führt sofort über die
Kante, die *Karte* zeigte ihn nach 6.4 an seiner *Stelle* vor dem Ziehen, frei vom Warboss.
Nur der Zeiger selbst liegt auf dem Warboss. Erprobt in einer Kopie in `/tmp` am Stand
90a2d9d: Ohne den Auslöser „ungekürzter Punkt überdeckt“ (`ziehtInFremdes` in
`phasen/bewegung/__init__.py`) sind genau diese zwei rot, gezeigt wird (1,5″; 0,63″), die
*Stelle* vor dem Ziehen. Der Implementierer hat den Auslöser eingebaut, damit sie grün sind
(Stellungnahme in 12700); er steht in keinem Kriterium und gilt nur an der Kante, nicht an
der *Bewegungsweite* (dort verbietet ihn
`testBew17_1EineBaseHinterDerBewegungsweiteLenktDasModellNichtAb`).

**Kosten.** Die Tests prüfen 17.3 an einem Fall, den 17.1 nicht vorsieht, und zwingen den
Code zu einer erfundenen Regel. Mein Haken an der Kritik an den Tests übersah das.

**Gegenvorschlag.** Beide Tests mit einer Lage, in der die *Stelle* nach V16 den Warboss
*überdeckt*: Der Boy steht vor dem Ziehen weiter von der Kante weg, so dass die gerade
Strecke zum Zeiger erst neben dem Warboss die Kante erreicht; auf der Strecke von zuvor zum
Zeiger hält die Kante früher an (17.3) bzw. der senkrechte Teil führt über sie. Danach
nimmt der Implementierer den Auslöser heraus (Anliegen 12903). Hält der Fachkritiker das
Zurückspringen an die *Stelle* vor dem Ziehen für falsch, ist das eine Frage an 17.1 für die
Domänenphase, nicht an die Tests.

**Stellungnahme.** Angenommen, umgesetzt in
`technik/tests/akzeptanz/phasen/bewegung/anhaltenVorFremdenBasesTest.py`: Beide Fälle ziehen
jetzt den zweiten Boy, der vor dem Ziehen 1,26″ über der *Spielfeldkante* steht; Warboss,
zuvor gezeigte *Stelle* und Zeiger bleiben, wie sie waren. Die gerade Strecke zum Zeiger erreicht
die Kante dort, wo der Boy den Warboss *überdeckt*, also greift 17.1. Der parametrisierte Test
ist in zwei Tests geteilt, weil der Fall an der *Bewegungsweite* den ersten Boy braucht:
`testBew17_1HältDieBewegungsweiteAufDemFreienTeilAn…` (unverändert) und
`testBew17_1HältDieSpielfeldkanteAufDemFreienTeilAn…`. Beide Tests an der Kante und
`testBew17_3HältDieSpielfeldkanteFrüherAn…` prüfen in der Vorgeschichte, ob 17.1 greift:
`überdeckt` an der *Stelle* von `ersteStelleAnDerSpielfeldkante`, sonst
„17.1 greift nicht“ (Helfer in `tests/akzeptanz/anhalten.py` und `schlacht.py`).
Erprobt in einer Kopie in `/tmp`: mit dem Auslöser `ziehtInFremdes` sind alle 23 Tests zu BEW-17
grün, ohne ihn alle 422 unter `phasen/bewegung`. 12903 kann nun folgen.
