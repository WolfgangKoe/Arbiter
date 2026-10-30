# Hindernis: Tests zu Item gemeinsamUebergehen

Form: Kritik
Von: Testautor
An: Planer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Die Tests zu BEW-8, QUE-5 und QUE-6 stehen vollständig, Formprüfungen grün. Das Häkchen setzt sich nicht, weil die Zeile Abhängigkeit in domaene/items/gemeinsamUebergehen.md BEW-2 nennt; die Prüfung zählt damit BEW-2 zum Item, und BEW-2.8 gehört zu Item 3 (anhaltenUndAuswahl) und hat dort noch keinen Test. Empfehlung: in der Abhängigkeit die Kennung streichen (die Sperren beim Ziehen stehen) statt BEW-2 zu nennen; Alternative für den Regelumsetzer: itemKriterienGetestet liest nur die Zeile Umfang. Das hält den Schritt „Tests zu Item gemeinsamUebergehen“ von Testautor im Fortschritt auf.

**Kosten.** Der Schritt bleibt offen, die Phase kommt nicht weiter.

**Gegenvorschlag.** Planer beseitigt das Hindernis.

**Stellungnahme.** Angenommen wie empfohlen: In [gemeinsamUebergehen](../../domaene/items/gemeinsamUebergehen.md) lautet die Abhängigkeit jetzt „keine; die *Sperren* beim Ziehen stehen.“, ohne Kennung. Geprüft mit `itemKriterienGetestet`: für gemeinsamUebergehen wahr, der Haken setzt sich beim nächsten Lauf des Fortschritts. Die Alternative für den Regelumsetzer braucht es nicht; die Abhängigkeit von Item 3 nennt BEW-8.2, das in Item 2 getestet ist, und hält darum nichts auf.
