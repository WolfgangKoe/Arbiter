# Kritik am Code zu Item einheitVerschieben: Loslassen ohne Stelle, Weg fünfmal addiert

1450 · Kritik · von Reviewer → Implementierer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Lesbarkeit ([Es](../../prozess/praemissen/es.md)) und Korrektheit der Umsetzung
von [1410](1410-kritikAmCodeEinheitVerschieben.md): `rückungInDieFläche` in
[messen.py](../../technik/arbiter/domaene/messen.py), früher Rückweg in
`Aufstellung._verschobeneStellen`, `Gesperrtes.vorher` als `MappingProxyType`. Die drei Punkte
sind richtig umgesetzt, das Verhalten bleibt. Nichts hält auf ([Ich 3](../../prozess/praemissen/ich.md):
Randfall, Ablage von Hilfen, keine Prüfung rot). Geprüft: `ruff` grün, Unit- und
Akzeptanztests 679 grün; `prozess/pruefungen` rot nur Glossar, Benennung und toter Code in
`messen.py` aus der laufenden Arbeit an anhaltenAnBases.
1. `_verschobeneStellen` ([aufstellen/\_\_init\_\_.py](../../technik/arbiter/domaene/phasen/aufstellen/__init__.py)):
   Die Bedingung `or not self.gesetzt(modell)` prüft kein Test mehr, seit
   `testEinGezogenesOhneStelleDavorBewegtDieGruppeNicht` entfiel. Probe: ohne sie bleiben alle
   679 Tests grün. Der Fall ist erreichbar: `PUT …/modelle/<n>` mit einem nicht *gesetzten*
   *Modell* einer *ausgewählten* *Einheit*, deren *Ebene* die ganze *Einheit* ist; ohne die
   Bedingung antwortet `web/` 500 (`KeyError` in `verschobeneStellen`). Der `# Regel:` darüber
   nennt AUF-21.1 und 20.4, beide gelten nur für ein *gesetztes* *Modell* (AUF-8.2); für das
   Loslassen eines nicht *gesetzten* gibt es kein Kriterium.
2. Eine *Stelle* um einen Weg verschieben steht fünfmal: `verschobeneStellen`, `hineingerückt`,
   `stellenDerFormation`, `_Annäherung.überdecktAm` (messen.py) und
   [anhaltenAnEinerBase.py](../../technik/arbiter/domaene/phasen/aufstellen/anhaltenAnEinerBase.py).
   `messen.py` hat jetzt den Typ `Weg`, `rückungInDieFläche` liefert trotzdem
   `tuple[Fraction, Fraction]`.
3. Der Docstring von `rückungInDieFläche` verspricht, danach liege jede *Base* *ganz in* der
   Fläche. Ist der Block breiter als die Fläche, rückt sie nur an die untere Kante, die obere
   steht weiter über; die *Sperre* kommt dann aus `gründeGegenDieStelle`.

**Kosten.** Zu 1: Ein Rückfall wird erst als 500 im Dienst sichtbar. Zu 2: Ändert sich die
Darstellung des Wegs (etwa für ein Raster nach S3), sind fünf Stellen zu ändern. Zu 3: Wer
der Messung glaubt, verlässt sich auf „ganz in“ und prüft nicht nach.

**Gegenvorschlag.**
1. Nach deinem Urteil: ein Unit-Test für das Loslassen eines nicht *gesetzten* *Modells* bei
   *Ebene* *Einheit* (die übrigen stehen wie davor), oder `modellLoslassen` verlangt ein
   *gesetztes* *Modell* wie `ebeneWählen` (`_prüfenDassGesetzt`), dann entfällt die Bedingung.
   Soll das Loslassen eines nicht *gesetzten* *Modells* fachlich etwas tun: Frage an den
   Anforderungsautor.
2. Eine Funktion `verschoben(stelle: Stelle, weg: Weg) -> Stelle` in `messen.py`; alle fünf
   rufen sie (ein Anteil skaliert den Weg vorher), `rückungInDieFläche` liefert `Weg`.
3. Docstring: „… soweit die Bases zusammen hineinpassen“, mit einem Unit-Test für den zu
   breiten Block in [messenTest.py](../../technik/tests/einheit/domaene/messenTest.py).

Erledigt: umgesetzt oder begründet abgelehnt, Tests grün, Verhalten unverändert.

**Stellungnahme.**
Alle drei Punkte umgesetzt, Tests grün.
1. Die zweite Möglichkeit geht nicht: `modellLoslassen` eines nicht *gesetzten* *Modells* ist das
   erste Setzen, es muss gehen. Stattdessen liegt der Fall in `verschobeneStellen`
   ([einheitVerschieben.py](../../technik/arbiter/domaene/phasen/aufstellen/einheitVerschieben.py)):
   ein *Modell* ohne *Stelle* in der Gruppe ergibt `{gezogenes: ziel}`, die Bedingung in
   `_verschobeneStellen` entfällt; Unit-Test `testEinNochNichtGesetztesModellBewegtDieGruppeNicht`.
2. `verschoben(stelle, weg)` und `teilDesWegs(weg, anteil)` in
   [messen.py](../../technik/arbiter/domaene/messen.py); `verschobeneStellen`, `hineingerückt`,
   `stellenDerFormation`, `_überdecktAm` und `angehalten` rufen sie. `rückungInDieFläche` lieferte
   schon `Weg`.
3. Docstring auf „soweit die Bases zusammen hineinpassen“; Unit-Test
   `testEinZuBreiterBlockRücktNurAnDieUntereKante`.
