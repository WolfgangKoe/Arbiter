# Klick auf ein Modell und Handgriffe der Schlacht für später

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Wartet (Ich 3: Namen und Ablage von Hilfsfunktionen, keine Prüfung rot).
1. `Aufstellung.modellAnklicken` und `Schlacht.modellAnklicken` heißen nach dem Klick auf ein
   *Modell*, decken aber nur AUF-20.6. Den Klick auf ein *Modell* der *ausgewählten* *Einheit*
   (AUF-25.1, 25.2) führen weiter `ebeneWählen` und `ebeneAbwählen`; welche der drei
   Handlungen gilt, entscheidet die Seite nach dem Spielstand. `karteAnklicken` dagegen
   entscheidet in der Domäne. Für Zyklus 8 lege ich den Vertrag so an wie heute: die Seite
   wählt die Anfrage.
2. Die Fixture `schlacht` in [conftest.py](../../technik/tests/akzeptanz/conftest.py)
   importiert `Schlacht` im Rumpf; ihr Docstring begründet das mit dem roten Zustand. Ist der
   Code grün, stimmt der Grund nicht mehr (Wir 4).
3. `zurBewegungsphaseDerNächstenSchlachtrunde` in
   [schlacht.py](../../technik/tests/akzeptanz/schlacht.py) hat als einziger Handgriff dort
   keinen Docstring und zählt mit `2 * len(phasenEinesZugs)` und `break`; ob die nächste
   *Schlachtrunde* erreicht ist, prüft er nicht.

**Kosten.** Keine in Zyklus 8. Bleibt 1, wächst mit jeder *Phase*, die einen Klick kennt, die
Fallunterscheidung im Frontend statt in der Domäne.

**Gegenvorschlag.**
1. In Technikphase 9 entscheiden: `modellAnklicken` nimmt alle drei Fälle (Domäne wie bei
   `karteAnklicken`, eine Route weniger), oder es heißt nach seinem einen Fall, etwa
   `einheitDesModellsAuswählen`. Empfehlung: alle drei Fälle, die Tests zu AUF-25 gehen dann
   über `modellAnklicken`.
2. Sobald der Code grün ist, den Import nach oben und den Docstring auf die Aufgabe kürzen.
3. Docstring ergänzen und aus `zügeBeenden` und `phaseBeendenBis` zusammensetzen, mit einem
   Fehler, wenn die *Schlachtrunde* nicht wechselt, wie in `phaseBeendenBis`.

**Stellungnahme.** Angenommen; die Docstrings aus 2 und 3 lasse ich weg, weil Es 8 sie seit
`Freigabe Plan 9` verbietet (Anliegen 6981).
1. `modellAnklicken` deckt in *Aufstellung* und *Schlacht* alle drei Fälle ab. Die Tests zu
   AUF-25 klicken über `modellAnklicken`, beim *Dienst* über `PUT …/modelle/<m>/anklicken`
   (V14). Die *Seite* schickt diese Anfrage bei jedem Klick auf ein *Modell*
   (`aufDasAnklickenWarten` in [ziehen.py](../../technik/tests/akzeptanz/ziehen.py)).
   `ebeneWählen`, `ebeneAbwählen`, `modellAlsEbene` und `einheitAlsEbene` gibt es in den Tests
   nicht mehr. Die Vorgeschichte heißt `modellZurEbeneMachen`, einmal in
   [handgriffe.py](../../technik/tests/akzeptanz/handgriffe.py) statt dreifach. Sie bricht ab,
   wenn der Klick das *Modell* nicht zur *Ebene* macht; so wird kein Test ohne Code grün.
   Betroffen: [modellPerKlickTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/modellPerKlickTest.py),
   [ebeneTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/ebeneTest.py),
   [einheitZuruecklegenTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/einheitZuruecklegenTest.py),
   [anhaltenAnEinerBaseTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/anhaltenAnEinerBaseTest.py).
   Rot sind sie, weil der Code fehlt. Für dich: V9 und die Seite in
   [auswahl.md](../../technik/architektur/vertrag/aufstellen/auswahl.md) und
   [seite.md](../../technik/architektur/vertrag/aufstellen/seite.md) auf V14 umstellen;
   `ebene.json` bleibt das Beispiel nach dem ersten Klick.
2. Der Import steht in [conftest.py](../../technik/tests/akzeptanz/conftest.py) oben, der
   Docstring ist weg.
3. `zurBewegungsphaseDerNächstenSchlachtrunde` in
   [schlacht.py](../../technik/tests/akzeptanz/schlacht.py) ruft `zügeBeenden(schlacht, 2)` und
   `phaseBeendenBis` auf. Folgt nicht die nächste *Schlachtrunde*, bricht er mit einem Fehler ab.
