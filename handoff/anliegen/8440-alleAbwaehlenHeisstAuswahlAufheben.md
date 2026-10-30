# alleAbwählen heißt nach BEW-9 Auswahl aufheben

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Lesbarkeit der Änderung seit 85fe22c (Stand b473b0b, Teillauf 1 und 2 von
anhaltenUndAuswahl). Tests und Benennung grün; ein Befund in
[auswahl.py](../../technik/arbiter/domaene/phasen/aufstellen/auswahl.py), Zeile 27:
1. Der Name `alleAbwählen` sagt, es gebe mehrere *ausgewählte* *Einheiten*. Nach dem
   [Glossar](../../domaene/glossar.md) ist die *Auswahl* „höchstens eine für beide *Spieler*
   zusammen“, und [BEW-9.1](../../domaene/anforderungen/phasen/bewegung/abwaehlen.md) sagt
   „hebt die *Auswahl* auf“. Der Name trägt nicht die Bedeutung ([Es](../../prozess/praemissen/es.md),
   Lesbarkeit; [Wir 2](../../prozess/praemissen/wir.md)).
2. Sein Rumpf wiederholt die zwei Zeilen von `abwählen(einheit)` darüber
   ([Wir 3](../../prozess/praemissen/wir.md)).

Einordnung: hält auf (neuer Code verletzt Lesbarkeit, [Kritik](../../prozess/ablauf/kritik.md)).

**Kosten.** Wer `Schlacht.karteAnklicken` liest, sucht eine zweite *Einheit*, die es nicht
gibt; ändert sich, was zur *Auswahl* gehört (etwa ein weiteres Feld), muss es an zwei
Stellen gleich geändert werden. Umbenennen kostet zwei Zeilen, keinen Test.

**Gegenvorschlag.** `Auswahl.alleAbwählen` heißt `aufheben()`, der Aufruf in
[schlachtrunden.py](../../technik/arbiter/domaene/querschnitt/schlachtrunden.py) Zeile 163
`self._auswahl.aufheben()`; `abwählen(einheit)` ruft innerhalb seiner Bedingung
`self.aufheben()`, statt die Felder selbst zurückzusetzen.

**Stellungnahme.** Angenommen, mit dem Namen `auswahlAufheben` statt `aufheben()` (wie in
Anliegen 8420, derselbe Befund): [auswahl.py](../../technik/arbiter/domaene/phasen/aufstellen/auswahl.py)
und [schlachtrunden.py](../../technik/arbiter/domaene/querschnitt/schlachtrunden.py)
umgestellt; `abwählen(einheit)` setzt die Felder nicht mehr selbst zurück, sondern ruft
`auswahlAufheben()`.
