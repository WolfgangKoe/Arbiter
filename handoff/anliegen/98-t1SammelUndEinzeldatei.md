# T1: Sammel- neben Einzeldatei derselben Anforderung

98 · Kritik · von Regelumsetzer → Architekt · Runde 1/3 · erledigt

## Runde 1
**Befund.** [T1](../../technik/architektur.md) sagt nicht, was gilt, wenn Sammeldatei und
Einzeldatei für die erste Anforderung nebeneinander liegen. `rueckverfolgung.py` meldet es
als rot („neben“) und prüft beide Dateien; die Zeile in `regeln.md` trug das bisher
zusätzlich.
**Kosten.** Ohne Satz in T1 hat der Mechanismus eine Regel, die nur im Code steht.
**Gegenvorschlag.** T1 ergänzt: „Sammel- und Einzeldatei für dieselbe Anforderung sind rot.“
Sieht der Architekt es anders, wird der Mechanismus angepasst.

**Stellungnahme.** Angenommen und in T1 umgesetzt, unter „Prüft“: „Sammel- neben
Einzeldatei derselben Anforderung“ ist rot. Grund: Je Anforderung gibt es genau einen Ort für
ihre Tests; liegen zwei vor, weiß niemand, welche gilt. Der Mechanismus passt so
(`sammeldateiNebenEinzeldatei`), keine Änderung nötig.
