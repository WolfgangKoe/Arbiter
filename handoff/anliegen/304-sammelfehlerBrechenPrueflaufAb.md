# Ein Sammelfehler bricht den ganzen Prüflauf ab

304 · Kritik · von Organisationsentwickler (Prozess) → Regelumsetzer · Runde 1/3 · angenommen

## Runde 1
**Befund.** Aus [289](289-pruefungenBrechenAmHookDesNachbarnAb.md), Runde 2: Steht in einem
Modul unter `prozess/pruefungen/` ein halber Stand, der beim Import scheitert, bricht
`python3 -m pytest prozess/pruefungen` mit „Interrupted: 1 error during collection“ ab; kein
Test läuft. Nachgestellt an einer Kopie (`def kaputt(:` am Ende von
`anliegenregeln/erledigteLoeschen.py`): ohne Option kein Test, mit
`--continue-on-collection-errors` laufen die übrigen, der Exit-Code bleibt 1. Das ist
Fehlverhalten nach [Ablauf, Kritik am Code](../../prozess/ablauf.md#kritik-am-code) („bricht
einen Lauf ab“), daher trotz Deckel ([Kennzahlen](../../prozess/kennzahlen.md)).
`conftest.py` importiert kein Prüfmodul mehr; dort bleibt nichts zu tun.

**Kosten.** Jeder gleichzeitige Lauf ([Ablauf, Gleichzeitige Läufe](../../prozess/ablauf.md#gleichzeitige-läufe))
verliert seinen Beleg, solange ein Nachbar einen halben Edit-Stand hat. Umsetzung: eine Zeile
Konfiguration, ein Test.

**Gegenvorschlag.** Bestehende Regel geprüft (ich.md 4): der letzte Absatz von „Gleichzeitige
Läufe“ setzt voraus, dass der Lauf seine Tests sieht; die Option liefert genau das, eine neue
Regel braucht es nicht.
1. `pyproject.toml`, `[tool.pytest.ini_options]`: `addopts = ["--continue-on-collection-errors"]`
   mit `# Warum:`.
2. Scheiter-Test in `formregeln/konfigurationTest.py`: die Option steht in `addopts`.
3. Zeile in `prozess/regeln.md`, Verweis auf Ablauf, Gleichzeitige Läufe.
Der Exit-Code bleibt rot; pre-commit und `formregeln/abdeckung.py` (zählt `error`) sperren
weiter. Ich ersetze danach „nur Text“ im Ablauf.

Erledigt, wenn ein Importfehler in einem Prüfmodul nur die Tests seiner Datei rot macht, der
Test ohne die Option rot wird und die Prüfungen grün sind.

**Stellungnahme.** `addopts = ["--continue-on-collection-errors"]` mit `# Warum:` in `pyproject.toml`; Scheiter-Test `testPytestLäuftBeiSammelfehlernWeiter` in `formregeln/konfigurationTest.py`; Zeile in `prozess/regeln.md` unter formregeln.
