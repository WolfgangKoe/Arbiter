# Kritik an 70c256b: Fehler beim Aufruf von Hand bleibt unsichtbar

197 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
Geprüft: `dashboard.py`, `laufLog.py`, `dashboardTest.py` (34 grün, ruff sauber). Die acht
Befunde aus Anliegen 196 sind umgesetzt; das hier ist neu.

**Befund.** `hauptlauf` fängt jeden Fehler von `dashboardSchreiben`, auch ohne `--still`, und
gibt dann nur `1` zurück. Der Aufruf von Hand (`python3 prozess/pruefungen/dashboard.py`,
[regeln.md](../../prozess/regeln.md), Zeile Dashboard) zeigte bisher den Traceback, jetzt
endet er ohne ein Wort. Das Warum am `except` begründet nur den Hook-Fall.

**Kosten.** Wer das Dashboard von Hand erzeugt und keine Seite bekommt, erfährt nicht, warum.

**Gegenvorschlag.** Im `except` ohne `--still` erneut auslösen (`raise`), mit `--still`
weiter `0`. `testFehlerBeimSchreibenIstMitStillStill` prüft dann
`pytest.raises(OSError)` statt `== 1`.

**Stellungnahme.**
