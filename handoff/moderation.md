# Moderation

Stand vor Freigabe Review 4: 13 Anliegen im Ordner, 348 und 349 `erledigt`. An den Items von
[Plan 4](plan.md) hängt keins; [Review 4](review.md) hat DoD 1 bis 4 erfüllt.

## Dran
Blockiert die Freigabe: nichts. Offen zur Technik sind nur 345 und 249, beide betreffen Plan 5.
- Anforderungsautor, erst in der nächsten Domänenphase (340 F6 A):
  [340](anliegen/340-aufstellenSchwerZuPruefen.md) (F5 A entschieden; F3: deine Antwort
  verlangt Kriterien als Anwendungsfall, den Zweck klarer),
  [345](anliegen/345-spiegelZwischenAnforderungUndCode.md) (F1 bis F3 offen).
- Organisationsentwickler: [353](anliegen/353-startbefehlImReview.md),
  [354](anliegen/354-commitsMitBetreffNennen.md) (Stellungnahme leer);
  [289](anliegen/289-pruefungenBrechenAmHookDesNachbarnAb.md) (Runde 2; 304 ist erledigt,
  die Wartebedingung entfällt); Nachprüfung
  [351](anliegen/351-reviewVierFormDerSchritteVierUndSechs.md).
- Regelumsetzer: [246](anliegen/246-dashboardAlleSessionsMitSeitenzaehler.md),
  [275](anliegen/275-dashboardSichtDerAnliegen.md),
  [249](anliegen/249-werkzeugFestUndImportvertragDerTests.md).
- Planer: Nachprüfung [350](anliegen/350-zykluszielFuerPlan5.md).
- UX: Nachprüfung [352](anliegen/352-planOhneLinksAufGeloeschteMockups.md).
- Reviewer, Testautor, Architekt, Fachkritiker: keins. AUF-5.5 wartet auf den Testautor
  (Plan 5, nicht jetzt).

## Vorschläge
- Löschen: 348 und 349 (Kopf `erledigt`, Löschlauf, kein Zug nötig).
- Schließen: 350, 351, 352 sind `angenommen` und umgesetzt (Review 4 und Plan 4 zeigen es);
  Planer, Organisationsentwickler und UX dürfen `erledigt` setzen, wenn die Nachprüfung stimmt.
- Zusammen: 340 und 345 in einem Zug des Anforderungsautors (gleiche Dateien, beide
  F6 A); 353 mit 354 in einem Lauf (beide ändern Schritt 6 in `ablauf.md`).
- Reihenfolge nach 340 F6 A und Review 4: erst 340 und 345, dann die Kriterien, dann Plan 5.
- Stränge Regelumsetzer, höchstens ein Hook-Code-Lauf
  ([Ablauf](../prozess/ablauf.md#gleichzeitige-läufe)): 246 mit 275 zuerst (`dashboard.py`,
  von `laufLog.py` als SubagentStop-Hook importiert), danach 249 (`pyproject.toml`,
  Importvertrag). Die Funde 1 bis 3 im Rundgang Prüfcode sind noch kein Anliegen; sie
  entstehen nach deinem Kommentar im Review.
- Organisationsentwickler: 353 mit 354 und 289 sind Text und `regeln.md`, sie laufen
  nebeneinander und neben dem Regelumsetzer; die Nachprüfung 351 ist ein eigener kurzer Lauf.
- Planer und UX: Nachprüfungen sind getrennte Dateien und laufen gleichzeitig.

## Fragen an dich
Keine offen. Deine Antwort zu 340 F3 liegt beim Anforderungsautor, nicht bei dir.
