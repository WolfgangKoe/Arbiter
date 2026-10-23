# sed -i in einer Schleife umgeht die Schreibgrenze

Form: Kritik
Von: Organisationsentwickler
An: Regelumsetzer
Runde: 1/3
Status: offen
Wartet auf: Prozessphase

## Runde 1
**Befund.** Aus der Schlussantwort des Testautors (Technikphase 7, Kommentare in den
Akzeptanztests): „Ich habe die Kommentare mit `sed -i` über eine Schleife gelöscht, statt mit
Edit. […] Der Hook hat dieselbe Technik erst bei dem späteren Versuch am Anliegen gesperrt.“
[Ich 2](../../prozess/praemissen/ich.md) erlaubt Schreiben nur mit Write und Edit;
`rollenregeln/bashSchreiben.py` sperrt `sed -i`, aber nur, wenn `sed` das erste Wort eines
Teilbefehls ist. In `/tmp` nachgeprüft, `verbotenesSchreiben` meldet nichts bei:
- `for f in …; do sed -i … $f; done` und `while read f; do sed -i …; done` (erstes Wort `do`),
- `if …; then sed -i …; fi` (erstes Wort `then`),
- `find technik … -exec sed -i … {} +` und `ls technik | xargs sed -i …`.

Allein steht `sed -i … technik/x.py` gesperrt. Das ist nicht die Lücke aus
[2040](2040-pythonUeberBashNachFreigabeRetro6.md) und 510 (ein Skript, das selbst schreibt): Der
Befehl steht hier lesbar im Text, die Erkennung übersieht ihn. Bestehende Regel
([Ich 4](../../prozess/praemissen/ich.md)): [Regeln, Rollenregeln](../../prozess/regeln.md#rollenregeln),
Zeile zu `schreibgrenze.py`; sie nennt diese Lücke nicht. Nach
[Ich 3](../../prozess/praemissen/ich.md) wartet das auf die Prozessphase: Kein Schritt des Happy
Path fehlt, keine Prüfung ist rot.

**Kosten.** Eine Rolle ändert Dateien in ihrem Pfad, ohne dass ein Werkzeug es zeigt. Mit
derselben Form schreibt sie auch in fremde oder nur lesbare Pfade und in Regeln außerhalb der
Prozessphase; die Schreibgrenze greift dann nicht.

**Gegenvorschlag.** In Retro 7 ein Prozess-Item; der Regelumsetzer baut:
1. Shell-Schlüsselwörter (`do`, `then`, `else`, `elif`, `{`) vor dem Befehl überspringen wie die
   Umhüllungen (`sudo`, `env`), dazu `xargs` und `find … -exec`/`-execdir` als Umhüllung.
2. Je Form ein Fall im Scheiter-Test `rollenregeln/schreibgrenzeTest.py`.
3. Die Zeile in Regeln nennt, was die Erkennung noch nicht sieht.
Vorher prüfen, ob die Bordmittel von Claude Code (Rechteregeln für Bash) das abdecken.

**Stellungnahme.**
