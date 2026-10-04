# SonarLint-Namensregeln auch in VS Code abschalten?

182 · Fragen · von Regelumsetzer (Prozess) → Stakeholder · Runde 1/3 · angenommen

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
