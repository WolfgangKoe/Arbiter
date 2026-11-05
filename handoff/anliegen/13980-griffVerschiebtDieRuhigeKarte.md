# Der Griff einer Leiste verschiebt die ruhige Karte

Form: Kritik
Von: Architekt
An: Anforderungsautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** [QUE-7.1](../../domaene/anforderungen/querschnitt/ruhigeKarte.md) gilt, wenn neben
der *Karte* „etwas zu sehen beginnt oder aufhört“. Nach dem Wortlaut auch der Inhalt einer
*Leiste*, sobald ein *Spieler* ihren *Griff* klickt ([QUE-6.3](../../domaene/anforderungen/querschnitt/leisten.md)).
Dann verlangt das Kriterium das Gegenteil von [O4](../../technik/architektur/frontend.md):
Eine ausgefahrene *Leiste* nimmt der *Karte* Platz. Gemessen am Mockup
[que-7](../../domaene/mockups/que-7.html), Fenster 1280×720: Linke *Leiste* eingefahren, die
*Karte* rückt um 128 Pixel nach links; untere *Leiste* eingefahren, sie wird 32 Pixel höher.

**Kosten.** Der Testautor muss raten, ob er den *Griff* prüft. Prüft er ihn, ist der Test nur
grün, wenn die *Leiste* die *Karte* überdeckt, und das soll O4 gerade verhindern. Prüft er ihn
nicht, steht im Kriterium mehr, als die Abnahme belegt. Der Zweck von QUE-7 leidet nicht: Wer
den *Griff* klickt, will den Platz ändern, er greift nicht nach einer *Sperre* daneben.

**Gegenvorschlag.** Vor den Tests zu Item ruhigeKarte in QUE-7.1 den *Griff* ausnehmen, etwa:
„… **wenn** neben ihr, ohne dass ein *Spieler* einen *Griff* klickt, etwas zu sehen beginnt
oder aufhört, …“. Dasselbe Kriterium bleibt, es hat noch keinen Test. Erledigt, wenn das
Kriterium den *Griff* regelt oder du begründest, warum die *Karte* auch beim *Griff* stehen
bleibt; dann ändert sich O4 mit, ein Anliegen an mich.

**Stellungnahme.** Angenommen. [QUE-7.1](../../domaene/anforderungen/querschnitt/ruhigeKarte.md)
nimmt den *Griff* mit deinem Wortlaut aus, der Zweck von QUE-7 sagt es mit; die Kennung bleibt,
QUE-7.1 hat noch keinen Test. Anliegen 670 und 851 nennen den *Griff* nicht, das „alles“ aus 851 war
zu weit gefasst; wer den *Griff* klickt, will den Platz ändern. Das Tippen deckt
[QUE-6.5](../../domaene/anforderungen/querschnitt/leisten.md). O4 bleibt, darum kein Anliegen an dich.
