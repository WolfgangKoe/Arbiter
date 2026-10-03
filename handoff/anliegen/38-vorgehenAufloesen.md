# VORGEHEN.md auflösen: Zuordnung und Offenes

38 · Fragen · von Organisationsentwickler (Prozess) → Stakeholder · Runde 1/3 · offen

## Runde 1
**Befund.** Jede Entscheidung aus `VORGEHEN.md` ist zugeordnet; die Datei bleibt unverändert.
- An ihrem Ort: E1, E7, E21, E22, E38 (`CLAUDE.md`, `prozess/ablauf.md`, `stand.py`) · E2,
  E8, E52 (`schreibgrenze.py`, `bashPositivliste.py`, `.gitignore`) · E3, E4/E15, E16, E24,
  E29, E30, E49, E51 (`.claude/agents/`) · E5, E11/E17, E20, E23, E25–E28, E33–E35,
  E39–E42, E46, DoR, DoD, Werkzeugprobe (`prozess/ablauf.md`, `prozess/kennzahlen.md`) ·
  E12, E36 (`prozess/praemissen/wir.md`) · E14 (`prozess/regeln.md`) · E43–E45, E48
  (`.claude/settings.json`, `rollenkontext.py`) · E50 (`domaene/ziel.md`) · E53–E55
  (`hoechstmassTest.py`, `schlussantwort.py`, `lesegrenze.py`, `stand.py`) · Formate von
  Anforderung, Item, Glossar, Daten (`domaene/CLAUDE.md`) und Akzeptanztest (Skill).
- Überholt: Einstieg, Ausgangslage, Schritte 1–7 (git) · E10 für `pyproject.toml` (schreibt
  der Regelumsetzer) · Kontextlandkarte als Vorabplan (Ordner entstehen mit Bedarf, E24) ·
  Testnamen `test_bw_4_3_…` und Anliegen „30 Zeilen“, „2.400“ · Harness-Fakten (in den Hooks
  umgesetzt, sonst `claude-code-guide`).
- An die Technik: Grundschnitt von Code und Tests, Spiegel, Daten, Design-System (E31),
  Refactoring-Items (E41): [Anliegen 39](39-architekturAusDemVorgehen.md).
- Offen:
  1. Dashboard (E18): [Anliegen 22](22-dashboard-und-budget-am-kontextfenster.md), Retro 1.
  2. Messung der Grund- und Arbeitslast (E47), Auslösezähler (E26), Kennzahlen zu Anliegen
     aus git (E33): Prozess-Items aus 22 und
     [31](31-kritikDesEntwicklersFuerRetro1.md), Retro 1.
  3. Prüfungen zu DoR, DoD 2 (Rest), kursiven Begriffen (E35) und Werkzeugsatz (E37):
     Prozess-Items, Retro 1.
  4. Skills bei Befund: `anliegen-schreiben` ([20](20-antwort-unter-jeder-frage.md)),
     `anforderung-schreiben`, `regel-nachschlagen`, `improve` (E19, E30).
  5. Migration (Schritt 9): Regeltexte, alte Spezifikationen, Dashboard (F2).
  6. `doku/` für Menschen (E32, Schritt 10): kein Auslöser (F3).
  7. Moderation: Auslöser „mehr als 5 offene Anliegen“ ist überschritten (F4).
  8. Koordinator ohne Systemprompt von Claude Code beobachten (E45): Retro 1.

**Löschbar.** `VORGEHEN.md`, wenn 39 erledigt ist und `pyproject.toml` nicht mehr auf E37
zeigt ([33](33-ablaufNachDenMechanismen.md)). `handoff/kritik-entwickler.md` nach Retro 1
(31). `Arbiter/`, `ArbiterMap/` nach F2: Heute verweisen `domaene/CLAUDE.md`, `architekt.md`
und 22 darauf.

**Kosten.** Bis dahin hält dieses Anliegen die offenen Punkte; Rollen lesen VORGEHEN.md nicht.

**F1 · Wie setzt du `erledigt` bei deinen Anliegen ([34](34-erledigtNurDurchDenAbsender.md))?**
A: selbst in der Kopfzeile. B: „.“ bei der Freigabe, der Empfänger trägt es ein;
`statusrecht.py` erlaubt ihm das bei deinen Anliegen. Empfehlung A: folgt aus deiner
Entscheidung, nichts zu bauen. `prozess/ablauf.md` steht so.

Antwort: .

**F2 · Wie zieht der Altbestand um?** A: Du kopierst `ArbiterMap/reference/rules/` und
`ArbiterMap/docs/spec/domain_rules.md` nach `domaene/referenz/`, ohne Tokenkosten; ich
setze die Verweise um. B: je Stück, wenn ein Item es braucht. Empfehlung A für die
Regeltexte (jede Anforderung braucht sie), B für Spezifikationen und Dashboard.

Antwort: . Ich habe den Ordner "rules" und die Datei "domain_rules.md" aus Arbitermap nach domaene/reference/ kopiert.

**F3 · `doku/` wann?** A: nach Etappe 1. B: erst auf deinen Wunsch. Empfehlung B: Niemand
hat danach gefragt; Pflege kostet je Retro.

Antwort: A

**F4 · Moderation bei 23 offenen Anliegen?** A: jetzt vorschlagen. B: in Retro 1 mit der
Zahl offener Anliegen je Phase bewerten; die meisten warten auf ihre Phase. Empfehlung B.

Antwort: .

**Stellungnahme.**
