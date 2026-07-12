# Startprompt — Nächste Session
<!-- Kanonisch: .claude/tasks/next_session.md — nie ins Root-Verzeichnis anlegen. -->
<!-- Nur „Stand + nächster Schritt + offene Fragen". Historie → session_archive.md; Backlog → backlog.md. -->
<!-- Referenz NICHT hier: Architektur → architecture.md, Regel-Gotchas → rules_insights.md, Constraints → CLAUDE.md. -->

## ⚠️ Session-Regeln
- **Start:** „start next session" → Planner-Subagent (`CLAUDE.md`+`docs/goals/ziel7.md`+`docs/goals/backlog.md`, Scope `docs/reference/agent_scopes.md`) legt Entwurf vor, Koordinator zeigt ihn, erst nach Freigabe los; „Plan ist freigegeben" = Shortcut direkt los. Einstieg `LEITSTAND.md`, Rollen/Tier `docs/governance/operating_model.md`.
- **ADR-0007:** Koordinator routet, liest keine Quelldateien/Vollergebnisse — Detail-Planung/Review laufen als Subagenten; Stakeholder-Entscheidungen async über Mailbox (`docs/handoff/`, NEEDS-DECISION→ANSWERED), nicht Chat.
- **Ende:** Review (Reviewer-SA) → Retro → Maßnahmen-Entscheid (Stakeholder) → Abschluss: diese Datei aktualisieren (ZUERST lesen) + ggf. Ziel-Checkboxen.
- **Doku-Gate:** Decke 120 Zeilen (Test rot darüber); beim Reißen tief auf ≤ 70 kürzen (Erledigtes → `backlog.md`/`session_archive.md`).
- **Freigabe vor Umsetzung; kein Memory/Skill(datei-ändernd) ohne Freigabe; Subagenten = stehende Freigabe (ADR-0005); rote vorher-grüne Tests = STOP + fragen.** → `CLAUDE.md`.
- **Auftragsgrößen-Gate (S130):** kein Executor-Brief > Effort M; Test-Budget (EINE Vollsuite zentral am Wellen-Ende, `run_in_background` für pytest VERBOTEN) + Selbst-Stopp in jedem Brief → `agent_scopes.md`.
- **Handoff-Marker-Pflicht (S131):** jeder Brief, der nach `docs/handoff/` schreibt, nennt den STATUS-Marker für Zeile 1 (S137: Haiku-Agent vergaß ihn trotz Brief → im Brief als ERSTE Schreibaktion vorgeben). Format exakt `STATUS: <WERT>` als nackte erste Zeile — **kein** HTML-Kommentar `<!-- … -->`, der reißt den Hygiene-Test (S140-Maßnahme 1).
- **Planner-Schreibrecht (S140-Maßnahme 2):** Planner als general-purpose-Subagent beauftragen (nicht Plan-Agent-Typ) — der legt den Entwurf selbst nach `docs/handoff/` ab, statt ihn durchs Koordinator-Fenster zu schleusen.
- **Grundannahmen-Block (S131):** Konzept-Dokumente starten mit bestätigungspflichtigen Grundannahmen (App würfelt NICHT — Tischwürfe!) → `agent_scopes.md`.
- **Executor-Klausel:** Dateiänderungen nur über Edit/Write, Bash nur lesend/git/pytest (S123); Selbstprüfliste enthält `python tools/mypy_gate.py` (S128).
- **mypy Zero-Error-Ratchet:** Baseline sinkt jede Session Richtung 0 (Stand S138: 62 — zwei Sessions überfällig, S139 P1-Pflicht).
- **Vollsuite-Timeout (S136):** Bash-`timeout: 600000` explizit setzen. Playwright = Standard für funktionale UI-Befunde.
- **Session-Limit-Abbrüche (S137):** Bricht ein Subagent mit „session limit" ab, NICHT neu starten — per `SendMessage` resumen (Kontext intakt, hat 6/6 funktioniert). Freigabe-Gate re-armt sich beim Neustart → Koordinator re-armt nur bei dokumentierter Chat-Freigabe.
- **markdownlint-Trial (S137–S139):** `.markdownlint.jsonc` + `npm run lint:md` (cli2 v0.14, Node-18-Pin). IDE-Diagnosen erreichen den Koordinator nach Edits. Nach S139: Stakeholder entscheidet behalten/entfernen.

## Was ist Arbiter?
Digitaler Spielbegleiter WH40k 9E, Streamlit (Python). Start: `streamlit run src/app.py` (Port 8501; **venv:** `source .venv/bin/activate`). Branch `feature/016` (Arbeit), `main` (nur PR). App bei Session-Start nur per curl prüfen, bei Bedarf selbst neu starten.

---

## Aktueller Stand (nach S140, 2026-07-12)

S140 (Review **GO**, 0 Auflagen; Vollsuite 1772 passed / 99,14 %, mypy **54 → 48**):
**Dynastie↔Protokoll-Kopplung komplett** — Round-Zweig wertet `subfaction_affinity`
jetzt aus: Gate `has_round` auf `bool(active_id)` gelockert + Affinitäts-Check in
`_active_directive_effects` (`ability_engine.py`) und `active_round_choice_buff_labels`
(`game_state.py`, Unit-Card-Badges); UI-Zweig in `armyCard._render_round_choice_ui`
rendert bei Treffer sofort „… BONUS (BOTH)"-Badge statt Primary/Secondary-Buttons.
Regressionstests je 6 Dynastien in beiden Schichten; Regelzuordnung vom Reviewer gegen
Wahapedia bestätigt. Stakeholder-UI-verifiziert: positiv. Zusätzlich
`gameActionsArea.py` voll typisiert (0 neue `type: ignore`). Backlog: Affinitäts-Punkt
✅, NEU 🔲 „Dynastie-Code je Einheit statt Roster-Ebene" (Konzept-Frage 2,
Stakeholder-Entscheid S140: erfassen, nicht umsetzen).

Frühere Sessions (S60–S139): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt (S141)

1. **Roster mit Subfactions anlegen (Stakeholder-Auftrag S140):** Necron- **und**
   Ork-Roster in `data/rosters/` mit gesetzten Subfactions (verschiedene Dynastien/
   Klans), damit Affinitäts-UI und Subfaction-Features real prüfbar sind (S139:
   Emergency Disembarkation scheiterte schon an fehlendem TRANSPORT-Roster — breit
   denken: Subfactions + Transport abdecken).
2. **mypy `state: dict`-Contract-Fix (Retro-Maßnahme 3, eigener geplanter Schritt):**
   `phase_handler.py`/`phase_runner.py` + 7 Phase-Dateien wiederholen
   `state: dict  # type: ignore[type-arg]` — Fix auf `MutableMapping[str, Any]`
   (SessionStateProxy-kompatibel) senkt mehrere Posten zugleich. Baseline 48; weitere
   Top-Posten: `armyCard.py` 6, `shootingPhase.py` 5, `movementPhase.py` 5; dazu alter
   `# type: ignore[type-arg]` in `ability_engine.py:141` (Review-Hinweis S140).
3. **Dokumentierte Ratchet-Schulden (unverändert aus S139):** (a) B12b-Header-Suffix
   „used on ⟨Einheit⟩" — XS-Folge-Task; (b) Stil-Nit `undo_stratagem` in-place-Mutation
   → bei nächster Modul-Berührung; (c) R-PROTO-02 `status: offen` (Aura-Tischhinweis
   entfernt, neuer Mechanismus offen).
4. **Rand-Design-Konzept** (heller Streifen links, beim 2. Spieler spiegeln, auf GOs
   übertragen); **GO-Keyword-Nachpflege** in YAML (systematisch, Subagent); **Rest
   unverändert (S137/S138):** 4c-Folge-Split (Paket 7/8) → B7/B9-Konzept + B2 Option A;
   Fold-Heuristik+Subfaction-Wiring (Retro-Maßnahme 3); Totalvernichtungs-Spielende;
   Kleinschulden (Smoke-Test `hook_pytest_foreground.py`, `_common.py`-Refactor,
   S130-GO-Verifikation, 037 Docker-Smoke, Deny-Caption, Direction-Entscheide,
   B4/B8-Welle-2-Screenshots + HI-UI-Ausrollung). Details → `backlog.md`.

**Retro S140 (freigegeben 1–3):** Marker-Format in Regel oben präzisiert (M1);
Planner-Schreibrecht-Regel ergänzt (M2); `state: dict`-Contract-Fix als S141-Punkt 2
eingeplant (M3). Retro-Leitlinie S139 (Kommentare reduzieren) bleibt in Kraft.

**Prozess:** Vollsuite bei parallelen Wellen nur EINMAL zentral am Wellen-Ende
(`operating_model.md` Event 3).

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor **99 %**); Architektur: `pytest tests/architecture/ --no-cov -q`; Doku/Akzeptanz: `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor** <150k, ab ~120k Wind-down, spätestens ~135k beenden; Fleißarbeit PROAKTIV an Sonnet-Subagent (Briefs ≤ M).
- **Token-Report + History (Abschluss-PFLICHT):** `python tools/token_report.py --write` + `python tools/rotate_history.py --session <N> --summary "…"`.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt (Ausnahmen: `docs/handoff/`, außerhalb Repo).
