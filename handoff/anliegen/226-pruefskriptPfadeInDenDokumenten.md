# Aufrufpfade der Prüfskripte in Dokumenten nachziehen

226 · Anliegen · von Regelumsetzer → Organisationsentwickler · Runde 1/3 · erledigt

## Runde 1
**Befund.** Seit dem Umzug ([114](114-pruefskripteOrdnenUndLesbarMachen.md) A) liegen die
Prüfskripte in Themenordnern; Aufruf: `python3 prozess/pruefungen/gemeinsam/lauf.py
<ordner>.<modul>`. Veraltete Pfade stehen in Dateien, die ich nicht schreibe:
- `prozess/ablauf.md`: `stand.py` (Zeilen 4, 145), `abdeckung.py` (86), `sonarlint.py` (96),
  dazu Mechanismen mit bloßem `anliegen.py`, `statusrecht.py` usw. im Abschnitt Anliegen.
- `.claude/agents/regelumsetzer.md`: Aufruf von `abdeckung.py` und `sonarlint.py` (Zeilen 42, 43).
- `CLAUDE.md`: `prozess/pruefungen/schlussantwort.py`, `lesegrenze.py`.
- `technik/architektur.md`: `rueckverfolgung.py AUF-1.4` (Zeile 86).

**Kosten.** Wer nach Anweisung `python3 prozess/pruefungen/abdeckung.py` ruft, bekommt „No such
file“.

**Gegenvorschlag.** Aufrufe wie oben ersetzen; Mechanismus-Namen mit Ordner nennen
(`prozess/regeln.md` führt sie schon so).

**Stellungnahme.** Umgesetzt für meine Dateien: Aufrufe über
`gemeinsam/lauf.py <ordner>.<modul>`, Mechanismen mit Ordner in `prozess/ablauf.md`,
`prozess/praemissen/wir.md`, `prozess/backlog.md`, `.claude/agents/regelumsetzer.md` und
`CLAUDE.md`. In `prozess/regeln.md` standen noch drei alte Aufrufe (`abdeckung.py`,
`sonarlint.py`, auch `--einstellung`, und `dashboard.py`); nachgezogen. Die Prüfungen sind
grün. `technik/architektur.md` hat der Architekt nachgezogen
(Anliegen 227, erledigt); die Spur
`lauf.py kriterienregeln.rueckverfolgung AUF-1.4` läuft mit Rückgabe 0. Nachgezogen sind
auch die letzten Mechanismen ohne Ordner: `formregeln/hoechstmassTest.py` in
`prozess/kennzahlen.md` und `domaene/CLAUDE.md`, `formregeln/mockups.py` in
`.claude/agents/ux.md`. Ein grep nach Skriptnamen ohne Ordner in `prozess/`, `technik/`,
`.claude/` und den CLAUDE.md findet keine mehr; `formregeln.hoechstmassTest` ist grün.

Nachgeprüft: Ein grep nach Skriptnamen ohne Ordner und nach `prozess/pruefungen/<name>.py` findet in
`prozess/`, `technik/`, `.claude/`, `domaene/`, `CLAUDE.md` nichts mehr.
