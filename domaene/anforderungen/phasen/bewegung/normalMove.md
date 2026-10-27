### BEW-1 · Normal Move

Etappe: 2
Zweck: In der *Bewegungsphase* zieht der *Spieler* *am Zug* eine eigene *Einheit* im *Normal Move* und beendet ihn; am Ende ist sie in *Kohärenz* (`core_rules.txt:710`, `:730`, `:745`). Ein *Modell* darf mehrmals gezogen werden (Anliegen 02 F5, git).
Am Bildschirm: *Modelle* ziehen wie beim Aufstellen ([AUF-8](../aufstellen/ziehen.md), [AUF-21](../aufstellen/einheitVerschieben.md)), „Bewegung der Einheit beenden“ klicken.

- BEW-1.1 **Gegeben** die *Bewegungsphase*, **wenn** jemand ein *Modell* einer *Einheit* des *Spielers* *am Zug* zieht und loslässt, **dann** ist sie die *Einheit in Bewegung*, und Arbiter *setzt* nach AUF-8.2, bei der ganzen *Einheit* als *Ebene* nach AUF-21.1, ohne in eine *Aufstellungszone* zu rücken.
- BEW-1.2 **Gegeben** die *Einheit in Bewegung* ist nicht in *Kohärenz* (QUE-4), **wenn** jemand *Bewegung der Einheit beenden* wählt, **dann** *Sperre* ‚keine Kohärenz‘, nach QUE-5.5 nicht zu übergehen (`core_rules.txt:434`, `:730`).
- BEW-1.3 **Wenn** *Bewegung der Einheit beenden* gelingt, **dann** gibt es keine *Einheit in Bewegung*, und jedes ihrer *Modelle* bleibt an seiner *Stelle*.
