# Befehl in conftest.py: ungelesene Fehlerausgabe und ein englischer Feldname

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund (wartet auf die Technikphase).** Die Tests zu QUE-8 passen zum Vertrag
([Web, W5 und B4](../../technik/architektur/web.md)): `portDesBefehls([])` mit
`adresseMitPort`, ein zweiter Befehl auf dem Port des ersten, Ende mit 1, nichts auf
stdout, eine Zeile auf stderr. Am Aufbau in
[conftest.py](../../technik/tests/akzeptanz/conftest.py) fällt zweierlei auf:

1. `_prozessStarten` setzt jetzt für jeden Start `stderr=subprocess.PIPE`, auch für
   `starten()`, das die Fehlerausgabe nie liest. Werkzeug schreibt je Anfrage eine Zeile
   auf stderr. Ist der Puffer der Pipe voll (unter Linux 64 KiB, gut 600 Anfragen), hält der
   Server beim Schreiben an, und der Test läuft in die Wartezeit. Heute bleiben QUE-2 und
   QUE-3 weit darunter. Später fällt das nur als Test auf, der ohne erkennbaren Grund hängt.
2. `Ende.exitCode` ist der einzige englische Name neben `ausgabe` und `fehlerausgabe`
   ([Wir 1](../../prozess/praemissen/wir.md)). Der Vertrag sagt „Ende mit 1“.

**Kosten.** 1 kostet später eine Fehlersuche ohne Hinweis. 2 bricht die gemeinsame Sprache
an einer Stelle, die jeder Test zu QUE-8 liest.

**Gegenvorschlag.**
1. `_prozessStarten(port, fehlerausgabe)`: `starten()` gibt `subprocess.DEVNULL`,
   `startenBisZumEnde` `subprocess.PIPE`, denn nur dort liest `communicate` sie.
2. `Ende.code`, dann liest sich `ende.code == 1` wie der Vertrag; der Docstring sagt
   entsprechend „ein Code unter 0 heißt, er lief weiter“.

Erledigt, wenn `starten()` keine ungelesene Pipe mehr öffnet und das Feld einen deutschen
Namen hat.

**Stellungnahme.** Angenommen, beides umgesetzt. 1: `_prozessStarten(port, fehlerausgabe)`;
`starten()` gibt `subprocess.DEVNULL`, `startenBisZumEnde` `subprocess.PIPE`. 2: `Ende.code`,
der Docstring sagt „ein Code unter 0“; `festeAdresseTest.py` liest `ende.code == 1`.

**Nachprüfung.** Erledigt: `starten()` öffnet keine ungelesene Pipe mehr, `Ende.code` ist
deutsch; die Tests zu QUE-8 sind grün.
