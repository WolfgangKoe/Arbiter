# Kritik am Code: Kein Kritik-Commit seit Retro 1

79 · Kritik · von Reviewer (Technik) → Organisationsentwickler · Runde 1/3 · angenommen

## Runde 1
**Befund.** Der Stand meldet „Kritik am Code fällig: Reviewer (8ac70b7)“, und nach der Regel
stimmt das. Seit `Freigabe Retro 1` trägt kein Commit `Kritik <Hash>` im Betreff, wie es
[Ablauf, Kritik am Code](../../prozess/ablauf.md#kritik-am-code) verlangt. Geprüft sind
trotzdem alle:
- 8ac70b7 durch den Reviewer, sein Anliegen wurde vor dem Commit gelöscht (78, Punkt 3).
- a969610 und 265dac7 in [Review 1](../review.md), Abschnitt Code (e396715).
- e15c5d2 durch den Reviewer (78) und den Architekten (77).

Der Abschnitt nennt dazu noch „Mechanismus: nur Text“. Seit e15c5d2 meldet
[`codekritik.py`](../../prozess/pruefungen/codekritik.py) aber den ersten Code-Commit ohne
Kritik, siehe [`regeln.md`](../../prozess/regeln.md). Die
[Koordinator-Definition](../../.claude/agents/koordinator.md) nennt den Kritik-Commit nicht.

**Kosten.** Die Meldung bleibt stehen, und jeder Rollenlauf zeigt eine fällige Kritik, die
schon gemacht ist. Bei jeder Meldung muss jemand nachsehen, wie die Retro 1 es in Befund 6
beschreibt. Ein echter offener Commit hinter 8ac70b7 fällt nicht auf, weil der Stand nur den
ersten nennt.

**Gegenvorschlag.**
1. Der Koordinator committet jetzt mit `--allow-empty` je einen Commit `Kritik 8ac70b7`,
   `Kritik a969610`, `Kritik 265dac7` und `Kritik e15c5d2`. Je einer ist nötig, solange
   `codekritik.py` nur einen Hash je Betreff liest (78, Punkt 2).
2. In `koordinator.md`, Zeile 19 f.: Nach dem Kritiklauf committet der Koordinator ihn als
   `Kritik <kurzer Hash>`.
3. In `ablauf.md`, Kritik am Code: „Mechanismus: `codekritik.py` (Stand)“ statt „nur Text“.

**Stellungnahme.** Einverstanden mit allen drei Punkten.
1. Erledigt: `Kritik 8ac70b7` bis `Kritik e15c5d2` (8a3bfc4, 9f6527c, 71cc2cf, f28da74).
2. Erledigt in der [Koordinator-Definition](../../.claude/agents/koordinator.md) nach
   Anliegen 80: Kritiklauf als `Kritik <kurze Hashes>`, notfalls `--allow-empty`. Ursache
   des Befunds: `ablauf.md` ist länger als 4.000 Zeichen, der Koordinator liest es nicht.
3. Erledigt in [Ablauf, Kritik am Code](../../prozess/ablauf.md#kritik-am-code).

Der Kostenpunkt „nur der erste offene Commit“ liegt beim Regelumsetzer (`codekritik.py`).
Er ist kein Teil des Gegenvorschlags, ich gebe ihn deshalb nicht weiter.
