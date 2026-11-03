# Zeile fliegen im Katalog vor den Tests zu Item fliegen

Form: Kritik
Von: Anforderungsautor
An: Implementierer
Runde: 1/3
Status: offen

## Runde 1
**Befund.** MIV-3.2 verlangt *Fliegen* bei der Canoptek-Spinne
([MIV-3](../../domaene/anforderungen/missionsvorbereitung/canoptekSpinne.md)). Den Wert
`fliegen: true` darf ich erst eintragen, wenn `katalog/` den Schlüssel kennt; davor lehnt der
Start ihn ab ([Katalog](../../technik/architektur/katalog.md) K3, K4, K7, Anliegen 11560).

**Kosten.** Bis dahin hat die Spinne in den Daten kein *Fliegen*, und
[9340](9340-fliegenDerSpinne.md) bleibt offen.

**Gegenvorschlag.** Lege die Zeile `fliegen` beim *Datenblatt* nach K3 an (freiwillig, fehlt
er, gilt `false`), vor den Tests zu Item [fliegen](../../domaene/items/fliegen.md), und nimm
dann an; danach trage ich den Wert ein.

**Stellungnahme.**
