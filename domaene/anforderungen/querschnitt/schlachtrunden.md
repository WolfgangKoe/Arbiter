### QUE-10 · Schlachtrunden und Phasen

Etappe: 2
Zweck: Arbiter führt Zug um Zug durch die *Phasen* bis zum Ende der *Schlacht*; außer der *Bewegungsphase* ist jede leer (Anliegen 07, Vorbild `Arbiter-old/…/gameHeader.py:313`).
Am Bildschirm: hinsehen, „Phase beenden“ klicken.

- QUE-10.1 **Gegeben** ein *Spieler* ist *am Zug*, **dann** zeigt Arbiter die Nummer der *Schlachtrunde*, diesen *Spieler* und den Namen der *Phase*.
- QUE-10.2 **Wenn** ein *Spieler* „Phase beenden“ klickt, **dann** ist die *Phase* die nächste in der Reihenfolge unter *Phase* im Glossar (`core_rules.txt:639`).
- QUE-10.3 **Wenn** QUE-10.2 die *Moralphase* beendet, **dann** ist der andere *Spieler* *am Zug* in der *Kommandophase*; hat er den *ersten Zug*, mit der nächsten *Schlachtrunde* (`core_rules.txt:667`).
- QUE-10.4 **Wenn** QUE-10.3 eine *Schlachtrunde* nach der letzten der *Mission* beginnen würde, **dann** ist die *Schlacht* beendet, Arbiter zeigt es, und keiner ist *am Zug* (`core_rules.txt:2337`).
- QUE-10.5 **Gegeben** eine *Phase* außer der *Bewegungsphase*, **wenn** jemand ein *Modell* zieht und loslässt, **dann** steht jedes *Modell* danach, wo es vor dem Ziehen war (Anliegen 07).
