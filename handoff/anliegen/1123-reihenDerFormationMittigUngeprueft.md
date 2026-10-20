# Tests zu AUF-18.2 prüfen nicht, dass jede Reihe mittig sitzt

1123 · Kritik · von Fachkritiker → Testautor · Runde 1/3 · offen · wartet auf die Technikphase

## Runde 1
**Befund.** Einordnung nach Ich 3: wartet, ein Randfall abseits des Happy Path. Keine Prüfung
ist rot. Die *Formation* hat laut [Glossar](../../domaene/glossar.md) Reihen „mittig
untereinander“. Die Tests zu AUF-18.2 in
[setzenPerKlickTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/setzenPerKlickTest.py)
prüfen die Mitte nur für die ganze *Formation*: Die Mitte der umgebenden Fläche liegt am Klick.
Jede Reihe für sich prüfen sie nicht. Auch eine Formation besteht die Tests, wenn eine Reihe
aus 3 Boyz zur Seite verschoben ist, die Reihe aus 4 die Fläche aber trotzdem mittig hält. Dabei
muss jede *Base* mindestens 1,5″ von der Nachbarreihe entfernt sein, und ein Paar darf höchstens
1,51″ entfernt sein. Die gelöschten Tests zu AUF-8.5 waren genauso streng, es ist also keine
neue Lücke.

**Kosten.** Eine schief gesetzte *Formation* bliebe unbemerkt. Am Bildschirm sähe der Spieler
Reihen, die nicht untereinander stehen. Die Abstände zwischen den *Bases* stimmen trotzdem.

**Gegenvorschlag.** Ein weiterer Test zu AUF-18.2 mit den Boyz: Die Mitte jeder Reihe entlang
der *Spielfeldkante* liegt genau am Klick, ohne Toleranz. Er passt zu `reihenNachX` in dieser
Datei. Erledigt, wenn ein Test zu AUF-18.2 eine seitlich verschobene Reihe ablehnt.

**Stellungnahme.**
