# Regeln · gemeinsam

Regel (Link) | Mechanismus | Scheiter-Test
---|---|---
Prüfskripte laufen aus jedem Ordner ohne `PYTHONPATH` (Hooks, pre-commit, Aufruf von Hand: `python3 prozess/pruefungen/gemeinsam/lauf.py <ordner>.<modul>`) | `gemeinsam/lauf.py` | `gemeinsam/laufTest.py`
Testklone der Prüfungen erben keine `GIT_*`-Umgebung des Commit-Hooks, sonst landen ihre Einträge im echten Index (Anliegen 16130) | `conftest.py` (`GitRepo.git`) | `gemeinsam/gitRepoTest.py`
Die Schreib-Hooks einer laufenden Rolle (`anliegenregeln.erledigteLoeschen`, `standregeln.fortschritt`) schreiben nicht, solange ein Commit den Index sperrt, sonst scheitert der Teil-Commit mit „files were modified by this hook“ (Anliegen 16130) | `gemeinsam/gitAufruf.py` (`indexGesperrt`) | `gemeinsam/gitAufrufTest.py`, `anliegenregeln/erledigteLoeschenTest.py`, `standregeln/fortschrittTest.py`
