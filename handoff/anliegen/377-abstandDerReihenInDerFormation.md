# Abstand der Reihen in der Formation

377 · Fragen · von Architekt (Technik) → Anforderungsautor (Domäne) · Runde 1/3 · erledigt

## Runde 1
**Befund.** Drei Quellen beschreiben die *Formation* (AUF-8.5) verschieden:
1. [Glossar](../../domaene/glossar.md), *Formation*: „je zwei benachbarte *Bases* im *Abstand*
   1,5″“, wie die Skizze des Stakeholders
   (`Arbiter-old/Arbiter_Specs/Arbiter - unitshape and modeldistribution.pdf`, Seite 1): Auch
   die schräg benachbarten *Bases* zweier Reihen haben dort Pfeile mit 1,5″.
2. Die Mockups ([auf-8](../../domaene/mockups/auf-8.html), auf-9, auf-15) setzen die Reihen
   2,76″ auseinander (*Durchmesser* 32 mm plus 1,5″); schräg benachbarte Boyz haben dort den
   *Abstand* 1,83″, die *Formation* ist 6,78″ statt 6,04″ breit.
3. Nach der Skizze ist der Abstand der Reihen (*Durchmesser* + 1,5″) · √3 / 2, keine Bruchzahl.
   Arbiter rechnet aber exakt mit Bruchzahlen ohne Wurzel
   ([Architektur, S2](../../technik/architektur.md#stelle-und-rechnen)); an genau diesen
   Grenzen entscheiden *überdecken*, *Kohärenz* und *ganz in*.

**Kosten.** Ohne Entscheidung prüft der Test zu AUF-8.5 eine Lage, die das Mockup nicht zeigt,
oder umgekehrt; die Skizze lässt sich nicht exakt rechnen.

**Gegenvorschlag.**

**F1 · Abstand der Reihen.** A: wie die Skizze; der Abstand der Reihen wird auf 1/100″
aufgerundet, schräg benachbarte *Bases* haben dann mindestens 1,5″ und höchstens 1,51″ (bei
32 mm). Glossar und Mockups (UX) ändern sich. B: wie die Mockups; die Reihen haben
untereinander 1,5″, schräg benachbarte *Bases* mehr. Nur das Glossar ändert sich.
Empfehlung A: Die Skizze ist die Quelle des Stakeholders, der Unterschied ist am Tisch
unsichtbar, und die *Kohärenz* (höchstens 2″) hält in beiden Fällen. Kosten in der Technik:
eine Rechnung mit ganzzahliger Wurzel, aufgerundet, und eine Zeile in S2.

Antwort: A

**Stellungnahme.** A. Die Skizze des Stakeholders entscheidet das: Auch schräg benachbarte
*Bases* haben dort 1,5″. Das steht jetzt ausdrücklich im [Glossar](../../domaene/glossar.md)
(*Formation*) und in [formation.yaml](../../domaene/daten/formation.yaml). Die Aufrundung auf
1/100″ trägt das Ziel („Die Karte bildet den Spielstand ab, nicht den exakten Tisch“). Wie fein
gerundet wird, gehört in deine S2, nicht in die Kriterien. Die Mockups bringt UX in Ordnung:
[381](381-reihenabstandInDenMockups.md).
