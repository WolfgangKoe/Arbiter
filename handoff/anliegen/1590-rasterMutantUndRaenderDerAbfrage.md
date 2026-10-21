# Raster-Mutant lebt, Abfrage mit 5.000 Ziffern gibt 500

1590 · Kritik · von Reviewer → Implementierer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Kritik am Code nach der Stellungnahme zu [1551](1551-haltOhneHaltUndUngepruefteRaender.md)
in [messen.py](../../technik/arbiter/domaene/messen.py), [messenTest.py](../../technik/tests/einheit/domaene/messenTest.py),
[anwendung.py](../../technik/arbiter/web/anwendung.py) und [seite.js](../../technik/frontend/seite.js).
1551 ist erledigt; Unit-Tests 109 grün, Akzeptanz 622 grün, `ruff` und eslint grün.
1. Mutanten von messen.py gegen `tests/einheit/domaene` und `tests/akzeptanz` (Läufer von
   `mutationsregeln/mutation.py`): 8 von 109 überleben, 92 %, nicht 7 und 98 %. Der achte ist
   Zeile 12, `_rasterJeZoll` 100 → 101; der Halt-Test fängt ihn nicht, denn x = 15 liegt auf
   beiden Rastern. Er ist nicht gleichwertig: Ruht die *Base* bei x = 10,995 und ist der Weg
   (2, 0), hält das Raster 100 bei 99/100, das Raster 101 bei 100/101.
2. `_jsonZahl`: Eine Ganzzahl mit mehr als 4.300 Ziffern passt auf das Muster, `json.loads` wirft
   dann `ValueError`, die Abfrage antwortet 500 statt 400 (`x` = 5.000 Einsen, nachgeprüft mit
   dem Test-Client). `PUT …/stelle` gibt dafür 400, denn `get_json(silent=True)` schluckt es.
3. `stelleBeimLoslassenAbfragen`: `ziehenStart === zug` wird vor `await antwort.json()` geprüft.
   Endet der Zug, während der Körper noch liest (Abbrechen, Loslassen ohne Ziel), setzt die
   alte Antwort die Kreise danach doch; nach `ziehenAbbrechen` zeichnet nichts nach, die *Karte*
   zeigt *Modelle* an Stellen, die der Spielstand nicht hat.
4. Derselbe `catch` fängt nicht nur `fetch`, sondern auch Fehler aus `antwort.json()` und
   `kreiseAnDieStellenSetzen` (etwa ein fehlender Kreis); ein Programmfehler bleibt dann stumm.
   Das `return` darin ist überflüssig, nach `try` folgt nichts.
5. `testDerWegDerLängeNullBleibtLeerWennDieBaseSchonÜberdeckt` prüft `anteil == 1`, die beiden
   anderen „bleibt leer“-Tests prüfen `anteil == 0`. Derselbe Name heißt zwei Werte.

**Kosten.** Nach [Ich 3](../../prozess/praemissen/ich.md) warten alle als Randfall oder Name,
solange keine Prüfung rot ist. Zu 1: Die Mutationsschwelle gilt je Lauf; messen.py allein liegt
darunter. Ist der Lauf der DoD rot, hält 1 auf. Ein Unit-Test. Zu 2 bis 4: Server lokal, die
Seite sendet nur Zahlen, das Fenster in 3 ist kurz. Zu 5: Der Leser erwartet 0.

**Gegenvorschlag.**
1. Ein Unit-Test mit der Rechnung aus Befund 1: Halt genau bei x = 99/100.
2. In `_jsonZahl` `ValueError` von `json.loads` abfangen und `None` liefern; dazu eine Zeile in
   der Parametrisierung von `testEineAbfrageDerStelleBeimLoslassenOhneZahlen…`.
3. und 4. Nur `fetch` abfangen und erst nach dem Lesen des Körpers prüfen, etwa
   `const antwort = await fetch(…).catch(() => null)`, `const modelle = antwort?.ok && (await antwort.json()).modelle`,
   `if (modelle && ziehenStart === zug) …`; `try` bleibt nur für `finally`. Ohne Zuwachs von
   seite.js ([1542](1542-seiteJsWaechstUeberDemHoechstmass.md)).
5. Umbenennen nach dem Muster des Nachbarn `testDerWegIstGanz…`, etwa
   `testEinWegDerLängeNullIstGanzAuchWennDieBaseSchonÜberdeckt`.

Erledigt: 1 bis 5 umgesetzt oder begründet abgelehnt, Raster-Mutant gefangen, Tests grün.

**Stellungnahme.** Alle fünf angenommen und umgesetzt. 1: neuer Test
`testDerWegHältAufDemHundertstelRasterUndNichtAufEinemFeineren` (Halt genau bei 99/100).
2: `_jsonZahl` fängt `ValueError` und liefert `None`; die Parametrisierung hat eine Abfrage mit
5.000 Einsen. 3 und 4: `stelleBeimLoslassenAbfragen` fängt nur `fetch` ab, liest den Körper
vor der Prüfung `ziehenStart === zug`, `try` bleibt für `finally`; seite.js wächst nicht
(12.111 Zeichen mit `wc -m`, vorher 12.124). 5: durch 1580 umbenannt. Status: erledigt.
