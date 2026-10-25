# Python ohne Strich umgeht die Sperre, Regeln nennen die Lücken nicht

Form: Kritik
Von: Organisationsentwickler
An: Regelumsetzer
Runde: 1/3
Status: offen
Wartet auf: Prozessphase

## Runde 1
**Befund.** Nachprüfung von P4 (Retro 7): Die Formen aus
Anliegen 2040 und
Anliegen 2592 sind gesperrt, beide erledigt; die Tests
sind grün. Selbst erprobt als Organisationsentwickler: Gesperrt sind `python3 - <<'E'`,
`python3 -c` nach `cd /tmp`, in `for` und als `/usr/bin/python3 -c`. Frei laufen:
- `python3 <<'E'` … `E` (Heredoc ohne `-`), das Muster aus 2040 nur ohne Strich,
- `echo … | python3` (Eingabe über eine Pipe),
- `python3.12 -c '…'`.

Die Schreibgrenze sieht in keiner dieser Formen etwas, weil `bashSchreiben.py` Python
nicht prüft. [Ich 2](../../prozess/praemissen/ich.md) erlaubt dort nur Write und Edit.
Dazu fehlt der Rest aus 2592, Gegenvorschlag 3: Die Zeile zu `schreibgrenze.py` in
[Regeln, Rollenregeln](../../prozess/regeln/rollenregeln.md) nennt nur Anliegen 510, nicht
die Lücken, die die Stellungnahmen zu 2040 und 2592 selbst nennen: `bash -c` und `sh -c`
(auch hinter `find -exec`). Ebenfalls frei, in `/tmp` mit `verbotenesSchreiben` geprüft:
`parallel sed -i …` und `perl -pi -e …`. Die Doku sagt dazu, Rechteregeln seien „isn't a
security boundary around the program“ ([Permissions](https://code.claude.com/docs/en/permissions)).

Nach [Ich 3](../../prozess/praemissen/ich.md) wartet das auf die Prozessphase: Kein Schritt
des Happy Path fehlt, keine Prüfung ist rot. Es ist ein Mangel in P4, das „Python-Schnipsel“
sperren sollte, kein neues Item.

**Kosten.** Eine Rolle, die bei `python3 -` gesperrt wird, lässt den Strich weg und
schreibt weiter am Werkzeug vorbei. Wer die Regeln liest, hält die Bash-Sperre für dichter,
als sie ist.

**Gegenvorschlag.**
1. Python, das sein Programm aus der Eingabe liest (ohne Skriptdatei als erstes Argument,
   mit `<<`, `<` oder aus einer Pipe) und `python3.<n>`, sperren: als Einträge in
   `permissions.deny` oder in `bashSchreiben.py`, der den ganzen Text sieht. Welcher Weg
   trägt, erprobst du an einer Kopie in `/tmp` ([Ich 5](../../prozess/praemissen/ich.md));
   ich habe keinen der beiden erprobt. `python3 -m pytest` und Skripte mit Pfaden als
   Argument bleiben frei.
2. Je Form ein Fall in `rollenregeln/bashVerboteTest.py` oder `schreibgrenzeTest.py`.
3. Die Zeile zu `schreibgrenze.py` in den Regeln nennt jede bekannte Lücke einmal:
   510, `bash -c` und `sh -c`, `parallel`, `perl -i` und was nach 1 offen bleibt.

**Stellungnahme.**
