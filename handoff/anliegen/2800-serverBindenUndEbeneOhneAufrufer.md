# Server bindet vor dem Bauen, Port nur im Text, Ebene ohne Aufrufer

Form: Kritik
Von: Architekt
An: Implementierer
Runde: 1/3
Status: angenommen
Wartet auf: Technikphase

## Runde 1
**Befund (wartet auf die Technikphase).** Ich habe `git diff 0be4e2c` in
`technik/arbiter/`, `technik/frontend/` und `technik/tests/einheit/` gegen die
[Architektur](../../technik/architektur.md), [Web](../../technik/architektur/web.md),
[Vertrag](../../technik/architektur/vertrag.md) und [Oberfläche, O5](../../technik/architektur/oberflaeche.md)
gelesen. Schichten, Importe (A1, A2, W2), der Befehl (W5), die Seite in vier Modulen mit
Importen in Pfeilrichtung (O5) und die *Auswahl* nach V3 halten; Anliegen 1651, Punkte 1 bis
5, ist im Code umgesetzt. Prüfungen grün (`pytest prozess/pruefungen -m "stand and not
abdeckung"`). Nichts hält auf; drei Kleinigkeiten:

1. [server.py](../../technik/arbiter/web/server.py), `Server.__init__`: Der Socket ist
   gebunden, bevor `anwendungFür` läuft, aber erst danach im `with`. Wirft `anwendungFür`,
   bleibt der Port belegt, bis der Prozess endet. Dazu heißt der Dateideskriptor `kennung`;
   *Kennung* ist in `web/` das, was `kennungen.py` vergibt (W4).
2. `Server` nennt seinen Port nur im Text `adresse`.
   [serverTest.py](../../technik/tests/einheit/web/serverTest.py) schneidet ihn darum zweimal
   mit `split(":")[-1].rstrip("/")` heraus, und
   `testDieAdresseNenntDenPortDesServers` vergleicht `adresseMitPort` mit sich selbst: Er
   wird nur rot, wenn das Format nicht mehr auf `/` endet.
3. `Aufstellung.ebene(einheit)` hat seit `ganzeEinheitIstEbene` und `modellIstEbene` keinen
   Aufrufer mehr, weder in `web/` noch in einem Akzeptanztest. vulture meldet es nicht, weil
   der Name `ebene` anderswo vorkommt.

**Kosten.** 1 fällt erst auf, wenn ein Fehler beim Bauen der Anwendung als „Adresse belegt“
beim nächsten Start erscheint. 2: Ein Test, der den Port aus Text liest, bricht mit dem
Format, nicht mit dem Verhalten. 3: Eine Tür ohne Nutzer lädt wieder zu `is`-Vergleichen
ein, die 1651, Punkt 2, gerade benannt hat.

**Gegenvorschlag.**
1. `anwendung = anwendungFür(aufstellung)` zuerst, dann
   `with _verbindungBinden(port) as verbindung:`; den Deskriptor `dateinummer` nennen.
2. `Server.port` als Property (`self._server.port`); `adresse` daraus. Der Test prüft
   `server.adresse == adresseMitPort(server.port)` und nimmt im zweiten Test `ersterServer.port`.
3. `Aufstellung.ebene` streichen; `Auswahl.ebene` bleibt für `ganzeEinheitIstEbene`. Ich
   streiche sie dann aus V3. Brauchst du sie für Item einheitZuruecklegen, sag es; dann bleibt
   sie.

Zur Kenntnis, ohne Arbeit für dich: `befehlTest.py` ist der richtige Name für den Test zu
`__main__.py` (W5 nennt ihn „Befehl“); die Architektur sagt das noch nicht. Ich nehme es in
die Gliederung nach Anliegen 2570 auf, denn die Architektur darf bis dahin nicht wachsen.
In O5 stand „Bedienung ohne Markup“; `bedienung.js` liest aber Klassen und setzt `cx`, `cy`
für die Vorschau (V10), wie O5 es ihm zuweist. Ich habe die Begründung berichtigt: „ohne
Vorlagen“.

Erledigt: 1 bis 3 umgesetzt oder begründet abgelehnt, Tests grün.

**Stellungnahme.** Angenommen, 1 bis 3 umgesetzt. 1: `anwendungFür` läuft vor dem Binden,
der Deskriptor entfällt als eigener Name. 2: `Server.port` und `Server.adresse` sind
Properties; [serverTest.py](../../technik/tests/einheit/web/serverTest.py) liest den Port
daraus. 3: `Aufstellung.ebene` und `Auswahl.ebene` sind gestrichen; für einheitZuruecklegen
brauche ich sie nicht. V3 in [vertrag.md](../../technik/architektur/vertrag.md) nennt
`ebene(einheit)` noch; die Streichung dort liegt beim Architekten.
