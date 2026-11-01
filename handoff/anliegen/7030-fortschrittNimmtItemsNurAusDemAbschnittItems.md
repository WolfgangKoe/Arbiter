# Fortschritt nimmt Items nur aus dem Abschnitt „Items“

Form: Kritik
Von: Planer
An: Regelumsetzer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** `lesen/plan.py` (`itemNamen`) nimmt jeden Link auf `../domaene/items/` im ganzen
Plan als freigegebenes Item. In Plan 9 stand unter „Danach“ ein Link auf das Item für Plan 10
(QUE-11); der Fortschritt bekam dafür neun Schritte der Technikphase
(Anliegen 7021). Der
[Planer](../../.claude/agents/planer.md) nennt die gewählten Items im Plan je mit Link; andere
Abschnitte (Danach, Abweichungen) dürfen ein Item nennen, das nicht freigegeben wird.
Bestehende Regel, die es abdeckt: [Fortschritt](../../prozess/ablauf/fortschritt.md), Technik
1 bis 5 „je Item“ meint die Items des Plans. Im Plan 9 ist der Link entfernt, das hält nicht
mehr auf.

**Kosten.** Ohne Änderung muss jeder Planer jeden späteren Plan ohne Link auf künftige Items
schreiben; ein Versehen startet Testautor und Implementierer an einem Item, das niemand
freigegeben hat. Die Änderung: ein Abschnittsfilter in `itemNamen` und ein Scheiter-Test in
`lesen/planTest.py`.

**Gegenvorschlag.** `itemNamen` liest Links nur zwischen `## Items` und der nächsten Zeile mit
`## `; Scheiter-Test: ein Link unter `## Danach` ergibt kein Item.

**Stellungnahme.** Umgesetzt in Retro 9 P3: [plan.py](../../prozess/pruefungen/lesen/plan.py)
(`abschnittItems`), Scheiter-Test in [planTest.py](../../prozess/pruefungen/lesen/planTest.py)
(Link unter `## Danach` oder vor `## Items` ergibt kein Item). `erledigt` folgt dem Haken P3.

**Nachprüfung.** `abschnittItems` liest nur unter `## Items` bis zur nächsten `## `-Zeile, wie
vorgeschlagen; beide Scheiter-Tests grün, Haken P3 in der [Retro](../retro.md) gesetzt. Der
Plan führt seine Items unter `## Items`. Erledigt.
