# Anforderungen zu den Items von Plan 8

Form: Kritik
Von: Planer
An: Anforderungsautor
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Das Zyklusziel aus [Review 7](../review.md) verlangt Phasen und Normal Move;
dazu gibt es noch keine Anforderung. Die Items
[phasenUndSchlachtrunden](../../domaene/items/phasenUndSchlachtrunden.md) und
[normalMove](../../domaene/items/normalMove.md) nennen darum kein Kriterium. Nach
Anliegen 3661 (A) nennt zudem jede Anforderung einer
noch offenen Etappe ihre Etappe.

**Kosten.** Hält auf: Ohne Kriterien ist Plan 8 nicht zur Freigabe bereit
([Domänenphase](../../prozess/ablauf/domaenenphase.md), Schritt 6).

**Gegenvorschlag.**
1. Die Happy Paths nach deinem Teil B aus Anliegen 2365, Punkte 4 und 5 ganz, aus 6 nur der
   Normal Move einer *Einheit* mit den *Sperren* über M, über eine fremde *Base* und am Ende
   ohne *Kohärenz*. Advance, Zurücksetzen, die Kante, Engagement Range, 7 und 8 kommen
   später.
2. Die Zeile `Etappe: 2` in den neuen Anforderungen. In den bestehenden nach den Items:
   Etappe 2: QUE-5, QUE-6, QUE-7, AUF-28.1, AUF-16.7, AUF-16.8, AUF-8.7, AUF-12.8;
   Etappe 3: AUF-29, AUF-28.2; Etappe 7: AUF-18.7, AUF-27, AUF-22, AUF-20.6, AUF-3.9,
   AUF-8.8; Etappe 8: AUF-11. Steht in einer Anforderung nur ein Teil, endet das Kriterium
   mit `(Etappe <n>)`. Was zur erreichten Etappe 1 gehört, bleibt ohne Angabe.

Nebenbei, wartet auf Etappe 7: [sperrenBeimSetzen](../../domaene/anforderungen/phasen/aufstellen/sperrenBeimSetzen.md)
liegt mit 1.295 Zeichen über 1.200, mit `(Etappe 7)` an AUF-3.9 noch mehr.

**Stellungnahme.** Angenommen.
1. Item phasenUndSchlachtrunden: [QUE-9](../../domaene/anforderungen/querschnitt/ersterZug.md)
   (erster Zug), [QUE-10](../../domaene/anforderungen/querschnitt/schlachtrunden.md) (Anzeige,
   Phase beenden, Zugwechsel, Ende nach Schlachtrunde 5, leere Phasen). Item normalMove:
   [BEW-1](../../domaene/anforderungen/phasen/bewegung/normalMove.md) (ziehen, beenden,
   ‚keine Kohärenz‘), [BEW-2](../../domaene/anforderungen/phasen/bewegung/sperrenBeimZiehen.md)
   (‚weiter als M‘, ‚über eine Base‘). *M* je *Einheit* in
   [ausgangslage.yaml](../../domaene/daten/ausgangslage.yaml), Glossar nachgeführt. Nicht
   aufgenommen, wartet: ‚schon bewegt‘ (`core_rules.txt:734`), andere *Einheit* während einer
   *Einheit in Bewegung*, „Phase beenden“ mit *Einheit in Bewegung*. Neue Begriffe, Kürzel BEW,
   Messung des Wegs und Knöpfe: Annahmen in [4280](4280-begriffeUndAnnahmenZuPlan8.md).
2. `Etappe: 2` in den vier neuen; nach deiner Liste `Etappe: 2` in QUE-5, 6, 7, AUF-16, 28,
   `Etappe: 3` in AUF-29, `Etappe: 7` in AUF-22, 27, `Etappe: 8` in AUF-11; am Kriterium
   `(Etappe 2)` AUF-8.7, 12.8, `(Etappe 3)` AUF-28.2, `(Etappe 7)` AUF-3.9, 8.8, 18.7, 20.6.
   Die Zeile steht über `Zweck:`.
