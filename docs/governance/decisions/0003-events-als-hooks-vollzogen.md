# 0003 — Operating-Model-Events werden von der Harness vollzogen, nicht erinnert

**Datum:** 2026-06-19
**Status:** angenommen

## Kontext

Das Operating Model beschreibt Events (Kontext-Korridor-Wind-down, Token-Report
im Review, Freigabe-Gate, Subagent-Routing). Diese Events waren bisher **Prosa**
in Markdown: Sie „feuern" nur, wenn der Orchestrator die Regel pro Session liest
und sich daran erinnert. Der Agent existiert zwischen Sessions nicht — Erinnern
ist damit kein verlässlicher Auslöser, sondern Hoffnung.

Der Stakeholder hat das benannt: alle vier Mechaniken „feuern gar nicht von
selbst". Die Wurzel ist strukturell — eine Verfassung ohne Vollzugsorgan. Echte
Trigger laufen in diesem Projekt nur über die **Harness** (Hooks in
`.claude/settings.json`), nicht über den guten Willen des Modells.

## Entscheidung

Wo ein Event als Konditionalprogramm formulierbar ist, wird sein Vollzug aus der
Prosa in die **Harness** verlagert:

1. **Kontext-Korridor-Event** — `tools/session_context.py` eskaliert gestuft
   (≥120k Warnung mit Retro-Vorankündigung, ≥135k laute Stopp-Direktive) statt
   einer neutralen Zeile.
2. **Token-Report im Review** — `tools/test_report_reminder.py` (PostToolUse auf
   pytest) injiziert nach jedem Testlauf die Pflicht, Peak/Korridor im Chat zu
   teilen.
3. **Freigabe-Gate** — `tools/freigabe_gate.py` (PreToolUse auf
   Edit/Write/NotebookEdit) **blockiert hart**, solange der Marker
   `.claude/.freigabe` fehlt. Freigabe ist ein **physischer** Akt des
   Stakeholders (`touch .claude/.freigabe`); ein SessionStart-Hook entfernt den
   Marker, sodass das Gate jede Session neu scharf ist. Ein PreToolUse-Hook kann
   ein „ja" im Chat nicht lesen — deshalb der Marker statt Intent-Parsing.

**Bewusst NICHT automatisiert:** Subagent-Routing bleibt ein Urteil
(„ist das Fleißarbeit?"), kein Konditionalprogramm — kein Hook kann das
entscheiden. Es bleibt Orchestrator-Verantwortung plus Reminder. Hier ehrlich
keine Scheinsicherheit bauen.

## Konsequenzen

- **Verlässlicher:** Die drei automatisierten Events feuern unabhängig vom
  Gedächtnis des Modells — der Hauptzweck dieser Änderung.
- **Reibung beim Freigabe-Gate:** Der harte Block bremst auch legitime Arbeit,
  bis der Stakeholder den Marker setzt — bewusst gewählt (er hat den harten Block
  dem weichen Reminder vorgezogen). Bekannte Lücke: Datei-Writes via Bash
  (`>`, `sed -i`) sind nicht gegated; alle Bash zu gaten würde Reads und pytest
  blockieren.
- **Prämissen-Schärfung:** Dies betrifft Prämisse 2 (Ablauforganisation/Vollzug).
  Die Events-Tabelle in `operating_model.md` markiert nun, welche Events
  Hook-vollzogen sind.

## Review-Termin

Nächste Retrospektive — Frage: Ist die Freigabe-Gate-Reibung (Marker pro Session)
im Verhältnis zum Gewinn an Verlässlichkeit tragbar, oder lockern wir auf einen
weichen Reminder?
