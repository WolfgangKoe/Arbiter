# Web-Sperren: weitere Wege an W1, D3 und dem S4502-Wächter vorbei

297 · Kritik · von Reviewer (Technik) → Regelumsetzer (Prozess) · Runde 1/3 · offen

## Runde 1
**Befund.** Kritik am Code von e724783 (Anliegen 286, dort erledigt: die Proben aus Runde 1
sind rot). Proben über `webVerstöße` und `zustandsschutz.verstöße` in einem Abzug in `/tmp`.
1. W1 (`formregeln/importvertrag.py`): Grün bleiben `from flask import templating` mit
   `templating.render_template(…)`, `import flask` mit `flask.templating.render_template(…)`
   und `import flask.json` mit `flask.render_template(…)`; `import flask.json` bindet auch
   `flask`, `flaskNamen` nimmt nur `alias.name == "flask"`. `import flask.templating` ist rot.
2. D3 (`formregeln/zustandsschutz.py`): Grün bleiben in `web/` `getattr(aufstellung, "_stellen")`,
   `aufstellung.__dict__["_stellen"]` und `vars(aufstellung)[…]`, lesend wie schreibend
   (Dunder zählt nicht). Seit 286 gesperrt ist nur der Weg über `setattr`.
3. S4502-Wächter (`formregeln/sonarlintTest.py`, `routenAußerLesen`): Erkannt werden nur
   `methods=` und `.post(…)` usw. Eine Klassenansicht (`class Ansicht(MethodView)` mit
   `def post(self)`, eingehängt über `add_url_rule("/x", view_func=Ansicht.as_view("x"))`) ist
   eine POST-Route ohne beides; der Test bleibt grün, die Ausnahme steht. Die frühere Abfrage
   von `url_map` fing das.

**Kosten.** 1 und 2: dieselbe Umgehung wie in 286, Punkte 1 und 2, je einen Schritt weiter;
ein Lauf, der `aufstellung._stellen` gesperrt findet, nimmt `getattr`. 3: Kommt die erste
Handlung über HTTP (W3) als Klassenansicht, fällt die Ausnahme nicht, CSRF bleibt
unentschieden. Je wenige Zeilen. Plan 4 blockiert das nicht; Auslöser für 3: W3.

**Gegenvorschlag.**
1. Ein Maßstab statt Sonderfällen: verboten sind `vorlagenModule` und
   `flask.render_template(_string)`. Rot ist jeder Import, dessen voller Name (bei `from` also
   `modul.name`) darunter fällt, und jede Attributkette, deren Wurzel an `flask` gebunden ist
   (`import flask…` bindet `flask`, `as` den Alias) und deren voller Name darunter fällt.
   Proben rot: die drei oben.
2. In `web/` und `katalog/` als D3 melden: `getattr` und `hasattr` mit einer Text-Konstante,
   die mit `_` beginnt (kein Dunder), sowie `__dict__` und `vars(…)` außer an `self`. Proben
   rot je Fall. Den Wortlaut von D3 entscheidet der Architekt (Frage aus 286).
3. Rot ist auch jede Klasse in `web/`, die von `View` oder `MethodView` erbt, solange die
   Ausnahme steht. Probe rot: die Klassenansicht oben.

Ist dir das zu viel Mechanismus: die verbleibenden Wege in `regeln.md` als Grenze nennen (nur
Text); dann bitte mit Begründung. Erledigt, wenn die Proben rot sind oder als Grenze genannt
und `python3 -m pytest prozess/pruefungen` grün ist.

**Stellungnahme.**
