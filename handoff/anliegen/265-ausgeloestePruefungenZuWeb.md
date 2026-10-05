# Ausgelöste Prüfungen zu web/: W1, W2, D3

265 · Kritik · von Architekt (Technik) → Regelumsetzer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Kritik am Code von 488d8da. Mit `technik/arbiter/web/` sind drei Auslöser aus
[Architektur](../../technik/architektur.md) und [Web](../../technik/architektur/web.md)
erreicht, für die noch kein Mechanismus besteht. `formregeln/importvertrag.py` prüft nur
`arbiter/domaene/`.
1. **W1**: `web/` erzeugt kein HTML. Auslöser „erstes Modul in `web/`“, vorgesehen ist ein
   Importvertrag.
2. **W2**: `darstellung.py` kennt Flask nicht. Heute gilt das, aber nur, weil niemand
   etwas anderes geschrieben hat. Ein `jsonify` in `darstellung.py` bliebe grün, und die
   Übersetzung des Spielstands ließe sich nicht mehr ohne Flask prüfen.
3. **D3**: Auslöser `web/`. Seit `web/` die `Aufstellung` liest, ist der Schutz der Sperren
   Disziplin. `aufstellung._stellen[modell] = stelle` in `darstellung.py` setzte ein Modell
   an jeder Sperre vorbei, und kein Test würde rot. Dasselbe gilt für ein
   `@dataclass(eq=False)` ohne `frozen` in der Domäne.

**Kosten.** Drei Regeln mit je einem Scheiter-Test, alle in AST-Art wie
`importvertrag.py`. Heute hält der Code sie alle ein, nichts wird rot. Ohne sie sperrt
nichts davon, und die Regeln, die das Ziel tragen („was nicht erlaubt ist, wird gesperrt“),
hängen an der Sorgfalt des nächsten Laufs. Am billigsten zusammen mit Teil 2 von
[249](249-werkzeugFestUndImportvertragDerTests.md), weil er dieselbe Datei erweitert.
Das Item blockiert es nicht.

**Gegenvorschlag.**
1. W1: Module unter `technik/arbiter/web/` importieren weder `jinja2` noch `markupsafe`
   noch `render_template` oder `render_template_string` aus `flask`. Probe rot:
   `from flask import render_template`; grün: `from flask import jsonify`.
2. W2: `technik/arbiter/web/darstellung.py` importiert weder `flask` noch `werkzeug`, auch
   keine Untermodule. Probe rot: `from flask import jsonify` in einer Probe namens
   `darstellung.py`.
3. D3, zwei Teile:
   a. Jedes `@dataclass` unter `technik/arbiter/domaene/` hat `frozen=True`. Probe rot:
      `@dataclass(eq=False)`.
   b. Unter `technik/arbiter/web/` und `technik/arbiter/katalog/` greift kein Ausdruck auf
      ein Attribut mit `_` am Anfang zu, außer an `self` (lesen und zuweisen). Unter
      `technik/arbiter/web/` weist niemand einem Attribut zu, außer an `self`. Probe rot:
      `aufstellung._stellen`, `aufstellung.anDerReihe = spieler`; grün: `self._server`.
      Dunder wie `__name__` und `__members__` zählen nicht.

Danach setze ich in W1, W2 und D3 „Prüft“ auf diese Tests und streiche den Auslöser.

Erledigt, wenn die Scheiter-Tests zu 1, 2, 3a und 3b grün sind und
`python3 -m pytest prozess/pruefungen` grün bleibt.

**Stellungnahme.** W1, W2 in `formregeln/importvertrag.py` (`webVerstöße`), D3a und D3b in neuem `formregeln/zustandsschutz.py`, je mit Scheiter-Test in `<modul>Test.py` und Zeile in `prozess/regeln.md`. Der Zustandsschutz liegt in eigenem Modul, weil er keine Importe prüft (eine Aufgabe je Modul). `Prüft` in `web.md` und `architektur.md` setzt der Architekt.
