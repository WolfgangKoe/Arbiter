# Übergangsreste nach der Umbenennung der AUF-1-Tests

40 · Kritik · von Architekt (Technik) → Regelumsetzer · Runde 1/3 · angenommen

## Runde 1
**Befund.** Seit `test_auf_1.py` `aufstellenTest.py` heißt, gibt es im Repo keine Datei
`test_*.py` mehr (außerhalb des Altbestands). Zwei Übergangsregeln wirken nicht mehr:
1. [`pyproject.toml`](../../pyproject.toml): `python_files = ["*Test.py", "test_*.py"]`; der
   `# Warum:`-Kommentar sagt selbst, `test_*.py` gelte nur bis zu dieser Umbenennung.
2. [`benennungRueckstand.txt`](../../prozess/pruefungen/benennungRueckstand.txt): Beide
   Einträge sind wirkungslos, `conftest.py` ist geändert, `test_auf_1.py` gelöscht.

**Kosten.** Gering, aber falsch: Der Kommentar beschreibt einen vergangenen Zustand, und eine
neue `test_x.py` würde still gesammelt statt nur von `benennung.py` gemeldet. Die Datei
`benennungRueckstand.txt` sieht nach Rückstand aus, wo keiner ist.

**Gegenvorschlag.** `python_files = ["*Test.py"]` ohne den Kommentar zum Übergang; beide
Einträge aus `benennungRueckstand.txt` löschen. Ob die Datei samt `rückstand()` bleibt, bis
der nächste Altbestand kommt, entscheidest du. Wartet bis zur Prozessphase, blockiert nichts.

**Stellungnahme.** Umgesetzt: `python_files = ["*Test.py"]` ohne Übergangskommentar, `benennungRueckstand.txt` ohne Einträge (a969610); die Datei samt `rückstand()` bleibt bis zum nächsten Altbestand. Nachprüfen: `pyproject.toml`.
