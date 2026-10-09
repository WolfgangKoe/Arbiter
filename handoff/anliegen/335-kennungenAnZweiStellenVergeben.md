# Die Kennungen nach W4 entstehen an zwei Stellen

335 · Kritik · von Reviewer (Technik) → Implementierer · Runde 2/3 · offen

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
Angenommen. Neues Modul `technik/arbiter/web/kennungen.py` (`spielerNachNummer`, `ablageNachNummer`); `darstellung.py` und `anwendung.py` nutzen beide.

## Runde 2
**Befund.** Geprüft: c1416e2. `kennungen.py` übersetzt jetzt Nummer → Objekt an einer Stelle,
und `anwendung.py` nutzt es. Die Gegenrichtung Spieler → Nummer leitet
[darstellung.py](../../technik/arbiter/web/darstellung.py) aber weiter selbst ab, zweimal:
`_nummer` mit `spieler.index(gesucht) + 1` (Besitzer der *Aufstellungszone*) und `_modelle`
mit `enumerate(spieler, start=1)`. `spielstand` macht dafür aus `spielerNachNummer` erst
wieder ein Tupel.

**Kosten.** Drei Stellen für die Spielernummer statt einer. Ändert sich die Zählung in
`kennungen.py`, tragen die *Ablage* und die *Karte* verschiedene Nummern für denselben
*Spieler*, und die Farbe eines *Modells* passt nicht mehr zur *Ablage*. Für Plan 5 (Kennung
des *Modells*) liegt die Vorlage dann in zwei Formen vor.

**Gegenvorschlag.** `spielstand` reicht `spielerNummern` an `_zone` und `_modelle` weiter;
`_modelle` iteriert `spielerNummern.items()`, `_zone` liefert die Nummer des Besitzers aus
derselben Zuordnung (etwa `next((nummer for nummer, einer in spielerNummern.items() if …), None)`).
`_nummer` und das Tupel entfallen.

Erledigt, wenn `grep -n "enumerate\|index(" technik/arbiter/web/darstellung.py` leer ist.

**Stellungnahme.**
