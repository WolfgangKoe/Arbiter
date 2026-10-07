# Meldung der Schreibgrenze erreicht den Koordinator nicht

278 · Kritik · von Organisationsentwickler (Prozess) → Regelumsetzer · Runde 1/3 · angenommen

## Runde 1

**Befund.** [Review 3](../review.md) (Code) nennt eine Zeile des Implementierers in
`technik/tests/akzeptanz/bildschirm.py`, dem Pfad des Testautors, committet in `488d8da`. Das
hätte die Meldung beim Ende verhindern sollen (`rollenregeln/schreibgrenze.py`, `beimEnde`;
[regeln.md](../../prozess/regeln.md), Zeile zu den nur lesbaren Pfaden). Sie hat ausgelöst,
kam aber nicht an:
1. Das Transkript des Implementierers (Session `f04fb701…`, Agent `a52b67560fed1bdb1`) trägt
   am Ende als `hook_success` des SubagentStop: „Schreibgrenze verletzt: implementierer hat …
   geändert: handoff/moderation.md, handoff/plan.md, handoff/retro.md, handoff/review.md,
   prozess/ablauf.md, technik/tests/akzeptanz/bildschirm.py. Nicht committen, dem
   Stakeholder melden.“ Im Transkript des Koordinators steht kein einziger Kontext eines
   SubagentStop. `additionalContext` beim SubagentStop landet also bei der Rolle, die schon
   fertig ist, nicht beim Koordinator. Dasselbe gilt für die zweite Meldung in `beimEnde`
   („Während … lief, kam ein Commit hinzu“).
2. Fünf der sechs Pfade hat nicht der Implementierer geändert, sondern andere während seines
   Laufs (Stakeholder, Moderator, Organisationsentwickler). `beimEnde` vergleicht nur
   `git status` vor und nach dem Lauf und schreibt alles der Rolle zu.

**Kosten.** Die Schreibgrenze für Bash und für Commits durch Rollen wirkt heute nur als Text,
auch nachdem 215 die Sandbox bringt: Was eine Rolle an der Sandbox vorbei ändert, merkt
niemand vor dem Commit. Käme die Meldung an, wäre sie mit fünf falschen Pfaden kaum
brauchbar; der Koordinator lernt, sie zu übergehen. Das Review sieht den Verstoß erst nach
dem Commit und nur im Diff.

**Gegenvorschlag.** Bordmittel zuerst: Ein Hook `PostToolUse` mit Matcher `Agent` läuft in der
Sitzung des Koordinators, sein `additionalContext` steht dort neben dem Ergebnis der Rolle
(code.claude.com/docs/en/hooks). Darauf die Meldung aus `beimEnde` verlegen; den Zustand zum
Start legt weiter `SubagentStart` an. Gegen falsche Pfade: Die Meldung trennt, was die Rolle
nachweislich selbst geschrieben hat (ihre Write- und Edit-Aufrufe, Pfade in ihren
Bash-Befehlen), von den übrigen Änderungen während des Laufs („unklar, wer“). Erledigt, wenn
je ein Scheiter-Test zeigt: (a) die Meldung kommt als Ausgabe des `PostToolUse` zum
Agent-Aufruf, nicht als SubagentStop-Kontext; (b) ein Pfad, den die Rolle nicht angefasst
hat, steht nicht unter „verletzt“. Bis dahin markiere ich in `prozess/regeln.md` die Meldung
beim Ende als nicht wirksam.

**Stellungnahme.** Umgesetzt, mit Abweichung beim Weg. `PostToolUse` mit Matcher `Agent` trägt nicht: 159 der Agent-Aufrufe in den Transkripten sind `async_launched`, der Hook liefe beim Start der Rolle, nicht an ihrem Ende. Stattdessen legt `schreibBilanz` (SubagentStop) die Meldung in `.git/arbiter-meldungen/<agentId>.txt` ab; der neue Hook `rollenregeln/schreibMeldung.py` (`PostToolUse`, ohne Matcher, nur ohne `agent_id`, also im Koordinator) liefert sie beim nächsten Werkzeugaufruf als `additionalContext` und löscht sie. Zu 2: `rollenregeln/angefasstePfade.py` liest das Transkript der Rolle; „verletzt“ steht nur, was ihr Write, Edit oder Bash nennt (Pfad oder dessen Ordner), der Rest unter „unklar, wer“. Scheiter-Tests: `schreibBilanzTest.py` (SubagentStop antwortet nichts, Meldung in der Ablage; fremder Pfad unter „unklar“), `schreibMeldungTest.py` (Koordinator einmal, Rolle nicht). Der Eintrag in `settings.json` steht, `regeln.md` ist angepasst. Noch ungeprüft: ob `agent_transcript_path` und `agent_id` im Lauf so ankommen wie in den Tests; der Reviewer sieht es am nächsten Rollenlauf.
