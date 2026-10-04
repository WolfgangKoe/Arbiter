# Lauf-Log: Schreibgrenze, doppelte Läufe, kaputte Zeile

189 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
Kritik am Code von Commit bbe724a (Retro 2 P4). `dashboardTest.py` ist grün. Sechs Befunde:

**B1 · Jeder Rollenlauf meldet eine verletzte Schreibgrenze.** `laufLog.py:45-52` schreibt
bei SubagentStop `dashboard.html` und `prozess/dashboard/laeufe.jsonl`, beide im git.
`schreibgrenze.beimEnde` vergleicht im selben Ereignis `git status` mit dem Stand beim
Start. War der Baum sauber, sind beide Dateien neu geändert und außerhalb der Schreibpfade
jeder Rolle außer dem Regelumsetzer: „Schreibgrenze verletzt … dem Stakeholder melden“.
Die Hooks laufen parallel, ob die Meldung kommt, ist ein Wettlauf. Dazu bleiben nach jedem
Lauf zwei Dateien uncommittet (Stand), und das Log wächst als Historie im Repo, gegen
CLAUDE.md „Keine Historie in Dateien, git ist das Archiv.“
Kosten: Fehlalarme, die echte Verstöße verdecken; Rauschen in jedem Commit.
Gegenvorschlag: beide Dateien in `.gitignore` (Ort bleibt wie in P4), mit Scheiter-Test in
`gitignoreTest.py`; aus dem Repo nehmen.

**B2 · Ein Lauf zählt doppelt.** `schlussantwort.py:23` blockt einen zu langen Bericht mit
`decision: block`; die Rolle läuft weiter, SubagentStop kommt ein zweites Mal
(`stop_hook_active`), `laufLog.py` trägt erneut ein.
Kosten: „Rolle (n)“ und das Mittel in der Verteilung stimmen nicht.
Gegenvorschlag: `agent_id` in den Eintrag; `läufeLesen` behält je `agent_id` den letzten.

**B3 · Eine kaputte Zeile friert das Dashboard ein.** `laufLog.läufeLesen:41` wirft bei
einer halben Zeile (zwei Rollen enden gleichzeitig, Hook nach 10 s abgebrochen)
`JSONDecodeError`. Im Hook schluckt `except Exception` das, ab dann wird `dashboard.html`
nie mehr erneuert, ohne Meldung; `python3 prozess/pruefungen/dashboard.py` bricht ab
(nachgestellt).
Gegenvorschlag: unlesbare Zeilen überspringen wie `belegung.belegungAusZeile`, mit Test.

**B4 · Uhrzeit in UTC.** `laufLog.py:51` `datetime.now(UTC)`, `dashboard.py:57` zeigt die
Stunde ohne Zone: der Lauf von 14:17 Ortszeit steht als „12:17“.
Gegenvorschlag: `datetime.now().astimezone()`.

**B5 · `punkte` steht doppelt.** `dashboard.py:35` baut `belegung.punkte` nach.
Gegenvorschlag: aus `belegung` importieren.

**B6 · Abweichung von P4 und Stellungnahme.** P4 legt „Daten und Skripte in
`prozess/dashboard/`“ fest, die Skripte liegen in `prozess/pruefungen/` (dein Auftrag
verlangt dort Skripte). Die Stellungnahme zu 158 sagt „Das Log beginnt leer“, der Commit
bringt einen Eintrag mit.
Gegenvorschlag: Ort mit dem Organisationsentwickler klären, Satz in 158 berichtigen oder
Eintrag mit B1 entfernen.

**Stellungnahme.**
