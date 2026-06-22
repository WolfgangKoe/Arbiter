# Startprompt — Nächste Session
<!-- Kanonisch: .claude/tasks/next_session.md — nie ins Root-Verzeichnis anlegen. -->
<!-- Nur „Stand + nächster Schritt + offene Fragen". Historie → ziel6.md; Backlog → backlog.md. -->
<!-- Referenzwissen NICHT hier: Architektur-Muster → architecture.md, Regel-Gotchas →
     rules_insights.md, Constraints → CLAUDE.md. -->

## ⚠️ Session-Regeln
- **Start "start next session" → Planning vorlegen** (Prioritäten + Token-Schätzung), erst nach
  Freigabe los; Shortcut „Plan ist freigegeben" = direkt los. **Lesen:** `CLAUDE.md` (Freigabe,
  bei Unklarheit fragen) + `docs/goals/ziel6.md` (Aufgaben/Historie) + `docs/goals/backlog.md`.
  Einstieg: `LEITSTAND.md`; Rollen/Tier/Events/Modi: `docs/governance/operating_model.md`.
- **Ende:** Review → Retro → **Maßnahmen-Entscheid** (Stakeholder wählt) → Abschluss: Checkboxen
  in `ziel6.md` + Historien-Zeile; **diese Datei** aktualisieren (ZUERST lesen, dann ergänzen).
- **Doku-Gate:** Decke **120** Zeilen (Test rot darüber). Beim Reißen **tief auf ≤ 70**
  kürzen, nicht knapp drunter — Erledigtes → `backlog.md`/`ziel6.md`, Referenz → s. o.
- **Freigabe vor Umsetzung; kein Memory/Skill(datei-ändernd) ohne Freigabe; Subagenten
  = stehende Freigabe (proaktiv, ohne Nachfrage, ADR-0005); rote vorher-grüne Tests =
  STOP + fragen.** Details: `CLAUDE.md`.

## Was ist Arbiter?
Digitaler Spielbegleiter für WH40k 9E, Streamlit (Python). Start:
`streamlit run src/app.py` (Port 8501). Branch `dev` (Arbeit), `main` (nur per PR).

---

## Aktueller Stand (nach S87, 2026-06-22)

**S87 (Branch `feature/024-arkana-protocol-effect-modeling`) — Plan 024 Steps 5–6 DONE** (Commit `7b6a23e`,
1116 grün/93 %, INV-4b unverändert 11):
- **Step 5:** `failsafe_overcharger` → `ability_type: activated`, dispatcht +1 Attacks auf CANOPTEK über die
  **vorhandene** `buff_stat`/`multi`-Infra — **kein STOP, kein neues Dataclass-Feld** (Befund: flache
  `effect:`-Form aus dem Plan würde NICHT dispatchen; `_active_effects_for_faction` verlangt `effect.type==multi`).
- **Step 6:** alle 11 restlichen Arkana mit engl. `rule_text` + `trigger/conditions/effect` (bleiben
  `descriptive`, kein Dispatch); **alle 12** Kosten −5 auf Wahapedia (Step-6-Fleißarbeit per Sonnet-Subagent).
- 2 vorher-grüne Loader-Tests auf neuen Sollzustand nachgezogen (failsafe lädt jetzt; quantum_orb 15, failsafe 25).

### ▶ Nächste Session
1. **Plan 024 Step 7 (Doku, vertagt) ZUERST:** `docs/spec/faction_abilities.md` (Direktiv-Wiring ✅ + welche
   Arkana warum `descriptive` bleiben), `docs/goals/backlog.md` #2 (Direktiven abhaken + INV-4b Cluster 6
   Dispatch-Status), Status-Zeile in `docs/audit/plans/README.md`. Dann Plan 024 vollständig DONE.
2. **Manueller UI-Test vorbereiten + durchführen:** ein **Roster** bereitstellen/finden, das `failsafe_overcharger`
   (TECHNOMANCER) + Arkana enthält, in der App laden und prüfen: lädt korrekt, Failsafe in Command-Phase
   aktivierbar, +1-Attacks-Anzeige auf CANOPTEK. Plus Steps-1–4-Anzeigen (S+1/AP/Move/Reroll/RP).
3. **BUG `docs/metrics/overview.md`:** wird nach einem Lauf wieder mit Müll (0-Werte) überschrieben — echte Werte
   nur kurz sichtbar, dann „gelöscht". Ursache finden (token_report/Hook-Reihenfolge?) und fixen.
4. Danach Queue: 016 → 018 → 015 → 017.

### Offene Fragen / Retro-Vormerke
- **Follow-up ADR-0006 (S86):** `CLAUDE.md` (Token-Disziplin/Subagent-Muster) um einen Verweis auf
  [ADR-0006](../../docs/governance/decisions/0006-subagent-grossausgaben-als-datei.md) ergänzen —
  Subagent-Großausgaben als Datei zurückgeben (Verweis statt Volltext) + Permanent/Temporär-Deklaration.
- **ADR-0005 geklärt (S87):** Freigabe-Gate feuert **auch im Subagent** — Subagent verweigert korrekt das
  Selbst-Setzen. Marker verfällt bei **SessionStart** (nicht Stop) → bei Session-Grenzen mitten in der Arbeit
  neu `touch .claude/.freigabe` nötig (in S87 passiert).
- **Doku-Drift:** `architecture.md` §session_state — `group_wounds` universell (backlog §4b).
- **INV-4b Restschuld:** noch `dynasty` (movementPhase), `gloom/prism` (psychicPhase → Cluster 5),
  `necrons`-Defaults (game_state/loader). `arkana` erledigt (S84). Ratchet weiter schrumpfen.

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor 90 %, `pyproject.toml`).
- **Schulden-Scoreboard** nach jedem `pytest` (`tests/conftest.py`).
- Architektur (INV-1..4b): `pytest tests/architecture/ --no-cov -q`.
- Doku/Akzeptanz (INV-5): `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor:** <150k, bei ~135k Session beenden; Fleißarbeit PROAKTIV an Sonnet-Subagent.
- **Token-Report:** `python tools/token_report.py --write` → `docs/metrics/overview.md`.
- **History-Rotation:** `python tools/rotate_history.py --session <N> --summary "…"`.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt.
</content>
</invoke>
