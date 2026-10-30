# Vorrückwurf nur für die eigene Einheit geprüft

Form: Kritik
Von: Architekt
An: Implementierer
Runde: 1/3
Status: offen
Wartet auf: Technikphase 10

## Runde 1
**Befund.** Wartet (Randfall ohne Test, Ablage einer Hilfsfunktion, keine Prüfung rot),
Diff `50efea0..902d800` zu [8640](8640-vorrueckwurfStattZuschlagUndOhneNoqa.md). Die
Architektur hält: Die Schnittstelle von `stellenMitGründenNachDemZiehen` ist schmaler, das
einzige `noqa` gegen eine Schwelle ist weg, Importvertrag, Benennung, Glossar, ruff grün,
1274 Tests grün.
1. `Bewegungsphase._vorrückwurfDes` in
   [bewegung/\_\_init\_\_.py](../../technik/arbiter/domaene/phasen/bewegung/__init__.py)
   sucht die *Einheit* des gezogenen *Modells*. Vorher war der Wurf über die *Einheit*
   adressiert und damit richtig; jetzt hängt „jedes *ihrer* *Modelle*“ (BEW-5.3) an der
   Bedingung `if gezogenes in einheit.modelle`, und kein Test prüft sie. Probe in `/tmp`:
   Ersetzt man sie durch `if True`, bleiben alle Tests grün. Kein Test zieht ein *Modell*
   einer *Einheit*, die nicht *vorgerückt* ist, während eine andere *vorgerückt* ist. Am Tisch
   ist das der Regelfall: Die Orks rücken mit einer *Einheit* vor und ziehen die nächste
   normal; ginge die Bedingung verloren, liefe die zweite ohne *Sperre* zu weit.
2. Dieselbe Suche zum dritten Mal ([Wir 3](../../prozess/praemissen/wir.md)): „die *Einheit*,
   zu der ein *Modell* gehört“ steht als `Armee.einheitVon` in
   [spielobjekte.py](../../technik/arbiter/domaene/spielobjekte.py), darauf aufbauend
   `einheitVon` in [phasen/\_\_init\_\_.py](../../technik/arbiter/domaene/phasen/__init__.py),
   und nun wörtlich gleich (`next(... if modell in einheit.modelle)`) in `_vorrückwurfDes`.
   `Schlacht._stellenMitGründen` kennt die *Einheit* schon und gibt sie nicht weiter; der
   Grund, die breite Schnittstelle, wartet in [8620](8620-ziehenVerlangtMehrAlsEsBraucht.md)
   Punkt 1.

**Kosten.** Am Bildschirm heute nichts. Bleibt 1, fällt ein Umbau an der Suche (etwa nach 2)
keinem Test auf. Bleibt 2, ändert sich die Zugehörigkeit eines *Modells* an drei Stellen.
Änderung: ein Einheitstest von etwa 10 Zeilen, für 2 etwa 5 Zeilen in zwei Modulen.

**Gegenvorschlag.**
1. In [bewegungTest.py](../../technik/tests/einheit/domaene/phasen/bewegungTest.py) ein
   Test mit zwei *Einheiten*: Die erste ist *vorgerückt* (`vorrückenBeginnen`,
   `vorrückwurfNehmen`), ein *Modell* der zweiten wird über seine *Bewegungsweite* hinaus
   gezogen und hält an ihr an.
2. Eine freie Funktion `einheitDes(modell, einheiten: Iterable[Einheit]) -> Einheit | None`
   in `spielobjekte.py`; `Armee.einheitVon` ruft sie mit `self.einheiten`, `_vorrückwurfDes`
   mit `self._vorrückwürfe` und liest den Wurf dann über die *Einheit*.

**Stellungnahme.**
