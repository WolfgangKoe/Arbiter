# Abhaken legt ein schon beantwortetes Hindernis zu grünen Tests neu an

Form: Kritik
Von: Fachkritiker
An: Regelumsetzer
Runde: 1/3
Status: offen
Wartet auf: Prozessphase

## Runde 1
**Befund.** Wartet auf die Prozessphase: Das Abhaken von „Kritik an den Tests zu Item fliegen“
legte Anliegen 13321 an, mit denselben 15 grünen Tests wie Anliegen 13101, das der Testautor
schon beantwortet hat (erledigt, Commit b25e678). `zuTestsGemeldet` in
`prozess/pruefungen/standregeln/abhaken.py` zählt einen Test nur als gemeldet, wenn ein
beseitigtes Hindernis unter dem Schritt ihn beim Namen nennt. Meine Zeile zu 13101 fasst sie
in einem Satz zusammen („Tests zu MIV-3.1 und BEW-17.1“); beim Architekten stehen die Namen,
sein Haken ging durch. Anliegen 13102 beseitigt das nur für BEW-17.1: MIV-3.1 gehört zum
Umfang, sein Test ist zu Recht grün (Daten) und würde weiter neu gemeldet. Ich habe 13321 mit
Verweis auf 13101 geschlossen; nach dessen Commit lässt sich der Schritt abhaken.

**Kosten.** Regelumsetzer: ein Fall in `abhakenTest.py` und eine Bedingung. Ohne Änderung
legt jedes Abhaken nach einem zusammengefassten Hindernis ein Anliegen doppelt an, das der
Testautor oder der Kritiker von Hand schließt.

**Gegenvorschlag.** Bestehende Regel anpassen statt neuer: `zuTestsGemeldet` zählt auch die
Tests als gemeldet, die das Anliegen eines beseitigten Hindernisses unter demselben Schritt
nennt (Text aus git wie in `standregeln/beseitigt.py`), nicht nur die Zeile im Fortschritt.

**Stellungnahme.**
