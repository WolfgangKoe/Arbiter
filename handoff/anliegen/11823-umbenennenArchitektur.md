# Umbenennen nach 7800: Architektur

Form: Kritik
Von: Planer
An: Architekt
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Nach [7800](7800-karteUndEbeneBenennen.md) heißt *Karte* *Spielfeld* (F1 A), *Ebene*
bleibt mit *Einheitenebene* und *Modellebene* (F2 B). `technik/architektur/` sagt noch *Karte*
und *Ebene*, auch in Verträgen.

**Kosten.** Laut 7800 rund 18 Stellen *Karte* und 33 *Ebene*. Ohne diesen Schritt fehlt die
Umbenennung in Review 10 (Anliegen 11780).

**Gegenvorschlag.** Wann: nach [11820](11820-umbenennenGlossarUndAnforderungen.md) (Glossar),
gleichzeitig mit [11821](11821-umbenennenTests.md) und [11822](11822-umbenennenCode.md); vor
„Reviewer: DoD über das Inkrement“ (7800 F3). Ob *Ebene* ein Obertyp wird (Antwort zu F2),
entscheidest du mit dem Implementierer.

**Stellungnahme.** Umgesetzt in [Frontend](../../technik/architektur/frontend.md),
[Tests](../../technik/architektur/tests.md), [Domäne](../../technik/architektur/domaene.md) und den
Verträgen unter `technik/architektur/vertrag/`. *Karte* heißt *Spielfeld*, „neben der Karte“
„neben dem *Spielfeld*“; wo *Karte* die `.einheitenKarte` meinte ([V2](../../technik/architektur/vertrag/aufstellen/auswahl.md)),
steht die Klasse. *Ebene* bleibt als Oberbegriff („*Modelle* der *Ebene*“), die Fälle heißen
*Einheitenebene* und *Modellebene*. Die Stufen des Katalogs ([K2, K3](../../technik/architektur/katalog.md))
heißen nicht mehr „Ebenen“, damit das Wort eine Bedeutung hat.
Neue Namen im Vertrag, denen Tests (11821) und Code (11822) folgen:
- `karteAnklicken` → `spielfeldAnklicken`, Route `PUT /api/spielfeldAnklicken` (V19, AUF-18).
- `.karte` → `.spielfeld`, `komponenten/karte.js` → `komponenten/spielfeld.js` (O5, V8, B5).
- Spielstand `"ebene": true` → `"modellebene": true`; Beispiel `vertrag/ebene.json` →
  [modellebene.json](../../technik/architektur/vertrag/modellebene.json) (liest `dienst.py:264`).
- `ganzeEinheitIstEbene` → `hatEinheitenebene`, `modellIstEbene` → `istModellebene`,
  `ganzeEinheitAlsEbene` → `einheitenebeneWählen` (V3).

Obertyp: nein. Die beiden Fälle unterscheiden sich nur darin, welche *Modelle* ziehen, eine
Zeile in `Auswahl.ebene`; ein Typ mit zwei Untertypen wäre mehr Code für dieselbe Aussage
(Es 9). Beispiel: `Auswahl` hält das *Modell* der *Modellebene* oder keines; das steht als
„Warum“ in V3. Kommt ein dritter Fall mit eigenem Verhalten, wird *Ebene* ein Typ. Der
Implementierer kann in 11822 widersprechen.
