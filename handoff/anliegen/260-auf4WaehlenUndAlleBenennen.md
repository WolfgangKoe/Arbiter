# AUF-4: Wählen und „alle Einheiten“ benennen

260 · Kritik · von Architekt (Technik) → Testautor · Runde 1/3 · erledigt

## Runde 1
**Befund.** Kritik am Code von d6e3af0 (Lesbarkeit, `prozess/praemissen/wir.md`), in
`technik/tests/akzeptanz/phasen/aufstellen/auf4Test.py`:
1. `modelleSetzen(…, necronWarriors, 0)` und in `…WandertDieKennzeichnung` zweimal
   `modelleSetzen(…, 0)` heißen „die *Einheit in Aufstellung* wählen“. Die 0 steht für eine
   Handlung, die die Domäne schon hat: `aufstellung.einheitInAufstellungWählen(einheit)`.
2. „Alle *Einheiten* aufstellen“ steht zweimal als Summe
   `len(spielerEins.armee.einheiten) + len(spielerZwei.armee.einheiten)`
   (`aufstellungOhneJemandAnDerReihe`, `…BleibtSeineAblageLeerUndNenntIhn`). 248 Punkt 3 hat
   die `4` benannt, der Begriff hat noch keinen Ort; beide Stellen holen dafür eine Fixture
   mehr.
3. „Vor der Wahl“ steht in derselben Datei in zwei Formen: `aufstellungOhneJemandAnDerReihe`
   parametrisiert mit Namen („ausgangslage“, „nachDerGewinnerwahl“),
   `testAuf4_6VorDerWahl…` mit dem Schalter `gewinnerGewählt` (`False`, `True`) und baut seine
   `Aufstellung` im Test. 252 hatte die erste Form vorgeschlagen.
4. Der neue Test zu AUF-4.3 (`…BleibtSeineAblageLeerUndNenntIhn`) steht am Ende der Datei,
   hinter AUF-4.7; die übrigen stehen nach Kriterium.

**Kosten.** Je Punkt wenige Zeilen in `auf4Test.py`, für 2 eine Funktion in `handgriffe.py`;
was geprüft wird, bleibt. Ohne sie liest man Zahlen und Schalter statt Begriffe. Der
Implementierer wird nicht blockiert.

**Gegenvorschlag.**
1. `aufstellungNachDerZonenwahl.einheitInAufstellungWählen(necronWarriors)`, ebenso für
   Boyz und Warboss.
2. `alleEinheitenAufstellen(aufstellung)` in `handgriffe.py`: zählt die *Einheiten* beider
   *Armeen* aus `aufstellung.ausgangslage` und ruft `einheitenAufstellen`; die Summen und
   ihre Fixtures entfallen.
3. Eine Fixture `aufstellungVorDerZonenwahl` mit `params=["ausgangslage",
   "nachDerGewinnerwahl"]`, die eine eigene `Aufstellung(ausgangslage)` baut (eine zweite
   neben `ausgangsaufstellung`, die `aufstellungMitModellenBeiderSpieler` schon belegt); der
   Test nimmt sie statt `gewinnerGewählt`.
4. Den Test zu den übrigen von AUF-4.3 stellen.

Am billigsten zusammen mit [259](259-handgriffeImportierenStattFixtures.md). Erledigt, wenn 1
bis 4 umgesetzt sind und jeder Test aus demselben Grund rot oder grün ist wie vorher.

**Stellungnahme.** Angenommen, umgesetzt in `auf4Test.py` und `handgriffe.py`: 1. Die Wahl heißt `einheitInAufstellungWählen(…)`. 2. `alleEinheitenAufstellen(aufstellung)` steht in `handgriffe.py`, die Summen entfallen. 3. `aufstellungVorDerZonenwahl` (ausgangslage, nachDerGewinnerwahl) ersetzt den Schalter; AUF-4.4 „solange keiner an der Reihe ist“ teilt sich dafür in zwei Tests (vor der Zonenwahl, nach der Aufstellung), weil die Fixture die dritte Form nicht trägt. 4. Der Test zu AUF-4.3 steht bei den übrigen von AUF-4.3.
