# Backlog · Prozess

Zurückgestellt, bis ein Befund es auslöst. Was ausgelöst ist, wird ein Prozess-Item der Retro.
Ein Mechanismus entsteht erst bei beobachtetem Bedarf (Retro 3).

- Belegte Kriterien je Etappe zählen ([Kennzahlen](kennzahlen.md)): Stand und Dashboard
  zeigen „Etappe <n>: x von y Kriterien belegt“, daneben alle (Anliegen 3550, A). Wie ein
  Kriterium seine Etappe nennt, legen Planer und Anforderungsautor in Domänenphase 8 fest
  (Anliegen 3661); dann wird die Zählung ein Item der Retro 8 für den Regelumsetzer.
- Mechanismus für „Der Empfänger setzt nie `erledigt`“ ([Ablauf, Anliegen](ablauf.md#anliegen)):
  Die Schreibgrenze sperrt Write und Edit, die `erledigt` in den Kopf schreiben, wenn die
  Rolle nicht der Absender ist (Gegenvorschlag in Anliegen 1591). Auslöser: Ein Empfänger
  setzt erneut `erledigt`.
- `ruff format --check` über `technik/` und `prozess/pruefungen/` in `ruffAufrufen`, Markdown
  ausgenommen, und unter Werkzeuge im Ablauf (Empfehlung a in Anliegen 1581); bis dahin
  „nicht verwendet“. Auslöser: Ein Kritiker meldet eine Formfrage in Python, die ruff format
  entschiede.

Mechanismus: nur Text, Höchstmaß `prozess/kennzahlen.md` (Backlog je Perspektive).
