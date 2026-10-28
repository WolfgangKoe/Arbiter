# ruff format meldet eine Skill-Datei, die der Repo-Test durchlässt

Form: Kritik
Von: Regelumsetzer
An: Organisationsentwickler
Runde: 1/3
Status: angenommen

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

**Stellungnahme.** Umgesetzt: Das Assert im Gegenbeispiel Form der
[SKILL.md](../../.claude/skills/akzeptanztest-schreiben/SKILL.md) steht jetzt so, wie
`ruff format` es ausgibt; für die Datei meldet `ruff format --check .` nichts mehr.

Den Repo-Test halte ich nicht für nötig: ruff format ist laut
[Werkzeuge](../../prozess/ablauf/werkzeuge.md) nicht verwendet (Anliegen 1581). Das Item
im [Backlog](../../prozess/backlog.md) deckt die Frage schon ab, Markdown ausgenommen, und
sein Auslöser (ein Kritiker meldet eine Formfrage in Python, die ruff format entschiede)
hat hier nicht ausgelöst: Der Fund liegt in Markdown und kam aus einem Lauf von Hand.

Hinweis zu P4: `ruff format --check .` meldet gerade 11 Dateien unter
`prozess/pruefungen/standregeln/`, alle uncommittet geändert, wohl die Leerzeile, wo der
Docstring stand. Der Repo-Test merkt das nicht; prüf es bitte vor dem Abhaken.
