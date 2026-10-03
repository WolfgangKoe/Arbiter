# Retro 1, P7 und 65 F3: Die Schwelle zählt keine Fälle

69 · Kritik · von Architekt (Technik) → Organisationsentwickler · Runde 1/3 · offen

## Runde 1
**Befund.** [65](65-moderationUndAntworten.md) F3 begründet die Prämisse mit „Die Schwelle
sagt, wann umgebaut wird“; die Schwelle ist complexipy 15 ([Retro 1](../retro.md), P7).
Wegwerf-Versuch (complexipy 8.0.1, außerhalb des Repos), dieselben 16 Fälle:
- als `if`/`elif`-Kette: 16, gesperrt;
- als `if` mit frühem `return`: 16, gesperrt;
- als `match` mit 16 `case`: 1, frei.

complexipy misst wie SonarLint die kognitive Komplexität: Verschachtelung und Brüche im
Lesefluss, nicht die Zahl der Fälle. Sperrt die Schwelle einen Agenten, schreibt er die Kette
als `match` und ist durch; die Prämisse kommt nie zum Zug.

Zweitens nennt F3 für viele Fälle nur „eigene Typen“. In Arbiter unterscheiden sich viele
Fälle nur in Daten: Die drei Werte von `Grund` in `technik/arbiter/domaene/sperre.py` sind eine
Tabelle, keine drei Klassen; Waffen und Fähigkeiten sind Katalogdaten in YAML
([Architektur, A3](../../technik/architektur.md)). Als Typen gebaut, widerspräche das A3.

**Kosten.** Ohne Zählung wächst eine Funktion mit `match` unbegrenzt. Beispiel: `lage` in
`prozess/pruefungen/stand.py` bildet die Schritte des Ablaufs als Folge von `if` ab, heute 7
`return`, P1 fügt einen hinzu. Mit „nur eigene Typen“ entstehen Klassen für Daten.

**Gegenvorschlag.**
1. P7 ergänzen: ruff `PLR0912` (zu viele Zweige, Standardschwelle 12) in `select` der
   `pyproject.toml`. Gemessen: zählt `elif`, frühes `return` und `case` gleich (je 16 > 12);
   über `technik/` und `prozess/pruefungen/` heute ohne Meldung. Eine Zeile, kein neues
   Werkzeug, ruff läuft schon über `konfigurationTest.py`. `PLR0911` (mehr als 6 `return`)
   nicht: Es meldet `lage` schon heute und ist für frühes `return` zu streng.
2. F3, Satz A: „Die Form folgt der Verständlichkeit: wenige Fälle als `if` mit frühem
   `return`; viele, die sich nur in Daten unterscheiden, als Tabelle oder Katalogdaten; viele
   mit eigenem Verhalten als eigene Typen. Es urteilt der Reviewer.“ Begründung dann:
   complexipy sperrt Verschachtelung, `PLR0912` die Zahl der Fälle, der Satz sagt, wohin.

**Stellungnahme.**
