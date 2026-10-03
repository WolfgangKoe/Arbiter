# Regeln und ihre Mechanismen

Regel (Link) | Mechanismus | Scheiter-Test (`prozess/pruefungen/`)
---|---|---
[Benennung](praemissen/wir.md): camelCase, mindestens 3 Zeichen, Dateinamen, `<anforderung>Test.py`, `testAuf1_4…` ([Anliegen 28](../handoff/anliegen/28-benennungOffenePunkte.md)) | `benennung.py`, im Lauf von `python3 -m pytest prozess/pruefungen` und in `.pre-commit-config.yaml`; Pytest-Hooks `pytest_<hook>` in `conftest.py` sind Werkzeugnamen; Altdateien unter `technik/` stehen mit Fingerabdruck in `benennungRueckstand.txt` | `benennungTest.py`
[Kriterium ↔ Test](ablauf.md#dod-item-fertig) (`testAuf1_4…` gehört zu AUF-1.4) | `rueckverfolgung.py`, wo die Testdatei zur Anforderung schon existiert | `rueckverfolgungTest.py`
[Anliegen](ablauf.md#anliegen): Kopf, Status, Höchstmaß 4.000 Zeichen | `anliegen.py`, `hoechstmassTest.py` | `anliegenTest.py`, `hoechstmassTest.py`
[Anliegen](ablauf.md#anliegen): Status `erledigt` löscht die Datei, ohne eigenen Lauf | `erledigteLoeschen.py` (pre-commit, SubagentStop, Lauf von `python3 -m pytest prozess/pruefungen`) | `erledigteLoeschenTest.py`
[Anliegen](ablauf.md#anliegen): `erledigt` setzt nur der Absender | `statusrecht.py` (PreToolUse, Write und Edit; nicht Bash, [Ablauf](ablauf.md#anliegen)) | `statusrechtTest.py`
[Anliegen](ablauf.md#anliegen): Stand nennt fällige Nachprüfungen mit Rolle | `stand.py` (SessionStart) | `standTest.py`
[Budget](ablauf.md#budget) nach Kontextfenster ([Anliegen 22](../handoff/anliegen/22-dashboard-und-budget-am-kontextfenster.md)): 120.000 Meldung, 150.000 Sperre | `belegung.py` (PreToolUse, PostToolUse); der Stand zeigt die Belegung; Freigabe durch den Stakeholder in `.git/arbiter/belegungsgrenze.txt` | `belegungTest.py`, `standTest.py`
Der Koordinator liest nur kurze Dateien, `git show` nur mit `--stat` oder unter 4.000 Zeichen | `lesegrenze.py` (Read), `bashPositivliste.py` ruft `gitShowZulässig` | `lesegrenzeTest.py`, `bashPositivlisteTest.py`
`VORGEHEN.md`, `handoff/kritik-entwickler.md`, `Arbiter/`, `ArbiterMap/` sind für alle Rollen und den Koordinator nur lesbar | `agenten.nurLesbar`, `schreibgrenze.py` (Write, Edit, Meldung beim Ende), `bashPositivliste.py` (rm, mv, cp, sed -i, Umleitung) | `schreibgrenzeTest.py`, `bashPositivlisteTest.py`
Jeder Hook zeigt auf eine vorhandene, gültige Datei; Reihenfolge beim Umbenennen: neue Datei, Einstellung, alte Datei löschen | `einstellungen.py` | `einstellungenTest.py`
Ruff nach E37, Namensregeln N802, N803, N806, N815, N816 aus; pytest erkennt `<name>Test.py` | `pyproject.toml` (ruff, `src`, N818 aus, Suchpfad `technik`, `dependency-groups`); `konfigurationTest.py` ruft ruff über das Repo und ist rot, wenn ruff fehlt (Dateien aus `benennungRueckstand.txt` ausgenommen); `.pre-commit-config.yaml` läuft nur nach `pre-commit install` | `konfigurationTest.py`
Koordinator: nur Positivliste; Rollen nutzen git nur lesend | `bashPositivliste.py` | `bashPositivlisteTest.py`
Schreibpfade je Rolle | `schreibgrenze.py` | `schreibgrenzeTest.py`
Schlussantwort höchstens 800 Zeichen | `schlussantwort.py` | `schlussantwortTest.py`
Stand und Ordner-CLAUDE.md beim Start einer Rolle; Rollenläufe als Kennzahl | `rollenkontext.py`, `rollenzaehler.py` | `rollenkontextTest.py`, `rollenzaehlerTest.py`
Höchstmaße der Dateien | `hoechstmassTest.py` | `hoechstmassTest.py`
cSpell prüft kein Markdown | `.vscode/settings.json` | `cspellTest.py`
[Technikphase, Schritt 5](ablauf.md#technikphase): Abnahme vor Review; offen ist ein Item, solange seine Datei in `domaene/items/` liegt ([Anliegen 56](../handoff/anliegen/56-standErkenntDieAbnahme.md)) | `stand.py` (`offeneItems`, `lage`) | `standTest.py`
[Anliegen](ablauf.md#anliegen): Stand nennt je offenem Anliegen, wer dran ist (nach Status, nicht nach „wartet auf“); [Kritik am Code](ablauf.md#kritik-am-code): erster Code-Commit seit der letzten Freigabe ohne `Kritik <Hash>` im Betreff; Meldung nach jedem Rollenlauf | `stand.py`, `anliegen.py` (`dran`), `codekritik.py`; Hook `PostToolUse` auf `Agent` in `.claude/settings.json` | `standTest.py`
[Anliegen](ablauf.md#anliegen): Nummer eindeutig; eine neue Datei mit vergebener Nummer ist gesperrt, die Meldung nennt die nächste freie; nie vergeben heißt auch: nicht in git ([Anliegen 42](../handoff/anliegen/42-anliegennummerDoppelt.md)) | `anliegennummer.py` (PreToolUse, Write), `anliegen.py` (`doppelteNummern`) | `anliegennummerTest.py`
[Anliegen](ablauf.md#anliegen): Rollen ändern Anliegen nie per Bash (Umleitung, `rm`, `mv`, `cp`, `sed -i`, `tee`; Heuristik wie bei den nur lesbaren Pfaden) | `bashPositivliste.py` (`ändertPfad`, `istAnliegen`) | `bashPositivlisteTest.py`
[Anliegen](ablauf.md#anliegen): Links auf ein gelöschtes Anliegen werden zu „Anliegen <nr>“ | `erledigteLoeschen.py` (`linksErsetzen`; pre-commit, SubagentStop) | `erledigteLoeschenTest.py`
[Anliegen](ablauf.md#anliegen): unter jeder Frage an den Stakeholder eine Zeile `Antwort:` (offene Anliegen an ihn; [Anliegen 20](../handoff/anliegen/20-antwort-unter-jeder-frage.md)) | `anliegen.py` (`antwortVerstöße`, über `kopfVerstöße`) | `anliegenTest.py`
Komplexität: Schwelle 15 (kognitiv, Verschachtelung) und höchstens 12 Fälle je Funktion ([Ablauf, Werkzeuge](ablauf.md#technikphase)) | `pyproject.toml` (`tool.complexipy`, ruff `PLR0912`, `max-branches`), `complexipy` in `dependency-groups`; im Lauf von `python3 -m pytest prozess/pruefungen`, rot, wenn complexipy fehlt | `komplexitaetTest.py`
[Kennzahlen](kennzahlen.md): Rollenläufe je Phase und Rolle, offene Anliegen je Rolle mit Alter (Aufruf `python3 prozess/pruefungen/kennzahlen.py`, für die Retro) | `kennzahlen.py` | `kennzahlenTest.py`
