# Tests mit einem Modell als Ebene prüfen den Aufbau nicht

Form: Kritik
Von: Fachkritiker
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Kritik an den Tests zu Item anhaltenUndAuswahl. Hält auf nach
[Kritik](../../prozess/ablauf/kritik.md) („ein Test prüft sein Kriterium nicht“) und
[Technikphase](../../prozess/ablauf/technikphase.md) Schritt 1 („rot“), wie Anliegen 7300:
`testBew7_2EinKlickAufDasModellDerEbeneMachtDieGanzeEinheitZurEbene` (beide Fälle) und
`testBew7_2DerDienstNenntNachDemDrittenKlickKeineEbeneUndAlleModelleAusgewählt` in
[auswahlInDerSchlachtTest.py](../../technik/tests/akzeptanz/phasen/bewegung/auswahlInDerSchlachtTest.py)
sind heute grün, obwohl es BEW-7 noch nicht gibt: `Schlacht.modellAnklicken` wählt immer die
ganze *Einheit*. Der Aufbau `modellZurEbeneMachen` in
[schlacht.py](../../technik/tests/akzeptanz/schlacht.py) stellt nicht fest, dass die *Ebene*
danach ein *Modell* ist; das verlangt BEW-7.2 im „Gegeben … deren *Ebene* ein *Modell* ist“.
Ebenso wird `testBew9_1EinKlickAufDieLeereKarteHebtAuchEineAuswahlMitEinemModellAlsEbeneAuf` in
[abwaehlenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/abwaehlenTest.py) grün, sobald
der Klick auf die leere *Karte* geht, auch ohne BEW-7.1; er unterscheidet dann nicht vom
ersten Test zu BEW-9.1.

**Kosten.** Am Bildschirm nichts. Ohne Änderung gehen drei Tests in die Umsetzung, die BEW-7.2
nicht prüfen; der Implementierer kann BEW-7.2 vergessen, ohne dass ein Test rot wird. Eine
Zeile.

**Gegenvorschlag.** In `modellZurEbeneMachen` nach dem Klick
`assert schlacht.modellIstEbene(modell)`; alle Nutzer erhalten so ihr „Gegeben“. Wollt ihr
keine Prüfung in einem Handgriff, dieselbe Zeile im Aufbau der drei Tests. Erledigt: die drei
Tests sind rot, bis BEW-7.1 gebaut ist.

Die übrigen Tests des Items treffen ihr Kriterium. Zu Recht schon grün sind die beiden zu
BEW-6.3 mit der *Bewegungsweite* als kürzester Strecke (dort halten beide Grenzen auf der
Strecke an, heute schon richtig nach BEW-3), die zu BEW-10.1 in Domäne und Dienst (gebaut seit
BEW-1, Anliegen 6300) und der zu AUF-30.1, was gleich bleibt. Ob die Tests der Seite aus dem
richtigen Grund rot sind, ließ sich nicht prüfen: Heute lädt keine Seite der *Karte*, auch
die älteren Tests zu BEW-1.7 und BEW-2.6 nicht; das prüfe ich bei der Abnahme.

**Stellungnahme.** Umgesetzt mit der zweiten Möglichkeit: die Zeile
`assert <schlacht>.modellIstEbene(angeklickt)` im Aufbau der drei Tests, direkt nach
`modellZurEbeneMachen`, in
[auswahlInDerSchlachtTest.py](../../technik/tests/akzeptanz/phasen/bewegung/auswahlInDerSchlachtTest.py)
(beide Tests zu BEW-7.2) und
[abwaehlenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/abwaehlenTest.py) (der zweite
zu BEW-9.1). Nicht im Handgriff: [schlacht.py](../../technik/tests/akzeptanz/schlacht.py) ändert
gerade der andere Testautor für Item grenzkreise, und `modellZurEbeneMachen` dient auch
[grenzen.py](../../technik/tests/akzeptanz/grenzen.py) und den Tests zu BEW-7.1 und 7.3, deren
Aufbau das Anliegen nicht nennt. Alle vier Fälle sind rot an dieser Zeile
(`AssertionError: assert False`), bis BEW-7.1 gebaut ist.
