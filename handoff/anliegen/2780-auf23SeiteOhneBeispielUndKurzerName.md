# AUF-23: Seite nicht gegen die Beispiele geprüft, ein Name zu kurz

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund (hält auf).** In
[einheitZuruecklegenTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/einheitZuruecklegenTest.py):

1. `formregeln.benennung` ist rot: Zeile 130, `for m in boyzMitEbene.modelle`, „m: weniger
   als 3 Zeichen“ ([Es 5](../../prozess/praemissen/es.md)).
2. Die Seite wird nur gegen den echten Server geprüft. [V6 und V7](../../technik/architektur/handlungen.md)
   verlangen unter „Prüft“ je Kriterium auch Bildschirmtests, denen `page.route` die Beispiele
   liefert, wie `testAuf10_3DieSeiteNenntBeimBeendenDenGrundDerSperreImBeispiel` in
   [beendenTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/beendenTest.py). Für
   AUF-23.1, 23.3 und 23.4 fehlen sie; `zurueckgelegt.json` liest nur der Dienst.

**Kosten.** 1 macht die DoD rot. Zu 2: Nur ein Test mit dem Beispiel zeigt, dass die Seite
den Vertrag liest (den Knopf an `einheitInAufstellung`, nicht etwa an `modelle`; die Antwort
von `PUT /api/zurücklegen` zeichnet), unabhängig davon, was der Server gerade schickt.
Ändert sich der Server, bleibt der Durchstich grün, solange beide Hälften gleich falsch sind.

**Gegenvorschlag.**
1. `for modell in boyzMitEbene.modelle`.
2. Drei kurze Tests mit `bildschirm.seiteMitSpielstand(ausgangsaufstellung, …)`:
   - AUF-23.1/23.3: Stand `spielstandDesVertrags()`, als `weitere` die Antwort
     `zurückgelegtDesVertrags()` auf `PUT /api/zurücklegen`; Klick auf „Einheit zurücklegen“,
     dann keine `.karte .modell` und `ausgewählteEinheiten(seite) == {"Necron Warriors"}`.
   - AUF-23.4: Mit `spielstandDesVertrags()` bietet die Seite beide Knöpfe an, mit
     `zurückgelegtDesVertrags()` nur „Aufstellen der Einheit beenden“.

   Achtung, im Wegwerf-Versuch geprüft: Das Glob-Muster `"**/api/zurücklegen"` greift nicht,
   denn der Browser fordert `/api/zur%C3%BCcklegen` an; die Anfrage ginge am Muster vorbei an
   den echten Server. Das Muster prozentkodiert schreiben (`"**/api/zur%C3%BCcklegen"`) oder
   ein Prädikat mit `unquote` wie `istHandlung` in
   [bildschirm.py](../../technik/tests/akzeptanz/bildschirm.py) nehmen.

**Stellungnahme.** Angenommen und umgesetzt. `m` heißt `modell`. Neu in
[einheitZuruecklegenTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/einheitZuruecklegenTest.py):
`testAuf23_1DieSeiteLeertDieKarteMitDerAntwortImBeispiel`,
`testAuf23_3DieSeiteZeigtDieEinheitMitDerAntwortImBeispielAusgewählt` (Stand und Antwort aus
`spielstandDesVertrags()` und `zurückgelegtDesVertrags()`, `page.route` mit dem kodierten
Muster `**/api/zur%C3%BCcklegen`) und zu AUF-23.4 zwei Tests, die mit Beispiel
`spielstand.json` beide Knöpfe, mit `zurueckgelegt.json` nur „Aufstellen der Einheit beenden“
erwarten. `formregeln.benennung` grün, ruff check und ruff format --check für die Datei grün.
Die Bildschirmtests sind in meinem Lauf noch rot, weil die Seite nicht lädt (halbfertiger Code).
