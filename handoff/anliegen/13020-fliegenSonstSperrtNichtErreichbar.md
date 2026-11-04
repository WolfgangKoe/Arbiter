# Fliegen: „sonst sperrt QUE-1.2“ ist nicht zu erreichen

Form: Kritik
Von: Testautor
An: Anforderungsautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Hält den Happy Path nicht auf. Zu
[BEW-18.2](../../domaene/anforderungen/phasen/bewegung/fliegen.md), Halbsatz „sonst sperrt
QUE-1.2“ (und über 18.4 dort): Ich finde keinen Fall, in dem er greift, darum steht kein Test
dazu. Die *Stelle* der Spinne vor dem Ziehen ist immer eine, an der keine *Base* eine fremde
*überdeckt* (QUE-1.4: Übergehen auf eine fremde *Base* gibt es nicht), die *ganz in* dem
*Spielfeld* liegt und keine *Distanz* über der *Bewegungsweite* hat. Damit gibt es immer eine
freie *Stelle*, ausgenommen den Fall, dass die Spinne schon in *Nahkampfreichweite* steht
(die Orks sind in ihrem Zug *gemeinsam übergehend* herangezogen). Dann hält sie nach BEW-25.1
an der vorigen *Stelle* an; ob 18.3 das für *Fliegen* ändert, regelt kein Kriterium. Nach
dem Regeltext darf eine *Einheit*, die in *Nahkampfreichweite* beginnt, keine normale
Bewegung machen (`core_rules.txt:724`), so dass 25.1 auch für die Spinne
gilt. Auch nach 18.4 (ohne 3.1 und 6.2) bleibt die *Stelle* vor dem Ziehen frei. Im Vertrag
begrenzt `zurück` die Suche auf genau diese Entfernung
([Vertrag Fliegen](../../technik/architektur/vertrag/bewegung/fliegen.md)), findet also
immer eine.

**Kosten.** A: ein Halbsatz weniger in 18.2, kein Test, im Code bleibt die Sperre als
Absicherung oder entfällt nach dem Urteil des Architekten. B: der Fall wird benannt
(Spinne beginnt in *Nahkampfreichweite*, Verhältnis von 25.1 und 18.3), ein Kriterium mehr
und ein bis zwei Tests mit vielen Modellen der Orks rings um die Spinne.

**Gegenvorschlag.** A: „sonst sperrt QUE-1.2“ streichen. Warum: Ein Halbsatz ohne
erreichbaren Fall lässt sich nicht prüfen, und am Bildschirm sieht ihn niemand (Absicht 3).
Gibt es einen Fall, den ich übersehe, nenne ihn; dann schreibe ich den Test dazu.

**Stellungnahme.** Angenommen, A für Etappe 2: „sonst sperrt QUE-1.2“ ist aus
[BEW-18.2](../../domaene/anforderungen/phasen/bewegung/fliegen.md) gestrichen. Den Fall, den
du suchst, gibt es erst mit AUF-27.1 (Etappe 7): Dort steht die Spinne schon vor dem Ziehen
auf einer fremden *Base*, und ist ringsum alles belegt, findet 18.2 keine *Stelle*. Der
Stakeholder will dann: „kann nicht bewegt werden“ (13010 F1). Das steht als neues BEW-18.6
mit `(Etappe 7)`, also jetzt kein Test. Zugleich ist BEW-18.4 nach 13010 F1 durch 18.5
ersetzt (18.2 gilt auch nach BEW-8.4, mit *Bewegungsweite* und *Nahkampfreichweite*); die
Tests zu 18.4 entfallen, 18.5 braucht neue.
