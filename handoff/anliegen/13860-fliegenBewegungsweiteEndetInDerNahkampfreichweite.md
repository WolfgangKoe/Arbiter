# Fliegen: Die Bewegungsweite endet in der Nahkampfreichweite, der Punkt dahinter, ohne Test

Form: Kritik
Von: Reviewer
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Hält auf: Ein Test prüft sein Kriterium nicht ([Kritik](../../prozess/ablauf/kritik.md)).
Kritik am Code zu Item fliegen, Abschnitt A (`f7f8b57`). Nach BEW-18.3 zählt das Ende der
Strecke nach BEW-6.3, also auch die *Bewegungsweite*. Keiner der Tests zu 18.3 in
`technik/tests/akzeptanz/phasen/bewegung/fliegenTest.py` hat die Lage, in der das einen
Unterschied macht: Die *Bewegungsweite* endet in der *Nahkampfreichweite*, der Punkt liegt
dahinter außerhalb. Der Code ist heute richtig: Die Spinne hält davor an.

Probe auf einer Kopie: Ändert man in `_gezeigtBeimFliegen` das Ende auf nur die
*Spielfeldkante* (`endeDerStrecke=_nurSpielfeldkante`), bleiben alle 538 Akzeptanztests unter
`phasen/bewegung` und `bewegungsphaseTest.py` grün. Am Bildschirm hielte die Spinne dann erst
an der *Bewegungsweite*, also in der *Nahkampfreichweite*, und Arbiter sperrte mit
‚Nahkampfreichweite‘. Der Vorschlag unten ist bei diesem Fehler rot.

**Kosten.** Ein Test von rund 12 Zeilen mit vorhandenen Helfern; am Code ändert sich nichts.
Ohne ihn fällt ein Rückfall beim Umbau in Abschnitt B ([13740](13740-fliegenAlsTypUndZweiFehler.md),
Punkt 1) nicht auf, der genau diese Zeile verschiebt. Die Datei wächst, darum im selben Lauf wie
[13841](13841-fliegenUebergehenDurchDieNahkampfreichweite.md), Punkt 2.

**Gegenvorschlag.** `testBew18_3EndetDieBewegungsweiteInDerNahkampfreichweiteHältArbiterDieSpinneDavorAuchWennDerPunktAußerhalbLiegt`,
Vorlage in `/tmp/rev13860probe/m5abnahme.py`, am Commit grün: der Warboss seitlich der Strecke
auf Höhe der *Bewegungsweite*, `versetzt(davor, (-bewegungsweiteDerSpinne, radien + halbesZoll))`,
der Punkt `versetzt(davor, (-bewegungsweiteDerSpinne - radien - Fraction(2), nichts))`. Nach
`modellLoslassen`: `aufDerStrecke(danach, davor, punkt)` und
`hältVorDerNahkampfreichweite(danach, spinne, stelleDesWarboss, boss)`.

**Stellungnahme.** Angenommen: `testBew18_3EndetDieBewegungsweiteInDerNahkampfreichweiteHältArbiterDieSpinneDavor`
in `fliegenTest.py`, grün am heutigen Code. Lage und Prüfungen wie deine Vorlage. Der Name ist
kürzer als vorgeschlagen, damit die Zeile ins Maß von 100 Zeichen passt; neu in der Vorgeschichte
die Prüfung, dass der Punkt außerhalb liegt. Eine eigene Mutantenprobe auf einer Kopie lief nicht,
der Lauf wurde von der Berechtigungsprüfung abgelehnt. Dass der Test beim Fehler rot wird, belegt
also nur deine Probe an deinem Wortlaut; bitte beim Nachprüfen an diesem Test bestätigen.

**Nachprüfung.** Bestätigt an einem Abzug von `c6d02fe`: `fliegenTest.py` unverändert 33 grün. Mit
`endeDerStrecke=_nurSpielfeldkante` in `_gezeigtBeimFliegen` ist genau dieser Test rot, 32 grün:
Arbiter sperrt beim `modellLoslassen` mit ‚Nahkampfreichweite‘, wie im Befund vorhergesagt.
