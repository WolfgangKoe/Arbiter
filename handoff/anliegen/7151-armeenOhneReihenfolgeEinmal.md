# MIV-1.5: Armeen ohne Reihenfolge einmal vergleichen

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Wartet (Ablage von Hilfsfunktionen, keine Prüfung rot). In
[ausgangslageTest.py](../../technik/tests/akzeptanz/missionsvorbereitung/ausgangslageTest.py)
steht dreimal dasselbe Gerüst `sorted(sorted(... sorted(...) ...) for armee ...)`: in
`einheitenAusDenDaten`, in `einheitenDerAusgangslage` und in
`testMiv1_5DieAusgangslageHatDieZweiArmeenMitIhrenEinheiten`, dazu dreimal
`(ausgangslage.ersterSpieler, ausgangslage.zweiterSpieler)`. Die Tests prüfen richtig; man
liest aber drei verschachtelte Sortierungen, bis man sieht, dass sie nur „Reihenfolge egal“
heißen ([Es](../../prozess/praemissen/es.md), Lesbarkeit; [Wir 3](../../prozess/praemissen/wir.md)).
Außerdem hängen `einheitenAusDenDaten("bewegungsweite")` und `bewegungsweiteDes` nur über
die Stelle im Aufruf zusammen.

**Kosten.** Ein Umbau der Hilfen im Test, kein anderes Verhalten der Tests; am Bildschirm
nichts.

**Gegenvorschlag.** Eine Hilfe `ohneReihenfolge(armeen)` sortiert einmal auf allen drei Ebenen;
`einheitenAusDenDaten` und `einheitenDerAusgangslage` liefern nur noch Listen je *Armee* von
(*Name*, Werte je *Modell*), der erste Test vergleicht die *Namen* daraus. Die Paare aus
Schlüssel und Merkmal stehen in einer Tabelle (`{"bewegungsweite": bewegungsweiteDes, …}`),
der Test nennt nur den Schlüssel.

**Stellungnahme.** Angenommen und umgesetzt. `ohneReihenfolge` sortiert jede Liste auf jeder
Ebene und lässt Tupel in ihrer Ordnung; `einheitenAusDenDaten` und `einheitenDerAusgangslage`
liefern nur noch Listen je *Armee* von (*Name*, Werte je *Modell*). Der erste Test vergleicht
die *Namen* über `namenJeArmee`, erst danach ohne Reihenfolge, damit ein falscher Wert an einem
*Modell* ihn nicht rot macht. Schlüssel und Merkmal stehen in `merkmalZumSchlüssel`, die Tests
nennen nur den Schlüssel; das Paar der *Spieler* steht einmal in `spielerDer`. Verhalten
unverändert, 15 Tests grün.
