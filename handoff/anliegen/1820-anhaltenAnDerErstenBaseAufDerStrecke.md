# AUF-26.2, 26.3 und 27.2 sollen an der ersten Base auf der Strecke anhalten

Form: Kritik
Von: Testautor
An: Anforderungsautor
Runde: 1/3
Status: offen
Wartet auf: Domänenphase

## Runde 1
**Befund.** Auf Wunsch des Stakeholders in [1320](1320-kreuztDieStreckeEineBaseUndLiegtDasZielFrei.md) (Kommentar: „wie in ArbiterMap, Anforderungen erst im nächsten Zyklus anpassen, vormerken“) gilt künftig: Ein gezogenes *Modell* oder ein Block hält an der ersten *Base* an, die seine gerade Strecke berührt, auch wenn das Ziel dahinter frei liegt. Heute lesen der Architekt ([V10](../../technik/architektur/handlungen.md)) und die Tests AUF-26.2 und 26.3 so, dass nur zählt, ob die *Stelle* am Ende des Wegs eine *Base* *überdeckt*. Betroffen sind [AUF-26.2 und 26.3](../../domaene/anforderungen/phasen/aufstellen/anhaltenAnEinerBase.md), AUF-26.4 (zeigt dieselbe *Stelle*) und AUF-27.2.

**Kosten.** Bleibt es beim Ist, springt ein *Modell* über fremde *Bases*, was am Tisch nicht geht. Die Änderung trifft Kriterien, V10, Tests und Code in einem Zyklus; deshalb erst in der nächsten Domänenphase.

**Gegenvorschlag.** Die Kriterien sagen ausdrücklich: Berührt die gerade Strecke von der vorigen *Stelle* zum Ziel eine fremde *Base*, steht das *Modell* an der letzten freien *Stelle* davor (Block: starr, die eigene *Einheit* sperrt sich nicht selbst). Vorbild: ArbiterMap, `docs/spec/interaction_map.md` (Entscheidungen 100. und 101. Sitzung, Item 061 F-1) und `backend/app/domain/geometry.py` (`last_allowed_point_before_blocked_discs`). Danach schreibt der Testautor die Fälle neu.

**Stellungnahme.**
