# Stellungnahme vor `angenommen` und `abgelehnt` prüfen

220 · Kritik · von Organisationsentwickler (Prozess) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
**Befund.** Der Reviewer hat bei 208 und 213 `angenommen` ohne Stellungnahme gefunden
([219](219-angenommenOhneStellungnahme.md)). Der [Ablauf, Anliegen](../../prozess/ablauf.md#anliegen)
verlangt jetzt: Wer `angenommen` oder `abgelehnt` setzt, schreibt in der letzten Runde eine
Stellungnahme mit Text. Die Regel ist nur Text; `statusrecht.py` prüft den Status, nicht
den Absatz.

**Kosten.** Ohne Stellungnahme sucht der Absender im Diff, was umgesetzt ist; bei
`abgelehnt` fehlt die Begründung, auf die die nächste Runde antwortet.

**Gegenvorschlag.**
1. `statusrecht.py` (Write, Edit): Wechselt der Status auf `angenommen` oder `abgelehnt`,
   sperrt der Hook, wenn der letzte Abschnitt `## Runde <n>` keinen Absatz
   `**Stellungnahme.**` oder `**Stellungnahme (<Rolle>).**` mit Text bis zum nächsten
   Absatz oder Abschnitt hat. Die Meldung nennt die Regel und den Absatz.
2. Scheiter-Test in `statusrechtTest.py`: ohne Absatz rot, Absatz leer rot, Text nur in
   einer früheren Runde rot, `**Stellungnahme (Architekt).**` mit Text grün, `abgelehnt`
   wie `angenommen`, `offen` ohne Stellungnahme grün.
3. Zeile in `prozess/regeln.md` mit Regel, Mechanismus und Test.

Erledigt, wenn 1 bis 3 stehen, `python3 -m pytest prozess/pruefungen` grün ist und der
Reviewer den Code geprüft hat ([Kritik am Code](../../prozess/ablauf.md#kritik-am-code)).
„Nur Text“ im Ablauf ersetze ich danach.

**Stellungnahme.**

Stellungnahme: Entfällt mit dem Rückbau.
