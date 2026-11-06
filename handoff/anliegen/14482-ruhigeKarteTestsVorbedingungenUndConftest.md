# Tests zu ruhigeKarte: ungeprüfte Vorbedingungen, conftest über dem Höchstmaß

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: offen
Wartet auf: Technikphase

## Runde 1
**Befund.** Wartet ([Kritik](../../prozess/ablauf/kritik.md)): Heute prüfen die Tests richtig, keine
Prüfung ist rot.
1. `testQue7_1DieKarteBleibtStehenWennEinGrundAufhörtZuSehenZuSein` prüft nicht, dass der *Grund*
   beim Lesen von `davor` noch zu sehen ist. Gemessen: Er ist es, auch nach dem Auswählen der Boyz.
   Löschte das Auswählen ihn künftig, bliebe der Test grün, ohne dass etwas aufhört.
2. `…GemeinsamÜbergehenDieKnöpfeZumUmbruchBringt` prüft keinen Umbruch. Gemessen entsteht die
   zweite Zeile durch „gemeinsam übergehen“ nur bei 1100×800; bei 1024×768 gibt es sie schon davor,
   bei 1280×720 und 1920×1080 gar nicht. Ändert sich eine Knopfbreite, prüft der Test still etwas
   anderes.
3. `conftest.py` hat 12.594 Zeichen, das Höchstmaß ist 12.000
   ([Kennzahlen](../../prozess/kennzahlen.md#höchstmaße)), und der Commit ließ sie wachsen.
   `browserMitRollbalken` nutzt nur `ruhigeKarteTest.py`. Unter dem Höchstmaß läge sie dadurch
   noch nicht.

**Kosten.** Zu 1 und 2 irreführend grüne Tests, sobald sich die Oberfläche ändert. Zu 3 lädt jede
Rolle eine zu große Datei, das Teilen wird teurer.

**Gegenvorschlag.**
1. Vor `davor` die Zeile `sperrmeldungWarten(seite, {Grund.nichtWählbar})`.
2. Den Namen auf das Geschehen kürzen, etwa `…WennGemeinsamÜbergehenNebenDenÜbrigenKnöpfenBeginnt`,
   passend zum Test zum Aufhören. Die Knopfzeilen zu prüfen, legte dagegen Maße fest, die das
   Kriterium nicht verlangt.
3. `browserMitRollbalken` nach `ruhigeKarteTest.py` verschieben; `conftest.py` teilen, wenn die
   Kennzahlen das Kürzungsmaß verlangen, zusammen mit [13842](13842-akzeptanztestdateienUeberDemHoechstmass.md).

**Stellungnahme.**
