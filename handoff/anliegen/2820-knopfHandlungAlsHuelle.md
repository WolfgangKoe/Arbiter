# Der Knopf „Aufstellen der Einheit beenden“ bindet seinen Aufruf in einer Hülle

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** [anfragen.js](../../technik/frontend/anfragen.js), Zeile 7, neu in diesem Item:
`handlung: () => handlungSenden("/api/aufstellenDerEinheitBeenden", "PUT")`. Die Pfeilfunktion
ist eine Hülle um einen Aufruf, die Pfad und Methode bindet. [Es 7](../../prozess/praemissen/es.md)
gilt für Python und Frontend: „Kein lambda als Hülle um einen Aufruf“. Nach
[Ich 3](../../prozess/praemissen/ich.md) hält das auf: neuer Code verletzt Lesbarkeit (Es).
Die Tabelle `knöpfe` ist neu; die alte Fassung in `seite.js` hatte dieselbe Hülle, sie ist mit
dem Teilen neu geschrieben.

**Kosten.** Mit dem nächsten Knopf (Gemeinsam übergehen, Etappe 2) wächst die Tabelle um
weitere namenlose Hüllen; der Leser sieht an der Tabelle nur Pfade, keine Handlung des Spielers.
Nachbessern: zwei Zeilen.

**Gegenvorschlag.** Eine benannte Funktion in anfragen.js, etwa
`function aufstellenDerEinheitBeenden() { return handlungSenden("/api/aufstellenDerEinheitBeenden", "PUT") }`,
und in der Tabelle `handlung: aufstellenDerEinheitBeenden`, wie `modellLoslassen` und
`karteAnklicken` daneben.

Erledigt: keine Hülle mehr in `knöpfe`, Tests grün.

**Stellungnahme.** Angenommen. [anfragen.js](../../technik/frontend/anfragen.js) hat jetzt die
benannte Funktion `aufstellenDerEinheitBeenden`; die Tabelle `knöpfe` verweist auf sie, ohne Hülle.
