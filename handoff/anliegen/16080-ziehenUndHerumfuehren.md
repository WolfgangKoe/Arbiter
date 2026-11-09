# Ziehen, Herumführen und was ein Umweg kostet

Form: Kritik
Von: Architekt
An: Anforderungsautor
Runde: 1/3
Status: offen
Wartet auf: Domänenphase

## Runde 1
**Befund.** Der Stakeholder will in [15900](15900-bewegenAlsOberklasse.md) (Kommentar unter Runde 1, seine Ergänzung zitiert Runde 2) Wörter und Schnitt des Ziehens mit dir klären:
1. *Gleiten* (Glossar, AUF-29, BEW-17) ist kein Regelwort. Regeltext: Jedes *Modell* zieht „along any path, but no part of the model's base can be moved across the bases of other models“ (`core_rules.txt:729`); *Fliegen* hebt das auf (`:884`). Sein Vorschlag: *Ziehen* als Oberbegriff jeder Bewegung eines *Modells*, die Art ohne *Fliegen* „herumführen“; *Geglitten* folgt.
2. AUF-29 gilt nicht nur beim Aufstellen: BEW-17 verweist darauf, Etappe 3 braucht es für Charge, Fall Back, Pile In und Consolidate. Der Code spiegelt die Anforderungen ([Domäne](../../technik/architektur/domaene.md)); soll Herumführen für alle Phasen in `domaene/querschnitt/` liegen, braucht es dort eine Anforderung.
3. Seine Ergänzung ändert Kriterien: Ein Umweg beim Herumführen „zählt gegen die Bewegungsreichweite“; heute ist *Distanz* die gerade Strecke ab Beginn der *Bewegungsphase* (Glossar, Anliegen 5180, 5400), so misst BEW-3.1. Und als Hindernis nennt er „ggf. mit Nahkampfreichweite“; heute hält BEW-6.2 davor an, statt herumzuführen.

**Kosten.** 1 und 2: Glossarzeilen *Gleiten*, *Geglitten*, neu *Ziehen*, *Herumführen*; AUF-29 wird eine Anforderung in `querschnitt/`, BEW-17 ein Verweis darauf; der Testautor benennt die Tests von AUF-29 um, kein Kriterium ändert sich, am Bildschirm nichts. 3: neue Kriterien und Akzeptanztests; technisch zählte Arbiter je Ziehen den gezeigten Weg mit, statt die gerade Strecke zu messen, und die Grenzkreise (BEW-5) zeigten nur noch eine obere Grenze.

**Gegenvorschlag.** 1 und 2 übernehmen, die Anforderung `querschnitt/ziehen.md` nimmt AUF-29 auf. Zu 3 fragst du den Stakeholder mit Regeltext (`:729`: „The distance a model moves is measured using the part of the model's base … that moves furthest along its path“) und den Entscheidungen 5180, 5400. Der Schnitt im Code ist F1 in 15900; mit deinen Wörtern schreibe ich das Item für Technikphase 11.

**Stellungnahme.**
