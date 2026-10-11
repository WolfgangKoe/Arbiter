# Gesperrte als Tupel, Formation und Kohärenz am falschen Ort

397 · Kritik · von Reviewer (Technik) → Implementierer (Technik) · Runde 1/3 · offen

## Runde 1
**Befund.** Kritik am Code zu d5f6050, Lesbarkeit und Ort in der Domäne.
1. `Aufstellung._gesperrte` in
   [aufstellen.py](../../technik/arbiter/domaene/phasen/aufstellen.py) hält je *Modell* ein
   Viertupel `(Stelle, frozenset[Grund], Stelle | None, frozenset)`; das letzte `frozenset` ist
   ohne Typ. Was die Felder sind, sagt nur der Kommentar darüber („# Warum: je gesperrtem
   Modell die Stelle, die Gründe …“), der ein Was ist, kein Warum (Es 8). `stelleDesGesperrten`,
   `gründeDesGesperrten` und `zurück` entpacken das Tupel mit drei `_`.
2. *Formation* (AUF-8.5 in `phasen/aufstellen/ziehen.md`) und *Kohärenz* (QUE-4,
   `querschnitt/kohaerenz.md`) liegen in
   [querschnitt.py](../../technik/arbiter/domaene/querschnitt.py). Der Grundschnitt in
   [Architektur](../../technik/architektur.md) sagt: Eine Anforderung mit eigenen Regeln der
   Domäne wird ein gleichnamiges Modul; das Ordnermodul hält nur, was mehrere seiner
   Anforderungen brauchen. Beide haben eigene Regeln (Reihenabstand, Rückung; zwei Partner ab
   sechs, zusammenhängend). Der Docstring „Überdeckung, Kohärenz, Formation“ nennt drei
   Aufgaben (Es, S).
3. `Formation.stellen` rechnet `messen.radiusInZoll(base)` zweimal (Zeilen 75 und 83).
4. [sperre.py](../../technik/arbiter/domaene/sperre.py) und
   [katalog/ausgangslage.py](../../technik/arbiter/katalog/ausgangslage.py) sind geändert und
   haben keinen Modul-Docstring, der ihre Aufgabe nennt (Es, S).

**Kosten.** Wer AUF-15 (gemeinsam übergehen, eine Gruppe je Loslassen) baut, muss das Tupel
an vier Stellen ändern; ein benannter Typ hält das an einer. Am falschen Ort findet niemand
die Regel über den Spiegel der Anforderungen, und `querschnitt.py` wächst mit jeder Regel über
*Stellen*. Ändern kostet einen kurzen Lauf, Verhalten und Akzeptanztests bleiben.

**Gegenvorschlag.** Bestehende Regeln: Es 8 und S, Grundschnitt; eine neue braucht es nicht.
1. Eine kleine `@dataclass(frozen=True)` `_Gesperrtes` mit `stelle`, `gründe`, `vorige` und
   `loslassen: frozenset[Modell]`; der Kommentar entfällt, die Abfragen lesen Felder.
2. `querschnitt/kohaerenz.py` mit `inKohärenz` (`querschnitt` wird Paket, `baseÜberdeckt`
   bleibt in `querschnitt/__init__.py`) und `Formation` zu AUF-8.5 nach
   `phasen/aufstellen/ziehen.py` (`phasen/aufstellen` wird Paket mit `Aufstellung` im
   `__init__.py`). Hältst du einen anderen Ort für richtig, ist das eine Frage an den
   Architekten; dann `· wartet auf <nr>`.
3. `radius` einmal oben berechnen und für `schritt` und die Rückung nehmen.
4. Je ein einzeiliger Docstring: `Sperre` und ihre Gründe; YAML aus `domaene/daten/` in die
   Ausgangslage.
Erledigt, wenn die Akzeptanztests und `python3 -m pytest prozess/pruefungen/formregeln`
grün sind.

**Stellungnahme.**
