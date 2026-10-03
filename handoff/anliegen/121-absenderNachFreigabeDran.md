# Nach der Freigabe ist der Absender dran

121 · Kritik · von Organisationsentwickler (Prozess) → Regelumsetzer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Aus [119](119-antwortenNachFreigabeAufgreifen.md): [83](83-sprungErproben.md)
blieb nach `Freigabe Plan 2` liegen, weil `wartetAuf` bei `offen` immer den Empfänger meldet,
also den Stakeholder, obwohl die Freigabe die Fragen beantwortet hatte. Die Regel steht jetzt
in [Ablauf, Anliegen](../../prozess/ablauf.md#anliegen): Ein Anliegen an den Stakeholder mit
Status `offen`, seit der letzten Freigabe unverändert, hat die Freigabe beantwortet; dran ist
der Absender.

**Kosten.** Antworten des Stakeholders warten, bis er nachfragt.

**Gegenvorschlag.** In `anliegen.py` (`wartetAuf`, `dran`): Empfänger Stakeholder, Status
`offen`, und die letzte Änderung der Datei liegt nicht nach dem jüngsten Commit mit Betreff
`Freigabe <Etappe|Plan|Retro> <n>` (gleicher Commit zählt als beantwortet; uncommittete
Änderung nicht) → dran ist der Absender. Ohne Freigabe in git bleibt der Stakeholder dran.
`eskaliert` bleibt beim Stakeholder: Er setzt mit seiner Entscheidung den Kopf selbst.
Den jüngsten Freigabe-Commit kann `gitAufruf.py` neben `freigabeCommit` liefern.

Scheiter-Tests in `anliegenTest.py` oder `standTest.py`:
- Fragen an den Stakeholder, vor der Freigabe committet → Absender dran.
- Dasselbe, im Freigabe-Commit geändert → Absender dran.
- Nach der Freigabe angelegt oder geändert → Stakeholder dran.
- `eskaliert`, vor der Freigabe → Stakeholder dran.
Eintrag in `prozess/regeln.md`; den Vermerk in `ablauf.md` setze ich.

Erledigt, wenn die vier Fälle grün sind und `python3 -m pytest prozess/pruefungen` grün ist.

**Stellungnahme.** Angenommen und umgesetzt: `wartetAuf(wurzel, anliegen)` in `anliegen.py`,
`jüngsteFreigabe` und `seitFreigabeUnverändert` in `gitAufruf.py`. Die vier Fälle stehen in
`anliegenTest.py`, dazu zwei Grenzfälle (keine Freigabe in git; neu nach der Freigabe).
Eintrag in `prozess/regeln.md`.

**Nachprüfung.** In Ordnung (89364ab): Bedingung wie vorgeschlagen, Freigabe-Commit zählt
mit, uncommittete Änderung nicht; `kennzahlen.py` nutzt dieselbe Regel; Tests grün. Vermerk
in `ablauf.md` (Anliegen) gesetzt.
