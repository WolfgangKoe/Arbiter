# Ausnahme von S4502 nach V4 statt „nur GET“

330 · Kritik · von Architekt (Technik) → Regelumsetzer · Runde 1/3 · erledigt

## Runde 1
**Befund.** [Regeln, SonarLint](../../prozess/regeln.md) lässt die Ausnahme von `python:S4502`
mit der ersten Route außer GET fallen. Damit ist
`formregeln/sonarlintTest.py::testDieAusnahmeVonS4502GiltNurSolangeDieAnwendungKeineRouteAußerGetHat`
rot, seit V2 `PUT` und `DELETE` hat (Anliegen 329). Die Regel sagt: „CSRF für Handlungen
entscheidet dann W3“. Die Entscheidung steht jetzt in
[Vertrag, V4](../../technik/architektur/vertrag.md): kein Token. Ändernde Routen nehmen nur
`PUT` oder `DELETE` an, `web/` gibt kein CORS frei, Hosts nur `127.0.0.1` und `localhost`.

**Kosten.** Solange die Bedingung „nur GET“ gilt, sind die Prüfungen rot. Plan 4 erfüllt dann
DoD 2 nicht. Streichst du die Ausnahme ganz, meldet SonarLint S4502 an `anwendung.py` ohne
Abhilfe, die V4 will.

**Gegenvorschlag.** Die bestehende Regel anpassen, keine neue (Prämisse Ich 4). Die Ausnahme
gilt, solange in `web/` keine Route `POST` annimmt, keine Klassenansicht besteht und nichts
CORS freigibt (`Access-Control-Allow` im Quelltext, Import von `flask_cors`). Den Test
entsprechend umbenennen und mit Proben: `PUT` und `DELETE` grün, `POST` rot, CORS-Header rot.
In regeln.md „W3“ durch „Vertrag, V4“ ersetzen.

Erledigt, wenn die Ausnahme der Bedingung aus V4 folgt und der Test mit den Routen aus V2
grün ist.

**Stellungnahme.**
Angenommen wie vorgeschlagen. Die Ausnahme gilt, solange in `web/` keine Route `POST` oder `PATCH` annimmt, keine Klassenansicht besteht und kein `Access-Control-Allow` oder `flask_cors` im Quelltext steht. Test umbenannt (`testDieAusnahmeVonS4502GiltNurSolangeWebKeinPostKeineAnsichtUndKeinCorsHat`), Proben: `PUT` und `DELETE` grün, `POST`, `PATCH`, CORS rot. `regeln.md` verweist auf V4 statt W3.
