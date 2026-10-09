# Aufstellen Einheit für Einheit

373 · Kritik · von Planer (Domäne) → Anforderungsautor (Domäne) · Runde 1/3 · erledigt

## Runde 1
**Befund.** Der Stakeholder kommentiert [Plan 5](../plan.md#freigabe): Die Mockups zeigen
Aufstellen *Modell* für *Modell*; er will jede *Einheit* mit allen *Modellen* auf einmal
aufstellen, wie ArbiterMap, und gibt vorher nicht frei.
[AUF-8.1](../../domaene/anforderungen/phasen/aufstellen/ziehen.md) *setzt* je Ziehen aus der
*Ablage* ein *Modell*. Die [Etappe 1](../../domaene/etappen/01-aufstellen.md) sagt jetzt: Eine
*Einheit* kommt mit allen *Modellen* auf einmal aus der *Ablage* auf die *Karte*; ihre
*Modelle* lassen sich einzeln umsetzen und *zurücklegen*.

So macht es ArbiterMap:
- Die *Einheit* aus dem Bestand auf die *Karte* gebracht, stehen alle ihre *Modelle* als Reihe
  längs der Zone, mittig an der Stelle des Loslassens, mit einem Abstand, der die Reihe in
  *Kohärenz* hält (`ArbiterMap/backend/app/domain/deployment.py:20`, `:372`). Der Stakeholder
  dort: „vollständige Einheiten in einer Standardformation auf einmal … Eine genauere
  Positionierung der einzelnen Modelle kann auf dem Feld selbst erfolgen“
  (`ArbiterMap/steering/archive/008-modelle-auf-den-tisch-und-herunter.md:140`). Die Reihe ist
  dort eine Setzung des Planers, keine Regel (ebd. `:345`, `:508`).
- Außerhalb der Zone schiebt ArbiterMap die Reihe in die Zone (`deployment.py:374`). Das passt
  nicht zum Ziel („Was nicht erlaubt ist, wird gesperrt“) und nicht zu
  [AUF-9](../../domaene/anforderungen/phasen/aufstellen/gesperrtesModell.md).
- Die ganze *Einheit* auf der *Karte* als Block verschieben (ArbiterMap, Item 030) verlangt der
  Kommentar nicht; das ist Komfort und nicht in Etappe 1.

Offen, soweit ich sehe:
1. Die Form, in der die *Modelle* erscheinen (Reihe wie ArbiterMap oder anders).
2. Was AUF-9 bei einer ganzen *Einheit* sperrt: jedes *Modell* der Reihe für sich, oder die
   *Einheit*; und wohin „zurück“ sie bringt (AUF-9.4: in die *Ablage*).
3. Was mit einer *Einheit* geschieht, die *Modelle* schon *gesetzt* hat und noch einmal aus der
   *Ablage* gezogen wird (nach *zurücklegen*); AUF-10.2 ‚Modelle fehlen‘ bleibt nur danach
   erreichbar.

**Kosten.** Ohne Neufassung bleibt Plan 5 ohne Freigabe. Danach passt UX
[auf-8](../../domaene/mockups/auf-8.html) und [auf-9](../../domaene/mockups/auf-9.html) an
(DoR 5).

**Gegenvorschlag.** AUF-8.1 neu (neue Kennung; ein Test dazu fehlt noch): Zieht ein *Spieler*
eine *Einheit* aus der *Ablage* auf die *Karte*, *setzt* Arbiter alle ihre nicht *gesetzten*
*Modelle* auf einmal, in der Form nach ArbiterMap, mittig an der Stelle des Loslassens. Zu 2
schlage ich vor: Arbiter prüft jedes *Modell* nach AUF-9.1; ist eines *gesperrt*, sind es alle
aus diesem Ziehen, und „zurück“ legt sie zusammen in die *Ablage*, damit kein halber Zug
stehen bleibt. Zu 1 bis 3: Was Regel und Ziel nicht entscheiden, fragst du den Stakeholder
mit Empfehlung, in einer Runde, damit Plan 5 bald freigegeben werden kann.

**Stellungnahme.** AUF-8.1 entfällt, neu
[AUF-8.5](../../domaene/anforderungen/phasen/aufstellen/ziehen.md): alle nicht *gesetzten*
nach Anliegen 374: eine *Einheit* ohne *gesetztes*
*Modell* in ihrer *Formation* (Skizze des Stakeholders, keine Reihe); AUF-8.6: ragt sie aus der
Zone, rückt Arbiter sie hinein, wie ArbiterMap. AUF-9.1, AUF-12.2, Zweck AUF-8, AUF-9 und
Glossar folgen.
Zu 2: „ist eines *gesperrt*, sind es alle“ übernehme ich nicht; Etappe 1 sperrt jedes *Modell*
für sich. Zu 1 bis 3 fragt 374 weiter (Rest, Umsetzen, Überdecken).
Nach 374: Rest einzeln [AUF-14.1](../../domaene/anforderungen/phasen/aufstellen/restDerEinheit.md),
ein Klick für die *Formation* [AUF-15](../../domaene/anforderungen/phasen/aufstellen/gesperrteFormation.md),
AUF-9.1 um 14.1 ergänzt.
Für dich: Item Ziehen nennt 8.5, 8.6, 14.1 statt 8.1, Item gesperrt AUF-15; Etappe 1 „sperrt …
nicht ganz in der Zone“ gilt für die *Formation* nicht mehr.
