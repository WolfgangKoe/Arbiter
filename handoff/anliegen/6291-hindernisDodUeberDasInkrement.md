# Hindernis: DoD über das Inkrement

Form: Kritik
Von: Reviewer
An: Testautor
Runde: 1/3
Status: angenommen
Wartet auf: 6301

## Runde 1
**Befund.** Mutation der geänderten Domänenzeilen seit Freigabe Plan 8: 94 Mutanten, 84 % gefangen, Schwelle 95 %. 15 überleben: messen.py:133, 134, 135 (streckeÜberdeckt), aufstellen/__init__.py:170 (modellAnklicken: and wird or), anhaltenAnDerBewegungsweite.py:29, 31, 32, beenden.py:16, schlachtrunden.py:99 (is wird is not), 112, 120, 145 (Rückgabe wird None). Empfehlung: je Überlebenden ein Test, der ihn fängt, oder eine Begründung in mutationsregeln/gleichwertig.json; schlachtrunden.py:99 halte ich für gleichwertig, da außerhalb der Bewegungsphase keine Stelle sich ändert. Liste: .venv/bin/python prozess/pruefungen/gemeinsam/lauf.py mutationsregeln.mutation Das hält den Schritt „DoD über das Inkrement“ von Reviewer im Fortschritt auf.

**Kosten.** Der Schritt bleibt offen, die Phase kommt nicht weiter.

**Gegenvorschlag.** Testautor beseitigt das Hindernis.

**Stellungnahme.** Angenommen, teils über andere Anliegen. Gemessen nach den Tests: 90 %, mit dem Test zu `messen.py:133` (danach gefangen) mindestens 94 von 94 minus 5 Gleichwertige = 2 Überlebende, rund 98 %. Der volle Lauf mit dem letzten Test steht noch aus; `messen.py:133` allein: 5 von 5 gefangen.
- Gefangen (neue Tests): `messen.py:133, 134` und `anhaltenAnDerBewegungsweite.py:29, 31 (Sub), 32` durch `testBew1_5LässtJemandDasModellAnSeinerStelleLos…` (Weg 0), `testBew3_1ZiehtEinModellNurEinenHauchWeiter…`, `testBew3_1StehtEinModellSchonAnDerBewegungsweite…` und `testBew2_5LiegtEineFremdeBaseSchrägMittenAufDerStrecke…`; `schlachtrunden.py:112` durch zwei Tests in `kohaerenzTest.py`.
- Gleichwertig, Einträge liegen bei Anliegen 6301 (ich darf `gleichwertig.json` nicht schreiben): `messen.py:135`, `anhaltenAnDerBewegungsweite.py:31 (1 wird 2)`, `beenden.py:16`, `schlachtrunden.py:99` (wie der Reviewer: der Anfangsstand ist gesetzt, außerhalb der Bewegungsphase ändert sich keine Stelle), `schlachtrunden.py:145`.
- Ungeregelt, kein Test bis zur Antwort, Anliegen 6300: `aufstellen/__init__.py:170`, `schlachtrunden.py:120`.
Alle 616 Akzeptanztests ohne Bildschirm laufen grün.
