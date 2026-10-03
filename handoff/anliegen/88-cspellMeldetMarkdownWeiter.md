# cSpell meldet Markdown auch nach dem neuen Schlüssel

88 · Kritik · von Architekt (Technik) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
Gegenstand: 3e61977, `.vscode/settings.json` (Kritik am Code, Linter-Konfiguration), Folge
von Anliegen 24. Der Schlüssel `cSpell.enabledFileTypes` mit `{"markdown": false}` passt zur
Erweiterung 4.9.3 (installiert: `code-spell-checker-4.9.3`).

**Befund.** Die Wirkung bleibt aus. Am 2026-10-03, Stunden nach 3e61977, brachte je ein Edit
an `handoff/anliegen/83-…md` und `84-…md` 40,7 bzw. 31,4 KB `ide_diagnostics` in den Kontext,
157 Meldungen „Possible spelling mistake found“ allein beim ersten („zwischen“, „und“,
„Kriterium“). Das ist der Befund aus 24.

Vermutung, unerprobt: Das VS-Code-Fenster, an dem Claude Code hängt, hat einen anderen
Ordner als Arbeitsbereich (etwa `Dokumente/`); dann gilt
`Arbiter_Structure/.vscode/settings.json` nicht. Oder die Meldung kommt von einer anderen
Erweiterung; die Diagnosen nennen keine `source`.

**Kosten.** Je Markdown-Edit 30 bis 40 KB, rund 10.000 Token. Eine Rolle mit fünf
Anliegen-Edits verbraucht so fast die Hälfte bis zur Meldegrenze (120.000).

**Gegenvorschlag.**
1. Quelle klären: Welche Erweiterung meldet, welcher Ordner ist der Arbeitsbereich? Die
   Ausgabe des Hooks liegt unter `~/.claude/projects/…/tool-results/hook-…-additionalContext.txt`.
2. Ist es cSpell: eine `cspell.json` im Wurzelordner mit `"ignorePaths": ["**/*.md"]`; die
   liest cSpell für jede Datei darunter, gleich welcher Arbeitsbereich offen ist.
3. Scheiter-Test wie in 24 verlangt: Wirkung, nicht Text der Einstellung.

Erledigt, wenn ein Edit an einer Anliegen-Datei keine Rechtschreibmeldung mehr in den
Kontext bringt.

**Stellungnahme.**
