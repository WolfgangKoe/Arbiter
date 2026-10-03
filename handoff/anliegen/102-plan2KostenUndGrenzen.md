# Plan 2: eine Grenze widerspricht D2, drei Kosten fehlen

102 · Kritik · von Architekt (Technik) → Planer · Runde 1/3 · erledigt

## Runde 1
Gegenstand: [Plan 2](../plan.md), Items `ausgangslage-only-war` und `sperren-beim-setzen`.
Schnitt und Reihenfolge sind gut: Item 3 erst nach 100 ist der kleinere Schritt.

**Befund.**
1. Grenze „Die Tests prüfen Sperre und Grund, nicht, wo das gesperrte Modell danach steht“
   widerspricht [D2](../../technik/architektur.md): Jeder Akzeptanztest einer Sperre prüft
   den unveränderten Zustand. Der Testautor bekommt zwei Anweisungen, der Implementierer
   muss eine wählen.
2. Item 1 heißt „reine Fachlogik“, ist es aber nicht: AUF-2.1 und AUF-2.2 verlangen die
   Armeen aus `ausgangslage.yaml`. YAML lesen kann die Domäne nicht (A1: nur
   Standardbibliothek, PyYAML gehört nicht dazu); nach A3 liest `katalog/`. Das ist der
   zweite Ordner unter `arbiter/` und löst den Importvertrag aus A1 aus (Regelumsetzer).
3. Item 2 ändert Bestehendes: `modellSetzen(modell)` bekommt eine *Stelle*, ein `Modell` eine
   *Base*. Alle 11 Aufrufe in den AUF-1-Tests brauchen dann eine gültige Stelle in der
   eigenen Zone, die Fixtures in `conftest.py` („kleine Armeen ohne Ausgangslage“) Bases.
   Der erste Abstand löst außerdem M1 aus (`messen.py`, Vertragstest), und M1 reicht nicht:
   *überdecken* ist mit dem *Abstand* nicht ausdrückbar, weil Berühren und Überdecken beide
   den Abstand 0 haben.
4. Technisches Neuland: die Grenzfälle aus 100 F2 (genau 1″, Bases berühren sich) mit
   Durchmessern in mm. Probe mit Gleitkommazahlen: Zwei Boyz (32 mm), die sich bei x = 10″
   berühren, gelten als überdeckend; genau 1″ Abstand zwischen Boy und Warboss wird an 245
   von 1.000 Stellen als „außerhalb“ gerechnet. Der Altbestand hat dasselbe Problem mit
   einem Raster aus 0,01″ und Ganzzahlen gelöst (`ArbiterMap/backend/app/domain/geometry.py`,
   Kopf), rundet dabei aber 16 mm Radius auf 0,63″. Dazu fehlt den Tests eine Lage: Wo liegt
   eine Stelle, an welcher Kante liegt die erste *Aufstellungszone*?

**Kosten.** Zu 1: Ein Item, das mitten in der Umsetzung angehalten wird. Zu 2 und 3: Der
Zyklus ist größer als der Plan sagt; ohne Nennung erscheint das Ändern grüner AUF-1-Tests als
Fehler des Testautors. Zu 4: Ohne Entscheidung vor den Tests erfindet der Testautor
Koordinaten und der Implementierer eine Toleranz, also eine Zahl ohne Begriff; rote Tests an
den Grenzfällen sehen dann wie Fachfehler aus.

**Gegenvorschlag.** Im Plan, ohne neues Item:
1. Grenze ersetzen: „Mit Sperre bleibt der Zustand unverändert (D2): Das Modell ist nicht
   gesetzt. Stehenbleiben mit Grund kommt später (16 F4).“ AUF-3.1 sagt dasselbe schon
   („ohne Sperre ist es danach gesetzt“).
2. Item 1: „liest `ausgangslage.yaml` und `onlyWar.yaml` über `katalog/`, ohne Datenbank;
   Importvertrag A1 durch den Regelumsetzer im selben Zyklus“. Die Datenbank aus A3 wartet
   auf ihren Auslöser.
3. Item 2: „ändert die AUF-1-Tests: Setzen mit Stelle, Modelle mit Base“.
4. Item 2 ist technisches Neuland (Ausnahme in `prozess/ablauf.md`, Technikphase): Vor dem
   Testautor legt der Architekt nach einem Wegwerf-Versuch in `architektur.md` fest, wie eine
   Stelle angegeben wird (Ursprung, Achsen, Lage der Zonen) und womit gerechnet wird. Mein
   Vorschlag für den Versuch: exakte Brüche (`fractions.Fraction`, Standardbibliothek) und
   Vergleiche über Quadrate, ohne Wurzel; dann gelten 25,4 mm je Zoll und die Grenzfälle ohne
   Toleranz. Dazu M1 um *überdecken* ergänzt.

**Stellungnahme.** Alle vier angenommen, im Plan unter Empfehlung und Grenzen; die Items
heißen nicht mehr „reine Fachlogik“.
