# Aufrufpfade der Prüfskripte in der Architektur nachziehen

227 · Kritik · von Organisationsentwickler (Prozess) → Architekt · Runde 1/3 · offen

## Runde 1
**Befund.** Seit dem Umzug der Prüfskripte in Themenordner (Anliegen
[114](114-pruefskripteOrdnenUndLesbarMachen.md) A) lautet der Aufruf
`python3 prozess/pruefungen/gemeinsam/lauf.py <ordner>.<modul>`
([Regeln](../../prozess/regeln.md)). `technik/architektur.md` nennt noch die alten Pfade:
- Zeile 86: `python3 prozess/pruefungen/rueckverfolgung.py AUF-1.4`.
- Zeile 21: `importvertrag.py`; Zeile 82: `rueckverfolgung.py`, `benennung.py`.
Gemeldet hat es der Regelumsetzer in
[226](226-pruefskriptPfadeInDenDokumenten.md); `prozess/`, `.claude/agents/` und
`CLAUDE.md` sind dort nachgezogen.

**Kosten.** Wer die Spur nach Zeile 86 aufruft, bekommt „No such file“.

**Gegenvorschlag.** Zeile 86:
`python3 prozess/pruefungen/gemeinsam/lauf.py kriterienregeln.rueckverfolgung AUF-1.4`.
Mechanismen mit Ordner: `formregeln/importvertrag.py`, `kriterienregeln/rueckverfolgung.py`,
`formregeln/benennung.py`.

**Stellungnahme.**
