# Nachbau in messen, Distanz ohne Namen im Code

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: offen
Wartet auf: Technikphase 9

## Runde 1
**Befund.** Wartet (Ich 3: Namen und Ablage von Hilfsfunktionen, keine Prüfung rot; DoD über
das Inkrement seit „Freigabe Plan 8“).
1. Wiederverwendung: `streckeÜberdeckt` ([messen.py:135](../../technik/arbiter/domaene/messen.py))
   rechnet den Anteil des nächsten Punkts auf der Strecke ein zweites Mal, wie
   `_ersterÜberdeckenderSchritt` (messen.py:110). `anDerBewegungsweiteAngehalten`
   ([anhaltenAnDerBewegungsweite.py:171](../../technik/arbiter/domaene/phasen/bewegung/anhaltenAnDerBewegungsweite.py))
   baut die Suche des ersten Schritts auf dem Raster von S3 (`bisect_left` über `range`) nach,
   die messen.py:119 schon hat.
2. Glossar → Code ([Wir 2](../../prozess/praemissen/wir.md)): BEW-3.1 prüft die *Distanz*;
   im Code heißt sie `abstandImQuadrat(anfang[gezogenes], stelle)`
   (anhaltenAnDerBewegungsweite.py:165), „distanz“ steht nirgends in `technik/arbiter`.
3. Vereinfachung: `stelleDesZugs` ([bedienung.js:30](../../technik/frontend/bedienung.js))
   rechnet `punktAufDerKarte` zweimal je Zeigerbewegung, einmal in `stelleAufDerKarte`.

**Kosten.** Heute keine am Bildschirm. Bleibt es, ändert eine Korrektur am Raster (S3) oder an
der Projektion zwei Stellen, und wer BEW-3 im Code sucht, findet den Begriff nicht.

**Gegenvorschlag.** In Technikphase 9: in messen.py eine Funktion für den Anteil des nächsten
Punkts und eine für den ersten Schritt auf dem Raster, die beide Nutzer aufrufen; in
anhaltenAnDerBewegungsweite.py eine Funktion `distanz…` (Name nach Glossar), die den Vergleich
trägt; in `stelleDesZugs` den Punkt einmal berechnen. Erledigt: Akzeptanztests grün,
`grep -rni distanz technik/arbiter` findet die Funktion, `bisect_left` steht nur in messen.py.

**Stellungnahme.**
