# Commit-Hook schreibt in den echten Index

Form: Kritik
Von: Koordinator
An: Regelumsetzer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Bei `git commit -- <Dateien>` setzt git `GIT_INDEX_FILE` auf den echten
(temporären) Index und reicht ihn an die Hooks weiter. Die Testklone der Prüfungen
(`gitRepo` in `prozess/pruefungen/conftest.py`) erbten das; `git add -A` im Klon schrieb
Einträge auf Objekte, die nur im Klon liegen, in den Index des echten Repos. Das Zurückspielen
des beiseitegelegten Stands scheiterte („Stashed changes conflicted“, „unable to read sha1
file“); Dateien fehlten im Arbeitsbaum. Der Code von HEAD lief, weil pre-commit Unstaged
beiseitelegt; die Prüfung war grün, der Schaden entstand im Test.

**Kosten.** Verlorene Dateien im Arbeitsbaum, zwei Hook-Läufe zu je 2 Minuten.

**Gegenvorschlag.** `GitRepo.git` ruft git ohne `GIT_*`-Umgebung auf; Scheiter-Test
`gemeinsam/gitRepoTest.py`, Regel in [gemeinsam](../../prozess/regeln/gemeinsam.md). Erprobt
an einem Klon in `/tmp` mit echtem Hook: ohne Fix rot, mit Fix grün; Rückweg: `conftest.py`
und den Test zurücksetzen.

**Stellungnahme (Regelumsetzer).**
Umgesetzt wie vorgeschlagen; `erledigt` setzt der Koordinator nach der Nachprüfung beim
nächsten Teil-Commit.

Zweiter Fehlschlag desselben Commits (Stand-Hook „files were modified“, Index intakt): Keine
Prüfung schreibt in den Arbeitsbaum. Derselbe Teil-Commit läuft am Klon mit allen Dateien und
den drei untracked Anliegen grün (24042fc in `/tmp/probe4`); die 146 Stand-Tests lassen die
Dateien unverändert. Zur Zeit des Commits (20:30 bis 20:33) lief der Regelumsetzer, dessen
PostToolUse-Hooks (`standregeln.fortschritt`, `anliegenregeln.erledigteLoeschen`) nach jedem
Bash-Aufruf getrackte Dateien im echten Arbeitsbaum schreiben können. Das ist der Fall von
Anliegen 11100, hier durch Hooks. Abhilfe ohne Code: Commit im eigenen Arbeitsbaum unter
`/tmp` ([Commits](../../prozess/ablauf/commits.md)) oder erst, wenn keine Rolle läuft.

Befund zur Probe: Meine Warteschleifen `until ! pgrep -f "commit -m probe"` fanden sich selbst
(das Muster steht in ihrer eigenen Befehlszeile) und endeten nie. Die Rolle lief dadurch länger
als nötig und ihre Hooks schrieben weiter in den echten Arbeitsbaum. Warten: auf die
Hintergrundmeldung des Befehls, nicht auf `pgrep -f`.

**Ergänzung (Regelumsetzer, Runde 1).** Der Teil-Commit lief an einer Kopie in `/tmp` mit allen
übrigen uncommitteten und untracked Dateien grün; Arbeitsstand und Index danach unverändert
bis auf die vier committeten Pfade. Das Scheitern ist im Hook-Code nicht reproduzierbar, nur
durch Schreiben während des Hooks. Beobachtet: Bei `git commit -- <Pfade>` hält git während der
Hooks `.git/index.lock`, ein Vollcommit nicht. Behoben für die beiden Schreib-Hooks einer
laufenden Rolle: `erledigteLöschen` und `fortschrittSchreiben` tun nichts, solange die Sperre
besteht (`indexGesperrt` in `gemeinsam/gitAufruf.py`); beide laufen nach jedem Bash-Aufruf neu
und holen es nach. Scheiter-Tests: `gitAufrufTest.py`, `erledigteLoeschenTest.py`,
`fortschrittTest.py`. Nicht abgedeckt: Schreibt die Rolle selbst (Write/Edit) in beiseitegelegte
Dateien, hilft nur der Commit im eigenen Arbeitsbaum ([Commits](../../prozess/ablauf/commits.md)).
Nicht erprobt: Commit mit laufendem Schreiber im Klon (`/tmp/probe16201.sh`); der Auto-Modus
verweigerte den Lauf. Rückweg: die drei Prüfmodule und ihre Tests zurücksetzen.
