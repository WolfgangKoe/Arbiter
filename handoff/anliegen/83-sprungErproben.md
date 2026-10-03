# Sprung zwischen Kriterium und Test: Klick erproben, behalten oder löschen

83 · Fragen · von Architekt (Technik) → Stakeholder · Runde 1/3 · offen

## Runde 1
**Befund.** Aus Anliegen 53: Befehl `rueckverfolgung.py AUF-1.3` (Weg B) oder eine
VS-Code-Erweiterung `prozess/pruefungen/sprung/` (Weg C).

**Stellungnahme (Stakeholder).** Muss ich VS Code dafür neu starten? Denn aktuell
funktioniert es nicht.

## Runde 2
**Befund.** Die Erweiterung wirkt nur in einem zweiten Fenster (`--extensionDevelopmentPath`).

**Stellungnahme (Stakeholder).** Das zweite Fenster öffnet sich nicht. Beim Versuch die
Datei in dem zweiten Fenster zu öffnen schaltet mich auf das erste VS Code Fenster zurück
ohne in eine Datei zu springen. Es funktioniert damit nicht!

Ich verstehe ehrlich gesagt auch nicht, warum hierfür ein neues Fenster geöffnet werden muss.
Mit "Sprung" meinte ich, dass die jeweiligen Dateien smart miteinander verlinkt sind. Das
machst du doch an anderer Stelle ganz häufig.

## Runde 3
**Befund.** Links auf Zeilen veralten; stabil ist ein Link je Anforderung auf ihre Testdatei.

**F1 · Welcher Sprung?**
- A: Link je Anforderung auf ihre Testdatei, geprüft; Erweiterung löschen.
- B: nur der Befehl; Erweiterung löschen.
Empfehlung: A.

Antwort: Die Erweiterung kann gelöscht werden. Gibt es keine Möglichkeit eine Art Tag zu setzen, so dass dieser mit der Zeile mitgeht? Software-Entwickler "springen" die ganze Zeit durch das System, weil die geschriebene Methode ja überall gleich heißt. Sowas muss doch einfach gehen.

## Nach Runde 3
**Befund.** Löschen gilt: [118](118-sprungErweiterungLoeschen.md) an den Regelumsetzer.

Deine Frage: Ja, die Marke gibt es schon. Es ist die Kennung im Namen: `AUF-1.3` im
Kriterium, `testAuf1_3…` im Test. Sie wandert mit, weil sie in der Zeile steht, nicht auf
sie zeigt. Genau so springen Entwickler: über den Namen, nie über eine Zeilennummer. F12
(„Gehe zu Definition“) klappt in Python, weil Pylance beide Enden kennt, Aufruf und Definition
in derselben Sprache. Zwischen einem Satz in Markdown und einer Python-Funktion gibt es keinen
solchen Dienst; den hätte die Erweiterung ergänzt. Ohne sie springt VS Code über die Suche
nach dem Namen, und die findet die Stelle immer dort, wo sie gerade steht:
- Kriterium → Tests: Strg+T, `auf1_3` tippen: alle Tests zu AUF-1.3, Enter springt hin.
- Test → Kriterium: Strg+Umschalt+F, `AUF-1.3`: die Zeile in `aufstellen.md`.

Damit braucht es auch den Link je Anforderung (F1 A) nicht. Steht in
[T2](../../technik/architektur.md).

**Kosten.** Keine: kein Code, keine Links, nichts veraltet; ein Tastendruck statt eines
Klicks. Unerprobt ist, ob Strg+T in deinem VS Code die Tests listet (Pylance tut das
standardmäßig). Strg+Klick je Kriterium ginge nur mit einer Erweiterung, einmal als Paket
installiert (`code --install-extension`, kein zweites Fenster), nach jeder Änderung an ihr
neu gebaut; erst ein Wegwerf-Versuch.

**Gegenvorschlag.** Sprung über den Namen wie oben, keine Links, keine Erweiterung.

**F2 · Reicht der Sprung über den Namen?** Probier: Strg+T, `auf1_3`.
- A: Ja. Ich setze `erledigt`.
- B: Nein, Strg+Klick je Kriterium: Anliegen an den Regelumsetzer für eine installierte
  Erweiterung, zuerst ein Wegwerf-Versuch.
Empfehlung: A.

Antwort: B, es funktioniert in VS Code mit den angegebenen Shortcuts nicht. 

Danach setzt du den Kopf auf `beantwortet`; sonst bleibt das Anliegen bei dir liegen.
