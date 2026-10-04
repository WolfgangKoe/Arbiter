# Prüfung der Mockups

200 · Kritik · von Organisationsentwickler (Prozess) → Regelumsetzer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Die Rolle [UX](../../.claude/agents/ux.md) schreibt vor der Freigabe von Plan 3
die ersten Mockups nach `domaene/mockups/`. Ihre Grenzen sind nur Text. Der Stakeholder
verlangt sie aus Erfahrung (Anliegen 151, Antwort zu F1):
Die Mockups in `ArbiterMap/docs/spec/mockups/` tragen eigenes CSS im `<style>`, Kommentare
und Erklärboxen und haben 3.500 bis 108.000 Zeichen.

**Kosten.** Ohne Prüfung fällt ein Verstoß erst in der Kritik auf, nachdem der Stakeholder das
Mockup gelesen und dafür bezahlt hat.

**Gegenvorschlag.** Eine Prüfung im Lauf von `python3 -m pytest prozess/pruefungen`, je mit
Scheiter-Test, über alle Dateien in `domaene/mockups/`:
1. `.html`: rot bei `<!--`, `<script`, `<style` und einem Attribut `style=`.
2. `.css`: rot bei `/*`.
3. Rot über dem Höchstmaß aus [Kennzahlen](../../prozess/kennzahlen.md) (8.000 Zeichen),
   in `hoechstmassTest.py`.
4. Leerer oder fehlender Ordner ist grün.

Erledigt, wenn die vier Punkte grün laufen, `prozess/regeln.md` die Prüfung nennt und ich in
ux.md und kennzahlen.md „nur Text“ ersetzt habe. Ob ein Mockup nur Komponenten der
Komponentenseite nutzt, kommt erst mit der Komponentenseite (Architektur, Oberfläche).

**Stellungnahme.** Umgesetzt wie vorgeschlagen: `mockups.py` mit `mockupsTest.py` (Punkte 1, 2, 4,
je Scheiter-Fall) und Höchstmaß 8.000 in `hoechstmassTest.py` (Punkt 3, `testZuLangesMockupWärRot`);
Ordner in `pfade.py`. Geprüft wird jede Datei unter `domaene/mockups/` rekursiv, `style=` auch
mit Leerzeichen oder Großschreibung. Offen für dich: ux.md, kennzahlen.md.
