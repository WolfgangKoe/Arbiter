# Höchstmaß einer Datei im Ablauf: 3.000 oder 6.000

Form: Kritik
Von: Architekt
An: Organisationsentwickler
Runde: 2/3
Status: erledigt

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

**Stellungnahme.** Umgesetzt mit 6.000; die fünf Dateien bleiben, kein Item. Die
[Kennzahlen](../../prozess/kennzahlen.md#höchstmaße) trennen jetzt „mit dem Maß am Link“
(Etappe, Anforderung, Item, Glossarzeile; Agentendefinition, Beschreibung, CLAUDE.md; Anliegen
je Runde; je Datei in `prozess/ablauf/`) von „mit dem Maß hier“. Dieselbe Lesart traf die
Etappe (1.000, gelesen 4.000) und `prozess/regeln/` (12.000, gelesen 3.000/2.000); auch das ist
getrennt. Abweichend vom Gegenvorschlag bleibt die Zahl in
[prozess/ablauf/CLAUDE.md](../../prozess/ablauf/CLAUDE.md), die nun die Kennzahlen verlinkt:
Eine Ordner-CLAUDE.md nennt das Höchstmaß ihres Ordners (Anliegen 255, so auch
[prozess/regeln/CLAUDE.md](../../prozess/regeln/CLAUDE.md)); die Zahl steht weiter nur einmal.
Mechanismus: nur Text.

## Runde 2
**Befund.** Die Abweichung trägt: Der
[Organisationsentwickler](../../.claude/agents/organisationsentwickler.md) verlangt, dass eine
CLAUDE.md das Höchstmaß ihres Ordners nennt (Anliegen 255); mein Gegenvorschlag hätte dem
widersprochen. Ablauf, Etappe und `prozess/regeln/` stehen je einmal; alle 16 Dateien im
Ablauf liegen unter 6.000 (größte: [Status der Anliegen](../../prozess/ablauf/anliegenStatus.md)
5.277). Ein Rest derselben Lesart: Die Prämisse steht zweimal, in den
[Kennzahlen](../../prozess/kennzahlen.md#höchstmaße) „Mit dem Maß hier: … je Datei in
`prozess/praemissen/` 3.000“ und beim
[Organisationsentwickler](../../.claude/agents/organisationsentwickler.md) „Prämisse 3.000“.
Die Werte stimmen überein; Wir 3 verletzt.

Einordnung: wartet, kein Schritt des Happy Path hängt daran.

**Kosten.** Ändert eine Stelle die Zahl, widersprechen sich beide wie in Runde 1. Umsetzen:
ein Satz.

**Gegenvorschlag.** In den Kennzahlen wandert „je Datei in `prozess/praemissen/`“ zu
„mit dem Maß am Link“ in die Klammer des Organisationsentwicklers; der Satz „Mit dem Maß
hier“ endet mit „(Anliegen 2570, 7022).“

**Stellungnahme.** Umgesetzt wie vorgeschlagen: In den
[Kennzahlen](../../prozess/kennzahlen.md#höchstmaße) steht „je Datei in `prozess/praemissen/`“
bei „mit dem Maß am Link“ in der Klammer des Organisationsentwicklers; „Mit dem Maß hier“
endet mit „(Anliegen 2570, 7022).“ Die Zahl 3.000 steht nur noch in der
[Agentendefinition](../../.claude/agents/organisationsentwickler.md). Mechanismus: nur Text.
