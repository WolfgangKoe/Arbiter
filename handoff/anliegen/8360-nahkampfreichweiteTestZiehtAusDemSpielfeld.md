# Test BEW-6.2 zur Nahkampfreichweite zieht aus dem Spielfeld

Form: Kritik
Von: Implementierer
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** In
[anhaltenVorDerGrenzeTest.py](../../technik/tests/akzeptanz/phasen/bewegung/anhaltenVorDerGrenzeTest.py)
bleibt `testBew6_2ZiehtEinModellInDieNahkampfreichweiteDesAnderenSpielersHältArbiterEsDavorAn`
rot (die übrigen 16 Tests der Datei sind grün). Es ist derselbe Fehler wie in Anliegen 8280:
Nach `aufeinanderZuZiehen` steht der Warboss bei y = 100/127 = Radius, seine *Base* liegt an
der *Spielfeldkante*; der Overlord steht bei y = 80/127. `westlichDavorMitAbstand` übernimmt
dessen y, der Weg hat dy = -20/127 und führt aus dem *Spielfeld*. BEW-6.1 hält den Warboss
deshalb schon beim ersten Schritt an (Stelle unverändert); BEW-6.2 allein hielte bei 4/5 des
Wegs. Der Test verlangt das Anhalten vor der *Nahkampfreichweite*, das die Regeln zusammen
nicht hergeben.

**Kosten.** Der Test bleibt rot; DoD 1 für den Teillauf BEW-6 ist offen. Ich ändere weder
Test noch Regel.

**Gegenvorschlag.** Wie bei 8280: Das Ziel auf die y-Linie des Warboss legen,
`Stelle(x=stelleDesAnderen.x - radien - abstand, y=stelle.y)` mit dem y des ziehenden
Modells statt dem des anderen, und den Abstand weiter an der *Stelle* des Overlords messen.

**Stellungnahme.** Angenommen wie vorgeschlagen. Das Ziel in
`testBew6_2ZiehtEinModellInDieNahkampfreichweiteDesAnderenSpielersHältArbiterEsDavorAn`
liegt jetzt auf der y-Linie des Warboss, einen halben Zoll westlich der Grenze der Radien
zum Overlord; die Hilfsfunktion heißt dafür `westlichDavorAufDerLinieVon` und nimmt das y
von der *Stelle* des Warboss. Der Weg bleibt im *Spielfeld*. Eine Prüfung in der
Vorgeschichte sichert, dass das Ziel weiter in der *Nahkampfreichweite* des Overlords
liegt; den Abstand misst der Test weiter an der *Stelle* des Overlords. Alle 17 Tests der
[Datei](../../technik/tests/akzeptanz/phasen/bewegung/anhaltenVorDerGrenzeTest.py) grün,
ruff und Benennung grün.
