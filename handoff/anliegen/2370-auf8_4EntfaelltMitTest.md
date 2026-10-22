# AUF-8.4 entfällt mit Test, Ablage heißt im Code Armeeliste

Form: Kritik
Von: Anforderungsautor
An: Planer
Runde: 1/3
Status: offen

## Runde 1
**Befund.** Zwei Folgen aus Antworten des Stakeholders fehlen in den Items:
1. [AUF-8.4](../../domaene/anforderungen/phasen/aufstellen/ziehen.md) (ein Boy einer
   *aufgestellten* *Einheit*, auf die *Armeeliste* gezogen: ‚nicht wählbar‘) widerspricht
   2220 F4 A: Die Spalte ist kein Ziel zum Hineinziehen mehr (Kritik in
   [2312](2312-auf8_4AblageAlsZiel.md)). AUF-8.4 ist getestet; lösche ich es jetzt, wird die
   Rückverfolgung rot. Mit ihm fallen die zwei Fälle `auf8_4…` im Test zu AUF-12.5, und
   AUF-16.8 heißt dann „neben der *Karte*, auch auf einer *Armeeliste*“.
2. Nach 2221 F1 A heißt *Ablage* in Glossar und Anforderungen jetzt *Armeeliste*. Im Code und in
   den Tests steht noch „Ablage“, etwa `modellAufAblageLoslassen` und Testnamen in
   `ziehenTest.py` ([Wir 2](../../prozess/praemissen/wir.md)).

**Kosten.** Ohne Item bleibt ein Kriterium stehen, das eine Geste meldet, die es nicht mehr
gibt, und Code und Glossar sprechen verschieden.

**Gegenvorschlag.**
1. Item [loslassenNebenDerKarte](../../domaene/items/loslassenNebenDerKarte.md), das AUF-16.8
   ohnehin baut, nennt „Entfällt mit Test: AUF-8.4“. Nach der Freigabe seines Plans lösche ich
   AUF-8.4, nehme 8.4 aus AUF-12.5 und dem Zweck von AUF-12 und fasse AUF-16.8 wie oben, im
   selben Schritt, in dem der Testautor die Tests löscht (Vorgehen wie Anliegen 801).
2. Ein Item in Plan 7, wohl [aufraeumenUndFesteAdresse](../../domaene/items/aufraeumenUndFesteAdresse.md),
   nennt „Ablage → Armeeliste in Code und Tests, Verhalten unverändert“.

Erledigt, wenn die Items das nennen oder du begründest, warum anders.

**Stellungnahme.**
