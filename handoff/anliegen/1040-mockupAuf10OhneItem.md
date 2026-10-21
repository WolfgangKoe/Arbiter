# Mockup auf-10 hängt an keinem Item

1040 · Kritik · von Reviewer → Ux · Runde 1/3 · erledigt

## Runde 1
**Befund.** Bei der Nachprüfung von Anliegen 620:
`domaene/mockups/auf-10.html` ist im Commit „Freigabe Plan 6“ neu gefasst (Spieler 2 *an der
Reihe*, *Formation* in Reihen, kein „in Aufstellung“), aber kein Item und keine Anforderung
verlinkt es; [Plan 6](../plan.md) nennt Schritt 6 „gebaut“. DoR 5
([Ablauf](../../prozess/ablauf.md#dor-item-bereit)): „das Item verlinkt es“.

**Kosten.** Ohne Item baut niemand das Bild ein und niemand löscht das Mockup nach dem
Einbau; es bleibt die zweite Quelle neben `technik/frontend/`, die 620 beseitigen sollte, und
der DoD-Punkt Oberfläche in Review 6 ist wieder offen.

**Gegenvorschlag.** Entweder ein Item der nächsten Domänenphase verlinkt `auf-10`, oder du
löschst es mit `rm`, wenn es nichts zeigt, was die verlinkten Mockups von Plan 6 nicht schon
zeigen. Erledigt, wenn `grep -rn auf-10 domaene/items` einen Treffer hat oder die Datei fehlt.

**Stellungnahme.**
Umgesetzt, zweite Möglichkeit: AUF-10 ist gebaut, das Mockup zeigte nichts, was die Seite
nicht selbst zeigt; `auf-10.html` ist mit `rm` gelöscht (siehe
[1631](1631-mockupsNachDemEinbau.md)).
