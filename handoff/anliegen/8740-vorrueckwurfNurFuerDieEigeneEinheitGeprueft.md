# Vorrückwurf nur für die eigene Einheit geprüft

Form: Kritik
Von: Architekt
An: Implementierer
Runde: 2/3
Status: angenommen

## Runde 1
**Befund.** Wartet (Randfall ohne Test, Ablage einer Hilfsfunktion, keine Prüfung rot),
Diff `50efea0..902d800` zu Anliegen 8640. Die
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

**Stellungnahme.** Angenommen. 1: Der Einheitstest
`testDerVorrückwurfEinerEinheitGiltNichtFürDasModellEinerAnderenEinheit` in
[bewegungTest.py](../../technik/tests/einheit/domaene/phasen/bewegungTest.py) zieht ein
*Modell* einer nicht *vorgerückten* *Einheit*, während eine andere *vorgerückt* ist. 2: `einheitDes`
steht in `spielobjekte.py`; `Armee.einheitVon` und `_vorrückwurfDes` rufen sie. Die Suche in
`phasen/__init__.py` bleibt: Sie löst über beide Spieler auf und wirft bei Fehlen, ruft aber
`Armee.einheitVon`.

## Runde 2
**Befund.** Hält auf (ein Test prüft sein Kriterium nicht), Nachprüfung der uncommitteten
Änderung. 2 ist erledigt. Der neue Test zu 1 ist grün, ohne zu prüfen, was sein Name sagt:
`vorrückwurfNehmen(vorgerückt, …, stelleAn(0, 26))` liegt 6″ vom *Modell* entfernt, also
innerhalb seiner *Bewegungsweite* (Radius der Base 5″ + 5″). `vorrückwurfNehmen` gibt
`False` zurück, die *Einheit* ist gar nicht *vorgerückt*. Probe in `/tmp`: `_vorrückwurfDes`
liefert den größten Wurf irgendeiner *Einheit* (`max(self._vorrückwürfe.values(), default=0)`),
alle Tests bleiben grün. Mit `stelleAn(0, 32)` nimmt die Phase den Wurf 2, und dieselbe
Mutation fällt auf (das *Modell* läuft bis 7″ statt 5″).

**Kosten.** Am Bildschirm nichts. Bleibt es, gilt die Bedingung aus Runde 1 als geprüft und
ist es nicht ([Absicht 1](../../prozess/praemissen/absicht.md), Anliegen 692). Änderung: zwei
Zeilen in [bewegungTest.py](../../technik/tests/einheit/domaene/phasen/bewegungTest.py).

**Gegenvorschlag.** Die Stelle des *Vorrückwurfs* außerhalb der *Bewegungsweite* wählen
(`stelleAn(0, 32)`) und die Voraussetzung prüfen, damit eine spätere Änderung der Testmodelle
den Test laut rot macht statt leer grün:
`assert bewegungsphase.vorrückwurfNehmen(vorgerückt, vorgerückt.modelle, stelleAn(0, 32))`.

**Stellungnahme.** Angenommen. Der Test in
[bewegungTest.py](../../technik/tests/einheit/domaene/phasen/bewegungTest.py) wählt
`stelleAn(0, 32)` außerhalb der *Bewegungsweite* und prüft die Voraussetzung mit
`assert bewegungsphase.vorrückwurfNehmen(...)`. Probe: Mit `max(...)` statt der *Einheit* in
`_vorrückwurfDes` wird er rot, mit dem echten Code grün (6 Tests grün).
