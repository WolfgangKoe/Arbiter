# Schreibgrenze auch für Bash

384 · Anliegen · von Stakeholder → Organisationsentwickler · Runde 1/3 · angenommen

## Runde 1
**Befund.** Auftrag des Stakeholders: Die Schreibgrenze greift nur bei Write und Edit; Rollen
schreiben per Bash oder sed an ihr vorbei. Zyklus 5, Domänenphase:
- Anforderungsautor: Status und Kürzungen in 374 per Bash; den Commit „Anforderungsautor: Rest
  einer Einheit einzeln, gesperrte Formation mit einem Klick (373, 374)“ setzte er selbst.
- UX: änderte per `sed -i` die Items [ziehen](../../domaene/items/ziehen.md) und
  [gesperrtStehenUndZurueck](../../domaene/items/gesperrtStehenUndZurueck.md) des Planers
  (Commit „UX: Mockups zeigen die Formation, neu auf-15 für die gesperrte Formation (375)“).
- Planer: zwei Items per Heredoc (Commit „Planer: Sperre ohne Stelle rückt in Item 2 (379)“).
- Architekt: Kopfzeilen per sed (Commit „Architekt: 377, 378, 379 erledigt, Neuladen gehört
  in Item 2 (382)“).

Frühere Läufe zeigen dasselbe bei jeder Rolle, auch bei mir. Ursachen:
[schreibgrenze.py](../../prozess/pruefungen/rollenregeln/schreibgrenze.py) hört nur auf Write
und Edit; Claude Code legt Rollen im Auto-Modus sed und Heredoc nahe; dass eine Rolle nicht
committet, steht nirgends.

**Kosten.** [Ich 2 und 3](../../prozess/praemissen/ich.md) gelten nur auf dem Papier: Eine
Rolle ändert ein fremdes Artefakt unbemerkt, Kritik wird Änderung statt Anliegen. Ein eigener
Commit überspringt die Prüfung des Koordinators.

**Gegenvorschlag.** Bestehende Regeln (Ich 4): Ich 2 und eine Zeile in
[Ablauf, Anliegen](../../prozess/ablauf.md#anliegen) („nie per Bash“, nur Text). Ich passe
Ich 2 an, statt eine Regel hinzuzufügen:
1. Ich 2 wird ergänzt: „Du schreibst Dateien nur mit Write und Edit und committest nicht;
   Bash nur zum Lesen, für Prüfungen, Tests und in `/tmp`.“
2. Die Zeile in Ablauf, Anliegen fällt weg, Ich 2 deckt sie ab.
3. Der Regelumsetzer erweitert `schreibgrenze.py` auf Bash (Anliegen 385). Den Koordinator
   betrifft das nicht.

Bordmittel geprüft ([Berechtigungen](https://code.claude.com/docs/en/permissions),
[Sandbox](https://code.claude.com/docs/en/sandboxing)): Beide gelten für alle Rollen gleich;
die Sandbox träfe auch Pytest-Caches und das Löschen erledigter Anliegen.

**F1 · Wie weit sperren?**
A: Hook nach 3 für alle Rollen. Empfehlung: ein Mechanismus für alle; jede Rolle ruft
Prüfungen und `git log` weiter selbst auf.
B: zusätzlich Bash aus Anforderungsautor, Planer, UX und Moderator nehmen (geänderte Rechte):
dichter, aber sie prüfen Länge und Form nicht mehr selbst.
Antwort: A

**Stellungnahme.** Nach A umgesetzt, 3 in Anliegen 385.
Kommentar: Bitte hier melden, sobald alles umgesetzt ist, damit ich das Anliegen auf "erledigt" setzen kann.
Stellungnahme: Alles umgesetzt, du kannst `erledigt` setzen.
Kommentar: Hier steht immer noch nicht, ob es umgesetzt ist
Stellungnahme: Ja, umgesetzt ist alles, was du mit A beauftragt hast, seit Commit
„Regelumsetzer und Organisationsentwickler: Schreibgrenze gilt auch für Bash (Anliegen 385,
384)“. Nichts davon ist offen:
1. Die Regel steht in [Ich 2](../../prozess/praemissen/ich.md): Eine Rolle schreibt Dateien
   nur mit Write und Edit und committet nicht.
2. Die doppelte Zeile im [Ablauf](../../prozess/ablauf.md#anliegen) ist gestrichen.
3. Die Sperre wirkt: Ändert eine Rolle eine Datei im Projekt per Bash (sed, Heredoc,
   Umleitung) oder committet sie, wird der Befehl abgewiesen, und sie liest „Nimm Write und
   Edit“. Den Koordinator trifft das nicht.

Bekannte Lücke: Ein Skript in `/tmp`, das selbst Dateien öffnet, erkennt die Sperre nicht
([Regeln](../../prozess/regeln.md#rollenregeln)). Dass Rollen seitdem nicht löschen können,
hast du in 418 entschieden; das baut der Regelumsetzer gerade.
