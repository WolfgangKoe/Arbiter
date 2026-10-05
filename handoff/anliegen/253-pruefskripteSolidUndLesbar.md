# Prüfskripte: eine Aufgabe je Modul, Abhängigkeit in einer Richtung

253 · Kritik · von Organisationsentwickler (Prozess) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
**Befund.** Neubewertung von [107](107-kritikAnDenPruefungen.md) gegen `prozess/pruefungen`
(5a3e886). Liskov und Schnittstellentrennung greifen nicht (keine Klassenhierarchien). Offen:
1. Kreise zwischen Themenordnern: `standregeln` ↔ `rollenregeln` (`stand` → `belegung`,
   `rollenkontext` → `stand`), ↔ `anliegenregeln` (`stand` → `anliegen`, `statusrecht` →
   `freigabeKommentare`), ↔ `kriterienregeln` (`phasenfolge` → `rueckverfolgung` → `plan`).
   Neun Module importieren `rollenregeln.agenten` nur für `projektordner` oder `altbestandOrdner`.
2. Mehrere Aufgaben je Modul: `anliegen.py` (Kopf lesen und prüfen, Antworten, wer dran ist,
   Text für den Stand, Nummern), `bashPositivliste.py` (Shell zerlegen, Positivliste,
   Freigabe-Commit, Pfadsperren, git lesend), `statusrecht.py` (auch Plan, Review, Retro),
   `schreibgrenze.py` (Sperre, Bilanz bei Start und Stopp), `dashboard.py` (13.780 Zeichen:
   Gruppieren, SVG, HTML, CSS, Datei).
3. Anliegen 114 Punkt 4 halb: 14 Module lesen
   `eingabe.get("agent_type")`, `"tool_name"`, `"agent_id"`, `"hook_event_name"` selbst.
4. Doppelt: git per `subprocess` in `schreibgrenze.py`, `lesegrenze.py` neben `gitAufruf.py`;
   Pfad relativ zur Wurzel viermal (`statusrecht`, `schreibgrenze`, `bashPositivliste.meintPfad`,
   `gitAufruf.dateiBeiCommit`); `"handoff"` als Literal in neun Zeilen; zwei Wurzeln
   (`projektordner()`, `pfade.wurzel`; 232 nur `__file__`).
5. Fachobjekte als Tupel oder dict (wir.md 6): `freigaben` (`alle[0][0]`), `abschnitte`
   (`gefunden[-1][1]`), `Kriteriumsnummer = tuple[…]` mit freien Funktionen, Läufe in
   `dashboard.py` und `laufLog.py`; Status als Text in sechs Modulen, `/3` neben `höchstRunde`.
6. Fälle als Kette (wir.md 9): drei Pfadsperren in `bashPositivliste.entscheide`.
7. Regel im Test: `hoechstmassTest.py`, `komplexitaetTest.py`, `konfigurationTest.py`; zehn
   Testdateien bauen je ein eigenes git-Repo.

**Kosten.** Wer den Stand ändert, kann eine Sperre brechen; eine Regel steht nicht an einem
Ort. Etwa ein Lauf je Punkt; vor 215 bis 221, die dieselben Dateien anfassen.

**Gegenvorschlag.** Verhalten unverändert, je Punkt ein Commit:
1. Schichten `gemeinsam` ← Lesen (Anliegen, Artefakt, Plan, Kriterium, Agent) ← Regeln ←
   `stand`; `projektordner`, `nurLesbar` nach `gemeinsam`. Mechanismus: import-linter
   ([Backlog](../../prozess/backlog.md)), Scheiter-Test mit Rückimport; Regel: [255](255-praemisseAufgabeUndRichtung.md).
2. Nach Aufgaben teilen; der Docstring nennt die eine Aufgabe.
3. `HookEingabe` in `hookProtokoll.py`; Mechanismus: `eingabe.get(` nur dort.
4. git nur in `gitAufruf.py`; `relativZurWurzel`, `handoffOrdner` in `pfade.py`;
   Mechanismus: `subprocess` und `"handoff` nur dort.
5. NamedTuple `Freigabe`, `Abschnitt`, `Kriterium`, `Lauf`; Enum `Status`.
6. Pfadsperren als Tabelle (Prüffunktion, Meldung).
7. Regeln aus `*Test.py` in Module; Fixture `gitRepo` in `conftest.py`.

Erledigt, wenn kein Fundort aus 1 bis 7 bleibt, die Mechanismen aus 1, 3, 4 an je einem
Gegenbeispiel rot werden, `python3 -m pytest prozess/pruefungen` grün ist und der Reviewer
geprüft hat.

**Stellungnahme.** Teilstand: Punkt 6 umgesetzt (`pfadsperren` als Tabelle in
`rollenregeln/bashPositivliste.py`, Verhalten unverändert). Punkte 1 bis 5 und 7 offen; Status
bleibt `offen`.
