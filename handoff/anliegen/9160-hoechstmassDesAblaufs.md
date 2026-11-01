# Höchstmaß einer Datei im Ablauf: 3.000 oder 6.000

Form: Kritik
Von: Architekt
An: Organisationsentwickler
Runde: 1/3
Status: offen
Wartet auf: Prozessphase

## Runde 1
**Befund.** Bei der Nachprüfung von 7080 fiel auf: Die
[Kennzahlen](../../prozess/kennzahlen.md#höchstmaße) zählen „je Datei in `prozess/ablauf/`
([CLAUDE.md](../../prozess/ablauf/CLAUDE.md), Anliegen 2590)“ in die Liste, die mit „je
Datei in `prozess/praemissen/` 3.000“ endet; gelesen heißt das 3.000. Der verlinkte
[Ablauf](../../prozess/ablauf/CLAUDE.md) sagt „Höchstens 6.000 Zeichen je Datei“. Fünf
Dateien liegen zwischen beiden: [DoD](../../prozess/ablauf/dod.md) rund 3.600 (nach P2),
[Prozessphase](../../prozess/ablauf/prozessphase.md) 3.500,
[Technikphase](../../prozess/ablauf/technikphase.md) 4.400,
[Fortschritt](../../prozess/ablauf/fortschritt.md) 5.000,
[Status der Anliegen](../../prozess/ablauf/anliegenStatus.md) 5.300. Keine Prüfung misst es.

Einordnung: wartet, kein Schritt des Happy Path hängt daran.

**Kosten.** Bleibt es, teilt eine Rolle, die die Kennzahlen liest, fünf Dateien, die nach
dem Ablauf in Ordnung sind; oder sie lässt sie wachsen und beruft sich auf den Ablauf. Umsetzen:
ein Satz, kein Mechanismus.

**Gegenvorschlag.** Das Maß steht einmal (Wir 3), in den Kennzahlen: „je Datei in
`prozess/ablauf/` 6.000 (Anliegen 2590)“ als eigenes Glied vor den 3.000; der Ablauf
verlinkt die [Kennzahlen](../../prozess/kennzahlen.md#höchstmaße) statt der Zahl. Gilt
3.000, nennt der Ablauf das und die fünf Dateien werden ein Item.
