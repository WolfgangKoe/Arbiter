# CSRF-Ausnahme gilt über ihren Grund hinaus

270 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · angenommen

## Runde 1
**Befund.** Kritik am Code von 2635eb8. Nachgeprüft: `formregeln.sonarlint` meldet „keine
Funde“, `sonarlintTest.py` hat 25 Tests, alle grün.
1. `ausnahmen` (`prozess/pruefungen/formregeln/sonarlint.py:36`) nimmt `python:S4502` für
   die ganze Datei `technik/arbiter/web/anwendung.py` aus. Begründet ist das mit „nur
   GET-Routen“. Plan 4 soll aber Wählen per Klick bringen, also nach W3 die erste Handlung
   über HTTP und damit die erste Route, die den Zustand ändert. Dann gilt der Grund nicht
   mehr. S4502 meldet sich am `Flask(...)`-Aufruf, also an derselben Stelle wie heute, und
   die Ausnahme verschweigt den Fund. Keine Prüfung merkt das.
2. `testDieAusnahmenGeltenNurFürWebUndZweiRegeln` (`sonarlintTest.py:107`) schreibt die
   Liste `ausnahmen` ein zweites Mal ab. Jede neue Ausnahme ändert dann beide Stellen, und
   über die Gültigkeit sagt der Test nichts.
3. `# Warum: … Anliegen 261` (`sonarlint.py:34`) und `# Regel: Anliegen 261, …`
   (`sonarlintTest.py:93`) verweisen auf den Prozess, das untersagt `prozess/praemissen/wir.md` 8. Das
   Anliegen wird gelöscht, sobald es erledigt ist, und der Verweis führt dann ins Leere. Den
   Grund nennt der Kommentar schon selbst.

**Kosten.** 1: Ohne Auslöser fällt beim ersten POST weg, dass die Sperre mindestens so streng
ist wie SonarLint (Ablauf, Werkzeuge). Ob CSRF über `127.0.0.1` eine Rolle spielt, entscheidet
dann niemand. Dagegen stehen etwa fünf Zeilen Test. 2 und 3: jeweils ein bis zwei Zeilen.

**Gegenvorschlag.**
1. Die Ausnahme bekommt eine Bedingung, die eine Prüfung sichert. Zum Beispiel ein Test in
   `sonarlintTest.py`: Solange `("…/anwendung.py", "python:S4502")` in `ausnahmen` steht,
   gibt `anwendungFür(...)` nur Regeln mit den Methoden `GET`, `HEAD` und `OPTIONS` zurück
   (`anwendung.url_map.iter_rules()`). Dieser Test ersetzt Punkt 2. In
   [Regeln](../../prozess/regeln.md) steht als Auslöser: „fällt mit der ersten Route außer
   GET“. Die Entscheidung zu CSRF für Handlungen gehört dann zu W3; reiche sie an den
   Architekten weiter, falls du sie nicht selbst als Prüfung fassen kannst.
2. `testDieAusnahmenGeltenNurFürWebUndZweiRegeln` löschen, oder durch den Test aus 1 ersetzen.
3. In beiden Kommentaren „Anliegen 261“ streichen. Als Fundstelle für `# Regel:` nimmst du
   die Zeile in `prozess/regeln.md`.

Erledigt, wenn eine Route außer GET in `anwendung.py` eine Prüfung rot macht, solange die
Ausnahme besteht, die Liste nur noch an einer Stelle steht, die Kommentare kein Anliegen
nennen und `python3 -m pytest prozess/pruefungen` grün ist.

**Stellungnahme.**
Umgesetzt wie vorgeschlagen. 1: `sonarlintTest.py`, `testDieAusnahmeVonS4502GiltNurSolangeDieAnwendungKeineRouteAußerGetHat`
liest `anwendungFür(...).url_map` und ist rot, sobald eine Route außer GET, HEAD, OPTIONS besteht, solange
S4502 in `ausnahmen` steht; Scheiter-Probe `testEineRouteMitPostIstEineRouteAußerLesen`. Auslöser steht in
`prozess/regeln.md`. Die Entscheidung zu CSRF für Handlungen bleibt bei W3 (Architekt, nicht von mir als Prüfung
fassbar). 2: der abgeschriebene Listentest ist gelöscht. 3: „Anliegen 261“ aus beiden Kommentaren gestrichen,
Fundstelle ist `prozess/regeln.md`. Zur Node-Frage: Anliegen 280.
