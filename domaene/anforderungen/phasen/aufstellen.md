# Aufstellen

Die *Aufstellung* ist Schritt 4 der *Mission* Only War ([core_rules.txt:2321]): Die *Spieler* bringen ihre *Armeen* aufs *Spielfeld*. *Einheiten*, die erst in der Bewegungsphase als „Reinforcements“ ins Spiel kommen ([core_rules.txt:800]), gehören nicht hierher.

[core_rules.txt:2321]: ../../referenz/rules/core_rules.txt#L2321
[core_rules.txt:2322]: ../../referenz/rules/core_rules.txt#L2322
[core_rules.txt:450]: ../../referenz/rules/core_rules.txt#L450
[core_rules.txt:464]: ../../referenz/rules/core_rules.txt#L464
[core_rules.txt:800]: ../../referenz/rules/core_rules.txt#L800

### AUF-1 · Reihenfolge der Aufstellung

Zweck: Wer wann wählt und *an der Reihe* ist ([core_rules.txt:2322]).

- AUF-1.1 Vom *Roll-off* wird nur der *Gewinner* eingegeben; die gewählte *Aufstellungszone* gehört ihm, die andere dem anderen.
- AUF-1.2 Erst wird der *Gewinner*, dann die *Aufstellungszone* gewählt, je einmal; sonst *Sperre* ‚nicht wählbar‘.
- AUF-1.3 Bis zur Wahl der *Aufstellungszone* ist keiner *an der Reihe*, danach, wer nicht *Gewinner* ist.
- AUF-1.7 Gelingt *Aufstellen der Einheit beenden*, ist die *Einheit* *aufgestellt*, keine *Einheit in Aufstellung* und der andere *Spieler* *an der Reihe*; hat er alle *aufgestellt*, derselbe; haben es beide, ist die *Aufstellung* beendet und keiner *an der Reihe*.

### AUF-2 · Ausgangslage von Only War

Zweck: Womit die *Aufstellung* beginnt; wer welche *Armee* führt, sagt [OBJ-1](../spielobjekte.md), woraus sie und das *Spielfeld* bestehen, das [Glossar](../../glossar.md). Werte in [ausgangslage.yaml](../../daten/ausgangslage.yaml) und [onlyWar.yaml](../../daten/onlyWar.yaml), Entscheidungen des Stakeholders zu Etappe 1 (Anliegen 09, F1 A, F10 B, git).

- AUF-2.4 Jede der zwei *Aufstellungszonen* ist das Band des *Spielfelds* mit der *Tiefe* aus `onlyWar.yaml` an einer langen *Spielfeldkante*, die eine an der gegenüberliegenden der anderen.
- AUF-2.5 In der *Ausgangslage* ist kein *Modell* *gesetzt* und keine *Einheit* *aufgestellt*.
- AUF-2.6 Die *Ausgangslage* hat die zwei *Armeen* aus `ausgangslage.yaml` mit ihren *Einheiten*, je Eintrag unter `durchmesser` ein *Modell*, dessen *Base* diesen *Durchmesser* hat.
- AUF-2.7 Das *Spielfeld* der *Ausgangslage* hat die Seitenlängen aus `onlyWar.yaml`.

### AUF-3 · Sperren beim Setzen

Zweck: Arbiter sperrt beim *Setzen* nach [QUE-1](../querschnitt.md) auch jede *Stelle*, die nur die *Aufstellung* verbietet, und nennt den *Grund*. Gemessen wird der *Abstand* ([core_rules.txt:464]).

- AUF-3.2 Liegt die *Base* des *Modells* an der *Stelle* nicht *ganz in* der *Aufstellungszone* seines *Spielers*: *Sperre* ‚nicht ganz in der Zone‘ ([core_rules.txt:2322]).
- AUF-3.4 Ist es an der *Stelle* in *Nahkampfreichweite* eines *gesetzten* *Modells* des anderen *Spielers*: *Sperre* ‚Nahkampfreichweite‘ ([core_rules.txt:450]).
- AUF-3.5 Sperrt an der *Stelle* mehr als eines von QUE-1.2, AUF-3.2 und AUF-3.4, nennt Arbiter den *Grund* jedes davon (Anliegen 100 F3 A, git).
- AUF-3.7 Auch ein *gesetztes* *Modell* der *Einheit in Aufstellung* lässt sich *setzen*, geprüft nach QUE-1.2, AUF-3.2 und AUF-3.4 (Etappe 1, Anliegen 16 F2 A, git).
- AUF-3.8 Ist das *Setzen* nach AUF-7.2 oder AUF-7.3 gesperrt, prüft Arbiter die *Stelle* nicht; der einzige *Grund* ist der von dort.

### AUF-4 · Anzeige der Aufstellung

Zweck: Neben der *Karte* nach [QUE-2](../querschnitt.md) sehen die *Spieler*, welche *Modelle* noch aufzustellen sind, wer *an der Reihe* ist und welche *Aufstellungszone* wem gehört.

- AUF-4.2 Den *Spieler* der ersten *Armee* aus `ausgangslage.yaml` nennt Arbiter „Spieler 1“, den anderen „Spieler 2“ (`Arbiter-old/docs/spec/setup.md:136`, Anliegen 195 F3 A).
- AUF-4.3 Je *Spieler* zeigt Arbiter eine *Ablage* mit jeder seiner nicht *aufgestellten* *Einheiten* unter ihrem *Namen*, auch wenn alle ihre *Modelle* *gesetzt* sind, und der Anzahl ihrer nicht *gesetzten*, wenn es welche gibt (Etappe 1, Anliegen 145 F1 A, 199, 239 F1 B).
- AUF-4.4 Arbiter zeigt, welcher *Spieler* *an der Reihe* ist, und keinen, solange es keiner ist.
- AUF-4.5 In der *Ablage* ist die *Einheit in Aufstellung* gekennzeichnet, solange es eine gibt.
- AUF-4.6 Die *Karte* zeigt jede *Aufstellungszone* in der Farbe der *Modelle* des *Spielers*, dem sie gehört, vor der Wahl nach AUF-1.1 in keiner der beiden (Vorbild `ArbiterMap/docs/spec/design_colors.md:72` bis `:74`).
- AUF-4.7 Die *Ablage* nennt ihren *Spieler* in der Farbe seiner *Modelle* auf der *Karte* (Anliegen 199).

### AUF-5 · Auswählen am Bildschirm

Zweck: Die *Spieler* zeigen per Klick, welche *Einheit* gemeint ist, ohne Handlung (Anliegen 309; Vorbild `ArbiterMap/docs/spec/interaction_map.md:282`).

- AUF-5.3 Ein Klick auf eine nicht *ausgewählte* *Einheit* in einer *Ablage* macht sie *ausgewählt*, auch wenn ihr *Spieler* nicht *an der Reihe* ist.
- AUF-5.4 Ein Klick auf eine *ausgewählte* *Einheit* in einer *Ablage* macht sie nicht *ausgewählt* (Vorbild `interaction_map.md:296`).
- AUF-5.5 Macht AUF-5.3 eine dritte *Einheit* desselben *Spielers* *ausgewählt*, ist es die zuerst *ausgewählte* der beiden anderen nicht mehr (Vorbild `interaction_map.md:337`).
- AUF-5.6 Die *Ablage* kennzeichnet jede *ausgewählte* *Einheit*, unterscheidbar von der Kennzeichnung nach AUF-4.5.
- AUF-5.7 Die *Karte* kennzeichnet jedes *gesetzte* *Modell* einer *ausgewählten* *Einheit*.
- AUF-5.8 Ein Klick nach AUF-5.3 oder AUF-5.4 ändert weder, wer *an der Reihe* ist, noch die *Einheit in Aufstellung* oder ein *Modell*.
- AUF-5.9 Nach dem Start nach QUE-2.1 ist keine *Einheit* *ausgewählt*.
- AUF-5.10 Wird eine *ausgewählte* *Einheit* *aufgestellt*, ist sie nicht mehr *ausgewählt* (Anliegen 309).

### AUF-6 · Vorläufig: Start mit gewähltem Gewinner und gewählter Zone

Zweck: Bis die *Spieler* *Gewinner* und *Aufstellungszone* am Bildschirm wählen können, trifft Arbiter beide Wahlen beim Start selbst, damit gleich ein *Modell* *gesetzt* werden kann. Die Anforderung ist eine Krücke: Sie entfällt mit der Wahl am Bildschirm und ihr Test mit ihr (Anliegen 308 F1 A, F2 A, git).

- AUF-6.1 Nach dem Start nach QUE-2.1 ist „Spieler 1“ nach AUF-1.1 *Gewinner* und hat die *Aufstellungszone* gewählt, die auf dem Bildschirm seiner *Ablage* am nächsten liegt; nach AUF-1.3 ist „Spieler 2“ *an der Reihe*.

### AUF-7 · Einheit in Aufstellung

Zweck: Die *Spieler* stellen ihre *Einheiten* abwechselnd und einzeln auf ([core_rules.txt:2322]); Arbiter führt, welche *Einheit* gerade aufgestellt wird, und sperrt jedes *Setzen* außer der Reihe.

- AUF-7.1 *Einheit in Aufstellung* ist die nicht *aufgestellte* *Einheit* mit *gesetztem* *Modell*, sonst keine.
- AUF-7.2 Ein *Modell* einer *aufgestellten* *Einheit* oder eines *Spielers* nicht *an der Reihe* *setzen*: *Sperre* ‚nicht wählbar‘.
- AUF-7.3 Sonst ein *Modell* *setzen*, wenn es eine andere *Einheit in Aufstellung* gibt: *Sperre* ‚Einheit begonnen‘.
- AUF-7.4 Ohne *Einheit in Aufstellung* *Aufstellen der Einheit beenden*: *Sperre* ‚nicht in Aufstellung‘.
