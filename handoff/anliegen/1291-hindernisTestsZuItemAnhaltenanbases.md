# Hindernis: Tests zu Item anhaltenAnBases

1291 · Kritik · von Testautor → Testautor · Runde 1/3 · angenommen

## Runde 1
**Befund.** Offen: 26.2 bis 26.4 stehen in anhaltenAnEinerBaseTest.py (ruff E501 und Format noch beheben; Hilfe anhalten.py; Fixture andereEinheitAufgestellt in conftest.py). AUF-24.1 fehlt in blockAlsGanzesTest.py: Abfrage stellenBeimLoslassen mit drei gesetzten Boyz (21.1, 21.2, fremde Base), Dienst samt Beispiel stelleBeimLoslassen.json, Seite mit haltenUndLosslassen. Danach Rotprüfung, ruff, prozess/pruefungen, abhaken Das hält den Schritt „Tests zu Item anhaltenAnBases“ von Testautor im Fortschritt auf.

**Kosten.** Der Schritt bleibt offen, die Phase kommt nicht weiter.

**Gegenvorschlag.** Testautor beseitigt das Hindernis.

**Stellungnahme.** Beseitigt. Die Tests zu 24.1 und 26.2 bis 26.4 stehen, ruff und Format sind sauber, `prozess/pruefungen` ist grün (739 bestanden). Die Kommentarform in `anhalten.py` ist behoben. Von 158 Tests der zwei Dateien sind 152 rot: Es fehlen `stellenBeimLoslassen`, `ebeneWählen`, die Antwort des Dienstes auf `stelleBeimLoslassen` und das Setzen durch `modellLoslassen`; Seite und Dienst scheitern daran, nicht am Test. Die 6 grünen sind Wächter: Zwei prüfen AUF-26.1 (Base berührt die Zonengrenze), vier AUF-26.2 (Ziel frei oder nur berührt: nicht anhalten). Die Rot-Gründe von 24.2 sind fehlender Code (Block rückt nicht), nicht meine Änderung. Die offene Frage, ob eine Strecke über eine Base mit freiem Ziel anhält, steht in Anliegen 1320.
