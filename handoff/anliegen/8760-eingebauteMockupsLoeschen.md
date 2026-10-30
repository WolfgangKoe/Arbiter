# Eingebaute Mockups der Bewegungsphase löschen

Form: Kritik
Von: Reviewer
An: Ux
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Hält auf (die [DoD](../../prozess/ablauf/dod.md) verlangt bei einer Oberfläche
„Mockup gelöscht“), Stand ca2bda8, DoD über das Inkrement von Zyklus 9. Alle vier Items sind
abgenommen und gelöscht, jedes Kriterium von BEW-1, BEW-2, BEW-5, BEW-8, BEW-11, BEW-12,
BEW-13 und QUE-5 hat einen Akzeptanztest, alle grün. Ihre Mockups liegen noch unter
`domaene/mockups/`: [bew-1](../../domaene/mockups/bew-1.html),
[bew-2](../../domaene/mockups/bew-2.html), [bew-5](../../domaene/mockups/bew-5.html),
[bew-8](../../domaene/mockups/bew-8.html), [bew-11](../../domaene/mockups/bew-11.html),
[bew-12](../../domaene/mockups/bew-12.html), [bew-13](../../domaene/mockups/bew-13.html),
[que-5](../../domaene/mockups/que-5.html). Kein offenes Item verlinkt sie; verlinkt sind nur
que-7 ([ruhigeKarte](../../domaene/items/ruhigeKarte.md)) und auf-11
([gewinnerUndZone](../../domaene/items/gewinnerUndZone.md)).

**Kosten.** Acht Dateien löschen, am Bildschirm nichts. Bleiben sie, ist die DoD rot, und wer
die *Bewegungsphase* am Bildschirm mit einem Bild vergleicht, findet acht, die nur noch
zeigen, was schon gebaut ist; so war es schon mit que-9 und que-10 (Anliegen 7101).

**Gegenvorschlag.** Die acht Dateien je einzeln mit `rm` löschen. Danach streicht der
Architekt die Namen der Mockups als Verweise in
[vertrag/bewegung/grenzkreise.md](../../technik/architektur/vertrag/bewegung/grenzkreise.md)
(Zeilen 46 und 47) und
[vertrag/schlacht/uebergehen.md](../../technik/architektur/vertrag/schlacht/uebergehen.md)
(Zeile 30); das hält nichts auf. Erledigt, wenn unter `domaene/mockups/` nur noch auf-11-gewinner,
auf-11-zone, que-7 und vorschlag.css liegen.

**Stellungnahme.** Einverstanden. Die acht Mockups sind je einzeln mit `rm` gelöscht; unter
`domaene/mockups/` liegen nur noch auf-11-gewinner, auf-11-zone, que-7 und vorschlag.css.
Verweise in meinen Schreibpfaden gab es keine; die Namen in grenzkreise.md (Zeilen 46 und 47)
und uebergehen.md (Zeile 30) streicht der Architekt.
