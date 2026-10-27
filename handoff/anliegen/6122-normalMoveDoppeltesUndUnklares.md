# normalMove im Code: Doppeltes und Unklares

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: offen
Wartet auf: Technikphase 9

## Runde 1
**Befund.** Wartet (Ich 3: Namen und Ablage von Hilfsfunktionen, keine Prüfung rot), Diff
`7684034..d527459` und uncommittet `bedienung.js`.
1. [bedienung.js](../../technik/frontend/bedienung.js), `stelleDesZugs`: rechnet
   `punktAufDerKarte` zweimal, `stelleAufDerKarte` liefert denselben Punkt schon;
   `ziehenStart.vorigeStelle` wiederholt den Eintrag des gezogenen Kreises in `ziehenStart.kreise`.
2. `inKohärenz(gesetzteModelle(einheit, stellen))` steht jetzt viermal: `Aufstellung.inKohärenz`,
   `_ohneKohärenz` (aufstellen/beenden.py), `Schlacht.inKohärenz`, `gründeGegenDasBeenden`
   (bewegung/beenden.py). `gesetzteModelle` liegt in `phasen/aufstellen/beenden.py`, die
   *Bewegungsphase* und die *Schlacht* holen es von dort.
3. `Schlacht._ebeneVon` mit `verschobeneStellen` wiederholt `Aufstellung._verschobeneStellen`
   (ganze *Einheit* als *Ebene* oder das eine *Modell*).
4. [anhaltenAnDerBewegungsweite.py](../../technik/arbiter/domaene/phasen/bewegung/anhaltenAnDerBewegungsweite.py):
   `modell, *_ = neue` liest den Weg an einem beliebigen *Modell* ab und setzt stillschweigend
   voraus, dass alle denselben gehen; `max(erster - 1, 0)` schützt vor `erster == 0`, das
   nicht eintritt, solange die vorige *Stelle* innerhalb der *Bewegungsweite* liegt.
5. [schlachtrunden.py](../../technik/arbiter/domaene/querschnitt/schlachtrunden.py): Der
   Docstring nennt Zug, Schlachtrunde und Phase; das Modul führt jetzt auch das Ziehen
   (Anfangsstellen, *Ebene*, Anhalten, Sperren). Es S: der Docstring nennt die Aufgabe.
6. `testDieDistanzZähltVomAnfang…` prüft `Fraction(49, 10) <= halt`, V16 verspricht höchstens
   1/100″ davor; der Nachbartest prüft so eng.

**Kosten.** Keine in Zyklus 8. Bleiben 2 und 3, ändert sich eine Regel an mehreren Stellen
(Wir 3); 4 und 5 kosten den nächsten Leser Zeit; 6 fängt ein Anhalten 1/10″ davor nicht.

**Gegenvorschlag.**
1. `const punkt = stelleAufDerKarte(ereignis); if (!punkt) return null` und die vorige
   *Stelle* aus `start.kreise` lesen.
2. `einheitInKohärenz(einheit, stellen)` in `querschnitt/kohaerenz.py`, `gesetzteModelle`
   daneben; die Ablage entscheidet der Architekt.
3. Eine Funktion `ebeneDesZugs(auswahl, einheit, modell, stellen)` für beide.
4. `anDerBewegungsweiteAngehalten(vorige, weg, anfang)`, `neue` folgt daraus; `erster - 1`.
5. Docstring um das Ziehen ergänzen oder das Ziehen nach `phasen/bewegung/` (Architekt).
6. Untergrenze `bewegungsweiteDerTestmodelle - Fraction(1, 100)`.

**Stellungnahme.**
