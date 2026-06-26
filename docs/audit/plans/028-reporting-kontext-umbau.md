# Plan 028 — Reporting- und Kontext-Umbau (O3–O7)

> **Executor-Anweisung:** Plan vollständig lesen. Jeden Step als isolierte Einheit
> behandeln; nach jedem Step Vollsuite + Lint. STOP-Bedingungen sind bindend.
> Kein Spielcode anfassen (kein `src/`, kein `data/`).
>
> **Drift-Check (zuerst ausführen):**
> `grep -n "WARN_THRESHOLD\|STOP_THRESHOLD\|120_000\|135_000" tools/session_context.py`
> Erwartet: eine Warn-Schwelle bei 120k, eine Stopp-Schwelle bei 135k (Namen ggf. anders).
> Wenn die Warn-Schwelle bereits 135k ist → Step 1 entfällt, melden.
>
> `grep -n "merge_session_into_archive\|archive\|peak_context" tools/token_report.py`
> Erwartet: Archiv-Merge-Logik vorhanden (Plan 023 DONE). Wenn die Merge-Funktion
> fehlt → STOP, unbekannte Drift melden.

## Status

- **Priority**: P1 (HOCH) — Überschreib-Bug (O4) kostet Daten; Schwellen-Fix (O3) XS
- **Effort**: M (fünf getrennte Aufgaben, O4 + O6 sind die größten)
- **Risk**: MEDIUM — O4 ändert Archiv-Schreib-Logik (bestehende Tests vorhanden)
- **Depends on**: Plan 023 ✅ (Archiv-Infrastruktur vorhanden)
- **Category**: Tooling-Bugfix + Feature (O4 Regressionstest, O6 neue Kontext-Sicht)

## Why this matters

Fünf Entscheidungen aus S103 betreffen das Reporting- und Kontext-Tooling:
- **O3** (XS): Warnschwelle im Live-Hook zu früh — Retro-Vorankündigung stört bei 120k,
  wo noch viel Headroom ist. Korrektur: erst >135k warnen.
- **O4** (M): `--write` überschreibt korrekte Archiv-Einträge mit veralteten Transcript-
  Daten. User-Wunsch: Echtzeit-Updates bei Subagent-Start/-Ende, nicht weniger.
- **O5** (XS): Der Koordinator (Opus-Hauptthread) taucht im Modellmix auf — er soll nur
  Subagenten zählen.
- **O6** (M): Neue Kontext-Sicht „womit ist MEIN Fenster gefüllt" (nach Quelle), orientiert
  an der Peter-Wegner-Präsentation (`context-engineering-slides.md`).
- **O7** (S): Planning-Darstellung klarer/lesbarer (Subagent bleibt zuständig).

## Scope (betroffene Dateien)

- `tools/session_context.py` — O3 (Schwellen)
- `tools/token_report.py` — O4 (Archiv-Überschreib-Bug), O5 (Modellmix-Filter),
  O6 (neue Kontext-Quellenansicht), O7 (Planning-Ausgabe-Format)
- `tests/tools/test_token_report.py` — O4 Regressionstest, O6 Tests
- `tests/tools/test_session_context.py` — O3 Schwellen-Test
- `docs/metrics/overview.md` — wird via `--write` neu generiert (kein Handgriff)
- `docs/reference/agent_scopes.md` — O7 Planning-Template (alternativ operating_model.md)
- `CLAUDE.md` — O3-Konsistenz-Fix (Schwellen-Text, koordiniert mit Plan 027 Step 4)

## Steps

### Step 1 — O3: Warnschwelle 120k → 135k in session_context.py (XS)

**Ziel:** `⚠️`-Warnung erscheint erst >135k; <135k zeigt nur neutralen Gauge.
STOP kommt weiterhin bei ≥135k (unverändertes Stopp-Verhalten).

Änderungen in `tools/session_context.py`:
- Warn-Schwelle 120k → 135k.
- Docstring-/Kommentarzeilen mit `120k` auf `135k` aktualisieren.
- Neutral-Nachricht („corridor <150k; wind-down ~135k") bleibt; sie darf jetzt bis
  135k erscheinen.

Test-Migration (Sicherheitsnetz):
`grep -rn "120_000\|120k\|WARN" tests/tools/test_session_context.py`
→ alle Treffer migrieren: Schwellen-Tests auf 135k prüfen (nicht 120k). Diese
Migration ist erwartet — kein STOP.

**Verify:**
`pytest tests/tools/test_session_context.py -q` → grün.
Manuell: 120k → neutraler Text (kein ⚠️); 135k → ⚠️-Text.

Danach CLAUDE.md-Verweis `≥120k ⚠️` auf `≥135k ⚠️` anpassen (koordiniert mit
Plan 027 Step 4 — Steps zusammenführen, wenn beide in derselben Session laufen).

### Step 2 — O4: Archiv-Überschreib-Bug finden + fixen + Regressionstest (M)

**Root-Cause-Analyse (vom Planner skizziert, vom Executor verifizieren):**

Die Archiv-Merge-Funktion macht einen Upsert für jede Session, die `collect_project`
aus dem Transcript-Verzeichnis liest. Problem: Wenn Transcripts fehlen (nach Rotation,
nach Session-Ende) oder ein `--write`-Lauf aus einem anderen cwd mit anderem Transcript-
Set kommt, überschreibt der Upsert korrekte Archiv-Einträge mit veralteten oder Null-
Werten. **Erst durch Lesen des Codes bestätigen, bevor gefixt wird.**

**Step 2a — Überschreib-Bug fixen:**

Bevorzugte Strategie: **peak_context-basiertes Überschreiben** — beim Upsert nur
schreiben, wenn die Session neu ist ODER der neue `peak_context` größer ist als der
bestehende (vollständigere Transcript-Daten gewinnen, fragmentierte verlieren). Skizze:

```python
existing = archive.get(session_id)
new_peak = session_summ.peak_context if session_summ else None
if existing is None or (new_peak and new_peak > (existing.get("peak_context") or 0)):
    archive = merge_session_into_archive(...)
```

Alternative „never overwrite existing" (nur neue Sessions hinzufügen) ist einfacher,
verhindert aber jedes Nachführen — daher nur Fallback. Der Executor wählt nach
Code-Lage; Begründung im Abschlussbericht.

**Step 2b — Echtzeit-Updates bei Subagent-Start/-Ende (Feature-Scope, blockiert):**

O4 nennt: „User will eher MEHR/Echtzeit-Updates (bei Subagent-Start/-Ende)." Optionen:
- **Option A:** neuer `PostToolUse`-Hook (harness-seitig) schreibt Partial-Einträge.
- **Option B:** Koordinator ruft `--write` nach jedem Subagent-Ende auf (kein neuer
  Hook; der Bug-Fix aus 2a macht das gefahrlos).

**`NEEDS-DECISION` (Koordinator/Stakeholder):** Option A vs. B entscheiden, da A einen
neuen Hook braucht. Step 2a ist davon **unabhängig** und sofort umsetzbar. Step 2b
nicht ohne Entscheid implementieren.

**Regressionstest (PFLICHT)** in `tests/tools/test_token_report.py`:

| Test | Prüft |
|------|-------|
| `test_merge_does_not_overwrite_higher_existing_peak` | Archiv `peak=131k`, neuer Lauf `peak=80k` → bleibt 131k |
| `test_merge_overwrites_when_new_peak_is_higher` | Archiv `peak=50k`, neuer Lauf `peak=131k` → 131k gewinnt |
| `test_merge_adds_new_session` | Neue Session (nicht im Archiv) wird hinzugefügt |

**Verify:**
`pytest tests/tools/test_token_report.py -q` → grün inkl. neue Tests.
`python tools/token_report.py --write` → overview.md aktuell, kein Datenverlust.

### Step 3 — O5: Koordinator aus Modellmix heraushalten (XS)

**Problem:** Der Modellmix-Balken (`model_mix_bar`) liest den gemischten `by_tier`
(Haupt + Subagenten); der Koordinator-Tier (Opus-Hauptthread) erscheint dadurch im Mix.

**Fix:** Den Modellmix-Balken im Verlaufsblock und im Fokus-Block auf
**Subagenten-Tiers** umstellen (`sub_by_tier` o. ä.). Die informative Zeile
„Modelle: Haupt X · Subagent Y" bleibt; nur der **Mix-Balken** zeigt künftig
ausschließlich Subagenten. Legende anpassen: „Modell-Mix (Subagenten)".

**Verify:**
`grep -n "model_mix_bar" tools/token_report.py` → alle Aufrufe nutzen Subagenten-Tiers.
`pytest tests/tools/test_token_report.py -q` → grün. Test
`test_mix_bar_uses_subagent_tiers_only` ergänzen.

### Step 4 — O6: Neue Kontext-Sicht „nach Quelle" (M)

**Konzept (ausgerichtet an `context-engineering-slides.md`, Abschnitt „Messen zuerst:
/context"):** Der Slide schlüsselt das Fenster nach System-Prompt, Tool-Defs + MCP,
Memory-Dateien, Verlauf inkl. Tool-Ergebnissen auf. Wir übersetzen das in Quellen, die
**aus dem Transcript-Usage rekonstruierbar** sind (Approximation, klar benannt):

| Quelle | Approximation |
|--------|---------------|
| **Warm (System/Memory/History)** | `cache_read_input_tokens` |
| **Neu gecacht (Tool-Ausgaben/Docs)** | `cache_creation_input_tokens` |
| **Ungecacht (Konversation/neue Inhalte)** | `input_tokens` |
| **Generiert** | `output_tokens` |

**Wichtig:** Exakte Per-Quelle-Aufschlüsselung gibt das Transcript nicht her — die Sicht
ist eine **Approximation** und muss als solche beschriftet sein.

Neuer Renderer `_render_context_sources(session) -> list[str]`:
- Überschrift: `## Kontext-Zusammensetzung (nach Quelle, approximiert)`
- 4 Balken analog `_render_composition`, mit obigen Labels.
- Legende: Bezug zu den Slide-Kategorien; `approximiert` explizit nennen.
- Einbau in `render_markdown` nach `_render_composition`.

Test `test_context_sources_section_present` — Abschnitt im `render_markdown`-Output.

**Verify:**
`python tools/token_report.py --write` → overview.md enthält neuen Abschnitt.
`pytest tests/tools/test_token_report.py -q` → grün.

### Step 5 — O7: Planning-Darstellung klarer/lesbarer (S)

**Scope:** Planning läuft als Planner-Subagent (ADR-0007) und gibt seine Ausgabe in
eine Datei. Lesbarkeit betrifft das **Format der Ausgabe**, nicht den Renderer in
`token_report.py`. Es reicht ein **Format-Template** als Konvention — kein Tool-Change.

In `docs/reference/agent_scopes.md` (oder operating_model.md unter dem Planner-Absatz)
ein **Ausgabe-Template** hinterlegen:

```
## Planning — <Datum>

**Priorität:** <P1/P2/P3>   **Scope:** <1 Satz>

| Aufgabe | Effort | Token-Schätzung | Modus |
|---------|--------|-----------------|-------|
| …       | XS/S/M | ~Nk             | Gate/Konsent/Konsens |

**Nächster Schritt:** <Datei>/<Abschnitt>
**Offene Entscheidungen:** <NEEDS-DECISION wenn vorhanden>
```

**Verify:** `grep -n "Planning.*Template\|Ausgabe-Template" docs/reference/agent_scopes.md`
→ Template-Block vorhanden.

### Step 6 — Vollsuite + Lint + Doku-Abschluss

- `pytest --tb=short` → grün, Coverage ≥ 90 %.
- `ruff check tools/ && black --check tools/ && isort --check-only tools/` → sauber.
- `python tools/token_report.py --write` → overview.md + session_archive.md korrekt.
- `next_session.md`: O3–O7 als erledigt markieren.
- `docs/audit/plans/README.md`: Status DONE.

## Test plan

| Test | Step | Prüft |
|------|------|-------|
| `test_gauge_message_below_threshold_is_neutral` | 1 | 120k → kein ⚠️ |
| `test_gauge_message_at_warn_threshold` | 1 | 135k → ⚠️ |
| `test_merge_does_not_overwrite_higher_existing_peak` | 2 | Archiv-Schutz |
| `test_merge_overwrites_when_new_peak_is_higher` | 2 | Upsert bei besserem Peak |
| `test_merge_adds_new_session` | 2 | Neue Session landet im Archiv |
| `test_mix_bar_uses_subagent_tiers_only` | 3 | Koordinator nicht im Mix |
| `test_context_sources_section_present` | 4 | Neuer Abschnitt in overview |

## Done criteria

- [ ] `tools/session_context.py`: Warn-Schwelle 135k; Tests grün.
- [ ] `tools/token_report.py`: Archiv-Überschreib-Bug gefixt; 3 Regressionstests grün.
- [ ] Modellmix zeigt nur Subagenten-Tiers.
- [ ] `render_markdown`-Output enthält Kontext-Quellen-Abschnitt (O6).
- [ ] Planning-Template in agent_scopes.md hinterlegt (O7).
- [ ] Vollsuite grün, Coverage ≥ 90 %, Lint sauber.
- [ ] CLAUDE.md: `≥120k`-Schwellen-Text bereinigt (koordiniert mit Plan 027 Step 4).
- [ ] README: Status DONE.

## STOP conditions

- Vorher grüner Test wird rot und steht nicht in der Step-Migrationsliste → STOP,
  Stakeholder fragen (CLAUDE.md Sicherheitsnetz-Regel).
- O4 Step 2b (Echtzeit-Updates) vor Stakeholder-Entscheid zu Option A/B → STOP,
  Koordinator fragen (NEEDS-DECISION im Plan markiert).
- `pytest --tb=short` Coverage < 90 % nach einem Step → nicht weiter, Fix zuerst.
- Kein Produktivcode (kein `src/`, kein `data/`) wird verändert — bei Scope-Drift STOP.
