# 0004 — Skill-/Claude-Inhalte über die API nur per Subagent ziehen

**Datum:** 2026-06-20
**Status:** angenommen

## Kontext

In einer Session wurden Skill-/Claude-Inhalte **über die API direkt im
Opus-Hauptfenster** geladen. Das kostete einmalig **~300k Token** und flutete
den Kontext unnötig — weit jenseits des Korridors (<150k, Wind-down ~135k). Die
Wurzel: ein Skill-Fetch ist mechanische Fleißarbeit (viel hereinströmender
Inhalt, kein Urteil), gehört also nach der bestehenden Token-Disziplin in einen
**isolierten Kontext** — wurde aber als Sonderfall nirgends festgehalten und ist
deshalb wiederholbar gefährlich.

Der Stakeholder hat das als wichtige, jederzeit wieder relevant werdende
Entscheidung benannt und um amnesie-feste Dokumentation gebeten.

## Entscheidung

Skill-Definitionen oder andere Inhalte über die Claude-/Skill-API werden **nie
direkt im Opus-Hauptfenster** geladen. Stattdessen macht ein **Subagent** den
Fetch im isolierten Kontext und gibt nur das **Ergebnis** (das benötigte Extrakt)
zurück. Dies ist eine konkrete Anwendung des bestehenden „Fleißarbeit →
Subagent"-Musters (Prämisse 3, Token-Disziplin) auf einen besonders teuren Fall.

## Konsequenzen

- **Günstiger / sicherer:** Der Opus-Hauptkontext bleibt schlank; ein einzelner
  Fetch kann das Fenster nicht mehr um Hunderttausende Token aufblähen.
- **Etwas mehr Reibung:** Auch ein „mal eben" benötigter Skill-Inhalt erfordert
  den Subagenten-Umweg statt direkten Zugriffs.
- **Vollzug bleibt Urteil, nicht Hook:** Wie das Subagent-Routing generell (ADR-0003)
  ist auch dies nicht hart automatisierbar — es lebt als Regel in `CLAUDE.md`
  (Token-Disziplin) und im Memory, nicht als PreToolUse-Block.

## Review-Termin

Nächste Retrospektive — Frage: Reicht die Regel als Erinnerung, oder braucht der
Skill-Fetch (wie das Freigabe-Gate) einen härteren Vollzug?
