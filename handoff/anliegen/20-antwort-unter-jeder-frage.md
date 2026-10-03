# Fragen an den Stakeholder: „Antwort: .“ unter jeder Frage

20 · Anliegen · von Stakeholder → Organisationsentwickler · Runde 1/3 · angenommen

Bearbeitung in der Retro von Zyklus 1.

## Runde 1
**Befund.** Notiz des Stakeholders, wörtlich: „Bei Fragen an mich, wäre als Default unter
jeder Frage ein "Antwort: ." gut. Dann kann ich das einfach ändern, ansonsten gilt eben "."
als Freigabe. das vergrößert die Zeichenmenge, sollte aber noch gehen.“
Heute ist das Format uneinheitlich: [Anliegen 15](15-aufstellen-begriffe-bereich-roll-off.md)
hat die Zeile unter jeder Frage, [16](16-aufstellen-ablage-beenden-uebergehen.md) nur einmal
am Ende, [09](09-fragen-freigabe-etappen.md) nur unter F10. Keine Agentendefinition, kein
Skill und keine Prüfung legt das Format fest.

**Kosten.** Je Frage rund 13 Zeichen. Anliegen 16 hat 2.356 von 2.400 Zeichen
(`prozess/pruefungen/test_hoechstmasse.py`, `ANLIEGEN`); mit vier Zeilen läge es darüber.
Dafür entfällt der Satz „Antwortest du „.“, gelten alle Empfehlungen.“ (rund 45 Zeichen),
weil „Antwort: .“ das je Frage sagt. Ohne festes Format sucht der Stakeholder, wo er antwortet,
und eine fehlende Zeile lässt offen, ob „.“ für diese Frage gilt.

**Gegenvorschlag.** Für die Retro von Zyklus 1:
1. Regel: Unter jeder Frage an den Stakeholder steht eine eigene Zeile `Antwort: .`; „.“ heißt,
   die Empfehlung gilt. Der Sammelsatz „Antwortest du „.“ …“ entfällt.
2. Ort: ein Skill „Frage an den Stakeholder“ mit Anliegen 15 als Beispiel und Anliegen 16 als
   Gegenbeispiel, verlinkt aus `planer.md` und `anforderungsautor.md`.
3. Mechanismus (Regelumsetzer): eine Prüfung in `prozess/pruefungen/`, die in jedem Anliegen
   mit „→ Stakeholder“ unter jeder `**F<n>`-Frage eine Zeile `Antwort:` verlangt, mit
   Scheiter-Test.
4. Höchstmaß: Zeilen `Antwort: …` zählen nicht zu den 2.400 Zeichen, damit die Antwort des
   Stakeholders kein Anliegen über die Grenze schiebt. Alternative: Grenze auf 2.600.

**Stellungnahme.** 1 angenommen, Regel in [`ablauf.md`](../../prozess/ablauf.md#anliegen).
3 angenommen als P6 der [Retro](../retro.md). 2 abgelehnt: Die Prüfung erzwingt die eine
Zeile, ein Skill kostet mehr. 4 entfällt: Anliegen haben heute 4.000 Zeichen.
