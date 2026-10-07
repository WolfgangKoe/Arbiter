# D3 meldet `getattr` an `self` und `vars()`; W1 lässt `from flask import *` durch

301 · Kritik · von Reviewer (Technik) → Regelumsetzer (Prozess) · Runde 1/3 · erledigt

## Runde 1
**Befund.** Kritik am Code von 94a94f9 (Anliegen 297, dort erledigt). Fehlverhalten nach
[Ablauf, Kritik am Code](../../prozess/ablauf.md#kritik-am-code). Proben über
`zustandsschutz.verstöße` und `importvertrag.webVerstöße` an einem Abzug in `/tmp`:
1. D3 meldet einen Verstoß, den es nicht gibt: `versteckterZugriff` (`formregeln/zustandsschutz.py`)
   nimmt `self` nur bei `vars` aus. `getattr(self, "_x", None)` und `hasattr(self, "_x")` in
   `web/` sind rot, obwohl D3 den Zugriff an `self` erlaubt ([Regeln](../../prozess/regeln.md),
   Zeile Zustandsschutz). Ebenso `vars()` ohne Argument: Das sind die lokalen Namen, kein
   fremdes Objekt.
2. W1 lässt einen Verstoß durch: `from flask import *` mit `render_template("x")` in `web/`
   ist grün; `importierteNamen` liefert `flask.*`, das unter keinen Vorlagennamen fällt.

**Kosten.** 1: Ein Implementierer, der in `web/` einen Zwischenspeicher an `self` per
`getattr(self, "_…", None)` liest, wird gesperrt und muss umbauen oder ein Anliegen stellen.
2: Derselbe Umweg wie in 297, Punkt 1, ein Schritt weiter. Je eine Zeile und ein Test.

**Gegenvorschlag.**
1. In `versteckterZugriff` für alle drei Namen `not anSelfGerichtet(aufruf)` verlangen,
   `vars` nur mit Argument. Proben grün: `getattr(self, "_x")`, `hasattr(self, "_x")`, `vars()`.
2. In `web/` ist ein `*`-Import aus `flask` oder einem `vorlagenModule` rot (W1). Probe rot:
   `from flask import *`.

Weitere Wege (`getattr(flask, "render_template")`, `app.jinja_env`) bitte als Grenze in
`regeln.md` nennen, nur Text; ein Mechanismus dafür lohnt nicht.

Erledigt, wenn die Proben wie genannt rot und grün sind und
`python3 -m pytest prozess/pruefungen` grün ist.

**Stellungnahme.** Umgesetzt, beide Punkte, mit Proben; die Grenze steht in `regeln.md`. 906 Tests grün.
