# Sprung per Strg+Klick: installierte Erweiterung, zuerst ein Wegwerf-Versuch

124 · Kritik · von Architekt (Technik) → Regelumsetzer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Der Stakeholder hat in [83](83-sprungErproben.md) F2 mit B beantwortet: Der
Sprung über den Namen (Strg+T, Strg+Umschalt+F) funktioniert bei ihm nicht; er will
Strg+Klick je Kriterium über eine installierte Erweiterung, zuerst einen Wegwerf-Versuch.

**Kosten.** Ohne Versuch wiederholt sich 83: Code, der beim Stakeholder nie wirkt. Mit
Erweiterung: JavaScript neben Python, ein Schritt bei jeder Installation.

**Gegenvorschlag.** Ein Wegwerf-Versuch in seinem VS Code (1.140): Strg+Klick auf `AUF-1.3`
zeigt die Tests, Strg+Klick auf `testAuf1_3…` springt zum Kriterium; installierbar in einem
Schritt. Erledigt, wenn der Versuch liegt und der Stakeholder ihn erprobt hat.

**Stellungnahme.** Der Versuch lag in `prozess/pruefungen/sprung/` (DefinitionProvider,
`.vsix`) und ließ sich beim Stakeholder installieren. Seine Entscheidung: Es gibt keinen
Weg, der die Verknüpfung von Anforderung, Akzeptanztest und Produktivcode per Klick liefert,
ohne Skripte und VS-Code-Erweiterungen zu bauen, deren Token sich nicht lohnen („Wenn es
nicht geht, geht es nicht. […] Wir bauen etwas anderes.“). Umgesetzt:
- Ordner `prozess/pruefungen/sprung/` samt Paket gelöscht, die `.gitignore`-Zeile für
  `*.vsix` und die Zeile „Bekannte Lücke JavaScript“ in `prozess/regeln.md` entfernt.
  Die Zeile zu `rueckverfolgung.py` in `regeln.md` verspricht den Sprung nicht mehr.
- Offen für den Architekten: [T2](../../technik/architektur.md) nennt noch „Strg+Klick in
  VS Code: Anliegen 124“; [83](83-sprungErproben.md) hängt an `sprung/`. Beides
  fortschreiben, die Entscheidung des Stakeholders steht oben.

Nachprüfen: Architekt. Der Stakeholder hat die Löschung und `.gitignore` noch nicht committet;
der Koordinator committet sie mit den übrigen Änderungen.
