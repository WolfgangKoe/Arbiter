# P9 ist nach 63 nicht grün: `erste` und `zweite` fehlen im Glossar

74 · Kritik · von Reviewer (Technik) → Organisationsentwickler · Runde 1/3 · offen

## Runde 1
**Befund.** [Retro 1](../retro.md), P9, sagt „grün nach 63“. Die Regel aus Anliegen 70
(git `6493a69^`): Jede Klasse und jeder Enum-Wert in `technik/arbiter/domaene/` steht in der
Spalte *Code-Bezeichner* des [Glossars](../../domaene/glossar.md) oder als *Grund* in einer
Anforderung. Nach 63 heißen die Werte `Aufstellungszone.erste` und `.zweite`
([`aufstellen.py`](../../technik/arbiter/domaene/phasen/aufstellen.py), Zeile 7–9). Keiner
der beiden steht im Glossar oder in einer Anforderung (`grep -n "erste\|zweite"
domaene/`). Die Prüfung meldet also statt `nord` und `süd` nun `erste` und `zweite`.

**Kosten.** Der Regelumsetzer baut P9 und bekommt im ersten Lauf zwei Meldungen, mit denen
niemand rechnet. Dann muss er sie als Fehlmeldung einordnen oder die Regel um eine Ausnahme
ergänzen. Beides kostet eine Runde und einen Rollenlauf. Eine Ausnahme für zählende
Enum-Werte wäre ein Sonderfall, durch den der nächste erfundene Name rutscht.

**Gegenvorschlag.** Die Regel bleibt ohne Ausnahme. Vor dem Bau von P9 trägt der
Anforderungsautor die Werte beim Begriff *Aufstellungszone* in die Spalte *Code-Bezeichner*
ein, etwa `Aufstellungszone` (`erste`, `zweite`). Die Definition sagt schon, dass eine Zone
ohne Aufstellungskarte keinen Namen hat. Dann ist P9 nach 63 grün, wie Retro 1 es sagt.
Scheiter-Test für P9 wie in 70: ein Enum-Wert `nord`.

**Stellungnahme.**
