# Akzeptanztests zu Plan 2: Lage der Zonen ohne Quelle, Maße doppelt, zwei Wege zu Gründen

122 · Kritik · von Architekt (Technik) → Testautor · Runde 1/3 · offen

## Runde 1
Gegenstand: 7752988 und 283f998, `technik/tests/akzeptanz/`. Die Schnittstelle ist gut: Die
Tests legen nur fest, was die Kriterien brauchen (`Aufstellung(ausgangslage)`,
`modellSetzen(modell, stelle)`, die Abfrage `stelle(modell)` nach D3, `Sperre.gründe`,
`ausgangslageLaden()`), nicht, wo Zone und Messung im Code liegen. Die Fixture `zone` prüft
beide Zonen, an x = 0 und an x = 44, mit denselben Tests. Kein Test ist bemängelt im Sinn von
`prozess/ablauf.md` (Technikphase, 2): Alle können grün werden, die Punkte betreffen Hilfen
und Kommentare.

**Befund.**
1. `conftest.py:12-13` nennt `onlyWar.yaml` als Quelle für „die erste Aufstellungszone an der
   Kante x = 0, die zweite an x = 44“ und für die Achsen der *Stelle*. Dort steht nur, dass
   die Zonen an den zwei langen Kanten liegen, einander gegenüber. Ursprung, Achsen und
   welche Zone wo liegt, sind eine technische Festlegung; sie gehört nach
   `technik/architektur.md` (Anliegen 102, Punkt 4, git), wo sie noch fehlt. `# Regel:` steht
   für eine Regel mit Fundstelle (`prozess/praemissen/wir.md`, 8).
2. Dieselben Maße stehen mehrfach: `breiteDesSpielfelds` in `conftest.py` und `auf3Test.py`,
   `längeDerSpielfeldkante` in `auf2Test.py` und `auf3Test.py`, `tiefeDerErstenReihe` in
   `conftest.py` und `auf3Test.py` (mit „(conftest.py)“ als Fundstelle), die Tiefe der Zone
   als `tiefeDerZone` in `auf2Test.py` und als `9` in `testAuf3_5ZweiGründe…`.
3. Zwei Wege zu denselben Gründen: die Fixture `sperrgründe` und `Platz.sperrgründe`. Ein
   *Platz* hat keine Gründe; wer `platz.sperrgründe(aufstellung.modellSetzen, …)` liest, sucht
   eine Bedeutung, die es nicht gibt.
4. Zweizeilige Kommentare in `conftest.py:12-13` und `auf3Test.py:12-13`; `wir.md` 8 verlangt
   einzeilige.
5. Fällt Item 3 (Plan, Empfehlung), bleiben seine sechs Tests rot in `auf3Test.py`. Fünf
   tragen `Nahkampfreichweite` im Namen,
   `testAuf3_5AufDemModellDesAnderenSpielersNenntArbiterAlleDreiGründe` nicht.

**Kosten.** Zu 1: Der Implementierer findet die Lage nur im Rumpf von `_stelleInZone`;
vertauscht er die Zonen, sind alle Tests mit `platz` rot, und die genannte Quelle hilft nicht.
Zu 2: Ändert sich ein Wert in `onlyWar.yaml` oder die Reihe der Testeinheiten, sind bis zu drei
Stellen zu finden. Zu 3 und 4: Lesezeit. Zu 5: Der Stand von Item 2 lässt sich nicht mit
`-k "not Nahkampfreichweite"` prüfen; ohne Item 3 ist DoD 1 nicht erreichbar, und niemand sieht
auf einen Blick, welche Tests dafür zurückgestellt werden müssten.

**Gegenvorschlag.**
1. Ich trage die Lage in `architektur.md` nach (eigener Pfad, vor dem Implementierer von
   Item 2). Danach ein einzeiliger Kommentar `# Warum:` mit Verweis auf den Abschnitt dort,
   ohne den Inhalt zu wiederholen.
2. Jedes Maß einmal, in `conftest.py` an `Platz` (`platz.breiteDesSpielfelds`,
   `platz.längeDerSpielfeldkante`, `platz.tiefeDerZone`, `platz.tiefeDerErstenReihe`);
   `stelleBeimAnderenSpieler` wird eine Methode von `Platz`, sie braucht nur diese Maße. Die
   Werte bleiben Zahlen im Test: Aus `ausgangslage.spielfeld` gelesen, bestätigten die Tests
   den Katalog mit sich selbst.
3. `Platz.sperrgründe` streichen, überall die Fixture `sperrgründe`.
4. Folgt aus 1 und 2.
5. Der Name des Tests enthält `Nahkampfreichweite`, Wortlaut nach deiner Wahl. Erledigt, wenn
   `pytest technik/tests -k Nahkampfreichweite` genau die Tests von Item 3 wählt.

Verhalten unverändert: Jeder Test prüft danach dasselbe wie vorher.

**Stellungnahme.**
