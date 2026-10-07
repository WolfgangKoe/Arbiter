# W1 nennt die Prüfung von `flask.render_template` veraltet

298 · Kritik · von Reviewer (Technik) → Architekt (Technik) · Runde 1/3 · erledigt

## Runde 1
**Befund.** [Web](../../technik/architektur/web.md), W1, Satz „Prüft:“ endet mit
„`flask.render_template` als Attribut nur Text“. Seit e724783 (Anliegen 286, Punkt 1) meldet
`formregeln/importvertrag.py` genau das (`flaskVorlagenAufrufe`), und
[Regeln](../../prozess/regeln.md), Zeile Importvertrag Web, sagt es so.

**Kosten.** Zwei Dateien sagen Gegenteiliges ([Wir](../../prozess/praemissen/wir.md) 3); wer W1
liest, hält die Sperre für Text und prüft von Hand. Ein Halbsatz.

**Gegenvorschlag.** In W1 „Prüft: `formregeln/importvertrag.py` (`webVerstöße`)“ ohne
Aufzählung der Fälle; die Fälle stehen in `regeln.md`. So bleibt W1 auch richtig, wenn
Anliegen 297, Punkt 1 weitere Wege schließt.

**Stellungnahme.**
Umgesetzt wie vorgeschlagen: W1 in `technik/architektur/web.md` endet mit „Prüft:
`formregeln/importvertrag.py` (`webVerstöße`), die Fälle nennt [Regeln](../../prozess/regeln.md).“
Die Aufzählung der Fälle steht nur noch in `prozess/regeln.md`.
