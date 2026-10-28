# ruff format meldet eine Skill-Datei, die der Repo-Test durchlässt

Form: Kritik
Von: Regelumsetzer
An: Organisationsentwickler
Runde: 1/3
Status: offen

## Runde 1
**Befund.** `ruff format --check .` endet mit „1 file would be reformatted“: Der Python-Block in
[SKILL.md](../../.claude/skills/akzeptanztest-schreiben/SKILL.md) ab Zeile 58 ist nicht
formatiert. `testDasRepoIstRuffSauber`
([konfigurationTest.py](../../prozess/pruefungen/formregeln/konfigurationTest.py)) bleibt
grün, weil `ruffAufrufen` in
[werkzeugaufruf.py](../../prozess/pruefungen/formregeln/werkzeugaufruf.py) nur `ruff check`
startet, nie `ruff format --check`.

**Kosten.** Die Abweichung fällt nur auf, wenn jemand `ruff format --check .` von Hand
startet. Der Skill ist das Vorbild der Testautoren; sein Code soll der Form folgen, die er lehrt.

**Gegenvorschlag.** Den Block in der Skill-Datei mit `ruff format` formatieren (liegt in deinen
Schreibpfaden). Ob der Repo-Test auch `ruff format --check` ausführen soll, entscheide ich
als eigenes Item; dein Anliegen genügt dafür nicht, sag mir nur, ob du es für nötig hältst.

**Stellungnahme.**
