# pfadeTest.py löschen: Freigabe fehlt

188 · Fragen · von Regelumsetzer (Prozess) → Stakeholder · Runde 1/3 · offen

## Runde 1
**Befund.** P3 der [Retro 2](../retro.md) ist nicht umgesetzt. Der Auto-Mode-Klassifizierer
verweigerte `rm prozess/pruefungen/pfadeTest.py` als „Security Test Removal“; `git rm` ist
den Rollen ohnehin gesperrt. Ich habe nichts geändert und keinen anderen Weg versucht.

**Kosten.** Ohne Löschung bleibt die Prozesslast-Kennzahl (52 %) ohne gelöschten Mechanismus,
und der Test mit bekannter Lücke bleibt im Lauf von `python3 -m pytest prozess/pruefungen`.

**Gegenvorschlag.** Bleibt für die Löschung nach Freigabe:
1. `prozess/pruefungen/pfadeTest.py` löschen. Nur dieser Test nennt sich selbst, sonst
   verweist nichts auf ihn; `pfade.py` bleibt, mehrere Prüfungen nutzen es.
2. In `prozess/regeln.md` die Zeile „Ordner, die mehrere Prüfungen kennen, stehen nur in
   `pfade.py`“ entfernen. Die Regel steht nur dort.
3. `python3 -m pytest prozess/pruefungen`, `abdeckung.py`, `sonarlint.py` laufen lassen.
Ein Scheiter-Test entfällt, die Löschung entfernt den Mechanismus.

**F1 · Löschung freigeben?** Empfehlung: ja, Regelumsetzer führt sie aus.
Antwort: .

**Stellungnahme.**
