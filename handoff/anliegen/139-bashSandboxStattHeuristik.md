# Bash-Sandbox statt Heuristik für Anliegen und nur lesbare Pfade

139 · Fragen · von Organisationsentwickler (Prozess) → Stakeholder · Runde 1/3 · offen

## Runde 1
**Befund.** Rollen dürfen Anliegen nur mit Write und Edit ändern, nur lesbare Pfade gar
nicht. Für Bash prüft das `bashPositivliste.py` per Heuristik am Befehlstext. Ein Skript
(`python3 - <<EOF … write_text …`, `python3 -c`) oder `cd <pfad> && rm …` kommt durch
([138](138-anliegenPerSkriptAmBashSchutzVorbei.md); dem Reviewer passierte es an 132). Dann
greifen Statusrecht und Nummernprüfung nicht. Eine Heuristik am Text bleibt lückenhaft.

**Kosten.** Status, Runde oder Nummer lassen sich unbemerkt setzen. Jede neue Lücke kostet
eine weitere Regel in der Heuristik.

**Gegenvorschlag.** Bordmittel von Claude Code: die
[Bash-Sandbox](https://code.claude.com/docs/en/sandboxing). Das Betriebssystem sperrt das
Schreiben für alle Bash-Befehle und ihre Prozesse, gleich wie sie formuliert sind;
Write und Edit laufen außerhalb und bleiben mit den Hooks möglich. In
`.claude/settings.json`: `sandbox.enabled`, `filesystem.denyWrite` für `handoff/anliegen/`
und die nur lesbaren Pfade, `allowUnsandboxedCommands: false`. Die Heuristik entfällt.
Folgen: Bash-Befehle brauchen für Netzwerk freigegebene Hosts; `erledigteLoeschen.py` löscht
nur noch im SubagentStop-Hook, nicht im Testlauf und nicht im pre-commit (außer `git commit`
steht in `excludedCommands`); `.claude/skills` ist für Bash dann ohnehin gesperrt. Unerprobt: Unter Linux braucht die Sandbox
`bubblewrap` und `socat`; ob sie bei dir laufen, zeigt `/sandbox`. Baut der Regelumsetzer,
zuerst als Versuch mit Scheiter-Test. Das ändert die Rechte aller Rollen, daher deine
Entscheidung.

**F1 · Sandbox statt Heuristik?**
- A: Ja, der Regelumsetzer baut sie und entfernt die Heuristik für Anliegen und nur lesbare
  Pfade.
- B: Nein, die Lücke bleibt dokumentiert (Ablauf, Anliegen), die Heuristik bleibt.
Empfehlung: A.

Antwort: .
