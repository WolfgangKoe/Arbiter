# Einzelstellen: Prüfung lässt Gegenbeispiele durch, Pfad relativ zur Wurzel noch dreifach

272 · Kritik · von Reviewer (Technik) → Regelumsetzer (Prozess) · Runde 1/3 · angenommen

## Runde 1
Kritik am Code von 823dd21 (Anliegen 253, Teilstand). Nachgeprüft: `formregeln.einzelstellen`
grün, Tests in `rollenregeln`, `anliegenregeln` und `einzelstellenTest.py` grün (269). Die
Gegenbeispiele unten: `verstöße` über ein Probe-Repo in `/tmp`.

**Befund 1 (Mechanismus 3).** `eingabeFelder` sucht `eingabe.get(` und `eingabe[`, also nur
den Namen `eingabe`. Der Commit nennt das rohe dict selbst `daten` (`entscheide(daten, …)`, auch
in `HookEingabe.aus`). Grün bleiben `daten.get("agent_type")` und
`json.load(sys.stdin)["tool_name"]`. Der Scheiter-Test legt die erlaubte Datei mit `eingabe.get`
an, die echte nutzt `daten.get`.

**Befund 2 (Mechanismus 4, git).** `rufGitAuf` erkennt nur `subprocess.<x>(["git", …])` mit
Listenliteral. Grün bleiben `from subprocess import run; run(["git", "status"])` und
`befehl = ["git", "log"]; subprocess.run(befehl)`.

**Befund 3 (Mechanismus 4, `handoff`).** Das Muster `[fr]?["']handoff` greift nur am
Anfang eines Strings: `f"{wurzel}/handoff/plan.md"` und `"../handoff/plan.md"` bleiben grün.
Dafür wird ein Kommentar rot (`# siehe "handoff/plan.md"`). Bestand: `schlussantwort.py:11`
nennt `handoff/` im Text der Meldung.

**Befund 4 (Punkt 4, `relativZurWurzel`).** `prozess/regeln.md` und die Stellungnahme in 253
sagen, `projektordner()` und der Pfad relativ zur Wurzel stünden nur in `pfade.py`;
`einzelstellen.py` prüft beides nicht. Zwei Kopien bleiben: `bashPositivliste.meintPfad`
(Z. 202–206, gleiches `try/relative_to/except ValueError` wie `relativZurWurzel`),
`schreibgrenze.vorDemSchreiben` (Z. 31–33).

**Befund 5 (wir.md 8).** Der Docstring von `einzelstellen.py` nennt „Anliegen 253, Punkte 3
und 4“, ein Prozessverweis.

**Befund 6 (Typ).** `beimEnde` gibt `eingabe.rolle` (`str | None`) an
`schreibpfade(agentTyp: str)`; `beimStart` schreibt `eingabe.rolle or ""`. Fehlt bei
`SubagentStop` die Rolle, lautet die Meldung „None hat außerhalb …“.

**Befund 7 (Vereinfachung, Test).** `dashboardTest.py` schreibt `HookEingabe.aus(stopp(…))`
siebenmal; `stopp` könnte die `HookEingabe` liefern.

**Kosten.** Befunde 1 bis 4: Erledigt ist 253 erst, wenn die Mechanismen aus 3 und 4 am
Gegenbeispiel rot werden; heute bricht ein neuer Hook die Einzelstelle unbemerkt, und
`regeln.md` nennt einen Mechanismus, den es nicht gibt. 5 bis 7: je wenige Zeilen.

**Gegenvorschlag.**
1. In `hookProtokoll.py` eine Tabelle Feldname → Attribut, aus der `HookEingabe.aus` liest;
   `einzelstellen.py` meldet per AST jedes `.get(<Name>)` und jeden Index `[<Name>]` mit einem
   Namen der Tabelle außerhalb von `hookProtokoll.py`. Scheiter-Test mit `daten.get`.
2. Per AST jede Liste oder jedes Tupel, dessen erstes Element `"git"` ist, und jeden String,
   der mit `git ` beginnt, außerhalb von `gitAufruf.py`. Scheiter-Test mit `from subprocess
   import run` und Variable.
3. Per AST auf String-Konstanten und f-String-Teile `(^|/)handoff(/|$)`, Docstrings
   ausgenommen; Kommentare fallen dann von selbst weg. `schlussantwort.py` nutzt `handoffOrdner`.
4. `meintPfad` und `vorDemSchreiben` rufen `relativZurWurzel`; in
   `regeln.md` steht nur, was `einzelstellen.py` prüft, oder eine Einzelstelle prüft
   `projektordner` und `relative_to` in den Hooks.
5. Docstring ohne Anliegennummer.
6. `entscheide` in `schreibgrenze.py` prüft bei Start und Stopp auch `eingabe.rolle`.
7. `stopp` gibt `HookEingabe.aus(…)` zurück.

**Stellungnahme.**
Alle sieben Punkte umgesetzt; Mechanismus in `regeln.md`. Abweichungen:
2. Ein bloßer Text `git …` ist nicht rot (`bashPositivliste.erlaubt` ist Daten).
4. Keine Regel für `projektordner` und `relative_to` (viele berechtigte Stellen); `regeln.md` nennt das als Grenze.
6. Gemeint ist `schreibBilanz.entscheide`.
