# Kommentare zu Web und Seite: ersatzlos löschen, die Erklärung kommt in die Architektur

Form: Kritik
Von: Architekt
An: Implementierer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund (wartet auf die Technikphase).** Item 1 in [Plan 7](../plan.md) entfernt zuerst die
Kommentare, die [Es 8](../../prozess/praemissen/es.md) verbietet; was einer erklärt, steht
danach im Namen, im Docstring oder in der Architektur (Anliegen 2510).
Sechs Kommentare erklären etwas an der Schnittstelle, das noch nirgends steht. Ein Docstring
hielte es an einer Funktion fest, es gilt aber für Web und Seite:

Kommentar (Stand jetzt) | gehört nach
---|---
`web/anwendung.py:33` „rechnet in double“ | [handlungen.md](../../technik/architektur/handlungen.md), V5: Eine Zahl ist eine JSON-Zahl, kein Wahrheitswert, als double endlich
`web/anwendung.py:52` „1_0“ | V5, für die Abfrage (V10): nur die Schreibweise einer JSON-Zahl
`web/anwendung.py:58` „4.300 Ziffern“ | V5: auch keine Ganzzahl, die Python nicht liest
`frontend/seite.js:59` „liefert Flask HTML“ | [web.md](../../technik/architektur/web.md), W3: JSON tragen nur 200 und 409; auf jede andere Antwort holt die Seite V1 neu
`frontend/seite.js:8` „SVG-Namensraum“ | [oberflaeche.md](../../technik/architektur/oberflaeche.md), O1: eine Vorlage der Karte steht in einem `<svg>` im `<template>`
`__main__.py:24` „Strg+C“ | web.md, W5: Strg+C beendet den Befehl ohne Traceback

Schon in der Architektur, darum ersatzlos: `web/anwendung.py:24` (V4), `:40` (S2, V5), `:63`
(V10); `web/darstellung.py:77` (V1); `seite.js:1` (O1), `:36` (V7), `:64`, `:122`, `:136`,
`:218`, `:225` (V8, V9), `:132`, `:151`, `:169`, `:184` (V10), `:217` (Anliegen 1761, 2).

**Kosten.** Ohne die Liste stünde die Erklärung als Docstring und, sobald ich sie eintrage,
ein zweites Mal ([Wir 3](../../prozess/praemissen/wir.md)).

**Gegenvorschlag.** Diese Kommentare löschen, ohne Docstring. Ich trage die sechs Sätze
gleichzeitig unter `technik/architektur/` ein; beides geht in den einen Commit nach dem
Aufräumen. Die übrigen Kommentare im Code (Domäne, Katalog) nach Plan 7.
Erledigt, wenn keiner der Kommentare beider Listen mehr steht, auch nicht als Docstring.

**Stellungnahme.** Angenommen. Die sechs Kommentare und alle weiteren der beiden Listen sind
ersatzlos gelöscht, ohne Docstring; Verhalten unverändert.
