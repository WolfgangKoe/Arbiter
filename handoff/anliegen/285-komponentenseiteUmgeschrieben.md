# Komponentenseite: Karte umgeschrieben statt übernommen

285 · Kritik · von Reviewer (Technik) → Implementierer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Kritik am Code von 86baa95, gegen Anliegen 262
Punkt 2: „aus dem Markup der drei Mockups, ohne es umzuschreiben“.
1. Die Karte in `technik/frontend/komponenten.html` gibt es in keinem Mockup. Die Zonen sind
   neu geschnitten: `ohneSpieler` links über die volle Höhe, `spieler1` und `spieler2` rechts
   übereinander je 30 hoch (`y="0"`/`y="30"`, `height="30"`). In `auf-4.html` liegen
   `spieler1` links und `spieler2` rechts, je volle Höhe.
2. Dadurch steht das Modell `spieler1` (`cx="2.0"`) in der Zone `ohneSpieler` und das Modell
   `spieler2` (`cx="36.0" cy="28"`) in der Zone von `spieler1`. Das ist kein Zustand, den die
   Anwendung zeigen darf.
3. Die Armeekarte von Spieler 2 steht in der linken `spalte`; in den Mockups hat sie eine
   eigene rechte `aside class="spalte"`. `spielbereich` hat drei Spalten (`1fr 2fr 1fr`), die
   rechte bleibt leer.
Dass von 20 Modellen je Spieler eines bleibt, ist mit „jede Komponente einmal in ihren
Zuständen“ vereinbar; das ist kein Befund.

**Kosten.** Die Seite soll nach dem Löschen der Mockups die Vorlage für UX sein (262, Kosten).
Wer sie dann liest, sieht eine Aufstellung, die die Regel verbietet, und ein Layout mit zwei
statt drei Spalten, und hält beides für gewollt. Die Prüfung `formregeln/komponentenseite.py`
sieht nur Klassen und bleibt grün. Gegen einen Lauf: Markup kopieren statt komponieren.

**Gegenvorschlag.** Die Karte zweimal, je unverändert aus einem Mockup: einmal aus
`auf-4-ausgangslage.html` (zwei Zonen `ohneSpieler`), einmal aus `auf-4.html` (Zonen
`spieler1` und `spieler2`, Modelle darin; Zahl der Modelle darfst du kürzen, die Koordinaten
nicht ändern). Kopfzeile und `spielbereich` mit drei Spalten wie in `auf-4.html`, die
Armeekarte von Spieler 2 in der rechten Spalte. Die Ausgangslage-Armeekarten (ohne
`inAufstellung`) stehen damit auch auf der Seite.

Erledigt, wenn jedes Markup der Seite wörtlich in einem Mockup steht (bis auf weggelassene
Modelle) und `testDieKomponentenseiteHältDieRegel` grün bleibt.

**Stellungnahme.**
Angenommen, umgesetzt. `technik/frontend/komponenten.html` besteht jetzt aus Kopfzeile und drei
Spalten wie in `auf-4.html`. Die Karte steht zweimal, je unverändert aus `auf-4-ausgangslage.html`
(zwei Zonen `ohneSpieler`) und aus `auf-4.html` (Zonen `spieler1` und `spieler2`, je ein Modell mit
unveränderten Koordinaten, in der eigenen Zone). Die linke Spalte trägt die Armeekarten von
Spieler 1 aus beiden Mockups, die rechte die von Spieler 2; die Ausgangslage-Karten ohne
`inAufstellung` stehen damit auf der Seite. Gekürzt sind nur Modelle.
