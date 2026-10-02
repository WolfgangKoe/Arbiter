# Etappe 1: Ausgangslage nur mit runden Bases und ohne FLY

01 · Kritik · von Architekt (Technik) → Planer · Runde 1/3 · angenommen

## Runde 1
**Befund.** Etappe 1 nennt „Einheiten mit Werten aus dem Katalog“, ohne die Art der Einheiten
einzugrenzen. Die 14 Einheiten in `ArbiterMap/data/poc/units/` haben drei Baseformen und zwei
Bewegungsarten, und jede ändert die Regel, nicht nur die Rechnung:
- Ovale Base (Bike Squad) und Hull (Trukk): Drehen zählt zur Bewegung (`core_rules.txt:729`).
- FLY (Deffkoptas, Scarab Swarms, Wraiths) darf über Modelle ziehen (`core_rules.txt:889-890`).
- Runde Base: Abstand = Mittelpunktabstand minus beide Radien. Drehen ist bedeutungslos.

**Kosten.** Beispiel Altbestand: `geometry.py` (54.678 Zeichen) und `base_shape.py` rechnen
Ovale per Bisektion, weil der Randabstand einer Ellipse eine Gleichung vierten Grades ist;
`model_drag.js` hat 85.402 Zeichen. Runde Bases allein brauchen wenige Zeilen Fachlogik und
keine Drehung in der Oberfläche. Ovale, Hulls und FLY würden Etappe 1 grob verdreifachen.

**Gegenvorschlag** (Frage 1).
- Ausgangslage fest, als Datei in `domaene/daten/`, Spielfeld 44″ × 60″
  (`core_rules.txt:2315`). Dieselbe Datei dient den Akzeptanztests als Ausgangsstand.
- Nur Einheiten mit runder Base ohne FLY, je Spieler eine mit sechs oder mehr Modellen
  (Kohärenz mit zwei Nachbarn) und ein Einzelmodell (keine Kohärenz). Beispiel: Boyz
  (10 × 32 mm) und Warboss (40 mm) gegen Necron Warriors (10 × 32 mm) und Overlord (32 mm).
- Nur diese Katalogeinheiten vorziehen; die YAML-Schlüssel werden dabei deutsch
  (`move_inches` → Bezeichner aus dem Glossar).
- Ovale, Hulls und FLY als eigene, spätere Etappe oder Etappe-2-Kriterium.

**Stellungnahme.** Angenommen, umgesetzt: Etappe 1 und 2 nur runde Bases ohne FLY, Etappe 1
fest auf 44″ × 60″; Ovale, Hulls und FLY werden Etappe 3, vor Schießen und Charge, damit deren
Abstände nicht umgebaut werden. Datei: Anforderungsautor, Schreibpfad fehlt (Anliegen 05).
