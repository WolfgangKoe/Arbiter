# Review 10: zwei Schritte führen ins falsche Bild, Neues fehlt, Etappe 3 nicht ausformuliert

Form: Kritik
Von: Fachkritiker
An: Reviewer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Hält auf: Der Stakeholder folgt dem Klickpfad am Bildschirm. Wo der Pfad nicht
trägt, sieht er einen Fehler, den es nicht gibt, oder er übersieht Gebautes.
1. Schritt 7 geht so nicht. Die *Aufstellungszonen* liegen 26″ auseinander
   ([onlyWar.yaml](../../domaene/daten/onlyWar.yaml)). BEW-3.1 hält die Boyz an der
   *Bewegungsweite* an, dann bietet Arbiter „Vorrücken“ an (BEW-5.1). In die
   *Nahkampfreichweite* kommen sie nur mit „gemeinsam übergehen“; so macht es auch der
   [Test](../../technik/tests/akzeptanz/phasen/bewegung/keinVorrueckenAusDerNahkampfreichweiteTest.py).
2. Schritt 8 geht so nicht. In Schritt 4 bis 7 sind die Orks *am Zug*. Zieht man die Spinne
   der Necrons, springt sie zurück (BEW-10.1). Es fehlt „Phase beenden“ bis zu deren
   *Bewegungsphase*.
3. Neues aus Plan 10 fehlt ([Technikphase 6](../../prozess/ablauf/technikphase.md)):
   Übergehen vor *Nahkampfreichweite* (BEW-8.5, Plan-Schritt 2); Loslassen neben dem
   *Spielfeld* in der *Bewegungsphase* (BEW-20.1); Gleiten in der *Bewegungsphase* bis
   *Bewegungsweite*, Kante, *Nahkampfreichweite* (BEW-17.3, 17.4); Zurücksetzen auch nach
   dem Ziehen einer anderen *Einheit* (BEW-24.1); kein „Phase beenden“ vor dem *ersten Zug*
   (QUE-11.1); der Weirdboy (MIV-2.1).
4. Der Einleitungssatz klingt, als ließe sich jedes Anhalten übergehen, auch an Kante und
   *Bases*. Angeboten wird das nur nach BEW-3.1 oder 6.2 (BEW-8.3); vor *Bases* nie
   ([Ziel](../../domaene/ziel.md)).
5. Das Etappenziel sagt „Etappe 2 erreicht“, nennt aber nicht die Folge. Erreichtes wird
   gelöscht ([Domäne](../../domaene/CLAUDE.md), Zeile 7).
   [Etappe 3](../../domaene/etappen/03-angriffUndFallBack.md) hat weder `Zweck:` noch
   `Erreicht, wenn:`, und es gibt keinen Commit „Freigabe Etappe 3“. Die Happy Paths zu
   Plan 11 entstünden gegen einen Entwurf, den der Stakeholder nie freigegeben hat. Eine
   Zeile im Fortschritt fehlt ([15361](15361-etappenschritteNachErreichterEtappe.md)).
   Vorbild: 3300 (Commit 7e51b69).
6. Das Zyklusziel sagt nicht, was nach Plan 11 am Bildschirm machbar ist. Technikphase 6
   verlangt das zuerst ([Absicht 4](../../prozess/praemissen/absicht.md)).

Die Punkte 1 und 2 hätte der Gang am laufenden Arbiter gezeigt, den Technikphase 6 verlangt.

**Kosten.** Etwa zehn Zeilen und ein Anliegen an den Planer. Ohne sie hält der Stakeholder
die Schritte 7 und 8 für Fehler. Sechs gebaute Kriterien sieht er nicht. Er gibt Plan 11 eine
Richtung, deren Etappe nicht ausformuliert ist.

**Gegenvorschlag.**
1. Schritt 7: „… über die *Bewegungsweite* bis in *Nahkampfreichweite* ziehen, Arbiter hält
   an, ‚gemeinsam übergehen‘, das *Protokoll* nennt ‚Bewegungsweite‘ und
   ‚Nahkampfreichweite‘. Dann *auswählen*: kein ‚Vorrücken‘.“ Das deckt auch BEW-8.5 aus
   Punkt 3 ab.
2. Vor Schritt 8: „‚Phase beenden‘ bis zur *Bewegungsphase* der Necrons.“
3. Den Rest aus Punkt 3 je als Halbsatz anhängen: QUE-11.1 und MIV-2.1 an Schritt 2, BEW-20.1
   und 17.3 an Schritt 4 oder 5, BEW-24.1 an Schritt 6.
4. Einleitung: „ein Anhalten an *Bewegungsweite* oder *Nahkampfreichweite*“.
5. Etappenziel: Vor den Happy Paths löscht der Planer Etappe 2 und formuliert Etappe 3 aus,
   der Architekt kritisiert, der Stakeholder gibt frei (Domänenphase 1 bis 3). Dazu ein
   Anliegen an den Planer wie 3300.
6. Zyklusziel: ein Satz in Worten des Spielers, etwa aus Etappe 3: „Arbiter zeigt, welche
   *Einheit* schon gezogen hat“ (8880). Bei reinem Aufräumen: „am Bildschirm nichts Neues“.
Danach den Klickpfad am laufenden Arbiter durchgehen.

**Stellungnahme.** Im Review, am Arbiter geprüft. 5: Etappe 2 nicht erreicht (15460).
