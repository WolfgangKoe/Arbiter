# Einheit auf einer Ablage, zurück ohne gesperrtes Modell

389 · Fragen · von Architekt (Technik) → Anforderungsautor (Domäne) · Runde 1/3 · offen

## Runde 1
**Befund.** Zwei Fälle regelt keine Anforderung:
1. Eine *Einheit* wird aus der *Ablage* auf eine *Ablage* gezogen und losgelassen. AUF-16.2
   nennt nur „neben *Karte* und *Ablagen*“, AUF-8 nur die *Karte*.
2. „zurück“ kommt an, ohne dass ein *Modell* *gesperrt* ist: zweimal gesendet oder von einer
   zweiten Seite (QUE-3.2). Das Glossar sagt nur, was mit einem *gesperrten* geschieht.

**Kosten.** Der Vertrag ([V5, V8](../../technik/architektur/handlungen.md)) nimmt bis zur
Antwort an: 1 schickt keine Anfrage, 2 ändert nichts, ohne *Grund*. Ohne Kriterium prüft
das kein Akzeptanztest.

**Gegenvorschlag.** 1: AUF-16.2 um „eine *Einheit* auf einer *Ablage*“ erweitern (Plan 5:
„Was ohne Ziel losgelassen wird, springt still zurück“). 2: ein Kriterium „Gegeben kein
*gesperrtes* *Modell*, wenn ein *Spieler* *zurück* wählt, dann bleibt alles wie davor, ohne
*Grund*“. Weichst du ab, ziehe ich den Vertrag nach.

**Stellungnahme.** 2 angenommen als neue Anforderung
[AUF-17.1](../../domaene/anforderungen/phasen/aufstellen/zurueckOhneSperre.md): Gegeben kein
*gesperrtes* *Modell* und keine *Sperre* nach AUF-10.2 oder 10.3, bleibt bei *zurück* alles wie
davor, ohne *Grund* (wie 380 F1 A). Die Sperre beim Beenden nehme ich aus, weil dort *zurück*
nach AUF-13.2 wirkt. 1 teilweise: Für die eigene *Ablage*
[AUF-16.4](../../domaene/anforderungen/phasen/aufstellen/loslassenOhneZiel.md), still zurück.
Für die *Ablage* des anderen *Spielers* sprechen 380 F1 A (still) und 380 F2 B (*Sperre*, wie
AUF-16.3); das frage ich den Stakeholder in [Anliegen 390](390-einheitAufDerAblageDesGegners.md).
Bis zur Antwort bleibt dein Vertrag dort bei „keine Anfrage“. 389 wartet auf 390; danach
setze ich `angenommen`.
