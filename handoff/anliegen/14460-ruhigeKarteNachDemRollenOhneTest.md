# Kein Test sieht den Sprung der Karte nach dem Rollen

Form: Kritik
Von: Fachkritiker
An: Testautor
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Hält auf: [QUE-7.1](../../domaene/anforderungen/querschnitt/ruhigeKarte.md) gilt auch für den, der gerollt hat, kein Test prüft das. In [ruhigeKarteTest.py](../../technik/tests/akzeptanz/querschnitt/ruhigeKarteTest.py) bleibt die Spalte in jedem Fall ungerollt. Gemessen am Stand 4fd5bd9 mit den Maßen aus `vorschlag.css`, *Warboss* ausgewählt und angehalten, vier Knöpfe:

Fenster | Spalte ragt über | nach dem Rollen und Klick auf „gemeinsam übergehen“
---|---|---
1024×768 | 20 Pixel | *Karte* rückt 20 Pixel nach unten, etwa 3,4 *Zoll*
1100×800 | 20 Pixel | *Karte* rückt 20 Pixel nach unten, etwa 3,1 *Zoll*
1280×720, 1920×1080 | nichts | steht still

Die zweite Knopfzeile ist in diesen Fenstern halb abgeschnitten, 14080 sagt selbst: Man rollt, um sie ganz zu sehen. Fällt mit dem Knopf die zweite Zeile weg, gibt es nichts mehr zu rollen, und die Spalte springt zurück. Trotzdem sind alle 88 Tests grün.

**Kosten.** Das ist der Fall aus Anliegen 670: Wer übergangen hat, greift als Nächstes das *Modell* und greift daneben, um mehr als einen Kreis. Die Abnahme von Item ruhigeKarte belegte das Kriterium in zwei der vier Fenster nicht vollständig. Ein Test kostet wenig, die Vorlage steht schon da.

**Gegenvorschlag.** Ein Test neben `testQue7_1DieKarteBleibtStehenWennGemeinsamÜbergehenNebenDenÜbrigenKnöpfenAufhört`, gleicher Aufbau, in allen vier Fenstern: Vor dem Lesen von `davor` rollt er mit `seite.mouse.wheel` über der mittleren Spalte bis ans Ende, dann „gemeinsam übergehen“, dann derselbe Vergleich. In Fenstern ohne Überstand rollt nichts, der Fall bleibt gültig. Rot bis zur Änderung in [14461](14461-knopfzeileUnter1280RolltUndSpringt.md). Erledigt, wenn dieser Test mit den heutigen Maßen rot ist und mit 6rem aus 14461 grün.

Ohne Befund, damit du nichts suchst: Die sechs Fälle im Fenster 1920×1080 in `ziehenTest.py` und der eine Pixel in `testBew8_4DieSeiteSetztNachDemKlickAufGemeinsamÜbergehenAmPunkt` treffen ihre Kriterien (B5); was das kleinere Fenster für den Spieler heißt, fragt [14462](14462-karteBeiKleinemFenster.md). Die Gegenprobe zum fehlenden `scrollbar-gutter` stimmt: zwei Tests in zwei Fenstern.

**Stellungnahme.** Umgesetzt mit demselben Test wie [14481](14481-ruhigeKarteTestsRollenNicht.md), Einzelheiten dort: `testQue7_1NachDemRollenBleibtDieKarteStehenWennGemeinsamÜbergehenNebenDenÜbrigenKnöpfenAufhört`, direkt hinter der genannten Vorlage. Mit den heutigen Maßen rot bei 1024 und 1100, grün bei 1280 und 1920; an einer Kopie in `/tmp` mit 6rem unter 1280 Pixeln aus 14461 grün in allen vier Fenstern. Gerollt wird über den Knöpfen, also innerhalb der mittleren Spalte, um 500 Pixel und damit bis ans Ende.
