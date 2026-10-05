# Schreibbilanz läuft nicht: Hook nicht eingehängt

287 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
**Befund.** Kritik am Code von 180d1d1 (Anliegen 253 Punkt 2).
1. `beimStart` und `beimEnde` sind von `rollenregeln/schreibgrenze.py` nach
   `rollenregeln/schreibBilanz.py` gezogen; `schreibgrenze.entscheide` antwortet nur noch auf
   `PreToolUse`. In `.claude/settings.json` stehen unter `SubagentStart` und `SubagentStop`
   aber weiter `rollenregeln.schreibgrenze`, `schreibBilanz` steht dort nirgends
   (`git grep schreibBilanz 180d1d1 -- .claude`: leer). Die Stellungnahme in 253 sagt „beide
   in `settings.json`“; im Diff kommt nur `freigabeSperre` hinzu. Beleg aus diesem Lauf: Der
   Kontext beim SubagentStart nennt keine Schreibpfade mehr.
2. `rollenregeln/dashboard.py` endet zweimal mit `if __name__ == "__main__":` (Zeilen 114 und
   118 in 180d1d1); der zweite Block ist toter Code.

**Kosten.** 1: Die Rolle erfährt beim Start ihre Schreibpfade nicht mehr, und die Bilanz beim
Ende (Änderungen per Bash außerhalb der Schreibpfade, Commit durch eine Rolle) läuft gar
nicht. Zusammen mit 278 (Meldung erreicht den Koordinator nicht) ist die Schreibgrenze für Bash
damit ganz Text. Keine Prüfung merkt es: `formregeln/einstellungen.py` prüft nur, dass das
Skript existiert. 2: eine Zeile Verwirrung.

**Gegenvorschlag.**
1. In `settings.json` unter `SubagentStart` und `SubagentStop` `rollenregeln.schreibgrenze`
   durch `rollenregeln.schreibBilanz` ersetzen.
2. Mechanismus, angepasst aus `formregeln/einstellungen.py` (Prämisse Ich 4): Jedes
   Hook-Modul nennt seine Ereignisse schon im Docstring (`Hook (SubagentStart,
   SubagentStop): …`). Die Prüfung verlangt, dass jedes in `settings.json` eingetragene Modul
   unter genau den Ereignissen steht, die sein Docstring nennt, und umgekehrt. Scheiter-Test:
   `schreibgrenze` unter `SubagentStart` ist rot, ein Modul mit `Hook (X)` ohne Eintrag ist
   rot. Das hätte 1 gefangen; nennen heute nicht alle Hook-Docstrings ihr Ereignis, ist das
   ein Satz Docstrings mehr.
3. Den doppelten `__main__`-Block in `dashboard.py` streichen.

Erledigt, wenn `schreibBilanz` bei Start und Ende läuft, die Prüfung aus 2 an beiden
Gegenbeispielen rot wird und `python3 -m pytest prozess/pruefungen` grün ist.

**Stellungnahme.** Status `offen`, nichts umgesetzt. Der Auto-Mode-Klassifikator lehnte meinen Schreibaufruf ohne Begründung ab. Er enthielt die Umstellung der Docstrings der Hook-Module und den Eintrag `schreibBilanz` statt `schreibgrenze` unter `SubagentStart` und `SubagentStop` in `.claude/settings.json`. Welcher Teil gesperrt war, weiß ich nicht, vermutlich `settings.json`. Ich habe den Aufruf weder zerlegt noch anders versucht. Gleichzeitige Läufe: Die Kette (253 P7) ändert Testcode und `conftest.py`, keinen Hook-Code; meine Dateien waren getrennt (`settings.json`, `formregeln/einstellungen.py` mit Test, Docstrings der Hook-Module, `rollenregeln/dashboard.py`).
Geplant: (1) `settings.json` wie im Gegenvorschlag; (2) `einstellungen.py` vergleicht je über `lauf.py` eingetragenes Modul die ersten Docstring-Zeile `Hook (A, B): …` mit den Ereignissen in `settings.json` (Mengengleichheit; ein Modul mit `Hook (X)` ohne Eintrag ist rot); (3) Scheiter-Test an beiden Gegenbeispielen plus Stand-Test; (4) elf Hook-Docstrings auf `Hook (…)`: stand, belegung, bashPositivliste, schlussantwort (PreToolUse, SubagentStop), lesegrenze, rollenkontext, laufLog, erledigteLoeschen, statusrecht, freigabeSperre, anliegennummer; (5) doppelten `__main__`-Block in `dashboard.py` streichen; (6) Zeile in `prozess/regeln.md`.
Nächster Schritt: Stakeholder gibt den Eingriff in `.claude/settings.json` frei, oder er trägt Punkt 1 selbst ein; dann setze ich 2 bis 6 um.
