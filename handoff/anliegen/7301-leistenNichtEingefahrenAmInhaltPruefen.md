# Leisten: nicht eingefahren am Inhalt prüfen, Namen nach dem Glossar

Form: Kritik
Von: Fachkritiker
An: Testautor
Runde: 1/3
Status: offen
Wartet auf: Technikphase 10

## Runde 1
**Befund.** Kritik an den Tests zu Item gemeinsamUebergehen, wartet nach
[Kritik](../../prozess/ablauf/kritik.md) (Lücke abseits des Happy Path, Namen), in
[leistenTest.py](../../technik/tests/akzeptanz/querschnitt/leistenTest.py):
1. `testQue6_2NachDemStartIstKeineLeisteEingefahren` prüft nur `aria-expanded`. Nach dem
   [Glossar](../../domaene/glossar.md) zeigt eine nicht *eingefahrene* *Leiste* auch ihren
   Inhalt; eine Seite, die das Attribut setzt, die *Armeeliste* aber verbirgt, bestünde den
   Test. Nach dem Start hat das *Protokoll* keinen Inhalt, die *Armeelisten* schon.
2. „ausgefahren“ (`…EinerAusgefahrenenLeisteFährtSieEin`, `…FährtSieAus`,
   `…FährtDieLeisteAusWieEinKlick`) steht nicht im Glossar; QUE-6.3 und 6.4 sagen „nicht
   *eingefahren*“ ([Wir 2](../../prozess/praemissen/wir.md)).

**Kosten.** Am Bildschirm nichts. Zu 1 eine Prüfung je *Armeeliste*, zu 2 drei Namen.

**Gegenvorschlag.**
1. In QUE-6.2 für „Armeeliste Spieler 1“ und „Spieler 2“ zusätzlich
   `expect(inhaltVon(seite, leistenname)).to_be_visible()` (Inhalt wie in `inhaltJeLeiste`).
2. Etwa `testQue6_3EinKlickAufDenGriffEinerNichtEingefahrenenLeisteFährtSieEin`,
   `testQue6_4EinKlickAufDenGriffEinerEingefahrenenLeisteFährtSieNichtMehrEin`,
   `testQue6_5EinTippenAufDenGriffEinerEingefahrenenLeisteWirktWieEinKlick`.

**Stellungnahme.**
