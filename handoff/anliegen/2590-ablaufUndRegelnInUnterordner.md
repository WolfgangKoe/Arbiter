# Ablauf und Regeln in einzelne Dateien in gleichnamigen Unterordnern

Form: Auftrag
Von: Stakeholder
An: Organisationsentwickler
Runde: 1/3
Status: offen

## Runde 1
**Befund.** Wortlaut des Stakeholders: „Bitte halte die für Prozessphase fest, dass wir
"ablauf.md" und "regeln.md" in einzelne Dateien aufteilen und in einen gleichnamigen
Unterordner legen. Die Dateien haben shcon für Text.“

Festgehalten vom Organisationsentwickler, umgesetzt wird in der Prozessphase.
Ablauf hat 33.664 Zeichen in 12 Abschnitten,
Regeln 33.772 Zeichen in 8 Abschnitten, je einer je Ordner unter
`prozess/pruefungen/`. Auf beide verweisen 41 Dateien, meist mit Anker
(`ablauf.md#anliegen`); 8 Prüfskripte und Tests nennen die Pfade.
Bestehende Regeln ([Ich 4](../../prozess/praemissen/ich.md)): die Höchstmaße der Dateien in der
[Definition des Organisationsentwicklers](../../.claude/agents/organisationsentwickler.md); für `ablauf.md` und `regeln.md` nennt keine Regel eines.

**Kosten.** Wer einen Abschnitt braucht, liest die ganze Datei mit über 33.000 Zeichen.

**Gegenvorschlag.** In der Prozessphase zu klären und als Prozess-Item in die Retro:
1. Was heißt „Die Dateien haben schon für Text.“? Vermutlich: Sie sind schon zu lang.
2. Schnitt: je Abschnitt eine Datei in `prozess/ablauf/` und `prozess/regeln/`, Höchstmaß je
   Datei und eine CLAUDE.md je Ordner nach Anliegen 255.
3. Verweise und Pfade in Prüfskripten umstellen; den Mechanismus baut der Regelumsetzer.

**Stellungnahme.** Umgesetzt in Retro 7, P2. Gelesen als „Die Dateien haben schon viel
Text“. Der [Ablauf](../../prozess/ablauf/) steht je Abschnitt in einer Datei, höchstens
6.000 Zeichen; der Abschnitt Anliegen ist deshalb zweigeteilt (Kopf, Status). Die
[Regeln](../../prozess/regeln/) stehen je Ordner der Prüfungen in einer Datei, höchstens
12.000, gekürzt auf 8.000. Jeder Ordner hat eine CLAUDE.md mit Format und Höchstmaß.
Prüfungen und Schreibrecht des Regelumsetzers auf die neuen Dateien folgen mit P8, die
Links in der Architektur zieht der Architekt nach; alles in einem Commit.
Kommentar: Ich nehme das Refactoring so ab. Bitte halte als Anliegen für die nächste Prozessphase fest, noch mal sorgfältig durch alle Regeln zu gehen inkl. der Ablaufdateien, ob man diese noch sinnvoll verschlanken kann. Vorsicht! So wie es jetzt läuft und lief, scheint es gut zu funktionieren. Das muss auf jeden Fall erhalten bleiben!. Sobald das Anliegen angelegt wurde, gib mir hier Bescheid und ich setze dieses hier auf "erledigt":
