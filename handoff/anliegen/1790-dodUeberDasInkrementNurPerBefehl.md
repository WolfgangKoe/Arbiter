# DoD über das Inkrement nur per Befehl des Reviewers

1790 · Kritik · von Organisationsentwickler → Regelumsetzer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Aus dem [Rundgang Prüfcode](../review.md#rundgang-prüfcode) in Review 6, Punkt 1,
auf Vorgabe des Stakeholders in die [Retro 6](../retro.md) aufgenommen:
`standregeln/fortschritt.py`, `technikzeilen`, hakt die Zeile „Reviewer: DoD über das
Inkrement“ ab, sobald kein Item mehr offen ist (`review or not offeneItems(wurzel)`). Die
Tabelle in [Ablauf, Fortschritt](../../prozess/ablauf.md#fortschritt), Technik 4, nennt dafür
den Befehl des Reviewers. In Zyklus 6 stand der Haken im Plan, bevor der Reviewer die DoD
geprüft hatte, bei rotem SonarLint (Anliegen 1630).

Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): Der Mechanismus weicht von seiner
Regel ab; die Prozessphase ist die Phase deiner Perspektive, es wartet nicht.

**Kosten.** Der Stand zeigt eine DoD als erfüllt, die niemand geprüft hat. Liest der
Stakeholder den Haken, kann er ein Inkrement mit Fehlern abnehmen (sein Kommentar in
[1671](1671-prozessphaseVorziehen.md)).

**Gegenvorschlag.** Bestehende Regel, kein neuer Text ([Ich 4](../../prozess/praemissen/ich.md)):
Die Zeile ist nur abgehakt, wenn der Reviewer sie mit dem Befehl abhakt; `review` und
`not offeneItems` entfallen dort. Das Review zählt nicht: Sein Kopf stand in Zyklus 6, bevor
die DoD durch war (Architekt in Anliegen 1850, Punkt 8).

Erledigt, wenn ein Scheiter-Test in `standregeln/fortschrittTest.py` zeigt: Alle Items
gelöscht, das Review des Zyklus geschrieben, kein Befehl, dann ist „DoD über das Inkrement“
offen.

**Stellungnahme.**
