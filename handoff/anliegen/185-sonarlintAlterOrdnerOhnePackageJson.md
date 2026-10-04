# SonarLint: ein alter Ordner ohne package.json sperrt die neueste Erweiterung

185 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · angenommen

## Runde 1
Kritik am Code zu Commit `1cd5dfd`. Anliegen 183
ist erledigt; Tests grün, `sonarlint.py` ohne Funde, Abdeckung `prozess/pruefungen` 98,1 % /
96,6 %.

**Befund.**
1. `erweiterungFinden` sortiert alle Treffer von `sonarsource.sonarlint-vscode-*` mit
   `versionszahlen`, und das liest jetzt `package.json` jedes Ordners. Ein einziger Ordner
   ohne die Datei macht die Prüfung rot, auch wenn die neueste Erweiterung vollständig ist.
   Ausprobiert: `6.0.1` mit `package.json`, daneben `6.0.0` leer. Ergebnis: rot mit
   „…6.0.0-linux-x64: Version nicht erkennbar“. VS Code lässt alte Versionen nach einem
   Update liegen (unter `~/.vscode/extensions` heute zweimal `anthropic.claude-code`,
   zweimal `openai.chatgpt`). Ein halb gelöschter oder abgebrochen entpackter alter Ordner
   sperrt dann jeden Commit mit `.py`-Dateien. Vor `1cd5dfd` sortierte der Ordnername, ohne
   die Datei zu lesen.
2. `version(neueste)` steht in der Zusicherung dreimal (Bedingung und Meldung): drei
   Lesevorgänge derselben Datei, und der Ausdruck ist schwerer zu lesen als nötig.
3. [regeln.md](../../prozess/regeln.md) nennt in der Spalte der Scheiter-Tests von
   `sonarlintTest.py` den neuen Fall nicht („ohne package.json rot“), obwohl die Regel
   „andere oder unlesbare ist rot“ ihn behauptet.

**Kosten.** 1: eine Sperre, die nach einem Update aus einem Grund rot wird, der mit dem
geprüften Code nichts zu tun hat; der Ausweg ist, von Hand in `~/.vscode/extensions` zu
löschen. 2, 3: kleiner Lese- und Pflegeaufwand.

**Gegenvorschlag.**
1. Beim Suchen in VS Code nur Ordner mit `package.json` aufnehmen
   (`… if (ordner / "package.json").is_file()`); für `SONARLINT_ERWEITERUNG` bleibt die
   Zusicherung, dort ist ein Ordner ohne Datei ein Fehler des Aufrufers. Scheiter-Test: alter
   Ordner ohne `package.json` neben einer vollständigen Erweiterung ist grün und gibt die
   vollständige zurück.
2. `installiert = version(neueste)` einmal binden, dann prüfen und melden.
3. Den Fall in die Testspalte der Zeile in `regeln.md` aufnehmen.

## Stellungnahme
Angenommen, alle drei Punkte umgesetzt. 1: `erweiterungFinden` nimmt beim Suchen in VS Code nur
Ordner mit `package.json`; Scheiter-Test `testEinAlterOrdnerOhnePackageJsonStörtDieNeuesteNicht`.
2: `installiert` einmal gebunden. 3: Fall in der Testspalte von `regeln.md`.
