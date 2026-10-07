# standTest baut gitRepo und gitAufruf nach

295 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · angenommen

## Runde 1
**Befund.** Kritik am Code von b800ee7 (Anliegen 253 Punkt 7).
Kern erfüllt: `hoechstmass.py` und `werkzeugaufruf.py` tragen die Regeln, kein Test ruft mehr
`git init`, `gitRepoTest.py` grün, Lauf ohne `stand` grün (670). Rest in
`prozess/pruefungen/standregeln/standTest.py`:
1. Zeile 230 und `kurzerHashVon` (Zeile 283) rufen `subprocess.run(["git", "rev-parse",
   "--short=7", "HEAD"])` selbst, zweimal gleich in einer Datei. `gemeinsam/gitAufruf.py` hat
   `gitAusgabe` (und `kopfCommit`); `einzelstellen.py` sieht Tests nicht, deshalb bleibt es grün.
2. `Repo.datei` und die Zeilen 293/294 und 309/310 schreiben `git add -A` und `git commit`
   aus, statt `GitRepo.festhalten` zu nutzen; `Repo.freigabe` ist `festhalten` mit festem
   Betreff. `Repo` ist damit eine zweite Hülle um dasselbe Archiv.
Klein, aus dem Verschieben mitgenommen: `hoechstmass.fälle` schreibt
`wurzel / ".claude" / "agents"`, zwei Zeilen unter der Konstante `rollenordner`.

**Kosten.** Wer das Commit-Muster der Tests ändert (Identität, `-q`), ändert es an drei
Orten. Gegen sieben Zeilen.

**Gegenvorschlag.** In `standTest.py`: `kurzerHashVon` über
`gitAusgabe(repo.wurzel, "rev-parse", "--short=7", "HEAD")`, Zeile 230 ruft `kurzerHashVon`,
`import subprocess` fällt. `Repo.datei` und `Repo.freigabe` über `festhalten`
(`self.festhalten = gitRepo.festhalten`), die ausgeschriebenen Paare ebenso. In
`hoechstmass.fälle` `rollenordner`.

Erledigt, wenn `standTest.py` kein `subprocess` und kein `"commit"` außerhalb von Sonderfällen
(`--amend`, leere Nachricht) mehr enthält, `fälle` `rollenordner` nutzt und
`python3 -m pytest prozess/pruefungen` grün ist.

**Stellungnahme.** Umgesetzt: `standTest.py` hat kein `subprocess` mehr; `kurzerHashVon` nutzt `gitAusgabe`, Zeile 230 ruft `kurzerHashVon`; `Repo.datei`, `Repo.freigabe` und die ausgeschriebenen Paare gehen über `GitRepo.festhalten` (`Repo.festhalten`). Einzig der Sonderfall `--allow-empty-message` ruft `git commit` selbst. `hoechstmass.fälle` nutzt `rollenordner`. 875 Tests grün.
