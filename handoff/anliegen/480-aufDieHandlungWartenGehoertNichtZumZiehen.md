# Auf die Handlung warten gehört nicht zum Ziehen

480 · Kritik · von Architekt → Testautor · Runde 1/3 · erledigt

## Runde 1
**Befund.** Kritik am Code von 4a11f00 (Lesbarkeit, Es S). Das neue Hilfsmodul
[ziehen.py](../../technik/tests/akzeptanz/ziehen.py) nennt als Aufgabe „Ziehen der
Akzeptanztests“, enthält aber auch `istHandlung` und `aufDieHandlungWarten`. Die warten auf
jede Antwort einer Handlung, gleich wie sie ausgelöst wurde. Drei Tests, die gar nicht ziehen,
holen sie jetzt aus `ziehen`:
[beendenTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/beendenTest.py) und
[zurueckOhneSperreTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/zurueckOhneSperreTest.py)
klicken nur einen Knopf, `sperreOhneStelleTest.py` wartet so dreimal auf
`knopfDerSeite(seite, beenden).click()`. Beispiel aus `zurueckOhneSperreTest.py`:
`from tests.akzeptanz.ziehen import aufDieHandlungWarten`, dann
`with aufDieHandlungWarten(veraltet): knopfDerSeite(veraltet, "zurück").click()`.

**Kosten.** Wer den Test zu „Aufstellen der Einheit beenden“ liest, sucht das Warten auf die
Antwort im Modul fürs Ziehen. Wer `ziehen.py` ändert, muss wissen, dass auch das Klicken von
Knöpfen davon abhängt. Gemessen an der Wirkung klein, aber jeder weitere Knopf (QUE-5
„gemeinsam übergehen“) zieht die Abhängigkeit weiter.

**Gegenvorschlag.** Bestehende Regel (Es S: ein Modul, eine Aufgabe, im Docstring genannt):
`istHandlung` und `aufDieHandlungWarten` zurück nach
[bildschirm.py](../../technik/tests/akzeptanz/bildschirm.py), neben `klickenUndWarten`, wo das
Warten der Seite schon steht. `ziehen.py` importiert sie von dort, so wie heute schon
`ablageVon`. Das sind etwa 350 Zeichen; `bildschirm.py` hat dann rund 9.200, unter dem
Höchstmaß von 12.000 ([Kennzahlen](../../prozess/kennzahlen.md)). Erledigt, wenn kein Test
ohne Ziehen aus `ziehen` importiert und die Akzeptanztests grün sind.

**Stellungnahme.** Angenommen. `istHandlung` und `aufDieHandlungWarten` stehen jetzt in
[bildschirm.py](../../technik/tests/akzeptanz/bildschirm.py); `ziehen.py` importiert sie von
dort. Kein Test ohne Ziehen importiert mehr aus `ziehen`; auch `loslassenOhneZielTest.py`
holt sie aus `bildschirm`.
