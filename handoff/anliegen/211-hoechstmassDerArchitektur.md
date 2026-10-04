# Höchstmaß der Architektur

211 · Kritik · von Organisationsentwickler (Prozess) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
**Befund.** Der Stakeholder hat in Anliegen 159 (F2: C) entschieden: Die
Architektur ist die Übersicht `technik/architektur.md` und je Thema eine Datei in
`technik/architektur/`, je Datei 6.000 Zeichen, zusammen 24.000. Den Schreibpfad trägt
[architekt.md](../../.claude/agents/architekt.md), die Maße stehen in
[Kennzahlen](../../prozess/kennzahlen.md) als nur Text. `technik/architektur.md` hat heute
5.998 Zeichen, 2 unter dem Höchstmaß; nichts würde rot, wenn sie darüber wächst.

**Kosten.** Ohne Prüfung wächst die Technik wie in ArbiterMap (vier Dateien, rund 75.000
Zeichen); das Gesamtmaß war im Anliegen der Grund, C statt `technik/*.md` zu wählen.

**Gegenvorschlag.** In `hoechstmassTest.py`, je mit Scheiter-Test:
1. Rot, wenn `technik/architektur.md` oder eine Datei in `technik/architektur/` über 6.000
   Zeichen hat.
2. Rot, wenn alle zusammen über 24.000 Zeichen haben.
3. Fehlender Ordner ist grün.

Die Prüfung ist sofort grün und wird sofort scharf; sie wartet nicht auf die Aufteilung
([212](212-architekturHatZeichenNichtBytes.md)).

Erledigt, wenn die drei Punkte grün laufen, `prozess/regeln.md` die Prüfung nennt und ich in
kennzahlen.md „nur Text“ ersetzt habe.

**Stellungnahme.**
