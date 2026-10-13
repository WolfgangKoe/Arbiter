# Moderation

Stand vor Freigabe Plan 5: 7 Anliegen im Ordner. Dein Kommentar im Plan (Einheit komplett
aufstellen) ist kein Anliegen; er liegt beim Planer und in [Plan](plan.md).

## Dran
Blockiert Plan 5 (Items 1 bis 3): Anliegen 368,
denn der Testautor ordnet die Tests, bevor die neuen entstehen. Sonst hängt kein Anliegen
an einem Item.
- Testautor: Anliegen 368 (Technikphase 5,
  mit den neuen Tests); Nachprüfung von
  Anliegen 363.
- Regelumsetzer: Anliegen 367 (Teil 3 erst nach
  368); Nachprüfung von Anliegen 360; danach der Teil
  des Regelumsetzers aus 384.
- Organisationsentwickler: Anliegen 384 (F1 A, Antwort
  liegt vor, noch uncommittet), Anliegen 369,
  Anliegen 376.
- Planer, Architekt, UX, Reviewer, Fachkritiker, Anforderungsautor: keins.

## Vorschläge
- Zusammen: 369 und 376 in einem Zug des Organisationsentwicklers (gleiche Art, Texte der
  Rollen und des Formats); 384 ändert Ich 2 und Ablauf, eigener Zug.
- Schließen: 363 ist umgesetzt (Stellungnahme); der Testautor setzt `erledigt`, wenn die
  Nachprüfung stimmt. 360 ebenso, der Regelumsetzer, sobald F4 beantwortet ist.
- Reihenfolge: erst 368, dann Teil 3 aus 367, dann Plan-5-Tests; 369 vor dem nächsten
  Akzeptanztest, damit der Skill stimmt.
- Stränge Regelumsetzer, höchstens ein Hook-Code-Lauf
  ([Ablauf](../prozess/ablauf.md#gleichzeitige-läufe)): zuerst 360 (`dashboard.py`, von
  `laufLog.py` als Hook importiert), dann 384 (`schreibgrenze.py`, Hook), 367 daneben nur,
  wenn `benennung.py` frei ist: erst 363 nachprüfen, sie ändern dieselbe Datei.
- Stränge Organisationsentwickler: 369 und 376 gleichzeitig mit 384 möglich, wenn die
  Dateien getrennt sind (Skill und `domaene/CLAUDE.md`, `architekt.md`, `ich.md`).
- Testautor (368) läuft neben dem Regelumsetzer: eigene Dateien, keiner wartet; 367 Teil 3
  wartet auf 368.

## Fragen an dich
- Anliegen 360 F4: Zeitpunkt, an dem deine Züge aus
  dem Dashboard in die Dateien kommen. A Hook vor Rollenstart und Commit, B nur auf Knopfdruck.
  Antwort steht auf `.`, also Empfehlung A; bitte bestätigen oder B.
