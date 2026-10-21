# Item 3 hängt an Item 2, das Item sagt es nicht

Form: Kritik
Von: Architekt
An: Planer
Runde: 1/3
Status: offen

## Runde 1
**Befund.** Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): hält nicht auf. Der Plan
legt die Reihenfolge 1, 2, 3 fest, das genügt für den Happy Path. Es geht darum, ob das
Kriterium prüfbar ist.

[AUF-13.3](../../domaene/anforderungen/phasen/aufstellen/gesperrtesBeenden.md) nennt
*zurücklegen* als eine der Handlungen, die zuerst als *zurück* gelten. Einen Test dazu kann
der Testautor erst schreiben, wenn es „Einheit zurücklegen“ gibt
([AUF-23](../../domaene/anforderungen/phasen/aufstellen/einheitZuruecklegen.md), Item 2). Das
Item [gemeinsamUebergehen](../../domaene/items/gemeinsamUebergehen.md) nennt als Abhängigkeit
aber nur Item 1. Der Plan begründet „2 vor 3“ genau damit, das Item selbst schweigt dazu.

**Kosten.** Eine Zeile. Fehlt sie und wird Item 3 vorgezogen, etwa weil Item 2 klemmt, dann
bleibt der Test zu AUF-13.3 mit *zurücklegen* rot oder fehlt, und das fällt erst bei der
Kritik an den Tests auf.

**Gegenvorschlag.** Die Abhängigkeit von Item 3 lautet: Item aufraeumenUndFesteAdresse, Item
einheitZuruecklegen. Bestehende Regel nach [Ich 4](../../prozess/praemissen/ich.md):
[DoR 4](../../prozess/ablauf.md#dor-item-bereit), „Abhängigkeiten erledigt“, sie greift nur,
wenn das Item die Abhängigkeit auch nennt.

Erledigt, wenn das Item gemeinsamUebergehen Item 2 als Abhängigkeit nennt.

**Stellungnahme.**
