# Wenn AUF-8.4 wegfällt, müssen AUF-12 und AUF-16.8 mitgehen

Form: Kritik
Von: Fachkritiker
An: Anforderungsautor
Runde: 1/3
Status: offen
Wartet auf: Domänenphase

## Runde 1
**Befund.** Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): wartet. Es geht um einen
Randfall abseits des Happy Path, und AUF-8.4 fällt erst mit dem Item
[loslassenNebenDerKarte](../../domaene/items/loslassenNebenDerKarte.md) in Etappe 2 weg
(„Entfällt mit Test: AUF-8.4“, 2220 F4 A). Zwei Folgen davon stehen bisher nur in der
Stellungnahme des gelöschten Anliegens 2312:
1. [sperreOhneStelle.md](../../domaene/anforderungen/phasen/aufstellen/sperreOhneStelle.md)
   nennt AUF-8.4 an zwei Stellen: im Zweck (Zeile 3, „ein *Modell* einer *aufgestellten*
   *Einheit*“) und in AUF-12.5 (Zeile 6, „AUF-7.2 oder 8.4“). Mit diesen Stellen fallen auch die
   Fälle `auf8_4…` in `sperreOhneStelleTest.py:108` und `:109` weg.
2. [AUF-16.8](../../domaene/anforderungen/phasen/aufstellen/loslassenOhneZiel.md) gilt nur
   „neben *Karte* und *Armeelisten*“. Fällt AUF-8.4 weg, regelt kein Kriterium mehr, was
   geschieht, wenn jemand ein *Modell* einer *aufgestellten* *Einheit* auf einer *Armeeliste*
   loslässt. Laut Glossar ist die *Armeeliste* „kein Ziel zum Hineinziehen“. Gemeint ist also:
   Das *Modell* springt still zurück, wie neben der *Karte*. Das Item nennt dafür aber nur den
   Grund, nicht die neue Fassung.

**Kosten.** Wird nur AUF-8.4 gelöscht, verweist AUF-12.5 auf ein Kriterium, das es nicht mehr
gibt. Außerdem sagt dann keine Anforderung, was das Loslassen auf einer *Armeeliste* bewirkt.
Der Testautor würde dazu nichts prüfen, und der Implementierer müsste raten.

**Gegenvorschlag.** Wenn du AUF-8.4 löschst, im selben Schritt den Zweck von AUF-12 und
AUF-12.5 ohne 8.4 fassen und AUF-16.8 auf „neben der *Karte*, auch auf einer *Armeeliste*“.
Damit das bis dahin nicht verloren geht, schreibst du es in das Item
loslassenNebenDerKarte, etwa „AUF-16.8 gilt dann auch auf der *Armeeliste*; AUF-12.5 ohne
8.4“.

**Stellungnahme.**
