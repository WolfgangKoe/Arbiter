# Backlog · Prozess

Zurückgestellt, bis ein Befund es auslöst. Was ausgelöst ist, wird ein Prozess-Item der Retro.
Ein Mechanismus entsteht erst bei beobachtetem Bedarf (Retro 3).

- `formregeln/glossar.py` prüft auch zusammengesetzte Namen auf eine Abkürzung, die das
  Glossar ersetzt hat (B statt *Bewegungsweite*). Auslöser: eine solche Abkürzung im Code.
- Tote Links in `handoff/` (Plan auf gelöschte Items, 5521 auf `anhaltenAmB.md`) meldet eine
  Prüfung. Auslöser: Du folgst einem toten Link.
- Die Form eines Anliegens prüft ein Hook schon beim Schreiben. Auslöser: wieder scheitert ein
  Commit an einem Anliegen.
- Kommentiert der Stakeholder im Chat, trägt der Koordinator es als `Kommentar:` ein
  ([Freigabe](ablauf/freigabe.md)). Auslöser: ein Kommentar im Chat geht verloren.
- Ein Skill des Testautors zum Umbenennen: ganze Testdateien nach einer Vorlage in `/tmp`
  neu schreiben statt Stelle für Stelle (Retro 10; vier Läufe für 11821). Auslöser: wieder
  eine Umbenennung über mehrere Testdateien.
- Die Moderation vor einer Freigabe wird ein Schritt im Fortschritt
  ([Moderator](../.claude/agents/moderator.md)). Auslöser: wieder eine Freigabe ohne
  Moderation davor (Retro 10, Review 10).
- Der Testautor schreibt `mutationsregeln/gleichwertig.json` selbst. Auslöser: wieder wartet die
  DoD auf das Anliegen; bis dahin prüft eine zweite Rolle die Begründung (Absicht 1).
- Mechanismus für „Der Empfänger setzt nie `erledigt`“ ([Ablauf, Status der Anliegen](ablauf/anliegenStatus.md)):
  Die Schreibgrenze sperrt Write und Edit, die `erledigt` in den Kopf schreiben, wenn die
  Rolle nicht der Absender ist (Gegenvorschlag in Anliegen 1591). Auslöser: Ein Empfänger
  setzt erneut `erledigt`.
- `ruff format --check` über `technik/` und `prozess/pruefungen/` in `ruffAufrufen`, Markdown
  ausgenommen, und unter Werkzeuge im Ablauf (Empfehlung a in Anliegen 1581); bis dahin
  „nicht verwendet“. Auslöser: Ein Kritiker meldet eine Formfrage in Python, die ruff format
  entschiede.

Mechanismus: nur Text, Höchstmaß `prozess/kennzahlen.md` (Backlog je Perspektive).
