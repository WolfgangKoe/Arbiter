# Begriffe Angebot, Übergangen und Anteile fehlen im Glossar

Form: Kritik
Von: Implementierer
An: Anforderungsautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Item anhaltenUebergehen braucht im Code drei Klassen in
[uebergehenBeimZiehen.py](../../technik/arbiter/domaene/phasen/bewegung/uebergehenBeimZiehen.py),
die nicht im [Glossar](../../domaene/glossar.md) stehen; die Glossarprüfung ist rot:
1. `Angebot`: das, was nach dem Loslassen bis zur nächsten Handlung bereitsteht, damit die
   Spieler das Anhalten gemeinsam übergehen können (Ebene, gezogenes Modell, Punkt).
2. `Übergangen`: das Ergebnis des gemeinsamen Übergehens (neue Stellen, Gründe, die
   weiter sperren, die übergangenen Gründe des Anhaltens, gezogenes Modell).
3. `Anteile`: die drei Anteile des Wegs, bis zu denen ein Modell kommt (Bewegungsweite,
   Spielfeldkante, Nahkampfreichweite).

**Kosten.** Die Prüfung bleibt rot, der Hook lässt keinen Commit durch.

**Gegenvorschlag.** Nimm die drei Begriffe ins Glossar auf, mit der Bedeutung oben oder
einer besseren. Gefällt dir ein anderer Name, nenne ihn; ich benenne um.

**Stellungnahme.** Angenommen, die Namen bleiben. Alle drei stehen im
[Glossar](../../domaene/glossar.md), an den Kriterien verankert: *Angebot* an BEW-8.3 und
8.4 („bietet … an“), *Anteile* an BEW-3.1, 6.1, 6.2 und 6.3 („gilt die kürzeste Strecke“),
*Übergangen* an BEW-8.4 und 8.5. Die Glossarprüfung (`formregeln.glossar`) ist grün.
