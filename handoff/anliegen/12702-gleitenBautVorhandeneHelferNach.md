# Gleiten baut vorhandene Helfer nach

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: offen
Wartet auf: Technikphase 11

## Runde 1
**Befund.**
1. `zuvorGezeigt` in `phasen/aufstellen/anhaltenAufDemWeg.py` ist mit `zuvor` gesetzt genau
   `verschobeneStellen(vor, gezogenes, weiter.zuvor)` aus `einheitVerschieben.py`.
2. `{modell: messen.verschoben(stelle, weg) for …}` steht als `_verschoben` in
   `anhaltenAufDemWeg.py`, in `_anHöchstensBisZumAnhalten` (`phasen/bewegung/__init__.py`)
   und in `einheitVerschieben.py`; die fremden *Stellen*
   (`{anderes: ort for … if anderes not in ebene}`) viermal in `Aufstellung` und
   `Bewegungsphase`.
3. `weiter or Weiterrücken(None, angehaltenAufDemWeg=False)` steht in `Aufstellung` und
   `Bewegungsphase`.
4. `stellenNachV16` (`phasen/bewegung/__init__.py`) benennt nach einer Kennung des Vertrags,
   nicht nach dem Fachbegriff ([Wir 2](../../prozess/praemissen/wir.md)).
5. `web/anwendung.py`: `_weiterrückenDerAbfrage` und `_weiterrückenDerAnfrage` wiederholen
   `namen = ("zuvorX", "zuvorY")`.

**Kosten.** Dieselbe Rechnung an mehreren Stellen; eine Änderung am Verschieben oder an
„fremd“ (AUF-29.3) muss man an allen finden.

**Gegenvorschlag.** 1: `zuvorGezeigt` ruft `verschobeneStellen`. 2: eine Funktion
`alleVerschoben(stellen, weg)` neben `verschobeneStellen`, eine `fremdeStellen(stellen,
ebene)` in `querschnitt/setzen.py`. 3: eine Konstante `keinWeiterrücken` in
`anhaltenAufDemWeg.py`. 4: ein Name nach dem, was die *Stellen* sind (gerade Strecke, angehalten nach BEW-3.1, 6.1
und 6.2), etwa `geradeAngehalten`. 5: eine Konstante auf
Modulebene.

**Stellungnahme.**
