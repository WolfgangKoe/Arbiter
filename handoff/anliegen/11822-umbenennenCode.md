# Umbenennen nach 7800: Code und Frontend

Form: Kritik
Von: Planer
An: Implementierer
Runde: 1/3
Status: offen
Wartet auf: Technikphase 10

## Runde 1
**Befund.** Nach [7800](7800-karteUndEbeneBenennen.md) heißt *Karte* *Spielfeld* (F1 A), *Ebene*
bleibt mit *Einheitenebene* und *Modellebene* (F2 B); der Stakeholder regt *Ebene* als Obertyp an,
überlässt es aber euch. Domäne, Web, Frontend und Einheitstests sagen noch *Karte* und *Ebene*
([Wir 2](../../prozess/praemissen/wir.md)). armeeKarte und einheitenKarte bleiben (7800).

**Kosten.** Laut 7800 rund 34 Stellen *Karte* im Frontend, *Ebene* 62 in 6 Domänendateien und 9 im
Frontend, dazu Einheitstests; mechanisch. Ohne diesen Schritt fehlt die Umbenennung in Review 10
(Anliegen 11780).

**Gegenvorschlag.** Wann: nach [11820](11820-umbenennenGlossarUndAnforderungen.md) (Glossar),
gleichzeitig mit [11821](11821-umbenennenTests.md); vor „Reviewer: DoD über das Inkrement“
(7800 F3).

**Stellungnahme.**
