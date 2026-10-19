# Plan 6: Fortschritt statt Prosa, Items gleichzeitig

983 · Kritik · von Organisationsentwickler → Planer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Einordnung nach Ich 3: hält auf, der Stakeholder gibt [Plan 6](../plan.md) so
nicht frei. Seine Worte zu Kommentar 2 unter der Freigabe: „wir hatten in einem Anliegen
vereinbart, wie der Fortschritt in jedem Artefakt dargestellt wird. Z.B. hier in review.md
[Abschnitt ## Fortschritt]. Das verstehe ich unter Plan! Das soll da stehen, bevor ich etwas
freigebe!“, „Und das bitte für jedes Item“ und „Die Umsetzung sollte dennoch so parallel wie
möglich erfolgen!“
1. Den Abschnitt `## Fortschritt` mit den Zeilen je Item schreibt das Skript in den Plan,
   sobald [982](982-fortschrittDerTechnikphaseVorDerFreigabe.md) gebaut ist. Die Schritte
   1 bis 6 und „Danach“ unter „Plan der Technikphase“ sagen dasselbe ein zweites Mal (Wir 3).
2. „Je Item nacheinander, das nächste beginnt, wenn das vorige abgenommen ist“ widerspricht
   seinem Wunsch. [Gleichzeitige Läufe](../../prozess/ablauf.md#gleichzeitige-läufe) erlaubt
   Items gleichzeitig, wenn ihre Dateien getrennt sind und keines auf das andere wartet.
3. Unter „Randfälle, Plan 7“ steht der Link auf `../domaene/items/ruhigeKarte.md`. Jeder
   solche Link gilt als Item des Plans (`lesen/plan.py`, `itemNamen`; Ablauf, Domänenphase
   6): Die *ruhige Karte* erschiene im Fortschritt, und nach der Freigabe wäre jedes ihrer
   Kriterien ohne Test rot.

**Kosten.** Zwei Fassungen desselben Ablaufs laufen auseinander; der Stakeholder liest eine
Reihenfolge, die er nicht will; ein Randfall würde zum Item.

**Gegenvorschlag.**
1. Die Überschrift „Plan der Technikphase“ und die allgemeinen Schritte entfallen. Was nur
   der Plan weiß, bleibt kurz beim Item unter `## Items`: Vorab 622, wegfallende Tests und
   Anliegen (621, 680, 682, 830), Vorarbeit des Architekten und Risiko bei Item 2, Item 2
   wartet auf 980 und 981.
2. Ein Satz, was gleichzeitig läuft und was wartet, je mit Grund (Item oder gemeinsame
   Datei), etwa: Verträge aller Items zugleich, Tests je Item zugleich; wartet ein Item auf
   den Code eines anderen, nenne die Stelle.
3. Den Randfall *ruhige Karte* ohne Link auf die Item-Datei nennen.

Erledigt, wenn der Plan keinen Schritt wiederholt, den der Fortschritt zeigt, nur begründete
Wartezeiten nennt und nur die drei Items verlinkt; deine Stellungnahme unter Kommentar 2 der
Freigabe nennt die Änderung.

**Stellungnahme.** Umgesetzt, kein Widerspruch. In [Plan 6](../plan.md):
1. „Plan der Technikphase“ samt Schritten und „Danach“ ist weg. Unter `## Items` steht je
   Item nur noch, was nur der Plan weiß: Vorab 622 und die wegfallenden Tests und Anliegen
   (621, 680, 682, 830) bei Item 1, Vertrag zum Block und Risiko bei Item 2. 980 und 981 sind
   erledigt, Item 2 wartet nicht mehr auf sie. Der Abschnitt `## Fortschritt` steht schon
   über der Freigabe, die Empfehlung verweist auf ihn.
2. Neuer Absatz „Gleichzeitig“: Verträge aller Items in einem Lauf des Architekten (eine
   Datei), Tests aller Items zugleich (je Anforderung eine Datei), Item 1 und 3 zugleich
   gebaut. Item 2 wird gebaut, wenn Item 1 grün ist; Grund: Beide ändern den Klick auf die
   *Karte* bei einer *ausgewählten* *Einheit* (AUF-18, AUF-25), und Item 2 braucht die
   gesetzte *Einheit*. Teilen Item 1 und 3 eine Datei (Klick in die Zone, AUF-18, AUF-11.3),
   nennt der Architekt im Vertrag, welches wartet.
3. *ruhige Karte* steht unter Randfällen ohne Link; der Plan verlinkt nur die drei Items.

Die Stellungnahme unter Kommentar 2 der Freigabe nennt die Änderung.
