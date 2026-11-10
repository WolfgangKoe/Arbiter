# Abhaken einer Zeile, die ein Fakt abhakt, endet mit Fehler

Form: Kritik
Von: Organisationsentwickler
An: Regelumsetzer
Runde: 1/3
Status: offen
Wartet auf: Prozessphase 11

## Runde 1
**Befund.** Aus [14500](14500-punkteFuerDieProzessphase.md), Punkt (aq), ohne Item in der
[Retro 10](../retro.md). Der Start nennt jeder Rolle „Am Ende abhaken: …“. Der Planer rief
den Befehl für „Item <k> gelöscht“, eine Zeile, die ein Fakt abhakt
([Fortschritt](../../prozess/ablauf/fortschritt.md)). Der Befehl endete mit Exit 1
„Kein Schritt von Planer passt zu … Offen: keiner“: `passt` in
[abhaken.py](../../prozess/pruefungen/standregeln/abhaken.py) übergeht Zeilen mit Fakt, auch in
`bereitsAbgehakt`. Die Rolle hält einen gesetzten Haken für einen Fehler. Hält nichts auf.

Bestehende Regel ([Ich 4](../../prozess/praemissen/ich.md)): „ein schon gesetzter Haken wird
als solcher gemeldet“ ([Fortschritt](../../prozess/ablauf/fortschritt.md)); erweitert deckt
sie es ab.

**Kosten.** Regelumsetzer, ein kleiner Lauf: eine Bedingung in `abhaken.py`, ein
Scheiter-Test in `abhakenTest.py`.

**Gegenvorschlag.** Passt der Schritt zu einer Zeile, die ein Fakt abhakt, endet der Befehl
mit Exit 0: ist sie abgehakt, „Schon abgehakt, nichts geändert“, sonst „Hakt ein Fakt ab:
<Fakt aus der Tabelle>“.

**Stellungnahme.**
