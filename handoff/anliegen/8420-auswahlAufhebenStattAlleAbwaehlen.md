# Auswahl aufheben statt alle abwählen

Form: Kritik
Von: Architekt
An: Implementierer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Hält auf (neuer Code verletzt Lesbarkeit, Es und Wir 2), Diff `85fe22c..b473b0b`,
Teillauf 1 und 2 des Items anhaltenUndAuswahl. Die Architektur hält sonst: `web/` reicht
`karteAnklicken` über `spiel()` an die *Schlacht* wie V19 und die
[Tür](../../technik/architektur/vertrag/schlacht/tuer.md) verlangen, die Regel BEW-9.1 liegt
in der *Schlacht*, nicht in `web/` oder der Seite; Importvertrag, Spiegel, Benennung,
Kommentare und ruff grün, die Tests beider Teilläufe und `tests/einheit` grün. Das unbenutzte
`_stelle` in `Schlacht.karteAnklicken` ist kein Befund: V20 (BEW-14) braucht die *Stelle* im
Item grenzkreise, dann heißt sie `stelle`.

Neu in [auswahl.py](../../technik/arbiter/domaene/phasen/aufstellen/auswahl.py) ist
`alleAbwählen()`. Das Glossar sagt zur *Auswahl*: „höchstens eine für beide *Spieler*
zusammen“; „alle“ lässt den Leser mehrere ausgewählte *Einheiten* suchen, die es nicht gibt.
BEW-9.1 nennt die Handlung: Der Klick „hebt die *Auswahl* auf“. Dazu setzt `abwählen(einheit)`
dieselben zwei Felder ein zweites Mal zurück; dass ohne *Einheit* keine *Ebene* bleibt, steht
damit an zwei Stellen (Wir 3).

**Kosten.** Am Bildschirm nichts. Bleibt es, liest man in `Schlacht.karteAnklicken` eine
Mehrfachauswahl, die die Domäne ausschließt, und eine dritte Rücksetzstelle (etwa für
BEW-14) läuft leicht nur in eine der beiden ein. Umbau: zwei Methoden, drei Zeilen, kein Test
ändert sich (die Akzeptanztests rufen nur `karteAnklicken`).

**Gegenvorschlag.** `alleAbwählen` heißt `auswahlAufheben`; `abwählen(einheit)` ruft es nach
seiner Prüfung:
```python
def abwählen(self, einheit: Einheit) -> None:
    if self._einheit is einheit:
        self.auswahlAufheben()
```

**Stellungnahme.** Angenommen und umgesetzt wie vorgeschlagen: `alleAbwählen` heißt jetzt
`auswahlAufheben` in [auswahl.py](../../technik/arbiter/domaene/phasen/aufstellen/auswahl.py),
`abwählen(einheit)` ruft es nach seiner Prüfung; der Aufruf in
[schlachtrunden.py](../../technik/arbiter/domaene/querschnitt/schlachtrunden.py) heißt
`self._auswahl.auswahlAufheben()`. Verhalten unverändert, ruff grün.
