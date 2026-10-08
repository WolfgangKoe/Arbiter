# Regeln und ihre Mechanismen

Pfade der Mechanismen und Tests liegen unter `prozess/pruefungen/`, gegliedert je Ordner.
Hart zurückgebaut nach Entscheidung des Stakeholders; neue Regeln kommen, wenn sie gebraucht werden.

## anliegenregeln

Regel (Link) | Mechanismus | Scheiter-Test
---|---|---
[Anliegen](ablauf.md#anliegen): Kopf und Status (Titel, Kopfzeile, Typ, Runde, Rollen) | `anliegenregeln/anliegen.py` | `anliegenregeln/anliegenTest.py`
[Anliegen](ablauf.md#anliegen): Status `erledigt` löscht die Datei, ohne eigenen Lauf, aber nur eine, die im letzten Commit steht und seit ihm unverändert ist; sonst bewahrt git die Begründung nicht | `anliegenregeln/erledigteLoeschen.py` (pre-commit, SubagentStop) | `anliegenregeln/erledigteLoeschenTest.py`
[Anliegen](ablauf.md#anliegen): Links auf ein gelöschtes Anliegen werden zu „Anliegen <nr>“ | `anliegenregeln/erledigteLoeschen.py` (`linksErsetzen`; pre-commit, SubagentStop) | `anliegenregeln/erledigteLoeschenTest.py`
[Anliegen](ablauf.md#anliegen): Wer bei den Anliegen dran ist (nach Status) und welche Nachprüfung fällig ist; der Stand nennt beides | `anliegenregeln/anliegenDran.py` (`dran`, `nachprüfungen`), `standregeln/anliegenText.py` | `anliegenregeln/anliegenTest.py`

## formregeln

Regel (Link) | Mechanismus | Scheiter-Test
---|---|---
[Benennung](praemissen/es.md): camelCase, mindestens 3 Zeichen, Dateinamen, `<anforderung>Test.py`, geteilt `<kürzel><n>Test.py` gegen `<KÜRZEL>-<n>` in der Anforderungsdatei, `testAuf1_4…`, Typaliase in PascalCase, `x` und `y` nur als Felder von `Stelle` (Anliegen 28, 116, 114, 128) | `formregeln/benennung.py`, im Lauf von `python3 -m pytest prozess/pruefungen` und in `.pre-commit-config.yaml`; Pytest-Hooks `pytest_<hook>` in `conftest.py` sind Werkzeugnamen | `formregeln/benennungTest.py` (Hilfsmodul grün; mit Testfunktion und im Unterordner rot)
[Kommentare](praemissen/es.md) (Regel 8): nur `# Regel:` und `# Warum:`, Docstring einzeilig, kein TODO oder FIXME; Werkzeugkommentare (`noqa`, `type:`) bleiben (Anliegen 114) | `formregeln/kommentare.py`, im Lauf von `python3 -m pytest prozess/pruefungen` | `formregeln/kommentareTest.py`
[DoD 2](ablauf.md#technikphase), Code → Glossar: Jede Klasse der Domäne steht im Glossar, jeder Enum-Wert in Klammern hinter seiner Klasse oder als *Grund* in einer Anforderung; Glossar → Code bleibt Urteil | `formregeln/glossar.py` (im Lauf von `python3 -m pytest prozess/pruefungen`) | `formregeln/glossarTest.py` (Enum-Wert `nord`, Klasse `Spielfeld`)
[Importvertrag](../technik/architektur.md) A1 und A2: `arbiter.domaene` importiert nur die Standardbibliothek und sich selbst, `katalog` kennt die Domäne, nie umgekehrt (Anliegen 123) | `formregeln/importvertrag.py` (relative Importe aufgelöst; im Lauf von `python3 -m pytest prozess/pruefungen`) | `formregeln/importvertragTest.py` (`import yaml`, `arbiter.katalog` und `from ..katalog` rot, `fractions` grün)
Ruff nach [Ablauf, Werkzeuge](ablauf.md#technikphase), Namensregeln N802, N803, N806, N815, N816 aus; höchstens 12 Fälle je Funktion (`PLR0912`); der Altbestand steht in `extend-exclude` | `pyproject.toml` (ruff); `formregeln/werkzeugaufruf.py` (`ruffAufrufen`) ruft ruff über das Repo, rot, wenn ruff fehlt | `formregeln/konfigurationTest.py` (Verstoß rot, Altbestand grün, `testDasRepoIstRuffSauber`)
Komplexität: Schwelle 15 (kognitiv, Verschachtelung, [Ablauf, Werkzeuge](ablauf.md#technikphase)) | `pyproject.toml` (`tool.complexipy`), `formregeln/werkzeugaufruf.py` (`complexipyAufrufen`); im Lauf von `python3 -m pytest prozess/pruefungen`, rot, wenn complexipy fehlt | `formregeln/komplexitaetTest.py` (der Code liegt unter der Schwelle)
[DoD 1](ablauf.md#dod-item-fertig): Zeilen und Zweige mindestens 95 % für `technik/arbiter` mit `technik/tests`; rote Tests setzen die Schwelle aus und werden mit ihrer Zahl genannt, denn Tests entstehen vor dem Code | `formregeln/abdeckung.py` (`abdeckungMessen`, `verstoß`, `aussetzung`), Test mit Marke `stand` im Lauf der Prüfungen | `formregeln/abdeckungTest.py` (Zweig ungeprobt rot, volle Abdeckung grün, Kindprozess gedeckt, rote Tests)
[DoD 2](ablauf.md#dod-item-fertig): kein toter Code: vulture über `technik/arbiter` und `technik/tests/akzeptanz`, 60 % Konfidenz; Ausnahmen in `pyproject.toml`; fehlender Pfad oder Syntaxfehler ist rot | `formregeln/abdeckung.py` (`unbenutzterCode`) | `formregeln/abdeckungTest.py` (`testDasProduktHatKeinenTotenCode`, Proben)
[Ablauf, Werkzeuge](ablauf.md#technikphase): Die Sperre ist mindestens so streng wie SonarLint. Wegwerf-Versuch (P2, Anliegen 150): `sonarlint-ls.jar` und `sonarpython.jar` der VS-Code-Erweiterung laufen ohne VS Code (Java 21, Sprachserver über stdio, Dateien nacheinander öffnen, sonst je Lauf andere Funde); die Prüfung sperrt das Standardprofil selbst, nicht über ruff. Abgeschaltet sind nur die Namensregeln S100, S101, S116, S117, S1542, S1578 (camelCase, [es.md](praemissen/es.md), `formregeln/benennung.py` prüft); in VS Code melden sie weiter, der Block für die Benutzereinstellungen: `python3 prozess/pruefungen/gemeinsam/lauf.py formregeln.sonarlint --einstellung` (Anliegen 182). Ausgenommen sind genau zwei Funde in `web/` (Anliegen 261): `python:S4502` in `anwendung.py`, `python:S5332` in `server.py`, unbegründet, weil nach [Vertrag, V4](../technik/architektur/vertrag.md) nur PUT und DELETE ändern, nichts CORS freigibt und nur `127.0.0.1` gilt ([Web](../technik/architektur/web.md), W5); Liste `ausnahmen`, je Datei und Regel; die Ausnahme von S4502 fällt mit der ersten Route für POST oder PATCH, Klassenansicht (`View`, `MethodView`; Anliegen 297) oder CORS-Freigabe (`Access-Control-Allow`, `flask_cors`) in `web/` (Test rot, solange sie besteht; CSRF entscheidet dann V4 neu; Anliegen 330). Prüft nur Python, das Frontend prüfen ESLint und Stylelint ([frontendregeln](#frontendregeln), Anliegen 280); geprüft: `technik/arbiter`, `technik/tests/einheit`, `technik/tests/akzeptanz`, `prozess/pruefungen`, ein fehlender oder leerer Ordner ist rot. Erweiterung unter `~/.vscode/extensions` oder `SONARLINT_ERWEITERUNG`, Version `6.0.` aus `package.json` (`erwarteteVersion`, andere oder unlesbare ist rot), sonst rot | `formregeln/sonarlint.py` (Aufruf `python3 prozess/pruefungen/gemeinsam/lauf.py formregeln.sonarlint`, Hook `sonarlint` in `.pre-commit-config.yaml` bei `.py`-Dateien, nicht im Lauf der Prüfungen) | `formregeln/sonarlintTest.py` (ungenutzte Variable rot, camelCase und sauberer Code grün, Ordner fehlt oder leer rot, Version 6.9 gegen 6.10, fremde Version rot, Umgebungsvariable auf Ordner ohne package.json rot, Wartezeit, Server beendet sich rot, Erweiterung fehlt rot, alter Ordner ohne package.json neben vollständiger Erweiterung grün, Einstellung gleich Regelliste, S5778 in pytest.raises rot, Einheitstests geprüft, Ausnahme gilt nur für ihre Datei, S4502-Ausnahme rot bei POST, Klassenansicht oder CORS, PUT und DELETE grün, Hook)

## frontendregeln

Regel (Link) | Mechanismus | Scheiter-Test
---|---|---
Frontend ([Web](../technik/architektur/web.md) O1, Anliegen 242): eslint 9 über `technik/frontend/**/*.js` (`camelcase`, `id-length` mindestens 3 außer `x`, `y`, `no-var`, `prefer-const`, `eqeqeq`, `no-unused-vars`, `complexity` 15, keine Elemente erzeugen (`no-restricted-properties` für `createElement`, `createElementNS`, `parseFromString`, `createContextualFragment`, `setHTMLUnsafe` auf jedem Objekt und `document.write`, `writeln`; `no-restricted-syntax` für `innerHTML`, `outerHTML` auch als berechneter Zugriff, `insertAdjacentHTML`, `new Image`, `new Option`, `new Audio`, Anliegen 268, 294), Kommentare nur `// Regel:` und `// Warum:`), stylelint 16 über `**/*.css` (camelCase für Klassen und Variablen, Farbwerte nur in `:root`, keine Farbnamen); fehlt `node_modules`, rot mit `npm install`; englische Wörter erkennt kein Linter, das bleibt Urteil des Reviewers | `frontendregeln/frontend.py` (Aufruf `python3 prozess/pruefungen/gemeinsam/lauf.py frontendregeln.frontend`, im Lauf von `python3 -m pytest prozess/pruefungen`), `eslint.config.mjs`, `.stylelintrc.json`, `package.json`, `frontendregeln/eslintKommentare.mjs`, `frontendregeln/stylelintFarben.mjs` | `frontendregeln/frontendTest.py` (`var`, snake_case, zu kurz, `let`, `==`, ungenutzt, Komplexität 16, `createElement`, `createElementNS`, `document.write`, `writeln`, `window.document.createElement`, `ownerDocument.createElement`, berechnetes `innerHTML`, `parseFromString`, `createContextualFragment`, `setHTMLUnsafe`, `new Option`, `new Image`, `innerHTML`, `outerHTML`, `insertAdjacentHTML` rot, Klonen der Template grün, Prosa-, Block- und TODO-Kommentar, kebab-case-Klasse, Variable, Hex, rgb, Farbname rot; sauber und leerer Ordner grün; ohne `npm install` rot)

## gemeinsam

Regel (Link) | Mechanismus | Scheiter-Test
---|---|---
Prüfskripte laufen aus jedem Ordner ohne `PYTHONPATH` (Hooks, pre-commit, Aufruf von Hand: `python3 prozess/pruefungen/gemeinsam/lauf.py <ordner>.<modul>`) | `gemeinsam/lauf.py` | `gemeinsam/laufTest.py`

## kriterienregeln

Regel (Link) | Mechanismus | Scheiter-Test
---|---|---
[Kriterium ↔ Test](ablauf.md#dod-item-fertig): `testAuf1_4…` gehört zu AUF-1.4; Kennung höchstens einmal je Datei; ein Kriterium ohne Test ist erst rot, wenn ein offenes Item eines freigegebenen Plans es oder seine Anforderung nennt, vorher nennt der Stand es; Testdatei je Anforderung nach [T1](../technik/architektur.md) | `kriterienregeln/rueckverfolgung.py`, `kriterienregeln/kriterium.py`, `kriterienregeln/spur.py`, `lesen/plan.py` | `kriterienregeln/rueckverfolgungTest.py`
Spur vom Kriterium zum Test und zurück (Anliegen 53): Befehl `python3 prozess/pruefungen/gemeinsam/lauf.py kriterienregeln.rueckverfolgung AUF-1.4` ([T2](../technik/architektur.md)) | `kriterienregeln/rueckverfolgung.py` (`spur`) | `kriterienregeln/rueckverfolgungTest.py`

## rollenregeln

Regel (Link) | Mechanismus | Scheiter-Test
---|---|---
[Budget](ablauf.md#budget) nach Kontextfenster (Anliegen 22): 120.000 Meldung, 150.000 Sperre | `standregeln/belegung.py` (PreToolUse, PostToolUse); der Stand zeigt die Belegung; Freigabe durch den Stakeholder in `.git/arbiter/belegungsgrenze.txt` | `standregeln/belegungTest.py`, `standregeln/standTest.py`
`VORGEHEN.md`, `handoff/kritik-entwickler.md`, `Arbiter-old/`, `ArbiterMap/` sind für alle Rollen und den Koordinator nur lesbar, und eine Rolle schreibt nur in ihren Schreibpfaden (Write und Edit, nicht Bash) | `rollenregeln/schreibgrenze.py`, `rollenregeln/pfadsperren.py` (nur lesbar), `lesen/agenten.py` (Schreibpfade) | `rollenregeln/schreibgrenzeTest.py`
Stand und Ordner-CLAUDE.md beim Start einer Rolle | `rollenregeln/rollenkontext.py` | `rollenregeln/rollenkontextTest.py`
Dashboard (Retro 2, P4; Anliegen 158): Rolle, Belegung, Dauer und Zyklus je Lauf, Tokenstand mit Verteilung je Rolle, Legende mit höchstens fünf Wörtern je Eintrag | `rollenregeln/laufLog.py` (SubagentStop) schreibt `prozess/dashboard/laeufe.jsonl`, `rollenregeln/laufLesen.py` liest es, `rollenregeln/dashboard.py` erzeugt `dashboard.html` (mit `dashboardGruppen.py`, `dashboardDiagramm.py`, `dashboardStil.py`); ohne Befehl: `python3 prozess/pruefungen/gemeinsam/lauf.py rollenregeln.dashboard` | `rollenregeln/dashboardTest.py`

## standregeln

Regel (Link) | Mechanismus | Scheiter-Test
---|---|---
Stand in einer Zeile (SessionStart, nach jedem Agent-Aufruf): Etappe, Zyklus, Phase, nächster Schritt, Belegung, offene Anliegen, wer dran ist, fällige Nachprüfungen, Kriterien ohne Test, uncommittete Dateien | `standregeln/stand.py` (SessionStart, PostToolUse auf Agent) | `standregeln/standTest.py`
[Ablauf](ablauf.md): Etappe, Zyklus, Phase und nächster Schritt aus `handoff/plan.md`, `review.md`, `retro.md`, den Commits `Freigabe …` und `P<k>: …`; der Stand, das Lauf-Log (`zyklus`, `phase`) und das Dashboard nennen sie | `standregeln/phasenfolge.py` (`lage`) | `standregeln/phasenfolgeTest.py` (jede Stufe von Plan 1 bis Plan n+1), `rollenregeln/dashboardTest.py` (Log und Seite)
