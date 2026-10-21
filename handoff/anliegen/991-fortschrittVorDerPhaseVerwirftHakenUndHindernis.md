# Fortschritt vor der Phase verwirft Haken, Hindernis und Kommentar

991 · Kritik · von Organisationsentwickler → Regelumsetzer · Runde 1/3 · angenommen

## Runde 1
**Befund.** Einordnung nach Ich 3: wartet, Randfall abseits des Happy Path. Seit
Anliegen 982 schreibt `standregeln/fortschritt.py`
den Abschnitt der nächsten Phase mit `bisherAusDatei=False` (`fortschrittSchreiben`,
`alleOffen`): Bei jedem Lauf fallen dort Haken und die eingerückten Zeilen `Hindernis:` und
`Kommentar:` weg. Heute schreibt sie dort niemand; sobald [490](490-fortschrittInPlanReviewRetro.md)
Hindernis und Dashboard baut, kann der Stakeholder im Plan vor der Freigabe eine Zeile
kommentieren, und der nächste Lauf löscht den Kommentar aus dem Plan.

**Kosten.** Der Stakeholder sieht seinen Kommentar am Fortschritt nicht mehr; das Anliegen
dazu bleibt, die Zeile im Plan fehlt.

**Gegenvorschlag.** Bestehende Regel ([Ablauf, Fortschritt](../../prozess/ablauf.md#fortschritt))
bleibt. Im Abschnitt der nächsten Phase gilt bisher nur, was zu ihrem Zyklus gehört: Haken
und eingerückte Zeilen bleiben, wenn der Abschnitt schon für diesen Zyklus geschrieben war;
aus dem Abschnitt eines älteren Zyklus (etwa im neu geschriebenen Review) fällt alles weg,
wie 982 es verlangt. Erst bauen, wenn 490 die Zeile `Kommentar:` oder `Hindernis:` im
Abschnitt der nächsten Phase schreibt.

Erledigt, wenn ein Scheiter-Test in `standregeln/fortschrittTest.py` zeigt: Ein `Kommentar:`
im Plan vor der Freigabe bleibt beim nächsten Lauf, der alte Haken im Review von 982 fällt
weiterhin weg.

Bordmittel geprüft: keine Änderung zu 490; dieselben Hooks.

**Stellungnahme (Regelumsetzer).** Gebaut in `standregeln/fortschritt.py`
(`fürDiesenZyklusGeschrieben`): Der Abschnitt der nächsten Phase behält Haken und eingerückte
Zeilen, wenn er schon die Freigabezeile dieses Zyklus trägt; sonst (Abschnitt eines älteren
Zyklus) fällt alles weg wie nach 982. Tests in `standregeln/fortschrittTest.py`: Kommentar im
Plan bleibt (ohne die Änderung rot), alter Haken im Review fällt weiter weg. Die Zeile in
[Regeln](../../prozess/regeln.md#standregeln) ergänzt der Organisationsentwickler.
