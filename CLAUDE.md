# CLAUDE.md — Workflow & Core Principles

## Workflow Orchestration

### Plan Mode Default
- Enter plan mode for **ANY** non-trivial task (3+ steps or architectural decisions)
- If something goes sideways, **STOP** and re-plan immediately
- Use plan mode for verification steps, not just building
- Write detailed specs upfront to reduce ambiguity

### Subagent Strategy
- Use subagents liberally to keep main context window clean
- Offload research, exploration, and parallel analysis to subagents
- For complex problems, throw more compute at it via subagents
- One task per agent for focused execution

### Self-Improvement Loop
- Use the established MCP memory to internalize user corrections and patterns
- Prevent the same mistake by referencing past session data
- Ruthlessly iterate on execution until mistake rate drops

### Verification Before Done
- Never mark a task complete without proving it works
- Diff behavior between main and your changes when relevant
- Ask yourself: *"Would a staff engineer approve this?"*
- Run tests, check logs, demonstrate correctness

### Demand Elegance (Balanced)
- For non-trivial changes: pause and ask *"is there a more elegant way?"*
- If a fix feels hacky: *"Knowing everything I know now, implement the elegant solution"*
- Skip this for simple, obvious fixes — don't over-engineer
- Challenge your own work before presenting it

### Autonomous Bug Fixing
- When given a bug report: just fix it. Don't ask for hand-holding
- Point at logs, errors, failing tests — then resolve them
- Zero context switching required from the user
- Go fix failing CI tests without being told how

### Task Management

| Step | Action |
|------|--------|
| **Plan First** | Write plan to `.claude/tasks/todo.md` with checkable items |
| **Verify Plan** | Check in before starting implementation |
| **Track Progress** | Mark items complete as you go |
| **Explain Changes** | High-level summary at each step |
| **Document Results** | Add review section to `.claude/tasks/todo.md` |

### Branch-Strategie
- **`main`** — stabiler Stand, nur per Pull Request von `dev`
- **`dev`** — aktiver Entwicklungszweig, hier wird gearbeitet
- Neue Features immer auf `dev` entwickeln
- Kein direktes Committen auf `main`
- Merge nach `main` nur wenn alle Tests grün sind

### Commit-Erinnerungen
- Nach jeder abgeschlossenen, in sich sinnvollen Änderung aktiv auf einen Commit-Punkt hinweisen
- Gute Commit-Punkte: neue Feature fertiggestellt, Bug behoben, Refactoring abgeschlossen, Konfiguration geändert
- Commit-Nachricht: kurz, imperativ, auf Englisch (`Add shooting phase UI`, `Fix slider crash for single-model units`)
- Kein Commit mitten in einer halbfertigen Änderung

---

## Clean Code

### Lesbarkeit
- Bedeutungsvolle Namen für Variablen, Funktionen und Klassen — der Name erklärt das *Was*, ein Kommentar höchstens das *Warum*
- Funktionen tun **genau eine Sache** (Single Responsibility Principle)
- Keine magischen Zahlen oder Strings — stattdessen benannte Konstanten (`MAX_CHARGE_DISTANCE = 12`)
- Kein tiefes Verschachteln — Early Returns bevorzugen
- DRY: Wiederholungen → Abstraktion; aber erst ab der **dritten** Wiederholung
- Boy Scout Rule: Code sauberer hinterlassen als vorgefunden

### Typsicherheit & Stil
- **Type Hints** überall (`def roll(n: int) -> list[int]`)
- `mypy` für statische Typprüfung
- Formatter: `black` + `isort` (nicht diskutieren, automatisch durchsetzen)
- Linter: `ruff` (ersetzt flake8/pylint)

### Automatisierung
- **Pre-commit Hooks**: Formatter, Linter und Typprüfung laufen vor jedem Commit
- **CI/CD**: alle Tests und Qualitätschecks bei jedem Push automatisch
- Kein Merge ohne grüne Pipeline

---

## Testing

### Teststrategie

| Testart | Zweck | Anteil |
|---------|-------|--------|
| **Unit-Tests** | Einzelne Funktionen/Klassen isoliert | ~70 % |
| **Integrations-Tests** | Zusammenspiel mehrerer Komponenten | ~20 % |
| **E2E-Tests** | Vollständiger Benutzerfluss | ~10 % |

### Regeln
- **Coverage-Schwelle: 80 %** — darunter wird der Build rot
- **Keine geteilten Zustände** zwischen Tests — jeder Test ist vollständig isoliert
- **Testnamen beschreiben Verhalten**, nicht Implementierung:
  `test_overlord_resurrection_orb_heals_destroyed_warrior` ✓ — `test_orb` ✗
- **Regression-Tests**: Jeder Bugfix bekommt einen Test, der genau diesen Bug abdeckt
- **Mocking-Strategie**: Externe Abhängigkeiten (DB, API, Dateisystem) werden gemockt — interne Logik nicht
- **Performance-Tests**: dort wo Skalierung relevant ist (z.B. Massenberechnungen)

### Pflicht bei Flask-Erweiterungen
- **Jede** neue Route, jedes neue Domain-Modell und jede neue Service-Funktion bekommt sofort Tests
- Eine Erweiterung der Flask-App gilt erst als fertig, wenn die zugehörigen Tests grün sind
- Struktur: `tests/domain/` für Modelle & Services, `tests/adapters/web/` für Routen

### Ablauf
1. Test schreiben (TDD bevorzugt, aber nicht erzwungen)
2. Test rot laufen lassen
3. Minimale Implementierung, die den Test grün macht
4. Refactoren — Test bleibt grün

---

## Core Principles

| Principle | Description |
|-----------|-------------|
| **Simplicity First** | Make every change as simple as possible. Impact minimal code. |
| **No Laziness** | Find root causes. No temporary fixes. Senior developer standards. |
| **Minimal Impact** | Only touch what's necessary. No side effects with new bugs. |
| **No Placeholders — Ever** | Never write `...`, `TODO`, `<value>`, or any placeholder in config files, snippets, or any file the user will deploy or paste directly. Always write the complete, real value. A placeholder in a config file is a production incident waiting to happen. |
