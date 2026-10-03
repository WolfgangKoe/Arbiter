# Aufstellen

Die *Aufstellung* ist Schritt 4 der *Mission* Only War ([core_rules.txt:2321]): Die *Spieler* bringen ihre *Armeen* aufs *Spielfeld*. *Einheiten*, die erst in der Bewegungsphase als „Reinforcements“ ins Spiel kommen ([core_rules.txt:800]), gehören nicht hierher.

[core_rules.txt:2321]: ../../referenz/rules/core_rules.txt#L2321
[core_rules.txt:2322]: ../../referenz/rules/core_rules.txt#L2322
[core_rules.txt:450]: ../../referenz/rules/core_rules.txt#L450
[core_rules.txt:464]: ../../referenz/rules/core_rules.txt#L464
[core_rules.txt:800]: ../../referenz/rules/core_rules.txt#L800

### AUF-1 · Reihenfolge der Aufstellung

Zweck: Zonenwahl, wer wann aufstellt. Kriterien: [core_rules.txt:2322].

- AUF-1.1 Vom *Roll-off* wird nur der *Gewinner* eingegeben; die gewählte *Aufstellungszone* gehört ihm, die andere dem anderen.
- AUF-1.2 Erst wird der *Gewinner*, dann die *Aufstellungszone* gewählt, je einmal; sonst *Sperre* ‚nicht wählbar‘.
- AUF-1.3 Bis zur Wahl der *Aufstellungszone* ist keiner *an der Reihe*, danach, wer nicht *Gewinner* ist.
- AUF-1.4 Ein *Modell* außerhalb der *Einheit in Aufstellung* *setzen* oder ohne sie *Aufstellen der Einheit beenden*: *Sperre* ‚nicht in Aufstellung‘.
- AUF-1.5 Wählbar als *Einheit in Aufstellung* ist nur eine nicht *aufgestellte* *Einheit* des *Spielers* *an der Reihe*; sonst *Sperre* ‚nicht wählbar‘.
- AUF-1.6 Eine wählbare *Einheit* wird *Einheit in Aufstellung*, außer eine andere ist es und von ihr ist ein *Modell* *gesetzt*: *Sperre* ‚Einheit begonnen‘.
- AUF-1.7 Gelingt *Aufstellen der Einheit beenden*, ist die *Einheit* *aufgestellt*, keine *Einheit in Aufstellung* und der andere *Spieler* *an der Reihe*; hat er alle *aufgestellt*, derselbe; haben es beide, ist die *Aufstellung* beendet und keiner *an der Reihe*.

### AUF-2 · Ausgangslage von Only War

Zweck: Womit die *Aufstellung* beginnt; woraus *Armeen* und *Spielfeld* bestehen, sagt [OBJ-1](../spielobjekte.md). Werte in [ausgangslage.yaml](../../daten/ausgangslage.yaml) und [onlyWar.yaml](../../daten/onlyWar.yaml), Entscheidungen des Stakeholders zu Etappe 1 (Anliegen 09, F1 A, F10 B, git).

- AUF-2.4 Jede der zwei *Aufstellungszonen* ist das Band des *Spielfelds* mit der *Tiefe* aus `onlyWar.yaml` an einer langen *Spielfeldkante*, die eine an der gegenüberliegenden der anderen.
- AUF-2.5 In der *Ausgangslage* ist kein *Modell* *gesetzt* und keine *Einheit* *aufgestellt*.
- AUF-2.6 Die *Ausgangslage* hat die zwei *Armeen* aus `ausgangslage.yaml` mit ihren *Einheiten*, je Eintrag unter `durchmesser` ein *Modell*, dessen *Base* diesen *Durchmesser* hat.
- AUF-2.7 Das *Spielfeld* der *Ausgangslage* hat die Seitenlängen aus `onlyWar.yaml`.

### AUF-3 · Sperren beim Setzen

Zweck: Arbiter sperrt beim *Setzen* nach [QUE-1](../querschnitt.md) auch jede *Stelle*, die nur die *Aufstellung* verbietet, und nennt den *Grund*. Gemessen wird der *Abstand* ([core_rules.txt:464]).

- AUF-3.2 Liegt die *Base* des *Modells* an der *Stelle* nicht *ganz in* der *Aufstellungszone* seines *Spielers*: *Sperre* ‚nicht ganz in der Zone‘ ([core_rules.txt:2322]).
- AUF-3.4 Ist es an der *Stelle* in *Engagement Range* eines *gesetzten* *Modells* des anderen *Spielers*: *Sperre* ‚Engagement Range‘ ([core_rules.txt:450]).
- AUF-3.6 Ist das *Setzen* nach AUF-1.4 gesperrt, prüft Arbiter die *Stelle* nicht; der einzige *Grund* ist ‚nicht in Aufstellung‘.
- AUF-3.7 Auch ein *gesetztes* *Modell* der *Einheit in Aufstellung* lässt sich *setzen*, geprüft nach QUE-1.2, AUF-3.2 und AUF-3.4 (Etappe 1, Anliegen 16 F2 A, git).
