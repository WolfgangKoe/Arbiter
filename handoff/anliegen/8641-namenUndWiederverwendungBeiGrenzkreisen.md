# Namen und Wiederverwendung bei Grenzkreisen

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 2/3
Status: angenommen

## Runde 1
**Befund.** Wartet (Namen und Ablage von Hilfsfunktionen, keine Prüfung rot), Stand
4b2f2ec, Item grenzkreise.
1. `_einheitMitGrenzen` in
   [schlachtrunden.py](../../technik/arbiter/domaene/querschnitt/schlachtrunden.py) liefert
   die *ausgewählte* *Einheit* des *Spielers* *am Zug* in der *Bewegungsphase* (BEW-5.1,
   11.1) und entscheidet auch, ob „Vorrücken“ angeboten ist; der Name nennt nur die
   Grenzkreise. `vorrücken` und `vorrückenZurücknehmen` prüfen dieselbe Bedingung über die
   Eigenschaft ein zweites Mal und reichen dann `self._auswahl.einheit` weiter, das
   `Einheit | None` ist.
2. [grenze.js](../../technik/frontend/komponenten/grenze.js): `kennung` gibt den Einträgen
   der *Nahkampfreichweite* `…-bewegung` als Kennung; die Vorlage in
   [index.html](../../technik/frontend/index.html) heißt `grenzeBoyz`, nach einer
   Testeinheit.
3. `grenze` setzt Breite und Länge der Maske von Hand wie `flächeSetzen` in
   [karte.js](../../technik/frontend/komponenten/karte.js).

**Kosten.** Am Bildschirm nichts. Ein Leser sucht hinter „mit Grenzen“ eine Bedingung, die
es nicht gibt, und eine Bewegung hinter der Kennung eines Gegners. Umbau: etwa 15 Zeilen in
drei Dateien.

**Gegenvorschlag.**
1. `_ausgewählteEinheitAmZug`; `vorrücken` und `vorrückenZurücknehmen` holen die *Einheit*
   einmal daraus und rufen mit ihr `self._bewegungsphase.vorrückenBeginnen(einheit)` bzw.
   prüfen `vorrückenZurücknehmenAngeboten(einheit)`.
2. Die Kennung der Maske aus der Stelle in der Liste: `karte` gibt `grenze` die Nummer des
   Eintrags, `grenze-${nummer}`; die Vorlage heißt neutral `grenze`.
3. `flächeSetzen` nach [vorlage.js](../../technik/frontend/komponenten/vorlage.js) und in
   `grenze` für Maske und Rechteck aufrufen.

**Stellungnahme.** Alle drei Punkte angenommen und umgesetzt: `_ausgewählteEinheitAmZug` mit
einmaliger Abfrage in `vorrücken` und `vorrückenZurücknehmen`; Maskenkennung `grenze-${nummer}`
aus der Stelle in der Liste, Vorlage neutral; `flächeSetzen` jetzt in `vorlage.js`.

## Runde 2
**Befund.** Hält auf: eine Prüfung ist rot. Nachgeprüft am uncommitteten Stand; Punkte 2 und
3 sind erledigt, Punkt 1 halb.
1. `ruff check` meldet E501 in
   [schlachtrunden.py, Zeile 270](../../technik/arbiter/domaene/querschnitt/schlachtrunden.py#L270)
   (101 Zeichen), `ruff format --check` will dieselbe Zeile umbrechen.
2. `vorrücken` prüft die Bedingung weiter ein zweites Mal, jetzt ausgeschrieben statt über die
   Eigenschaft: `self._bewegungsphase.vorrückenAngeboten(…)` steht in der Eigenschaft
   `vorrückenAngeboten` und in `vorrücken`, und `Bewegungsphase.vorrückenBeginnen` prüft sie
   selbst noch einmal ([bewegung/\_\_init\_\_.py, Zeile 145](../../technik/arbiter/domaene/phasen/bewegung/__init__.py#L145)).
   `_stellenDesGegners()` läuft dabei zweimal.
3. `einheitZurücksetzen` hat das Muster aus Runde 1 noch: Prüfung über die Eigenschaft
   `einheitZurücksetzenAngeboten`, dann `self._auswahl.einheit` (`Einheit | None`)
   weitergereicht.

**Kosten.** Am Bildschirm nichts. Rot hält den Commit auf; dieselbe Bedingung an drei
Stellen. Umbau etwa 8 Zeilen in einer Datei.

**Gegenvorschlag.**
1. und 2. `vorrücken` holt die *Einheit* und ruft ohne eigene Prüfung
   `vorrückenBeginnen(einheit, self._stellen, self._stellenDesGegners())`, nur wenn
   `einheit is not None`; die Prüfung bleibt in `Bewegungsphase.vorrückenBeginnen`.
3. `einheitZurücksetzen` wie `vorrückenZurücknehmen`: `einheit = self._ausgewählteEinheitAmZug()`,
   Rückkehr bei `None` oder `not self._bewegungsphase.einheitZurücksetzenAngeboten(einheit,
   self._stellen)`, dann `stellenZuBeginnDer(einheit)`.

**Stellungnahme.** Alle drei Punkte angenommen und umgesetzt: Zeile 270 entfällt; `vorrücken`
prüft nicht mehr selbst, die Prüfung bleibt in `Bewegungsphase.vorrückenBeginnen`, und
`_stellenDesGegners()` läuft einmal; `einheitZurücksetzen` holt die *Einheit* wie
`vorrückenZurücknehmen` und reicht keine `Einheit | None` weiter.
