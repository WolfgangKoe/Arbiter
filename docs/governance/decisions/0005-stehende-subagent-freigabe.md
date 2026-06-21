# 0005 — Stehende Freigabe für Subagenten-Einsatz

**Datum:** 2026-06-21
**Status:** angenommen

## Kontext

Bisher galt: Subagenten starten ist freigabepflichtig wie Code-Edits
([ADR-0001](0001-explizite-freigabe-beibehalten.md), `CLAUDE.md`). In der Praxis
musste der Orchestrator den Subagent-Einsatz **pro Fall** anfragen, obwohl die
Token-Disziplin (`CLAUDE.md`) Subagenten für mechanische Fleißarbeit ohnehin
**proaktiv** vorschreibt und Sonnet/Haiku deutlich günstiger als Opus sind. Die
Einzel-Freigabe war damit doppelte Reibung: Sie verlangsamte genau das Muster,
das die Effizienz heben soll, und zwang den Stakeholder, eine Erlaubnis zu
erteilen, die er ohnehin grundsätzlich wollte.

Der Stakeholder hat in der Retro ausdrücklich gesagt: Subagenten soll der
Orchestrator **grundsätzlich immer** einsetzen dürfen, wenn er es für angebracht
hält — selbst vorschlagen und starten, nicht nachfragen. Das geht schneller und
ist billiger.

## Entscheidung

**Subagenten = stehende Freigabe.** Der Orchestrator setzt Subagenten ohne
Einzel-Freigabe ein, wann immer angebracht — er schlägt sie proaktiv vor und
startet sie selbst. Die Tier-Wahl (Opus behält Design/Mehrdeutiges; Sonnet/Haiku
für Fleißarbeit/Lookups) bleibt sein Urteil.

Zwei Pflichten bleiben:

1. **Transparenz** — Auftrag + gewähltes Tier werden genannt, der Verbrauch wird
   getrennt ausgewiesen (Token-Report).
2. **Freigabe für datei-/einstellungsändernde Arbeit bleibt** — Code-, Memory-
   und Skill-Edits laufen weiter durchs Freigabe-Gate
   ([ADR-0001](0001-explizite-freigabe-beibehalten.md)), **auch wenn ein Subagent
   sie ausführt**. Die stehende Freigabe betrifft nur das *Starten* von
   Subagenten (Lesen/Recherche/Entwürfe), nicht das Schreiben in geschützte
   Artefakte.

Dies verengt ADR-0001 gezielt: Die Freigabe-Pflicht hängt am *Effekt* (Datei-
/Einstellungsänderung), nicht am *Werkzeug* (Subagent).

## Konsequenzen

- **Schneller / günstiger:** Fleißarbeit wandert ohne Verzögerung in den
  isolierten Sonnet-/Haiku-Kontext; das Opus-Hauptfenster bleibt schlank.
- **Klarere Grenze:** „Werkzeug vs. Effekt" — das Freigabe-Gate schützt weiterhin
  jede Datei-/Einstellungsänderung, egal wer sie auslöst.
- **Kein neuer Hook nötig:** Das bestehende `tools/freigabe_gate.py` (PreToolUse
  auf Edit/Write/NotebookEdit) bleibt die harte Schranke. Subagent-*Starts* sind
  bewusst nicht gegated — sie sind jetzt grundsätzlich erlaubt.

## Bekannte Lücke / Review-Termin

Ob der `freigabe_gate.py`-Hook auch **innerhalb** eines Subagent-Kontexts feuert
(also ob ein Subagent das Gate umgehen könnte), ist nicht verifiziert.
**Review-Termin nächste Retro:** Falls Subagent-Edits das Gate umgehen, braucht es
entweder einen Subagent-seitigen Vollzug oder die Regel „Subagenten dürfen keine
geschützten Artefakte schreiben, nur Entwürfe zurückliefern, die Opus freigibt".
