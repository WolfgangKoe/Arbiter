# Modell anklicken ohne doppelte Einheit, Meldung ohne Bedienelement

Form: Kritik
Von: Architekt
An: Implementierer
Runde: 1/3
Status: offen
Wartet auf: Technikphase

## Runde 1
**Befund.** Wartet (Kritik: Namen und Ablage von Hilfsfunktionen, keine Prüfung rot),
Kritik am Code des Strangs 8100/8121 (uncommittet). Importvertrag, Spiegel, Benennung und
Kommentare grün.
1. [auswahl.py](../../technik/arbiter/domaene/phasen/aufstellen/auswahl.py):
   `Auswahl.modellAnklicken(einheit, modell)` nimmt zwei Angaben, von denen die eine aus der
   anderen folgt. Seit die Prüfung entfallen ist (8100, 8121), macht ein Aufruf mit einem
   *Modell* einer anderen *Einheit* still ein fremdes *Modell* zur *Ebene*, und
   `ebeneDerAuswahl` reicht es zum Ziehen weiter. Beide Türen halten den Vertrag nur, weil sie
   `einheitVon` rufen, und das in verschiedener Reihenfolge:
   [Aufstellung](../../technik/arbiter/domaene/phasen/aufstellen/__init__.py) erst
   `einheitVon`, dann `gesetzt` (fremdes *Modell*: `ValueError`),
   [Schlacht](../../technik/arbiter/domaene/querschnitt/schlachtrunden.py) umgekehrt
   (fremdes *Modell*: nichts geschieht).
2. [aufstellen/\_\_init\_\_.py](../../technik/arbiter/domaene/phasen/aufstellen/__init__.py)
   `auswählen`: Die Meldung „… wählt man nicht über die Einheitenkarte“ nennt ein
   Bedienelement; Anzeige und Bedienung liegen nach dem
   [Grundschnitt](../../technik/architektur/domaene.md#grundschnitt-der-domäne) in `web/` und
   `frontend/`, und „Einheitenkarte“ steht nicht im Glossar (Wir 2). Der Begriff des
   Kriteriums (AUF-5.11) ist die *Armeeliste*; sie zeigt laut Glossar nur nicht *aufgestellte*
   *Einheiten*.

**Kosten.** Am Bildschirm nichts: `web/` reicht nur *Modelle* der *Armee* und *Einheiten* der
*Armeeliste* durch. Bleibt 1, hält ein Vertrag, den kein Code prüft, und dieselben zwei Zeilen
stehen in zwei Türen; bleibt 2, kennt die Domäne ein Bedienelement. Je Punkt wenige Zeilen.

**Gegenvorschlag.**
1. `auswahl.py` importiert `einheitVon` aus `phasen/__init__.py` (kein Kreis: an einer Kopie in
   `/tmp` geprüft, Schlacht und Auswahl laden; der Kreis aus 8100 entsteht nur in der
   Gegenrichtung). `Auswahl.modellAnklicken(beideSpieler, modell, stellen)` lässt nur ein
   *gesetztes* *Modell* zu, holt die *Einheit* selbst und setzt dann *Auswahl* oder *Ebene*;
   beide Türen rufen nur noch diese Zeile. Die Unit-Tests in `auswahlTest.py` geben
   `beideSpieler` und `stellen` mit.
2. Die Meldung mit dem Begriff des Glossars, etwa „Eine aufgestellte Einheit steht nicht in
   der Armeeliste“.

**Stellungnahme.**
