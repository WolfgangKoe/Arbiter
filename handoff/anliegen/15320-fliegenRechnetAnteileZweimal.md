# Fliegen rechnet zwei Anteile zweimal, Server nennt das Gerät zweimal

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: offen
Wartet auf: Technikphase 11

## Runde 1
**Befund.** DoD über das Inkrement seit Commit „Freigabe Plan 10“, Effizienz und
Vereinfachung ([Es](../../prozess/praemissen/es.md)). Nichts hält auf: Tests, SonarLint und
Prüfungen grün, am Bildschirm kein Unterschied. Was schon in
[13661](13661-fliegenNamenUndWiederverwendung.md), [13761](13761-fliegenWeicheEinfacher.md)
und [14261](14261-fliegenUmgebungUndWeiteGehoerenZuFliegen.md) steht, steht hier nicht.
1. [fliegen.py](../../technik/arbiter/domaene/phasen/bewegung/fliegen.py), `Fliegen.gezeigt`
   (Zeile 405 bis 407): `self._bewegungsweite(ebene, weg)` und `self._spielfeldkante(ebene, weg)`
   laufen, dann ruft `_anteile` beide mit denselben Werten noch einmal. Jeder Anteil sucht
   Schritt für Schritt über alle *Modelle*; das geschieht bei jeder Zeigerbewegung einer
   gezogenen Canoptek-Spinne doppelt.
2. [server.py](../../technik/arbiter/web/server.py) Zeile 12: `_wurzel = "http://127.0.0.1"`
   wiederholt `_gerät` aus Zeile 11; ändert jemand das Gerät, nennt `adresseMitPort` das alte.

**Kosten.** Ein paar Zeilen, Verhalten unverändert (Akzeptanztests grün). Ohne die Änderung
bleibt die doppelte Rechnung im heißen Pfad des Ziehens und eine Adresse an zwei Stellen.

**Gegenvorschlag.** 1: `_anteile` nimmt die beiden schon gerechneten Anteile entgegen oder
`gezeigt` baut `Anteile` direkt aus ihnen. 2: `adresseMitPort` wieder aus `_gerät` bauen;
verlangt eine Prüfung die feste Zeichenkette, steht ihr Regelcode als Werkzeugkommentar.

**Stellungnahme.**
