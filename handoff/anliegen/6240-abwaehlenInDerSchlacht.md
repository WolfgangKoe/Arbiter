# Abwählen einer Einheit in der Schlacht

Form: Kritik
Von: Fachkritiker
An: Anforderungsautor
Runde: 1/3
Status: offen
Wartet auf: Domänenphase 9

## Runde 1
**Befund.** Wartet (Ich 3: Lücke abseits des Happy Path; Schritt 3 aus Plan 8 läuft am
Bildschirm mit Maus und Finger, an einer Kopie in `/tmp` geprüft). Klickt man in der
*Bewegungsphase* ein *Modell* der Boyz an, ist ihre ganze *Einheit* *ausgewählt* (AUF-20.6),
und jeder Zug verschiebt sie als Block. Einzeln zieht man danach keines ihrer *Modelle*
mehr, etwa um einen Boy zurück in *Kohärenz* zu bringen: Ein weiterer Klick auf ein *Modell*
wählt sie nur wieder aus (in der *Schlacht* keine *Ebene*, [Vertrag Bewegung](../../technik/architektur/vertrag/bewegung.md) V14;
5520 Punkt 1, F3 B), die *Armeeliste* zeigt in der *Schlacht* keine *Einheit* zum Abwählen,
ein Klick auf die *Karte* wirkt nur auf die *Aufstellung*. Abwählen geht nur, indem man ein
*Modell* einer anderen *Einheit* anklickt („und keine andere“). Keine Anforderung regelt das
Abwählen in der *Schlacht*. ArbiterMap hebt die Auswahl mit einem Klick auf eine Leerfläche
auf (`ArbiterMap/frontend/static/js/model_selection.js:363`).

**Kosten.** Keine in Zyklus 8. Bleibt es, sucht der Spieler den Umweg über eine andere
*Einheit*; der Review muss ihn im Klickpfad nennen.

**Gegenvorschlag.** In Domänenphase 9 zusammen mit 5520 F3 B (*Ebene* in der *Schlacht*) ein
Kriterium zum Abwählen in der *Schlacht*, als Frage an den Stakeholder mit ArbiterMap als
Quelle (Klick auf eine Leerfläche der *Karte*).

**Stellungnahme.**
