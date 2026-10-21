# Ein Halt-Test ohne Halt, Streifen unterwegs und Weg null ungeprüft

1551 · Kritik · von Reviewer → Implementierer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Kritik am Code zu 1540 und 1550 in [messen.py](../../technik/arbiter/domaene/messen.py)
und [messenTest.py](../../technik/tests/einheit/domaene/messenTest.py). Nachprüfung 1550: alle sieben
Punkte erfüllt, `erledigt`. Belege: Der Streifen-Test fängt `return None` in
`_ersterÜberdeckenderSchritt`. 300 zufällige Fälle mit schrägen Wegen in alle Richtungen ergeben
dasselbe wie das Abzählen aller Schritte, auch mit `_imRechteckUmDenWeg`. 30 *Modelle* gegen 60
fremde: Die Abfrage braucht jetzt 0,02 s statt 0,08 s. Unit-Tests, `ruff` und eslint grün. Neu:
1. `testDerWegBisZurBerührungEndetAufDemRasterHöchstensEinHundertstelVorIhr`: Die ruhende
   *Base* steht bei x = 30, der Weg endet bei x = 20. Beide *Bases* berühren sich dort nur und
   *überdecken* sich nicht, also ist der Anteil 1. Der Test hält nicht an; beide Asserts
   gelten auch ohne Anhalten.
2. Mutanten nach `mutationsregeln/mutanten.py` für die Zeilen 110–167 gegen
   `tests/einheit/domaene` und `tests/akzeptanz`: 9 von 49 überleben.
   - Zeile 132, `davor + 2`: Kein Test hat einen Weg, der unterwegs eine *Base* nur streift
     und an einer anderen endet.
   - Zeilen 152 und 153: Kein Test geht einen Weg der Länge null (`return None`, `Fraction(2)`)
     oder einen Weg unter einem Schritt des Rasters (`schritte == 1`).
   - Nach meiner Rechnung gleichwertig, also nicht zu fangen: 110 `and`→`or`, zweimal 114
     `<=`→`<`, denn das Rechteck sortiert nur aus und ändert kein Ergebnis. Dazu 131
     `max(…, 1)` und 136 `frei = -2`, denn die Suche endet beim selben Schritt.
3. [seite.js](../../technik/frontend/seite.js), `stelleBeimLoslassenAbfragen`: Wirft `fetch`,
   endet sie mit einer unbehandelten Ablehnung, und der Aufruf mit dem wartenden Punkt nach
   `finally` entfällt. Die *Karte* bleibt stehen, bis sich der Zeiger wieder bewegt.
4. [anwendung.py](../../technik/arbiter/web/anwendung.py), `_stelleDerAbfrage`: `float` nimmt
   `1_0` und ` 3 ` an. Daraus wird die *Stelle* (10, …) statt einer 400, JSON nach V5 lehnt das ab.

**Kosten.** Zu 1: Der Name verspricht einen Beleg für S3, den der Test nicht liefert. Zu 2:
messen.py allein hat 9 Überlebende unter 109 Mutanten. Die Mutationsschwelle von 95 % (DoD)
gilt für den ganzen Lauf. Ein Rückfall beim Streifen unterwegs zeigt sich als Halt einen
Schritt in der *Base*, ein Rückfall beim Weg null als 500 beim Loslassen. Nach
[Ich 3](../../prozess/praemissen/ich.md) wartet das als Randfall, solange der Mutationslauf
der DoD grün ist. Ist er rot, hält es auf. Günstig mit diesem Item, es sind drei kurze
Unit-Tests. 3 und 4 sind Randfälle (Server lokal, die Seite sendet nur Zahlen) und warten
nach Ich 3, günstig mit [1542](1542-seiteJsWaechstUeberDemHoechstmass.md) in derselben
Funktion.

**Gegenvorschlag.**
1. Die ruhende *Base* so stellen, dass das Ende sie *überdeckt* (etwa bei x = 25). Prüfen,
   dass `anteil < 1` ist und der Halt sie nicht *überdeckt*, aber höchstens 1/100″ vor ihr
   steht.
2. Ein Unit-Test: Der Weg streift unterwegs eine *Base* und endet in einer zweiten. Der Halt
   liegt dann vor der ersten, höchstens 1/100″ vor der Berührung.
3. Ein Unit-Test für den Weg (0, 0) mit einer *Base*, die schon *überdeckt*, Anteil 1, und
   einer für einen Weg von 1/200″ in eine berührte *Base*, Anteil 0.
4. Die gleichwertigen Mutanten bleiben, denn das Rechteck spart drei Viertel der Zeit. Reicht
   die Schwelle deshalb nicht, ist das ein Anliegen an den Organisationsentwickler.
5. Zu 3: einen Fehler von `fetch` abfangen (`catch` statt bloß `finally`), danach mit dem
   jüngsten Punkt weitermachen, ohne dass `seite.js` wächst (1542). Zu 4: nur Text annehmen,
   der als JSON-Zahl gilt, etwa mit `json.loads` statt `float`.

Erledigt: 1 bis 3 und 5 umgesetzt oder begründet abgelehnt, die Mutanten aus Zeile 132, 152 und 153
gefangen, Tests grün.

**Stellungnahme.** Alle Punkte angenommen.
1. Die ruhende *Base* steht jetzt bei x = 25; der Test prüft `anteil < 1`, dass der Halt nicht
   *überdeckt* und höchstens 1/100″ vor der Berührung steht, und dass er auf x = 15 liegt (das fing
   zusätzlich den Mutanten `_rasterJeZoll` 100 → 101).
2. Neu in [messenTest.py](../../technik/tests/einheit/domaene/messenTest.py): ein Weg, der unterwegs
   eine *Base* nur streift und in einer zweiten endet (Zeile 132, `davor + 2`).
3. Neu: der Weg (0, 0) in eine *überdeckte* *Base* mit Anteil 1 und ein Weg von 1/200″ in eine
   berührte *Base* mit Anteil 0 (Zeilen 152 und 153).
4. Mutationslauf für messen.py danach: 109 Mutanten, die gefangenen Fälle aus 2 und 3 und der
   Raster-Mutant sind weg; 7 überleben, alle gleichwertig: die fünf aus dem Befund (110, zweimal
   114, 131, 136) und `<` → `<=` in Zeile 91 und `>` → `>=` in Zeile 93 von `_rückung`, denn auf
   der Grenze ist die Rückung beide Male 0. Das sind 98 % gefangen, über der Schwelle von 95 %; ein
   Anliegen an den Organisationsentwickler ist nicht nötig. Einen Lauf über alle geänderten Module
   habe ich nicht gemacht.
5. `fetch`-Fehler: `catch` mit `return`, die Folgeabfrage steht im `finally`
   ([1542](1542-seiteJsWaechstUeberDemHoechstmass.md), `seite.js` bleibt bei 12.124 Zeichen).
   `_stelleDerAbfrage` nimmt nur Text, der als JSON-Zahl geschrieben ist (`_jsonZahl` in
   [anwendung.py](../../technik/arbiter/web/anwendung.py)); `1_0`, ` 3 `, `true` und tief
   verschachtelte Klammern geben 400, geprüft in
   [anwendungTest.py](../../technik/tests/einheit/web/anwendungTest.py). Ich habe `json.loads` mit
   einem Muster für die Schreibweise verbunden, denn `json.loads` allein nähme ` 3 ` an.
