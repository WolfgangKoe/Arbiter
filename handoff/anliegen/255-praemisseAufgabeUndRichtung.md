# Prämisse: eine Aufgabe je Modul, Abhängigkeit in einer Richtung

255 · Fragen · von Organisationsentwickler (Prozess) → Stakeholder · Runde 2/3 · erledigt

## Runde 1
Wortlaut: `git show a82c85a:handoff/anliegen/255-praemisseAufgabeUndRichtung.md`.

**F1 · Was kommt in wir.md?** Empfohlen: Regel 10 (eine Aufgabe je Modul), Regel 11 (Abhängigkeit ohne Kreis).
Antwort: s. Stellungnahme

**Stellungnahme.** Grundsätzlich gehe ich bei A und C auf deine Frage mit. Ich habe die Sorge, dass wir nun an einem Punkt stehen, an dem wir darauf achten sollten, dass sich die CLAUDE.md im Wurzelordner und den Domänen, Technik und Prozess-Ordner in ein Regelwerk verwandeln, was nicht deren Absicht ist. Die CLAUDE.md sollte überall möglichst schlank konkret und kurz sein. SOLID würde ich in einer solchen Datei sehen, eine Regel allerdings nicht. Du beziehst dich ja bereits auf "wir.md" Es braucht hier vielleicht auch eine "ich.md", wobei diese das gewünschte Verhalten nach außen beschrieben (4 Quadranten-Modell nach Ken Wilber). Lange Rede kurzer Sinn. Mache dir hier mehr Gedanken, statt kurz etwas mit einem Pflaster zu versehen, was eine ganzheitliche Sicht benötigt. Bitte Konzept vorlegen und die Details bedenken. 

## Runde 2
**Befund.**
1. Die Wurzel-CLAUDE.md (2.041 Zeichen) trägt schon Regeln mit Mechanismus (Schlussantwort,
   Lesegrenze 4.000). Das Regelwerk wächst darunter: `ablauf.md` 20.896 Zeichen, 47-mal
   „Mechanismus“.
2. `wir.md` heißt „Sprache und Kultur“, regelt aber fast nur die Form des Codes.
3. Prämissen lädt niemand; fünf Agentendefinitionen verweisen auf `wir.md`.
4. Claude Code: `@import` lädt immer (Datei kürzer, Kontext nicht); `.claude/rules/` mit
   `paths:` lädt erst, wenn eine Rolle passende Dateien liest oder schreibt.

**Kosten.** Regeln an drei Orten; jede neue verlängert CLAUDE.md.

**Gegenvorschlag.** Je Quadrant ein Ort; CLAUDE.md nennt je eine Zeile Prinzip und Link.

Quadrant | Inhalt | Ort
---|---|---
Ich (einzeln, innen) | Haltung und Verhalten jeder Rolle: erfinde nichts, frag nach, kritisiere statt zu ändern, Schlussantwort | `praemissen/ich.md`
Es (einzeln, außen) | Handwerk: SOLID, S und D als Regel 10, 11; Lesbarkeit 1 bis 9 aus `wir.md` | `praemissen/es.md`
Wir (gemeinsam, innen) | Sprache: Deutsch, Glossar wörtlich, eine Aussage einmal, keine Historie | `praemissen/wir.md`
System (gemeinsam, außen) | Phasen, Status, Mechanismen | `ablauf.md`, `regeln.md`

Bei Wilber ist Verhalten außen (Es), Haltung innen (Ich); eine Rolle hat nur ihren Text,
daher beides in `ich.md`, das Handwerk eigens. Agentendefinitionen tragen nur, was die Rolle
allein betrifft. Prämissen höchstens 3.000 Zeichen; Kritik an `es.md` vom Architekten.
Verweise in Prüfskripten (`wir.md 8`) zieht der Regelumsetzer nach.

**F1 · Welche Ordnung?**
- A: Vier Quadranten wie oben.
- B: `ich.md` nimmt auch das Handwerk auf.
- C: SOLID in die Wurzel, Regeln 10, 11 in `wir.md` (Runde 1).
Empfehlung: A. Das Handwerk betrifft nur den, der Code schreibt oder prüft.
Antwort: A, allerdings fehlt mir da noch O, L und I von SOLID. Wir mögen da noch keine Regeln haben, aber die können hier schon mal angelegt werden.

**F2 · Wie erreichen die Prämissen die Rollen?**
- A: `ich.md` und `wir.md` per `@import` in der Wurzel; `es.md` als `.claude/rules/` mit
  `paths:` auf Code, nach einem Versuch, ob Subagenten sie laden (Schreibpfad für mich).
- B: Verweis in den Agentendefinitionen, wie heute.
Empfehlung: A. Was alle brauchen, lädt immer; das Handwerk dort, wo Code entsteht.
Antwort: .

**F3 · Was darf in einer CLAUDE.md stehen?**
- A: Ziel, Perspektiven, Format und Höchstmaß der Dateien des Ordners, Prinzip mit Link;
  keine Regel mit Mechanismus. Eine Prüfung meldet `Mechanismus:` in CLAUDE.md.
- B: Wie A, nur Text.
Empfehlung: A. Sonst wächst sie wieder.
Antwort: .

**Stellungnahme.**

**Nachprüfung (Organisationsentwickler).** F1: `ich.md`, `es.md` (mit O, L, I), `wir.md`;
Verweise zeigen auf `es.md`. F2: Import in CLAUDE.md, `.claude/rules/es.md`; die Verweise der
Agentendefinitionen bleiben bis zur Messung. F3: meine Definition, `domaene/CLAUDE.md`.
Rest: Anliegen 276. Erledigt.
