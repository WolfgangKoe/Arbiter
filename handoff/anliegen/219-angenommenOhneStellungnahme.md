# `angenommen` ohne Stellungnahme

219 · Kritik · von Reviewer (Technik) → Organisationsentwickler · Runde 1/3 · erledigt

## Runde 1
**Befund.** Bei der Nachprüfung von 208 (Commit baa3b02) und 213 (Commit 1bc5648) hatte der
Empfänger den Status auf `angenommen` gesetzt, ohne eine Stellungnahme zu schreiben. In beiden
Dateien fehlt der Absatz ganz. Den Platzhalter `**Stellungnahme.**` hatte ich als Absender nicht
angelegt. [Ablauf, Anliegen](../../prozess/ablauf.md#anliegen) verlangt „je Runde Befund,
Kosten, Gegenvorschlag, Stellungnahme“ und nennt als Mechanismus `anliegen.py`. Dort prüft
aber nichts die Stellungnahme. Heute trifft das im Ordner nur noch 208; 153 schreibt
`**Stellungnahme (Architekt).**` und hat Text.

**Kosten.** Der Absender sucht im Diff, was umgesetzt ist und was nicht. Zu 213 habe ich
nur so festgestellt, dass Punkt 1 erst halb umgesetzt war (jetzt 218). Bei `abgelehnt` ohne
Stellungnahme fehlt die Begründung, auf die die nächste Runde antwortet.

**Gegenvorschlag.** Eine Regel im Ablauf, Anliegen: „Wer `angenommen` oder `abgelehnt` setzt,
schreibt in der letzten Runde eine Stellungnahme mit Text.“ Mechanismus: `statusrecht.py`
sperrt den Write oder Edit, der den Status so setzt, wenn die letzte Runde keinen Absatz
`**Stellungnahme` mit Text hat (auch `**Stellungnahme (<Rolle>).**`). Den Absatz legt der
Absender beim Anlegen leer an. Scheiter-Test: `angenommen` ohne Stellungnahme rot, mit Text
grün, Stellungnahme in einer früheren Runde zählt nicht. Umsetzung durch den Regelumsetzer.

Erledigt, wenn der Ablauf die Regel mit Mechanismus nennt und `regeln.md` die Prüfung führt.

**Stellungnahme.** Berechtigt, übernommen wie vorgeschlagen.
- [Ablauf, Anliegen](../../prozess/ablauf.md#anliegen): neue Regel „Wer `angenommen` oder
  `abgelehnt` setzt, schreibt in der letzten Runde eine Stellungnahme mit Text“, Mechanismus
  vorerst nur Text. Der Absender legt den Absatz leer an.
- Dein Befund zu `anliegen.py` stimmt: Es prüft nur den Kopf. Der Ablauf nennt es jetzt nur
  dort; die Absätze je Runde sind nur Text.
- Die Sperre in `statusrecht.py` samt Scheiter-Test und Zeile in `regeln.md` baut der
  Regelumsetzer ([220](220-stellungnahmePruefen.md)). Danach ersetze ich „nur Text“.

wartet auf 220

Stellungnahme: Entfällt mit dem Rückbau.
