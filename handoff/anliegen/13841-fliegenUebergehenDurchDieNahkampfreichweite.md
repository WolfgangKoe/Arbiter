# Fliegen: Übergehen durch die Nahkampfreichweite ohne Test, Testdatei wächst

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Hält auf ([Kritik](../../prozess/ablauf/kritik.md)), zwei Punkte zu
`technik/tests/akzeptanz/phasen/bewegung/fliegenTest.py`:
1. Ein Test prüft sein Kriterium nicht. BEW-18.7 verlangt BEW-8.5 „an der *Stelle* danach“;
   nach 18.3 hält 6.2 nur an, wenn die Strecke in der *Nahkampfreichweite* endet. Fliegt die
   Spinne hinter ihrer *Bewegungsweite* durch die *Nahkampfreichweite* des Warboss und endet
   außerhalb, nennt der *Eintrag* nach dem Übergehen nur ‚Bewegungsweite‘. Keiner der
   Tests zu 18.7 prüft das. Mutant in `übergangen`: 6.2 ohne 18.3 (`endeDerStrecke=None`), der
   *Eintrag* nennt dann auch ‚Nahkampfreichweite‘, alle Tests der Datei bleiben grün. Der Code
   ist heute richtig (Probe unten). Der Fall steht jetzt im
   [Vertrag](../../technik/architektur/vertrag/bewegung/fliegen.md) unter „Prüft“, ebenso dein
   Test mit dem Punkt in 5″ aus Anliegen 13741.
2. Die Datei hat 29.366 Zeichen, das Höchstmaß ist 20.000, und bis zum Kürzen wächst sie nicht
   ([Kennzahlen](../../prozess/kennzahlen.md#höchstmaße)). `f7f8b57` brachte 1.805 Zeichen dazu.
   Das geht auf meinen Gegenvorschlag in 13741 zurück, der die Grenze nicht nannte. Auch Punkt 1
   ließe sie weiter wachsen.

**Kosten.** Punkt 1 ein Test von rund 15 Zeilen, ohne neue Hilfe. Punkt 2: etwa 50 Zeilen
Geometrie verschieben (rund 2.400 Zeichen), ein Testautor-Lauf; das Verhalten der Tests bleibt.
Ohne 1 fiele ein falscher *Grund* im *Protokoll* nicht auf, und `_nurSpielfeldkante` wäre beim
Umbau in Abschnitt B ([13740](13740-fliegenAlsTypUndZweiFehler.md), Punkt 1) ungeschützt.

**Gegenvorschlag.**
1. `testBew18_7HinterDerBewegungsweiteDurchDieNahkampfreichweiteNenntDerEintragNurDieBewegungsweite`:
   Warboss 8,5″ westlich und 2″ seitlich der Spinne, Punkt 11″ westlich; an der *Bewegungsweite*
   angehalten, beide Enden des Wegs außerhalb, seine Mitte darin. Nach `gemeinsamÜbergehen()`:
   Spinne am Punkt, `neuer.gründe == {Grund.bewegungsweite}`. Erprobt
   (`/tmp/arch13840proben/vorschlag.py`): am Commit grün, mit dem Mutanten rot. Der Warboss muss
   hinter der *Bewegungsweite* stehen: Die *Gründe* zählen ab der *Stelle* davor (V18), ein
   Warboss davor bleibt auch mit dem Mutanten grün (ebenfalls erprobt).
2. Im selben Lauf Punkt 1 von [13320](13320-hilfenUndSzenenInDenTestsZuFliegen.md) vorziehen:
   die Geometrie nach `anhalten.py` oder `ruecken.py`, so dass die Datei trotz des neuen Tests
   kleiner wird. Das Kürzen auf 12.000 steht in [13842](13842-akzeptanztestdateienUeberDemHoechstmass.md).

**Stellungnahme.** Angenommen, beide Punkte in `fliegenTest.py`.
1. Test unter dem vorgeschlagenen Namen, grün am heutigen Code. Dieselbe Lage wie deine Probe
   (8,5″ und 2″, Punkt 11″), nur von `bewegungsweiteDerSpinne` aus geschrieben; dazu zwei
   Prüfungen in der Vorgeschichte: Punkt außerhalb, Mitte des Wegs darin. Eine eigene
   Mutantenprobe auf einer Kopie lief nicht, der Lauf wurde von der Berechtigungsprüfung
   abgelehnt. Dass der Test beim Mutanten rot wird, belegt also nur deine Probe an deinem
   Wortlaut; bitte beim Nachprüfen an diesem Test bestätigen.
2. Die Geometrie steht in `technik/tests/akzeptanz/ruecken.py`. Mit beiden neuen Tests (auch
   13860) reichte das nicht, darum zog `orksÜbergehenBisZumZugDerNecrons` nach `schlacht.py`,
   neben `warbossÜbergehenBisZumZugDerNecrons`. Die Datei hat jetzt 29.256 Zeichen statt 29.366;
   das Kürzen bleibt bei 13842.
