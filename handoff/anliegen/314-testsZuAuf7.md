# Tests zu AUF-7

314 · Kritik · von Anforderungsautor (Domäne) → Testautor (Technik) · Runde 1/3 · angenommen

## Runde 1
**Befund.** Nach [312](312-teilungVonAuf1.md) sind AUF-1.8 bis AUF-1.11 aus AUF-1 in eine
eigene Anforderung gezogen, gleichlautend als AUF-7.1 bis AUF-7.4
([aufstellen.md](../../domaene/anforderungen/phasen/aufstellen.md)). Die alten Kennungen
kommen nicht wieder. AUF-3.8 verweist jetzt auf AUF-7.2 und AUF-7.3, sein Inhalt bleibt.
Die 18 Tests `testAuf1_8…` bis `testAuf1_11…` in
`technik/tests/akzeptanz/phasen/aufstellen/auf1Test.py` haben damit kein Kriterium mehr.

**Kosten.** `testDasRepoHältDieRückverfolgung` in `prozess/pruefungen` bleibt rot, bis die
Tests umgezogen sind (4 Meldungen, AUF-1.8 bis AUF-1.11).

**Gegenvorschlag.** Die Tests nach `technik/tests/akzeptanz/phasen/aufstellen/auf7Test.py`
verschieben und umbenennen: `testAuf1_8…` → `testAuf7_1…`, `testAuf1_9…` → `testAuf7_2…`,
`testAuf1_10…` → `testAuf7_3…`, `testAuf1_11…` → `testAuf7_4…`; der Satz nach dem
Unterstrich bleibt. Gemeinsame Fixtures und Handgriffe ziehen mit, wo nur noch `auf7Test.py`
sie braucht. Die offenen Punkte aus [311](311-testsDerAufstellungNachDerWahl.md) und
[313](313-wahlDerEinheitInDenTestsDerAufstellung.md) zu diesen Tests gelten danach für die
neuen Namen.

**Stellungnahme.** Angenommen und umgesetzt: Die Tests liegen in `auf7Test.py` als `testAuf7_1…` bis `testAuf7_4…`. `nachDerWahlDerAufstellungszone` zog in `handgriffe.py` um, weil `auf1Test.py` und `auf7Test.py` es brauchen.
