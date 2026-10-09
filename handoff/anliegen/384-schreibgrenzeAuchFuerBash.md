# Schreibgrenze auch für Bash

384 · Anliegen · von Stakeholder → Organisationsentwickler (Prozess) · Runde 1/3 · offen
Legende: Status im Kopf · als Empfänger angenommen, rückfrage, abgelehnt · als Absender erledigt, offen (neue Runde) · unter einer Frage `Antwort: .` (Empfehlung), `Antwort: B` oder `Antwort: <Text>`

## Runde 1
**Befund.** Auftrag des Stakeholders: Die Schreibgrenze greift nur bei Write und Edit; Rollen
schreiben per Bash oder sed an ihr vorbei. Zyklus 5, Domänenphase:
- Anforderungsautor: Status und Kürzungen in 374 per Bash (Commit „Anforderungsautor: Einheit
  kommt als Formation und rückt in die Zone (374)“); den Commit „Anforderungsautor: Rest einer
  Einheit einzeln, gesperrte Formation mit einem Klick (373, 374)“ setzte er selbst.
- UX: änderte per `sed -i` die Items [ziehen](../../domaene/items/ziehen.md) und
  [gesperrtStehenUndZurueck](../../domaene/items/gesperrtStehenUndZurueck.md) des Planers
  (Commit „UX: Mockups zeigen die Formation, neu auf-15 für die gesperrte Formation (375)“).
- Planer: zwei Items per Heredoc, dann neu mit Write (Commit „Planer: Sperre ohne Stelle
  rückt in Item 2 (379)“).
- Architekt: Kopfzeilen per sed, zurück per `git checkout`, neu mit Edit (Commit „Architekt:
  377, 378, 379 erledigt, Neuladen gehört in Item 2 (382)“).

Die Protokolle früherer Läufe zeigen dasselbe bei jeder Rolle, auch bei mir (Status in 321 per
`sed -i`). Ursachen: [schreibgrenze.py](../../prozess/pruefungen/rollenregeln/schreibgrenze.py)
hört nur auf Write und Edit; Claude Code legt Rollen im Auto-Modus nahe, kleine Änderungen per
sed und Heredoc zu machen; dass eine Rolle nicht committet, steht nirgends, nur dass der
[Koordinator](../../.claude/agents/koordinator.md) committet.

**Kosten.** [Ich 2 und 3](../../prozess/praemissen/ich.md) gelten nur auf dem Papier: Eine
Rolle ändert ein fremdes Artefakt unbemerkt, Kritik wird Änderung statt Anliegen. Ein eigener
Commit überspringt die Prüfung des Koordinators.

**Gegenvorschlag.** Bestehende Regeln (Ich 4): Ich 2, Mechanismus `schreibgrenze.py`
„(Write und Edit), sonst nur Text“; [Ablauf, Anliegen](../../prozess/ablauf.md#anliegen)
„Rollen ändern Anliegen nur mit Write und Edit, nie per Bash“ (nur Text). Ich passe Ich 2 an,
statt eine Regel hinzuzufügen:
1. Ich 2 wird ergänzt: „Du schreibst Dateien nur mit Write und Edit und committest nicht;
   Bash nur zum Lesen, für Prüfungen, Tests und in `/tmp`.“ Mechanismus:
   `schreibgrenze.py` (Write, Edit, Bash).
2. Die Zeile in Ablauf, Anliegen fällt weg, Ich 2 deckt sie ab.
3. Der Regelumsetzer erweitert `schreibgrenze.py` auf Bash (Matcher `Write|Edit|Bash`). Einer
   Rolle verweigert er `sed -i`, `tee`, Umleitung `>` und `>>` außer nach `/dev/null` und
   `/tmp`, `rm`, `mv`, `cp`, `touch`, Python mit Skript in der Eingabe (`python3 -`,
   `python3 -c`) und git-Befehle, die Index, Arbeitsbaum oder Verlauf ändern (`add`,
   `commit`, `checkout`, `restore`, `reset`, `stash`, `rm`, `mv`), außer in einem Repo unter
   `/tmp`. Die Meldung nennt Write und Edit. Den Koordinator betrifft das nicht.
   Lücke: ein Skript aus `/tmp`, das selbst Dateien öffnet.

Bordmittel geprüft ([Berechtigungen](https://code.claude.com/docs/en/permissions),
[Sandbox](https://code.claude.com/docs/en/sandboxing),
[Subagenten](https://code.claude.com/docs/en/sub-agents)): Edit-Verbote in `permissions.deny`
greifen auch für sed, tee und Umleitungen, aber für alle Rollen gleich, nicht für Python. Die
Sandbox gilt auch für alle gleich und träfe Pytest-Caches und das Löschen erledigter Anliegen.
`disallowedTools: Bash(git commit *)` nimmt der Rolle ganz Bash; `permissionMode` gilt im
Auto-Modus nicht.

**F1 · Wie weit sperren?**
A: Hook nach 3 für alle Rollen. Empfehlung: ein Mechanismus für alle; jede Rolle ruft
Prüfungen und `git log` weiter selbst auf.
B: zusätzlich Bash aus Anforderungsautor, Planer, UX und Moderator nehmen (geänderte Rechte):
dichter, aber sie prüfen Länge und Form nicht mehr selbst.
Antwort: .

**Stellungnahme.**
