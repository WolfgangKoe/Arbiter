# Aufstellen aufteilen: Spielobjekte, Setzen, Bewegen

105 · Fragen · von Anforderungsautor (Domäne) → Stakeholder · Runde 1/3 · offen

## Runde 1
Aus deiner Stellungnahme in [97](97-kritikAmZweckDerAufstellung.md) zu
[aufstellen.md](../../domaene/anforderungen/phasen/aufstellen.md). Das Höchstmaß von 1.200
Zeichen gilt je Anforderung (`domaene/CLAUDE.md`); eigene Dateien machen AUF-1 nicht kürzer.
Die Verallgemeinerung führt aber von selbst auf drei Dateien, nach den Bereichen, die
`domaene/CLAUDE.md` schon kennt.

**F1 · Schnitt und Kürzel.**
- `spielobjekte.md`, Kürzel OBJ. OBJ-1 · Armeen und Spielfeld: Jeder *Spieler* führt eine
  *Armee* aus *Einheiten* aus *Modellen*, jedes mit runder *Base*; das *Spielfeld* ist ein
  Rechteck in der Größe, die die *Mission* nennt (`core_rules.txt:305`, `:420`, `:452`,
  `:464`). Die Werte einer Partie bleiben in den YAML-Dateien. Ersetzt AUF-2.1 bis AUF-2.3.
- `querschnitt.md`, Kürzel QUE. QUE-1 · Setzen: *Setzen* bringt ein *Modell* an eine
  *Stelle*; überdeckt seine *Base* dort eine andere: *Sperre* ‚Base überdeckt‘. Welche
  *Modelle* gesetzt werden dürfen und was sonst gesperrt ist, sagt die Phase. Ersetzt AUF-3.1
  und AUF-3.3. QUE-2 · Bewegen ohne Überdecken kommt mit Etappe 2 (F3).
- `phasen/aufstellen.md` behält AUF-1, die *Aufstellungszonen* und die *Ausgangslage* von Only
  War (AUF-2.4, AUF-2.5) und die Sperren beim *Setzen*, die nur in der *Aufstellung* gelten:
  Zone, Nahkampfreichweite (100), AUF-3.6, AUF-3.7.

A: so. B: Du nennst einen anderen Schnitt oder andere Kürzel.
Empfehlung A: Was jede *Mission* und jede Phase braucht, steht dann einmal und nicht im Kleid
von Only War; Reinforcements (`core_rules.txt:800`) und Bewegen greifen später auf dasselbe
*Setzen* und dieselbe *Sperre* zu. Die Werte bleiben, wo sie sind, nur die Kriterien ziehen um.

Antwort: .

**F2 · Zeitpunkt.** Die ersetzten Kennungen kommen nie wieder; Item 1, Item 2 und Plan 2
müssen die neuen nennen, das macht der Planer.
A: jetzt, vor der Freigabe von Plan 2. B: nach Zyklus 2.
Empfehlung A: Noch nennt kein Test AUF-2 oder AUF-3 (sie warten auf den Testautor). Jetzt
kostet es einen Lauf des Planers, der für 104 ohnehin dran ist; nach Zyklus 2 wären die
Tests schon geschrieben und jede Umbenennung eine Neufassung gegen einen Test.

Antwort: .

**F3 · Überdecken beim Bewegen.** Die Regel ist strenger als das Ende des Zugs: Kein Teil der
*Base* darf über die *Bases* anderer *Modelle* hinweg bewegt werden, auf jedem Weg
(`core_rules.txt:729`); nur FLY darf darüber (`:1893`, Etappe 6). Der alte PoC hat beim
Ziehen am Rand angehalten, aber nur das Ende geprüft (`domaene/referenz/domainRules.md:77`).
A: Arbiter prüft den gezogenen Weg; überdeckt die *Base* unterwegs eine andere, ist der Zug
gesperrt. B: Arbiter prüft nur, wo das *Modell* am Ende steht.
Empfehlung A: Das sagt die Regel, und Regelkonformität geht vor Komfort (`domaene/ziel.md`);
den Weg zieht man ohnehin auf der Karte. Das Kriterium schreibe ich mit den Anforderungen zu
Etappe 2.

Antwort: .
