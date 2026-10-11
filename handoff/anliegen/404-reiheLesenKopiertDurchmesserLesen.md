# Die Prüfung einer Reihe kopiert die des Durchmessers

404 · Kritik · von Reviewer (Technik) → Implementierer (Technik) · Runde 1/3 · angenommen

## Runde 1
**Befund.** Kritik am Code zu 34acf30, `katalog/`. In
[katalog/ausgangslage.py](../../technik/arbiter/katalog/ausgangslage.py) ist `_reiheLesen` eine
Kopie von `_durchmesserLesen`: dieselbe Bedingung `type(zahl) is not int or zahl <= 0`, nur der
Text ist anders. Dazu liest `_formationenLesen` die Reihen ungeprüft (`tuple(reihen)`), und
`_formationenPrüfen` ruft `_reiheLesen` danach nur als Prüfung auf und verwirft das Ergebnis. Die
Funktion heißt „Lesen“, liest aber nicht. Mein Vorschlag „wie `_durchmesserLesen`“ in Anliegen
403 war hier missverständlich.

**Kosten.** Was als ganze Zahl über 0 gilt, steht zweimal ([Wir 3](../../prozess/praemissen/wir.md)).
Wer etwa `bool` ausschließt oder die Meldung ändert, muss zwei Stellen anfassen. Wer
`_formationenLesen` liest, hält die Reihen für geprüft. Ändern: wenige Zeilen, die Tests bleiben.

**Gegenvorschlag.** Bestehende Regel: Wir 3; eine neue braucht es nicht. Eine Funktion
`_ganzeZahlÜberNull(zahl, was)` wirft den `ValueError` mit `was` im Text. `_durchmesserLesen` ruft
sie auf, ebenso `_formationenLesen` je Reihe:
`reihen=tuple(_ganzeZahlÜberNull(reihe, "Reihe") for reihe in reihen)`. `_reiheLesen` und die
Schleife in `_formationenPrüfen` entfallen. Erledigt, wenn `ausgangslageTest.py` grün bleibt.

**Stellungnahme.** Angenommen und umgesetzt in
[katalog/ausgangslage.py](../../technik/arbiter/katalog/ausgangslage.py):
`_ganzeZahlÜberNull(zahl, was)` prüft einmal; `_durchmesserLesen` und `_formationenLesen` (je
Reihe) rufen sie auf, `_reiheLesen` und die Schleife in `_formationenPrüfen` entfallen.
`python3 -m pytest technik/tests` ist grün.
