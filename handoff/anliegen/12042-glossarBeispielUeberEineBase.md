# Glossar: Beispiel überEineBase

Form: Kritik
Von: Architekt
An: Anforderungsautor
Runde: 1/3
Status: offen
Wartet auf: Domänenphase 11

## Runde 1
**Befund.** Wartet (keine Prüfung rot), Kritik an den Tests zu Item anhaltenAufDemWeg. Seit
8840 gibt es BEW-2 nicht mehr. Mit diesem Item fällt im Code `Grund.überEineBase` weg (V15,
[Handlungen](../../technik/architektur/vertrag/bewegung/handlungen.md)). Das
[Glossar](../../domaene/glossar.md), Zeile *Grund*, nennt aber weiter `Grund (überEineBase)`
als Code. Dieser Name steht dann nirgends mehr im Code.

**Kosten.** Ein Wort. Bleibt es, sucht man im Code nach einem Namen, den es nicht gibt.

**Gegenvorschlag.** Ein bestehender Name, etwa `Grund (baseÜberdeckt)`.

**Stellungnahme.**
