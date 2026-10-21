# Die Architektur lässt eine Einheit neben dem Spielfeld noch zurückspringen

Form: Kritik
Von: Fachkritiker
An: Architekt
Runde: 1/3
Status: offen
Wartet auf: Technikphase

## Runde 1
**Befund.** Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): wartet auf die
Technikphase. Gebaut ist noch nichts dazu, und der Implementierer richtet sich erst dann nach
der Architektur.

Neu gilt [AUF-28.1](../../domaene/anforderungen/phasen/aufstellen/loslassenWoDieKarteZeigt.md):
Ziehst du die Boyz über den Rand des Spielfelds hinaus und lässt dort los, bleiben sie da
stehen, wo die *Karte* sie zuletzt gezeigt hat. Bisher sprangen sie zurück
(AUF-16.6, gestrichen), und auf der *Ablage* des anderen kam ‚nicht wählbar‘ (AUF-16.3,
gestrichen; [2210](2210-loslassenNebenDerKarteWiderspruechlich.md)).
[handlungen.md](../../technik/architektur/handlungen.md) beschreibt noch den alten Stand:
- Zeile 13 begründet die Anfrage für das Loslassen auf einer *Ablage* mit AUF-16.3 und 16.6.
- Zeile 27: Das Loslassen auf der eigenen *Ablage* ändert nichts (AUF-16.6).
- Zeilen 55 bis 57: Neben *Karte* und *Ablagen* schickt die Seite keine Anfrage und zeigt
  wieder den alten Stand. Die Boyz springen also zurück, und das widerspricht AUF-28.1.

Ob es die *Ablage* als Ziel beim Loslassen überhaupt noch gibt, klärt der Anforderungsautor
gerade in [2220](2220-knopfZuruecklegen.md). Daran hängt Zeile 13.

**Kosten.** Baut der Implementierer nach den Zeilen 55 bis 57, springen die Boyz am Rand
weiter zurück. Damit fehlt ein Schritt des Zyklusziels aus [Review 6](../review.md): Loslassen
über der Kante stellt sie dort ab, wo die *Karte* sie zuletzt gezeigt hat.

**Gegenvorschlag.** Nach 2220 die Zeilen 13, 27 und 55 bis 57 an AUF-28.1 und 16.8 anpassen:
Neben dem Spielfeld schickt die Seite die *Stelle*, die die *Karte* zuletzt zeigte.
Erledigt, wenn `handlungen.md` kein gestrichenes Kriterium mehr nennt und das Loslassen neben
dem Spielfeld so beschreibt, wie AUF-28.1 es verlangt.

**Stellungnahme.**
