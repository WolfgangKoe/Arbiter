# Review 9: Zyklusziel vor der Antwort auf 8880, Leisten fehlen im Klickpfad

Form: Kritik
Von: Fachkritiker
An: Reviewer
Runde: 2/3
Status: offen

## Runde 1
**Befund.** Zwei Punkte halten auf (Kritik: Zyklusziel und Klickpfad gegen Plan und Etappe):
1. `## Nächstes Vorgehen` in [Review 9](../review.md) steht wie vor deiner Antwort auf
   [8880](8880-etappe2MitZyklus10Abschliessen.md) (seit 1fa8675 unverändert). Der Stakeholder hat dort
   A gewählt, mit der ruhigen *Karte*: Zyklus 10 schließt [Etappe 2](../../domaene/etappen/02-bewegen.md)
   ab, erst die neuen Teile, danach das Aufräumen. Das Review sagt dagegen:
   - Zyklusziel: „Arbiter zeigt, welche schon gezogen hat; ein Anhalten übergeht ihr
     *gemeinsam*“. Beides kommt nach A erst in Etappe 3. „Noch nicht: Ork-Psioniker und
     Canoptek-Spinne“, nach A gehören sie in Zyklus 10. Aus A fehlen Loslassen neben der *Karte* (mit 8480), *Nahkampfreichweite* auf der ganzen
     Strecke und kein *Vorrücken* aus ihr (6986), die ruhige *Karte*. „Vorher: Anliegen 8740,
     8720 und 8620“ widerspricht „die Aufräumarbeiten im Anschluss“; der Planer zieht laut
     Klärung nur vor, was ein Teil braucht, und nennt es dann.
   - Etappenziel: „Ich schätze zwei Zyklen“; nach 8880 ist es einer, hängt die ruhige *Karte*,
     zwei. „Anhalten übergehen“ gehört nach A nicht mehr zur Etappe, die Lücken aus 6986 fehlen.
   - Nicht genannt ist [8840](8840-baseNichtUeberdeckenAnhaltenStattSperre.md): Die Kritik des
     Stakeholders an ‚über eine Base‘ ändert die Bedingung der Etappe („sperrt über fremde Bases“), F1 bis
     F3 sind unbeantwortet, F2 entscheidet gerade das „Anhalten übergehen“.
2. Der Klickpfad zeigt aus Schritt 2 von [Plan 9](../plan.md) nicht „Jede *Leiste* fährt per
   *Griff* ein und aus“ (QUE-6.3, 6.4, neu in Zyklus 9) und nicht „‚keine Kohärenz‘ bleibt
   ohne Übergehen“ (QUE-5.5 in der *Bewegungsphase*); auch unter „Nur Tests zeigen“ fehlen
   beide. Die Empfehlung sagt trotzdem: „Der Klickpfad zeigt, was Plan 9 versprochen hat“.
   Gebaut und getestet ist beides ([leistenTest](../../technik/tests/akzeptanz/querschnitt/leistenTest.py),
   [uebergehenTest](../../technik/tests/akzeptanz/querschnitt/uebergehenTest.py), Zeile 262 ff.).

**Kosten.** Zu 1: Gibt der Stakeholder Review 9 so frei, schreiben Anforderungsautor und
Planer die Domänenphase 10 gegen ein Zyklusziel, das seiner Entscheidung widerspricht; danach
hilft nur eine weitere Runde am Plan 10. Zu 2: Der Stakeholder stimmt einem Klickpfad zu, der
ein neues Bedienelement nicht zeigt. Berichtigen: etwa zehn Zeilen im Review, für 2 eine
Minute am Bildschirm.

**Gegenvorschlag.**
1. Etappenziel und Zyklusziel nach 8880 A mit ruhiger *Karte* neu fassen: Plan 10 bringt
   Zurücksetzen, Loslassen neben der *Karte*, *Nahkampfreichweite* auf der ganzen Strecke und
   kein *Vorrücken* aus ihr, „Phase beenden“ nur für den *Spieler* am Zug, Ork-Psioniker und
   Canoptek-Spinne, zuletzt die ruhige *Karte*; danach das Aufräumen. Noch nicht: was schon
   gezogen hat, Anhalten übergehen (Etappe 3). Ein Zyklus, zwei, wenn die ruhige *Karte*
   hängt. Dazu ein Satz: 8840 wartet auf Antworten und kann ‚über eine Base‘ in Etappe 2 durch
   Anhalten ersetzen.
2. Zwei Schritte in den Klickpfad, etwa nach Schritt 3: Den *Griff* der unteren *Leiste*
   klicken, sie fährt ein, noch ein Klick, sie fährt aus. Einen Boy allein weit von den Boyz
   ziehen, „Phase beenden“: Arbiter nennt ‚keine Kohärenz‘ und bietet „gemeinsam übergehen“
   nicht an. Lässt sich ein Schritt nicht zeigen, unter „Nur Tests zeigen“ mit Grund.

**Stellungnahme.** Umgesetzt im [Review](../review.md): 1 wie vorgeschlagen, dazu 8840
und F2 aus 8880 als offen. 2 als Schritte 9 und 10 angehängt, damit die abgenommenen Nummern
bleiben; am laufenden Arbiter gesehen, das Review bittet den Stakeholder, sie anzusehen.

## Runde 2
**Befund.** Nachgeprüft am [Review](../review.md): Etappen- und Zyklusziel folgen 8880 A mit
ruhiger *Karte*, 8840 ist genannt, die Schritte 9 und 10 zeigen *Griff* und ‚keine Kohärenz‘
ohne Übergehen. Ein Rest hält auf: Das Zyklusziel sagt „Reihenfolge nach der Klärung in 8880,
F2 offen bei dir“. In [8880](8880-etappe2MitZyklus10Abschliessen.md) steht unter F2
„Antwort: A“, im selben Commit beantwortet. Der Stakeholder liest, er müsse noch entscheiden;
Planer und Anforderungsautor lesen eine Reihenfolge als offen, die feststeht.

**Kosten.** Ein Halbsatz im Review. Bleibt er, fragt der Planer in Plan 10 erneut nach oder
der Stakeholder beantwortet F2 ein zweites Mal.

**Gegenvorschlag.** „F2 offen bei dir“ ersetzen, etwa: „Reihenfolge nach der Klärung in
8880, von dir mit F2 A bestätigt: erst diese Teile, dann das Aufräumen …“.
