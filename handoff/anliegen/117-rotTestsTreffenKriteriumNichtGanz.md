# Rote Tests zu AUF-2, AUF-3, QUE-1, OBJ-1 treffen ihr Kriterium nicht ganz

117 · Kritik · von Fachkritiker (Domäne) → Testautor · Runde 1/3 · angenommen

## Runde 1
**Befund.** Nachgerechnet mit Radius 16/25,4″ (32 mm) und den Stellen aus `conftest.py`:
1. `auf3Test.py::testAuf3_2…[zoneDesGegners]`: 11 Radien sind 6,93″; die *Base* reicht von
   6,30″ bis 7,56″ und liegt *ganz in* der eigenen *Aufstellungszone* (9″). Der Test verlangt
   ‚nicht ganz in der Zone‘, das Kriterium gibt keine *Sperre*.
2. `auf3Test.py::testAuf3_4JenseitsVonEinemZoll…[schräg]`: Die *Stelle* liegt 0,20″ vom
   zweiten *Modell* des anderen *Spielers* (Länge 3 Radien); sie ist in *Nahkampfreichweite*,
   der Test verlangt das Gegenteil. Aus demselben Grund prüft `[einZollSchräg]` (und
   `halberZoll`, `berührend`, `überdeckend` nur gerade) das schräge Messen nicht für sich: Das
   zweite *Modell* sperrt ohnehin.
3. `auf3Test.py::testAuf3_2…[überDieKurzeKante]` (1, 0): Mit Tiefe r − 1/1.000.000 ragt die
   *Base* auch über die lange *Spielfeldkante*. Dass das Band (AUF-2.4: „Band des
   *Spielfelds*“) an den kurzen Kanten endet, prüft kein Test; eine Zone als endloser Streifen
   bleibt grün.
4. `auf1Test.py` verlangt in 19 Tests die Fixture `sperrgründe`; `conftest.py` hat nur
   `Platz.sperrgründe`. Diese Tests bleiben rot, auch wenn der Code stimmt.
5. OBJ-1.1: Da `Armee` und `Einheit` nach Identität vergleichen (`eq=False`), bestehen alle
   drei Tests auch dann, wenn beide *Spieler* je eine Kopie derselben *Armee* bekommen. Das
   Kriterium („eine andere der zwei *Armeen*“) meint den Inhalt. Heute fängt nur
   `testAuf2_6DieBaseJedesModells…` diesen Fehler.
6. Namen: „Gegner“ (`einheitNachDemGegner`, `stelleBeimGegner`, `…DesGegners`) steht nicht im
   Glossar; AUF-3.4 sagt „des anderen *Spielers*“.

**Kosten.** 1, 2 und 4 können nicht grün werden; der Implementierer müsste den Code verbiegen
oder die Tests anfassen. Nach `prozess/ablauf.md` (Technikphase, 2) gehen diese Tests nicht
in die Umsetzung, bis das Anliegen geklärt ist. 3 und 5 lassen falschen Code grün. 6 bricht die
Regel, dass Namen wörtlich im Glossar stehen.

**Gegenvorschlag.**
1. Eine Tiefe in der Zone des anderen *Spielers*, etwa 57 Radien (35,9″ − 1/1.000.000″,
   also *Base* ab 35,3″) und die Kennung so lassen; oder den Fall streichen, `mitteDesSpielfelds`
   deckt die Mitte ab.
2. Als Bezug das letzte *Modell* der Reihe des anderen *Spielers* (Länge 3 Radien) nehmen und
   schräg in Richtung wachsender Länge gehen; dann liegt kein weiteres *Modell* näher als 1″.
3. `überDieKurzeKante` mit Tiefe 3 und Länge r − 1/1.000.000; dazu derselbe Fall am anderen
   Ende (Länge 60 − r + 1/1.000.000).
4. Eine Fixture `sperrgründe` in `conftest.py`, die `_sperrgründe` liefert.
5. Prüfen, dass sich die *Armeen* im Inhalt unterscheiden, etwa die *Durchmesser* je
   *Einheit* der zwei *Spieler* (`durchmesserJeEinheit` aus `auf2Test.py`).
6. „anderer Spieler“ statt „Gegner“, etwa `einheitNachDemAnderenSpieler`.

Sonst decken die Tests jedes Kriterium von OBJ-1.1, QUE-1.1, QUE-1.2, AUF-2.4 bis AUF-2.7 und
AUF-3.2 bis AUF-3.7, ohne über Plan und Kriterien hinauszugehen. Rot sind derzeit alle wegen
des fehlenden `arbiter.katalog` (Importvertrag des Regelumsetzers), also nicht wegen dieser Fälle.

**Stellungnahme.** Angenommen, alle sechs Punkte nach Gegenvorschlag umgesetzt:
1. `zoneDesAnderenSpielers` mit 57 Radien.
2. Bezug ist das letzte *Modell* der Reihe (Länge 3 Radien), schräg in wachsender Länge.
3. `überDieKurzeKante` ersetzt durch zwei Tests, `…AmAnfang` und `…AmEnde`.
4. Fixture `sperrgründe` in `conftest.py`.
5. `testObj1_1DieZweiArmeenUnterscheidenSichImInhalt` über `durchmesserJeEinheit`, jetzt Fixture in `conftest.py`, von `auf2Test.py` mitgenutzt.
6. „Gegner“ ersetzt durch „anderer Spieler“ (`einheitNachDemAnderenSpieler`, `stelleBeimAnderenSpieler`).
