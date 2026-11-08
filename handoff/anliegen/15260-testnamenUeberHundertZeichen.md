# Testnamen über 100 Zeichen und doppelt belegte ids

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: offen
Wartet auf: Technikphase 11

## Runde 1
**Befund.** Kritik am Umbenennen nach Anliegen 7800 (Commit 1523136),
Schnittstelle und Lesbarkeit der Akzeptanztests. Nichts hält auf: ruff, Benennung, Glossar,
Kommentare und Importvertrag sind grün; Fachbegriffe folgen dem [Glossar](../../domaene/glossar.md).
1. Sechs Testnamen tragen `# noqa: E501`, die ersten `noqa` unter `technik/` überhaupt
   (Review 9: „Kein `noqa`“). [Es 8](../../prozess/praemissen/es.md) erlaubt den Kommentar,
   darum wartet es; aber `noqa` ist für Fälle, in denen das Werkzeug irrt, und hier lässt sich
   jeder Name kürzen, ohne die Aussage zu verlieren:
   - [modellPerKlickTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/modellPerKlickTest.py):
     `testAuf25_1EinKlickAufEinModellOhneModellebeneSendetEinPutUndDieEbeneIstSeineModellebene`,
     `testAuf25_2EinKlickAufDasModellDerModellebeneSendetEinPutUndDieEbeneIstDieEinheitenebene`
     (je 93 Zeichen mit `def` und Klammer).
   - [normaleBewegungTest.py](../../technik/tests/akzeptanz/phasen/bewegung/normaleBewegungTest.py):
     `…OhneSperrmeldung` → `…OhneSperre`, wie die beiden Tests darüber.
   - [auswahlTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/auswahlTest.py) Auf5_7:
     `ImBeispielDesVertrags` → `ImVertragsbeispiel`.
   - [ruhigesSpielfeldTest.py](../../technik/tests/akzeptanz/querschnitt/ruhigesSpielfeldTest.py):
     `WennKeinSpielerAnDerReiheIst` → `WennKeinerAnDerReiheIst`;
     `NebenDenÜbrigenKnöpfen` → `NebenDenKnöpfen`, falls QUE-7.1 das trägt.
2. Die id `einModell` heißt zweierlei: in [ziehen.py](../../technik/tests/akzeptanz/ziehen.py)
   (`alleinUndMitEinheitenebene`) ein *Modell* ohne *Auswahl*, in
   [vorruecken.py](../../technik/tests/akzeptanz/vorruecken.py) (`ebenen`) die *Modellebene*;
   dort heißt die andere `ganzeEinheit`, in ziehen.py `einheitenebene`,
   in [anhalten.py](../../technik/tests/akzeptanz/anhalten.py) die *Modellebene* `modellebene`.
   Liest man im Testlauf `[einModell]`, weiß man nicht, welcher Fall rot ist.

**Kosten.** Sechs Namen und zwei ids, mechanisch, ohne Folge für Code oder Vertrag. Ohne die
Änderung bleiben sechs Ausnahmen von der Zeilenlänge, die nächste Umbenennung fügt weitere hinzu.

**Gegenvorschlag.** In Technikphase 11 die Namen nach 1 kürzen, die `noqa` entfernen; in
`vorruecken.py` die ids `einheitenebene` und `modellebene`, in `ziehen.py` statt `einModell`
`ohneAuswahl`.

**Stellungnahme.**
