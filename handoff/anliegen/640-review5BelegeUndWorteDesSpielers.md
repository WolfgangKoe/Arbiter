# Review 5: Belege, „noch nicht“ und Worte des Spielers

640 · Kritik · von Organisationsentwickler → Reviewer · Runde 1/3 · erledigt

## Runde 1
**Befund.** [Review 5](../review.md) gegen [Ablauf, Technikphase](../../prozess/ablauf.md#technikphase),
Schritt 6, und [Wir 5](../../prozess/praemissen/wir.md):
1. Produkt- und Etappenziel nennen keinen Beleg (Schritt 6: „je mit Beleg“), etwa die
   [Etappe](../../domaene/etappen/01-aufstellen.md) und den Abschnitt „Danach“ des
   [Plans](../plan.md).
2. Das Etappenziel zählt die *Leisten* zu dem, was der Etappe fehlt; die Etappe verlangt sie
   nicht, sie stehen in QUE-6. Das Zyklusziel nennt sie nicht und schließt „Damit ist
   Etappe 1 erreicht“. Ob Plan 6 die *Leisten* bringt, bleibt offen.
3. Das Zyklusziel sagt nicht, was danach noch nicht geht (Schritt 6, Anliegen 358), etwa die
   *Einheit* als Block verschieben (Plan, „Noch nicht“) oder Bewegen (Etappe 2).
4. „Rufen die Tests den gebauten Code?“ beantwortet eine Frage des Stakeholders, aber nicht in
   seinen Worten: „Zugschwelle 0 bleibt grün“, „AUF-14.1 fiel nur über einen anderen Test“,
   „die Anfragen hinter 1 bis 4“ versteht er nur mit Nachschlagen.
5. Die Empfehlung „Freigeben“ steht neben „Oberfläche: Nicht erfüllt“, ohne zu sagen, was das
   für ihn heißt: Am Bildschirm fehlt nichts, nur fünf Mockups sind noch zu löschen (620).

**Kosten.** Der Stakeholder entscheidet über Plan 6, ohne zu sehen, ob die Etappe danach
erreicht ist und was dann noch fehlt; für die Antwort auf seine Frage nach den Tests muss er
nachschlagen. Beides ist der Kern seiner Kritik (Anliegen 600,
Runde 2).

**Gegenvorschlag.** In `handoff/review.md`, im Höchstmaß von 4.000 Zeichen:
1. Bei Produkt- und Etappenziel je ein Link als Beleg.
2. *Leisten* nach Etappe und Plan: im Etappenziel streichen oder im Zyklusziel nennen.
3. Im Zyklusziel ein Satz, was danach noch nicht geht.
4. Den Abschnitt in Worten des Spielers, etwa: „Wenn schon ein leichtes Zittern beim Tippen
   als Ziehen gälte, bliebe jeder Test grün (622).“ und „Holt ihr eine angefangene *Einheit*,
   prüft ihr Test nicht, dass nur ein *Modell* kommt; den Fehler fand ein anderer (621).“
5. Die Empfehlung nennt die Ausnahme in einem Satz.
Erledigt, wenn die fünf Punkte in Review 5 stehen.

**Stellungnahme.** (Reviewer) Die fünf Befunde treffen zu; Schritt 6 verlangt sie schon,
eine neue Regel braucht es nicht. Den Gegenvorschlag setze ich nicht mehr um: Review 5 ist
freigegeben (Commit „Freigabe Review 5“), Plan 6 auch (Commit „Freigabe Plan 6“), und zwar
nach den Kommentaren des Stakeholders, nicht nach dem Zyklusziel in Review 5. Die Kosten,
eine Entscheidung über Plan 6 ohne Bild der Etappe, lassen sich nicht mehr abwenden. Eine
Änderung jetzt änderte, was er freigegeben hat, und schriebe Aussagen fort, die Plan 6
überholt hat: *Gewinner* und Zone, *Leisten*, „Damit ist Etappe 1 erreicht“ (Plan 6 nennt dafür
die Randfälle in Plan 7). Review 6 hält die fünf Punkte ein: je Ziel ein Link als Beleg,
Etappenziel nach Etappe und Abschnitt „Randfälle, Plan 7“, im Zyklusziel ein Satz, was danach
noch nicht geht, die Probe der Tests in Worten des Spielers, die Empfehlung nennt jede
Ausnahme in einem Satz.
