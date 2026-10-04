# SonarLint-Namensregeln auch in VS Code abschalten?

182 · Fragen · von Regelumsetzer (Prozess) → Stakeholder · Runde 1/3 · beantwortet

## Runde 1
Aus Anliegen 181. Die Sperre schaltet die Namensregeln S100, S101,
S116, S117, S1542 und S1578 ab, weil [wir.md](../../prozess/praemissen/wir.md) 1 und 2 camelCase
entschieden haben. In deinem VS Code melden sie weiter: heute 276 Meldungen, unter denen die
8 echten Funde untergehen. `sonarlint.rules` gilt in der Erweiterung nur in den
Benutzereinstellungen, also für alle deine Projekte.

`python3 prozess/pruefungen/sonarlint.py --einstellung` gibt den Block aus, aus derselben
Liste wie die Sperre.

**F1 · Fügst du den Block in deine Benutzereinstellungen ein?**
- A: Ja. Die Sicht gleicht der Sperre; gilt auch für andere Projekte mit snake_case.
- B: Nein. Du siehst die Namensmeldungen weiter; die Sperre bleibt, wie sie ist.

Empfehlung: A, sonst geht jeder echte Fund unter.
Antwort: A, gib mir hier bitte genau an, was ich machen muss. 

## Anleitung zu A
Ich kann deine Benutzereinstellungen nicht ändern (liegen außerhalb des Projekts). Du:
1. In VS Code `Strg+Umschalt+P`, dann „Preferences: Open User Settings (JSON)“. Geöffnet wird
   `~/.config/Code/User/settings.json`.
2. Im Terminal im Projekt `python3 prozess/pruefungen/sonarlint.py --einstellung` ausführen
   und die Ausgabe ab `"sonarlint.rules"` bis zur schließenden Klammer des Eintrags kopieren,
   ohne die äußeren geschweiften Klammern.
3. In die Datei einfügen, direkt hinter die `{` oder hinter einen vorhandenen Eintrag (dort
   mit Komma trennen). Gibt es schon `"sonarlint.rules"`, deren Einträge zusammenführen.
4. Speichern. SonarLint neu laden: „Developer: Reload Window“.
5. Prüfen: In einer `.py`-Datei des Projekts zeigt das Problemfenster keine S100, S101,
   S116, S117, S1542, S1578 mehr (vorher 276 Meldungen).

Danach setze ich `erledigt`, wenn du es bestätigst.

Antwort: Ich habee die Einstellungen gesetzt. Bei mir sieht es gut aus. Prüfe es aber nochmal selbst. Danach ist es vermutlich erledigt. cSpell und Spellchecker geben noch Probleme aus. Stören die dich?
