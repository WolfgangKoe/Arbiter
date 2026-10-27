# Sollen 3780 und 3900 jetzt oder in der Prozessphase 8 bearbeitet werden?

Form: Fragen
Von: Regelumsetzer
An: Stakeholder
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** [3780](3780-restePruefcodeNach3301.md) (Reste im Prüfcode) und
[3900](3900-standNenntFalscheRolleFuerProzessItems.md) (der Stand nennt für Prozess-Items die
falsche Rolle) halten weder eine Prüfung rot noch einen Plan-Punkt der Items auf. Beide
ändern Hook-Code, den in der Technikphase alle Rollen nutzen. 3780 sagt selbst, er sei in
der Prozessphase ohnehin dran. Die Frage stand bisher nur in der Moderation (Anliegen 5040).

**Kosten.** Jetzt: Hook-Code ändert sich mitten in der Technikphase, ein Fehler träfe alle
laufenden Rollen. Prozessphase 8: Der Stand nennt bis dahin bei Prozess-Items die falsche
Rolle (3900).

**F1 · Wann bearbeitet der Regelumsetzer 3780 und 3900?**
- A: In der Prozessphase 8, im Strang der Moderation (3900, dann 3780). (Anliegen 5040)
- B: Jetzt, neben den Items der Technikphase. (neu)
- Empfehlung A: Kein Plan-Punkt hängt daran, und Hook-Code ändert sich nicht, während die
  Rollen damit arbeiten. Rückweg beider: die Änderung per `git revert` zurücknehmen.
Antwort: A

**Stellungnahme.** Antwort A umgesetzt: [3780](3780-restePruefcodeNach3301.md) und
[3900](3900-standNenntFalscheRolleFuerProzessItems.md) tragen `Wartet auf: Prozessphase 8`.
Nachgeprüft, damit erledigt.
