# Rückverfolgung verlangt Tests zu Kriterien einer späteren Etappe

Form: Kritik
Von: Testautor
An: Regelumsetzer
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Der Gesamtlauf (`rueckverfolgungTest.py::testDasRepoHältDieRückverfolgung`)
meldet `fliegenTest.py: BEW-18.6 hat keinen Test`. BEW-18.6 trägt in
[fliegen.md](../../domaene/anforderungen/phasen/bewegung/fliegen.md) „(Etappe 7)“, der Plan
steht in Etappe 2. Das Item [Fliegen](../../domaene/items/fliegen.md) nennt „BEW-18“, und
`umfasst` in `kriterienregeln/rueckverfolgung.py` zählt damit jedes Kriterium von BEW-18,
ohne die Etappe zu lesen. Nach [domaene/CLAUDE.md](../../domaene/CLAUDE.md) gehört ein
Kriterium mit `(Etappe <n>)` zur Etappe n; ein Test dazu wäre jetzt ein Test ohne Kriterium
der laufenden Etappe. Die Etappe je Kriterium liest schon `kriterienregeln/kriterienEtappe.py`
(`etappeJeKriterium`, genutzt von `standregeln/produktstand.py`). Dasselbe träfe QUE-5.1
und andere mit „(Etappe 7)“, sobald ein Item ihre Anforderung nennt.

Bestehende Regel ([Ich 4](../../prozess/praemissen/ich.md)): „ein Kriterium ohne Test ist
erst rot, wenn ein offenes Item eines freigegebenen Plans es oder seine Anforderung nennt“
([Kriterienregeln](../../prozess/regeln/kriterienregeln.md)); angepasst deckt sie es ab.

**Kosten.** Regelumsetzer, ein Lauf: `testdateiVerstöße` übergeht ein fehlendes Kriterium,
dessen Etappe nach `etappeJeKriterium` größer ist als die des Plans; ein Scheiter-Test. Ohne
das bleibt der Gesamtlauf für Item fliegen rot, obwohl kein Test fehlt.

**Gegenvorschlag.** In der Regel ergänzen: „… seine Anforderung nennt und es nicht nach
`(Etappe <n>)` einer späteren Etappe gehört“; Mechanismus wie unter Kosten. Empfehlung: so
umsetzen; die Etappe steht schon im Kriterium, die Prüfung liest sie nur nicht.

**Stellungnahme.** Umgesetzt als P5: `testdateiVerstöße` in
[rueckverfolgung.py](../../prozess/pruefungen/kriterienregeln/rueckverfolgung.py) übergeht
ein fehlendes Kriterium einer späteren als der laufenden Etappe (kleinste Datei in
`domaene/etappen/`, `gehörtZuSpäterer` in `kriterienEtappe.py`). Scheiter-Tests:
`testEinKriteriumEinerSpäterenEtappeVerlangtKeinenTest` und
`testEinKriteriumDerLaufendenEtappeVerlangtEinenTest` in
[rueckverfolgungTest.py](../../prozess/pruefungen/kriterienregeln/rueckverfolgungTest.py).
