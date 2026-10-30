# Review 9: Rundgang, Commits, Mutation und Nächstes Vorgehen

Form: Kritik
Von: Organisationsentwickler
An: Reviewer
Runde: 2/3
Status: erledigt

## Runde 1
**Befund.** Kritik am [Review 9](../review.md), Stand 9cb9142 („Review 9 bis auf Mutation
fertig, 8880 gekürzt und beantwortet“), nach [Technikphase](../../prozess/ablauf/technikphase.md) 6
und [Wir 5](../../prozess/praemissen/wir.md). Das Nächste Vorgehen nach 8880 steht schon in
[8950](8950-review9ZykluszielNachAntwort8880.md). Alle vier halten auf: Das Review liest der
Stakeholder einmal zur Freigabe; was erst in Technikphase 10 nachkäme, erreicht ihn für
Zyklus 9 nie, der nächste Rundgang beginnt nach diesem Review.
1. Rundgang unvollständig. `git diff --stat fa882ab 9cb9142` („Freigabe Review 8“) zeigt
   Prüfcode und Prüfkonfiguration, die der Rundgang nicht nennt:
   - [eslint.config.mjs](../../eslint.config.mjs), Zeile 32: neue Regel `no-inline-comments`
     (Commit „P1: Testautor auf Opus, …“).
   - [gleichwertig.json](../../prozess/pruefungen/mutationsregeln/gleichwertig.json): elf neue
     Begründungen, nach denen ein überlebender Mutant nicht zählt, sieben davon in
     `ausgangslage.py` und `spielobjekte.py` (Commit „Voller Mutationslauf 8 ausgewertet …“).
     Sie zählen nicht gegen die Schwelle; gerade die soll er sehen.
   - [hookProtokoll.py](../../prozess/pruefungen/gemeinsam/hookProtokoll.py), Zeile 56: eine
     leere Eingabe gilt als Eingabe ohne Angaben, statt abzubrechen (Commit „Schreibgrenze:
     Bash-Schreiben und Hook-Protokoll nachgeschärft“).
2. Commits ohne Betreff (Wir 5): „auf ca2bda8“ und zweimal „1cafd47“ im Abschnitt DoD.
3. Produktziel ohne Beleg (Technikphase 6, „je mit Beleg“): „Etappe 1 von 10 ist erreicht“
   nennt weder Link noch Commit.
4. Mutation offen: Die Empfehlung ist bedingt, die DoD unvollständig. Der Text sagt nicht,
   warum die Schwelle auf den vollen Lauf wartet, obwohl der nach der
   [DoD](../../prozess/ablauf/dod.md) „nichts aufhält“: Der gezielte Lauf will dessen
   Ergebnisse aus dem Merkzettel holen und die Messung zu 8122 nicht stören.

**Kosten.** Ohne Nachbessern gibt er frei, ohne die elf Ausnahmen vom Mutationszählen und
die neue Lint-Regel zu kennen, und weiß nicht, worauf er bei der Mutation wartet.
Nachbessern: etwa acht Zeilen im Review, keine Tests.

**Gegenvorschlag.** 1: drei Punkte unter „Neu oder geändert“, je mit Fundstelle, die elf
Begründungen in einem Satz mit ihren Modulen. 2: Betreff in Anführungszeichen statt Kennung.
3: Beleg wie beim Etappenziel, etwa der Commit „Freigabe Etappe 1“. 4: ein Satz zum Warten
mit Link auf [8961](8961-vollerMutationslaufJeEtappe.md); die Zahl trägst du nach, sobald der
Lauf fertig ist.

**Stellungnahme.** Umgesetzt im [Review](../review.md): 1 drei Punkte unter „Neu oder
geändert“; dazu Problem 8: Ein gleichwertiger Eintrag gilt für jede Zeile mit gleichem
Text, auch eine neue Klasse. 2 Betreffe statt Kennungen. 3 Commit „Freigabe Etappe 1“. 4 ein
Satz zum Warten mit Anliegen 8961.

## Runde 2
**Befund.** Nachgeprüft am [Review](../review.md), Stand db366fd: 2, 3 und 4 sind erledigt,
1 bis auf eine Zahl. Unter „Neu oder geändert“ steht „Sieben davon nehmen `frozen` oder
`eq=False` aus `@dataclass` […]; die übrigen vier“. In
[gleichwertig.json](../../prozess/pruefungen/mutationsregeln/gleichwertig.json) sind es sechs
(je drei in `spielobjekte.py` und `ausgangslage.py`) und fünf übrige: `zweite = 2`, zwei in
`setzenPerKlick.py`, je einer in `web/darstellung.py` und `web/server.py`. Hält auf: Gerade
diese Ausnahmen soll der Stakeholder zur Freigabe richtig sehen.

**Kosten.** Zwei Wörter im Review; du fasst es ohnehin noch einmal an, wenn du die Zahl der
Mutation nachträgst.

**Gegenvorschlag.** „Sechs davon …; die übrigen fünf“, im selben Zug wie die Zahl der
Mutation.

**Stellungnahme.** Umgesetzt: „Sechs davon, je drei in `spielobjekte.py` und
`ausgangslage.py`, …; die übrigen fünf“. Gleich jetzt statt mit der Zahl der Mutation.
