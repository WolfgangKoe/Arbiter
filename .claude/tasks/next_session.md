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
- **Start-Sync prüft auch `docs/handoff/` auf liegengebliebene ANSWERED/DONE-Dateien** (r-proto-02
  lag seit S116).
- **Executor-Aufträge enthalten die Klausel:** Dateiänderungen nur über Edit/Write-Tools, Bash nur
  lesend/git/pytest (Freigabe-Gate-Umgehung S123).

## Was ist Arbiter?
Digitaler Spielbegleiter WH40k 9E, Streamlit (Python). Start: `streamlit run src/app.py`
(Port 8501; **venv:** `source .venv/bin/activate`). Branch `feature/016` (Arbeit), `main` (nur PR).
**App permanent laufen lassen:** bei Session-Start nur kurz prüfen (`curl -s -o /dev/null -w "%{http_code}" http://localhost:8501` → 200), nur bei Bedarf neu starten — nicht den Nutzer fragen.

---

## Aktueller Stand (nach S127, 2026-07-05)

S127 (Pläne 038+039 + Doku-Paket): `db87d48` mypy-Ratchet-Gate (tools/mypy_gate.py, Baseline
134, deploy.yml-Gate statt continue-on-error). `69d6484`+`6500c94` README-Setup komplett,
.env.example gelöscht, pytest-xdist in CI (218s→75s). `868ec36` r-proto-02-Handoff geschlossen
(war seit S116 umgesetzt, Backlog Z.51 ✅), Schulden-Tabelle nachgezogen (2026-07-05: INV-4b 11
· INV-4 5 · INV-5 5), Backlog-Einträge: INV-4-Allowlist→0 (S128) + mypy-Abbau modulweise.
Review: GO, keine Blocker. Vollsuite 1456 passed, Coverage 99,11 %. Kein UI-Code berührt.

Frühere Sessions (S60–S126): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt

**INV-4-Mini-Task ausführen** (Allowlist 5→0: `necrons`-Defaults in `game_state.py`/`loader.py`
aus gewählten Rostern ableiten, Größe S, terminiert S128 — Backlog Z.~96). Daneben nächsten
Plan aus der Queue planen: 041 verbleibt, Regel beachten: 041 NICHT parallel zu 015/026, erst
nach 015/026 — Reihenfolge klärt der Planner.
**Stehende Regel (Retro S127, Maßnahme 1):** Jede Session enthält mind. einen Ledger-Abbau-
Schritt, bis alle „→0"-Ledger bei 0 sind: INV-4 (S128) → INV-4b (11 Tokens, 2–3 Schritte) →
mypy (Baseline 134, modulweise, Baseline-Senkung im selben Commit).

**Offene Verifikation (VOR Merge nach `main`):**
- **037 Docker**: `docker build` + `docker run --rm arbiter-test id -u` → 1000 +
  Port-7860-Smoke beim nächsten HF-Spaces-Deploy (lokal kein Docker).

**Offene Punkte / Merksätze:**
(b) ADR-0006:32 referenziert alten Pfad des 024-Digests (kosmetisch, bei Gelegenheit).
(c) Merkposten `hand_of_the_phaeron`/ExtraUses steht in Plan 032.
(d) Direction-Entscheide offen (Audit S124): ziel9-Fetcher vorziehen? Deployment-Phase
bauen oder ADR „bleibt am Tisch"? Mission-Scoring (eine Mission end-to-end)?
(e) Merkposten: 6 ungenutzte Loader-Funktionen (`load_points` u. a.) — Intent klären
(ziel9-Scaffolding?), dann löschen/behalten (Rejected-Liste plans/README).
(f) Retro S124: ab ~6 Plänen splitten oder Entwürfe an Sonnet delegieren.
(g) Retro S126: Lösch-Pläne → Executor-Selbstprüfliste MUSS entfernte Bezeichner
auch über `docs/spec/` greppen (S126-Blocker: 2 Specs beschrieben Gelöschtes).
(h) Retro S126: App VOR jeder UI-Verifikation neu starten (alter Prozess/State
lieferte 4 falsche ❌); UI-Prüfanleitungen vorher gegen Roster-Realität validieren
(Flayed-Ones-Check ohne Roster-Deckung, „Szenario-UI" existiert nicht — nur
`?scenario=`-Query-Param).

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor **99 %**, `pyproject.toml`); **Schulden-Scoreboard** danach.
- Architektur: `pytest tests/architecture/ --no-cov -q`. Doku/Akzeptanz: `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor** <150k, bei ~135k beenden; Fleißarbeit PROAKTIV an Sonnet-Subagent.
- **Token-Report + History (M4, PFLICHT beim Abschluss):** `python tools/token_report.py --write` + `python tools/rotate_history.py --session <N> --summary "…"` — Koordinator stößt an.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt.
