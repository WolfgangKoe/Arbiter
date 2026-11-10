# Fliegen: „gemeinsam übergehen“ bleibt nach der Sperre angeboten

Form: Kritik
Von: Planer
An: Anforderungsautor
Runde: 1/3
Status: abgelehnt

## Runde 1
**Befund.** Hält den Happy Path nicht auf, betrifft erst Etappe 7. Zu
[BEW-18.6](../../domaene/anforderungen/phasen/bewegung/fliegen.md) und
[QUE-1.4](../../domaene/anforderungen/querschnitt/setzen.md): Wählen die *Spieler* für die
Spinne *gemeinsam übergehen* und findet BEW-18.7 keine *Stelle*, sperrt Arbiter mit ‚Base
überdeckt‘ ([schlachtrunden.py](../../technik/arbiter/domaene/querschnitt/schlachtrunden.py),
Zeile 149). Nach dem Code bricht `gemeinsamÜbergehen` dort ab, bevor das Angebot endet; der
Knopf „gemeinsam übergehen“ bliebe also stehen, jeder weitere Klick sperrt erneut. QUE-1.4
sagt: Nach einer *Sperre* nach QUE-1.2 bietet Arbiter *gemeinsam übergehen* nie an. Kein
Kriterium sagt, ob das auch für ein Angebot gilt, das vor der *Sperre* nach BEW-8.3 bestand.
Nach Anliegen 16100 überdeckt eine *Base* nie eine
andere; entfällt BEW-18.6 darum ([16150](16150-basesNieUeberdeckt.md)), erübrigt sich dies.

**Kosten.** Mit BEW-18.6 ein Halbsatz oder ein Kriterium, ein Test; im Code eine Zeile.
Ohne Klärung prüft der Test zu BEW-18.6 in Etappe 7 nur die *Sperre*, der Knopf bliebe
unbemerkt stehen.

**Gegenvorschlag.** Mit Etappe 7 in BEW-18.6 festlegen, ob Arbiter nach dieser *Sperre*
*gemeinsam übergehen* weiter anbietet; nach QUE-1.4 wohl nicht, dann steht die Spinne, wo
Arbiter sie angehalten hatte, und der Knopf verschwindet. Ist es unklar, frage den
Stakeholder mit Empfehlung.

**Stellungnahme.** Abgelehnt, weil überholt; die Frage verwerfe ich. Der Stakeholder hat in
Anliegen 16100 entschieden, dass eine *Base* nie eine andere *überdeckt*, auch nicht nach
*gemeinsam übergehen*. Damit entfällt der Fall der *Sperre* aus BEW-18.6: Nach dem Übergehen
ist immer zumindest die *Stelle* frei, an der das *Modell* vor dem Ziehen stand (Anliegen
13020). Was mit BEW-18.6 geschieht, entscheide ich in [16150](16150-basesNieUeberdeckt.md),
dessen Gegenvorschlag auch dieses Anliegen nennt: Bleibt BEW-18.6 mit neuer Begründung, lege
ich dort im selben Kriterium fest, ob das Angebot nach der *Sperre* endet. Eine Anforderung
ändere ich hier nicht. Planer: nachprüfen und `erledigt` setzen oder eine neue Runde.
