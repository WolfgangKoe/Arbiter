# Bases blitzen nach dem Loslassen an der alten Stelle auf

1640 · Kritik · von Stakeholder → Implementierer · Runde 1/3 · offen

## Runde 1
**Befund.** „Nachdem ich eine Einheit infolge des Ziehens der Bases loslasse, blitzen die
Bases nochmal kurz an der ursprünglichen Position auf. Das dürfte ein Bug sein. Das Resetten
eines Zugs brauchen wir noch als Feature, aber dieses ‚Blitzen‘ sollte nicht geschehen.“

(Fachkritiker) Am laufenden Arbiter nachgestellt: Spieler 2 *setzt* seine Necron Warriors per
Klick, zieht ein *Modell* nach rechts und lässt im *Spielfeld* los. Beim Halten zeigt die
*Karte* den Block an der Vorschau. Beim Loslassen springen alle Kreise an ihre *Stelle* vor dem
Ziehen zurück, erst die Antwort auf das Loslassen zeichnet sie am Ziel. Ohne Verzögerung liegen
im Testbrowser 5 ms dazwischen; kommt die Antwort 0,5 s später, steht der Block so lange
sichtbar am Anfang. Ursache: `ziehenBeenden` in [seite.js](../../technik/frontend/seite.js)
ruft `ziehenZurücknehmen(start)` vor `modellLoslassen`. Seit dem Anhalten
([V10](../../technik/architektur/handlungen.md)) nimmt es alle mitgezogenen Kreise zurück,
vorher nur den gezogenen.

Kriterium: Keines regelt den Augenblick zwischen Loslassen und Antwort. AUF-24.1 und 26.4
(beim Halten) und AUF-8.2 und 21.1 (nach dem Loslassen) sind erfüllt, darum fängt auch kein
Akzeptanztest das Blitzen. ArbiterMap lässt die Kreise bis zur Antwort am Ziel stehen und nimmt
sie nur bei einem Fehler zurück (`ArbiterMap/frontend/static/js/model_drag.js:1605`, `:1609`).

Bezug: [1610](1610-ziehenUeberDieKanteUndGreifpunkt.md) Punkt 1 ist ein anderer Fall: Lässt
man über der Kante los, schickt die Seite nichts, und der Block bleibt nach AUF-16.6 am Anfang
stehen. Das ist eine Frage an die Anforderung, nicht an den Code. Das Blitzen dagegen trifft
jedes Loslassen im *Spielfeld*. Folgt der Stakeholder dort der Empfehlung, blitzt es ohne
Abhilfe auch an der Kante. [1590](1590-rasterMutantUndRaenderDerAbfrage.md) Punkt 3 (eine alte
Antwort der Abfrage setzt Kreise nach dem Zug) ist behoben und nicht die Ursache: Nach dem
Loslassen schreibt keine Abfrage mehr.

Hinweis an den Anforderungsautor, kein Befund: Der Stakeholder will einen Zug zurücksetzen
können. Bisher gibt es nur „zurück“ bei einer *Sperre* (AUF-13.1) und das *Zurücklegen* in die
*Ablage* (AUF-23). Ob und wie ein Verschieben zurückgesetzt wird, fragst du in der
Domänenphase.

**Kosten.** Bei jedem Loslassen in den Schritten 4 und 5 aus [Plan 6](../plan.md) springt
die *Einheit* für einen Augenblick an den Anfang zurück, und der Spieler hält das für ein
Zurücksetzen. Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): wartet. Kein
Kriterium ist verletzt und kein Schritt fehlt, also trifft keiner der Fälle von „hält auf“
zu. Der Stakeholder kann es mit seinem Kommentar zu Review 6 vorziehen. Die Abhilfe kostet
wenige Zeilen in seite.js.

**Gegenvorschlag.** Wie ArbiterMap: Beim Loslassen bleiben die Kreise, wo die *Karte* sie
zuletzt zeigte, bis `zeichnen` die Antwort zeichnet. Ohne Ziel zeichnet
`zeichnen(letzterSpielstand)` ohnehin neu. Prüfe, ob `darunter` das Zurücknehmen noch braucht
(Zweck des alten Kommentars: Der Kreis lag unter dem Zeiger), sonst entfällt der Aufruf in
`ziehenBeenden`.

**Stellungnahme.**
Angenommen. `ziehenBeenden` nimmt die Kreise nicht mehr zurück; sie bleiben, wo die *Karte* sie zuletzt zeigte, bis `zeichnen` die Antwort zeichnet. Der Aufruf entfällt dort ganz: `darunter` wird nur ohne *Stelle* im *Spielfeld* gefragt, dann liegt kein Kreis unter dem Zeiger. Abbrechen nimmt weiter zurück.
Kommentar: BItte rückmelden, wenn die Arbeit erledigt ist und ich es prüfen kann wie in der Review. Ich setze das Anliegen so lange auf "offen".
Stellungnahme: Die Arbeit ist erledigt und zum Prüfen bereit: Beim Loslassen bleiben die Kreise am Ziel stehen, bis die Antwort sie zeichnet ([seite.js](../../technik/frontend/seite.js), `ziehenBeenden`). Alle Unit- und Akzeptanztests der Phasen sind grün, die Seite habe ich nicht im Browser angesehen. Der Status bleibt bei dir.
