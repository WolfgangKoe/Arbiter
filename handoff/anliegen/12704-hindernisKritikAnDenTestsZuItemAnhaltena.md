# Hindernis: Kritik an den Tests zu Item anhaltenAufDemWeg

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Diese Tests sind grün, bevor der Code besteht: testBew17_1EineBaseHinterDerBewegungsweiteLenktDasModellNichtAb. Mache sie rot oder nenne die Stelle, die das Kriterium schon erfüllt. Das hält den Schritt „Kritik an den Tests zu Item anhaltenAufDemWeg“ von Architekt im Fortschritt auf.

**Kosten.** Der Schritt bleibt offen, die Phase kommt nicht weiter.

**Gegenvorschlag.** Testautor beseitigt das Hindernis. Empfehlung: Nenne die Stelle, der Test
bleibt, wie er ist. Er ist der Fall „Base hinter der Bewegungsweite“ aus Anliegen 12682 und
prüft einen Fehler, den erst die Umsetzung brachte: Vor Commit 096dfed zeigte
`anteilBisZurBewegungsweite` in `technik/arbiter/domaene/phasen/bewegung/anhaltenAnDerBewegungsweite.py`
das *Modell* nach V16 an der *Bewegungsweite*, und ein Verschieben nach AUF-29.2 gab es noch
nicht. Am Commit-Stand (2054c5c) ist er rot, erprobt in einer Kopie in `/tmp`: Der Dienst
zeigt das *Modell* nach 29.2 seitlich verschoben.

**Stellungnahme.** Angenommen, der Test bleibt, wie er ist. Vor 096dfed erfüllte
`anteilBisZurBewegungsweite` in
`technik/arbiter/domaene/phasen/bewegung/anhaltenAnDerBewegungsweite.py` das Kriterium. Aufgerufen
wird es aus `_anteile` in `technik/arbiter/domaene/phasen/bewegung/__init__.py`. Es kürzte den
Weg auf den Teil bis zur *Bewegungsweite* (V16). Ein Verschieben nach AUF-29.2 gab es in der
*Bewegungsphase* noch nicht, also lenkte eine *Base* hinter der *Bewegungsweite* das *Modell*
nicht ab. Der Test prüft einen Fehler, den die Umsetzung brachte (Anliegen 12682). Nachgeprüft
in einer Kopie in `/tmp`, mit den Tests vom Stand HEAD: gegen den Produktstand 4d8ca81 (vor
096dfed) grün, gegen HEAD rot. Gezeigt wird dort (1,5″, 14,07″) statt (6,3″, 13,37″). Dass
Abhaken nachgereichte Tests am falschen Stand misst, steht in Anliegen 12900.
