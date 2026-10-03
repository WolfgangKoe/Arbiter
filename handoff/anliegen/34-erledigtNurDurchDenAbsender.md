# Ablauf: erledigte Anliegen löschen sich, nur der Absender setzt erledigt

34 · Anliegen · von Regelumsetzer (Prozess) → Organisationsentwickler · Runde 1/3 · offen

## Runde 1
**Befund.** Entscheidung des Stakeholders: Ein Skript löscht jedes Anliegen mit Status
`erledigt` ohne eigenen Lauf; `erledigt` setzt nur der Absender, auch der Stakeholder bei
seinen Anliegen. Gebaut: `erledigteLoeschen.py` (pre-commit, SubagentStop, pytest-Lauf) und
`statusrecht.py` (sperrt Write und Edit durch andere Rollen). `prozess/ablauf.md`,
Abschnitt Anliegen, stimmt nicht mehr, und ich darf ihn nicht schreiben:
1. Statustabelle, Zeile erledigt: „Datei im selben Lauf löschen“ ist falsch. Das Skript
   löscht die Datei; niemand löscht von Hand.
2. Der Satz „Ein Anliegen mit Status `erledigt` hält … rot“ ist überholt und zu ersetzen
   durch: Das Skript löscht es (`erledigteLoeschen.py`).
3. „Ist der Stakeholder Absender, prüft er … löscht der Empfänger“ ist überholt. Offen:
   Der Stakeholder hat keine Schreibrechte als Rolle; wer trägt `erledigt` für ihn ein?
   Der Koordinator hat kein Write und kein Edit. Die Sperre greift ohne `agent_type` nicht,
   der Stakeholder selbst kann es also ohne Hindernis eintragen.
4. Nicht mechanisch durchsetzbar: Eine Rolle mit Bash kann per `sed -i` oder Umleitung
   `erledigt` setzen, an `statusrecht.py` vorbei. Das Skript löscht die Datei dann trotzdem.
   Der Ablauf muss festhalten: Rollen ändern Anliegen nur mit Write und Edit.
5. `statusrecht.py` verweist auf diese Datei; sie darf erst mit der Korrektur von Punkt 4
   verschwinden.

**Kosten.** Eine Änderung an `ablauf.md`; keine Laufzeitkosten.

**Gegenvorschlag.** Punkte 1 bis 4 in `ablauf.md` übernehmen und die Zeile in
`prozess/regeln.md` danach mit Vermerk versehen.

**Stellungnahme.** Offen.
