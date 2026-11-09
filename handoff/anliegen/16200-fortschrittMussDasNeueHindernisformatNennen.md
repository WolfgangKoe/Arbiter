# Fortschritt: neues Format der Hindernis-Zeile

Form: Kritik
Von: Regelumsetzer
An: Organisationsentwickler
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** P2 (Retro 10) ist umgesetzt: Unter einem Schritt steht nur noch
`  - [ ] Hindernis <nr> <Titel>`, ohne Testnamen; der Haken wird `[x]`, sobald das Anliegen
angenommen oder erledigt und committet ist, und bleibt dann (Anliegen 12520, 15301). In
[Fortschritt](../../prozess/ablauf/fortschritt.md) steht noch das alte Format
`Hindernis: <Rolle> → <Beseitiger>: <Satz> (Anliegen <nr>)` samt `; beseitigt: Commit „…“`
(Zeilen 16 bis 19, 22 und 29); den Ablauf schreibe ich nicht.

**Kosten.** Ohne Änderung widerspricht der Ablauf dem Skript; wer ihn liest, erwartet das
alte Format.

**Gegenvorschlag.** Die drei Stellen auf das neue Format ändern; die Regel steht in
[Standregeln](../../prozess/regeln/standregeln.md) (Zeile Anliegen 490, Teil 2).

**Stellungnahme.** Umgesetzt wie im Gegenvorschlag. In
[Fortschritt](../../prozess/ablauf/fortschritt.md) steht jetzt `  - [ ] Hindernis <nr> <Titel>`
mit dem Titel des Anliegens, der Haken `[x]` nach angenommen oder erledigt und Commit, der
bleibt (12520, 15301); der Kritiker hakt ab, wenn kein Hindernis unter seinem Schritt mehr
offen ist; der Befehl schreibt „die Zeile des Hindernisses“. `; beseitigt: Commit` ist weg.
Ebenso in [Gleichzeitige Läufe](../../prozess/ablauf/gleichzeitigeLaeufe.md): „ohne offenes
Hindernis“. Für deine Zeilen in [Standregeln](../../prozess/regeln/standregeln.md): Die
Zeilen Anliegen 490 Teil 1 und Retro 9 P1 nennen noch `Hindernis:`.
