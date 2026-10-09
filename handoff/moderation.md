# Moderation

Stand vor Freigabe Plan 5: 7 Anliegen im Ordner. Dein Kommentar im Plan (Einheit komplett
aufstellen) ist kein Anliegen; er liegt beim Planer und in [Plan](plan.md).

## Dran
Blockiert Plan 5 (Items 1 bis 3): [368](anliegen/368-akzeptanztestsInDerFolgeDerKriterien.md),
denn der Testautor ordnet die Tests, bevor die neuen entstehen. Sonst hängt kein Anliegen
an einem Item.
- Testautor: [368](anliegen/368-akzeptanztestsInDerFolgeDerKriterien.md) (Technikphase 5,
  mit den neuen Tests); Nachprüfung von
  [363](anliegen/363-spiegelpruefungStuerztBeiTestImAkzeptanzordnerAb.md).
- Regelumsetzer: [367](anliegen/367-spiegelpruefungInhaltUndDomaene.md) (Teil 3 erst nach
  368); Nachprüfung von [360](anliegen/360-dashboardAnliegenBearbeiten.md); danach der Teil
  des Regelumsetzers aus 384.
- Organisationsentwickler: [384](anliegen/384-schreibgrenzeAuchFuerBash.md) (F1 A, Antwort
  liegt vor, noch uncommittet), [369](anliegen/369-skillUndDomaenenformatNachDemNeuenSchnitt.md),
  [376](anliegen/376-ausnahmeFuerDenArchitektenInDerDomaenenphase.md).
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
- [360](anliegen/360-dashboardAnliegenBearbeiten.md) F4: Zeitpunkt, an dem deine Züge aus
  dem Dashboard in die Dateien kommen. A Hook vor Rollenstart und Commit, B nur auf Knopfdruck.
  Antwort steht auf `.`, also Empfehlung A; bitte bestätigen oder B.
