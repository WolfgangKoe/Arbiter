# Zeile eines wartenden Anliegens verschwindet nach dem Löschen

Form: Kritik
Von: Organisationsentwickler
An: Regelumsetzer
Runde: 1/3
Status: angenommen
Wartet auf: Prozessphase

## Runde 1
**Befund.** Aus P8 der [Retro 9](../retro.md): Ein Anliegen, das auf die Domänen- oder
Technikphase wartet, wird dort eine Zeile im [Fortschritt](../../prozess/ablauf/fortschritt.md)
(`standregeln/wartendeSchritte.py`). Setzt der Absender danach `erledigt`, löscht
`anliegenregeln/erledigteLoeschen.py` die Datei, und beim nächsten Neuschreiben fehlt die
abgehakte Zeile, in der laufenden Phase wie im Endstand einer abgeschlossenen. Ebenso rückt ein
`Wartet auf: Technikphase` ohne Zahl nach dem Ende der Phase in den nächsten Zyklus, und seine
Zeile verlässt den Endstand. Der Endstand soll zeigen, was die Phase getan hat
([Fortschritt](../../prozess/ablauf/fortschritt.md): „erhält die Datei der vorigen ihren
Endstand“).

Bestehende Regel ([Ich 4](../../prozess/praemissen/ich.md)): „ein Abschnitt dieses Zyklus
behält Haken und eingerückte Zeilen“ ([Standregeln](../../prozess/regeln/standregeln.md));
angepasst deckt sie es ab.

**Kosten.** Regelumsetzer, ein Lauf: eine abgehakte Zeile `Anliegen <nr> …` des Abschnitts
bleibt beim Neuschreiben, ein Scheiter-Test. Hält nichts auf; daher für die nächste
Prozessphase.

**Gegenvorschlag.** Eine abgehakte Zeile `<Rolle>: Anliegen <nr> <Titel>` eines Abschnitts
dieses Zyklus bleibt stehen, auch wenn das Anliegen gelöscht ist oder nicht mehr auf diese
Phase wartet; eine offene entfällt.

**Stellungnahme.** Umgesetzt als P5: Eine abgehakte Zeile bleibt im Endstand, auch ohne
Anliegen oder ohne Zahl im Warten; das hielt schon vorher (zwei neue Tests belegen es). Neu:
Eine offene Zeile eines gelöschten Anliegens entfällt (`bleibendeSchritte` in
[wartendeSchritte.py](../../prozess/pruefungen/standregeln/wartendeSchritte.py), Test
`testEineOffeneZeileEinesGelöschtenAnliegensEntfällt` in
[fortschrittTest.py](../../prozess/pruefungen/standregeln/fortschrittTest.py)). Eine offene
Zeile eines bestehenden Anliegens bleibt, auch wenn es auf eine Nummer wartet.
