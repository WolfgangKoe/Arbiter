# Aufräumen und feste Adresse: Reste in Auswahl, Server, Befehl, Bedienung und Einheitstests

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: angenommen
Wartet auf: Technikphase

## Runde 1
**Befund.** Lesbarkeit seit `Freigabe Plan 7`, alles wartet nach
[Ich 3](../../prozess/praemissen/ich.md): Prüfungen grün, Randfälle oder Ablage.
1. `Aufstellung.ebene` und `Auswahl.ebene` ([__init__.py](../../technik/arbiter/domaene/phasen/aufstellen/__init__.py):79,
   [auswahl.py](../../technik/arbiter/domaene/phasen/aufstellen/auswahl.py):29) ruft im Produkt
   niemand mehr, seit `ganzeEinheitIstEbene` und `modellIstEbene` sie ersetzen (1651); nur
   auswahlTest.py fragt noch.
2. [server.py](../../technik/arbiter/web/server.py):28–33: `anwendungFür` läuft zwischen Binden
   und `with`; wirft es, bleibt der Socket offen. `gebundenerPort` ist überflüssig: Mit `fd`
   liest werkzeug den Port aus dem Socket.
3. [__main__.py](../../technik/arbiter/__main__.py):32: Der Port wird erst nach
   `aufstellungNachDemStart()` gelesen (`arbiter --help` lädt den Katalog). `--port 70000`
   endet mit `OverflowError`, ein Port unter 1024 mit `PermissionError`, beide als Traceback.
4. [bedienung.js](../../technik/frontend/bedienung.js):66: `return ausgewählteKarteVon(…) && ebeneSenden(…)`
   ist ein Fall als Ausdruck statt `if` mit frühem `return` ([Es 9](../../prozess/praemissen/es.md));
   `ausgewählteKarteVon` liefert ein Element, gefragt ist, ob die *Einheit* ausgewählt ist.
5. [serverTest.py](../../technik/tests/einheit/web/serverTest.py): Den Port liest der Test
   zweimal per `split(":")`; der erste Test vergleicht die Adresse mit sich selbst
   (`adresseMitPort` des eigenen Ports); `beenden()` läuft nicht, wenn eine Annahme scheitert.
6. [anwendungTest.py](../../technik/tests/einheit/web/anwendungTest.py),
   `testDasZurückSetzenEinesModellsAufEineArmeelisteGibtEsNichtMehr`: prüft, dass entfernte
   Pfade fehlen ([Wir 4](../../prozess/praemissen/wir.md): Historie ist git). Die 405 kommt nur
   von der Route der statischen Dateien (`static_url_path=""`).

**Kosten.** 1: drei Fragen an denselben Zustand, der Leser sucht, welche gilt. 2: ein offener
Socket je Fehlstart in Tests. 3: ein Spieler sieht einen Traceback statt einer Meldung. 4: der
nächste Fall an derselben Stelle wird ein weiteres `&&`. 5: bricht ein Test, bleibt sein Server
bis Prozessende. 6: der Test bricht, wenn sich die statischen Dateien ändern, nicht wenn ein
Pfad zurückkehrt.

**Gegenvorschlag.**
1. `ebene` entfernen; auswahlTest.py fragt `ganzeEinheitIstEbene` und `modellIstEbene`.
2. `anwendung = anwendungFür(aufstellung)` zuerst, dann
   `with _verbindungBinden(port) as verbindung:` und `make_server(_gerät, port, anwendung, fd=verbindung.fileno())`.
3. `port = portDesBefehls(sys.argv[1:])` als erste Zeile von `starten`; `type` prüft 0 bis
   65535 (argparse meldet dann selbst); `PermissionError` wie `AdresseBelegt` mit einer Zeile
   melden. Ob dafür ein Kriterium nötig ist, entscheidet der Anforderungsautor (QUE-8).
4. `if (!einheitAusgewählt(modell.dataset)) return` und danach `return ebeneSenden(…)`.
5. Fixture mit `yield` und `beenden()`; den Port per `urlparse(…).port` wie in
   festeAdresseTest.py, oder `Server.port`; den ersten Test streichen oder auf `127.0.0.1` und
   einen Port über 0 prüfen.
6. Test streichen.

Erledigt: 1 bis 6 umgesetzt oder begründet abgelehnt, Tests grün.

**Stellungnahme.** Angenommen; 1, 2, 4, 5 und 6 umgesetzt, 3 zum Teil.
1: `ebene` gestrichen, auswahlTest.py fragt `ganzeEinheitIstEbene` und `modellIstEbene`.
2: Binden nach dem Bauen der Anwendung; `fd` trägt den Port. 4: `einheitAusgewählt` in
[bedienung.js](../../technik/frontend/bedienung.js), früher `return`. 5: Fixture mit `yield`
und `beenden()`, Port über `Server.port`, der Test auf die eigene Adresse ist durch einen auf
den freien Port ersetzt. 6: Test gestrichen.
3: Der Port wird als erste Zeile von `starten` gelesen, und `--port` außerhalb von 0 bis 65535
lehnt argparse ab (Unit-Test in [befehlTest.py](../../technik/tests/einheit/befehlTest.py)).
Nicht umgesetzt: die einzeilige Meldung bei `PermissionError`. Dazu fehlt ein Kriterium, und
ohne Test baue ich kein Verhalten (Ich 1); der Anforderungsautor entscheidet das bei QUE-8.
