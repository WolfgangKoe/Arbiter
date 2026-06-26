# Plan 027 — Doku-Org-Alignment (ADR-0007 dünner Koordinator)

> **Executor-Anweisung:** Plan vollständig lesen, jeden Verify-Befehl ausführen,
> Ergebnis bestätigen bevor der nächste Step beginnt. STOP-Bedingungen sind ernst.
> Kein Produktivcode anfassen — dieser Plan ändert ausschließlich Doku-Dateien.
>
> **Drift-Check (zuerst ausführen):**
> `grep -n "120k\|≥120k\|>120k" .claude/tasks/next_session.md CLAUDE.md docs/governance/operating_model.md`
> Erwartet: Treffer in CLAUDE.md (`≥120k ⚠️`). Dieser Wert wird in Plan 028
> Step 1 korrigiert (O3) — hier nur dokumentieren, nicht anpassen.
>
> `grep -n "Pilot\|pilot" docs/governance/operating_model.md docs/governance/decisions/0007-*.md`
> Erwartet: „Pilot"-Vorbehalt in operating_model.md Einleitung + ADR-0007.
> Wenn operating_model.md keinen „Pilot"-Vorbehalt mehr enthält → STOP, melden.

## Status

- **Priority**: P2 (MITTEL) — Doku-Klarheit, kein Feature-Block
- **Effort**: S–M (5 Doku-Dateien, kein Produktivcode)
- **Risk**: NIEDRIG — reine Doku; kein Code-Gate, aber next_session.md-Zeilen-Gate
- **Depends on**: —
- **Category**: Doku-Alignment (O1, S103)

## Why this matters

`next_session.md`, `CLAUDE.md` und `operating_model.md` sind die drei Dateien, die
jede Session direkt lesen. Nach ADR-0007 (S101) und dem Mailbox-Pilot (S102) haben
sich Arbeitsweise und Kommunikationswege real verändert — die Texte beschreiben aber
noch Übergangs- oder Pilot-Zustände. Das erzeugt Drift: ein Executor-Subagent liest
einen Auftrag, der auf ein Muster zeigt, das nicht mehr gilt. Außerdem fehlen in
`agent_scopes.md` die Reporting-/Token-Tooling-Aufgaben als eigenständiger Scope-Typ.

## Scope (betroffene Dateien)

- `.claude/tasks/next_session.md` — Session-Regeln auf ADR-0007 aktualisieren;
  **Zeilen-Gate ≤ 120 beachten** (Test `tests/docs/` schlägt darüber an).
- `CLAUDE.md` — Carry-over-Vermerke (ADR-0006-Verweis) sauber; Schwellen-
  Inkonsistenz mit Plan 028 Step 1 koordinieren.
- `docs/governance/operating_model.md` — „Pilot"-Vorbehalt (Einleitung + Diagramme
  A/B) streichen, sobald Mailbox-Pilot bestätigt; Diagramme A/B nachziehen.
- `docs/reference/agent_scopes.md` — Eintrag für Aufgabentyp „Reporting / Token-
  Tooling" ergänzen; bestehende Scope-Tabelle nachführen.
- `docs/governance/decisions/0007-duenner-koordinator-und-datei-kanal.md` (ADR-0007)
  — „Bekannte Lücke / Review-Termin"-Block auf „bestätigt" aktualisieren.

## Steps (je Step = eigener Freigabe-Punkt)

### Step 1 — operating_model.md: Pilot-Vorbehalt streichen + Diagramme nachziehen (XS)

**Voraussetzung:** Mailbox-Pilot ist real gelaufen (S102 bestätigt: NEEDS-DECISION →
ANSWERED in `docs/handoff/` verifiziert). Wenn nicht → STOP, Stakeholder fragen.

Änderungen:
- Einleitungs-Kasten (Status-Zeile): Status `**Status — im Übergang (ADR-0007, Pilot)**`
  auf `**Status — verbindlich (ADR-0007, seit S102)**` aktualisieren; Satzteil
  „verbindlich wird die Mailbox erst nach dem Pilot-Round-Trip" entfernen.
- Diagramm A (Aufbauorganisation): Reviewer-Knoten auf `Reviewer (Opus-Subagent)`
  aktualisieren; Planner-Knoten ergänzen (`PL[Planner\nOpus-Subagent]`).
  ASCII-Fallback entsprechend anpassen.
- Diagramm B (Ablauforganisation): `5 · Review→Retro→Abschluss` auf
  `5 · Review (Reviewer-SA)→Retro→Abschluss` aktualisieren.

**Querverweise:** Nur Abschnitts-Anker (`#aufbauorganisation-rollen--model-tier`,
`#diagramm-a`), keine Zeilennummern.

**Verify:** `grep -n "Pilot\|im Übergang" docs/governance/operating_model.md`
→ kein Treffer mehr in der Einleitung; ADR-0007-Verweis darf bleiben.

### Step 2 — ADR-0007: Bekannte Lücke auf bestätigt setzen (XS)

Im Abschnitt `## Bekannte Lücke / Review-Termin`:
- Ersten Bullet (Harness-Fakten ungeprüft): ergänzen
  `→ Pilot S102 durchgelaufen (NEEDS-DECISION→ANSWERED in docs/handoff/ verifiziert).`
- Zweiten Bullet (wortgleiches Durchreichen): ergänzen
  `→ S102-Retro: kein Befund.`

**Querverweise:** Stable Anker `#bekannte-lücke--review-termin`.

**Verify:** `grep -n "Bekannte Lücke\|Pilot S102" docs/governance/decisions/0007-*.md`
→ Pilot-Eintrag vorhanden.

### Step 3 — next_session.md: Session-Regeln auf ADR-0007 bringen (S)

Zeilen-Gate: die Datei hat aktuell ~96 Zeilen; das Gate liegt bei 120. Beim Bearbeiten
auf ≤ 120 achten; falls nötig Erledigtes nach `session_archive.md`/`backlog.md` auslagern.

Konkrete Änderungen (Abschnitt `## ⚠️ Session-Regeln`):
- Verweis auf `docs/governance/operating_model.md` für Rollen/Tier um expliziten
  Hinweis ergänzen: „Koordinator routet — liest keine Quelldateien/Vollergebnisse;
  Detail-Planung → Planner-Subagent; finales Review → Reviewer-Subagent (ADR-0007)."
- `agent_scopes.md` als Pflichtlektüre für Subagent-Briefing nennen
  (neben `operating_model.md`).
- Den KOORDINATOR-DELEGIERT-MEHR-Block komprimieren — Kernbotschaft
  behalten, Details nach `operating_model.md` verweisen (Abschnitt
  `#ablauforganisation-events`).

**Querverweise:** Abschnitts-Anker `#session-regeln`, `#was-ist-arbiter`,
keine Zeilennummern.

**Verify:**
`wc -l .claude/tasks/next_session.md` → ≤ 120.
`pytest tests/docs/ --no-cov -q` → grün (Zeilen-Gate).

### Step 4 — CLAUDE.md: Carry-over-Vermerke nachziehen (XS)

- Abschnitt `Token-Disziplin & Arbeitsweise`: Schwellen-Text `≥120k ⚠️` auf
  `≥135k ⚠️` aktualisieren (koordiniert mit Plan 028 Step 1 — erst nach dessen
  Freigabe ausführen oder in einem Zug). Wenn Plan 028 Step 1 bereits erledigt:
  nur prüfen, ob CLAUDE.md konsistent ist.
- `ADR-0006`-Verweis: Im Abschnitt `Token-Disziplin` den Satz
  „Subagenten = stehende Freigabe (ADR-0005)" um `ADR-0006`
  (Subagent-Großausgaben als Datei) ergänzen.
- Abschnitt `Tiering` bereits konform (O2-MUST eingebaut); keine Änderung nötig.

**Querverweise:** Abschnitte `#token-disziplin--arbeitsweise` und
`#kontext-korridor`.

**Verify:** `grep -n "≥120k\|>=120k" CLAUDE.md` → kein Treffer nach dem Fix.

### Step 5 — agent_scopes.md: Reporting/Token-Tooling ergänzen (XS)

Neue Zeile in der Scope-Tabelle:

| Aufgabentyp | Pflicht-Lesen | Optional |
|---|---|---|
| **Reporting / Token-Tooling** (`token_report.py`, `session_context.py`, Schwellen) | `tools/token_report.py`, `tools/session_context.py`, `docs/metrics/overview.md`, `tests/tools/test_token_report.py` | `docs/metrics/session_archive.json`, `docs/metrics/session_archive.md` |

**Verify:** `grep -n "Reporting\|token_report" docs/reference/agent_scopes.md`
→ neuer Eintrag vorhanden.

### Step 6 — Abschluss + README

- Statuszeile in `docs/audit/plans/README.md` auf DONE setzen (nach allen Steps).
- `next_session.md` Carry-over-Punkt O1 als erledigt markieren (oder entfernen).

**Verify:**
`grep -n "027" docs/audit/plans/README.md` → Status DONE.
`wc -l .claude/tasks/next_session.md` → ≤ 120.
Volltest: `pytest tests/docs/ --no-cov -q` → grün.

## Test plan

- `pytest tests/docs/ --no-cov -q` nach Step 3 und Step 6 — prüft next_session.md-Gate.
- Kein Coverage-Gate nötig (reine Doku, kein Produktivcode).
- Manuelle Sichtprüfung der drei Hauptdateien nach Step 6.

## Done criteria

- [ ] operating_model.md: kein „Pilot"-Vorbehalt mehr in Einleitung; Diagramme A/B
      zeigen Reviewer + Planner als Subagenten.
- [ ] ADR-0007: Bekannte-Lücke-Block trägt Pilot-S102-Bestätigung.
- [ ] next_session.md: ADR-0007-Arbeitsweise explizit; agent_scopes.md als Pflichtlektüre
      genannt; Zeilen-Gate ≤ 120; tests/docs/ grün.
- [ ] CLAUDE.md: keine Schwellen-Inkonsistenz mehr (nach Plan 028 Step 1); ADR-0006-Verweis.
- [ ] agent_scopes.md: Reporting/Token-Tooling-Scope-Zeile vorhanden.
- [ ] README: Status DONE, Datum.

## STOP conditions

- next_session.md wird durch Änderungen > 120 Zeilen → tief auf ≤ 70 kürzen,
  Erledigtes nach session_archive/backlog auslagern, erst dann fortfahren.
- Mailbox-Pilot S102 ist nicht verifiziert → Step 1 nicht ausführen, Stakeholder fragen.
- Ein Querverweis verweist auf eine Zeilennummer statt auf einen Abschnitts-Anker →
  STOP, Anker-Form wählen.
