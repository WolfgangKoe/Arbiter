# Akzeptanztests in der Folge der Kriterien, Ausgangslage aus der Missionsvorbereitung

368 · Kritik · von Architekt (Technik) → Testautor (Technik) · Runde 1/3 · offen

## Runde 1
**Befund.** Kritik am Code von 986d3fb (Schnittstelle, Lesbarkeit). Der neue Schnitt ist gut:
Ort, Docstring und Kennungen spiegeln die Anforderungen. Zwei Stellen passen nicht zur
[Architektur](../../technik/architektur.md), die jetzt den Spiegel festhält (Anliegen 345, 365):
1. T1 (3): Die Tests stehen nicht in der Folge der Kriterien. `querschnitt/karteTest.py`:
   QUE-2.7 vor QUE-2.5 (die frühere 2.4); `phasen/aufstellen/sperrenBeimSetzenTest.py`: 3.8 vor
   3.7; `querschnitt/bedienungTest.py`: ein Test zu QUE-3.2 nach QUE-3.3;
   `phasen/aufstellen/auswahlTest.py`: zwei Durchgänge 5.3 bis 5.10, erst Bildschirm, dann
   Dienst. Wer AUF-5.7 liest, findet seine Tests an zwei Stellen der Datei.
2. Grundschnitt: `Ausgangslage` und `Aufstellungszone` gehören zu MIV-1, also nach
   `arbiter.domaene.missionsvorbereitung.ausgangslage`. Die Tests importieren sie aus
   `arbiter.domaene.phasen.aufstellen`.

**Kosten.** 1: Funktionen verschieben, Verhalten unverändert; ohne das bleibt die Prüfung aus
[367](367-spiegelpruefungInhaltUndDomaene.md), Teil 3, am Repo rot. 2: die Importzeilen;
danach sind die Tests rot, bis der Implementierer die zwei Klassen verschiebt (Test vor dem
Code). Ohne 2 bleibt eine Regel der Missionsvorbereitung im Modul der Aufstellung, und
`missionsvorbereitung/ausgangslageTest.py` spiegelt keinen Code.

**Gegenvorschlag.**
1. Je Datei die Tests eines Kriteriums beisammen, die Kriterien in der Folge der Anforderung;
   innerhalb eines Kriteriums frei, etwa erst Dienst, dann Bildschirm.
2. `from arbiter.domaene.missionsvorbereitung.ausgangslage import Ausgangslage,
   Aufstellungszone` in allen Akzeptanztests und Hilfsmodulen; der Implementierer zieht nach.

Erledigt, wenn `python3 -m pytest technik/tests` nur an diesem Import rot ist und Teil 3 aus
367 am Repo grün wäre. Beides in der Technikphase von Plan 5, mit den neuen Tests.

**Stellungnahme.**
