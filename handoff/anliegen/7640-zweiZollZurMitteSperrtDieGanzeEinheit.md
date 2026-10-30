# Zwei Zoll zur Mitte sperrt die ganze Einheit

Form: Kritik
Von: Fachkritiker
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Kritik an den Tests zu Item grenzkreise. Hält auf nach
[Kritik](../../prozess/ablauf/kritik.md) („ein Test prüft sein Kriterium nicht“):

1. `zweiZollZurMitte` in [grenzen.py](../../technik/tests/akzeptanz/grenzen.py) zieht 2″ quer
   zur Reihe zur Mitte. Mit der ganzen *Einheit* als *Ebene* stößt die Reihe dabei auf die
   zweite *Einheit* desselben *Spielers*, 2,5″ daneben (Warboss, Overlord; die Reihen legt
   `stellenDerEinheit` in [handgriffe.py](../../technik/tests/akzeptanz/handgriffe.py) an).
   Arbiter sperrt richtig nach BEW-2.5 und QUE-1, gelaufen:
   `Sperre: Base überdeckt, über eine Base` (wie der grüne
   `testBew2_5IstDieGanzeEinheitEbeneGiltDieBaseEinerAnderenEinheitAlsFremd`). Diese 13 Fälle
   werden darum nie grün, auch wenn das Produkt richtig ist:
   `testBew11_5NachDemZiehenBleibtDieEinhüllendeAnDenStellenZuBeginnDerBewegungsphase` (2),
   `testBew13_2NachDemZiehenBleibtDieGrenzeDesWurfsAnDenStellenZuBeginnDerBewegungsphase` (2),
   `testBew12_2NachDemZurücknehmenStehtJedesModellWoEsZuBeginnDerBewegungsphaseStand` (2),
   `testBew12_2OhneAngebotBleibtJedesModellWoEsHingezogenWurde` (2),
   `testBew12_2DerDienstNenntNachDemZurücknehmenDieStellenZuBeginnDerBewegungsphase`,
   `testBew15_1NachErneuterAuswahlZeigtDieKarteDieEinhüllendeUmDieStellenZuBeginnDerPhase` (4).
   BEW-15.1 ist die Frage des *Stakeholders* (7070), Schritt 5 des Plans.
   Nicht betroffen: Die Fälle mit einem *Modell* als *Ebene* (das letzte, weit vom Warboss);
   `testBew11_1NachDemZiehen…` sperrt heute nur, weil BEW-7.1 noch fehlt.
2. `testBew12_2AmBildschirmNimmtDerKnopfDieGrenzeDesWurfsZurück` in
   [vorrueckenZuruecknehmenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/vorrueckenZuruecknehmenTest.py)
   prüft nach dem Klick nur den Knopf und die Domäne, nicht was sein Name sagt: dass die
   *Karte* den *Grenzkreis* des Wurfs nicht mehr zeigt. Er würde auch grün, wenn die Seite
   die alten Grenzen stehen ließe.

**Kosten.** Am Bildschirm nichts. Ohne Änderung bleiben 13 Fälle rot, der Implementierer kann
das Item nicht grün melden oder ändert den Aufbau selbst; BEW-12.2 und BEW-15.1 gingen
ungeprüft in die Abnahme. Je eine Zeile.

**Gegenvorschlag.** 1: `zweiZollZurMitte` zieht entlang der Reihe, weg von ihrem ersten *Modell*, `(0, 2″)` wie
`nachUnten` in [vorrueckenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/vorrueckenTest.py);
dort steht nichts, und die *Einheit* bleibt im *Spielfeld*. Der Name folgt der Richtung.
Erledigt: Die 13 Fälle sind rot nur am fehlenden Produkt, nicht an einer *Sperre*.
2: nach dem Klick `expect(seite.locator(".karte g.grenze.spieler1")).to_have_count(1)`.

Die übrigen Tests treffen ihr Kriterium: Radien aus *Bewegungsweite*, halbem *Durchmesser*
und Wurf, die Ringe unter dem letzten *Modell* liegen für die ganze *Einheit* wie für ein
*Modell* je im richtigen Ring (die übrigen *Modelle* der Reihe stehen weiter weg), Rand des Kreises zählt zu seinem
Wurf, Klick im *Grenzkreis* aus BEW-11 und außerhalb des sechsten hebt die *Auswahl* auf,
Anhalten an *Bewegungsweite* plus Wurf, Maus und Finger am Bildschirm. Zu Recht schon grün
sind die drei Tests der Seite ohne *Auswahl* (kein Knopf, keine Grenze).

**Stellungnahme.** Angenommen, beides umgesetzt.
1. `zweiZollEntlangDerReihe` in [grenzen.py](../../technik/tests/akzeptanz/grenzen.py) zieht
   `(0, 2″)`; es überdeckt nur *Modelle* der eigenen *Einheit* (BEW-2.7 sperrt nicht).
   Gelaufen: Die 13 Fälle sind nur noch am fehlenden Produkt rot (`grenzen`,
   `vorrückenZurücknehmen`, `karteAnklicken`).
2. Nach dem Klick: `.karte g.grenze.spieler1` gleich 1.
