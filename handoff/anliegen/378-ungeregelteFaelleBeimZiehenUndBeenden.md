# Ungeregelte Fälle beim Ziehen und Beenden

378 · Fragen · von Architekt (Technik) → Anforderungsautor (Domäne) · Runde 1/3 · angenommen

## Runde 1
**Befund.** In den Kriterien von Plan 5 fehlen drei Fälle, die Bildschirm und Vertrag
entscheiden müssen:
1. Wie lange nennt Arbiter den *Grund* einer *Sperre* nach AUF-7.4, AUF-10.2 oder AUF-10.3?
   [AUF-12.3](../../domaene/anforderungen/phasen/aufstellen/sperreOhneStelle.md) gilt nur für
   AUF-12.2; „zurück“ dazu bringt erst AUF-13 (Plan 6).
2. Lädt jemand die Seite neu (QUE-3.2), nennt Arbiter dann den *Grund* eines *gesperrten*
   *Modells* noch? QUE-3.2 nennt nur *Karte* und *Ablagen*.
3. Was geschieht beim Loslassen, wenn keins von AUF-8.2 bis 8.5 und AUF-14.1 greift: eine
   *Einheit*, deren *Modelle* alle *gesetzt* sind (AUF-4.3 zeigt sie noch), auf die *Karte*;
   ein *Modell* der *Einheit in Aufstellung* auf die *Ablage* des anderen *Spielers*; irgendetwas
   neben *Karte* und *Ablagen*?

**Kosten.** Ohne Kriterium entscheidet der Implementierer, und kein Test hält es fest. Für 2
wählt die Technik, ob der *Grund* zum Spielstand gehört oder nur zur Antwort auf die Handlung.

**Gegenvorschlag.**

**F1 · Anzeige.** A: ein Kriterium: „Gegeben eine *Sperre* nach AUF-7.4, AUF-10.2 oder
AUF-10.3, dann nennt Arbiter ihren *Grund* bis zur nächsten Handlung.“ AUF-13.3 passt dazu.
B: Der *Grund* bleibt bis zum nächsten erfolgreichen *Aufstellen der Einheit beenden*.
Empfehlung A: gleich wie AUF-12.3.

Antwort: A

**F2 · Neu laden.** A: QUE-3.2 nennt auch jeden *Grund* eines *gesperrten* *Modells*.
B: nein, nach dem Neuladen steht es *gesperrt* ohne *Grund*. Empfehlung A: Das *Modell* bleibt
*gesperrt*, der Spieler soll wissen, warum.

Antwort: A

**F3 · Loslassen ohne Ziel.** A: ein Kriterium: „Wenn jemand eine *Einheit* oder ein *Modell*
loslässt und keins von AUF-8.2 bis 8.5 und AUF-14.1 greift, dann steht sie oder es, wo sie
oder es vor dem Ziehen war, ohne *Grund*.“ B: wie A, aber mit *Sperre* ‚nicht wählbar‘.
Empfehlung A: Es ist keine regelwidrige Handlung, nur kein Ziel.

Antwort: an den Stakeholder, [380](380-loslassenOhneZiel.md)

**Stellungnahme.** F1 A steht als
[AUF-12.4](../../domaene/anforderungen/phasen/aufstellen/sperreOhneStelle.md). AUF-12 zählt
AUF-7 schon zu den *Sperren* ohne *Stelle*, und nach AUF-13.3 endet die *Sperre* nach AUF-10.2
oder 10.3 mit der nächsten Handlung. F2 A steht als
[QUE-3.5](../../domaene/anforderungen/querschnitt/bedienung.md). Nach dem Glossar bleibt ein
*gesperrtes* *Modell* mit seinem *Grund* stehen, bis die *Spieler* *zurück* oder *gemeinsam
übergehen* wählen; Neuladen ist keins von beiden. F3 sagen Regel und Ziel nicht, deshalb
frage ich den Stakeholder in [380](380-loslassenOhneZiel.md). Ein *Modell* auf die *Ablage* des
anderen *Spielers* empfehle ich dort als *Sperre* wie AUF-8.4.
