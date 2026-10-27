# Schließt die Strecke in BEW-2.2 die neue Stelle ein

Form: Fragen
Von: Testautor
An: Anforderungsautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** BEW-2.2 sperrt mit ‚über eine Base‘, wenn die *Base* „auf der geraden Strecke von
der vorigen zur neuen *Stelle*“ eine fremde *Base* *überdeckt*. Das Kriterium sagt nicht, ob
die neue *Stelle* selbst zur Strecke zählt. BEW-2.3 verlangt, dass Arbiter „jeden *Grund*“
nennt. Setzt ein *Modell* auf eine fremde *Base*, nennt Arbiter also entweder nur
‚Base überdeckt‘ (QUE-1.2) oder zusätzlich ‚über eine Base‘. Der Test zu BEW-2.3 prüft
deshalb vorerst nur, dass ‚Base überdeckt‘ unter den *Gründen* ist, nicht die ganze Menge.

**Kosten.** Ohne Klärung kann der Implementierer beide Lesarten grün machen, und der Test
sperrt keine davon; der *Spieler* sieht je nach Lesart einen oder zwei *Gründe*.

**Gegenvorschlag.** BEW-2.2 nennt die Strecke „einschließlich der neuen *Stelle*“.
Dann nennt Arbiter beim Setzen auf eine fremde *Base* beide *Gründe*, und der Testautor
prüft die Menge genau. Alternative: Die neue *Stelle* zählt nicht dazu; dann gilt nur
QUE-1.2, wenn die *Base* dort überdeckt.

**Fragen.** Empfehlung: einschließlich. Die gerade Strecke ist ein geschlossener Weg, und
BEW-2.3 verlangt ausdrücklich jeden *Grund*. Bis zur Antwort prüft der Test die Teilmenge.

**Stellungnahme.** Angenommen: einschließlich. [BEW-2.2](../../domaene/anforderungen/phasen/bewegung/sperrenBeimZiehen.md)
sagt jetzt „von der vorigen bis einschließlich der neuen *Stelle*“. So prüft auch das Vorbild:
Der Endpunkt in der Sperrfläche zählt als Treffer (`ArbiterMap/backend/app/domain/geometry.py:1253`).
Setzt ein *Modell* auf eine fremde *Base*, nennt Arbiter nach BEW-2.3 also ‚Base überdeckt‘
und ‚über eine Base‘; der Test zu BEW-2.3 kann die ganze Menge prüfen. Fremd bleibt nach AUF-29.3:
Ist die *Ebene* die ganze *Einheit*, entfallen an einem *Modell* derselben *Einheit* beide
*Gründe* (BEW-2.4). Die Kennung bleibt, weil kein bestehender Test der Schärfung widerspricht.
