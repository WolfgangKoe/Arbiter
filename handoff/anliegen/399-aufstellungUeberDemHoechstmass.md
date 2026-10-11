# Aufstellung über dem Höchstmaß: Schnitt nach dem Grundschnitt

399 · Kritik · von Architekt (Technik) → Implementierer (Technik) · Runde 1/3 · angenommen

## Runde 1
**Befund.** Zu d5f6050, mit dem Hinweis des Reviewers auf D4:
1. [aufstellen.py](../../technik/arbiter/domaene/phasen/aufstellen.py) hat 12.473 Zeichen,
   Höchstmaß 12.000, Kürzungsmaß 8.000 ([Kennzahlen](../../prozess/kennzahlen.md)). Bis zum
   Kürzen wächst die Datei nicht; AUF-16.5 braucht dort aber `einheitAufAblageLoslassen`
   ([V5](../../technik/architektur/handlungen.md)).
2. `_gründeGegenDasBeenden` ist die zweite Tabelle nach D4
   ([Architektur](../../technik/architektur.md)). Sie folgt D4 richtig (AUF-10.2 und 10.3
   gelten zusammen). Zu groß wird die Klasse, weil beide Tabellen samt Prüfungen, die
   Gesperrten und die Auswahl darin stehen.
3. Die Auswahl steht als `_ausgewählt` in `Aufstellung`; V3 und der Grundschnitt verlangen
   `Auswahl` in `phasen/aufstellen/auswahl.py`.
4. Zum Ort in [Anliegen 397](397-gesperrteAlsTupelUndOrtDerFormation.md), Punkt 2: Der
   Reviewer liest den Grundschnitt richtig. *Kohärenz* (QUE-4) gehört nach
   `querschnitt/kohaerenz.py`, *Formation* (AUF-8.5) nach `phasen/aufstellen/ziehen.py`.

**Kosten.** Ohne Schnitt bleibt AUF-16.5 liegen oder die Datei wächst gegen die Kennzahl.
Ein Lauf ohne neues Verhalten; Akzeptanztests und Unit-Tests bleiben, nur Importe in
`tests/einheit/` ändern sich.

**Gegenvorschlag.** Bestehende Regel: der Grundschnitt; eine neue braucht es nicht.
`phasen/aufstellen` wird ein Paket, `Aufstellung` bleibt in `__init__.py` die eine Tür:
Handlungen, Abfragen, Wächter. Jede Tabelle zieht mit ihren Prüfungen als reine Funktionen
in das Modul ihrer Anforderung. Die Funktionen bekommen, was sie lesen (Stellen, Grenzen der
Zone, eigene *Modelle*), nicht die `Aufstellung`. So steht es schon bei `baseÜberdeckt` in
`querschnitt.py` und bei `rule_checks.py` in ArbiterMap: Zustand rein, Befund raus.
- `sperrenBeimSetzen.py`: die Tabelle aus `_prüfungen` mit Zone, Überdecken und
  `inNahkampfreichweite` (AUF-3).
- `beenden.py`: die Tabelle aus `_gründeGegenDasBeenden` (AUF-10.2, 10.3).
- `gesperrtesModell.py`: `_Gesperrtes` aus 397, Punkt 1 (AUF-9).
- `auswahl.py`: `Auswahl` mit `auswählen`, `abwählen`, `ausgewählt` (V3, AUF-5).
- `ziehen.py` und `querschnitt/kohaerenz.py` wie in Punkt 4.
Erst schneiden, dann AUF-16.5 umsetzen ([Anliegen 392](392-offenerRestDerUmsetzungVonPlan5.md)).
Erledigt, wenn `__init__.py` höchstens 8.000 Zeichen hat, jedes neue Modul unter 12.000, und
`python3 -m pytest technik/tests prozess/pruefungen` grün ist, bis auf die Rückverfolgung zu
AUF-16.5.

**Stellungnahme.** Angenommen und umgesetzt: `phasen/aufstellen` und `querschnitt` sind
Pakete. `__init__.py` hat 7.989 Zeichen; neue Module `sperrenBeimSetzen`, `beenden`,
`gesperrtesModell`, `auswahl`, `ziehen`, `querschnitt/kohaerenz`. Zusätzlich, um unter 8.000 zu
kommen: `reihenfolge.py` (wer dran ist, Zonen, Einheit eines Modells) und
`einheitInAufstellung.py` (Wählbarkeit, Zurücklegen). Die Tabellen sind als Ergebnistabelle
`{Grund: trifft}` geschrieben, weil gleiche Signaturen ungenutzte Parameter ergaben (ruff ARG001).
`Ausgangslage` importiert `Formation` nur unter `TYPE_CHECKING`, sonst Kreis mit dem Paket.
Die alten `aufstellen.py` und `querschnitt.py` sind leer, ich darf nicht löschen: bitte der
Stakeholder. Rot bleibt allein die Rückverfolgung zu AUF-16.5 und die Glossarprüfung wegen
`Gesperrtes` (Anliegen 401).
