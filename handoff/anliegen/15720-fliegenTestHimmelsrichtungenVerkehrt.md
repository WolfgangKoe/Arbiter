# Neue Tests zu 15462: Himmelsrichtungen verkehrt, Zahlen ohne Begriff

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Lesbarkeit der neuen Akzeptanztests seit `5ffc953` ([Es](../../prozess/praemissen/es.md):
der Name trägt die Bedeutung). Ruff und Format sind grün.
1. Norden und Süden sind in
   [fliegenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/fliegenTest.py) vertauscht.
   Das *Spielfeld* zeichnet `y` nach unten (`viewBox="0 0 44 60"`), und die Nachbartests
   nennen `+y` Süden: `einZollNachSüden = (nichts, Fraction(1))` in derselben Änderung
   ([weiterziehenNachDemUebergehenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/weiterziehenNachDemUebergehenTest.py)),
   ebenso in `anhaltenVorDerGrenzeTest.py` und `uebergehenTest.py`. In `lagenAnDenSpielfeldkanten`
   liegt `"süden"` aber bei `y = 0`, also am oberen Rand des Bildschirms, und `"norden"` bei
   `y = 60`. In `schrägZumWarrior` zeigt `"nachNordwesten"` mit `(-3/5, 4/5)` nach Südwesten und
   `"nachSüdwesten"` nach Nordwesten. Die ids stehen in jeder Ausgabe von pytest und mutmut.
   Wer einen roten Fall `[süden]` am Bildschirm nachstellt, sucht am falschen Rand.
2. `eins = Fraction(1)` steht für zwei Begriffe, die Einheitsrichtung in `nachInnen` und
   `entlang` und eine Länge in Zoll: `anDerKante(lage, eins, nichts)`, `2 * eins`,
   `summeDerRadien(spinne, lord) - eins`. Was `2 * eins` ist, liest man erst aus der Rechnung
   ab. Im selben Ordner gibt es schon die Form mit Begriff (`halberZoll`, `einZollNachOsten`).
3. In `testBew25_1EinenZollZurückInDieBewegungsweite…` heißt die Länge
   `überDieBewegungsweite`, sie ist aber negativ und streckt `zurück` gegen seine Richtung:
   `gestreckt(zurück, -(bewegungsweite(…) + halberZoll))`. Der Name sagt nicht, dass die
   vorige *Stelle* entgegen `zurück` liegt, das zeigt nur das Minuszeichen.

**Kosten.** Ein paar Zeilen, das Verhalten bleibt gleich, und die gefangenen Mutanten
bleiben gefangen. Ohne die Änderung widersprechen sich zwei Testdateien desselben
Ordners bei den Himmelsrichtungen, und jeder spätere Test an einer *Spielfeldkante* muss
raten, welche gilt.

**Gegenvorschlag.**
1. Die ids und Schlüssel tauschen: `"norden"` für `y = 0`, `"süden"` für `y = längeDerSpielfeldkante`,
   `"nachSüdwesten"` für `(-3/5, 4/5)` und `"nachNordwesten"` für `(-3/5, -4/5)`. Die Vektoren
   bleiben, wie sie sind.
2. `einZoll = Fraction(1)` für die Längen, `zweiZoll` statt `2 * eins`. Die Richtungen
   schreibt man als `Fraction(1)` aus oder gibt ihnen einen Namen in der Form der Nachbartests.
3. `vorige = versetzt(start, gestreckt(zurück, -überDieBewegungsweite))` mit positiver
   Länge, oder die Richtung umbenennen (`weg`, `vonDerStelleWeg`), sodass kein
   Minuszeichen die Bedeutung trägt.

**Stellungnahme.** Alle drei angenommen, Vektoren und Werte unverändert, die Tests grün.
1. [fliegenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/fliegenTest.py):
   `"norden"` bei `y = 0`, `"süden"` bei `y = längeDerSpielfeldkante`, `"nachSüdwesten"` für
   `(-3/5, 4/5)`, `"nachNordwesten"` für `(-3/5, -4/5)`.
2. Statt `eins` die Richtungen `nachOsten`, `nachWesten`, `nachSüden`, `nachNorden` in
   `lagenAnDenSpielfeldkanten`, die Längen `einZoll` und `zweiZoll`. Dazu `halbesZoll` durch
   `halberZoll` aus `grenzen.py` ersetzt, wie im übrigen Ordner.
3. [weiterziehenNachDemUebergehenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/weiterziehenNachDemUebergehenTest.py):
   `überDieBewegungsweite` ist positiv, `gestreckt(zurück, -überDieBewegungsweite)`.
