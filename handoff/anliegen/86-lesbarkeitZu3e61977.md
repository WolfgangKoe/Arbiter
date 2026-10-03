# Lesbarkeit von 3e61977: Prozessverweise im Code, Doppeltes in regeln.md

86 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · angenommen

## Runde 1
Gegenstand: 3e61977, nur die geänderten Zeilen. Korrektheit: 87.

**Befund.**
1. [`wir.md`](../../prozess/praemissen/wir.md), Punkt 8, gilt auch für Prüfskripte:
   „Kommentare nur einzeilig … Docstrings höchstens einzeilig; kein … Prozessverweis.“
   Dagegen verstoßen:
   - `glossar.py`, Modul-Docstring mit acht Zeilen, „Regel: Anliegen 70, Retro 1 (P9).“
   - `rueckverfolgung.py`, Modul-Docstring mit 16 Zeilen, „Anliegen 52, Architektur T1“,
     „Anliegen 62“, „Anliegen 60“, „Anliegen 53, Architektur T2“.
   - `cspellTest.py`, Kommentar mit drei Zeilen, „(Anliegen 24)“.
   - `sprung/extension.js`, Zeile 1, „Anliegen 53, Weg C“.
   - mehrzeilige Docstrings in `codekritik.py` (Modul), `erledigteLoeschen.py`
     (`erledigteLöschen`) und `plan.py` (`itemsOhneLink`).
2. [`regeln.md`](../../prozess/regeln.md): „cSpell prüft kein Markdown“ und die
   Komplexitätsschwelle stehen je zweimal. Die alte Zeile zur Kritik am Code („ohne
   `Kritik <Hash>` im Betreff“) steht neben der neuen Zeile aus 78, die den Betreff
   `Kritik <a> <b>` regelt. „Kriterium ↔ Test, Fortsetzung“ ergänzt eine Zeile, statt sie zu
   ersetzen.
3. `rueckverfolgung.py`, `umfasst`: Je fehlendem Kriterium laufen ein ganzes `git log` und das
   Lesen aller Items erneut. Das geschieht in `verstöße` und in `wartende`, also auch im Stand
   nach jedem Rollenlauf. `anforderungenMitTestdatei` liest `kriterien()` je Anforderung neu.
   Heute ist das billig (0,14 s), es wächst aber mit der Zahl der Kriterien mal der Zahl der
   Commits.

**Kosten.** Zu 1: Wird ein Anliegen erledigt, zeigt „Anliegen 70“ ins Leere, denn
`linksErsetzen` erfasst nur Markdown-Links. Die Docstrings wiederholen auch Regeln aus
`ablauf.md` und `regeln.md` (in `codekritik.py` den Abschnitt Kritik am Code). Ändert sich
eine Regel, veralten sie unbemerkt. Zu 2: „Jede Aussage steht genau einmal“ (CLAUDE.md). Wer
`regeln.md` liest, bekommt zwei Fassungen und weiß nicht, welche gilt. Zu 3: Gering, aber die
Arbeit liegt im Hook nach jedem Rollenlauf.

**Gegenvorschlag.**
1. Docstrings einzeilig, ohne Verweis auf Anliegen oder Retro. Woher eine Regel kommt, steht
   nur in `regeln.md`. Im Code höchstens `# Regel: <Fundstelle in ablauf.md oder
   architektur>`.
2. Je Mechanismus eine Zeile in `regeln.md`. Die alten Zeilen zu cSpell, Komplexität, Kritik
   am Code und Kriterium ↔ Test ersetzen, statt neue anzuhängen.
3. `freigegebenerPlan` und `offeneItemTexte` einmal je Lauf bestimmen und an `umfasst`
   übergeben, `kriterien()` einmal je Datei.

**Stellungnahme.** Umgesetzt: 1 Docstrings einzeilig und ohne Verweis in `glossar.py`, `rueckverfolgung.py`, `cspellTest.py`, `codekritik.py`, `erledigteLoeschen.py`, `plan.py`, `stand.py`, `sprung/extension.js`; `# Regel:` bleibt nur, wo eine Fundstelle gilt. Die älteren mehrzeiligen Modul-Docstrings (`schlussantwort.py`, `statusrecht.py`, `benennung.py` u. a.) gehören nicht zu 3e61977 und bleiben; ein Urteil, ob sie fallen, steht beim Reviewer. 2 `prozess/regeln.md`: je Mechanismus eine Zeile, die Zeilen zu cSpell, Komplexität, Kriterium ↔ Test, Höchstmaß und Kritik am Code ersetzt statt ergänzt. 3 `rueckverfolgung.py`: Itemtexte einmal je Lauf (`itemTexteDesFreigegebenenPlans`), `kriterien()` einmal je Datei (`zuordnungen`).
