# Zurücksetzen auf Stellen, die inzwischen eine andere Einheit belegt

Form: Kritik
Von: Architekt
An: Anforderungsautor
Runde: 1/3
Status: offen
Wartet auf: Domänenphase 11

## Runde 1
**Befund.** Randfall abseits des Happy Path, darum wartend; hält Plan 10 nicht auf.
[BEW-24.2](../../domaene/anforderungen/phasen/bewegung/einheitZuruecksetzen.md) und
[BEW-12.2](../../domaene/anforderungen/phasen/bewegung/vorrueckenZuruecknehmen.md) stellen
jedes *Modell* dorthin, wo es zu Beginn der *Bewegungsphase* stand. Beispiel: Die Boyz
ziehen weg, der Warboss zieht auf eine ihrer alten *Stellen*, dann „Einheit zurücksetzen“
bei den Boyz: Eine ihrer *Bases* *überdeckt* die des Warboss. Beide Kriterien sagen „steht“, nicht
*setzt*, also greift QUE-1.2 nicht; nach [Ziel](../../domaene/ziel.md) sind überdeckte
*Bases* aber nie erlaubt, auch nicht übergangen.

**Kosten.** Ein Halbsatz je Kriterium; im Code eine Prüfung mit QUE-1.2 vor dem Zurücksetzen
(D2), die es schon gibt.

**Gegenvorschlag.** In BEW-24.2 und BEW-12.2 ergänzen: „… außer eine *Base* *überdeckte*
dort eine fremde; dann *Sperre* ‚Base überdeckt‘ (QUE-1.2, QUE-1.4)“. Frag den Stakeholder,
falls er stattdessen das Zurücksetzen nur anbieten will, wenn alle *Stellen* frei sind;
meine Empfehlung ist die *Sperre*, denn sie nennt den *Grund*.
