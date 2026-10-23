# Kommentare zu Bildschirmtests: ersatzlos löschen, die Erklärung kommt in die Architektur

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: offen
Wartet auf: Technikphase

## Runde 1
**Befund (wartet auf die Technikphase).** Item 1 in [Plan 7](../plan.md) entfernt zuerst die
Kommentare, die [Es 8](../../prozess/praemissen/es.md) verbietet; was einer erklärt, steht
danach im Namen, im Docstring oder in der Architektur (Anliegen 2510).
Drei Kommentare in den Akzeptanztests erklären, wie ein Bildschirmtest misst und wartet; das
gilt für alle Bildschirmtests und steht noch nirgends:

Kommentar (Stand jetzt) | gehört nach [web.md](../../technik/architektur/web.md)
---|---
`akzeptanz/conftest.py:39` „Ungepuffert“ | B4: Der Test startet den Befehl mit `PYTHONUNBUFFERED=1`, sonst kommt die erste Zeile zu spät
`akzeptanz/bildschirm.py:154` „Länger als das“ | B2: Eine Seite wartet höchstens 5 s (`set_default_timeout`); länger heißt, der Server antwortet nicht
`akzeptanz/querschnitt/karteTest.py:11` „getBoundingClientRect“ | B3: Was der Test in Pixeln misst, gilt relativ auf 1e-4; exakt bleiben die Attribute in Zoll

Schon in der Architektur, darum ersatzlos: `querschnitt/karteTest.py:22` (W5),
`akzeptanz/dienst.py:14` (W4), `phasen/aufstellen/ziehenTest.py:27` (V8),
`phasen/aufstellen/blockAlsGanzesTest.py:285` (V10, Beispiel).

**Kosten.** Ohne die Liste stünde die Erklärung als Docstring und, sobald ich sie eintrage,
ein zweites Mal ([Wir 3](../../prozess/praemissen/wir.md)).

**Gegenvorschlag.** Diese Kommentare löschen, ohne Docstring. Ich trage die drei Sätze
gleichzeitig in web.md ein; beides geht in den einen Commit nach dem Aufräumen. Die übrigen
Kommentare in den Tests nach Plan 7.
Erledigt, wenn keiner der Kommentare beider Listen mehr steht, auch nicht als Docstring.

**Stellungnahme.**
