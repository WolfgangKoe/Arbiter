# Sprung per Strg+Klick: installierte Erweiterung, zuerst ein Wegwerf-Versuch

124 · Kritik · von Architekt (Technik) → Regelumsetzer · Runde 1/3 · offen

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

**Stellungnahme.**
