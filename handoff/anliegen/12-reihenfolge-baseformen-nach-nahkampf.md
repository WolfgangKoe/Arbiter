# Reihenfolge: Etappe 4 erst nach Charge und Nahkampf

12 · Kritik · von Architekt (Technik) → Planer · Runde 1/3 · offen

## Runde 1
**Befund.** [Etappe 4](../../domaene/etappen/04-jede-baseform.md) steht vor dem Schießen,
„bevor Schießen und Charge messen“. Sie ist die teuerste Etappe, die einzige mit
geometrischem Neuland, und bündelt zwei unabhängige Dinge: Baseformen samt FLY und das
Zusammenstellen der Armee aus allen Katalogeinheiten. Sie schiebt das erste Probespiel
(ab Etappe 5) um ihre ganze Dauer nach hinten.

**Kosten.** Altbestand: `geometry.py` (54.678 Zeichen) und `base_shape.py` rechnen Ovale per
Bisektion, `model_drag.js` (85.402) dreht Modelle. Der Grund „bevor … messen“ trägt nur, wenn
Schießen und Charge die Baseform selbst kennen. Das verhindert eine Regel, die ich in
`technik/architektur.md` mit einem Vertragstest je Baseform festschreibe: Phasen messen nur
über „Abstand zweier Modelle“ und „Base vollständig in Fläche“. Positives Beispiel:
`rule_checks.py` prüft Kohärenz und Engagement Range allein über `is_within_contours`, ohne
die Form zu kennen. Dann fügt Etappe 4 Formen hinzu, ohne Schießen oder Charge zu ändern.
Preis der Umstellung: Die Akzeptanztests von 5 und 6 laufen zuerst nur mit runden Bases,
Etappe 4 ergänzt Fälle; Drehen trifft nur Bewegen, Pile In und Consolidate.

**Gegenvorschlag.**
1. Reihenfolge 1, 2, 3, 5, 6, 4, 7: das Probespiel mit der festen Ausgangslage früher, das
   Neuland danach.
2. Etappe 4 teilen: Baseformen und FLY bleiben, „Armee aus allen Katalogeinheiten
   zusammenstellen“ geht zu Etappe 7.
Braucht der Stakeholder die Formen vor dem ersten Probespiel (etwa weil seine Armeen Bikes und
Trukks haben), bleibt die Reihenfolge; dann gilt nur 2.

**Stellungnahme.**
