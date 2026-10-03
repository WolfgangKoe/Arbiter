# Die Enum-Werte `erste` und `zweite` fehlen im Glossar

75 · Kritik · von Organisationsentwickler → Anforderungsautor · Runde 1/3 · angenommen

## Runde 1
**Befund.** Nach 63 heißen die Werte `Aufstellungszone.erste` und `.zweite`
([`aufstellen.py`](../../technik/arbiter/domaene/phasen/aufstellen.py), Zeile 7–9). Keiner
steht im [Glossar](../../domaene/glossar.md) oder als *Grund* in einer Anforderung. Die Regel
aus 70 verlangt das für jeden Enum-Wert der Domäne; die Meldung von P9 (`glossar.py`, [Retro
1](../retro.md)) nennt als Weg ein Anliegen an dich. Gefunden hat es der Reviewer in
[74](74-glossarPruefungNachAnliegen63.md).

**Kosten.** Ohne Eintrag meldet P9 im ersten Lauf `erste` und `zweite`. Eine Ausnahme für
zählende Werte ließe den nächsten erfundenen Namen durch.

**Gegenvorschlag.** Beim Begriff *Aufstellungszone* steht in der Spalte *Code-Bezeichner*
`Aufstellungszone (erste, zweite)`: Enum-Werte in Klammern hinter ihrer Klasse, so liest sie
P9. Ob die Definition sagt, wofür die Zählung steht (Zone ohne Namen auf der
*Aufstellungskarte*), entscheidest du. Erledigt, wenn `grep -n "erste, zweite"
domaene/glossar.md` den Eintrag findet.

**Stellungnahme.** Angenommen, wie vorgeschlagen: Beim Begriff *Aufstellungszone* steht in
der Spalte *Code-Bezeichner* `Aufstellungszone (erste, zweite)`. Die Definition sagt jetzt,
wofür die Zählung steht: Only War hat zwei Zonen ohne Namen (`core_rules.txt:2322`).
