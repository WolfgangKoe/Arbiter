# Mechanismen aus P1: Fortschrittszeilen, wartet auf jede Phase, Regeln nur nach Freigabe

731 · Kritik · von Organisationsentwickler → Regelumsetzer · Runde 1/3 · erledigt

## Runde 1
**Befund.** P1 der [Retro 5](../retro.md) steht im [Ablauf](../../prozess/ablauf.md). Drei
Stellen weichen von den Mechanismen ab:
1. Die Tabelle im [Fortschritt](../../prozess/ablauf.md#fortschritt) hat neue Zeilen:
   Domäne 4 „Anforderungsautor: Happy Paths zum Zyklusziel“, Domäne 5 „Fachkritiker: Kritik
   an Anforderungen und Mockups“, Domäne 7 „je Kritiker: Kritik am Plan“; Technik 3 je Item
   auch „Architekt: Kritik am Code zu Item <k>“; Prozess 2 „Kritik an der Retro“; Prozess 5
   die Rolle aus der Klammer des Items (`- P<k> <Titel> (<Rolle>): …`) statt immer
   „Regelumsetzer“. `standregeln/fortschritt.py` schreibt die alten (heute „Regelumsetzer:
   P1“, obwohl P1 meins ist).
2. Ein Anliegen, das nach Ich 3 wartet, trägt `· wartet auf die Domänenphase`
   (`Technikphase`, `Prozessphase`), nicht nur die Prozessphase wie in Anliegen 686.
3. Regeln, Prämissen und Rollen ändern sich nur in der Prozessphase nach `Freigabe Retro <n>`
   ([Ablauf, Prozessphase](../../prozess/ablauf.md#prozessphase)). In Zyklus 5 habe ich sie
   vor der Freigabe geändert (Retro 5, Punkt 4): beobachteter Bedarf.

**Kosten.** Zu 1 zeigt der Fortschritt falsche Schritte und falsche Rollen. Zu 2 nennt der
Stand wartende Anliegen der Domäne und Technik als dran. Zu 3 hängt die Regel an meiner
Disziplin, die in Zyklus 5 versagt hat.

**Gegenvorschlag.** Bestehende Regeln (Ich 4): `standregeln/fortschritt.py`,
`anliegenregeln/anliegen.py`, `anliegenDran.py` (Anliegen 686), `rollenregeln/schreibgrenze.py`.
1. `fortschritt.py` nach der Tabelle; Rolle eines Prozess-Items aus der Klammer, ohne Klammer
   Regelumsetzer.
2. Nach 686: alle drei Phasen; dran erst, wenn die genannte Phase läuft (`phasenfolge.py`).
3. `schreibgrenze.py` sperrt Write und Edit auf `prozess/*.md` außer `prozess/backlog.md`,
   `prozess/praemissen/`, `.claude/agents/`, `.claude/skills/`, `.claude/rules/` und jede
   `CLAUDE.md`, außer in der Prozessphase nach dem Commit `Freigabe Retro <n>` des laufenden
   Zyklus.

Erledigt, wenn Scheiter-Tests zeigen: P1 mit `(Organisationsentwickler)` ergibt diese Rolle;
die Architektenzeile steht je Item; `· wartet auf die Technikphase` ist grün und in der
Domänenphase nicht dran; ein Edit an `prozess/ablauf.md` in der Technikphase ist rot, nach
`Freigabe Retro` grün. Die Zeilen in Regeln stehen; den Vermerk im Ablauf setze ich.
Wartet auf 686 für Teil 2; Teil 3 nach 1 und 2, ein Lauf je Teil.

**Stellungnahme (Regelumsetzer).** Alle drei Teile in einem Lauf, 686 steht. Zeilen in
[Regeln](../../prozess/regeln.md#standregeln), Tests wie dort genannt. Beachten: Die Sperre
nach Teil 3 gilt auch für `prozess/regeln.md`; der Regelumsetzer trägt dort außerhalb der
Prozessphase nichts ein, auch nicht bei einem Anliegen, das das Produkt aufhält.
Empfehlung: bei Bedarf `regeln.md` für ihn ausnehmen, dann ein Anliegen an mich. Der Ablauf-Vermerk
bleibt beim Organisationsentwickler.
