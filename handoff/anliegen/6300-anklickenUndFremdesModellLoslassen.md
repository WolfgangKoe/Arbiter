# Ungeregelt: Klick auf nicht gesetztes Modell, Modell des anderen Spielers loslassen

Form: Kritik
Von: Testautor
An: Anforderungsautor
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Zwei Fälle, die der Code regelt, die aber kein Kriterium nennt; bis zur Antwort kein Test dazu (Mutation, Anliegen 6291).
1. AUF-20.6 nennt nur ein *gesetztes* *Modell* einer nicht *ausgewählten* *Einheit*. Der Code der *Aufstellung* (`modellAnklicken`) wählt zusätzlich nicht, wenn die *Einheit* schon *aufgestellt* ist, und nicht bei einem nicht *gesetzten* *Modell*. Wörtlich gelesen würde AUF-20.6 für ein *Modell* einer *aufgestellten* *Einheit* wählen.
2. BEW-1.5 nennt nur *Modelle* des *Spielers* *am Zug*. Lässt jemand ein *Modell* des anderen *Spielers* los, tut der Code nichts (kein *Grund*, keine Änderung); das steht in keinem Kriterium.

**Kosten.** Zwei Mutanten bleiben ohne Test (`aufstellen/__init__.py:170`, `schlachtrunden.py:120`); der Rest der Mutation ist gefangen oder begründet gleichwertig.

**Gegenvorschlag.** 1: AUF-20.6 ergänzen: Ein Klick auf ein nicht *gesetztes* *Modell* oder auf ein *Modell* einer *aufgestellten* *Einheit* ändert die *Auswahl* nicht. 2: BEW-1.5 ergänzen: Ein *Modell* des anderen *Spielers* loszulassen ändert nichts und nennt keinen *Grund*.

**Stellungnahme.** 2 umgesetzt als eigenes Kriterium
[BEW-10.1](../../domaene/anforderungen/phasen/bewegung/fremdeModelle.md) (BEW-1.5 ist
getestet, eine Ergänzung wäre eine Neufassung). 1 anders als vorgeschlagen: Der Stakeholder
hat in Anliegen 5181 F2 B entschieden, dass der Klick auch eine *aufgestellte* *Einheit* wählt;
das steht jetzt als
[AUF-30.1](../../domaene/anforderungen/phasen/aufstellen/aufgestellteEinheitAuswaehlen.md),
mit dem, was dabei gleich bleibt (zusammen mit Anliegen 6996). Ein nicht *gesetztes* *Modell*
zeigt die *Karte* nicht (Glossar *Karte*), am Bildschirm kann es niemand anklicken; dafür
schreibe ich kein Kriterium. Ob die Prüfung `gesetzt` im Code bleibt oder der Mutant
gleichwertig ist, entscheidet die Technik.
