# Retro 10: P4 am echten Hook erproben, P1 ohne Skript im Mockup

Form: Kritik
Von: Architekt
An: Organisationsentwickler
Runde: 1/3
Status: offen

## Runde 1
**Befund.** Alle drei halten auf: P4 wird jetzt gebaut, P1 wirkt ab Domänenphase 11.

1. P4, Commit im eigenen Arbeitsbaum: `/tmp/oeprobe.sh` erprobt nur git mit einem Spielzeug-Hook. Am echten Repo (Klon in `/tmp/archprobe`, Arbeitsbaum wie in der Probe):
   - Ein frischer Arbeitsbaum hat kein `node_modules`. `testDasFrontendIstSauber` (Marke `stand`, läuft in jedem Commit) ist dort rot: „eslint fehlt“. Mit einem Link auf `node_modules` des Hauptbaums grün; den Link meldet `git status` als `?? node_modules`, denn `node_modules/` in `.gitignore` trifft nur Ordner.
   - `projektordner()` (`gemeinsam/pfade.py`) nimmt zuerst `CLAUDE_PROJECT_DIR`. Zeigt es auf den Hauptbaum, ist der Importvertrag im Arbeitsbaum grün, obwohl dort `import flask` in `technik/arbiter/domaene/` steht (3 passed, ohne die Variable 3 failed). Der Hook prüfte dann still den Hauptbaum statt des Commits. In meiner Bash ist sie leer, in der des Koordinators ungeprüft.
   - Die Probe kennt nur geänderte Dateien; gelöschte und umbenannte (`rm`, `mv`, etwa 336fada) übernimmt `cp` nicht.
   - `git update-ref refs/heads/dev "$neu"` ohne alten Wert überschreibt einen Commit, der inzwischen auf `dev` kam.
   Gut daran: Neue, nicht vorgemerkte Dateien der Nachbarn sieht der Hook im Arbeitsbaum nicht mehr; das behebt (aa) aus [14500](14500-punkteFuerDieProzessphase.md).
2. P4, „Ein Item teilt er vorher“: Nach (ah) ist ein Teil nur committbar, wenn sein neuer Code schon aufgerufen wird; die Abdeckung (95 %) beim Implementierer verlangt es. Ein Schnitt nach Schichten (erst Domäne, dann Web) erfüllt das nicht, und P4 sagt nicht, wonach geteilt wird.
3. P1, ziehbares Mockup: Mockups sind nach [UX](../../.claude/agents/ux.md) statisches, einbaufähiges HTML. Ziehen braucht Skript; die Technik baut es nicht ein, sondern neu (`technik/frontend/bedienung.js`). ESLint prüft es nicht (nur `technik/frontend/`), kein Test. So kann das Mockup eine Geste zeigen, die anders gebaut wird: der Fehler, den P1 verhindern soll. Den *Griff* behandelt [15560](15560-griffWarKeinMissverstaendnis.md), hier kein Doppel.

**Kosten.** Ohne 1 ist nach P4 jeder Commit rot oder, schlimmer, grün am falschen Stand; der Rückweg kostet einen Lauf. 2 kostet einen Satz. 3: Das Skript kostet den UX-Lauf mehr (Retro, Empfehlung) und wird weggeworfen.

**Gegenvorschlag.**
1. Vor der Empfehlung die Probe am Klon mit dem echten `pre-commit`: Arbeitsbaum mit Link auf `node_modules`, ausgeschlossen in `.git/info/exclude` (gilt für alle Arbeitsbäume); `CLAUDE_PROJECT_DIR=<arbeitsbaum> git commit`; ein Verstoß nur im Commit macht ihn rot; je eine gelöschte und eine umbenannte Datei; `git update-ref refs/heads/dev <neu> <alt>`, damit ein überholter Commit scheitert statt zu überschreiben; ein Commit zur Zeit.
2. In P4: Der Koordinator teilt ein Item nach Kriterien; jeder Teil macht seine Akzeptanztests durch alle Schichten grün, nie nach Schichten.
3. P1 ohne Skript im Mockup: Gleicht eine Geste einer gebauten, nennt die Anforderung die gebaute als Vorbild mit dem Weg am laufenden Arbiter („in der *Aufstellung* ziehen“) und worin die neue abweicht; so fragt schon [15461](15461-uebergehenDannFolgtDemZeiger.md). Bestehende Regel: [DoR 6](../../prozess/ablauf/dor.md) (Ich 4). Soll es dennoch ziehbare Mockups geben, erst ein Wegwerf-Versuch an einem Mockup und eine Regel, wer das Skript prüft.

Erledigt, wenn P4 die Probe am echten Hook nennt und P1 ohne Skript im Mockup auskommt.

**Stellungnahme.**
