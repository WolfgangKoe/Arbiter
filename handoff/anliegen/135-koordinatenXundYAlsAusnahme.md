# Koordinaten x und y als Ausnahme von der Namenslänge

135 · Fragen · von Organisationsentwickler (Prozess) → Stakeholder · Runde 1/3 · offen

## Runde 1
**Befund.** [wir.md](../../prozess/praemissen/wir.md) 5 verlangt Namen mit mindestens 3
Zeichen; Ausnahmen entscheidest nur du. Die Architektur legt `Stelle(x, y)` fest
([S1](../../technik/architektur.md)), die Akzeptanztests rufen `Stelle(x=…, y=…)` auf.
`benennung.py` lässt deshalb `x` und `y` als Felder der Klasse `Stelle` zu, sonst nirgends
(Anliegen 128, in git). Entschieden hast du das nicht (Anliegen
[134](134-praemisseUndDodHinkenDenPruefungenNach.md), Punkt 1).

**Kosten.** Heute setzt die Prüfung eine Ausnahme durch, die wir.md nicht nennt. Wer wir.md
liest, hält `x` für einen Verstoß.

**Gegenvorschlag.** x und y sind die übliche Schreibweise für Achsen; die Ausnahme ist eng
(nur Felder von `Stelle`). Umbenennen änderte Akzeptanztests und S1.

**F1 · `x` und `y` als Felder von `Stelle` zulassen?**
- A: Ja. wir.md 5 nennt die Ausnahme, Mechanismus `benennung.py` (`koordinatenfelder`).
- B: Nein. Der Testautor benennt in den Tests um, der Architekt passt S1 an, der
  Regelumsetzer entfernt die Ausnahme.
Empfehlung: A.

Antwort: .
