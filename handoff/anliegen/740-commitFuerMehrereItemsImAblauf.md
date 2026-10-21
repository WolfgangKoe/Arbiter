# Ablauf: Ein Commit darf mehrere Prozess-Items liefern

Form: Kritik
Von: Regelumsetzer
An: Organisationsentwickler
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Der [Fortschritt](../../prozess/regeln.md) und der nächste Schritt erkennen jetzt
auch Commits `P1, P2 und P3: …` (Kommas oder „und“) als Commit jedes genannten Items; Anlass
war Commit a3a867c. Der [Ablauf, Prozessphase Schritt 5](../../prozess/ablauf.md) nennt nur
`P<k>: …` und `Retro <n> P<k>: …`; er sagt nicht, dass ein Commit mehrere Items liefern darf,
wenn sie sich Dateien teilen. Zusätzlich schreibt der Fortschritt beim Beginn der nächsten
Phase der vorigen ihren Endstand; auch das steht im Ablauf (Fortschritt) nicht.

**Kosten.** Ohne den Satz wirkt die Prüfung gegen den Wortlaut des Ablaufs.

**Gegenvorschlag.** In Schritt 5 nach „einen Zwischenstand mit `P<k> Zwischenstand: …`“:
„Items, die sich Dateien teilen, liefert ein Commit `P<j>, P<k> und P<l>: …`.“ Im Abschnitt
Fortschritt: „Beginnt die nächste Phase, erhält die Datei der vorigen ihren Endstand.“

**Stellungnahme.** Angenommen (Retro 6, P1), beide Sätze wie vorgeschlagen:
[Ablauf, Prozessphase](../../prozess/ablauf.md#prozessphase) Schritt 5 (Commit
`P<j>, P<k> und P<l>: …`, Mechanismus `hatItemCommit`), [Fortschritt](../../prozess/ablauf.md#fortschritt)
(Endstand der vorigen Datei), dazu [Commits](../../prozess/ablauf.md#commits) („mehrere mit
`P<j>, P<k> und P<l>: …`“). Bitte nachprüfen.
