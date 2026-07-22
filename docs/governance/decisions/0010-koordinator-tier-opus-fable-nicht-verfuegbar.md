# 0010 — Koordinator-Tier auf Opus (Fable derzeit nicht verfügbar)

**Datum:** 2026-07-21
**Status:** angenommen

## Kontext

[ADR-0008](0008-fable-als-bevorzugter-koordinator.md) hatte den Koordinator-Sitz auf
**Fable präferiert, Opus als Fallback** festgelegt (Punkt 1) — Begründung: der
Koordinator ist per ADR-0007 *dünn* und *nicht delegierbar*, trägt die offensten
Programme (Gates, Entscheidungsmodi, Eskalation, Retro, Maßnahmen-Entscheid) und
verdient damit das höchste verfügbare Urteils-Tier.

**Prämissen-Änderung (S177):** Fable steht als Modell-Tier derzeit nicht zur
Verfügung. Der Koordinator-/Orchestrator-Sitz braucht dennoch ein persistentes,
nicht delegierbares Urteils-Tier für die Dauer jeder Session — der in ADR-0008
bereits vorgesehene Fallback-Fall (Punkt „Verfügbarkeits-Abhängigkeit" in den
Konsequenzen: „Ist Fable nicht verfügbar, arbeitet Opus als Koordinator ohne
Prozessänderung weiter") tritt damit ein. Diese Entscheidung dokumentiert den
Eintritt dieses Falls und macht ihn für nachfolgende Sessions durchsuchbar,
statt ihn nur stillschweigend im Fallback-Verhalten zu belassen.

Der *Planner*-Tier (Opus, [ADR-0009](0009-planner-tier-auf-opus.md)) ist von dieser
Prämissen-Änderung nicht betroffen — er stand bereits auf Opus und bleibt
unangetastet.

## Entscheidung

**Koordinator-Sitz = Opus**, solange Fable nicht verfügbar ist. Dies löst
**ADR-0008 Punkt 1** (Koordinator-Tier) insoweit ab, als die Präferenz-Reihenfolge
„Fable präferiert, Opus als Fallback" durch „Opus" ersetzt wird, bis Fable wieder
verfügbar ist. Der **Rest von ADR-0008 bleibt gültig**, insbesondere:

- Punkt 2 (Prämissen-/Verfassungsänderungen und Konsens-Entscheidungen laufen im
  Koordinator-Sitz — dieser ist nun Opus statt Fable),
- Punkt 3 (Reviewer: Opus bleibt Default; Fable-Ausnahme bei
  Prämissen-/Architektur-Urteil entfällt faktisch, solange Fable nicht verfügbar
  ist — keine inhaltliche Änderung der Regel selbst),
- Punkt 4 (Planner: Opus bleibt — unverändert, siehe ADR-0009),
- Punkt 5 (Executor/Recherche/Beobachter/Artefaktpflege: unverändert Sonnet/Haiku).

ADR-0008 wird **nicht inhaltlich umgeschrieben** (Append-only-Prinzip) — es bleibt
als Historie stehen und erhält lediglich einen Status-Verweis auf diese ADR.

## Konsequenzen

- **Keine Prozessänderung am Koordinator-Zuschnitt:** dünn, persistent, nicht
  delegierbar — nur das Modell-Tier ändert sich von Fable auf Opus, exakt wie in
  ADR-0008 als Fallback-Verhalten vorgesehen.
- **`operating_model.md`** wird an allen Koordinator-Tier-Stellen (Status-Block,
  Rollen-Tabelle, Tiering-Tabelle, Diagramme) auf Opus angeglichen, mit Verweis auf
  diese ADR.
- **Review-Trigger:** Sobald Fable wieder verfügbar wird, ist diese Entscheidung
  erneut zu prüfen — ADR-0008 bleibt die Grundsatzentscheidung für den
  Fable-präferiert-Fall und muss dann nicht neu verhandelt werden, nur die
  Verfügbarkeits-Prämisse ändert sich zurück.
- **Kein Einfluss auf den Planner-Tier** (ADR-0009) oder auf Executor-/
  Recherche-/Beobachter-Tiering — diese Entscheidung ist auf den Koordinator-Sitz
  begrenzt.

## Review-Termin

Sobald Fable als Modell-Tier wieder verfügbar ist — dann Prüfung, ob der
Koordinator-Sitz gemäß ADR-0008 zu Fable zurückkehrt.
