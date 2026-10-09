# Commits mit Betreff statt Kennung nennen

354 · Kritik · von Reviewer (Technik) → Organisationsentwickler (Prozess) · Runde 1/3 · offen

## Runde 1
**Befund.** Der Stakeholder schreibt in [351](351-reviewVierFormDerSchritteVierUndSechs.md):
„Die committ-Ids wie "38aae1f" finde ich sehr problematisch. Denn ich kann die nicht auf den
ersten Blick verstehen. […] Datum oder Nummer ist keine Alternative. Es muss irgendwie zum
Ausdruck bringen, woraum es da geht.“ Plan, Review, Retro und Anliegen nennen Commits bisher
oft per Kennung; keine Regel sagt, wie.

**Kosten.** Der Stakeholder versteht Verweise in `handoff/` nicht, ohne `git show` zu
tippen; Kommentar und Freigabe stützen sich dann auf Ungelesenes. Eine Zeile im Ablauf,
Review 4 hält sie schon.

**Gegenvorschlag.** Bestehende Regel: Der Ablauf nennt Commits schon per Betreff
(`Freigabe Plan <n>`, `Freigabe Review <n>`, Technikphase und Freigabe und Kommentare).
Erledigt, wenn [Ablauf, Freigabe und Kommentare](../../prozess/ablauf.md#freigabe-und-kommentare)
oder [Anliegen](../../prozess/ablauf.md#anliegen) sagt: „Ein Commit heißt in `handoff/` mit
seinem Betreff in Anführung (Commit „Freigabe Plan 4“), nicht mit der Kennung; `git log
--grep` findet ihn.“ Folge für alle Rollen: Betreffe, die für sich verständlich sind.

**Stellungnahme.**
