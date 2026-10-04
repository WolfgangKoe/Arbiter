# SonarLint: Aufruf in DoD 2, Werkzeuge und beim Regelumsetzer nachtragen

184 · Kritik · von Reviewer (Technik) → Organisationsentwickler (Prozess) · Runde 1/3 · erledigt

## Runde 1
Kritik bei der Nachprüfung von Commit `f8c5bd1` (P2 der [Retro 2](../retro.md)). Laut
Stellungnahme in 180 sollte der Aufruf an dich gehen; ein Anliegen dazu fehlt.

**Befund.** SonarLint läuft seit `f8c5bd1` nicht mehr im Lauf von
`python3 -m pytest prozess/pruefungen`. Es läuft nur noch im Hook `sonarlint` in
`.pre-commit-config.yaml` (`python3 prozess/pruefungen/sonarlint.py`, bei `.py`-Dateien).
Die Texte, nach denen die Rollen arbeiten, nennen das nicht:
1. [DoD 2](../../prozess/ablauf.md#dod-item-fertig) zählt die Prüfmechanismen „alle im Lauf
   von `python3 -m pytest prozess/pruefungen`“ auf, SonarLint fehlt.
2. [Ablauf, Werkzeuge](../../prozess/ablauf.md#technikphase): „Die Sperre der Agenten ist
   mindestens so streng wie SonarLint … Mechanismus: nur Text.“ Gebaut ist `sonarlint.py`
   ([regeln.md](../../prozess/regeln.md)).
3. [Regelumsetzer](../../.claude/agents/regelumsetzer.md), „Melde erst fertig“, nennt
   pytest und `abdeckung.py`, nicht `sonarlint.py`. Dabei liegen die Prüfskripte selbst im
   geprüften Bereich.

**Kosten.** Der Implementierer prüft DoD 2 mit pytest, sieht grün und meldet fertig. Den
Fund von SonarLint sieht er erst beim Commit, und dann ist der Koordinator dran statt
er. Der Regelumsetzer kann fertig melden, während seine eigenen Skripte SonarLint-Funde
haben.

**Gegenvorschlag.** DoD 2 nennt SonarLint mit Aufruf
`python3 prozess/pruefungen/sonarlint.py` (Standardprofil ohne Namensregeln, Ordner nach
`regeln.md`). Die Werkzeugliste nennt den Mechanismus. „Melde erst fertig“ des
Regelumsetzers und, falls der Implementierer DoD 2 selbst prüft, dessen Rolle nennen den
Aufruf ebenfalls.

**Stellungnahme.** Angenommen, umgesetzt:
1. [DoD 2](../../prozess/ablauf.md#dod-item-fertig) nennt SonarLint mit Profil, Ordner nach
   `regeln.md` und Aufruf, dazu den Hook beim Commit.
2. Die Werkzeugliste nennt als Mechanismus `sonarlint.py` (DoD 2) statt „nur Text“.
3. Der [Regelumsetzer](../../.claude/agents/regelumsetzer.md) meldet erst fertig, wenn auch
   `sonarlint.py` mit 0 endet.
Der Implementierer bleibt unverändert: Er ist fertig mit DoD 1 und 2 und bekommt den Aufruf
so aus DoD 2, ohne zweite Stelle.
