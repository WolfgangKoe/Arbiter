# Kritik am Code zu Item einheitVerschieben: Lesbarkeit, Doppeltes, Ebene bei erneutem Auswählen

1420 · Kritik · von Reviewer → Implementierer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Lesbarkeit ([Es](../../prozess/praemissen/es.md)) und Korrektheit der Änderung
seit dem letzten Commit. Nichts hält auf ([Ich 3](../../prozess/praemissen/ich.md): Randfall,
Ablage von Hilfen, keine Prüfung rot). Was [1410](1410-kritikAmCodeEinheitVerschieben.md)
nennt, fehlt hier. Geprüft: Unit-Tests 84 grün; Akzeptanztests ohne
`anhaltenAnEinerBaseTest.py` 453 grün, rot nur 14 zu AUF-24.1 (Item anhaltenAnBases);
`prozess/pruefungen` rot nur `ruff` in Testdateien von anhaltenAnBases.
1. Erneutes Auswählen verwirft die *Ebene*: `Auswahl.auswählen`
   ([auswahl.py](../../technik/arbiter/domaene/phasen/aufstellen/auswahl.py)) setzt
   `_modellAlsEbene = None` auch, wenn die *Einheit* schon *ausgewählt* ist. AUF-20.2 gilt,
   „wenn AUF-5.11 eine *Einheit* *ausgewählt* macht“; V2 und V9 nennen `PUT` idempotent.
   Beispiel: Auf Seite B ist ein *Modell* der Boyz die *Ebene*, Seite A zeigt die Boyz noch
   nicht *ausgewählt* (QUE-3.2). Ein Klick dort auf die Einheitenkarte schickt `PUT`, die
   *Ebene* ist wieder die *Einheit*, der nächste Zug auf B verschiebt den Block.
2. [seite.js](../../technik/frontend/seite.js): `ebeneSenden` wiederholt die
   Antwortbehandlung von `auswahlSenden`, ohne deren `// Warum:` zum 404; den Pfad
   `${einheitenPfad(kreis)}/modelle/${kreis.dataset.nummer}` bauen jetzt drei Funktionen.
3. `gesetztesModellDerAusgewählten` ([anwendung.py](../../technik/arbiter/web/anwendung.py))
   sucht *Spieler* und *Einheit* ein zweites Mal, die `modellDerArmee` schon gefunden hat.
4. Wächter ungleich verteilt: `web/` antwortet 404 ohne *gesetztes* *Modell* (V9),
   `Aufstellung._prüfenDassGesetzt` wirft danach `ValueError`, den kein Test erreicht;
   `Auswahl.ebeneWählen` prüft die Zugehörigkeit zur *ausgewählten* *Einheit*,
   `ebeneAbwählen` nicht.
5. [einheitVerschiebenTest.py](../../technik/tests/einheit/domaene/phasen/aufstellen/einheitVerschiebenTest.py):
   `testEinGezogenesOhneStelleDavorBewegtDieGruppeNicht` schreibt einen Fall fest, den
   `modellLoslassen` nie erzeugt, und damit den Ersatzwert aus 1410, Punkt 2. `zehnZoll` mit
   `# Regel: 254 mm sind 10″…` steht jetzt in fünf Testdateien, der Kommentar ohne
   Fundstelle (Es 8).

**Kosten.** Zu 1: Ein *Spieler* verliert unbemerkt seine Wahl und verschiebt die ganze
*Einheit*, wo er ein *Modell* meinte. Zu 2 bis 5: Eine Änderung an Antwort, Pfad, Wächter
oder Test-Base trifft mehrere Stellen; der Test zu 5 hält fest, was 1410 abschaffen will.

**Gegenvorschlag.**
1. `auswählen` setzt die *Ebene* nur zurück, wenn eine andere *Einheit* *ausgewählt* wird;
   Unit-Test in [auswahlTest.py](../../technik/tests/einheit/domaene/phasen/aufstellen/auswahlTest.py):
   zweimal dieselbe *Einheit*, die *Ebene* bleibt das *Modell*. Siehst du AUF-20.2 anders:
   Frage an den Anforderungsautor.
2. Eine Hilfe für die Antwort beider (mit dem `// Warum:`) und `modellPfad(kreis)`.
3. `modellDerArmee` liefert die *Einheit* mit, oder sie kommt aus `einheitenNachNummer`.
4. Je Wächter eine Stelle: `Auswahl` prüft in beiden Methoden die Zugehörigkeit, `web/` die
   404; `_prüfenDassGesetzt` entfällt oder bekommt einen Unit-Test, nach deinem Urteil.
5. Den Test mit 1410, Punkt 2 anpassen oder streichen; `zehnZoll` einmal in einem
   Hilfsmodul der Unit-Tests, der Kommentar als `# Warum:`.

Erledigt: umgesetzt oder begründet abgelehnt, Tests grün, Verhalten unverändert außer 1.

**Stellungnahme.**
Alle fünf Punkte umgesetzt, Unit- und Akzeptanztests grün (570, ohne die rote Datei zu AUF-24.1).
1. `Auswahl.auswählen` kehrt bei derselben *Einheit* früh zurück, die *Ebene* bleibt; Unit-Test
   `testDieselbeEinheitErneutAuswählenBehältDieEbene`.
2. `zeichneAntwort` (mit dem `// Warum:`) und `modellPfad(kreis)` in
   [seite.js](../../technik/frontend/seite.js), von `auswahlSenden`, `ebeneSenden`, Loslassen und
   Abfrage gerufen.
3. `einheitDerArmee` und `modellDerEinheit` in
   [anwendung.py](../../technik/arbiter/web/anwendung.py); *Spieler* und *Einheit* werden einmal gesucht.
4. `_prüfenDassGesetzt` entfällt (die 404 für ein nicht *gesetztes* *Modell* bleibt in `web/`);
   `Auswahl` prüft die Zugehörigkeit in `ebeneWählen` und `ebeneAbwählen`, Unit-Test dazu.
5. Der Test zu 1410, Punkt 2 entfiel schon; der Fall steht jetzt in
   `testEinNochNichtGesetztesModellBewegtDieGruppeNicht` (1450, Punkt 1). `zehnZoll` ist eine Fixture in
   [conftest.py](../../technik/tests/einheit/conftest.py) mit `# Warum:`, alle fünf Testdateien
   nutzen sie.
