# Hilfen der Tests zum Übergehen

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Kritik an den Tests zu Item gemeinsamUebergehen. Wartet nach
[Kritik](../../prozess/ablauf/kritik.md) (Hilfsfunktionen, Randfall, keine Prüfung rot):

1. `warbossÜberDieBoyzÜbergehen` in [schlacht.py](../../technik/tests/akzeptanz/schlacht.py)
   gelingt nur nach `boyÜberDenWarbossÜbergehen`: Der Warboss steht östlich der Boyz, 5″
   nach Osten liegt erst dann eine *Base* im Weg, wenn ein Boy über ihn gezogen ist; allein
   scheitert die Hilfe an `pytest.raises`. Der Name verschweigt das, ebenso das gleiche
   Ziehen in `testQue5_1JedesÜbergehenTrägtGenauEinenEintragMehrEinUndBehältDieÄlteren` und
   `testQue5_4DerDienstNenntDenNeuerenEintragZuerstWieImBeispiel`.
2. Doppelt ([Wir 3](../../prozess/praemissen/wir.md)): Der Aufbau „Einheit ohne
   *Kohärenz* in der *Aufstellung*“ steht dreimal in
   [uebergehenTest.py](../../technik/tests/akzeptanz/querschnitt/uebergehenTest.py);
   `aufDieBoyz` steht in beiden Testdateien; `zugÜberEineBase` in
   [conftest.py](../../technik/tests/akzeptanz/conftest.py) wiederholt
   `schlachtInDerBewegungsphaseDesZweitenSpielers`. In
   `testQue5_1DerDienstNenntDenEintragImSpielstand` rechnet ein `if` die Spielernummer, und
   `"einheit": 1`, `"über eine Base"` stehen als Wert statt aus der Aufstellung und
   `Grund.überEineBase.value` wie in den anderen Tests.
3. Randfall: Mit `übergehen`, aber ohne *Sperre*, setzt `modellLoslassen` ohne Eintrag; der
   Eintrag nennt die *Gründe* der *Sperre*. Das habe ich in
   [V18](../../technik/architektur/vertrag/schlacht/uebergehen.md) nachgetragen (QUE-5.1:
   „bei einer *Sperre*“); kein Test prüft es.
4. Zur Kenntnis: Die Prüfung des Frontends mit `page.route` und dem Beispiel
   ([Querschnitt](../../technik/architektur/vertrag/querschnitt.md), Absatz „Prüft“) hat
   kein Test der *Schlacht*, auch hier nicht. Ob die Forderung neben Dienst- und
   Bildschirmtest bleibt, entscheide ich in der Technikphase 10; bis dahin nichts zu tun.

**Kosten.** Am Bildschirm nichts. 1 kostet beim nächsten Test, der die Hilfe allein nutzt,
eine Fehlersuche; 2 drei Stellen je Änderung; 3 ein ungeprüfter Zweig im Produktcode.

**Gegenvorschlag.**
1. Eine Hilfe `beideÜbereinanderÜbergehen(schlacht, boyz, warboss)` statt zweier, oder
   `warbossÜberDenGezogenenBoyÜbergehen`.
2. Fixture `einheitOhneKohärenzInDerAufstellung`; `aufDieBoyz` nach `schlacht.py` neben
   `fünfZollNachOsten`; `zugÜberEineBase` trägt die Spielernummer und baut auf den Fixtures
   der Bewegungsphase auf.
3. Ein Test zu QUE-5.1: Loslassen ohne *Sperre* mit `übergehen={Grund.überEineBase}`,
   danach `list(schlacht.protokoll) == []`.

**Stellungnahme.**
1. Angenommen, umgesetzt: Die beiden Hilfen sind fort; `warbossUndDanachEinenBoyÜbergehen` in
   `schlacht.py` nennt die Reihenfolge, `anhaltenUndÜbergehen` prüft das Angebot vor dem Übergehen.
2. Angenommen, umgesetzt: `zugÜberEineBase` und `aufDieBoyz` sind fort; die Fixture
   `zugÜberDieBewegungsweite` baut auf `schlacht` auf, der Dienst-Test liest Kennungen aus
   `kennungenDerEinheiten` ohne `if`. Der dreifache Aufbau ohne *Kohärenz* steht nur noch zweimal
   (Dienst und Seite der *Aufstellung*), die Prüfung in der Domäne entfiel mit `übergehbar`.
3. Durch V18 umgekehrt: Loslassen trägt nie ein; Tests `testQue5_6…`.
4. Durch V18 entschieden; Tests mit `page.route` und `angehalten.json`/`protokoll.json`.
