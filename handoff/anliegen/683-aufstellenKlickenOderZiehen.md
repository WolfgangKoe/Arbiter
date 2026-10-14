# Aufstellen: in die Zone klicken, ziehen oder beides?

683 · Fragen · von Ux → Stakeholder · Runde 2/3 · offen

## Runde 1
**Befund.** Dein Test am Bildschirm: Das Ziehen der Karte aus der *Ablage* ist nicht intuitiv.
Du erwartest: *Einheit* in der *Ablage* auswählen, in die *Aufstellungszone* klicken, die *Einheit*
steht dort in *Kohärenz*, dann setzt du sie als Ganzes an die gewünschte *Stelle*; so macht es
ArbiterMap (`deployment.js`, `docs/spec/interaction_map.md`: „Ganze Einheit“, Zeile 360).
Heute: Klick wählt nur aus (AUF-5.3); *setzen* geht nur durch Ziehen aus der *Ablage* (AUF-8.5,
8.6); einzelne *Modelle* lassen sich ziehen (AUF-8.2), die *Einheit* als Block nicht. Fehler beim
Ziehen: [682](682-gezogeneKarteVerschwindetAmSpaltenrand.md) und
[680](680-markierterTextSperrtDasZiehen.md).

**Kosten.** Ohne Antwort baut keiner die Bedienung, die du erwartest.
[681](681-zeigenWasDerSpielerTunKann.md) bleibt offen.

**Gegenvorschlag.** Ich empfehle B.

**F1 · Wie stellt der *Spieler* eine *Einheit* auf?**
- A · Nur klicken, wie ArbiterMap. Das Ziehen aus der *Ablage* entfällt. Ändert: AUF-8.5 (Klick
  statt Ziehen), AUF-16.1, 16.4, 16.5 entfallen; neu: Block verschieben. Betroffen: die Items
  „ziehen“ und „gesperrtStehenUndZurueck“, ihre Tests; ein neues Item. Größter Eingriff.
- B · Klicken und Ziehen; kein Kriterium entfällt, ein neues Item.
- C · Nur Ziehen wie heute, besser erklärt; ein neues Item.

Antwort: A

**F2 · Wie wählt der *Spieler*, ob Ziehen die ganze *Einheit* oder ein *Modell* verschiebt?**
- a · Umschalter „Ganze Einheit / Einzelmodelle“ wie ArbiterMap (`interaction_map.md:191`).
- b · Dein eigener Vorschlag.

Antwort: A
Kommentar: Rückfrage: Ich würde Review 5 so erstmal abnehmen, weil die DoD erfüllt ist und hier offensichtlich eine Anforderung fehlt. Hinweis für die Retro: Wie können wir so etwas künftig vermeiden? An sich funktioniert der Ablauf wie gedacht. Von dem her ist es okay. Nur haben wir so viel Zeit und ressourcen "vergeudet", um überhaupt hierher zu kommen. Ich möchte solche Interventionen nicht in jedem Zyklus fahren. Dann ist das hier auch nicht so schlimm. Ich möchte ein funktinoierendes Produkt, dass sich vom Handling und Aussehen an Arbiter-old und ArbiterMap orientiert. Ich meine, dass ich das immer wieder gesagt habe. Die Problem an diesen beiden PoCs ist, dass die Code-Grundlage irgendwann Müll und nicht mehr zu warten ist. Das muss hier gelöst werden. Ansonsten ist das meisten von außen betrachtet schon so ziemlich das, was ich haben will. Hast du das verstanden?

## Runde 2
**Befund.** Deine Antworten: F1 A, F2 a. Ja, ich habe verstanden:
1. Die Bedienung folgt ArbiterMap: *Einheit* auswählen, in die Zone klicken, *Formation* steht
   in *Kohärenz*, dann als Ganzes verschieben; einzelne *Modelle* über den Umschalter. Das Ziehen
   aus der *Ablage* entfällt, damit auch sein Randfehler (682) und das Markieren (680) für diesen
   Weg.
2. Du nimmst Review 5 ab: Die DoD ist erfüllt, die Anforderung fehlte. Das ist Fehler der
   Anforderungen, nicht der Technik.
3. Du willst Handling und Aussehen von Arbiter-old und ArbiterMap, aber ohne deren wuchernden
   Code; das löst die Technik, nicht die Domäne.
4. Der Eingriff hat viel gekostet; er soll nicht jeden Zyklus nötig sein. Dein Retro-Hinweis
   liegt als [685](685-bedienungVorDemBildschirmTestPruefen.md) beim Organisationsentwickler.

Daraus folgt: [684](684-anforderungenFuerKlickenBlockUndGrund.md) auf A und a angepasst, der
Anforderungsautor beginnt; 681 angepasst; Mockups erst nach den Kriterien.

**Kosten.** Bleibt 683 offen, wartet niemand mehr auf etwas; es geht nur um deine Bestätigung.

**Gegenvorschlag.** Setze `angenommen`, wenn das stimmt, sonst schreibe, was fehlt.

**Stellungnahme.**
