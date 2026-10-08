# Der Dienst-Test zu AUF-6.1 trifft die Wahl selbst

328 · Kritik · von Fachkritiker (Domäne) → Testautor · Runde 1/3 · angenommen

## Runde 1
**Befund.** `testAuf6_1DerSpielstandNenntSpielerZweiAnDerReiheUndSpielerEinsDieErsteZone`
(`auf6Test.py`, d9ddabd) ruft `gewinnerWählen(spielerEins)` und
`aufstellungszoneWählen(Aufstellungszone.erste)` selbst auf. Danach prüft er nur, wie V1
diesen Stand ausgibt. AUF-6.1 verlangt aber, dass Arbiter diese Wahl *nach dem Start nach
QUE-2.1* selbst getroffen hat. Der Test ist schon vor dem Code grün (ausgeführt: 1 passed
neben 25 roten Dienst-Tests). Er prüft eher AUF-1.3, AUF-4.4 und AUF-4.6 über V1 als AUF-6.1.

**Kosten.** `kriterienregeln/rueckverfolgung.py` zählt ihn als Test zu AUF-6.1. Das Kriterium
hält nur der Bildschirmtest gegen den Befehl. Fällt die Wahl beim Start weg, bleibt dieser
Test grün. Wenn AUF-6 nach dem Plan später entfällt, wird er gelöscht, obwohl er die Darstellung
einer Wahl prüft, die bleibt.

**Gegenvorschlag.** Eine von zwei Möglichkeiten:
(a) Der Test fragt den Spielstand, den der Start erzeugt. Das ist dieselbe Funktion, die
`python3 -m arbiter` aufruft. Ihren Namen legt der Architekt fest; der Test trifft die Wahl
also nicht selbst.
(b) Der Test entfällt. AUF-6.1 halten dann die drei Bildschirmtests gegen den Befehl.

Erledigt, wenn kein Test zu AUF-6.1 die Wahl selbst trifft.

**Stellungnahme.**
Umgesetzt mit (b): Der Test `testAuf6_1DerSpielstandNenntSpielerZweiAnDerReiheUndSpielerEinsDieErsteZone`
ist aus `auf6Test.py` entfernt. Variante (a) braucht eine Startfunktion, die es nicht gibt und
deren Namen ich nicht erfinde. AUF-6.1 halten die drei Bildschirmtests gegen den Befehl; die
Darstellung der Wahl in V1 deckt schon AUF-4 ab.
