# BEW-24: „Einheit zurücksetzen“ ohne Rückfrage weicht von ArbiterMap ab

Form: Kritik
Von: Fachkritiker
An: Anforderungsautor
Runde: 1/3
Status: offen
Wartet auf: 10480

## Runde 1
**Befund.** Hält auf, weil das Item [zuruecksetzenUndLuecken](../../domaene/items/zuruecksetzenUndLuecken.md)
sonst nicht bereit ist ([DoR 6](../../prozess/ablauf/dor.md)). Die Kriterien von
[BEW-24](../../domaene/anforderungen/phasen/bewegung/einheitZuruecksetzen.md) und das Mockup
[bew-24](../../domaene/mockups/bew-24.html) zeigen „Einheit zurücksetzen“ als Knopf unter der
*Karte*, ein Klick setzt die *Einheit* zurück. Das Vorbild, das BEW-24 nennt, macht es anders:
In ArbiterMap steht der Knopf „Zurücksetzen (…″)“ mit der gezogenen Strecke auf der Karte der
*ausgewählten* *Einheit*; der Klick öffnet einen Dialog mit Skizze von alter und neuer *Stelle*
je *Modell*, erst „Bestätigen“ setzt zurück, „Abbrechen“ lässt alles stehen
(`ArbiterMap/frontend/CLAUDE.md`, Abschnitt „Reset-Dialog“; `model_drag.js:1143`). Der
Stakeholder hat in 2364 F4 A nur entschieden, bis wann man zurücksetzt, nicht wie; als Frage
entschieden ist die Abweichung nicht. Gleich gebaut wie bei uns sind „Einheit zurücklegen“
(AUF-23, 2220) und „Vorrücken zurücknehmen“ (BEW-12).

**Kosten.** Eine Frage an den Stakeholder, keine Zeile Code. Bleibt sie aus, sieht er im
Review 10 eine Bedienung, die er nicht gewählt hat; will er den Dialog, kommt er als neues
Kriterium und Mockup erst in Zyklus 11.

**Gegenvorschlag.** Frage ihn in einem Anliegen, Antwort zusammen mit der Freigabe von Plan 10;
bis dahin gilt die Empfehlung, also hält die Frage den Happy Path nicht auf
([Ich 1](../../prozess/praemissen/ich.md)):
- A: Ein Klick auf „Einheit zurücksetzen“ unter der *Karte*, ohne Rückfrage, wie „Einheit
  zurücklegen“ und „Vorrücken zurücknehmen“.
- B: Wie ArbiterMap: Knopf mit Strecke, Dialog mit Skizze, „Bestätigen“ oder „Abbrechen“; ein
  Kriterium und ein Mockup mehr.
Empfehlung A: gleiche Bedienung wie die beiden anderen Rücknahmen, und ein Fehlklick kostet
nichts, die *Einheit* zieht man neu. Schreib die Entscheidung als Quelle an BEW-24.1.

**Stellungnahme.** Befund trifft zu (`ArbiterMap/frontend/CLAUDE.md:350`). Die Frage steht mit
deinen Möglichkeiten und Empfehlung A in [10480](10480-zuruecksetzenMitOderOhneRueckfrage.md);
bis zur Antwort gilt A, BEW-24 und bew-24 bleiben. Mit der Antwort schreibe ich sie als Quelle an
BEW-24.1 (A) oder lege das Kriterium für den Dialog an (B) und setze `angenommen`.
