# Klickpfad und Etappenziel im Review 8 unvollständig

Form: Kritik
Von: Fachkritiker
An: Reviewer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Hält auf (Ich 3: ein Schritt des Happy Path aus Plan 8 fehlt im Klickpfad;
[Technikphase](../../prozess/ablauf/technikphase.md), Schritt 6: „nur, was in diesem Zyklus
neu oder anders machbar ist“, mit dem erwarteten Bild je Schritt).
1. Korrigieren fehlt (Plan 8, Schritt 3: „korrigiert sie nach Belieben“; BEW-1.6). Schritt 5
   zeigt nur einen Zug. Nicht zu sehen ist, dass die *Distanz* von der *Stelle* zu Beginn der
   *Bewegungsphase* zählt, nicht je Zug: Den Warboss 3″ ziehen, loslassen, wieder 3″ weiter:
   Er hält 5″ vom Ausgangspunkt an. Und: erst die Boyz ziehen, dann den Warboss noch einmal,
   das geht.
2. Andere *Phasen* sind leer (Plan 8, Schritt 2; QUE-10.5) ist neu, steht aber nicht da: In
   der Kommandophase ein *Modell* ziehen und loslassen, es steht wieder, wo es war, ohne
   *Grund*.
3. Erwartetes Bild fehlt. Schritt 3: Woran sieht man den *Spieler* *am Zug* (QUE-10.1)? Die
   Anzeige steht auf seiner Seite der Kopfzeile (`technik/frontend/zeichnen.js:28`).
   Schritt 10: Was zeigt Arbiter, wenn die *Schlacht* endet (QUE-10.4, Plan 8, Schritt 4)? Die
   Kopfzeile zeigt „Schlacht beendet“ (`technik/frontend/index.html:14`).
4. *Nahkampfreichweite*: Plan 8 nennt sie unter „Noch nicht“, Arbiter sperrt sie in der
   *Bewegungsphase* aber schon, ohne Test ([Anliegen 6241](6241-bewegungOhneTestZuQue1_3UndAuf8_7.md)).
   Der Review sagt das nicht. Unter „Etappenziel“ fehlt sie, obwohl der Satz verspricht, alles
   aus „Noch nicht“ von Plan 8 aufzuzählen. Im Zyklusziel fehlen sie und „Loslassen neben der
   *Karte*“ ganz: weder in Plan 9 noch unter „Noch nicht“
   ([Etappe 2](../../domaene/etappen/02-bewegen.md): „sperrt … in Nahkampfreichweite“).

**Kosten.** Der Stakeholder beurteilt am Bildschirm das Korrigieren und die leeren *Phasen*
nicht, obwohl beides neu ist. Ihn überrascht eine *Sperre* ‚Nahkampfreichweite‘, die kein
Plan angekündigt hat. Plan 9 kann zwei Punkte der Etappe verlieren. Nachbessern kostet ein
paar Zeilen im Review.

**Gegenvorschlag.** Im Klickpfad zwei Schritte nach Schritt 5 (1 und 2 oben) mit erwartetem
Bild; in Schritt 3 „bei Spieler 1“, in Schritt 10 „Die Kopfzeile zeigt ‚Schlacht beendet‘“.
Ein Satz unter dem Klickpfad: Arbiter sperrt ‚Nahkampfreichweite‘ beim Ziehen schon, ein Test
folgt (6241). Unter „Etappenziel“ steht *Nahkampfreichweite* als „sperrt schon, ohne Test“.
Das Zyklusziel nennt sie und „Loslassen neben der *Karte*“ entweder in Plan 9 oder unter
„Noch nicht“.

**Stellungnahme.** Angenommen, alle vier in [Review 8](../review.md) nachgebessert. 1: neue
Schritte 6 (3″ und 3″ hält 5″ vom Ausgangspunkt) und 8 (Warboss nach den Boyz noch einmal);
2: neuer Schritt 4 (Kommandophase, steht wieder, ohne *Grund*); 3: Schritt 3 „auf seiner
Seite der Kopfzeile, links“, Schritt 12 „Schlacht beendet“, „Phase beenden“ fort; 4: Satz
unter dem Klickpfad, *Nahkampfreichweite* im Etappenziel, im Zyklusziel in Plan 9 (Test aus
6241), Loslassen neben der *Karte* unter „Noch nicht“. Am laufenden Arbiter durchgegangen
(Skript `/tmp/review8b/rundgang.py`): Kommandophase Warboss unverändert, kein *Grund*; 3″
dann 4,993″ vom Ausgangspunkt; Boyz je 2″; Warboss danach frei gesetzt; nach 68 Mal „Phase
beenden“ „Schlacht beendet“, kein Knopf. Schritt 12 ist damit gesehen, nicht nur im Test.
