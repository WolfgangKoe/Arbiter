# Namen und Aufbau in den Tests zu BEW-17

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: offen
Wartet auf: Technikphase 11

## Runde 1
**Befund.** Wartet (Namen und Aufbau, keine Prüfung rot), Kritik an den Tests zu Item
anhaltenAufDemWeg.
1. [anhaltenVorFremdenBasesTest.py](../../technik/tests/akzeptanz/phasen/bewegung/anhaltenVorFremdenBasesTest.py):
   Zwei Tests entpacken `boyz, warboss, *_ = spielerEins.armee.einheiten`, obwohl die
   Fixtures `boyz` und `warboss` bestehen. So hängen sie an der Reihenfolge der *Armeeliste*.
2. Ebenda: `(gezeigt,) = gezeigteStellen(…)` steht vor `status_code == OK`. Bei einer 409
   bricht der Test mit `KeyError: 'modelle'` ab, statt den Status zu nennen (gesehen im Lauf
   gegen den heutigen Code).
3. Ebenda: Zahlen wie `Fraction(99, 20)` (knapp unter der *Bewegungsweite*) oder
   `(Fraction(-16, 5), Fraction(1))` haben keinen Namen. Der Leser sieht nicht, warum die
   Szene so liegt. In `amNeuntenVorbei` geht es schon so.
4. [uebergehenBeimZiehenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/uebergehenBeimZiehenTest.py):
   `gezeigteStellen` liest dort die *gesetzten* *Stellen* nach V18, nicht die gezeigten.
   Der Name passt also nur zu V10.
5. [setzenTest.py](../../technik/tests/akzeptanz/querschnitt/setzenTest.py), QUE-1.4: `zuvor`
   liegt auf der *Base* des fünften Boys, schon über der *Bewegungsweite*. Ein Name, der das
   sagt, macht die Szene ohne Nachrechnen lesbar.

**Kosten.** Je Punkt wenige Zeilen. Bleibt es, rechnet der Leser die Szenen nach, und ein
Fehler zeigt sich als `KeyError`.

**Gegenvorschlag.** 1: die Fixtures nehmen. 2: den Status vor dem Entpacken prüfen. 3 und 5:
die Stellen benennen. 4: Hilfsfunktion für gesetzte *Stellen* aus dem Spielstand, etwa
`gesetzteStellen`, oder ein neutraler Name für beide.

**Stellungnahme.**
