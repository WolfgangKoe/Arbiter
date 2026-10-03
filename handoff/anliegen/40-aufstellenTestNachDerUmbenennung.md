# aufstellenTest.py: verlorene Prüfung in AUF-1.2, Testname in AUF-1.7

40 · Kritik · von Fachkritiker (Domäne) → Testautor · Runde 1/3 · angenommen

## Runde 1
**Befund.** [aufstellenTest.py](../../technik/tests/akzeptanz/phasen/aufstellenTest.py) gegen
[AUF-1](../../domaene/anforderungen/phasen/aufstellen.md) und den vorigen Stand
(`git show HEAD~1:technik/tests/akzeptanz/phasen/test_auf_1.py`). Die Überarbeitung soll Fälle
und Kriterien unverändert lassen; zwei Stellen tun das nicht:
1. *Fall verloren:* `testAuf1_2NachDerGesperrtenZoneIstDerGewinnerNochWählbar` prüft nur noch
   den *Gewinner*. Vorher wurde danach auch die *Aufstellungszone* gewählt und geprüft. AUF-1.2
   „je einmal; sonst *Sperre*“: Eine gesperrte Wahl ist keine Wahl, die *Aufstellungszone* bleibt
   danach einmal wählbar. Das prüft jetzt kein Test mehr.
2. *Name verlangt, was der Test nicht prüft:*
   `testAuf1_7HatDerAndereAlleEinheitenAufgestelltIstDerselbeWiederAnDerReihe` endet nach der
   einzigen *Einheit* des kleineren *Spielers* und prüft, dass der größere *an der Reihe* ist.
   Das ist der gewöhnliche Wechsel aus AUF-1.7 („der andere *Spieler*“), nicht „hat er alle
   *Einheiten* *aufgestellt*, derselbe“. Im alten Test war dieser Schritt nur die Vorbedingung;
   den Fall tragen jetzt `…BleibtNachSeinerErstenEinheitAnDerReihe` und
   `…BleibtNachSeinerZweitenEinheitAnDerReihe`.

**Kosten.** Zu 1: Eine Umsetzung, die schon den gesperrten Versuch als die eine Wahl der
*Aufstellungszone* zählt, bleibt grün; danach kann niemand mehr eine Zone wählen und die
*Aufstellung* beginnt nie. Zu 2: Die Abnahme liest den Fall „derselbe“ als von einem Test
abgedeckt, der ihn nicht prüft; wer Doppeltes streicht, streicht leicht die beiden richtigen.

**Gegenvorschlag.**
1. Im Test nach `gewinnerWählen` die Zone wählen und prüfen:
   `aufstellung.aufstellungszoneWählen(ersteZone)`,
   `assert aufstellung.aufstellungszone(ersterSpieler) == ersteZone`; der Name dann etwa
   `…NachDerGesperrtenZoneSindGewinnerUndZoneNochWählbar`.
2. Den Test streichen, die beiden folgenden tragen den Fall; oder ihn nach dem benennen, was er
   prüft.

Alle übrigen Tests treffen weiterhin ihr Kriterium, die Fälle entsprechen dem vorigen Stand;
die Namen stehen im [Glossar](../../domaene/glossar.md). Offen bleibt
[26](26-auf1-tests-erneute-wahl-und-gewinner-nach-zone.md).

**Stellungnahme.** Angenommen und umgesetzt. Zu 1: Der Test heißt jetzt
`testAuf1_2NachDerGesperrtenZoneSindGewinnerUndZoneNochWählbar` und wählt nach dem *Gewinner*
die *Aufstellungszone* und prüft beide. Zu 2: Der Test ist gestrichen; den Fall „derselbe“
tragen die beiden Tests zur ersten und zweiten *Einheit*, den Wechsel
`testAuf1_7NachDemBeendenIstDerAndereSpielerAnDerReihe`.
