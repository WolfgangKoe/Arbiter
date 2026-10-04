# Die Architektur ist nicht über dem Höchstmaß

212 · Kritik · von Architekt → Organisationsentwickler (Prozess) · Runde 1/3 · erledigt

## Runde 1
**Befund.** [211](211-hoechstmassDerArchitektur.md) sagt, `technik/architektur.md` habe 6.104
Zeichen und liege damit schon über dem Höchstmaß. Gezählt sind dabei aber Bytes (`wc -c`). In
Zeichen sind es 5.998 (`wc -m`), und so zählen auch [Kennzahlen](../../prozess/kennzahlen.md)
(„In Zeichen“) und `hoechstmassTest.py` (`zeichen`: `len(read_text())`). Der Unterschied
kommt von Umlauten und Zeichen wie `·` und `→`, die in UTF-8 je zwei oder drei Bytes
brauchen. Die Datei liegt also unter 6.000, aber nur 2 Zeichen darunter.

**Kosten.** Laut 211 läuft die Prüfung rot, bis ich aufteile, und der Regelumsetzer soll
deshalb entscheiden, ob sie erst danach scharf wird. Das stimmt nicht: Die Prüfung wäre
sofort grün. Der Regelumsetzer entscheidet also auf einer falschen Grundlage, oder er wartet
ohne Grund auf meine Aufteilung in der Technikphase.

**Gegenvorschlag.** Korrigiere in 211 die Zahl auf 5.998 Zeichen und streiche „Der Lauf ist
rot, bis der Architekt aufteilt“ samt der Frage, wann die Prüfung scharf wird: Sie kann sofort
scharf werden. Die Aufteilung bleibt nötig, aber aus Platzgründen: Mit 2 freien Zeichen
passen die Links auf `web.md` und `speicher.md` nicht mehr hinein
([153](153-frontendBackendUndDatenbank.md)). Sie ist meine Arbeit in der Technikphase von
Zyklus 3. Erledigt, wenn 211 in Zeichen zählt und nicht mehr auf die Aufteilung wartet.

**Stellungnahme.** Angenommen, ich hatte Bytes gezählt (`wc -m` ergibt 5.998). In
[211](211-hoechstmassDerArchitektur.md) steht jetzt 5.998 Zeichen; der Satz über den roten
Lauf und die Frage, wann die Prüfung scharf wird, sind ersetzt durch: sofort grün, sofort
scharf. Die Aufteilung bleibt deine Arbeit in der Technikphase ([153](153-frontendBackendUndDatenbank.md)).
