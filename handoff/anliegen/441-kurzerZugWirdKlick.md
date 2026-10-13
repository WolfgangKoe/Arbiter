# Ein kurzer Zug wird zum Klick, architektur.md über dem Höchstmaß

441 · Kritik · von Reviewer → Architekt · Runde 1/3 · angenommen

## Runde 1
**Befund.** DoD über das Inkrement von Plan 5.
1. [V8](../../technik/architektur/handlungen.md): „Endet das Ziehen über dem Element, an dem
   es begann, ist es ein Klick“. `ziehenBeenden` in
   [seite.js](../../technik/frontend/seite.js) stellt dafür den Kreis an seinen alten Platz
   und fragt, was unter dem Zeiger liegt. Endet der Zeiger innerhalb des alten Kreises, geht
   keine Anfrage. Ein *Modell* um weniger als seinen Radius zu verschieben (0,63″ bei 32 mm)
   gelingt also weder mit Maus noch Finger, etwa um die *Kohärenz* knapp herzustellen; es
   springt still zurück, gegen AUF-8.2.
2. [architektur.md](../../technik/architektur.md) hat 6.043 Zeichen, Höchstmaß 6.000
   ([Kennzahlen](../../prozess/kennzahlen.md)); vor Plan 5 waren es 5.985.

**Kosten.** (1) Der *Spieler* muss das *Modell* erst weit weg und dann zurückziehen; das
Verhalten kennt kein Test. (2) Die Datei darf nicht weiter wachsen.

**Gegenvorschlag.** Bestehende Regel (Ich 4): V8, angepasst.
1. Ein Klick ist ein Ziehen, dessen Zeiger sich insgesamt weniger als eine feste Zahl Pixel
   bewegt hat (etwa 4 px, gemessen an `ziehenStart`), unabhängig vom Element darunter; der
   Testautor ergänzt den Bildschirmtest „Modell um 0,3″ ziehen“ zu AUF-8.2.
2. architektur.md unter 6.000 Zeichen kürzen oder einen Abschnitt nach `architektur/`
   auslagern.

**Stellungnahme.** Angenommen, (1) mit einer Änderung.
1. [V8](../../technik/architektur/handlungen.md) neu: Ein Zug beginnt erst, wenn der Zeiger
   in x oder y mehr als 4 px (`zugschwelle`) von seinem Startpunkt abweicht; erst dann folgt
   das Element dem Zeiger. Ohne Zug ist es ein Klick (auf einer *Einheit* der *Ablage*
   Auswahl nach V2, sonst nichts), mit Zug Loslassen, auch über dem Startelement. Vorbild:
   `dragStartThresholdPx` in ArbiterMap, ebenfalls 4 px. Änderung gegenüber dem Vorschlag:
   Die Schwelle entscheidet beim ersten Überschreiten, nicht beim Loslassen. Sonst bliebe
   eine tote Zone von 4 px; bei etwa 12 px je Zoll sind das 0,3″, genau die Strecke des
   vorgeschlagenen Tests. Jetzt kann der *Spieler* ein *Modell* auch um 0,1″ versetzen: über
   die Schwelle ziehen, zurück, loslassen. Was er sieht, gilt: Ein *Modell*, das sich noch
   nicht bewegt hat, springt auch nicht zurück. Den Test bestellt
   [Anliegen 460](460-kurzerZugImBildschirmtest.md) beim Testautor (0,5″ statt 0,3″,
   Begründung dort); danach macht der Implementierer `ziehenBeenden` nach V8 grün.
2. [architektur.md](../../technik/architektur.md) hat 5.949 Zeichen: zweites Beispiel im
   Grundschnitt und ein Verweis gestrichen; alle Architekturdateien zusammen 22.928.
