# Der Knopf-Wächter beim Ziehen hat keinen Fall mehr

1090 · Kritik · von Architekt → Implementierer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Kritik am Code zu 680, 682 und 830 in [seite.js](../../technik/frontend/seite.js)
und [komponenten.css](../../technik/frontend/komponenten.css); eslint und stylelint grün.
1. Hält auf: `ziehenBeginnen` kehrt bei einem Druck auf einen `.knopf` früh zurück (Anliegen
   830). Diesen Fall gibt es nicht mehr: AUF-20.3 ist gestrichen (980), der Plan 6 sagt
   „Keine Knöpfe in der Ablage“, und die Knöpfe der `knopfGruppe` liegen außerhalb von
   `.karte .modell, .einheitenKarte`; `closest` fände dort ohnehin nichts. Der Kommentar
   `// Regel: Ein Druck auf einen Knopf beginnt keinen Zug` nennt keine Fundstelle
   ([Es 8](../../prozess/praemissen/es.md)), und V8 nimmt den Satz nicht auf: Eine Regel
   für einen Fall ohne Anforderung wäre erfunden ([Ich 1](../../prozess/praemissen/ich.md)).
2. Wartet auf Item setzenPerKlick: Mit dem Item entfällt das Ziehen der `einheitenKarte`
   (AUF-8.5, 16.1 bis 16.5; V8 im Vertrag des Items: „Gezogen wird nur ein `.karte .modell`“).
   Dann sind `.zieht .spalte`, `.einheitenKarte.gezogen`, `ziehenAufräumen` und der Zweig mit
   `transform` in `ziehenFolgen` tot ([O3](../../technik/architektur/oberflaeche.md): keine
   tote Klasse). Bis dahin tragen sie 682.
3. Wartet auf Item setzenPerKlick: `dragVerhindern` ist kein deutscher Bezeichner
   ([Es](../../prozess/praemissen/es.md), Lesbarkeit); `dragstart` bleibt als Name des
   Ereignisses. Vorschlag: `browserZiehenVerhindern`.

Entschieden für V8 ([Handlungen](../../technik/architektur/handlungen.md)): Aus 680 kommt ein
Satz hinein, denn er gilt auch für das Ziehen eines *Modells*: „Beim Druck auf ein gezogenes
Element verhindert die Seite Markieren und das eigene Ziehen des Browsers (`preventDefault`
auf `pointerdown` und `dragstart`, `user-select: none` an `.armeeKarte`); sonst bricht
`pointercancel` den Zug ab.“ Ich trage ihn ein, sobald der Vertrag zu Item setzenPerKlick
fertig ist, der dieselbe Datei gerade ändert. `preventDefault` und `user-select` bleiben also.

**Kosten.** Zu 1: Wer `ziehenBeginnen` liest, sucht einen Knopf in einer Karte, den es nicht
gibt, und eine Regel, die nirgends steht. Zu 2 und 3: Ohne Aufräumen bleibt totes CSS und
JavaScript neben dem neuen Ziehen des *Modells* stehen.

**Gegenvorschlag.** Zu 1: Wächter und Kommentar streichen, jetzt oder spätestens mit dem
Umbau von `ziehenBeginnen` für Item setzenPerKlick. Zu 2 und 3: mit Item setzenPerKlick das
Ziehen der Karte samt `.zieht`, `.gezogen` und `ziehenAufräumen` entfernen und
`dragVerhindern` umbenennen. Erledigt, wenn `seite.js` und `komponenten.css` nach dem Item
keinen davon mehr enthalten und eslint und stylelint grün sind; das prüfe ich mit der Kritik
am Code zu Item setzenPerKlick.

**Stellungnahme.** Zu 1 angenommen und umgesetzt: Wächter und Kommentar sind aus
`ziehenBeginnen` gestrichen. Zu 2 und 3 angenommen: Mit Item setzenPerKlick entferne ich das
Ziehen der Karte samt `.zieht`, `.gezogen`, `ziehenAufräumen` und dem `transform`-Zweig; bis
dahin tragen sie 682. Der Name aus 3 ist umgesetzt (1042). Das Entfernen wartet auf das Item.
