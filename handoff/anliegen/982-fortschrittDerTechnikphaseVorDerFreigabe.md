# Fortschritt der Technikphase vor der Freigabe des Plans

982 · Kritik · von Organisationsentwickler → Regelumsetzer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Einordnung nach Ich 3: hält auf. Der Stakeholder gibt Plan 6 erst frei, wenn
darin `## Fortschritt` der Technikphase steht, im Format wie in [Review](../review.md)
(Abschnitt Fortschritt): „Das verstehe ich unter Plan! Das soll da stehen, bevor ich etwas
freigebe!“ und „Und das bitte für jedes Item, damit ich den Fortschritt zu jedem Item sehen
kann.“ `standregeln/fortschritt.py` (`fortschrittSchreiben`) schreibt nur die laufende und
die vorige Phase; die Technikzeilen entstehen erst nach `Freigabe Plan <n>`. Dieselbe Lücke
hat das Review: Die Zeilen der folgenden Domänenphase fehlen, wenn er es freigibt.

**Kosten.** Der Stakeholder gibt frei, ohne zu sehen, wer danach was je Item tut; der Planer
schrieb den Ablauf deshalb als Prosa in den Plan, doppelt zur Liste (Wir 3, Anliegen 983).

**Gegenvorschlag.** Bestehende Regel ([Ablauf, Fortschritt](../../prozess/ablauf.md#fortschritt),
Tabelle) bleibt; das Skript schreibt den Abschnitt früher:
1. Zusätzlich zur laufenden und vorigen Phase die nächste, sobald ihre Datei zum Zyklus
   gehört: in der Domänenphase n die Technikzeilen in `plan.md` mit `# Plan · Zyklus n`; in
   der Technikphase n die Domänenzeilen von Zyklus n+1 (`Freigabe Plan n+1`) in `review.md`
   mit `# Review · Zyklus n`. Die Retro entsteht schon in ihrer Phase.
2. Bis die Phase beginnt, sind alle Zeilen offen: Fakten haken nicht ab, Haken aus einem
   älteren Abschnitt (etwa dem des Vorzyklus im neu geschriebenen Review) werden nicht
   übernommen.
3. Je Item vor „Tests zu Item <k>“ die Zeile `Architekt: Vertrag zu Item <k>, bei beiden
   Hälften`, abgehakt per Befehl (Ablauf, Technikphase 1; im Plan 6 nennt der Planer diesen
   Schritt, in der Tabelle fehlt er).
4. Je Item eigene Zeilen gibt es schon; sie stehen in der Reihenfolge der Items im Plan.

Erledigt, wenn je Punkt ein Scheiter-Test in `standregeln/fortschrittTest.py` steht (Plan
ohne Freigabe hat Technikzeilen, alle offen, auch wenn ein Kriterium schon einen Test hat;
Review n hat die Domänenzeilen von n+1 offen, auch wenn der alte Abschnitt Haken trug;
Vertragszeile je Item) und `handoff/plan.md` den Abschnitt nach dem nächsten Lauf trägt.

Die Zeile in `prozess/regeln.md` und den Text im Ablauf (früher Stand, Vertragszeile in der
Tabelle) sperrt die Schreibgrenze bis `Freigabe Retro 6`
(`rollenregeln/regelnNurInProzessphase.py`); nenne die Zeile in deiner Stellungnahme, ich
trage beides dann ein ([Backlog](../../prozess/backlog.md)). Skript und Test in
`prozess/pruefungen/` sind frei.

Bordmittel geprüft: keine Änderung zu [490](490-fortschrittInPlanReviewRetro.md); dieselben
Hooks.

**Stellungnahme.** Umgesetzt in `standregeln/fortschritt.py`: Das Skript schreibt nun auch
den Abschnitt der nächsten Phase (Plan in der Domänenphase, Review mit den Domänenzeilen des
Folgezyklus in der Technikphase und Prozessphase), alle Zeilen offen, ohne Fakten und ohne
übernommene Haken. Die Vertragszeile `Architekt: Vertrag zu Item <k>, bei beiden Hälften`
steht je Item vor den Tests. Scheiter-Tests in `standregeln/fortschrittTest.py`: Plan vor
der Freigabe mit offenen Technikzeilen (trotz vorhandenem Test), Review mit offenen
Folgezeilen (trotz alter Haken), Vertragszeile; der Test für Zyklus 1 gilt nun für das
Review. `handoff/plan.md` trägt den Abschnitt mit Vertragszeilen. Prüfungen und SonarLint grün.

Für dich zum Eintragen (Schreibgrenze bis `Freigabe Retro 6`):
- `prozess/regeln.md`, Zeile Fortschritt: Mechanismus `standregeln/fortschritt.py` schreibt
  Plan und Review schon vor der Freigabe, Scheiter-Test `standregeln/fortschrittTest.py`
  (`testDerPlanTrägtVorDerFreigabeDieTechnikzeilenAlleOffen`,
  `testDasReviewTrägtVorDerFreigabeDieDomänenzeilenDesFolgezyklusOffen`,
  `testJedesItemHatVorDenTestsDieVertragszeileDesArchitekten`).
- `prozess/ablauf.md`, Fortschritt: Der Abschnitt entsteht vor Beginn der Phase, alle Zeilen
  offen; die Tabelle hat je Item die Zeile `Architekt: Vertrag zu Item <k>, bei beiden
  Hälften | Befehl` vor „Tests zu Item <k>“.
