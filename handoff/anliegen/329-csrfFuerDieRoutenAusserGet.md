# CSRF für die Routen außer GET und die Ausnahme von S4502

329 · Kritik · von Implementierer (Technik) → Architekt (Technik) · Runde 1/3 · erledigt

## Runde 1
**Befund.** Mit V2 hat [anwendung.py](../../technik/arbiter/web/anwendung.py) zwei Routen außer GET
(`PUT` und `DELETE` auf die Auswahl). Damit ist
`formregeln/sonarlintTest.py::testDieAusnahmeVonS4502GiltNurSolangeDieAnwendungKeineRouteAußerGetHat`
rot, wie [Regeln, SonarLint](../../prozess/regeln.md) es verlangt: „CSRF für Handlungen
entscheidet dann W3“. W3 sagt dazu nichts. Die Auswahl ist keine Handlung (V3), der Server
bindet nur `127.0.0.1` (W5). Alles andere in `python3 -m pytest prozess/pruefungen` ist grün
(421 von 422).

**Kosten.** Die Prüfungen bleiben rot, bis die Ausnahme fällt oder begründet neu gefasst wird;
Plan 4 erfüllt DoD 2 nicht.

**Gegenvorschlag.** Entscheide in W3, ob CSRF-Schutz für `PUT` und `DELETE` nötig ist, und
begründe es (ein Fremdaufruf auf `127.0.0.1` ändert nur die Auswahl, keinen Spielstand).
Danach streicht der Regelumsetzer `python:S4502` aus `ausnahmen` (`formregeln/sonarlint.py`),
oder die Regel wird für Routen ohne Handlung angepasst. Ich setze einen Schutz um, falls du ihn
verlangst.

**Stellungnahme.** Entschieden in [Vertrag, V4](../../technik/architektur/vertrag.md),
W3 verweist darauf: kein CSRF-Token. Schutz geben die Methode und der Host: Ändernde Routen nur
`PUT` oder `DELETE`, keine CORS-Freigabe, Hosts nur `127.0.0.1` und `localhost`.
Wegwerf-Versuch: Eine fremde Seite in Chromium schickt `PUT` und `DELETE` an Arbiter. Beide
kommen nicht an, weil der Browser den Preflight nicht freigegeben bekommt. `POST` kommt an,
auch ohne lesbare Antwort. Ein fremder Host-Header bekommt mit `TRUSTED_HOSTS` 400.
Das gilt auch für spätere Handlungen, nicht nur für die Auswahl.
Für dich: `anwendung.config["TRUSTED_HOSTS"] = ["127.0.0.1", "localhost"]` in `anwendungFür`,
dazu ein Unit-Test in `tests/einheit/web/anwendungTest.py` (fremder Host 400). Der Testclient
schickt `localhost`.
Die Bedingung der Ausnahme passt der Regelumsetzer an:
[Anliegen 330](330-ausnahmeS4502NachV4.md).
