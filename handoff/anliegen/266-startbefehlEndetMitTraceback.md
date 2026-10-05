# Startbefehl endet mit Traceback, Stelle doppelt gelesen

266 · Kritik · von Reviewer (Technik) → Implementierer · Runde 1/3 · angenommen

## Runde 1
**Befund.** Kritik am Code von 488d8da.
1. `python3 -m arbiter` lässt sich nur mit Strg+C beenden, und dann steht ein Traceback im
   Terminal: `KeyboardInterrupt` aus `Server.warten` (`self._thread.join()`,
   `technik/arbiter/web/server.py:24`), aufgerufen in `starten`
   (`technik/arbiter/__main__.py:11`). Nachgestellt mit SIGINT an den Prozess: Exit -2,
   15 Zeilen Traceback auf stderr. Der Stakeholder sieht das bei jedem Ende einer Partie
   und liest es als Absturz.
2. `darstellung._modelle` (`technik/arbiter/web/darstellung.py:42`) fragt je Modell erst
   `aufstellung.gesetzt(modell)`, dann zweimal `aufstellung.stelle(modell)` für `x` und `y`.
   Dieselbe Frage dreimal; `stelle` liefert `None` genau dann, wenn das Modell nicht
   gesetzt ist.

**Kosten.** 1: zwei bis drei Zeilen, kein Akzeptanztest ändert sich. Ohne sie bleibt der
erste Eindruck des Befehls aus QUE-2.1 ein Traceback. 2: eine Zeile; ohne sie liest man drei
Abfragen, wo eine reicht, und ein Typprüfer (mypy oder pyright strikt, Ablauf, Werkzeuge)
meldet `.x` auf `Stelle | None`.

**Gegenvorschlag.**
1. In `starten` das Warten in `try … except KeyboardInterrupt:` fassen und dort
   `server.beenden()` rufen, mit `# Warum: Strg+C beendet den Befehl ohne Traceback`. Oder
   `Server.warten` fängt es selbst; den Ort wählst du. `beenden` gibt es schon.
2. Die Stelle einmal lesen, etwa über eine Hilfsfunktion `_modell(stelle, modell, nummer)`
   mit `for modell in einheit.modelle if (stelle := aufstellung.stelle(modell))`, oder
   eine Abfrage der Domäne, die die gesetzten Modelle mit Stelle liefert; `gesetzt` fällt
   hier weg.

Erledigt, wenn SIGINT an `python3 -m arbiter` ohne Traceback endet, `_modelle` je Modell
eine Abfrage stellt und `python3 -m pytest technik/tests` grün ist.

**Stellungnahme.** Umgesetzt. 1: `starten` in `__main__.py` fängt `KeyboardInterrupt` und ruft `server.beenden()`; SIGINT an `python3 -m arbiter` endet mit Exit 0 und leerem stderr. 2: `_modelle` fragt `aufstellung.stelle(modell)` einmal je Modell (`:=`). Alle Tests grün.
