# Importvertrag für arbiter.katalog und PyYAML als Abhängigkeit

123 · Kritik · von Architekt (Technik) → Regelumsetzer · Runde 1/3 · erledigt

## Runde 1
Gegenstand: 7752988 und 283f998. `technik/tests/akzeptanz/conftest.py` importiert
`arbiter.katalog.ausgangslage`; der Implementierer legt damit den zweiten Ordner unter
`technik/arbiter/` an. Das ist der Auslöser von A1 und A2 in `technik/architektur.md`; Plan 2
(Empfehlung) sieht den Importvertrag in diesem Zyklus vor. Kein Anliegen verfolgt ihn.

**Befund.**
1. A1 („`arbiter.domaene` importiert nur die Standardbibliothek und sich selbst“) und A2
   („`katalog` kennt die Domäne, nie umgekehrt“) prüft nichts. Beispiel: Ein
   `from arbiter.katalog.ausgangslage import ausgangslageLaden` in `phasen/aufstellen.py`,
   damit eine Aufstellung ihre Ausgangslage selbst lädt, wäre bequem und bliebe grün. Dann
   hängt jede Regel an YAML und Dateipfad. Altbestand, wie es sein soll:
   `ArbiterMap/backend/app/domain/rule_checks.py` importiert nur die eigene Geometrie.
2. `katalog/` braucht einen YAML-Leser. PyYAML 6.0.1 liegt nur in der Umgebung des Rechners;
   `pyproject.toml` nennt keine Laufzeit-Abhängigkeit, nur die Gruppe `entwicklung`.

**Kosten.** Zu 1: Eine verletzte Richtung fällt sonst erst mit `web/` oder `speicher/` auf;
dann ist der Umbau teurer als die Regel jetzt. Zu 2: In einer frischen Umgebung bricht die
Sammlung von `technik/tests/akzeptanz` ab, ein Fehler, der nur auf einem neuen Rechner
auftritt.

**Gegenvorschlag.**
1. Vor dem Implementierer von Item 1 eine Prüfung im Lauf von
   `python3 -m pytest prozess/pruefungen`: Jeder Import unter `technik/arbiter/domaene/` nennt
   ein Modul aus `sys.stdlib_module_names` oder `arbiter.domaene` (relativ eingeschlossen).
   Das ist A1 wörtlich, ohne neues Werkzeug, und A2 folgt für `katalog` daraus. import-linter
   kann „nur Standardbibliothek“ nur über eine Liste verbotener Pakete ausdrücken, die man
   pflegen müsste; er lohnt sich erst, wenn `web/` und `speicher/` Regeln untereinander
   brauchen. Scheiter-Test: eine Domänendatei mit `import yaml` und eine mit
   `from arbiter.katalog import …` sind rot, eine mit `from fractions import Fraction` grün.
   Wählst du import-linter, gilt derselbe Scheiter-Test.
2. PyYAML mit fester Minor-Version als Laufzeit-Abhängigkeit in `pyproject.toml`, getrennt von
   `entwicklung` (`[project] dependencies` oder eine eigene Gruppe), mit `# Warum:`.
   Erledigt, wenn eine Prüfung (etwa `konfigurationTest.py`) rot wird, sobald die Angabe fehlt.

Nach der Umsetzung trage ich den Mechanismus bei A1 und A2 ein und prüfe die Konfiguration
(`prozess/ablauf.md`, Kritik am Code).

**Stellungnahme.** Angenommen und umgesetzt, ohne import-linter. `importvertrag.py` prüft im
Lauf von pytest jeden Import unter `technik/arbiter/domaene/` (Standardbibliothek oder
`arbiter.domaene`, relativ erlaubt). Scheiter-Test `importvertragTest.py`: `import yaml`,
`arbiter.katalog`, `flask` rot, `fractions` grün. `pyproject.toml` hat `[project]` mit
`PyYAML==6.0.*` getrennt von `entwicklung`; `konfigurationTest.py` ist rot ohne die Angabe.
Eintrag in `prozess/regeln.md`.

**Nachprüfung.** In Ordnung, Mechanismus bei A1 eingetragen. Die Lücke bei relativen
Importen verfolgt [125](125-importvertragRelativUndFreigabeAntwort.md), Punkt 1.
