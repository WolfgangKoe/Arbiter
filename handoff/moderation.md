# Moderation

Stand: Zyklus 3, Technikphase, 30 Anliegen offen; [Plan 3](plan.md) ist freigegeben.

## Wartezeit
Git kennt nur drei Tage (2. bis 4.10.); gezählt nach Phasen.
- [107](anliegen/107-kritikAnDenPruefungen.md) und [114](anliegen/114-pruefskripteOrdnenUndLesbarMachen.md): seit 3.10., über zwei Phasen. Zugesagt für die Prozessphase von Zyklus 2. Es wuchsen Folgeanliegen (113, 225, 226, 227, 228 bis 232) und die Warteschlange des Regelumsetzers (20 Anliegen), die 114 hinter 215 bis 221 stellte (Moderation F2). 107 wartet auf 114.
- Stand 114: Umzug, B, C, D fertig; offen `regeln.md` je Ordner, Kritik am Code, Pfade ([226](anliegen/226-pruefskriptPfadeInDenDokumenten.md)). Die Datei hat 4.103 Zeichen, über der Grenze.
- Dein Hinweis (nicht SOLID, schlecht lesbar) hat in 107 niemand beantwortet.

## Dran
Blockiert den Implementierer bei QUE-2.1: [242](anliegen/242-eslintUndStylelint.md), [243](anliegen/243-befehlUndAbdeckungImEigenenProzess.md) (Regelumsetzer); [245](anliegen/245-schnittstelleDerBildschirmtests.md) (Architekt, Schnittstelle freigeben).
- Regelumsetzer: 114 zu Ende (läuft); danach die Folge unten.
- Organisationsentwickler: 107 neu bewerten, jetzt; 150 (wartet auf 216); 138 (nach 215); 219 (nach 220); 226 (nach 114).
- Architekt: 245; Kritik am Code 09a195e ist mit 247 eingegangen (Reviewer fertig).
- Testautor: [244](anliegen/244-nameDerEinheitFehltImGlossar.md) nachprüfen. Anforderungsautor: nichts offen.
- Stakeholder: [241](anliegen/241-frontendUndBackendParallel.md), [153](anliegen/153-frontendBackendUndDatenbank.md) und [246](anliegen/246-dashboardAlleSessionsMitSeitenzaehler.md) nachprüfen.

## Vorschläge
Reihenfolge Regelumsetzer, mit Parallelität zum Organisationsentwickler:
1. 114 Rest. Parallel bewertet der Organisationsentwickler 107 gegen den Code (SOLID, Lesbarkeit) und legt Befunde als neues Anliegen an den Regelumsetzer; kein Schreiben in Prüfskripten, also kein Konflikt.
2. Das Neue aus 107, solange die Skripte offen sind; sonst fassen 215 bis 221 sie noch einmal an.
3. 242, 243 (blockieren), mit 240.
4. 215, 216, 218, 220, 221; dann 229+232, 231+247 (`konfigurationTest.py`-Tabellen), 228+230.
5. 202 bis 206 (204 mit 205), 246.
Schließen: 107 nach 114 und Neubewertung; 138 nach 215; 226 nach 114; 219 nach 220 (je Organisationsentwickler).
Zusammen: 231, 232, 247 in einem Lauf.

## Fragen an dich
- [Moderation](moderation.md) F1: 107 und 114 vor 215 bis 221 (ändert deine Antwort auf F2 von vorhin)? 114 ist fast fertig, und die Lesbarkeitsarbeit gehört vor die Mechanismen, die dieselben Dateien anfassen. Empfehlung: ja.
- [Moderation](moderation.md) F2: 242 und 243 vor 215 bis 221, weil sie den Implementierer blockieren? Empfehlung: ja.
- [241](anliegen/241-frontendUndBackendParallel.md) F1 (A), F2 (A): beide offen. Empfehlung A und A.
- [153](anliegen/153-frontendBackendUndDatenbank.md) F1: `Antwort: .` steht noch; die Freigabe galt A. Bitte eintragen oder bestätigen. - Bestätigt.

Auch hier fehlt mir eine Möglichkeit, deine Empfehlung einfach anzunehmen oder zu korrigieren. ich habe oben einfach mal reingeschrieben. Wenn du das anders haben willst, bitte den Regelumsetzer, dies anzupassen.