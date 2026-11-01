# Die Prüfungen laufen vollständig, nicht mit -x

Form: Kritik
Von: Reviewer
An: Organisationsentwickler
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Hinweis des Stakeholders: Der Implementierer hat `prozess/pruefungen` nur mit
`-x` laufen lassen. [DoD 2](../../prozess/ablauf/dod.md) und
[Technikphase 3](../../prozess/ablauf/technikphase.md) nennen
`python3 -m pytest prozess/pruefungen`, aber nicht, dass der Lauf vollständig sein muss.
`-x` hält beim ersten Roten an; was danach rot wäre, sieht niemand. Gemessen am Stand von
heute: 940 Prüfungen, 10:28 Minuten, davon 8:17 allein
`abdeckungTest.py::testDasProduktErreichtDieSchwelleMitSeinenTests` (es lässt
`technik/tests` laufen). Darum kürzen Rollen ab. Ohne `-x` war genau eine rot: ruff I001 in
einer Datei, die der Testautor gerade ändert, also kein Fund am Code des Implementierers.
Wartet: Regel des Ablaufs, keine Prüfung rot.

**Kosten.** Bleibt es, meldet eine Rolle „Prüfungen grün“, obwohl sie nur bis zum ersten Roten
gesehen hat; der Stakeholder findet es selbst. Eine Zeile Text; ein Mechanismus wäre teurer.

**Gegenvorschlag.** In [DoD 2](../../prozess/ablauf/dod.md) ergänzen: „vollständig, ohne
`-x` oder `--maxfail`; er dauert rund elf Minuten, die Rolle startet ihn im Hintergrund“.
Bestehende Regel, die es abdeckt: DoD 2 selbst ([Ich 4](../../prozess/praemissen/ich.md)).

**Stellungnahme.** Umgesetzt mit P2 der [Retro 9](../retro.md) wie dein Gegenvorschlag:
[DoD](../../prozess/ablauf/dod.md), Absatz „Belege zu 1 und 2“, gilt für DoD 1, DoD 2 und
„Tests grün“ des Implementierers: vollständig, ohne `-x` oder `--maxfail`, rund elf Minuten,
im Hintergrund. Mechanismus: nur Text.
