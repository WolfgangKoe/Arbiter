# Ablaufplan zeigt weniger als gebaut, und auf-19 eine Sperre, die nicht greift

970 · Kritik · von Fachkritiker → Ux · Runde 2/3 · erledigt

## Runde 1
**Befund.** Hält auf (Ich 3): Der Stakeholder gibt Plan 6 nach dem
[Ablaufplan](../../domaene/mockups/ablaufplan.html) frei, weil er dort „so wenig Knöpfe und
Hinweise wie in ArbiterMap“ sehen will. Zwei Bilder zeigen nicht, was er nach Zyklus 6 sieht.
1. Knopf und Abzeichen. „Aufstellen der Einheit beenden“ steht gebaut immer da
   ([seite.js](../../technik/frontend/seite.js), `knopfGruppe`; AUF-7.4 sperrt den Klick ohne
   *Einheit in Aufstellung*, getestet). In auf-11-rolloff, auf-11-gewinner, auf-11-zone,
   auf-18-ausgewaehlt und auf-10 fehlt er. Ebenso zeigt die *Ablage* gebaut das Wort „in
   Aufstellung“ ([index.html](../../technik/frontend/index.html), `einheitenKartenAbzeichen`),
   auf-18, auf-19, auf-20, auf-21 nicht. Kein Kriterium der drei Items nimmt Knopf oder Wort weg.
2. [auf-19](../../domaene/mockups/auf-19.html) zeigt eine *Sperre*, die nach den Kriterien nicht
   greift: Das neunte *Modell* der Boyz steht von (6.89, 30.0) auf (6.89, 33.4) verschoben auf
   der *Base* eines *Modells* derselben *Einheit*, bei *Ebene* „Ganze Einheit“. Ein Klick *setzt*
   die *Formation* regelmäßig (AUF-18.2, [Glossar](../../domaene/glossar.md) *Formation*), ein
   Block sperrt sich nicht an der eigenen *Einheit* (AUF-24.2). So entsteht das Bild nur mit
   „Einzelmodelle“; dann nimmt *zurück* aber nur dieses *Modell* zurück (AUF-9.3), nicht „die
   Einheit“, wie der Ablaufplan darunter sagt (das gilt nach AUF-19.2 nur für den Klick).

**Kosten.** Gibt er auf diese Bilder frei, sieht er im Review den Knopf vor dem *Roll-off* und
das Wort an der *Ablage* wieder, also genau das, woran Plan 6 schon einmal scheiterte. auf-19
lässt ihn glauben, seine eigene *Einheit* sperre sich selbst, was 920 gerade behoben hat.

**Gegenvorschlag.**
1. Die Bilder zeigen Knopf und Wort wie gebaut. Hältst du das schlanke Bild für seinen Wunsch
   (962 verlangte das Kennzeichen „so leise wie in ArbiterMap“), nenne in deiner Stellungnahme
   je Element das Kriterium, damit der Planer es einem Item zuordnet: Das Wort zu streichen
   ändert kein Kriterium (AUF-4.5 verlangt keins); den Knopf nur mit *Einheit in Aufstellung*
   zu zeigen braucht ein neues Kriterium vom Anforderungsautor und macht AUF-7.4 am Bildschirm
   unerreichbar.
2. auf-19 zeigt den Fall des Happy Path: Der Warboss steht schon, die Boyz werden per Klick
   daneben *gesetzt*, eines steht auf seiner *Base*, *gesperrt* mit ‚Base überdeckt‘ und
   „zurück“, das die ganze *Formation* in die *Ablage* bringt (AUF-19.1, 19.2).

Erledigt, wenn: Jedes Bild des Ablaufplans zeigt, was nach den drei Items und dem Gebauten am
Bildschirm steht, oder deine Stellungnahme nennt das Kriterium für jede Abweichung; auf-19 zeigt
eine *Sperre*, die nach AUF-19.1 greift.

**Stellungnahme.** Der Befund trifft zu, nachgebessert. 1: Alle Bilder zeigen „Aufstellen der Einheit beenden“ (AUF-7.4, 12.7) und das Wort „in Aufstellung“ an der *Ablage* der *Einheit in Aufstellung* (AUF-4.5) wie gebaut; keine Abweichung, kein neues Kriterium nötig. 2: [auf-19](../../domaene/mockups/auf-19.html) und [auf-19-ohneUmschalter](../../domaene/mockups/auf-19-ohneUmschalter.html) zeigen jetzt den Klick: Der Warboss steht, ein *Modell* der Boyz liegt auf seiner *Base*, *gesperrt* mit ‚Base überdeckt‘ (AUF-19.1) und „zurück“ (AUF-19.2); der Ablaufplan beschreibt es so.

## Runde 2
**Befund.** 1 erledigt. auf-19 und -ohneUmschalter: Der Warboss steht, die *Ablage* zeigt ihn mit „1“ (AUF-4.3); Spieler 2 hat nichts *gesetzt*, Spieler 1 ist wieder dran (AUF-1.7).

**Kosten.** Ein Bild, das nie am Bildschirm steht.

**Gegenvorschlag.** Warboss nicht in der *Ablage*, Overlord in Zone 2.

**Stellungnahme.** Der Befund trifft zu, umgesetzt: In [auf-19](../../domaene/mockups/auf-19.html) und [auf-19-ohneUmschalter](../../domaene/mockups/auf-19-ohneUmschalter.html) steht der Warboss nur auf der *Karte*, nicht mehr in der *Ablage* (AUF-4.3: *aufgestellte* *Einheiten* zeigt sie nicht); der Overlord steht in Zone 2 und fehlt in der *Ablage* von Spieler 2, damit ist Spieler 1 wieder *an der Reihe* (AUF-1.7).
