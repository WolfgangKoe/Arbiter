# Formation im Glossar als Klasse

393 · Kritik · von Implementierer (Technik) → Anforderungsautor (Domäne) · Runde 1/3 · erledigt

## Runde 1
**Befund.** Die Zeile *Formation* in `domaene/glossar.md` nennt als Code-Bezeichner
`formation`. Im Code ist *Formation* eine Klasse (`technik/arbiter/domaene/querschnitt.py`,
Modell der Reihen und des Abstands nach `domaene/daten/formation.yaml`); Klassen heißen nach
[Es, 1](../../prozess/praemissen/es.md) in PascalCase. `formregeln/glossar.py` meldet:
„Klasse Formation steht nicht im Glossar“, und `python3 -m pytest prozess/pruefungen` ist
dadurch rot (`testDasRepoHältDieÜbereinstimmungVonCodeUndGlossar`).

**Kosten.** Ohne die Änderung bleibt die volle Prüfung rot und Plan 5 nicht abnahmefähig.

**Gegenvorschlag.** Den Code-Bezeichner der Zeile *Formation* auf `Formation` ändern. Der
Code bleibt, wie er ist; `formation` bleibt der Schlüssel in `formation.yaml`.

**Stellungnahme.** Angenommen. Die Zeile *Formation* in
[Glossar](../../domaene/glossar.md) nennt jetzt `Formation`, wie die anderen Klassen
(`Stelle`, `Base`, `Einheit`). Der Schlüssel `formation` in
[formation.yaml](../../domaene/daten/formation.yaml) bleibt wie vorgeschlagen.
