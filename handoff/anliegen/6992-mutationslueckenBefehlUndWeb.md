# Mutationslücken im Befehl und in web

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: offen
Wartet auf: Technikphase 9

## Runde 1
**Befund.** Voller Mutationslauf von Zyklus 8, rot bei 93 % ([DoD](../../prozess/ablauf/dod.md)).
Fünf Überlebende fehlt ein Unit-Test:
1. [`__main__.py`](../../technik/arbiter/__main__.py) Zeile 18, `LtE wird Lt`: Port 65535
   ist gültig, [befehlTest.py](../../technik/tests/einheit/befehlTest.py) prüft nur 0 und die
   Ablehnung von 65536.
2. [anwendung.py](../../technik/arbiter/web/anwendung.py) Zeile 27, `_größterNenner = 10**6`,
   `10 wird 11` und `6 wird 7`: Die Rundung auf Nenner höchstens 10⁶
   ([Architektur Domäne](../../technik/architektur/domaene.md)) prüft kein Test.
3. [kennungen.py](../../technik/arbiter/web/kennungen.py) Zeile 49, `raise entfällt`:
   `kennungenDerEinheit` mit einer Einheit außerhalb der Aufstellung gibt dann None statt
   `ValueError`.
4. [server.py](../../technik/arbiter/web/server.py) Zeile 69, `raise entfällt`: Ein anderer
   `OSError` als die belegte Adresse würde beim Binden verschluckt; `Server.__init__` bricht
   danach mit einem `TypeError` ab.

**Kosten.** Am Bildschirm nichts. Wir: 5 der 32 Überlebenden; vier kleine Tests.

**Gegenvorschlag.** 1: `"65535"` als gültige Angabe in `testMitPortGiltDieAngabe`.
2: Eine Koordinate mit mehr Nachkommastellen, etwa `0.0000009`, wird zu `1/10⁶`; das fängt
`11**6` und `10**7`. 3: Vorbedingungsverletzung wie in
[aufstellenTest.py](../../technik/tests/einheit/domaene/phasen/aufstellenTest.py), eine fremde
Einheit wirft `ValueError`. 4: `socket.create_server` per `monkeypatch` wirft
`OSError(errno.EACCES)`; `serverStarten` gibt ihn weiter.

**Stellungnahme.**
