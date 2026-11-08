# Überschrift von AUF-20 nach Einheiten- und Modellebene

Form: Kritik
Von: Planer
An: Anforderungsautor
Runde: 1/3
Status: offen
Wartet auf: Domänenphase 11

## Runde 1
**Befund.** Nach Anliegen 7800 F2 B unterscheidet die *Ebene* *Einheitenebene* und
*Modellebene*; Glossar und Kriterien von AUF-20 folgen dem (Commit 1523136). Die Überschrift
in [ebene.md](../../domaene/anforderungen/phasen/aufstellen/ebene.md) heißt noch
„AUF-20 · Ganze Einheit oder ein Modell“, ebenso der Zweck („die ganze *Einheit* verschiebt“).
Die Tests übernehmen die alte Wortwahl: der Kopf von `ebeneTest.py`, der Helfer
`ganzeEinheitAuswählen` und die Parameter `"ganzeEinheit"` und `"einModell"` in 13
Akzeptanztestdateien (etwa `technik/tests/akzeptanz/vorruecken.py:9`, `:20`). So stehen für
dieselbe Sache zwei Namen ([Wir 2](../../prozess/praemissen/wir.md)).

**Kosten.** Am Bildschirm nichts. Domäne: eine Überschrift und ein Satz; Kennung und Sinn
bleiben. Danach benennt der Testautor Kopf, Helfer und Parameter um (mechanisch, 13 Dateien);
das plane ich in Zyklus 11 ein. Ohne Änderung wächst die alte Wortwahl mit jedem neuen Test.

**Gegenvorschlag.** Überschrift „AUF-20 · Einheitenebene oder Modellebene“; den Zweck fasst
du im Wortlaut des Glossars. Den Testautor benachrichtige ich danach mit einem eigenen Anliegen.

**Stellungnahme.**
