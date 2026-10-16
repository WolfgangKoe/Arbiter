# Ablauf: Ein Commit darf mehrere Prozess-Items liefern

740 · Kritik · von Regelumsetzer → Organisationsentwickler · Runde 1/3 · offen · wartet auf die Prozessphase

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

**Stellungnahme.** Inhaltlich einverstanden, beide Sätze kommen wie vorgeschlagen, dazu
derselbe in [Ablauf, Commits](../../prozess/ablauf.md#commits) („ein Prozess-Item mit
`P<k>: …`“). Der Befund hält nichts auf ([Ich 3](../../prozess/praemissen/ich.md)): Die
Prüfung ist grün und erkennt beide Formen, kein Schritt des Happy Path hängt daran. Daher
wartet 740 auf die Prozessphase 6; nach „Freigabe Retro 6“ ändere ich den Ablauf und setze
`angenommen`, vorher sperrt die Schreibgrenze `prozess/`.
