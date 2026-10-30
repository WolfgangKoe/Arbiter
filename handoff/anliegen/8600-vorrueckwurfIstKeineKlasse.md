# Vorrückwurf ist keine Klasse

Form: Kritik
Von: Architekt
An: Implementierer
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Hält auf (Prüfung rot), Arbeitsbaum zu Item grenzkreise, Abweichung von
[V20](../../technik/architektur/vertrag/bewegung/grenzkreise.md) nach Glossar und Anforderung.
1. `Kreis` zu `Grenzkreis` in
   [grenzkreise.py](../../technik/arbiter/domaene/phasen/bewegung/grenzkreise.py): richtig.
   V20 nannte einen Namen, der nicht im [Glossar](../../domaene/glossar.md) steht, obwohl
   V21 schon „je *Grenzkreis* oder *Einhüllende* ein Eintrag“ sagt. Der Fehler liegt im
   Vertrag; ich ziehe V20 nach, sobald dein Lauf endet.
2. `Grenze` zu `Einhüllende`: richtig, gleicher Grund; BEW-11.3, 11.5 und 13.1 nennen den
   Eintrag so. Die Abfrage `grenzen`, der Schlüssel `schlacht.grenzen` und `grenze.js`
   bleiben, wie V21 sie nennt; zehn Akzeptanztestdateien lesen den Schlüssel. Eine
   Unschärfe im Glossar bei nur einem *Modell*: [8601](8601-einhuellendeEinesGrenzkreises.md).
3. `Vorrücken` zu `Vorrückwurf` in
   [vorruecken.py](../../technik/arbiter/domaene/phasen/bewegung/vorruecken.py): falsch,
   und die Prüfung bleibt rot:
   `python3 prozess/pruefungen/gemeinsam/lauf.py formregeln.glossar` meldet
   „Klasse Vorrückwurf steht nicht im Glossar“. Das Glossar führt den Code-Bezeichner
   klein (`vorrückwurf`), als Wert: „Ein W6 … je *Einheit* einen“. Die Klasse ist aber kein
   Wurf, sondern hält für alle *Einheiten* der *Bewegungsphase*, ob sie wartet, *vorgerückt*
   ist und mit welchem Wurf. So liest sich `self._bewegungsphase.vorrücken.angeboten(einheit)`
   als „der Vorrückwurf ist angeboten“; BEW-5.1 sagt „bietet Arbiter Vorrücken an“.
   Mit einer Großschreibung im Glossar würde die Prüfung grün und der Begriff falsch.
   V20 schreibt keine Klasse vor, nur was `vorruecken.py` hält.

**Kosten.** Am Bildschirm nichts. Bleibt es, ist die DoD rot, und ein Leser hält einen
Zustand aller *Einheiten* für einen Wurf. Umbau: eine Klasse weg, etwa 25 Zeilen in
`Bewegungsphase`, die Aufrufe in
[schlachtrunden.py](../../technik/arbiter/domaene/querschnitt/schlachtrunden.py) werden
kürzer, `vorrueckenTest.py` zieht nach. Ein neuer Glossarbegriff wäre erfunden (Ich 1).

**Gegenvorschlag.** Keine eigene Klasse: Der Zustand gehört zur *Bewegungsphase* wie
`_stellenZuBeginn`. `Bewegungsphase` hält zwei Sammlungen statt `None` als Zeichen für
„wartet“, `_wartendeEinheiten: set[Einheit]` und `_vorrückwürfe: dict[Einheit, int]`, und
gibt die Wörter der Anforderung als Methoden: `vorrückenAngeboten(einheit)` (in keiner,
BEW-5.1), `vorrückenBeginnen(einheit)` (5.2), `wartetAufVorrückwurf(einheit)`,
`vorrückwurf(einheit) -> int | None` (5.3), `vorgerückt(einheit)`,
`vorrückenZurücknehmen(einheit)` (12.2); die Bedingung von 12.1 ist „wartet oder
vorgerückt“. `Schlacht` ruft dann `self._bewegungsphase.wartetAufVorrückwurf(einheit)` und
spiegelt die Namen, die sie schon hat. `vorruecken.py` entfällt; V20 ziehe ich mit 1 und 2
nach. Wird `Bewegungsphase` dadurch zu groß für die Schwellen der
[DoD](../../prozess/ablauf/dod.md), bleibt `vorruecken.py` mit Funktionen über diese zwei
Sammlungen, ohne Klasse, wie `gesetzteModelle` in `querschnitt/setzen.py`.

**Stellungnahme.** Angenommen, so umgesetzt: Die Klasse `Vorrückwurf` und
`vorruecken.py` entfallen. `Bewegungsphase` hält `_wartendeEinheiten` und `_vorrückwürfe` und
bietet `vorrückenAngeboten`, `vorrückenZurücknehmenAngeboten`, `vorrückenBeginnen`,
`vorrückenZurücknehmen`, `wartetAufVorrückwurf`, `vorgerückt`, `vorrückwurf`; `Schlacht` ruft
sie. Die Einheitstests stehen in `bewegungTest.py`. `Grenzkreis` und `Einhüllende` bleiben.
