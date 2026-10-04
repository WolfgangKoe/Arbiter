# Domäne: Die Prüfungen beim Setzen leiten Spieler und eigene Modelle je Schritt neu ab

160 · Kritik · von Reviewer (Technik) → Implementierer · Runde 1/3 · erledigt

## Runde 1
Gegenstand: b940ef8 (Kritik am Code), Umsetzung von Anliegen 154.
`python3 -m pytest technik/tests` 153 grün, `python3 -m pytest prozess/pruefungen` 443 grün,
ruff grün. Die Tabelle `_prüfungen`, `_zonen` und `Armee.modelle` lesen sich gut; zwei
Kleinigkeiten.

**Befund.**
1. `aufstellen.py`, `_inNahkampfreichweiteVonGegnern`: `anderes not in spieler.armee.modelle`
   steht im Generator. `Armee.modelle` ist eine Property ohne Zwischenspeicher und baut die
   `frozenset` aller Modelle der Armee je *gesetztem* Modell neu; vorher geschah das einmal
   je *Setzen* (`eigene = _modelleVon(spieler)`).
2. `aufstellen.py`: `spieler = self._anDerReihe` mit `assert spieler is not None  # Warum: …`
   steht jetzt dreimal wortgleich (`aufstellenDerEinheitBeenden`, `_nichtGanzInDerZone`,
   `_inNahkampfreichweiteVonGegnern`).

**Kosten.** 1: Aufwand je *Setzen* wächst mit gesetzten Modellen mal Modellen der Armee
statt mit ihrer Summe; heute 22 Modelle und unmerklich, ab `web/` liegt es auf dem Weg
jedes Ziehens. 2: dieselbe Begründung an drei Stellen; jede neue Prüfung aus der Tabelle,
die den Spieler braucht, kopiert sie ein weiteres Mal.

**Gegenvorschlag.**
1. `eigene = spieler.armee.modelle` vor dem `any(…)` und im Generator `anderes not in eigene`.
2. Eine private Property `_spielerAnDerReihe -> Spieler` mit dem einen `assert` und seiner
   Begründung; die drei Stellen rufen sie.

Erledigt, wenn 1 umgesetzt ist, 2 umgesetzt oder begründet abgelehnt ist und beide
Testläufe grün sind.

**Stellungnahme (Implementierer).** Angenommen, beides umgesetzt in `aufstellen.py`:
1. `_inNahkampfreichweiteVonGegnern` bildet `eigene = spieler.armee.modelle` einmal je Setzen.
2. Die Property `_spielerAnDerReihe` trägt das eine `assert` mit Begründung; die drei Stellen
   rufen sie.
`python3 -m pytest technik/tests` und `python3 -m pytest prozess/pruefungen` grün.

**Nachprüfung (Reviewer).** In 9b003b1 umgesetzt: `eigene` einmal je Setzen,
`_spielerAnDerReihe` mit dem einen `assert`, drei Aufrufer. Die Invariante der Begründung hält
für alle drei (beide Wege prüfen vorher `einheitInAufstellung`). Tests grün (153 und 450),
ruff grün. Erledigt.
