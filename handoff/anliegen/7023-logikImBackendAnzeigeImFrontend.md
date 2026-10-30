# Logik im Backend, Anzeige im Frontend

Form: Fragen
Von: Architekt
An: Stakeholder
Runde: 2/3
Status: angenommen

## Runde 1
**Befund.** Deine Frage: Linien blockieren im Backend, das Frontend zeigt sie nur und hebt
eine wählbare durch die Dicke hervor. Ja, so gilt es schon (Anliegen 6995 F2, F3;
[W2](../../technik/architektur/web.md#aufbau): Regeln und Rechnen nur in der Domäne). Ich
schärfe es an einer Stelle: Nicht die Linie blockiert, sondern die Regel. Arbiter hält an
der *Bewegungsweite* oder 1″ vor dem Gegner an, ohne dass eine Linie existiert
([V16](../../technik/architektur/vertrag/bewegung/handlungen.md)); der *Grenzkreis* ist nur Anzeige
(Glossar). Beides rechnet die Domäne aus denselben Werten, darum passen sie zusammen. In den
Verträgen zu Plan 9:
- Welche Kreise, wo, wie groß, ob `wählbar`: Domäne, der Spielstand nennt sie
  ([Grenzkreise](../../technik/architektur/vertrag/bewegung/grenzkreise.md)).
- Ein Klick in einen Ring: Die Seite schickt nur den Punkt, die Domäne entscheidet, welcher
  Wurf es ist oder ob die *Auswahl* fällt (V19, V21). Ebenso *Ebene* in der *Schlacht* (V14)
  und „gemeinsam übergehen“ (V18).
- Dicke, Farbe, Strichart: nur `komponenten.css`; das Frontend zeichnet, rechnet nicht.

Abweichung heute: In der *Aufstellung* entscheidet die Seite, ob ein Klick *Ebene* (V9) oder
*Auswahl* (V14) ist, und nur `web/` prüft, dass die *Ebene* ein *gesetztes* *Modell* ist
(6995 Befund 3, dort F2 A: mit dem Umbau zu `anwendung/`).

**Kosten.** Am Bildschirm gleich. Code: je Klick eine Anfrage, die Seite wartet auf die
Antwort (lokal wenige ms). Token: keine weiteren, die Verträge stehen so.

**Gegenvorschlag.** Siehe F1.

**Stellungnahme.**

**F1 · Soll auch die Aufstellung den Klick ganz der Domäne überlassen?**
A: Ja, mit dem Umbau zu `anwendung/` (6995 F2 A): ein Klick auf ein *Modell* immer V14, die
Domäne wählt *Auswahl* oder *Ebene*, V9 entfällt.
B: Sofort als Item in Plan 10.
C: Bleibt wie heute.
Empfehlung: A; heute fängt `web/` den Fall ab, ein eigener Umbau kostet ein Item ohne
Wirkung am Bildschirm.
Antwort: A, bitte meinen Kommentar beachten
Kommentar: Ich verstehe diese Frage nicht.

**Klärung.** Ein Klick auf einen Boy heißt zweierlei: Sind die Boyz nicht *ausgewählt*,
werden sie es; sind sie es schon, zieht danach nur dieser Boy (*Ebene*), noch ein Klick:
wieder alle. F1 fragt nicht, was du siehst, sondern wer die beiden Fälle unterscheidet.
- Heute die Seite im Browser: Sie schaut, ob sie die Boyz als *ausgewählt* gezeichnet hat,
  und schickt Arbiter „wähle die Boyz aus“ oder „nur dieser Boy zieht“.
- Ab Item 3 in der *Bewegungsphase* Arbiter: Die Seite schickt nur „Boy angeklickt“,
  Arbiter entscheidet nach seinem Spielstand. Beim Aufstellen bliebe es bei der Seite.

Warum das zählt: Wer entscheidet, muss den Stand kennen. Arbiter kennt ihn sicher, die Seite
nur so, wie sie ihn zuletzt gezeichnet hat, etwa wenn ihr Arbiter auf einem zweiten Gerät
offen habt (QUE-3.2). Und dieselbe Regel stünde an zwei Stellen, die auseinanderlaufen können.
Am Bildschirm ändert sich bei A, B und C nichts:
- A: Das Aufstellen wird wie die *Bewegungsphase*, aber erst, wenn ohnehin an diesem Code
  umgebaut wird (dein 6995 F2 A); kostet nichts extra.
- B: Dasselbe sofort als eigenes Item in Plan 10; kostet ein Item, das du nicht sehen kannst.
- C: Es bleibt; dann gibt es für denselben Klick zwei Wege, je nach Phase.

Bei dir liegt es, weil es um Arbeit ohne Wirkung am Bildschirm geht: wann sie kommt, entscheidest
du (Absicht 4). Meine Empfehlung bleibt A.
Kommentar: Sei meinen "Wünschen" gegenüber bitte immer kritisch. Nach meinem Verständnis soll sich das Frontend ja nur um die Anzeige kümmern und enthält entsprechend nur die Logik, die es dafür braucht. Ob ein Modell oder dessen ganze Einheit ausgewählt ist, ist ja etwas, an dem das Backend beteiligt ist, weil es die Positionen protokollieren und persistieren muss. Mir fällt es schwer, hier die Trennung zu machen. Hilf mir dabei. Was macht man typischerweise? Erkläre es mir auf verständliche Weise.

## Runde 2
**Befund.** Dein Verständnis stimmt, und so ist Arbiter gebaut; ich korrigiere nur einen
Punkt. Die *Auswahl* gehört zum Spielstand, den Arbiter speichert: Öffnest du die Seite neu,
ist dieselbe *Einheit* *ausgewählt* (QUE-3.2). Ins *Protokoll* kommt sie nicht, denn Auswählen
ist keine Handlung (Glossar, *ausgewählt*).

Was man typischerweise macht, als Faustregel mit zwei Fragen:
1. Ist es eine Regel, oder muss es auf zwei Geräten gleich sein? Dann entscheidet das
   Backend. Beispiele: ob ein Klick die Boyz *auswählt* oder nur einen Boy zur *Ebene* macht,
   wo ein *Modell* anhält, welcher *Grund* sperrt, welcher *Grenzkreis* *wählbar* ist.
2. Betrifft es nur, wie es aussieht oder sich anfühlt? Dann das Frontend. Beispiele: Farbe
   und Dicke einer Linie, das *Modell* folgt beim Ziehen dem Finger, eine *Leiste* fährt ein.

Das Frontend meldet also nur, was der Spieler getan hat („Boy angeklickt“, „hier
losgelassen“), und zeichnet die Antwort. Selbst die Vorschau beim Ziehen (BEW-1.7) fragt es
bei Arbiter ab, statt selbst zu rechnen. Man nennt das ein dünnes Frontend.

Das Gegenbeispiel kennst du aus ArbiterMap: Dort entschied
`frontend/static/js/model_selection.js` allein im Browser, was ein Klick auswählt
(`cycleSelectionForModel`, Zeile 336); die Datei hat 929 Zeilen, viele davon Erklärungen zu
Sonderfällen wie dem Doppelklick. Positiv dagegen `backend/app/domain/rule_checks.py`: Regeln
an einer Stelle, ohne Browser prüfbar.

Die eine Ausnahme in Arbiter ist genau, was F1 meinte: Beim Aufstellen schaut die Seite noch
selbst nach, ob die *Einheit* schon *ausgewählt* ist, und schickt danach eine von zwei
Anfragen. Das ist Logik im Frontend, nach deiner Regel falsch. Ob sie raus soll, ist darum
keine Frage an dich: Sie soll. Offen war nur, wann; das hast du in 6995 F2 A schon entschieden
(mit dem Umbau zu `anwendung/`). F1 entfällt.

**Kosten.** Keine neuen: Am Bildschirm ändert sich nichts, die Arbeit steht schon im Umbau zu
`anwendung/`.

**Gegenvorschlag.** Du musst nichts entscheiden. Reicht dir die Erklärung, setze
`angenommen`; sonst `rückfrage` mit dem, was unklar bleibt.

**Stellungnahme.**
