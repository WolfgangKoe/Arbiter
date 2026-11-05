# Freiwillige Schlüssel in Name und Meldung der Tabellenprüfung

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: offen
Wartet auf: Technikphase 11

## Runde 1
**Befund.** Seit 11840 liest `genauDieseSchlüsselLesen` auch `freiwillig`e Schlüssel
([eintragLesen.py](../../technik/arbiter/katalog/eintragLesen.py)). Name und Meldung sagen
noch „genau“: Ein *Datenblatt* mit `oc` meldet „braucht genau die Schlüssel
['modellarten']“, obwohl `fliegen` auch erlaubt ist. Der neue Parameter hat keinen eigenen
Fall in `tests/einheit/katalog/eintragLesenTest.py`, nur über `datenblaetterTest.py`
([Es](../../prozess/praemissen/es.md), Lesbarkeit und 2).

**Kosten.** Wer einen Wert in `datenblaetter.yaml` einträgt und sich vertippt (`Fliegen`),
liest eine Meldung, die `fliegen` nicht nennt; der Name verspricht, was die Funktion nicht
mehr tut. Kein Verhalten falsch, darum wartend.

**Gegenvorschlag.** Meldung nennt beide Mengen, etwa „braucht die Schlüssel [...], erlaubt
dazu [...]“; Name nach der Aufgabe, etwa `schlüsselNachTabelleLesen`; in
`eintragLesenTest.py` je ein Fall: freiwilliger Schlüssel da, fehlt, Pflichtschlüssel fehlt
neben freiwilligem.

**Stellungnahme.**
