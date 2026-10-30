# Gegner und Klick auf ein Modell je einmal

Form: Kritik
Von: Architekt
An: Implementierer
Runde: 1/3
Status: offen
Wartet auf: Technikphase 10

## Runde 1
**Befund.** Wartet (Kritik: Namen und Ablage von Hilfsfunktionen, keine Prüfung rot), Diff
`90801c5..819896b`. Die Architektur hält: Importvertrag, Benennung, Spiegel grün, keine
Regel mehr in `web/` oder der Seite (8030, 7023 erledigt).
1. Ablage von `gegnerVon` (offen aus 5701): Die
   [Schlacht](../../technik/arbiter/domaene/querschnitt/schlachtrunden.py) holt den Gegner aus
   [reihenfolge.py](../../technik/arbiter/domaene/phasen/aufstellen/reihenfolge.py), einer
   Anforderung der *Aufstellung*. Der Gegner gilt in jeder *Phase*; nach dem
   [Grundschnitt](../../technik/architektur/domaene.md#grundschnitt-der-domäne) liegt, was
   mehrere brauchen, im Ordnermodul, hier neben `einheitVon` in
   [phasen/\_\_init\_\_.py](../../technik/arbiter/domaene/phasen/__init__.py), das dieselben
   `beideSpieler` nimmt.
2. Schnittstelle von `Auswahl`
   ([auswahl.py](../../technik/arbiter/domaene/phasen/aufstellen/auswahl.py)): `ebeneWählen`
   und `ebeneAbwählen` ruft im Produkt nur noch `modellAnklicken` derselben Klasse; öffentlich
   halten sie nur die Unit-Tests in `auswahlTest.py` (Es, I). Der `ValueError` aus
   `_prüfenDassZurAusgewähltenEinheit` ist über `modellAnklicken` nicht mehr erreichbar.
3. Dieselbe Regel zweimal (Wir 3): `Aufstellung.modellAnklicken` und `Schlacht.modellAnklicken`
   tun wörtlich dasselbe (nur ein *gesetztes* *Modell*, `einheitVon`, dann
   `Auswahl.modellAnklicken`).

**Kosten.** Keine am Bildschirm. Bleibt 1, sucht ein Leser den Gegner der *Schlacht* in der
*Aufstellung*; bleibt 2, testen die Unit-Tests einen Weg, den das Produkt nicht geht; bleibt 3,
läuft eine Änderung an V14 (etwa eine Sperre fürs Auswählen) leicht nur in einer *Phase* ein.
Je Punkt wenige Zeilen.

**Gegenvorschlag.**
1. `gegnerVon` nach `phasen/__init__.py`, `reihenfolge.py` und `schlachtrunden.py`
   importieren es dort.
2. `ebeneWählen`, `ebeneAbwählen` und die Prüfung privat oder in `modellAnklicken` aufgehen
   lassen; die Unit-Tests gehen über `modellAnklicken`.
3. Eine Funktion neben `einheitVon`, die beide Türen rufen, etwa
   `modellAnklicken(auswahl, beideSpieler, modell, gesetzt)`; passt sie nicht sauber, genügt
   es, 3 zu verwerfen.

**Stellungnahme.**
