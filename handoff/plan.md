# Plan · Zyklus 1

Etappe: [1 · Aufstellen](../domaene/etappen/01-aufstellen.md)

## Item
1. [Reihenfolge der Aufstellung](../domaene/items/reihenfolge-der-aufstellung.md): alle
   Kriterien von [AUF-1](../domaene/anforderungen/phasen/aufstellen.md).

Mehr ist nicht bereit: AUF-1 ist die einzige Anforderung. Vor der Freigabe arbeitet der
Anforderungsautor [15](anliegen/15-aufstellen-begriffe-bereich-roll-off.md),
[17](anliegen/17-auf1-reihe-nach-dem-beenden.md) und
[18](anliegen/18-auf1-begriffe-und-grund-der-sperre.md) in AUF-1 ein; das Item folgt dieser
Fassung, auch einem Kriterium für die Wahl des Gewinners des Roll-offs (15 F3).

## Empfehlung
Freigeben mit diesem einen Item, sobald AUF-1 nach 15, 17 und 18 steht. Es baut das Gerüst,
an dem jede weitere Sperre der Etappe hängt: wer an der Reihe ist, welche Einheit in
Aufstellung ist, wann die Aufstellung endet. Das Item ist reine Fachlogik
([19](anliegen/19-plan1-fachlogik-oder-karte.md)): Danach belegen Akzeptanztests die
Reihenfolge; spielbar wird sie mit Spielfeld und Ablage in den nächsten Items. Nach Zyklus 1
ist nichts klickbar.

Grenzen des Items, damit Testautor und Implementierer nichts erfinden:
- Den Gewinner des Roll-offs wählen die Spieler; Arbiter nimmt keine Würfel entgegen (15 F3).
- Die zwei Aufstellungszonen sind nur unterscheidbar; ihre Form (09 F10) kommt mit dem
  Spielfeld.
- Die Stelle eines gesetzten Modells wird nicht geprüft (Zone, Überdecken, Engagement Range);
  Ablage, Umsetzen und Zurücklegen kommen später (16 F1, F2).
- Akzeptanztests beenden eine Einheit erst, wenn alle ihre Modelle gesetzt sind; die Sperren
  beim Beenden (fehlende Modelle, Kohärenz) kommen später (16 F3).
- Die Sperre aus AUF-1.4 nennt ihren Grund (18). Die Tests prüfen Sperre und Grund, nicht, wo
  das Modell danach steht; Zurück, Übergehen und Protokoll kommen später (16 F4).
- Die Armeen der Tests sind Testdaten; die Ausgangslage (09 F1) kommt mit dem Spielfeld.

## Danach, nach Abhängigkeit
Ausgangslage und Spielfeld mit Aufstellungszonen (09 F1, F10) · Ablage, Setzen, Umsetzen und
die Sperren beim Loslassen (09 F12, 16 F1, F2) · Beenden mit fehlenden Modellen und Kohärenz
(16 F3) · Zurück, Übergehen und Protokoll (16 F4). Die Anforderungen dazu schreibt der
Anforderungsautor; die erste Oberfläche braucht ein Mockup.

## Offene Anliegen
An dich: keine offene Frage. Eingearbeitet sind
[09](anliegen/09-fragen-freigabe-etappen.md) (F4 und F11 bleiben zurückgestellt),
[16](anliegen/16-aufstellen-ablage-beenden-uebergehen.md) aus
[11](anliegen/11-etappe1-ablage-umsetzen-uebergehen.md) und 15 F3.

Zur Kenntnis, angenommen und umgesetzt:
- [12](anliegen/12-reihenfolge-baseformen-nach-nahkampf.md): Schießen (4) und Charge und
  Nahkampf (5) kommen vor Jede Baseform (6); das erste Probespiel kommt so früher, mit der
  Ausgangslage aus runden Bases. Brauchst du die Formen früher, widersprich in 12.
- [19](anliegen/19-plan1-fachlogik-oder-karte.md): Item 1 ohne Oberfläche, Grenzen oben.

Zwischen Rollen:
- 15, 17, 18 an den Anforderungsautor: vor der Freigabe.
- [14](anliegen/14-planer-liest-git-vor-dem-ausformulieren.md) und
  [20](anliegen/20-antwort-unter-jeder-frage.md) an den Organisationsentwickler: Prozessphase.
