# AUF-16.5: Der neue Testname liest sich wie das Gegenteil von AUF-16.4

412 · Kritik · von Architekt (Technik) → Testautor (Technik) · Runde 1/3 · angenommen

## Runde 1
**Befund.** Commit 83a9901 benennt den zweiten Domänentest zu AUF-16.5 in
`testAuf16_5EineEinheitAufDerAblageDesSpielersAnDerReiheIstNichtWählbar` um
([loslassenOhneZielTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/loslassenOhneZielTest.py)).
„an der Reihe“ ist richtig (Anliegen 411), aber mit „am Zug“ fiel auch „des anderen“ weg.
Wörtlich sagt der Name jetzt: Jede *Einheit* auf der *Ablage* des *Spielers* an der Reihe ist
nicht wählbar. Das widerspricht AUF-16.4 zwei Tests darüber: Die Boyz von Spieler 1, der an der
Reihe ist, springen auf seiner eigenen *Ablage* still zurück, ohne *Grund*. Was den Fall
ausmacht, steht nur im Körper: Die Necron Warriors gehören Spieler 2, also dem anderen
*Spieler*. Nach [Es](../../prozess/praemissen/es.md), Lesbarkeit, trägt der Name die
Bedeutung; hier muss man die Fixtures lesen, um ihn nicht falsch zu verstehen.

Beispiel: Ein Leser, der nur die Ausgabe von pytest sieht, findet nebeneinander
„Einheit auf der Ablage ihres Spielers steht wie davor“ (16.4) und „Einheit auf der Ablage des
Spielers an der Reihe ist nicht wählbar“ (16.5). Bei Spieler 1 an der Reihe ist das dieselbe
*Ablage*.

**Kosten.** Gering: ein Name. Ohne Änderung bleibt ein Testname, der dem Kriterium daneben
scheinbar widerspricht; die Prüfungen selbst sind richtig.

**Gegenvorschlag.** Bestehende Form, die das abdeckt: der Name von AUF-16.5 selbst, „auf der
*Ablage* des anderen *Spielers*“, den der erste Domänentest schon trägt.
1. (empfohlen) Umbenennen in
   `testAuf16_5EineEinheitDesAnderenSpielersAufDerAblageDesSpielersAnDerReiheIstNichtWählbar`.
   Aufbau und Prüfungen bleiben.
2. (Alternative) Beide Domänentests zu AUF-16.5 zu einem zusammenlegen, parametrisiert wie der
   Dienst-Test darunter (`ids=["boyzAufAblageVonSpielerZwei",
   "necronWarriorsAufAblageVonSpielerEins"]`), Name des ersten. Die Körper der Zeilen 113 bis
   120 und 126 bis 135 sind bis auf Einheit und *Spieler* gleich. Kosten: Der Fall „Boyz mit 0
   oder 3 gesetzten *Modellen*“ braucht dann eine zweite Achse, der Test wird schwerer zu lesen.
   Deshalb nur Alternative.

Den Fachkritiker betrifft das mit, weil der Name aus seinem Gegenvorschlag in 411 stammt.

**Stellungnahme.** Angenommen und umgesetzt, Option 1: Der Test heißt jetzt
`testAuf16_5EineEinheitDesAnderenSpielersAufDerAblageDesSpielersAnDerReiheIstNichtWählbar` in
[loslassenOhneZielTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/loslassenOhneZielTest.py).
Aufbau und Prüfungen unverändert. Die Zusammenlegung (Option 2) bleibt aus dem genannten Grund aus.
