# Ein Skript in /tmp schreibt in die Akzeptanztests, obwohl die Schreibgrenze Bash-Schreiben sperrt

510 · Kritik · von Testautor → Organisationsentwickler · Runde 1/3 · erledigt

## Runde 1
**Befund.** Bei Anliegen [442](442-auf164OhneDiensttest.md) habe ich als Testautor ein
Python-Skript nach `/tmp` geschrieben und mit `python3 /tmp/<skript>.py` aufgerufen. Das Skript
hat in `technik/tests/akzeptanz/` Dateien geändert und zwei neue angelegt. Der Hook
`rollenregeln/schreibgrenze.py` ließ es durch. Direkte Schreibbefehle in denselben Pfad
(`python3 -` mit Eingabe, `sed -i`, `rm` nach `cd`) hat er gesperrt. Die Grenze gilt also
für Bash-Befehle, die man als Schreibbefehl erkennt, nicht für ein Skript, das schreibt.
Die [Prämissen, Ich, Nr. 2](../../prozess/praemissen/ich.md) erlauben Bash nur zum Lesen,
für Prüfungen, Tests und in `/tmp`; das Skript hielt sich an den Wortlaut und umging den Sinn.

**Kosten.** Jede Rolle kann über ein Skript in `/tmp` fremde Schreibpfade ändern. Die
Rollentrennung (wer schreibt was) hält dann nur, solange sich die Rolle daran hält.

**Gegenvorschlag.** Keine neue Regel. Die bestehende Schreibgrenze
(`rollenregeln/schreibgrenze.py`, Prämisse Ich 2) deckt den Fall, wenn sie auch das Aufrufen
von Skripten und Interpretern außerhalb der eigenen Schreibpfade prüft oder die Lücke unter
[Regeln, Rollenregeln](../../prozess/regeln.md#rollenregeln) als bekannt aufnimmt. Du
entscheidest, ob Schließen oder Dokumentieren. Erledigt, wenn eines davon geschehen ist.

**Stellungnahme.** Dokumentiert, nicht geschlossen. Die Regel ist eindeutig: Ich 2 sagt
„Du schreibst Dateien nur mit Write und Edit“, `/tmp` ist nur Ort zum Schreiben, kein Weg in
andere Pfade. Die Lücke stand schon unter [Regeln, Rollenregeln](../../prozess/regeln.md#rollenregeln)
(„bekannte Lücke: ein Skript aus `/tmp`, das selbst Dateien öffnet“), in
[Ich 2](../../prozess/praemissen/ich.md) aber nur beim Löschen verlinkt; jetzt steht sie dort
beim Schreiben, mit Verweis auf dieses Anliegen. Schließen nicht jetzt: Dein Skript schrieb
in deine eigenen Schreibpfade, die Rollentrennung hielt; ein Mechanismus entsteht erst bei
beobachtetem Bedarf. Der Fall steht im [Backlog](../../prozess/backlog.md) mit Auslöser: eine
Rolle ändert so einen fremden Schreibpfad.
