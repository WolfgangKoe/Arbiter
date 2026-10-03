# Sprung per Strg+Klick: installierte Erweiterung, zuerst ein Wegwerf-Versuch

124 · Kritik · von Architekt (Technik) → Regelumsetzer · Runde 1/3 · angenommen

## Runde 1
**Befund.** Der Stakeholder hat in [83](83-sprungErproben.md) F2 mit B beantwortet: Der
Sprung über den Namen (Strg+T, Strg+Umschalt+F) funktioniert bei ihm nicht; er will
Strg+Klick je Kriterium über eine installierte Erweiterung, zuerst einen Wegwerf-Versuch. Die
alte Erweiterung (`prozess/pruefungen/sprung/`, gelöscht nach 118, in git vor 89364ab) lief
nur im zweiten Fenster und holte ihr Ziel über `rueckverfolgung.py --json`.

**Kosten.** Ohne Versuch wiederholt sich 83: Code, der beim Stakeholder nie wirkt. Mit
Erweiterung: JavaScript neben Python, ein Schritt bei jeder Installation.

**Gegenvorschlag.** Ein Wegwerf-Versuch, den der Stakeholder in seinem VS Code (1.140)
ausprobiert:
1. Strg+Klick auf `AUF-1.3` in `domaene/anforderungen/` zeigt alle Tests zu AUF-1.3 (bei
   mehreren die Liste, etwa über einen DefinitionProvider); Strg+Klick auf `testAuf1_3…` in
   `technik/tests/akzeptanz/` springt zur Zeile des Kriteriums.
2. Das Ziel sucht die Erweiterung selbst in den Dateien, nicht über Pylance: Pylance ist bei
   ihm installiert, und Strg+T hat trotzdem nichts gezeigt.
3. Installation ohne zweites Fenster und ohne Entwicklermodus, in einem Schritt, den der
   Stakeholder einmal ausführt (etwa `code --install-extension <datei>.vsix` oder ein Ordner
   unter `~/.vscode/extensions/`); welcher Weg bei 1.140 wirkt, klärt der Versuch.
4. Ort der Dateien nach deiner Gliederung aus [114](114-pruefskripteOrdnenUndLesbarMachen.md).

Erledigt, wenn der Versuch liegt und eine Zeile sagt, wie der Stakeholder ihn installiert.
Danach frage ich ihn in 83, ob der Klick gelingt; erst dann folgen Scheiter-Test, Zeile in
`prozess/regeln.md` und T2.

**Stellungnahme.** Der Versuch liegt in `prozess/pruefungen/sprung/` (`extension.js`,
`suche.js`, `package.json`, `baue.py`, fertig gebaut `arbiter-sprung.vsix`). Er ist ein
DefinitionProvider für Markdown und Python und sucht das Ziel selbst in den Dateien (kein
Python-Aufruf, kein Pylance); mehrere Tests zeigt VS Code als Liste. Die Suche läuft im
Repo (4 Tests zu AUF-1.3, Rückweg zur Zeile des Kriteriums); in einer VS-Code-Instanz mit
leerem Erweiterungsordner ließ sich das vsix installieren, den Klick selbst konnte ich nicht
ausprobieren.

Installation: siehe Nachtrag unten. Probe: Strg+Klick auf `AUF-1.3` in
`domaene/anforderungen/phasen/aufstellen.md`; Strg+Klick auf `testAuf1_3…` in
`technik/tests/akzeptanz/phasen/aufstellen/auf1Test.py`. Hilft das nicht: Rechtsklick,
„Gehe zu Definition“, und Fehler aus „Ausgabe“ ➜ „Erweiterungshost“ melden. Nach deiner
Rückmeldung in 83 folgen Scheiter-Test, `regeln.md` und T2.

**Stellungnahme, Nachtrag (Anliegen 133).** Das Paket heißt jetzt `arbitersprung`; VS Code
behält das alte `arbiter-sprung` neben dem neuen, die Installation von oben ersetzt es nicht.
Anleitung, einmal, im Repo:
1. `code --uninstall-extension arbiter.arbiter-sprung`
2. `python3 prozess/pruefungen/sprung/baue.py && code --install-extension prozess/pruefungen/sprung/arbitersprung.vsix`
3. In VS Code „Developer: Reload Window“.
Die Probe bleibt wie oben. Ob das Paket in git steht oder jedes Mal gebaut wird, entscheidet
der Stakeholder: [143](143-sprungpaketInGit.md).

Rückmeldung: Ergebnis im Terminal:
(.venv) wolfgang@wolfgang-GT62VR-6RD:~/Dokumente/Arbiter_Structure$ code --install-extension prozess/pruefungen/sprung/arbiter-sprung.vsix
Installing extensions...
Extension 'arbiter-sprung.vsix' was successfully installed.
(node:368084) [DEP0169] DeprecationWarning: `url.parse()` behavior is not standardized and prone to errors that have security implications. Use the WHATWG URL API instead. CVEs are not issued for `url.parse()` vulnerabilities.
(Use `code --trace-deprecation ...` to show where the warning was created)
