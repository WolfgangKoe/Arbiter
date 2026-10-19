# Die Karte springt, wenn ein Grund erscheint

670 · Kritik · von Fachkritiker → Anforderungsautor · Runde 1/3 · erledigt

## Runde 1
**Befund.** Beim Durchspielen von [Review 5](../review.md), Schritt 5, im Browser (Fenster
1400×900): Ohne *Grund* ist die *Karte* 544×741 Pixel groß. Nennt Arbiter „keine Kohärenz“,
schiebt die Zeile mit dem *Grund* die *Karte* zusammen: 544×689, das *Spielfeld* wird um 7 %
kleiner gezeichnet, jeder Kreis rückt um bis zu 35 Pixel. Verschwindet der *Grund*, wächst
sie zurück. Ebenso nach der letzten *Einheit*: Ohne „an der Reihe“ wird die Kopfzeile
niedriger, die *Karte* rückt hoch und wächst (757 Pixel). Kein Kriterium regelt das:
[QUE-2](../../domaene/anforderungen/querschnitt/karte.md) verlangt nur, dass ein *Zoll*
überall gleich lang ist, nicht, dass er gleich lang bleibt.

**Kosten.** Schritt 5 lautet „Zurückziehen“: Wer nach „keine Kohärenz“ den Kreis dort greift,
wo er ihn losgelassen hat, greift daneben; mir ist genau das passiert. Am Touchgerät deckt
der Finger den Kreis ab, der Spieler merkt den Sprung erst danach. Jede *Sperre* mit *Grund*
löst ihn aus, also gerade die Momente, in denen der Spieler etwas berichtigen will. Nach
[Ziel](../../domaene/ziel.md) zieht man Abstände auf der *Karte*; ab Etappe 2 (Bewegen)
misst jeder Zug dort.

**Gegenvorschlag.** Ein Kriterium in QUE-2, etwa: „QUE-2.8 **Gegeben** die offene *Karte*,
**wenn** Arbiter einen *Grund* nennt oder nicht mehr nennt oder ein anderer *Spieler* oder
keiner *an der Reihe* ist, **dann** zeigt sie jede *Stelle* an demselben Punkt des
Bildschirms wie davor.“ Bestehende Regel (Ich 4): QUE-2.5, die du um „bleibt“ erweitern
kannst, statt ein neues Kriterium anzulegen. Wo der *Grund* steht, entscheiden danach UX und
Architekt. Ein kleines Item für Plan 6, neben „gemeinsam übergehen“, das ebenfalls *Gründe*
und Knöpfe unter der *Karte* zeigt. Erledigt, wenn das Kriterium in QUE-2 steht oder du
begründest, warum der Sprung hinzunehmen ist.

**Stellungnahme.** Angenommen, mit deinem Wortlaut, ergänzt um „zurück“ und „gemeinsam
übergehen“, die ebenfalls unter der *Karte* erscheinen. QUE-2.5 erweitern wäre eine Neufassung
gegen ihre Tests, und `karte.md` hat keinen Platz mehr (1.200 Zeichen); deshalb steht es als
eigene Anforderung [QUE-7.1](../../domaene/anforderungen/querschnitt/ruhigeKarte.md). Das Item
dazu legt der Planer an.
