# Mockups zur Formation

375 · Kritik · von Planer (Domäne) → UX (Domäne) · Runde 2/3 · angenommen

## Runde 1
**Befund.** Nach dem Kommentar des Stakeholders zu [Plan 5](../plan.md#freigabe) kommt eine
*Einheit* ganz auf die *Karte*. Neu sind
[AUF-8.5, 8.6](../../domaene/anforderungen/phasen/aufstellen/ziehen.md): Arbiter *setzt* die
*Formation* ([formation.yaml](../../domaene/daten/formation.yaml), Boyz in Reihen 3, 4, 3,
Abstand 1,5″) mittig ans Loslassen und rückt sie in die eigene *Aufstellungszone*;
[AUF-14.1](../../domaene/anforderungen/phasen/aufstellen/restDerEinheit.md): nach
*zurücklegen* bringt jedes Ziehen der *Einheit* ein *Modell*;
[AUF-15.1](../../domaene/anforderungen/phasen/aufstellen/gesperrteFormation.md): Ist ein
*Modell* der *Formation* *gesperrt*, nimmt ein *zurück* alle *Modelle* dieses Loslassens.
AUF-8.1 entfällt. Die Mockups zeigen noch Aufstellen *Modell* für *Modell*:
- [auf-8](../../domaene/mockups/auf-8.html): vier Boyz auf der *Karte*, sechs in der
  *Ablage*; so entsteht nach AUF-8.5 kein Stand.
- [auf-9](../../domaene/mockups/auf-9.html): ‚nicht ganz in der Zone‘ kann nach AUF-8.6 nur
  ein umgesetztes (AUF-8.2) oder einzeln geholtes (AUF-14.1) *Modell* haben. Eine *gesperrte*
  *Formation* (‚Base überdeckt‘ oder Nahkampfreichweite) mit einem „zurück“ für alle fehlt.
- [auf-10](../../domaene/mockups/auf-10.html), [auf-12](../../domaene/mockups/auf-12.html):
  Boyz mit zwei oder acht *Modellen* in der *Ablage* gibt es nur noch nach *zurücklegen*;
  bitte prüfen, ob die Stände so bleiben können.

**Kosten.** Ohne Anpassung erfüllt keins der drei Items in Plan 5 DoR 5; der Plan bleibt
ohne Freigabe.

**Gegenvorschlag.** auf-8 zeigt die Boyz in ihrer *Formation* auf der *Karte*. AUF-14 und
AUF-15 bekommen je ein Mockup oder stehen in auf-8 und auf-9, wie es deine Regel „je
Anforderung ein Mockup“ verlangt. auf-9 zeigt ‚nicht ganz in der Zone‘ an einem umgesetzten
*Modell*. Braucht ein Bestandteil eine Entscheidung des Architekten, gehört er in
[372](372-bestandteileDerOberflaecheFuerZiehenSperreUndBeenden.md).

**Stellungnahme.**
Angenommen, umgesetzt:
- [auf-8](../../domaene/mockups/auf-8.html): Boyz in Reihen 3, 4, 3 mittig in der
  *Aufstellungszone*, *Ablage* 0.
- [auf-9](../../domaene/mockups/auf-9.html): *Formation* mit zwei Lücken, ein einzeln
  geholtes *Modell* (AUF-14.1) ‚nicht ganz in der Zone‘, „zurück“ und „gemeinsam übergehen“.
- [auf-15](../../domaene/mockups/auf-15.html) neu: *gesperrte* *Formation*, ein *Modell* über
  dem Warboss ‚Base überdeckt‘; „zurück“ nimmt alle *Modelle* dieses Loslassens.
- auf-10, auf-12 unverändert: Stände mit 2 und 8 *Modellen* in der *Ablage* entstehen nach
  *zurücklegen*.
Die Items [Ziehen](../../domaene/items/ziehen.md) und
[Gesperrt stehen und zurück](../../domaene/items/gesperrtStehenUndZurueck.md) verlinken die
Mockups. Der *Abstand* 1,5″ ist zwischen den Rändern der *Bases* gemessen (Glossar).

## Runde 2
**Befund.** *Formation* und Geometrie stimmen. Gezählt wie in auf-12 (ein *gesperrtes*
*Modell* zählt in der *Ablage* mit) passen vier Stände nicht:
1. auf-8: Boyz „0“; nach [AUF-4.3](../../domaene/anforderungen/phasen/aufstellen/anzeige.md)
   steht keine Anzahl, wenn alle *gesetzt* sind.
2. auf-9: 8 + 1 auf der *Karte* und 3 in der *Ablage* sind 12 Boyz statt 10; richtig ist 2.
3. auf-15: Der Warboss steht auf der *Karte* und noch in der *Ablage* (Glossar: nur nicht
   *aufgestellte*); Spieler 2 wäre zwischen Warboss und Boyz an der Reihe gewesen ([AUF-1.7](../../domaene/anforderungen/phasen/aufstellen/reihenfolge.md)).
4. Warboss-*Base*: [ausgangslage.yaml](../../domaene/daten/ausgangslage.yaml) nennt 40 mm,
   r ≈ 0,787″.

**Kosten.** Die Technik baut die Mockups wörtlich ein, gegen AUF-4.3.

**Gegenvorschlag.** auf-8 ohne Anzahl, auf-9 mit 2, auf-15 mit Warboss r 0,787 ohne
*Ablage*-Eintrag und einer *aufgestellten* *Einheit* von Spieler 2. Zählst du anders, frag
den Anforderungsautor.

**Stellungnahme.**
Angenommen, berichtigt: [auf-8](../../domaene/mockups/auf-8.html) ohne Anzahl;
[auf-9](../../domaene/mockups/auf-9.html) mit 2; [auf-15](../../domaene/mockups/auf-15.html)
ohne Warboss in der *Ablage*, Warboss-*Base* r 0,787, Overlord von Spieler 2 *aufgestellt*
auf der *Karte* und nicht mehr in der *Ablage*.
