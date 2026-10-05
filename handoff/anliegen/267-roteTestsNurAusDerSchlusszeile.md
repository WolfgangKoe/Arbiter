# Rote Tests nur aus der Schlusszeile zählen

267 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
**Befund.** Kritik am Code von 0235e05. `roteTests` in
`prozess/pruefungen/formregeln/abdeckung.py:56` verspricht im Docstring „Summe aus `failed`
und `error(s)` der Schlusszeile von pytest“, sucht aber mit `re.findall` in der ganzen
Ausgabe. Bei roten Tests stehen dort Tracebacks, Assertions und die Kurzübersicht. Probe:
ein roter Test mit `assert f"{len(fehler)} errors" == "0 errors"` gibt die Schlusszeile
`1 failed in 0.02s`, `roteTests` liefert 7. Die Zahl landet in `aussetzung` und `verstoß`
(„7 Tests rot“). DoD 1 verlangt, dass die Prüfung „die Zahl der roten Tests“ nennt.
Ein Akzeptanztest, der Gründe oder Fehler zählt, schreibt solche Texte leicht.

Am Rand: `oberordner.py` importiert `ausgeschlosseneOrdner` aus `formregeln/benennung.py`,
eine Prüfung hängt damit an einer Konstante einer anderen. Der gemeinsame Ort wäre
`gemeinsam/pfade.py`, wo auch `frontendOrdner` steht. Das ist nur ein Hinweis, kein Teil der
Erledigt-Bedingung.

**Kosten.** Eine Zeile und ein Scheiter-Test. Ohne sie nennt die Prüfung in der
Technikphase eine falsche Zahl, und wer sie mit dem Lauf vergleicht, sucht Tests, die es
nicht gibt.

**Gegenvorschlag.** Nur die letzte nicht leere Zeile der Ausgabe auswerten, etwa
`re.findall(…, pytestAusgabe.strip().splitlines()[-1])`, bei leerer Ausgabe 0.
Scheiter-Test: eine Ausgabe mit `assert '2 errors' == '0 errors'` im Traceback und der
Schlusszeile `1 failed in 0.02s` ergibt 1.

Erledigt, wenn der Scheiter-Test grün ist und `python3 -m pytest prozess/pruefungen` grün
bleibt.

**Stellungnahme.**
