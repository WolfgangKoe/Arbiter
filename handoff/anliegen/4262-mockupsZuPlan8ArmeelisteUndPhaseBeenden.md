# Mockups zu Plan 8: Armeeliste, Phase beenden, Ende der Schlacht

Form: Kritik
Von: Fachkritiker
An: Ux
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Hält auf (Ich 3: Schritt des Happy Path fehlt, im Mockup).
1. „Phase beenden“ fehlt in der *Bewegungsphase*:
   [bew-1](../../domaene/mockups/bew-1.html) und [bew-2](../../domaene/mockups/bew-2.html)
   zeigen nur „Bewegung der Einheit beenden“. QUE-10.2 gilt in jeder *Phase*; ohne den Knopf
   kommt man aus der *Bewegungsphase* nicht heraus (Plan 8, Schritte 2 und 3).
2. Die *Armeelisten* führen nach der *Aufstellung* alle *Einheiten* mit der Zahl ihrer
   *Modelle* (Boyz 10, Warboss 1, …), in [que-9](../../domaene/mockups/que-9.html),
   [que-10](../../domaene/mockups/que-10.html), bew-1 und bew-2. Die *Armeeliste* führt nur
   nicht *aufgestellte* *Einheiten* (Glossar); so ist es gebaut
   (`technik/arbiter/web/kennungen.py:46`), nach der *Aufstellung* ist sie leer. bew-1 und
   bew-2 zeigen dazu Boyz in der *Armeeliste* *ausgewählt*: einen Weg zur *Auswahl*, den
   keine Anforderung kennt (siehe Anliegen 4260, Punkt 3).
3. Plan 8, Schritt 4 („Nach der fünften *Schlachtrunde* endet die *Schlacht*“, QUE-10.4) hat
   kein Mockup; offen ist dazu deine Frage
   Anliegen 4200 an den Architekten.

**Kosten.** Der Implementierer baut nach dem Mockup: ohne „Phase beenden“ in der
*Bewegungsphase* bleibt die Partie dort stehen; mit gefüllten *Armeelisten* baut er gegen
Glossar und Bestand oder sucht eine *Auswahl* über die *Armeeliste*, die es nicht gibt.
Ohne Bild für das Ende sieht der Stakeholder Schritt 4 erst am fertigen Bildschirm.
Nachbessern: ein Knopf in zwei Dateien, die *Einheitenkarten* aus vier Dateien löschen,
ein Mockup mehr.

**Gegenvorschlag.**
1. „Phase beenden“ in bew-1 und bew-2 neben „Bewegung der Einheit beenden“.
2. Leere *Armeelisten* in allen vier Mockups (que-9 nur mit „Erster Zug“). Wie die
   *Einheit* in bew-1 *ausgewählt* erscheint, nach der Stellungnahme zu 4260: bei (a) nur
   am *Modell* auf der *Karte*, bei (b) gar nicht.
3. Ein Mockup zum Ende der *Schlacht*, sobald 4200 beantwortet ist.

**Stellungnahme.** Punkt 1 und 2 sind umgesetzt, Punkt 3 bleibt offen.
1. [bew-1](../../domaene/mockups/bew-1.html) und [bew-2](../../domaene/mockups/bew-2.html)
   zeigen „Phase beenden“ neben „Bewegung der Einheit beenden“.
2. In [que-9](../../domaene/mockups/que-9.html), [que-10](../../domaene/mockups/que-10.html),
   bew-1 und bew-2 sind die *Armeelisten* leer; que-9 zeigt nur „Erster Zug“. In bew-1 und
   bew-2 ist keine *Einheit* *ausgewählt*; zu sehen ist nur das *ausgewählte* *Modell* auf
   der *Karte*. Das ist Variante (a) aus deinem Gegenvorschlag.
3. Gezeichnet nach der Antwort des Architekten auf
   Anliegen 4200:
   [que-10-ende](../../domaene/mockups/que-10-ende.html) zeigt „Schlacht beendet“ unter
   „ARBITER“, kein *Spieler* ist *am Zug*, kein Knopf. Dazu heißt es in que-10, bew-1 und
   bew-2 jetzt `amZug` und `kopfzeileAmZug`.
