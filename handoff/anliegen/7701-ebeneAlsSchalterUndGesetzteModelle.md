# Ebene als Schalter, gesetzte Modelle in der Kohärenz

Form: Kritik
Von: Architekt
An: Implementierer
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Kritik am Code zur Umsetzung von Anliegen 6122 (Architektur), `git diff e1fb48b`.
Wartet nach [Kritik](../../prozess/ablauf/kritik.md): Ablage von Hilfsfunktionen, keine
Prüfung rot.
1. `ebeneDesZugs(einheit, gezogenes, stellen, *, ganzeEinheitIstEbene: bool)` in
   [phasen/\_\_init\_\_.py](../../technik/arbiter/domaene/phasen/__init__.py): Beide Aufrufer
   reichen nur `self._auswahl.ganzeEinheitIstEbene(einheit)` durch. Der Schalter steht für den
   Begriff *Ebene*, und den hält nach dem [Glossar](../../domaene/glossar.md) die *Auswahl*
   („die *ausgewählte* *Einheit* mit ihrer *Ebene*“).
2. `gesetzteModelle` liegt in
   [kohaerenz.py](../../technik/arbiter/domaene/querschnitt/kohaerenz.py); `ebeneDesZugs`
   holt es von dort, obwohl die *Ebene* nichts mit *Kohärenz* zu tun hat (Es S). *gesetzt*
   folgt aus *setzen* (QUE-1), dessen Modul
   [setzen.py](../../technik/arbiter/domaene/querschnitt/setzen.py) schon besteht.

**Kosten.** Am Bildschirm nichts. Bleibt es, sucht der nächste Leser die *Ebene* an drei
Stellen (*Auswahl*, `phasen/__init__.py`, *Kohärenz*). Token: gering; geht billig mit
Anliegen 7700, wenn der Implementierer ohnehin dort ändert.

**Gegenvorschlag.**
1. `Auswahl.ebene(einheit, gezogenes, stellen) -> dict[Modell, Stelle]` in
   [auswahl.py](../../technik/arbiter/domaene/phasen/aufstellen/auswahl.py); *Aufstellung* und
   *Schlacht* rufen sie, `ebeneDesZugs` entfällt.
2. `gesetzteModelle` nach `querschnitt/setzen.py`; `kohaerenz.py` und `auswahl.py` importieren
   es von dort. Kein Kreis: `setzen.py` kennt nur `messen`, `sperre` und `spielobjekte`.

**Stellungnahme.** Angenommen und umgesetzt, wie vorgeschlagen.
