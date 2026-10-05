# Prämisse: eine Aufgabe je Modul, Abhängigkeit in einer Richtung

255 · Fragen · von Organisationsentwickler (Prozess) → Stakeholder · Runde 1/3 · offen

## Runde 1
**Befund.** Deine Kritik in [107](107-kritikAnDenPruefungen.md) (nicht SOLID) trifft Regeln,
die [wir.md](../../prozess/praemissen/wir.md) nicht hat: Sie regelt Namen, Kommentare und
die Form der Fälle, nicht den Zuschnitt der Module und die Richtung der Abhängigkeiten. Die
Befunde in [253](253-pruefskripteSolidUndLesbar.md) zeigen beides. Für das Produkt regelt die
Architektur die Richtung (Importvertrag A1, A2), für die Prüfskripte nichts. Von SOLID greifen
hier S und D; O deckt Regel 9 (Tabelle), L und I brauchen Klassenhierarchien.

**Kosten.** Ohne Prämisse meldet der Reviewer solche Verstöße nicht als Regelverstoß
(Retro 2, Befund 6), und nach dem Umbau wachsen sie nach.

**Gegenvorschlag.**

**F1 · Was kommt in wir.md?**
- A: Regel 10: Ein Modul hat eine Aufgabe, sein Docstring nennt sie (Urteil des Reviewers,
  Höchstmaß Code-Modul). Regel 11: Abhängigkeiten ohne Kreis, im Produkt nach der Architektur,
  in den Prüfskripten `gemeinsam` ← Lesen ← Regeln ← Stand (import-linter, 253).
- B: Nur Regel 11, sie ist prüfbar.
- C: „SOLID“ als Wort, ohne Ausprägung.
Empfehlung: A. C gibt dem Reviewer keinen Maßstab.
Antwort: .

**Stellungnahme.**
