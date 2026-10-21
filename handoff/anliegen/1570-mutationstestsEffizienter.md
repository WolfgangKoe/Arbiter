# Mutationstests effizienter

1570 · Auftrag · von Stakeholder → Organisationsentwickler · Runde 1/3 · offen · wartet auf die Prozessphase

## Runde 1
**Befund.** Mutationstests sind mir sehr wichtig, weil sie Lücken in den Tests und toten
Code finden. Sie sollen effizienter werden: schneller, parallel oder gezielter. Läuft nach
einem Mutationslauf keine Änderung mehr, soll der komplette Lauf nicht noch einmal nötig
sein. Anlass: In Zyklus 6 lief die Nachprüfung von
Anliegen 1550 durch den Reviewer über 57 Minuten, davon ein
Lauf, der die überlebenden Mutanten gegen alle Akzeptanztests startet. Heute baut das
Werkzeug Fehler in alle seit der jüngsten `Freigabe Plan` geänderten Domänenmodule und
lässt je Mutant Einheits- und Akzeptanztests laufen
([Regeln, mutationsregeln](../../prozess/regeln.md#mutationsregeln),
`prozess/pruefungen/mutationsregeln/`).

**Kosten.** Ein Lauf von fast einer Stunde hält Reviewer und Koordinator auf und lädt dazu
ein, ihn auszulassen; dann bleiben Lücken und toter Code unentdeckt.

**Gegenvorschlag.** Fragen an die Prozessphase; den Mechanismus baut der Regelumsetzer:
1. Laufen je Mutant nur die Tests, die die mutierte Zeile ausführen?
2. Entstehen Mutanten nur im geänderten Code statt im ganzen geänderten Modul, und gilt ein
   Ergebnis weiter, solange sich Modul und Tests seit dem letzten Lauf nicht geändert haben?
3. Lassen sich die Mutanten auf mehrere Prozesse verteilen, ohne dass sie sich gegenseitig
   stören (eigene Kopie, eigene Ports, eigener Browser)?
4. Welchen Anteil an der Laufzeit haben die Bildschirmtests, und gehören sie in den Lauf?
5. Wann ist der Lauf im Ablauf nötig: je Item vor dem Review, bei der Nachprüfung, nur für
   Geändertes ([Ablauf, DoD](../../prozess/ablauf.md#dod-item-fertig))?

**Stellungnahme.**
