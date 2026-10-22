# Zum zweiten Schnitt: Fahrzeug, Moral, Siegpunkte, Zurücksetzen

Form: Fragen
Von: Planer
An: Stakeholder
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Beim Prüfen des Schnitts in [2363](2363-schnittBewegungsformenZuerst.md) fallen
vier Lücken oder Konflikte auf, die weder Regel noch Quelle entscheiden.

**Kosten.** Ohne Antwort baut Etappe 2 ein Fahrzeug, das die Karte nicht zeigen kann. Ab
Etappe 4 weicht die Partie von der Regel ab, und eine Partie hat keinen Sieger.

**Gegenvorschlag.** Antwortest du „.“, gelten alle Empfehlungen.

**F1 · Wann kommt das Fahrzeug?** Der Trukk hat keine *Base*
(`ArbiterMap/data/poc/units/orks_trukk.yaml:20`). Hull, ovale *Bases* und Drehen standen in
der Etappe „Jede Baseform“, die dein Schnitt nicht mehr nennt.
- A: in Etappe 2, mit Hull und Drehen.
- B: in einer eigenen Etappe „Fahrzeuge und jede Baseform“ nach Etappe 3; bis dahin nur
  runde *Bases*.

Empfehlung: B. Etappe 2 ist ohnehin die größte. Spätestens in Etappe 4 braucht ihr die Hulls,
weil die Reichweite von der *Base* oder dem Hull aus gemessen wird. Psioniker und Spinne
kommen in Etappe 2, sofern ihre *Base* rund ist; sonst kommen sie mit dem Fahrzeug.
Antwort: B, übernimm die Konzepte von ArbiterMap, da ist schon viel angelegt. Wichtig ist, dass wir hier SOLID und Clean Code schreiben

**F2 · Moral mit den Verlusten?** Ab Etappe 4 entfernt ihr Verluste. Ohne Moralphase fehlen
die Moraltests (`core_rules.txt:2095`), und eine zerrissene *Einheit* bleibt auf der *Karte*
stehen (`:2143`). So hast du es in Anliegen 09 (F13 A) entschieden.
- A: Die Moralphase kommt in Etappe 4, die Psiphase bleibt in Etappe 5.
- B: Wie in deinem Schnitt, beide in Etappe 5.

Empfehlung: A. Kohärenz prüfen und *Modelle* entfernen gibt es dann schon.
Antwort: B, wir können fürs erste auf die Verluste in der Moralphase verzichten, als ob das dort nicht passieren würde.

**F3 · Missionsziele und Siegpunkte?** Dein Schnitt nennt sie nicht. Bei Only War entscheiden
die Siegpunkte, wer gewinnt, wenn keine Armee vernichtet ist (`core_rules.txt:2339`).
- A: in Etappe 5, damit danach eine Partie Orks gegen Necrons zu Ende geht.
- B: in Etappe 7, mit der Startseite.
- C: später, den Sieger bestimmt ihr am Tisch.

Empfehlung: A.
Antwort: A

**F4 · Bis wann lässt sich eine Bewegung zurücksetzen?** Die Regel bewegt jede *Einheit*
höchstens einmal je Bewegungsphase (`core_rules.txt:738`).
- A: bis die Bewegungsphase endet.
- B: bis die nächste *Einheit* bewegt wird.

Empfehlung: A. Ein Fehler fällt oft erst bei der nächsten *Einheit* auf. Zurückgesetzt steht
die *Einheit*, wo sie vorher stand, und darf neu bewegen.
Antwort: A

**Stellungnahme.**
