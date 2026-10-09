# Moderation

Stand vor Freigabe Retro 4: 9 Anliegen im Ordner. An den Items von [Plan 4](plan.md) hängt
keins; Plan 5 braucht [249](anliegen/249-werkzeugFestUndImportvertragDerTests.md).

## Dran
Blockiert die Freigabe: nichts.
- Anforderungsautor, erst in der nächsten Domänenphase (340 F5 A, F6 A):
  [340](anliegen/340-aufstellenSchwerZuPruefen.md),
  [345](anliegen/345-spiegelZwischenAnforderungUndCode.md) (F1 bis F3 offen).
- Regelumsetzer: [246](anliegen/246-dashboardAlleSessionsMitSeitenzaehler.md),
  [275](anliegen/275-dashboardSichtDerAnliegen.md) (Stellungnahme leer),
  [249](anliegen/249-werkzeugFestUndImportvertragDerTests.md) (vor Technikphase 5).
- Reviewer, Nachprüfung der umgesetzten Stellungnahmen:
  Anliegen 289 (Runde 2),
  Anliegen 353,
  Anliegen 354,
  Anliegen 355.
- Testautor: AUF-5.5 wartet (Plan 5, nicht jetzt). Organisationsentwickler, Planer, UX,
  Architekt, Fachkritiker: keins.

## Vorschläge
- Zusammen: 340 und 345 in einem Zug des Anforderungsautors (gleiche Dateien); 353, 354,
  355 in einer Nachprüfung des Reviewers (alle ändern Schritt 6 in `ablauf.md`), 289 dazu.
- Schließen: 289, 353, 354, 355 sind umgesetzt (Stellungnahme, Retro 4); der Reviewer setzt
  `erledigt`, wenn die Nachprüfung stimmt.
- Reihenfolge: nach Retro 4 erst 340 und 345, dann die Kriterien, dann Plan 5; 249 vor der
  Technikphase 5.
- Stränge Regelumsetzer, höchstens ein Hook-Code-Lauf
  ([Ablauf](../prozess/ablauf.md#gleichzeitige-läufe)): 246 mit 275 zuerst (`dashboard.py`,
  von `laufLog.py` als Hook importiert), danach 249 (`pyproject.toml`, Importvertrag). Das
  Spiegelskript aus 340 kommt nach 345, im Zug der Domänenphase.
- Der Reviewer läuft neben dem Regelumsetzer und dem Anforderungsautor: eigene Dateien,
  keiner wartet.

## Fragen an dich
Keine offen. 345 F1 bis F3 liegen beim Anforderungsautor, nicht bei dir.
