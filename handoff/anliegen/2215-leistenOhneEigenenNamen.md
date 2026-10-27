# Die drei Leisten haben keinen eigenen Namen

Form: Kritik
Von: Fachkritiker
An: Architekt
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): wartet auf die
Technikphase. In [auf-13.html](../../domaene/mockups/auf-13.html) und
[que-5.html](../../domaene/mockups/que-5.html) meldet SonarLint in der IDE je dreimal
Web:S5255: Gleichartige Elemente sollen sich per `aria-label` unterscheiden. Gemeint sind die
drei `<aside class="leiste">`; einen Namen haben nur ihre *Griffe* („Ablage Spieler 1“,
„Ablage Spieler 2“, „Protokoll“), nicht die *Leisten* selbst. Das Markup der *Leiste* legt
[Oberfläche, O4](../../technik/architektur/oberflaeche.md) fest. Kein Schritt des Happy Path
fehlt, keine *Sperre* ist betroffen, und keine Prüfung ist rot, denn SonarLint prüft nach
[Ablauf](../../prozess/ablauf/technikphase.md) nur Python (Anliegen 280). Barrierefreiheit
steht nicht im [Ziel](../../domaene/ziel.md); fachlich ist das deshalb kein Mangel, es fällt
aber in die Sicht des Stakeholders.

**Kosten.** Nach O3 übernimmt der Implementierer das Markup der Mockups ohne Umschreiben. Ohne
Entscheidung erben die Spielseite und die Komponentenseite dieselben Warnungen
(Anliegen 2240 trägt die *Leisten* dort ein). Wird es
später geändert, müssen Mockups, Komponentenseite und Seite noch einmal angepasst werden.

**Gegenvorschlag.** In O4 entscheiden, ob jede *Leiste* ein `aria-label` bekommt, das ihren
Inhalt mit den Begriffen des Glossars nennt: links „Ablage Spieler 1“, rechts
„Ablage Spieler 2“, unten „Protokoll“. Dann entscheidet O4 auch, was der *Griff* weiter als
Namen trägt. Wird das nicht übernommen, die Warnung in O4 mit Begründung als bewusst
hingenommen festhalten. Ux zieht danach auf-13.html und que-5.html nach.

**Stellungnahme.** Übernommen, mit einer Änderung an den Namen.
[O4](../../technik/architektur/oberflaeche.md) legt jetzt fest: Das `aria-label` der *Leiste*
nennt ihren Inhalt, „Armeeliste Spieler 1“, „Armeeliste Spieler 2“, „Protokoll“; der *Griff*
heißt dazu „… ein- und ausfahren“. Statt „Ablage“ steht *Armeeliste*, denn so heißt sie seit
Anliegen 2221. Den *Griff* benennt O4 nach seiner Handlung, wie ArbiterMap
(`map.html:122`, `:169`): Ein Screenreader liest dann „Armeeliste Spieler 1, Schaltfläche
Armeeliste Spieler 1 ein- und ausfahren, ausgeklappt“. Die Bildschirmtests finden *Leiste* und
*Griff* über Rolle und Namen; das prüft die Namen mit. Die *Leisten* gibt es noch nicht im
Code, also kostet die Entscheidung jetzt nur die Mockups. Die Mockups zieht Ux mit
[2920](2920-leistenNamenInDenMockups.md) nach (auf-13.html gibt es nicht mehr, dafür
que-7.html); 2920 ist erledigt, beide Mockups tragen die Namen nach O4. Für Anliegen 2240
gilt O4 schon jetzt.
