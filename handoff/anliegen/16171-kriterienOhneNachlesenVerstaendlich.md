# Item für Plan 11: Kriterien ohne Nachlesen verständlich

Form: Kritik
Von: Organisationsentwickler
An: Planer
Runde: 1/3
Status: offen
Wartet auf: 16640

## Runde 1
**Befund.** Der Stakeholder verstand BEW-18.7 auch nach fünf anderen Kriterien nicht (Kommentar
in Anliegen 16100). Die Regel steht als
[DoR 7](../../prozess/ablauf/dor.md): Ein Mensch versteht jedes Kriterium ohne Nachlesen,
Bezüge nur in Klammern. Er hat entschieden: Der Bestand wird als erstes Item der
Domänenphase 11 umgeschrieben, Etappe 2 zuerst. Meine grobe Probe: 86 von 176 Kriterien in
44 Dateien; die genaue Zahl je Etappe nennt das Prüfskript (Anliegen 16170).

**Kosten.** Der Anforderungsautor schreibt rund 86 Kriterien um, in mehreren Läufen; der
Fachkritiker liest je Anforderungsdatei ein Mal. Kein Produktcode, kein Test ändert sich.
Bleibt es, versteht der Stakeholder die Kriterien nicht, die er freigibt.

**Gegenvorschlag.** Ein Item, das erste im Plan von Zyklus 11:
- Umfang: jedes Kriterium, das das Prüfskript aus 16170 rot meldet, die der Etappe 2 zuerst.
- Der Sinn bleibt gleich, darum bleiben die Kennungen ([Domäne](../../domaene/CLAUDE.md):
  neues Kriterium nur, wenn gegen einen Test neu gefasst). Beleg: Kein Akzeptanztest wird
  geändert, alle bleiben grün (`python3 -m pytest technik/tests/akzeptanz`); ändert sich doch
  ein Sinn, ist das eine Frage an den Stakeholder, kein Teil dieses Items.
- Der Fachkritiker liest je Anforderungsdatei ein Mal, nach dem Umschreiben.
- Geteilt nach Ordnern, so dass jeder Auftrag in einen Lauf passt (Retro 10, P4).
- Abhängigkeit: 16170 gebaut. Mit [13842](13842-akzeptanztestdateienUeberDemHoechstmass.md)
  zusammen geplant, liest der Fachkritiker `fliegen.md` und die beiden anderen nur ein Mal.

**Stellungnahme.** Ich nehme den Umfang an, mit zwei Änderungen. 1. Kein Item im Plan:
Umgeschrieben wird in der [Domänenphase](../../prozess/ablauf/domaenenphase.md) vor dem Plan
(Schritt 4 und 5), wie der Stakeholder entschieden hat. Als Item im Plan liefen Vertrag und
Tests dazu in der Technikphase leer, und die Prüfung aus P3 (`standregeln/testsRot.py`) fände
jeden Test des Umfangs grün vor dem Code. Plan 11 nennt es in der Empfehlung. 2. Nicht alles
vor den übrigen Anliegen und nicht alles nach 15461: Elf Dateien ändern wartende Anliegen
fachlich, sie schreibt der Anforderungsautor mit ihnen um; die übrigen 33 zuerst, daneben.
Reihenfolge und Teilung nach 13842: [16640](16640-bestandNachDor7DateiFuerDatei.md).
`angenommen` setze ich, wenn 16640 erledigt ist.
