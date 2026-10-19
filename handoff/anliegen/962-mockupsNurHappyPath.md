# Mockups zu Plan 6 zeigen den Happy Path, so schlank wie ArbiterMap

962 · Kritik · von Planer → Ux · Runde 1/3 · erledigt

## Runde 1
**Befund.** Der Stakeholder gibt Plan 6 nicht frei (Kommentar unter
[Freigabe](../plan.md#freigabe)): In den Mockups sieht er mehr Hinweise und Knöpfe, als er aus
ArbiterMap kennt, und nicht seinen Happy Path. [Plan 6](../plan.md) ist darauf neu geschnitten.
1. [auf-19](../../domaene/mockups/auf-19.html) und [que-7](../../domaene/mockups/que-7.html)
   zeigen „gemeinsam übergehen“; Plan 6 baut es nicht.
2. [auf-22](../../domaene/mockups/auf-22.html) (‚nicht an der Reihe‘ mit „Spieler 2 ist an der
   Reihe“), [auf-23](../../domaene/mockups/auf-23.html),
   [auf-23-sperre](../../domaene/mockups/auf-23-sperre.html) und que-7 gehören zu Randfällen für
   Plan 7; kein Item von Plan 6 verlinkt sie mehr.
3. Kein Mockup zeigt den Ablauf: *Roll-off*, *Einheit* wählen, in die Zone klicken, verschieben,
   beenden, der andere ist *an der Reihe*. Jedes zeigt einen Zwischen- oder Sperrzustand.
4. Item 3 ([Gewinner und Zone](../../domaene/items/gewinnerUndZone.md), AUF-11) hat kein Mockup.
5. Maßstab ArbiterMap: Ablage mit *Namen* und Modellzahl, Umschalter „Ganze Einheit /
   Einzelmodelle“ an der *ausgewählten* *Einheit* (`ArbiterMap/docs/spec/interaction_map.md:190`),
   sonst nichts.

**Kosten.** Ohne neue Mockups sieht der Stakeholder seine Vorstellung nicht und gibt nicht frei.

**Gegenvorschlag.** Mockups zu Item 1 bis 3 nur mit Zuständen des Happy Path: vor dem
*Roll-off* „Roll-off gewonnen“ je *Ablage*; Zone gewählt; *Einheit* *ausgewählt*; nach dem Klick
die *Formation* in der Zone; als Block verschoben; „Einzelmodelle“; nach dem Beenden der andere
*an der Reihe*. Sichtbar dabei nur Kopfzeile mit „an der Reihe“, *Ablagen*, das Kennzeichen von
*Auswahl* und *Einheit in Aufstellung* so leise wie in ArbiterMap (AUF-4.5 und 5.6 verlangen kein
Wort), der Umschalter und „Aufstellen der Einheit beenden“. Einen Sperrzustand zeigt nur
auf-19: *Grund* und „zurück“, ohne „gemeinsam übergehen“. Nach
[960](960-happyPathOffeneEntscheidungen.md) F3, Annahme A, zeigt keines zwei *ausgewählte*
*Einheiten*. Die Randfall-Mockups behältst du für Plan 7 oder löschst sie.

Erledigt, wenn: Jedes Mockup, das ein Item von Plan 6 verlinkt, zeigt nur, was die Kriterien
dieses Items verlangen; keines zeigt „gemeinsam übergehen“; AUF-11 hat ein Mockup; deine
Stellungnahme nennt die Dateien je Item, damit ich die Links setze.

**Stellungnahme.** Umgesetzt nach dem Gegenvorschlag, je ein Bild je Schritt in Spielreihenfolge; keines zeigt „gemeinsam übergehen“, einen Abzeichen-Text oder zwei *ausgewählte* *Einheiten*. Ablaufplan zum Öffnen im Browser: [ablaufplan](../../domaene/mockups/ablaufplan.html).
- Item 3 (AUF-11, neu): [auf-11-rolloff](../../domaene/mockups/auf-11-rolloff.html), [auf-11-gewinner](../../domaene/mockups/auf-11-gewinner.html), [auf-11-zone](../../domaene/mockups/auf-11-zone.html).
- Item 1: [auf-18-ausgewaehlt](../../domaene/mockups/auf-18-ausgewaehlt.html), [auf-18](../../domaene/mockups/auf-18.html), [auf-19](../../domaene/mockups/auf-19.html) (nur *Grund* und „zurück“).
- Item 2: [auf-20](../../domaene/mockups/auf-20.html) (Block), [auf-21](../../domaene/mockups/auf-21.html) („Einzelmodelle“; die Nummern waren vertauscht), [auf-10](../../domaene/mockups/auf-10.html) (nach dem Beenden der andere *an der Reihe*; neu, Item 10 hat keines, Zuordnung zu Item 2 ist meine Empfehlung).
- Plan 7: auf-22, auf-23, auf-23-sperre und que-7 bleiben unverändert liegen; kein Item von Plan 6 verlinkt sie, und `ruhigeKarte` verlinkt que-7 weiter.
Kein neues CSS und keine neue Klasse; „Roll-off gewonnen“ ist ein `knopf` in der *Ablage*, die neutrale Zone `ohneSpieler`.

