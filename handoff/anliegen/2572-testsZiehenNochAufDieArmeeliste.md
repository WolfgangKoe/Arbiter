# Tests ziehen noch auf die Armeeliste und warten auf eine Antwort, die es nicht mehr gibt

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund (hält auf).** Nach [handlungen.md](../../technik/architektur/handlungen.md) schickt
die Seite beim Loslassen auf einer `armeeKarte` keine Anfrage mehr (AUF-16.8), die Route
`DELETE …/stelle?ablage=` steht nicht mehr im Vertrag. Drei Stellen bauen noch auf ihr:

1. [sperreOhneStelleTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/sperreOhneStelleTest.py):
   `einAufgestelltesModellAufDieEigeneAblageZiehen` erwartet ‚nicht wählbar‘ für ein
   *Modell* einer *aufgestellten* *Einheit* auf der eigenen *Armeeliste*, also AUF-8.4.
   Zwei Tests zu AUF-12.6 (`…NochNachDemAuswählen`, `…NichtMehrNachDerNächstenHandlung`)
   bauen ihre Vorgeschichte darauf; AUF-16.8 verlangt dort keinen *Grund*.
2. Ebenda ohne Aufrufer: das Feld `Loslassen.ablage`, die Zweige `fall.ablage` in
   `inDerDomäneLoslassen`, `imDienstLoslassen`, `amBildschirmLoslassen`, damit
   `dienst.modellAufAblageLoslassen`; der Docstring von `Loslassen` nennt noch die *Ablage*.
3. [bedienungTest.py](../../technik/tests/akzeptanz/querschnitt/bedienungTest.py),
   `testQue3_4EinModellAufDieAblageZiehen…`: `modellAufDieAblageZiehen` wartet auf eine
   Antwort (`_ziehenBisZurAntwort`), die nach dem Vertrag nie kommt.

Dazu ist `formregeln/benennung.py` rot: `zurueckOhneSperreTest.py` (AUF-17) hat keine
Anforderung mehr; Plan 7 streicht ihn samt „zurück“.

1 und 3 sind heute grün nur, weil der Code AUF-8.4 noch hat; sobald der Implementierer es entfernt, laufen
1 und 3 in die Wartezeit.

Zwei Erklärungen sind mit den Kommentaren verloren, Name und Architektur tragen sie nicht
(Plan 7: „steht danach im Namen, in einem einzeiligen Docstring oder in der Architektur“):

4. [blockAlsGanzesTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/blockAlsGanzesTest.py),
   `testAuf24_2DerDienstAntwortet…`: `pytest.approx(…, abs=1e-9)` weicht von
   [S2](../../technik/architektur.md) („ohne Toleranz“) ab; warum (der Dienst liest den
   gesendeten Weg als Dezimalzahl, die anderen *Modelle* folgen ihm), steht nirgends mehr.
5. [setzenPerKlickTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/setzenPerKlickTest.py),
   `testAuf18_3…`: `assert {*grenzenInX, *grenzenInY} & set(ränder)` ist die einzige
   Prüfung von „auf kürzestem Weg“; dass sie „eine *Base* berührt die Grenze der Zone“
   heißt, liest man nicht mehr.

Von den übrigen 20 der 22 Kommentare außerhalb von Anliegen 2541 trägt ein Name, ein
Docstring (`inZoll`) oder die Architektur (S1, S2, V8, V10) alle bis auf drei in
Hilfsmodulen und Aufbauten; die warten (Anliegen 2573).

**Kosten.** 1 bis 3 machen den Schritt „Tests grün“ unmöglich, ohne die Tests anzufassen;
4 und 5 kosten je einen Namen.

**Gegenvorschlag.**
- 1: Die beiden Tests zu AUF-12.6 sperren mit AUF-7.2 auf der *Karte*, wie
  `einModellEinerAufgestelltenEinheit`; der Handgriff entfällt.
- 2: Feld, Zweige und `dienst.modellAufAblageLoslassen` löschen; die drei Funktionen
  werden einzeilig.
- 3: Mit `ziehenOhneAnfrage` auf die Mitte der *Armeeliste* ziehen und prüfen: keine Anfrage,
  jedes *Modell* steht, wo es war. Danach hat `modellAufDieAblageZiehen` keinen Aufrufer
  und entfällt.
- 4: Die Toleranz als benannte Konstante, etwa `rundungDesGesendetenWegs = 1e-9`.
- 5: `berührtDieGrenze = bool({*grenzenInX, *grenzenInY} & set(ränder))`, dann
  `assert berührtDieGrenze`.

- AUF-17: `zurueckOhneSperreTest.py` löschen; „zurück“ nehme ich aus dem Vertrag.

Erledigt, wenn `formregeln/benennung.py` grün ist, kein Akzeptanztest mehr `?ablage=` sendet oder auf die Antwort eines Zugs auf
eine *Armeeliste* wartet und 4 und 5 je einen Namen haben.

**Stellungnahme.** Angenommen, alles wie vorgeschlagen.
- 1 und 2 (mit 2610): AUF-12.6 sperrt mit AUF-7.2 auf der *Karte*; `Loslassen.ablage`, die
  Zweige und `dienst.modellAufAblageLoslassen` sind weg.
- 3: `testQue3_4EinModellAufDieArmeelisteZiehenUndLoslassenSendetNichtsUndLässtJedesModellWoEsWar`
  zieht mit `ziehenOhneAnfrage` auf die Mitte der *Armeeliste* und prüft: keine Anfrage,
  jedes *Modell* steht, wo es war. `modellAufDieAblageZiehen` ist gelöscht.
- 4: `rundungDesGesendetenWegs = 1e-9` in `blockAlsGanzesTest.py`.
- 5: `berührtDieGrenze` in `setzenPerKlickTest.py`.
- AUF-17: `zurueckOhneSperreTest.py` und der Helfer `zurück` in `dienst.py` gelöscht; weitere
  Helfer ohne Aufrufer gibt es nicht.
- `formregeln/benennung.py` ist grün.

Offen für den Implementierer: Solange der Code AUF-8.4 noch hat, sendet die Seite
`DELETE …/stelle?ablage=`; der neue Test zu QUE-3.4 ist deshalb in beiden Eingaben rot
(`[maus]`, `[finger]`), alle übrigen 492 sind grün. Das ist der geforderte Test und wird
mit dem Entfernen von AUF-8.4 grün.
