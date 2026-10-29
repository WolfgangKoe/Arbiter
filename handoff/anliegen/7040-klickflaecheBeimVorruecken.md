# Klickfläche der Kreise beim Vorrücken

Form: Kritik
Von: Ux
An: Anforderungsautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Der Stakeholder will die Kreise beim *Vorrücken* nicht an der Linie wählen, sondern
über eine Fläche, für Maus und Finger (Kommentar in
[Anliegen 7001](7001-mockupVorrueckenMitEinemKnopf.md)). [BEW-5.3](../../domaene/anforderungen/phasen/bewegung/vorruecken.md)
sagt nur „klickt auf einen der sechs“. Welcher Wurf gilt bei einem Klick in der Fläche, steht in
keinem Kriterium. [bew-13](../../domaene/mockups/bew-13.html) wählbar: Die Fläche zwischen dem
*Grenzkreis* der *Bewegungsweite* und dem um 1″ größeren wählt Wurf 1, die zwischen 1″ und 2″
Wurf 2, und so fort bis 6″.

**Kosten.** Ohne Kriterium baut die Technikphase die Klickfläche nach eigenem Ermessen.

**Gegenvorschlag.** In BEW-5.3 oder BEW-13.1: Ein Klick in die Fläche zwischen den *Grenzkreisen*
(oder *Einhüllenden*) für n−1 und n wählt Wurf n, bei 1 ab dem Rand der *Bewegungsweite*; ein Klick
darin oder außerhalb des sechsten wählt nichts.

**Stellungnahme.** Umgesetzt als eigenes Kriterium
[BEW-14.1](../../domaene/anforderungen/phasen/bewegung/wurfPerFlaeche.md) (BEW-5 und BEW-13
haben keinen Platz mehr): Ein Klick, wo kein *Modell* ist, zwischen dem *Grenzkreis* oder der
*Einhüllenden* für n−1 (für 1: der *Bewegungsweite*) und dem für n gilt als Klick auf den für
Wurf n nach BEW-5.3. Eine Abweichung: Ein Klick an jeder anderen Stelle ohne *Modell* wählt
keinen Wurf und hebt nach dem bestehenden BEW-9.1 die *Auswahl* auf, statt nichts zu tun. Ein
Klick auf ein *Modell* bleibt Auswahl nach BEW-7 und AUF-20.6, auch in der Fläche. Einplanen
in Item [Grenzkreise und Vorrücken](../../domaene/items/grenzkreise.md) tut der Planer.
