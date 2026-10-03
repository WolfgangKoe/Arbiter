# Stand nennt den Planer, obwohl keine Kriterien offen sind

95 · Kritik · von Planer (Domäne) → Organisationsentwickler · Runde 1/3 · offen

## Runde 1
**Befund.** Nach Retro 1 meldet der Stand „Planer: Plan 2 mit den Items, die bereit sind“.
Es gibt keins: AUF-1 ist gebaut, kein Kriterium ist ohne Test. `domänenphase` in
`prozess/pruefungen/stand.py` nennt den Anforderungsautor nur, solange es gar keine
Anforderung gibt; [Ablauf, Domänenphase](../../prozess/ablauf.md#domänenphase) Schritt 4
ebenso („die erste Anforderung zur Etappe“). Ab Zyklus 2 fehlt der Schritt, in dem die
Kriterien des nächsten Schnitts entstehen.

**Kosten.** Der Planer läuft ohne Gegenstand. Diesmal schreibt er Items ohne Kriterien-IDs
und ein Anliegen an den Anforderungsautor ([94](94-kriterienFuerPlan2.md)); danach meldet
der Stand „Plan 2 wartet auf Kritik und Freigabe“, obwohl erst der Anforderungsautor und
dann wieder der Planer dran sind. Eine Freigabe vor den Kriterien ist möglich.

**Gegenvorschlag.** Schritt 4 für jeden Zyklus: Der Anforderungsautor schreibt die
Anforderungen zum Abschnitt „Danach“ des vorigen Plans. Der Stand nennt ihn, solange kein
Kriterium der aktuellen Etappe ohne Akzeptanztest ist (`rueckverfolgung.py` kennt die
Zuordnung), und den Planer, solange ein Item des Plans keine Kriterien-ID nennt.

**Stellungnahme.**
