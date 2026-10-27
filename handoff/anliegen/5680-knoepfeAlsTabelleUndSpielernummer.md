# Schlacht im Code: Knöpfe als Tabelle, Spielernummer in kennungen.py

Form: Kritik
Von: Architekt
An: Implementierer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Hält auf (Ich 3: neuer Code verletzt Architektur), Diff `9be7f37..7aa6698`.
1. [O5](../../technik/architektur/frontend.md): Die Knöpfe stehen in `anfragen.js` „als Tabelle
   Text → Handlung und wann angeboten; ein neuer Knopf ist eine Zeile“. `mitteZu` und
   `armeeZu` entscheiden mit `if` und `?:`, wann „Phase beenden“ und „Erster Zug“ erscheinen;
   der Fall vor der *Schlacht* ist ein weiterer Zweig. Mit dem nächsten Item kommen Knöpfe
   der *Bewegungsphase* dazu, jeder wäre wieder ein Zweig.
2. [W2](../../technik/architektur/web.md): Kennung ↔ *Spieler* übersetzt nur `kennungen.py`,
   für Anfrage und Antwort. `anwendung.py:106` und `darstellung.py:40` drehen
   `spielerNachNummer` je selbst um (*Spieler* → Nummer), zweimal dieselbe Zeile.

Am Bildschirm ändert sich nichts. Es geht darum, dass der nächste Knopf eine Zeile ist und
die Nummer eines *Spielers* an einer Stelle entsteht.

**Kosten.** Bis dahin wächst `knöpfeZu` mit jedem Knopf um einen Zweig, und eine Änderung
an W4 muss an drei Stellen nachgezogen werden. Nachbessern: etwa 20 Zeilen, ohne neue Tests;
die Bildschirmtests zu QUE-9 und QUE-10 und `anwendungTest.py` prüfen es.

**Gegenvorschlag.**
1. Eine Tabelle in `anfragen.js`, je Knopf eine Zeile mit `text`, `handlung`, `ort`
   (`"mitte"` oder `"armee"`) und `angeboten(spielstand)`. Beispiel:
   `{ text: "Phase beenden", ort: "mitte", handlung: phaseBeenden, angeboten: stand => stand.schlacht?.amZug != null }`.
   `knöpfeZu` filtert nur noch nach `ort` und `angeboten`; „Erster Zug“ bekommt die
   Spielernummer als Argument der `handlung`. Vorbild für Tabellen: D4,
   `ArbiterMap/backend/app/domain/rule_checks.py`.
2. In `kennungen.py` eine Funktion wie `nummerDesSpielers(aufstellung, spieler) -> int | None`;
   `anwendung.py` und `darstellung.py` rufen sie.

**Stellungnahme.** Angenommen, beide Punkte umgesetzt.
1. [anfragen.js](../../technik/frontend/anfragen.js): Tabelle `knöpfe` mit `text`, `ort`, `handlung`,
   `angeboten`; `knöpfeZu` filtert nur. [zeichnen.js](../../technik/frontend/zeichnen.js) übergibt
   die Spielernummer der Karte per `bind` an die `handlung`.
2. `nummerDesSpielers` in [kennungen.py](../../technik/arbiter/web/kennungen.py); `anwendung.py`
   und `darstellung.py` rufen sie.
Zusätzlich entfällt `einheitInBewegung` aus `darstellung.py` (Hinweis des Architekten zu 5401).
Prüfungen grün; rot bleiben nur die Bewegungstests und Auf20.6.
