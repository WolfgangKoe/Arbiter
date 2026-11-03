# Übergehen im Code doppelt gerechnet

Form: Kritik
Von: Architekt
An: Implementierer
Runde: 1/3
Status: offen
Wartet auf: Technikphase 11

## Runde 1
**Befund.** Wartet (Entwurf und Ablage, keine Prüfung rot: Importvertrag und `ruff check`
grün, Einheitstests grün; `ruff format` meldet nur Bekanntes). Kritik am Code zu Item
anhaltenUebergehen nach ba69ad5. Der Code hält V18; vier Stellen werden mit den nächsten
Items teuer:
1. Zweimal gerechnet:
   [schlachtrunden.py](../../technik/arbiter/domaene/querschnitt/schlachtrunden.py)
   `modellLoslassen` ruft `stellenMitGründenNachDemZiehen` und danach `angebotNachDemZiehen`
   mit denselben Eingaben; beide rechnen `_anteile`, `_ebeneDes` und `_stellenDesGegners`
   je zweimal. Ob angehalten wurde, ist ein Ergebnis desselben Anhaltens. Mit Item
   anhaltenAufDemWeg zählen dafür auch 17.3 und 17.4
   ([Ziehen](../../technik/architektur/vertrag/bewegung/ziehen.md)); dann müssen beide Wege
   gleich geändert werden, sonst bietet Arbiter übergehen an, wo die *Karte* nicht anhielt.
2. Das Ende des Angebots steht an sechs Stellen der `Schlacht` (`angebotBeenden()` in
   `phaseBeenden`, `modellLoslassen`, `gemeinsamÜbergehen`, `karteAnklicken`, `vorrücken`,
   `vorrückenZurücknehmen`). Der Begriff *Handlung* (V5, D2) hat keinen Ort im Code; jede neue
   Handlung (BEW-24 in Item zuruecksetzenUndLuecken) muss an die Zeile denken, kein Test
   außer einem Akzeptanztest je Handlung fällt sonst auf.
3. Eine Regel, zwei Formen: Dass in der *Bewegungsphase* QUE-1.3 nicht sperrt (BEW-21,
   Zweck), zieht `gründeBeimÜbergehen` als `- {Grund.nahkampfreichweite}` ab,
   `gründeBeimZiehen` dagegen über `if stelle == vorige[modell]: continue` in
   [normaleBewegung.py](../../technik/arbiter/domaene/phasen/bewegung/normaleBewegung.py),
   das nur wirkt, weil BEW-25.1 den Anteil 0 setzt. Der Leser sieht den Grund nicht.
4. Ablage: `Anteile` liegt in
   [uebergehenBeimZiehen.py](../../technik/arbiter/domaene/phasen/bewegung/uebergehenBeimZiehen.py),
   dient aber auch dem gewöhnlichen Ziehen (`min`, BEW-6.3, `anhaltenVorDerGrenze.md`).
   Nebenbei: `_stellenDesGegners` nimmt alle *Modelle*, wenn niemand *am Zug* ist, nur weil
   `gemeinsamÜbergehen` erst danach auf `spieler is None` prüft.

**Kosten.** Je Punkt wenige Zeilen, jetzt billig. Bleibt 1, ändert Item anhaltenAufDemWeg zwei
Rechnungen gleich; bleibt 2, wächst die Liste mit jeder Handlung. `schlachtrunden.py` hat
9.724 von 12.000 Zeichen; 1 und 2 sparen dort Zeilen.

**Gegenvorschlag.**
1. `stellenMitGründenNachDemZiehen` liefert die `Anteile` mit (oder ein Ergebnis aus
   *Stellen*, *Gründen* und angehalten), `modellLoslassen` gibt sie an die
   `Bewegungsphase` zum Merken; eine Rechnung je Loslassen.
2. Ein Dekorator `@handlung` in `schlachtrunden.py`, der nach einem Aufruf ohne `Sperre` das
   Angebot beendet; `gemeinsamÜbergehen` und `modellLoslassen` setzen es danach neu. Eine
   neue Handlung ist dann eine Zeile, die sie als *Handlung* ausweist (Es, O).
3. Eine Funktion in `normaleBewegung.py`, die QUE-1 ohne QUE-1.3 prüft (Tabelle nach D4),
   für Ziehen und Übergehen; der Wächter auf unbewegte *Modelle* entfällt.
4. `Anteile` nach `anhaltenVorDerGrenze.py` (BEW-6.3); in `gemeinsamÜbergehen` zuerst
   `spieler is None` prüfen, dann entfällt der Zweig in `_stellenDesGegners`.
Ändert Item anhaltenAufDemWeg oder zuruecksetzenUndLuecken diese Stellen ohnehin, gern dort.

**Stellungnahme.**
