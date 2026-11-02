# BEW-25 hält vorgerückte Einheiten zu Unrecht an, BEW-18.2 ohne Grenzen

Form: Kritik
Von: Architekt
An: Anforderungsautor
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Hält die Freigabe von Plan 10 auf, weil eine *Sperre* zu Unrecht greift und ein
Test sein Kriterium nicht ohne Erfundenes prüft ([Kritik](../../prozess/ablauf/kritik.md)):
1. [BEW-25.1](../../domaene/anforderungen/phasen/bewegung/weiterziehenNachDemUebergehen.md)
   hält an, sobald ein *Modell* „eine *Distanz* über seiner *Bewegungsweite* hat“.
   [BEW-5.3](../../domaene/anforderungen/phasen/bewegung/vorruecken.md) lässt eine
   *vorgerückte* *Einheit* aber bis *Bewegungsweite* plus *Vorrückwurf* ziehen. Beispiel:
   Boyz (B 5″) *rücken vor*, *Vorrückwurf* 4, ziehen 7″ und lassen los, ganz ohne Übergehen.
   Zieht ihr sie noch 1″ weiter (BEW-1.6), hält BEW-25.1 sie an und bietet „gemeinsam
   übergehen“ an, obwohl BEW-5.3 bis 9″ erlaubt; Schritt 1 des Happy Path („wie bisher“)
   ändert sich. Zudem sagt „halten BEW-3.1 oder 6.2“ nicht, welches; davon hängen die
   *Gründe* im *Protokoll* nach BEW-8.5 ab.
2. [BEW-18.2](../../domaene/anforderungen/phasen/bewegung/fliegen.md) *setzt* „an die nächste
   *Stelle*, an der keine eine fremde *überdeckt*“, sagt aber nicht,
   - ob diese *Stelle* im *Spielfeld*, innerhalb der *Bewegungsweite* und außerhalb der
     *Nahkampfreichweite* liegen muss. Beispiel: Die Spinne endet am Ende ihrer *Bewegungsweite* auf einem
     Necron Warrior; die nächste freie *Stelle* liegt 1″ weiter, also über der *Bewegungsweite*, oder
     hinter der Kante oder 0,5″ vor einem Boy;
   - wie genau „nächste“ gilt. Die Berührung zweier runder *Bases* liegt meist auf einer
     Wurzel, die Arbiter nicht exakt *setzt*; BEW-3.1 nennt dafür „höchstens 1/100″ davor“,
     BEW-18.2 nichts. Der Test müsste eine Toleranz erfinden.

**Kosten.** Je ein Halbsatz, keine Zeile Code. Bleibt 1, schreibt der Testautor einen Test,
der heutiges Verhalten bricht, oder der Implementierer erfindet die Ausnahme. Bleibt 2,
entscheidet der Implementierer, wohin die Spinne rückt; die Antwort ändert die Rechnung
erheblich (mit Kante, *Bewegungsweite* und *Nahkampfreichweite* sucht sie in einer
eingeschränkten Fläche statt in der freien).

**Gegenvorschlag.**
1. BEW-25.1: „… das an der vorigen *Stelle* eine *Distanz* hat, an der BEW-3.1 (auch nach
   BEW-5.3) es anhalten würde, oder in *Nahkampfreichweite* … ist, … **dann** halten im
   ersten Fall BEW-3.1, im zweiten 6.2 die gezogenen *Modelle* an der vorigen *Stelle* an …“.
2. BEW-18.2: „… an die nächste *Stelle*, an der keine eine fremde *überdeckt* [und BEW-3.1,
   6.1 und 6.2 keines anhalten], höchstens 1/100″ weiter“; die eckige Klammer nur, wenn
   der Stakeholder es so will. Fehlt dir die Entscheidung, frag ihn mit Empfehlung; meine:
   mit Klammer, denn sonst endet die Spinne regelwidrig über ihrer *Bewegungsweite* oder
   in *Nahkampfreichweite* (`core_rules.txt:745`, `:884`).

**Stellungnahme.** Beides umgesetzt, wie vorgeschlagen.
1. [BEW-25.1](../../domaene/anforderungen/phasen/bewegung/weiterziehenNachDemUebergehen.md):
   „eine *Distanz*, an der BEW-3.1 (auch nach BEW-5.3) es anhalten würde“; im ersten Fall hält
   BEW-3.1, im zweiten 6.2, in beiden beide (`core_rules.txt:754`). Die *Gründe* folgen so
   eindeutig aus BEW-8.5.
2. [BEW-18.2](../../domaene/anforderungen/phasen/bewegung/fliegen.md): „an die nächste
   *Stelle*, höchstens 1/100″ weiter, an der keine eine fremde *überdeckt* und BEW-3.1, 6.1
   und 6.2 keines anhalten würden“. Die Klammer verlangt der Regeltext, keine Frage an den
   Stakeholder: Ein *Modell* endet nicht über seiner *Bewegungsweite* (`:745`), nicht über der
   Kante (`:729`) und mit *Fliegen* nicht in *Nahkampfreichweite* (`:888`); 6.2 gilt für die
   Spinne nach BEW-18.3. Damit die Datei unter 1.200 Zeichen bleibt, verweist der Zweck von
   BEW-18 auf *Fliegen* im Glossar, statt es zu wiederholen.
