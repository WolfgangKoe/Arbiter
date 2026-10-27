# Schlacht im Code: Auswahl-Routen bei der Aufstellung, Phasenfolge ohne Indizes

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Hält auf (Ich 3: neuer Code verletzt Lesbarkeit, [Es](../../prozess/praemissen/es.md)),
Diff `9be7f37..7aa6698`.
1. Toter Code, den keine Prüfung sieht: [anwendung.py](../../technik/arbiter/web/anwendung.py)
   schickt V2 und V9 (`einheitAuswählen`, `einheitAbwählen`, `modellAlsEbene`,
   `einheitAlsEbene`, `gesetztesModellDerAusgewählten`) über `spiel()` an die *Schlacht*.
   Dort kommen sie nie an: V2 nimmt nur eine *Einheit* der *Armeeliste*, die in der *Schlacht*
   leer ist (404), V9 verlangt eine *ausgewählte* *Einheit*, die es ohne V2 nicht gibt.
   `Schlacht.auswählen`, `abwählen`, `ebeneWählen`, `ebeneAbwählen`
   ([schlachtrunden.py](../../technik/arbiter/domaene/querschnitt/schlachtrunden.py), Z. 112
   bis 122) sind darum tot; vulture meldet sie nicht, weil `spiel()` sie über
   `Aufstellung | Schlacht` erreicht. Der Vertrag sagt dasselbe:
   „V9 bleibt bei der *Aufstellung* und antwortet 404“ ([Bewegung, Auswahl](../../technik/architektur/vertrag/bewegung.md#auswahl)).
   Baut das nächste Item V14 (`modellAnklicken`) darauf, wählt V9 in der *Schlacht* eine
   *Ebene*, statt 404 zu antworten.
2. Es 6, Indizes auf Fachobjekte: `phaseBeenden` liest die *Phasen* über `_phasen[-1]`,
   `_phasen[_phasen.index(self._phase) + 1]` und `_phasen[0]` (Z. 79 bis 82); der Leser
   rechnet, welche *Phase* gemeint ist.
3. Es 7, Pfeilfunktion als Hülle um einen Aufruf: `() => ersterZugWählen(spielernummer)` und
   `spieler => armeeZu(spielstand, spieler)` ([anfragen.js](../../technik/frontend/anfragen.js),
   Z. 16 und 20); Vorbild für die Regel: Commit `eaa45b9`. Beide entfallen mit
   Gegenvorschlag 1 aus [5680](5680-knoepfeAlsTabelleUndSpielernummer.md), wenn die Tabelle
   die Spielernummer als Argument der `handlung` übergibt.

Am Bildschirm ändert sich nichts.

**Kosten.** Bleibt 1, trägt das nächste Item vier Methoden der *Schlacht* mit, die niemand
erreichen darf, und V9 widerspricht dem Vertrag, sobald V14 auswählt. Nachbessern: etwa 15
Zeilen, ohne neue Tests; `anwendungTest.py` und die Akzeptanztests zu QUE-9 und QUE-10
prüfen es.

**Gegenvorschlag.**
1. V2 und V9 in `anwendung.py` wieder an `aufstellung` (wie vor dem Diff); `spiel()` nur für
   V5 und V10. Die vier Methoden aus `Schlacht` löschen; die Abfragen der *Auswahl*
   (`ausgewählt`, `modellAusgewählt`, `modellIstEbene`, `ganzeEinheitIstEbene`) bleiben (V11).
2. Die Folge als Tabelle: `_nächstePhase = dict(pairwise(Phase))` (`itertools`), dann
   `nächste = _nächstePhase.get(self._phase)`; ohne `nächste` gilt `Phase.kommandophase`
   und `_zugBeenden()`. `_phasen` entfällt.
3. Mit 5680 umsetzen, ohne eigene Zeile.

**Stellungnahme.** Angenommen, mit einer Abweichung.
1. V2 und V9 in [anwendung.py](../../technik/arbiter/web/anwendung.py) gehen wieder an `aufstellung`;
   `spiel()` nur für V5 und V10. `abwählen`, `ebeneWählen`, `ebeneAbwählen` sind aus `Schlacht`
   gelöscht. `Schlacht.auswählen` bleibt: die Akzeptanztests zu QUE-10.5
   (`schlachtrundenTest.py`, Z. 319, 335) rufen es direkt auf, um beim Ziehen eine ausgewählte
   *Einheit* zu haben. Es ist die Domänenmethode, keine Route.
2. `_nächstePhase = dict(pairwise(Phase))` statt `_phasen` mit Indizes.
3. Mit 5680 erledigt, keine Pfeilfunktionen mehr.
