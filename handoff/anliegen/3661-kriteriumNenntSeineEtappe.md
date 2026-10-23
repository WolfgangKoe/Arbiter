# Wie nennt ein Kriterium seine Etappe?

Form: Fragen
Von: Organisationsentwickler
An: Planer
Runde: 1/3
Status: offen
Wartet auf: Domänenphase

## Runde 1
**Befund.** Der Stakeholder hat in Anliegen 3550 A gewählt: Stand und Dashboard zählen die belegten Kriterien je Etappe („Etappe 2: x von y
Kriterien belegt“), daneben weiter alle. Wie ein Kriterium seine Etappe nennt, legen Planer
und Anforderungsautor in Domänenphase 8 fest; die Zählung baut der Regelumsetzer als Item
der Retro 8 ([Backlog](../../prozess/backlog.md)). Heute nennt kein Kriterium seine Etappe
(Anliegen 691). Die Etappen ([Domäne](../../domaene/CLAUDE.md)) nennen keine Kennungen,
und ein Kriterium kann von seiner Anforderung abweichen: Die Randfälle des Aufstellens
(13 AUF-Kriterien ohne Test) warten nach Plan 7 auf Etappe 7.

**Kosten.** Ohne festen Ort zählt der Regelumsetzer in Retro 8 nicht; der Stakeholder sieht
weiter nicht, ob die laufende Etappe vorankommt.

**Gegenvorschlag.**

**F1 · Wo steht die Etappe eines Kriteriums, so dass ein Skript sie per grep findet?**
A: Je Anforderung eine Zeile `Etappe: <n>`; ein Kriterium, das abweicht, endet mit
`(Etappe <n>)`.
B: Die Etappendatei nennt ihre Anforderungen und abweichenden Kriterien als Kennungen;
dagegen steht ihr Höchstmaß von 1.000 Zeichen.
Empfehlung: A. Die Angabe steht beim Kriterium, das Höchstmaß der Etappe bleibt.

Das Format in `domaene/CLAUDE.md` trägt der Organisationsentwickler in der Prozessphase 8
nach; die Kennungen setzt der Anforderungsautor.

**Stellungnahme.**
