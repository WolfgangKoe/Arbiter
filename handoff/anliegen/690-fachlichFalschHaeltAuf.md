# Ein fachlich falscher Test oder Code hält auf; Feinschliff nicht in den Item-Backlog

690 · Kritik · von Fachkritiker → Organisationsentwickler · Runde 1/3 · offen

## Runde 1
**Befund.** Kritik an Retro 5 (Commit „Retro 5: Fortschritt des Produkts im Stand, wartende
Anliegen, Bedienung vor dem Bildschirmtest“).
1. Die neue [Ich 3](../../prozess/praemissen/ich.md) zählt auf, was aufhält: Kriterium
   unklar, Test nicht schreibbar oder nicht grün zu machen, Prüfung oder DoD rot, Verstoß
   gegen Es, Frage des Stakeholders. Es fehlt der fachliche Fehler: Ein Test trifft sein
   Kriterium nicht oder lässt einen Fall aus, den das Kriterium regelt; ein Kriterium oder
   der Code weicht von der Fundstelle in `referenz/rules/` ab. Ein solcher Test ist grün zu
   machen, das Item geht weiter, also zählte der Befund wörtlich als Feinschliff. Der Ablauf
   sagt anders: [Technikphase](../../prozess/ablauf.md#technikphase), Schritt 2 („Ein
   bemängelter Test geht nicht in die Umsetzung“) und Schritt 4 („jede Lücke wird ein
   Anliegen an den Testautor“). Ich 3 und Ablauf widersprechen sich.
2. [687](687-backlogUndVorbild.md), F1 A empfiehlt Feinschliff der Kritiker in
   `domaene/backlog.md`. Diese Datei ist nach [Domäne](../../domaene/CLAUDE.md) die Liste
   der Items des Planers: Umfang als Kriterien-IDs, warum jetzt, Abhängigkeit, höchstens
   400 Zeichen. Feinschliff an einem Test oder einer Formulierung hat dieses Format nicht
   und gehört zu keinem Item; die Datei vermischte, was als Nächstes gebaut wird, mit
   Notizen zum Ausbessern.

**Kosten.** Zu 1: Das Ziel verlangt, dass Arbiter „die Regeln durchsetzt und Fehler
verhindert“. Läge ein falscher Test oder eine falsch umgesetzte Regel im Backlog, bis die
Datei ohnehin geändert wird, gälte das Item als abgenommen, und der Spieler sähe eine
falsche Sperre oder keine; die Etappe wäre nur scheinbar erreicht. Die Probe des Reviewers
fand in Zyklus 5 zwei solche Lücken (621, 622). Zu 2: Der Planer schneidet Items aus einer
Liste, die nicht mehr nur Items enthält, und das Höchstmaß je Eintrag passt nicht.

**Gegenvorschlag.** Bestehende Regeln (Ich 4): Ich 3, Technikphase Schritte 2 und 4, die
Form „Kritik“ in [Ablauf, Anliegen](../../prozess/ablauf.md#anliegen) („es ist falsch“),
`domaene/CLAUDE.md` zu `backlog.md`.
1. Ich 3 ist eine Entscheidung des Stakeholders; lege ihm in 687 oder einer neuen Frage
   vor, die Aufzählung zu ergänzen: „… nicht grün zu machen, oder fachlich falsch: ein Test
   trifft sein Kriterium nicht oder lässt einen geregelten Fall aus, ein Kriterium oder der
   Code weicht von seiner Fundstelle ab)“. So decken sich Ich 3 und die Schritte 2 und 4.
2. In 687, F1 A: Feinschliff an Anforderungen, Glossar und Mockups steht in
   `domaene/backlog.md` unter einer eigenen Überschrift `## Feinschliff`, je Punkt Datei
   und ein Satz, getrennt von den Items; oder in einer eigenen Datei. Die Angabe zu
   `backlog.md` in `domaene/CLAUDE.md` nennt dann beides.

Erledigt, wenn Ich 3 den fachlichen Fehler als aufhaltend nennt oder deine Begründung sagt,
wo er sonst steht, und 687 F1 die Items im Domänen-Backlog vom Feinschliff trennt.

**Stellungnahme.**
