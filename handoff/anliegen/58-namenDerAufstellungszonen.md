# Wie heißen die zwei Aufstellungszonen?

58 · Fragen · von Anforderungsautor (Domäne) → Stakeholder · Runde 1/3 · offen

## Runde 1
Anlass: [43](43-aufstellungszoneNamen.md). Der Implementierer hat `nord` und `süd` ohne Quelle
gesetzt; die *Spieler* sehen den Namen, wenn der *Gewinner* seine *Aufstellungszone* wählt
([AUF-1.2](../../domaene/anforderungen/phasen/aufstellen.md)).

**F1 · Namen der Aufstellungszonen.** Die Regel nennt keine: Die Mission zeigt die Zonen nur auf
ihrer Karte, einem Bild (`core_rules.txt:2182`), und spricht von „one of the two deployment
zones“ (`:2322`). Etappe 1 legt sie als 9″-Bänder an die beiden langen Kanten des Spielfelds
44″ × 60″ ([09](09-fragen-freigabe-etappen.md) F10 B).
A: Nord und Süd, fest am Spielfeld; dreht sich die Ansicht, bleibt der Name.
B: Oben und Unten, nach der Lage auf dem Bildschirm; der Name folgt der Ansicht.
C: Keine Namen; die *Spieler* tippen die Zone auf der Karte an. Bis zur Karte (nicht in
Zyklus 1) braucht der Code trotzdem zwei Werte ohne fachlichen Namen.
Empfehlung A: Ein Name, der an der Karte hängt, gilt auch für Protokoll und spätere Regeln
(„enemy's battlefield edge“, `:3324`), unabhängig von Gerät und Drehung; `nord` und `süd`
stehen schon im Code. Nach deiner Antwort kommen die zwei Namen mit Code-Bezeichner ins
Glossar.

Antwort:
