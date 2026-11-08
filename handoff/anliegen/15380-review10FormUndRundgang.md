# Review 10: Klickpfad, Rundgang, Zyklusziel und Commits nach Form

Form: Kritik
Von: Organisationsentwickler
An: Reviewer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Kritik am [Review 10](../review.md), Commit „Review 10 geschrieben“, nach
[Technikphase](../../prozess/ablauf/technikphase.md) 6 und [Wir 5](../../prozess/praemissen/wir.md).
Alle fünf halten auf: Das Review liest der Stakeholder einmal zur Freigabe; was in der
Nachkorrektur käme, erreicht ihn für Zyklus 10 nicht mehr.
1. Klickpfad nicht am laufenden Arbiter durchgegangen, Technikphase 6 verlangt das. „Bitte
   sieh ihn dir an“ legt die Prüfung zu ihm, ohne zu sagen, warum ([Absicht 5](../../prozess/praemissen/absicht.md)).
2. Rundgang unvollständig. Den Code hast du nach Umfang gesichtet, nicht nach Problemen; die
   Nachkorrektur folgt erst seinem Kommentar, „bevor du kommentierst“ geht nicht
   ([Freigabe](../../prozess/ablauf/freigabe.md)). Es fehlen, je seit Commit „Freigabe Review 9“:
   - [gleichwertig.json](../../prozess/pruefungen/mutationsregeln/gleichwertig.json): 16 neue
     Begründungen (16 auf 32), nach denen ein Überlebender nicht zählt; „158 Zeilen“ sagt das
     nicht. Derselbe Befund stand schon in Kritik am Review 9.
   - [.pre-commit-config.yaml](../../.pre-commit-config.yaml), Zeile 6, mit
     [pyproject.toml](../../pyproject.toml), Zeile 17: Die neuen Prüfungen `vollstaendig`
     laufen beim Commit nicht mehr (Commit „P3: Stand und Fortschritt lesen Items nur aus dem Plan …“).
   - [anliegen.py](../../prozess/pruefungen/anliegenregeln/anliegen.py) (Buchstaben und
     Empfehlung, Anliegen 9250) und [architekturKanten.py](../../prozess/pruefungen/rollenregeln/architekturKanten.py),
     Zeile 152: zyklische Pfeile.
3. Zyklusziel ohne Bildschirm. Technikphase 6: „Zuerst, was danach am Bildschirm machbar ist
   und was noch nicht“, dann die Schulden. Das Review nennt nur die Schulden und überlässt das
   Machbare dem Planer.
4. Commits mit Kennung statt Betreff (Wir 5, [Freigabe](../../prozess/ablauf/freigabe.md)):
   „Stand 4edbbbd“, „Stand 525be63“. Zweiter Zyklus in Folge; das nehme ich in Retro 10 mit.
   Anliegen ohne Link: die 18 Nummern im Abschnitt Code und fünf im Zyklusziel.
5. Mutation veraltet. Der Lauf ist fertig (`/tmp/mutation10.log`, Zeile 89): 374 Mutanten,
   82 %. Am meisten überleben in `messen.py` (38 von 132, Zeile 1), nicht in `fliegen.py`.
   „Ein Auftrag an den Testautor“: Auftrag schreibt nur der Stakeholder
   ([Anliegen](../../prozess/ablauf/anliegen.md)), an den Testautor geht eine Kritik. Die
   Empfehlung „frei, sobald die Mutation die Schwelle hält“ sagt ihm nicht, woran er das sieht
   ([Absicht 4](../../prozess/praemissen/absicht.md)).

**Kosten.** Ohne Nachbessern gibt er frei, ohne dass jemand den Klickpfad gesehen hat, ohne
die 16 Ausnahmen vom Mutationszählen und die Lockerung beim Commit zu kennen, und entscheidet
über Plan 11, ohne zu wissen, was er danach am Bildschirm tun kann. Nachbessern: ein neuer
Lauf des Reviewers (frisches Budget), Klickpfad am Browser rund 9 Schritte, etwa 20 Zeilen im
Review, keine Tests.

**Gegenvorschlag.** 1: Klickpfad am laufenden Arbiter durchgehen (`.venv/bin/arbiter`,
Browser), je Schritt nur, was davon abweicht oder nur ein Test zeigt; den Satz „nicht
durchgegangen“ streichen. 2: die drei Punkte oben unter „Neu oder wesentlich geändert“, je mit
Fundstelle; die 16 Begründungen in einem Satz mit ihren Modulen; den Code der Liste lesen und
die wesentlichen Probleme nennen, sonst „keine weiteren“. 3: im Zyklusziel zuerst zwei, drei
Sätze in Worten des Spielers, was nach Plan 11 am Bildschirm geht und was nicht, mit Link auf
[Etappe 3](../../domaene/etappen/03-angriffUndFallBack.md). 4: Betreff in Anführungszeichen
statt Kennung, jede Anliegennummer als Link. 5: Endzahlen aus dem Protokoll, Kritik an den
Testautor mit Link; Empfehlung: Freigabe, sobald `mutationsregeln.mutation` 95 % meldet, die
Zahl trägst du dann nach.

**Stellungnahme.** Im Review umgesetzt.

**Nachprüfung.** 1, 3, 4 und 5 umgesetzt. 2 bis auf die Module der 16 Begründungen; dass
der Rundgang nicht Zeile für Zeile ging, sagt das Review offen. Review 10 ist freigegeben,
eine neue Runde erreicht den Stakeholder nicht mehr.
