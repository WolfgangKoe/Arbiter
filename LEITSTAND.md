# 🎛️ Leitstand — Arbiter

Die eine Tür für den Stakeholder. Hier ist der Rahmen sichtbar; alle Inhalte liegen in ihren kanonischen Artefakten (hier nur verlinkt). Nichts steht doppelt — Duplikate erzeugen Drift.

---

## 1 · Prämissen / Leitplanken

| Artefakt | Was es ist |
|---|---|
| [CLAUDE.md](CLAUDE.md) | Projekt-Verfassung: Kultur, Workflow-Regeln, Clean Code, Testing — gilt repo-weit und ist nicht pro Task verhandelbar |
| [docs/governance/operating_model.md](docs/governance/operating_model.md) | Aufbau- und Ablauforganisation: Rollen, Model-Tier, Events, Entscheidungsmodi, Eskalationswege — iterierbar wie Code |
| [docs/spec/architecture_invariants.md](docs/spec/architecture_invariants.md) | Vier messbare Architektur-Invarianten mit Schulden-Ledger; Wächter laufen automatisch in `pytest` |

---

## 2 · Aktueller Stand

→ [.claude/tasks/next_session.md](.claude/tasks/next_session.md)

Dort steht: was zuletzt getan wurde, was als nächstes ansteht, offene Fragen. Wird am Session-Ende aktualisiert.

---

## 3 · Backlog & Ziele

| Artefakt | Was es ist |
|---|---|
| [docs/goals/backlog.md](docs/goals/backlog.md) | Zentraler Backlog — die einzige Stelle für priorisierte offene Aufgaben |
| [docs/goals/](docs/goals/) | Aktive Zieldateien (ziel6.md … ziel8.md) mit Checkboxen und Detailstatus; erledigte Ziele unter `archive/` |

---

## 4 · Konditionalprogramme (Status)

Die Gates laufen automatisch — sie entscheiden nicht, sie beschränken.

**Messung immer so:**
```bash
pytest --tb=short
```

Das schließt ein:
- **Coverage-Gate** ≥ 92 % (Konfiguration in `pyproject.toml`; Render-Code ausgeschlossen — siehe [CLAUDE.md](CLAUDE.md))
- **Architektur-Gate** — vier Invarianten in `tests/architecture/`; Details + Schulden-Ledger: [docs/spec/architecture_invariants.md](docs/spec/architecture_invariants.md)
- **Debt-Scoreboard** — läuft bei jedem `pytest`-Lauf mit; zählt offene Regel-Schulden aus dem Rule-Conformance-Catalog

**Bericht (kein Gate):** [Token-Report / Wer leistete was](docs/metrics/overview.md) — Haupt- vs. Subagent-Verbrauch je Modell-Tier und Session. Aktualisieren: `python tools/token_report.py --write`.

---

## 5 · Ideen-Eingang (Refinement)

| Ort | Rolle |
|---|---|
| [Fotos/](Fotos/) | Roher Einwurf — Bilder, Skizzen, Fotos von Notizen; unstrukturiert |
| [docs/inbox/](docs/inbox/) | Aufbereiteter Eingang — Ideen als strukturierter Text, bereit für Refinement |

Ablauf: Fotos/ → Subagent extrahiert Idee als Text nach docs/inbox/ → Refinement-Event mit Stakeholder → akzeptierte Ideen wandern in [docs/goals/backlog.md](docs/goals/backlog.md). Details: [docs/inbox/README.md](docs/inbox/README.md).

---

## 6 · Entscheidungslog

→ [docs/governance/decisions/](docs/governance/decisions/)

Konsens-Entscheidungen (Scope, Architektur-Richtung, Prämissen-Änderungen) werden dort als ADR dokumentiert — warum, nicht nur was.
