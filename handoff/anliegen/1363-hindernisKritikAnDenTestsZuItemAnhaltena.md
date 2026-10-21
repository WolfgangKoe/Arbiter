# Hindernis: Kritik an den Tests zu Item anhaltenAnBases

1363 · Kritik · von Architekt → Testautor · Runde 1/3 · erledigt

## Runde 1
**Befund.** Die Seite wird nie gegen das Beispiel stelleBeimLoslassen.json geprüft (V10 verlangt page.route): ein Bildschirmtest in blockAlsGanzesTest.py fehlt, siehe Anliegen 1360. Das hält den Schritt „Kritik an den Tests zu Item anhaltenAnBases“ von Architekt im Fortschritt auf.

**Kosten.** Der Schritt bleibt offen, die Phase kommt nicht weiter.

**Gegenvorschlag.** Testautor beseitigt das Hindernis.

**Stellungnahme.** Beseitigt: Die zwei Bildschirmtests gegen das Beispiel stehen in
`blockAlsGanzesTest.py` (Anliegen 1360) und sind rot, weil die Seite die Abfrage nicht stellt.
