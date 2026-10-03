# Spur vom Kriterium zum Test und zurück: Befehl und VS-Code-Versuch

53 · Kritik · von Architekt (Technik) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
**Befund.** Der Stakeholder will von jedem Kriterium zu seinen Tests springen und zurück.
Entschieden (Anliegen 46, Commit `91905db`): Weg B „auf jeden Fall“, Weg C als erster
Versuch, VS Code ist sein Editor. Regel T2 in
[`technik/architektur.md`](../../technik/architektur.md): Der Weg wird berechnet, nicht
gespeichert; keine Links in Anforderung oder Test. Heute gibt es nur die Suche.

**Kosten.** Fachkritiker und Stakeholder suchen je Kriterium per Hand
(`AUF-1\.4|Auf1_4`); mit jeder Anforderungsdatei mehr.

**Gegenvorschlag.**
1. **B, Spur-Befehl.** `python3 prozess/pruefungen/rueckverfolgung.py AUF-1.4` gibt das
   Kriterium und jeden seiner Tests als `pfad:zeile` aus, eine Zeile je Fundstelle.
   Eingabe ebenso ein Testname (`testAuf1_4…`) oder `pfad:zeile` einer Datei. Das Skript
   liest beide Seiten schon; nur die Zeilennummern fehlen (`ast` liefert `lineno`). Ohne
   Argument bleibt es die Prüfung. Im Terminal von VS Code springt Strg+Klick auf
   `pfad:zeile`. Scheiter-Tests: unbekannte Kennung meldet einen Fehler; ein Kriterium
   mit zwei Tests liefert drei Zeilen.
2. **C, Versuch.** Eine VS-Code-Erweiterung unter `prozess/pruefungen/sprung/`
   (`package.json`, `extension.js`, zusammen unter 80 Zeilen): ein `DocumentLinkProvider`
   für Markdown und Python macht `AUF-1.4` in `domaene/anforderungen/` und `testAuf1_4…` in
   `technik/tests/akzeptanz/` zu Links; das Ziel holt er beim Klick aus B (einmal je
   Datei, `--json` als Ausgabeform von B genügt). Ziel-URI `file:///…#L161`.
   Start ohne Installation: `code --extensionDevelopmentPath=prozess/pruefungen/sprung .`
   Mein Vorab-Befund aus VS Code 1.140: Der Öffner liest `#L<n>` aus dem Fragment
   (`/^L?(\d+)(?:,(\d+))?…/` in `workbench.desktop.main.js`), und
   `--extensionDevelopmentPath` ist vorhanden. Unerprobt: der Klick selbst; den macht der
   Stakeholder. Danach entscheidet er: behalten (dann eslint und ein Test) oder löschen.
   Gibt es zwei Treffer (Kriterium mit mehreren Tests), springt der Link zum ersten Test;
   die Liste aller liefert B.
3. Passt `prozess/pruefungen/` nicht als Ort für C, schlage einen vor; der Ordner liegt in
   deinen Schreibpfaden.

**Stellungnahme.**
