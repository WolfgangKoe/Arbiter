# Prüfskripte ordnen und lesbar machen

114 · Kritik · von Organisationsentwickler (Prozess) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
**Befund.** Der Stakeholder findet sich in `prozess/pruefungen/` nicht zurecht und hält die
Skripte für schwer lesbar ([107](107-kritikAnDenPruefungen.md)). ruff, Komplexität und
Benennung sind grün; verletzt sind `prozess/praemissen/wir.md` und „Jede Aussage genau einmal“:
1. Fachobjekte als nackte Tupel, gelesen per Index (wir.md 6): `stand.py` `etappe[1]` und
   `lage` mit `tuple[int, str, str]`; `codekritik.py` `fällig[0]`, `fällig[1]`;
   `rueckverfolgung.py` `kriteriumsnummer = tuple[str, int, int]`, `fundstelle`, `stelle[1]`.
2. Typaliase kleingeschrieben (`anforderungsnummer`, `kriteriumsnummer`, `fundstelle`); Typen
   stehen in PascalCase (wir.md 1).
3. Erklärkommentar `rueckverfolgung.py:16` `# Art, Pfad, Zeile` (wir.md 8); er steht für einen
   fehlenden benannten Typ.
4. Das Hook-Protokoll baut jedes von neun Modulen selbst: `hookSpecificOutput`-Hüllen,
   `eingabe: dict` mit `eingabe["agent_type"]` und `(eingabe.get("tool_input") or {})`.
5. Pfade des Repos mehrfach als Literal: `technik/tests/akzeptanz` in `stand.py`,
   `benennung.py`, `rueckverfolgung.py`, `codekritik.py`; `handoff/anliegen` in `anliegen.py`,
   `bashPositivliste.py`, `benennung.py`, `erledigteLoeschen.py`.
6. Phasennamen als Literal, siebenmal (`"Domänenphase"`, …).
7. Module mit mehreren Aufgaben: `rueckverfolgung.py` (14.861 Zeichen: Prüfung, Spur,
   Kommandozeile), `stand.py` (Phasenfolge, Rollenläufe, Belegungstext, Hook-Ausgabe).

**Kosten.** Der Stakeholder kann die Mechanismen nicht nachprüfen. Eine Regel steht in
mehreren Modulen; ein Tupel-Index bricht still.

**Gegenvorschlag.** In der Prozessphase von Zyklus 2.
- A · Themenordner, Test neben dem Modul (Stakeholder, Anliegen 113): `anliegen/` (anliegen,
  anliegennummer, statusrecht, erledigteLoeschen), `rollen/` (agenten, schreibgrenze,
  lesegrenze, bashPositivliste, schlussantwort, rollenkontext, belegung), `stand/` (stand,
  plan, codekritik, kennzahlen, rollenzaehler), `form/` (benennung, glossar, hoechstmass,
  komplexitaet, konfiguration, cspell, einstellungen), `rueckverfolgung/` (mit Spur und
  `sprung/`), `gemeinsam/` (gitAufruf, Hook-Ein- und -Ausgabe, Pfade). Umzug: neue Datei,
  Einstellung, alte löschen (`einstellungen.py`). Querimporte ohne `sys.path`-Eingriff je
  Skript; den Weg wählst du, der Architekt kritisiert `pyproject.toml`. Scheiter-Test: kein
  Modul im Wurzelordner außer `conftest.py`. `prozess/regeln.md` gliederst du je Ordner.
- B · Lesbarkeit, Verhalten unverändert: 1 bis 7 beheben, etwa mit benannten Typen
  (`Kriterium`, `Lage`), je einem Modul für die Ein- und Ausgabe der Hooks und für die Pfade,
  einem Enum `Phase`; `rueckverfolgung.py` und `stand.py` nach Aufgaben teilen.
- C · Mechanismen mit Scheiter-Test für zwei Regeln, die heute nur Text sind: Kommentare und
  Docstrings nach wir.md 8 (nur `# Regel:` und `# Warum:`, Docstring einzeilig, kein TODO
  oder FIXME) und Typaliase in PascalCase (wir.md 1), Geltungsbereich nach wir.md. Den
  Vermerk in wir.md setze ich.
- D · erledigt: Rückstand der Benennung gelöscht (Datei, Funktionen, Tests, `regeln.md`).

Erledigt, wenn keine Fundstelle aus 1 bis 7 mehr besteht, D gelöscht ist, die Mechanismen aus C an je einem
Gegenbeispiel rot werden, `python3 -m pytest prozess/pruefungen` grün ist und der Reviewer den
Code geprüft hat ([Kritik am Code](../../prozess/ablauf.md#kritik-am-code)).

**Stellungnahme.** D und C umgesetzt (`kommentare.py`, PascalCase-Typaliase in `benennung.py`, je mit Scheiter-Test, `regeln.md`); aus B `Fundstelle` als NamedTuple und Aliase in PascalCase. A und B (1, 4 bis 7) stehen aus; A zieht den Pfad der Sprung-Erweiterung um, die der Stakeholder gerade erprobt (124). Status bleibt offen.
