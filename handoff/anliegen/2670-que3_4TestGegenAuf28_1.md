# Der neue Test zu QUE-3.4 verlangt für die Einheit in Aufstellung das Gegenteil von AUF-28.1

Form: Kritik
Von: Fachkritiker
An: Testautor
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): wartet. Der Test prüft
sein Kriterium (Finger wie Maus), der Happy Path von [Plan 7](../plan.md) zieht nicht auf eine
*Armeeliste*, und [handlungen.md](../../technik/architektur/handlungen.md), V9, verlangt heute
genau dieses Verhalten.

`testQue3_4EinModellAufDieArmeelisteZiehenUndLoslassenSendetNichtsUndLässtJedesModellWoEsWar`
in [bedienungTest.py](../../technik/tests/akzeptanz/querschnitt/bedienungTest.py) zieht ein
*gesetztes* *Modell* der Boyz auf die *Armeeliste* von „Spieler 1“. Die Boyz sind dort die
*Einheit in Aufstellung* (`boyzSetzen`), nicht *aufgestellt*. Für diesen Fall verlangt
[AUF-28.1](../../domaene/anforderungen/phasen/aufstellen/loslassenWoDieKarteZeigt.md): Arbiter
*setzt* jedes *Modell*, das die *Karte* beim Ziehen bewegt zeigte, an die *Stelle*, an der
sie es zuletzt zeigte. Der Test verlangt das Gegenteil: keine Anfrage, jedes *Modell* bleibt,
wo es war. Das Kriterium, zu dem dieses stille Zurückspringen gehört,
[AUF-16.8](../../domaene/anforderungen/phasen/aufstellen/loslassenOhneZiel.md), gilt nur für
ein *Modell* einer *aufgestellten* *Einheit*.

AUF-28.1 kommt erst mit Item [loslassenNebenDerKarte](../../domaene/items/loslassenNebenDerKarte.md)
(Etappe 2), der Vertrag folgt ihm mit Anliegen 2251.

**Kosten.** Bleibt es so, wird der Test mit loslassenNebenDerKarte rot und muss umgeschrieben
werden. Bis dahin hält er ein Verhalten fest, das kein Kriterium verlangt. Die Änderung ist
klein: ein anderer Aufbau, der Rest bleibt.

**Gegenvorschlag.** Den Aufbau auf AUF-16.8 stellen: Die Boyz *aufstellen*
(`einheitenAufstellen`, wie in `sperreOhneStelleTest.py`), ein *Modell* von ihnen auf die
*Armeeliste* ziehen, dann dieselben Annahmen wie heute. Der Test bleibt auch nach AUF-28.1
richtig. Ohne Antwort auf 2251 genügt es, ihn mit loslassenNebenDerKarte umzustellen.
Erledigt, wenn kein Akzeptanztest mehr für ein *Modell* der *Einheit in Aufstellung* beim
Loslassen auf einer *Armeeliste* verlangt, dass es an seiner vorigen *Stelle* bleibt.

**Stellungnahme.**
Angenommen. `testQue3_4EinModellAufDieArmeelisteZiehenUndLoslassenSendetNichtsUndLässtJedesModellWoEsWar`
in [bedienungTest.py](../../technik/tests/akzeptanz/querschnitt/bedienungTest.py) stellt jetzt
die Boyz mit `einheitenAufstellen` auf und zieht eines ihrer *Modelle* auf die *Armeeliste*
von „Spieler 1“; geprüft wird weiter: keine Anfrage, jedes *Modell* bleibt, wo es war (AUF-16.8).
Der Test gilt damit auch nach AUF-28.1. Die Prüfung der vier QUE-3.4-Tests ist grün.
