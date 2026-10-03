# Dashboard: wann und wo

90 · Fragen · von Organisationsentwickler (Prozess) → Stakeholder · Runde 1/3 · offen

## Runde 1
**Befund.** Du hast das Dashboard im Backlog ausgelöst (027b75d). Nach dem
[Ablauf](../../prozess/ablauf.md#prozessphase) wird es ein Prozess-Item der Retro; Retro 1 ist
freigegeben, Retro 2 folgt nach Review 2. Vorlage: `ArbiterMap/harness/report_page.*`
(57.000 Zeichen), gebündelt von `process_report.py` aus drei Quellen: Kontextkurve,
Subagenten-Läufe, Backlog-Items. Hier hält `belegung.py` je Lauf nur den letzten Wert
(`.git/arbiter/belegung/`), `rollenzaehler.py` Rolle und Phase ohne Token; Kurve und Token je
Lauf fehlen. Bordmittel: Ein Plugin (`.claude-plugin/plugin.json`, `hooks/hooks.json`) lädt
seine Hooks in jedem Repo, in dem es aktiviert ist (Nutzer- oder Projekt-Scope).

**Kosten.** Als Item der Retro 2 ist das Dashboard erst nach ihr da; Retro 2 hätte wieder nur
`kennzahlen.py`, also genau den Befund aus dem Backlog. Jetzt gebaut, läuft der Regelumsetzer
außerhalb seiner Phase, zwischen den Läufen der Domäne, nie gleichzeitig mit ihnen.

**Gegenvorschlag (Prozess-Item für den Regelumsetzer).**
1. Plugin `dashboard` in `prozess/dashboard/`: Ein Hook auf `SubagentStop` und `Stop` hängt je
   Lauf eine Zeile an `.git/arbiter/laeufe.jsonl` (Zeit, Rolle, Phase, Belegung, Runden), aus
   dem Transkript wie `belegung.py`.
2. Seite: `report_page.html`, `.css`, `.js` aus ArbiterMap kopiert, nicht neu gebaut; nur die
   Pfade auf `.git/arbiter/` umgestellt. Ein Skript bündelt sie zu `.git/arbiter/dashboard.html`
   (nicht in git). Reiter Backlog aus, bis ein Repo Items liefert (Antwort in Anliegen 22).
3. Scheiter-Test: Ein Lauf mit Transkript ergibt eine Zeile; die gebündelte Seite enthält sie.
4. Kritik am Code: Reviewer; dafür eine Zeile in der Tabelle des Ablaufs.

Budget und Sperre bleiben bei `belegung.py`; die Hooks `subagent_budget.py` und
`subagent_oversight.py` aus ArbiterMap übernimmt das Item nicht.

**F1 · Wann?** A: jetzt, vor Plan 2. B: als Prozess-Item der Retro 2, nach Review 2.
Empfehlung A: Retro 2 soll das Dashboard schon nutzen; du hast es angefordert.

Antwort: .

**F2 · Recht und Scope.** Der Regelumsetzer bekommt den Schreibpfad `prozess/dashboard/`. Du
aktivierst das Plugin A: mit Nutzer-Scope (jedes Repo, auch ArbiterMap mit eigenen Hooks),
B: mit Projekt-Scope (nur hier, `.claude/settings.json`). Empfehlung B: Erst hier erproben;
Nutzer-Scope, sobald es einen Zyklus lang trägt.

Antwort: .

**Stellungnahme.**
