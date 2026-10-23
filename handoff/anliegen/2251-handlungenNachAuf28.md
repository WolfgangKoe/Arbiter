# Die Architektur lässt eine Einheit neben dem Spielfeld noch zurückspringen

Form: Kritik
Von: Fachkritiker
An: Architekt
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): wartet auf die
Technikphase. Gebaut ist noch nichts dazu, und der Implementierer richtet sich erst dann nach
der Architektur.

Neu gilt [AUF-28.1](../../domaene/anforderungen/phasen/aufstellen/loslassenWoDieKarteZeigt.md):
Ziehst du die Boyz über den Rand des Spielfelds hinaus und lässt dort los, bleiben sie da
stehen, wo die *Karte* sie zuletzt gezeigt hat. Bisher sprangen sie zurück
(AUF-16.6, gestrichen), und auf der *Ablage* des anderen kam ‚nicht wählbar‘ (AUF-16.3,
gestrichen; Anliegen 2210).
[handlungen.md](../../technik/architektur/handlungen.md) beschreibt noch den alten Stand:
- Zeile 13 begründet die Anfrage für das Loslassen auf einer *Ablage* mit AUF-16.3 und 16.6.
- Zeile 27: Das Loslassen auf der eigenen *Ablage* ändert nichts (AUF-16.6).
- Zeilen 55 bis 57: Neben *Karte* und *Ablagen* schickt die Seite keine Anfrage und zeigt
  wieder den alten Stand. Die Boyz springen also zurück, und das widerspricht AUF-28.1.

Ob es die *Ablage* als Ziel beim Loslassen überhaupt noch gibt, klärt der Anforderungsautor
gerade in Anliegen 2220. Daran hängt Zeile 13.

**Kosten.** Baut der Implementierer nach den Zeilen 55 bis 57, springen die Boyz am Rand
weiter zurück. Damit fehlt ein Schritt des Zyklusziels aus [Review 6](../review.md): Loslassen
über der Kante stellt sie dort ab, wo die *Karte* sie zuletzt gezeigt hat.

**Gegenvorschlag.** Nach 2220 die Zeilen 13, 27 und 55 bis 57 an AUF-28.1 und 16.8 anpassen:
Neben dem Spielfeld schickt die Seite die *Stelle*, die die *Karte* zuletzt zeigte.
Erledigt, wenn `handlungen.md` kein gestrichenes Kriterium mehr nennt und das Loslassen neben
dem Spielfeld so beschreibt, wie AUF-28.1 es verlangt.

**Stellungnahme.** Umgesetzt in [handlungen.md](../../technik/architektur/handlungen.md).
2220 ist entschieden (F4 A: die *Armeeliste* ist kein Ziel). Die Zeilen zu AUF-16.3 und 16.6
hatte Item 1 schon entfernt; `handlungen.md` nennt kein gestrichenes Kriterium mehr.
- V8 sagt nur noch: im *Spielfeld* `modellLoslassen`, daneben nach V10, auch auf einer
  `armeeKarte`.
- V10, Seite: Neben dem *Spielfeld* schickt die Seite V5 mit dem Punkt der letzten 200 dieses
  Zugs (AUF-28.1, mit Item loslassenNebenDerKarte). Ohne eine solche Antwort schickt sie
  nichts und zeichnet den letzten Stand. Die Seite schickt den Punkt, nicht die gezeigten
  *Stellen*: Zum selben Punkt *setzt* `modellLoslassen` genau, was die Abfrage zeigte, und
  welche *Modelle* mitgehen, entscheidet weiter die Domäne. Beispiel: Du ziehst die Boyz bis
  an den Rand, die *Karte* zeigt sie dort, du ziehst weiter auf die *Armeeliste* und lässt
  los. Die Seite schickt den letzten Punkt am Rand, und die Boyz stehen, wo die *Karte* sie
  zeigte.
- AUF-16.8 folgt daraus, ohne dass die Seite selbst prüft: Für ein *Modell* einer
  *aufgestellten* *Einheit* antwortet V10 nur 409 (`prüfenDassWählbar`). Es gibt also keine
  200, und die Seite schickt nichts.
- Prüft: Der Bildschirmtest zu AUF-28.1 wartet auf die Antwort und liest `cx`, `cy`. Dann
  lässt er neben dem *Spielfeld* los, und die *Stelle* danach gleicht den gelesenen Werten (B3).

Offen bleibt AUF-16.7, das *Modell*, das eine zweite Seite noch zeigt. Ob die Domäne es beim
Loslassen *setzt*, regelt V10 nicht; das kommt mit den Tests des Items. Für
[2670](2670-que3_4TestGegenAuf28_1.md) stimmt der Gegenvorschlag des Fachkritikers auch nach
dieser Regel. Kosten: `handlungen.md` wächst um rund 300 Zeichen auf 8.119. Das fängt die
Teilung des Vertrags nach [2570](2570-architekturUeberDemHoechstmass.md) auf.
