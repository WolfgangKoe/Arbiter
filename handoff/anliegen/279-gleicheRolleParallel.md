# Läufe derselben Rolle gleichzeitig, wenn ihre Dateien getrennt sind

279 · Kritik · von Reviewer (Technik) → Organisationsentwickler (Prozess) · Runde 1/3 · erledigt

## Runde 1
**Befund.** Der Stakeholder schreibt in [Review 3](../review.md): Anliegen an dieselbe Rolle laufen parallel, solange keines vom anderen abhängt. Der [Ablauf](../../prozess/ablauf.md#domänenphase) verbietet das: „Gleichzeitig laufen nur Rollen, die ausschließlich Anliegen schreiben; Ausnahme: Technikphase, Schritt 3.“ Für die Aufträge an den Regelumsetzer aus der [Moderation](../moderation.md) habe ich die Dateien aus Befund und Gegenvorschlag und den `git status` geprüft:
1. Unabhängig, ohne Hook-Code: 240 (eine Zelle in `regeln.md`), 262 (neues Modul in `formregeln/`), 265 (`importvertrag.py`), 267 (`abdeckung.py`), 268 (`eslint.config.mjs`, `frontendTest.py`), 270 (`sonarlint.py`). Kein Hook importiert `formregeln` oder `frontendregeln`.
2. Überschneidung: 253 P1 läuft gerade, 23 Pfade in allen Ordnern samt `settings.json`. P2 teilt `anliegen`, `bashPositivliste`, `statusrecht`, `schreibgrenze`, `dashboard`. Dieselben Dateien ändern 272, 273, 274, 278 und 275+246. P5 ändert `anliegen`, `statusrecht`, `dashboard`, `laufLog`. P7 ändert die zehn Tests mit eigenem git-Repo und `hoechstmassTest` (276). Weitere Paare: 272 und 273 (`bashPositivliste`), 272 und 278 (`schreibgrenze`), 276 mit 268 (`frontendTest.py`), mit 270 (`sonarlint.py`) und mit P7. Abhängig sind 275, das Formen und `wartet auf` aus 274 liest, und 246, dessen Kopf 274 umstellt.
3. Dateien getrennt, aber Hook-Code: 273 (`bashPositivliste`, `phasenfolge`), 274 (`anliegen`, `statusrecht`), 278 (`schreibgrenze`, `settings.json`). Diese Module laufen aus demselben Arbeitsbaum als Hooks jedes gleichzeitigen Laufs. Ein halber Stand sperrt die anderen Läufe oder lässt sie durch.
4. Nebenbefund: `eslint.config.mjs` (268) sowie `package.json` und `.stylelintrc.json` (276) stehen nicht in den Schreibpfaden des Regelumsetzers, `schreibgrenze.py` sperrt sie.

**Kosten.** Nacheinander sind es 16 Läufe, gleichzeitig nach Punkt 1 werden es 10 Schritte. Auch dann bleiben Kosten: Ein Lauf meldet erst fertig, wenn `pytest prozess/pruefungen` grün ist; ein roter Scheiter-Test des Nachbarn hält ihn auf. Der Koordinator committet nach Pfaden; die Zeile des Nachbarn in `regeln.md` geht dann mit. `beimEnde` meldet den Commit des Nachbarn (278).

**Gegenvorschlag.** Die bestehende Ausnahme (Technikphase, Schritt 3: gleichzeitig, Commit je Lauf nach Pfaden) erweitern: „Läufe derselben Rolle zu verschiedenen Anliegen laufen gleichzeitig, wenn ihre Dateien getrennt sind, keines auf das andere wartet und höchstens einer Hook-Code ändert (Module, die `.claude/settings.json` startet, und deren Importe).“ Die Moderation nennt je Rolle die Stränge. Hier:
- Nach dem Commit von 253 P1 gleichzeitig: 240, 262, 265, 267, 268, 270, dazu die Kette.
- Kette: 253 P2 → P5 → P7 → 272 → 278 → 273 → 274 → 276 (nach 268 und 270) → 275+246.
- Hätte jeder Lauf eine eigene Arbeitskopie (git worktree), fiele die Grenze beim Hook-Code weg; dann liefen 273, 274 und 278 gleichzeitig. Ob Claude Code das für Subagenten mitbringt, klärt claude-code-guide.
- Zu 4: Schreibpfade ergänzen, oder 268 und 276 gehen an die Rolle, die den Pfad hat.

Erledigt, wenn der Ablauf die Ausnahme nennt und die Moderation die Stränge zeigt.

**Stellungnahme.** Umgesetzt in [Ablauf, Gleichzeitige Läufe](../../prozess/ablauf.md#gleichzeitige-läufe), Moderator und Regelumsetzer verweisen darauf; die Stränge schreibt der Moderator. Erledigt erst nach F1 und F2.

**F1 · Worktree je Lauf jetzt statt im [Backlog](../../prozess/backlog.md)?** A ja, B nein (Empfehlung: kostet mehr als zwei gesparte Schritte).
Antwort: Nein.

**F2 · Regelumsetzer schreibt `eslint.config.mjs`, `.stylelintrc.json`, `package.json`, `package-lock.json`?** A ja (Empfehlung, [Ablauf](../../prozess/ablauf.md#kritik-am-code): Linter-Konfiguration), B nein.
Antwort: ja.
