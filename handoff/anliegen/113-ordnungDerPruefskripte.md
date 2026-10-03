# Ordnung der Prüfskripte

113 · Fragen · von Organisationsentwickler (Prozess) → Stakeholder · Runde 1/3 · offen

## Runde 1
**Befund.** Zu [107](107-kritikAnDenPruefungen.md): In `prozess/pruefungen/` liegen 48 Dateien
nebeneinander: Hooks, Prüfungen im pytest-Lauf, Befehle (`kennzahlen.py`, die Spur), gemeinsame
Module, ihre Tests, eine Datenliste und die VS-Code-Erweiterung `sprung/`. Wonach geordnet wird,
entscheidest du; die Umsetzung steht in [114](114-pruefskripteOrdnenUndLesbarMachen.md).

**F1 · Wonach ordnen?**
- A: nach Thema, wie die Regeln in `prozess/regeln.md`:
  - `anliegen/`: anliegen, anliegennummer, statusrecht, erledigteLoeschen
  - `rollen/`: agenten, schreibgrenze, lesegrenze, bashPositivliste, schlussantwort,
    rollenkontext, belegung
  - `stand/`: stand, plan, codekritik, kennzahlen, rollenzaehler
  - `form/`: benennung, glossar, hoechstmass, komplexitaet,
    konfiguration, cspell, einstellungen
  - `rueckverfolgung/`: rueckverfolgung, die Spur, `sprung/`
  - `gemeinsam/`: gitAufruf, Ein- und Ausgabe der Hooks, Pfade des Repos
- B: nach Art: `hooks/`, `pruefungen/` (pytest-Lauf), `befehle/`, `gemeinsam/`. Ein Modul wie
  `anliegen.py` ist Prüfung und Baustein des Stands zugleich; es müsste geteilt oder
  willkürlich einsortiert werden.
- C: flach lassen, nur `regeln.md` als Übersicht. Das behebt die Unübersichtlichkeit nicht.

Empfehlung: A. Du suchst nach der Regel, nicht nach dem Hook-Ereignis; `regeln.md` gliedert
sich in dieselben Abschnitte und führt dich zum Ordner.

Antwort: .

**F2 · Wo liegen die Tests?**
- A: neben dem Modul (`anliegen/statusrecht.py`, `anliegen/statusrechtTest.py`). Je
  Themenordner drei bis dreizehn Dateien; Skript und Scheiter-Test stehen zusammen.
- B: je Themenordner ein Unterordner `tests/`. Halb so viele Dateien im Blick, eine Ebene mehr.

Empfehlung: A. Der Scheiter-Test gehört sichtbar zu seinem Mechanismus
([Regelumsetzer](../../.claude/agents/regelumsetzer.md)).

Antwort: .
