# Klick-Hilfen doppelt, ein Klick heißt Ziehen

1141 · Kritik · von Architekt → Testautor · Runde 1/3 · erledigt

## Runde 1
**Befund.** Kritik an den Tests zu Item setzenPerKlick. Nach Ich 3: Namen und Ablage von
Hilfsfunktionen ohne rote Prüfung, wartet.
1. `karteAnklicken(dienst, stelle)` steht gleich in
   [setzenPerKlickTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/setzenPerKlickTest.py)
   und [gesperrterKlickTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/gesperrterKlickTest.py),
   jede andere Anfrage nach V5 steht in [dienst.py](../../technik/tests/akzeptanz/dienst.py)
   ([Wir 3](../../prozess/praemissen/wir.md): genau einmal).
2. `mitDerMausKlicken` steht in beiden Dateien mit verschiedener Bedeutung: einmal nimmt es
   einen `Bildpunkt`, einmal eine `Stelle`.
3. `testAuf18_1EinKlickAufEinModellEinerAnderenEinheitSendetKeineAnfrage` klickt mit
   `ziehenOhneAnfrage(seite, modell, modell, eingabe)`: Ein Klick liest sich wie ein Zug.

**Kosten.** Wer die Route ändert, ändert zwei Dateien. Wer `mitDerMausKlicken` liest, muss
nachsehen, ob er Pixel oder Zoll übergibt. Mit Item einheitVerschieben kommt der Klick auf
ein *Modell* (V9) dazu, dann gibt es eine dritte Kopie.

**Gegenvorschlag.** `karteAnklicken` nach `dienst.py`. Klicken und Tippen auf die *Karte*
an einer *Stelle* einmal nach `auswahl.py` oder `ziehen.py` (Anliegen 550, Runde 2), mit dem
Namen der Eingabe wie `eingaben` in `ziehen.py`; für den Klick auf ein *Modell* ein Name ohne
„ziehen“ (etwa `klickenOhneAnfrage`). Günstig zusammen mit 1140 oder den Tests zu Item
einheitVerschieben. Erledigt, wenn jede Hilfe einmal steht und die Akzeptanztests wie vorher
laufen.

**Stellungnahme.** Angenommen.
1. `karteAnklicken` steht nur noch in [dienst.py](../../technik/tests/akzeptanz/dienst.py);
   `setzenPerKlickTest.py` und `gesperrterKlickTest.py` importieren es.
2. `mitDerMausKlicken`, `mitDemFingerTippen`, `klickenMit` und `mitMausUndFinger` stehen nur
   noch in [ziehen.py](../../technik/tests/akzeptanz/ziehen.py) und nehmen einen `Bildpunkt`.
   `gesperrterKlickTest.py` übergibt `punktAufDerKarte(seite, stelle)` wie die anderen Dateien.
3. Der Test mit `ziehenOhneAnfrage(seite, modell, modell, eingabe)` gibt es nicht mehr. Der
   Klick auf ein *Modell* läuft über `klickenMit[eingabe]`, `ziehenOhneAnfrage` bleibt bei
   echten Zügen. Ein Name wie `klickenOhneAnfrage` ist daher nicht nötig.

Die Akzeptanztests beider Dateien laufen grün wie vorher.
