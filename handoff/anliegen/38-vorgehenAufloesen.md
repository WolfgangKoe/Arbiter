# VORGEHEN.md auflösen: Zuordnung und Offenes

38 · Fragen · von Organisationsentwickler (Prozess) → Stakeholder · Runde 1/3 · beantwortet

## Runde 1
**Befund.** Jede Entscheidung aus `VORGEHEN.md` ist zugeordnet; die Datei bleibt unverändert.
- An ihrem Ort: E1, E7, E21, E22, E38 (`CLAUDE.md`, `prozess/ablauf.md`, `stand.py`) · E2,
  E8, E52 (`schreibgrenze.py`, `bashPositivliste.py`, `.gitignore`) · E3, E4/E15, E16, E24,
  E29, E30, E49, E51 (`.claude/agents/`) · E5, E11/E17, E20, E23, E25–E28, E32, E33–E35,
  E39–E42, E46, DoR, DoD, Werkzeugprobe (`prozess/ablauf.md`, `prozess/kennzahlen.md`) ·
  E12, E36 (`prozess/praemissen/wir.md`) · E14 (`prozess/regeln.md`) · E43–E45, E48
  (`.claude/settings.json`, `rollenkontext.py`) · E50 (`domaene/ziel.md`) · E53–E55
  (`hoechstmassTest.py`, `schlussantwort.py`, `lesegrenze.py`, `stand.py`) · Grundschnitt,
  Spiegel, Daten, Design-System, E31, E41 (`technik/architektur.md`, `prozess/ablauf.md`,
  `architekt.md`) · Formate (`domaene/CLAUDE.md`, Skill `akzeptanztest-schreiben`).
- Überholt: Einstieg, Ausgangslage, Schritte 1–7 (git) · E10 für `pyproject.toml` (schreibt
  der Regelumsetzer) · Kontextlandkarte als Vorabplan (Ordner entstehen mit Bedarf, E24) ·
  Testnamen `test_bw_4_3_…` und Anliegen „30 Zeilen“, „2.400“ · Harness-Fakten (in den Hooks
  umgesetzt, sonst `claude-code-guide`).
- Offen, alles in Retro 1:
  1. Dashboard (E18): [Anliegen 22](22-dashboard-und-budget-am-kontextfenster.md).
  2. Messung der Grund- und Arbeitslast (E47), Auslösezähler (E26), Kennzahlen zu Anliegen
     aus git (E33): aus 22 und [31](31-kritikDesEntwicklersFuerRetro1.md).
  3. Prüfungen zu DoR, DoD 2 (Rest), kursiven Begriffen (E35) und Werkzeugsatz (E37).
  4. Skills bei Befund: `anliegen-schreiben` ([20](20-antwort-unter-jeder-frage.md)),
     `anforderung-schreiben`, `regel-nachschlagen`, `improve` (E19, E30).
  5. Moderation (F4).
  6. Koordinator ohne Systemprompt von Claude Code beobachten (E45).

**Löschbar.** `VORGEHEN.md`, wenn Retro 1 die offenen Punkte übernommen hat und
`pyproject.toml` nicht mehr auf E37 zeigt ([Anliegen 57](57-pyprojectOhneVorgehen.md)).
`handoff/kritik-entwickler.md` nach Retro 1 (31). `Arbiter/`, `ArbiterMap/`, wenn nichts mehr
darauf zeigt: alte Spezifikationen (`domaene/CLAUDE.md`), Altbestand-Code als Beispiel
(`technik/architektur.md`, `architekt.md`), Dashboard (22).

**Kosten.** Bis dahin hält dieses Anliegen die offenen Punkte; Rollen lesen VORGEHEN.md nicht.

**F1 · Wie setzt du `erledigt` bei deinen Anliegen?** A: selbst in der Kopfzeile. B: „.“ bei
der Freigabe, der Empfänger trägt es ein. Empfehlung A.

Antwort: .

**F2 · Wie zieht der Altbestand um?** A: Du kopierst die Regeltexte und `domain_rules.md` nach
`domaene/referenz/`; ich setze die Verweise um. B: je Stück, wenn ein Item es braucht.
Empfehlung A für die Regeltexte, B für Spezifikationen und Dashboard.

Antwort: . Ich habe den Ordner "rules" und die Datei "domain_rules.md" aus Arbitermap nach domaene/reference/ kopiert.

**F3 · `doku/` wann?** A: nach Etappe 1. B: erst auf deinen Wunsch. Empfehlung B.

Antwort: A

**F4 · Moderation bei 23 offenen Anliegen?** A: jetzt vorschlagen. B: in Retro 1 mit der
Zahl offener Anliegen je Phase bewerten. Empfehlung B.

Antwort: .

**Eingearbeitet.** F1 steht so in `prozess/ablauf.md` (Anliegen). F2: `domaene/CLAUDE.md`
zeigt auf `domaene/referenz/rules/` und `referenz/domainRules.md`; die Kopien gleichen dem
Original, Fundstellen gelten weiter. F3: `prozess/ablauf.md`, Prozessphase 1: `doku/` in der
Retro, nachdem eine Etappe erreicht ist. F4: Offen 5. Nach Retro 1 setze ich `erledigt`.
