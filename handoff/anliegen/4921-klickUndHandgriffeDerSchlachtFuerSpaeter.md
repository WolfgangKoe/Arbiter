# Klick auf ein Modell und Handgriffe der Schlacht für später

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: offen
Wartet auf: Technikphase 9

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

**Stellungnahme.**
