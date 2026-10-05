# Prüfungen zu web/ und Komponentenseite: Lücken und Doppeltes

286 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
**Befund.** Kritik am Code von 9d6514a, dbb0059 und 7e97123. 829f5ce (267) ohne Befund.
1. W1 (`formregeln/importvertrag.py`, `vorlagenImporte`): `import flask` und dann
   `flask.render_template(...)` bleibt grün; geprüft wird nur `from flask import …`.
2. D3 (`formregeln/zustandsschutz.py`): `setattr(aufstellung, "anDerReihe", x)` und
   `object.__setattr__(aufstellung, "_stellen", {})` in `web/` bleiben grün; der zweite
   umgeht auch `frozen=True`, weil Dunder ausgenommen sind.
3. `"technik/arbiter/web"` steht dreimal: `importvertrag.webOrdner`, in `zustandsschutz.py` in
   `lesenGesperrtOrdner` und `schreibenGesperrtOrdner`; `katalog` zweimal (Modul, Test).
   `erlaubt` in `importvertrag.py` baut `istOderUnter` nach.
4. `komponentenseite.klassenSeiten` nimmt `komponenten.html` aus der Prüfung auf neue Klassen
   aus. Eine Klasse, die nur auf der Komponentenseite steht und in `komponenten.css` fehlt,
   bleibt grün. 262, 1c nennt alle `technik/frontend/*.html`.
5. `sonarlintTest.py` importiert als erstes Prüfskript Produktcode (`arbiter.web.anwendung`,
   `flask`) und ruft `anwendungFür(None)` gegen die Signatur (`Aufstellung`). Bricht der
   Import von `web/`, fallen alle 25 SonarLint-Tests in der Sammlung, nicht nur dieser eine.

**Kosten.** 1, 2: Die Sperren, die 265 sichern soll, haben je einen naheliegenden Weg
vorbei; ein Lauf, der den ersten Weg gesperrt findet, nimmt den zweiten. 3: Benennt jemand
`web/` um, ändert er drei Stellen, sonst prüft eine Regel ins Leere, still grün
([Wir](../../prozess/praemissen/wir.md) 3). 4: Die tote Klasse fängt die Prüfung, die neue auf
der Seite selbst nicht. 5: Kopplung der Prüfskripte an das Produkt; laut Anliegen 253 sind
die Schichten der Prüfskripte nur Text, das fällt heute niemandem auf.

**Gegenvorschlag.**
1. Zusätzlich jedes `ast.Attribute` mit `attr` in `vorlagenFunktionen` an einem Namen, der
   an `flask` gebunden ist, als W1 melden; Probe rot: `import flask\nflask.render_template`.
2. In `web/` Aufrufe von `setattr`, `delattr` und `object.__setattr__` als D3 melden;
   Probe rot je Fall. Ist das mehr als die Regel D3 sagt, frag den Architekten.
3. `webOrdner` und `katalogOrdner` nach `gemeinsam/pfade.py` (wie `frontendOrdner`), beide
   Module und Tests importieren sie; `erlaubt` nutzt `istOderUnter`.
4. In `klassenSeiten` `komponenten.html` nicht ausnehmen; Scheiter-Test: Klasse nur in
   `komponenten.html`, nicht im Stil, ist rot.
5. Den Auslöser-Test nach `technik/tests/einheit/` (Testautor) oder als AST-Prüfung:
   `add_url_rule`/`route` mit `methods` außer GET, HEAD, OPTIONS in `web/` ist rot, solange
   die Ausnahme steht. Dann braucht `sonarlintTest.py` weder Flask noch `arbiter`.

Erledigt, wenn die Proben zu 1, 2, 4 rot sind, die Ordner je einmal stehen und
`python3 -m pytest prozess/pruefungen` grün ist.

**Stellungnahme.**
