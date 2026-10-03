# Ruff-Test nennt E37 statt des Ablaufs

89 · Kritik · von Organisationsentwickler (Prozess) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
Gegenstand: `prozess/pruefungen/konfigurationTest.py`, Folge von Anliegen 85.

**Befund.** Der Test heißt `testRuffEnthältDenWerkzeugsatzAusE37`. E37 steht nur in
`VORGEHEN.md`, das der Stakeholder löscht. Die Quelle des Regelsatzes ist nach 85 der Absatz
Werkzeuge in [`prozess/ablauf.md`](../../prozess/ablauf.md#technikphase); `prozess/regeln.md`
verweist schon dorthin.

**Kosten.** Nach dem Löschen nennt der Test eine Quelle, die niemand mehr findet; wer die
Regel nachschlagen will, landet in git.

**Gegenvorschlag.** Den Test nach dem Ablauf benennen, etwa
`testRuffEnthältDenWerkzeugsatzAusDemAblauf`. Erledigt, wenn `git grep E37 -- prozess` nichts
mehr findet.

**Stellungnahme.**
