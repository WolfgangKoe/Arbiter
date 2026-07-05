# Startprompt — Nächste Session
<!-- Kanonisch: .claude/tasks/next_session.md — nie ins Root-Verzeichnis anlegen. -->
<!-- Nur „Stand + nächster Schritt + offene Fragen". Historie → session_archive.md; Backlog → backlog.md. -->
<!-- Referenz NICHT hier: Architektur → architecture.md, Regel-Gotchas → rules_insights.md, Constraints → CLAUDE.md. -->

## ⚠️ Session-Regeln
- **Start „start next session" → Planner-Subagent beauftragen** (liest `CLAUDE.md` + `docs/goals/ziel7.md`
  + `docs/goals/backlog.md`, Scope aus `docs/reference/agent_scopes.md`); Entwurf als Datei, Koordinator
  legt vor, erst nach Freigabe los. Shortcut „Plan ist freigegeben" = direkt los. Einstieg `LEITSTAND.md`;
  Rollen/Tier/Modi: `docs/governance/operating_model.md`.
- **ADR-0007 (verbindlich seit S102):** Koordinator routet — liest keine Quelldateien/Vollergebnisse;
  Detail-Planung → Planner-Subagent; finales Review → Reviewer-Subagent. Asynchrone Stakeholder-
  Entscheidungen über Mailbox (`docs/handoff/`, NEEDS-DECISION → ANSWERED), nicht Chat.
  Details: `docs/governance/operating_model.md` [#events].
- **Ende:** Review (Reviewer-SA) → Retro → **Maßnahmen-Entscheid** (Stakeholder wählt) →
  Abschluss: **diese Datei** aktualisieren (ZUERST lesen, dann ergänzen) + ggf. Ziel-Checkboxen.
- **Doku-Gate:** Decke **120** Zeilen (Test rot darüber). Beim Reißen **tief auf ≤ 70** kürzen —
  Erledigtes → `backlog.md`/`session_archive.md`, Referenz → s. o.
- **Freigabe vor Umsetzung; kein Memory/Skill(datei-ändernd) ohne Freigabe; Subagenten =
  stehende Freigabe (proaktiv, ADR-0005); rote vorher-grüne Tests = STOP + fragen.** → `CLAUDE.md`.
- **Checkbox-Sync prüft auch Commit-Behauptungen:** Session-Start-Sync nicht nur gegen Ziel-Checkboxen,
  sondern auch Titel wie „archive/close" gegen Datei-Realität verifizieren (b3ebfd5 behauptete
  Archivierung ohne Vollzug, S119→S120-Befund). Restrisiko bewusst nicht test-bewacht — Kompensation:
  Reviewer-Pflicht + dieser Sync.

## Was ist Arbiter?
Digitaler Spielbegleiter WH40k 9E, Streamlit (Python). Start: `streamlit run src/app.py`
(Port 8501; **venv:** `source .venv/bin/activate`). Branch `feature/016` (Arbeit), `main` (nur PR).
**App permanent laufen lassen:** bei Session-Start nur kurz prüfen (`curl -s -o /dev/null -w "%{http_code}" http://localhost:8501` → 200), nur bei Bedarf neu starten — nicht den Nutzer fragen.

---

## Aktueller Stand (nach S125, 2026-07-05)

**S125 (Audit-Pläne 033–037 umgesetzt):** Alle vier P1-Bugs + die P2-Deps-Härtung
committet und auf `feature/016-protocol-rp-effects` konsolidiert (5 Commits linear,
Sub-Branches gelöscht), Pläne nach `docs/audit/plans/archive/` verschoben:
- `3ec5ad9` **033** Phasen-Modifier-Expiry (`_reset_phase_state()` vor `phase_idx`)
- `57c1593` **034** State-Key-Lookups bei Duplikat-Trupps (`unit_id_from_state_key`)
- `45db5b4` **036** `.rosz`-Import gehärtet (Sanitize + 20-MB-Cap + `html.escape`)
- `1be845f` **035** `active_buffs` besitzer-bedingt leeren (MWBD überdauert Gegnerzug)
- `c5ea24f` **037** Deps gepinnt, `pip-audit`-CI, Docker non-root
Reviewer-Subagent (Opus): **GO**, keine Blocker. Vollsuite 1461 passed, Coverage
99,12 % (`game_state.py` 100 %), Architektur-Gate grün, INV-4b-Ratchet unverändert.
Verbleibende Audit-Queue: 040 → 038 → 039 → 041 (s. `docs/audit/plans/README.md`).

Frühere Sessions (S60–S124): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt

**Plan 040 ausführen** (Totes Phasen-Lifecycle entfernen, P2, S–M) — Deps 033/035
sind erledigt. Danach **038 → 039 → 041**. Regeln: 041 zwingend nach 034 (✅) + 040
und NICHT parallel zu 015/026; 041 erst nach 015/026. Jeder Plan self-contained
(Drift-Check gegen `f6c464a` eingebaut) → Executor-Subagent direkt beauftragbar.

**Offene Verifikationen aus S125 (VOR Merge nach `main`, Render-/Runtime-Code — nicht test-gedeckt):**
- **034 UI** mit `data/rosters/necrons_1500pts_silent_king.yaml`: (1) zweiter
  Warriors-Trupp bekommt Moraltest, (2) Battle-Log-Snapshot listet beide Duplikate
  mit Klarnamen, (3) Melee-Liste zeigt Klarnamen statt `#N`, (4) Resurrection-Orb-
  Heal-UI rendert für Duplikat-Ziel.
- **036 UI**: Header zeigt legitime Spielernamen unverändert (Escaping-Artefakte prüfen).
- **037 Docker**: `docker build` + `docker run --rm arbiter-test id -u` → 1000 +
  Port-7860-Smoke beim nächsten HF-Spaces-Deploy (lokal kein Docker).

**Offene Punkte / Merksätze:**
(a) Retro-Beobachtung S123: Archiv-Executor umging das wieder scharfe Freigabe-Gate per
Bash-Schreibzugriff statt zu eskalieren — Maßnahme in nächster Retro entscheiden.
(b) ADR-0006:32 referenziert alten Pfad des 024-Digests (kosmetisch, bei Gelegenheit).
(c) Merkposten `hand_of_the_phaeron`/ExtraUses steht in Plan 032.
(d) Direction-Entscheide offen (Audit S124): ziel9-Fetcher vorziehen? Deployment-Phase
bauen oder ADR „bleibt am Tisch"? Mission-Scoring (eine Mission end-to-end)?
(e) Merkposten: 6 ungenutzte Loader-Funktionen (`load_points` u. a.) — Intent klären
(ziel9-Scaffolding?), dann löschen/behalten (Rejected-Liste plans/README).
(f) Retro-Beobachtung S124: 9 Pläne inline schreiben sprengte den Korridor (~190k) —
künftig ab ~6 Plänen splitten oder Entwürfe an Sonnet delegieren, Opus finalisiert.

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor **99 %**, `pyproject.toml`); **Schulden-Scoreboard** danach.
- Architektur: `pytest tests/architecture/ --no-cov -q`. Doku/Akzeptanz: `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor** <150k, bei ~135k beenden; Fleißarbeit PROAKTIV an Sonnet-Subagent.
- **Token-Report + History (M4, PFLICHT beim Abschluss):** `python tools/token_report.py --write` + `python tools/rotate_history.py --session <N> --summary "…"` — Koordinator stößt an.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt.
