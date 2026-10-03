# Plan · Zyklus 2

Etappe: [1 · Aufstellen](../domaene/etappen/01-aufstellen.md)

## Items
1. [Ausgangslage von Only War](../domaene/items/ausgangslage-only-war.md)
2. [Sperren beim Setzen](../domaene/items/sperren-beim-setzen.md), nach Item 1

Noch keins ist bereit: [AUF-1](../domaene/anforderungen/phasen/aufstellen.md) ist gebaut, für
den nächsten Schnitt fehlen Kriterien. Was sie abdecken sollen, steht in
[94](anliegen/94-kriterienFuerPlan2.md) an den Anforderungsautor; danach trage ich die
Kriterien-IDs in die Items ein.

## Empfehlung
Freigeben mit beiden Items, sobald die Kriterien aus 94 stehen und der Architekt sie geprüft
hat; vorher nicht. Reihenfolge nach Abhängigkeit und Nutzen: Die Sperren beim Setzen sind der
Kern von Etappe 1 und das erste Stück Geometrie (Bases, Zonen, Abstände), auf dem Bewegen,
Schießen und Charge aufbauen; prüfen lassen sie sich erst mit den Bases und Zonen der
Ausgangslage. Reicht der Zyklus nur für eins, kommt Item 1 allein. Beide Items sind reine
Fachlogik wie Item 1 in Zyklus 1: Nach Zyklus 2 ist noch nichts klickbar.

Grenzen der Items, damit Testautor und Implementierer nichts erfinden:
- Gesetzt wird in Tests nur aus der Ausgangslage; die Ablage als Ort neben der Karte, Umsetzen
  und Zurücklegen kommen später (Etappe 1, Anliegen 16 F1, F2, git).
- Die Tests prüfen Sperre und Grund, nicht, wo das gesperrte Modell danach steht; Stehenbleiben,
  „zurück“, „gemeinsam übergehen“ und Protokoll kommen später (16 F4).
- Akzeptanztests beenden eine Einheit erst, wenn alle ihre Modelle gesetzt sind und die Einheit
  in Kohärenz steht; die Sperren beim Beenden kommen später (16 F3).
- Nur runde Bases ohne FLY; andere Formen bringt Etappe 6.

## Danach, nach Abhängigkeit
Ablage, Umsetzen, Zurücklegen und die erste Oberfläche: Karte mit Spielfeld und Zonen,
Ziehen mit Maus und Touch, dafür UX und Mockup · Zurück, gemeinsam übergehen und Protokoll
(16 F4) · Beenden mit fehlenden Modellen und Kohärenz (16 F3). Mit diesen drei ist Etappe 1
erreichbar.

## Offene Anliegen
An dich:
- [21](anliegen/21-auf1-neue-begriffe.md), Vorschlag des Anforderungsautors: neue Begriffe
  zu AUF-1, deine Antwort steht.
- [83](anliegen/83-sprungErproben.md): Sprung zwischen Kriterium und Test erproben.
- [90](anliegen/90-dashboardWannUndWo.md): Dashboard, wann und wo.

Zwischen Rollen:
- [94](anliegen/94-kriterienFuerPlan2.md) an den Anforderungsautor: blockiert die Freigabe.
- [95](anliegen/95-standNenntAnforderungsautorNichtMehr.md) an den Organisationsentwickler: Der
  Stand kennt ab Zyklus 2 den Schritt des Anforderungsautors nicht; wartet bis zur
  Prozessphase.
- [13](anliegen/13-kuerzen-ohne-entscheidungsverlust.md) angenommen, Nachprüfung durch den
  Architekten. 09 und 16 sind erledigt: Ihre Entscheidungen stehen in Etappe 1 und, für
  später zurückgestellt, in git.
