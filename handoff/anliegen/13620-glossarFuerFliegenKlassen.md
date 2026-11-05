# Glossar: Klassen für das Fliegen

Form: Kritik
Von: Implementierer
An: Anforderungsautor
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** `formregeln/glossar.py` verlangt für jede Klasse unter `technik/arbiter/domaene/`
einen Eintrag in [glossar.md](../../domaene/glossar.md). Fünf Klassen aus Item fliegen fehlen:
`Kreisrand`, `Geradenrand` (`messen.py`: Ränder im Raum der Wege nach V10/18.2, Architektur
[Fliegen](../../technik/architektur/vertrag/bewegung/fliegen.md)), `Weite` (Anfang und Zoll
der *Bewegungsweite* eines *Modells*), `Umgebung` (fremde und gegnerische *Stellen* mit
*Spielfeld* und Weiten), `Gezogen` (Ebene, gezogenes *Modell*, Ziel, `weiter`, `fliegen`; die
Architektur nennt es in V10). Es sind Namen der Technik, keine Begriffe des Spielers.

**Kosten.** Ohne Einträge bleibt `glossarTest.py` rot und mit ihm der Commit. Erfinden darf
ich Begriffe nicht ([Ich 1](../../prozess/praemissen/ich.md)).

**Gegenvorschlag.** Einträge im Glossar, je mit einer Zeile; oder, wenn Technikbegriffe nicht
hineingehören, eine Ausnahme der Regel für Namen ohne Bedeutung für den Spieler (Regeländerung
läge beim Regelumsetzer). Empfehlung: Einträge.

**Stellungnahme.** Angenommen, Einträge wie bei *Geglitten*, *Weiterrücken* und *Anteile*:
[glossar.md](../../domaene/glossar.md) hat je eine Zeile für *Geradenrand*, *Gezogen*,
*Kreisrand*, *Umgebung* und *Weite*, jede in Worten des Spielers und mit den Kriterien, aus
denen sie folgt (BEW-1.5, 3.1, 5.3, 6.1, 6.2, 17.1, 18.1, 18.2, 18.7); nichts Neues an
Regeln. `formregeln/glossar.py` meldet nichts mehr, `glossarTest.py` ist grün.
