# Ruff-Regelsatz: Der Kommentar verweist auf eine Stelle, die ihn nicht nennt

85 · Kritik · von Architekt (Technik) → Organisationsentwickler · Runde 1/3 · offen

## Runde 1
Gegenstand: 3e61977, `pyproject.toml` (Kritik am Code, Linter-Konfiguration). Sonst in
Ordnung: `complexipy==8.0.*` mit Begründung; die Grenzproben machen `komplexitaetTest.py` rot,
wenn `max-complexity-allowed` oder `max-branches` steigt oder `PLR0912` aus `select` fällt
(Wegwerf-Versuch in einer Kopie, alle drei rot).

**Befund.** Der Kommentar über `select` lautet nach Anliegen 57:
„# Warum: Stil, ARG, PLR2004, PLR0913, FBT, ERA nach prozess/ablauf.md (Technikphase,
Werkzeuge).“ Der Absatz Werkzeuge in [`prozess/ablauf.md`](../../prozess/ablauf.md) nennt
von ruff nur `PLR0912` und was nicht verwendet wird. ARG, PLR2004, PLR0913, FBT und ERA
stehen nur in `VORGEHEN.md` (E37), und das löscht der Stakeholder.

**Kosten.** Nach dem Löschen hat der Regelsatz keine Quelle. Wer eine Regel aus `select`
streicht, verstößt gegen nichts Nachlesbares, und der Reviewer kann es nicht beanstanden.

**Gegenvorschlag.** Im Absatz Werkzeuge von `prozess/ablauf.md` „ruff `PLR0912` (12)“ zu
„ruff (Stil, ARG, PLR2004, PLR0913, FBT, ERA, `PLR0912` mit 12)“ erweitern. Dann stimmt der
Kommentar, und `pyproject.toml` bleibt, wie es ist.

**Stellungnahme.**
