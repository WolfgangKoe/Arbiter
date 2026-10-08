# Die Kennungen nach W4 entstehen an zwei Stellen

335 · Kritik · von Reviewer (Technik) → Implementierer · Runde 1/3 · offen

## Runde 1
**Befund.** Seit 6bea166 vergibt `web/` die Kennungen nach
[Web, W4](../../technik/architektur/web.md) zweimal: [darstellung.py](../../technik/arbiter/web/darstellung.py)
zählt *Spieler* und *Einheiten* mit `enumerate(…, start=1)` für die Antwort,
`einheitInDerAblage` in [anwendung.py](../../technik/arbiter/web/anwendung.py) baut dieselbe
Zuordnung je Anfrage neu als `dict(enumerate(…))`. Das Tupel
`(ausgangslage.ersterSpieler, ausgangslage.zweiterSpieler)` steht in beiden Modulen, und
„in der *Ablage* heißt nicht *aufgestellt*“ steht als Filter in `_spieler` und als Wächter in
`einheitInDerAblage`.

**Kosten.** Die Seite schickt die Nummer zurück, die `darstellung.py` vergeben hat; der Server
löst sie mit der Zählung aus `anwendung.py` auf. Ändert sich eine der beiden (etwa eine
Nummer nur über die *Ablage*, oder Modelle mit Kennung in Plan 5), wählt ein Klick eine andere
*Einheit* als die angeklickte, und kein Test merkt es, solange die Testarmeen zwei *Einheiten*
haben. Jede weitere Route mit Kennung (Plan 5: *Modell*) kopiert die Zählung ein drittes Mal.

**Gegenvorschlag.** Eine Stelle in `web/`, die Kennung und Objekt in beide Richtungen
übersetzt, ohne Flask: etwa `spielerNachNummer(ausgangslage)` und
`einheitNachNummer(spieler)` in `darstellung.py` oder in einem eigenen Modul `kennungen.py`
(W2: je Modul ein Grund zur Änderung). `darstellung.py` und `anwendung.py` nutzen sie beide;
der Filter „in der *Ablage*“ steht dann einmal.

**Stellungnahme.**
