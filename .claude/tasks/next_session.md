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
- **mypy Zero-Error-Ratchet:** Baseline sinkt jede Session Richtung 0 (Stand S138: 62 — zwei Sessions überfällig, S139 P1-Pflicht; **S141: 48 → 28**, `state`-Contract-Fix erledigt, Rest 17 `uiLayout/` + 11 `gameMechanic/`-Restfehler anderer Klasse, s. `backlog.md` §4).
- **Vollsuite-Timeout (S136):** Bash-`timeout: 600000` explizit setzen. Playwright = Standard für funktionale UI-Befunde.
- **Session-Limit-Abbrüche (S137):** Bricht ein Subagent mit „session limit" ab, NICHT neu starten — per `SendMessage` resumen (Kontext intakt, hat 6/6 funktioniert). Freigabe-Gate re-armt sich beim Neustart → Koordinator re-armt nur bei dokumentierter Chat-Freigabe.
- **markdownlint-Trial (S137–S139):** `.markdownlint.jsonc` + `npm run lint:md` (cli2 v0.14, Node-18-Pin). IDE-Diagnosen erreichen den Koordinator nach Edits. Nach S139: Stakeholder entscheidet behalten/entfernen.

## Was ist Arbiter?
Digitaler Spielbegleiter WH40k 9E, Streamlit (Python). Start: `streamlit run src/app.py` (Port 8501; **venv:** `source .venv/bin/activate`). Branch `feature/016` (Arbeit), `main` (nur PR). App bei Session-Start nur per curl prüfen, bei Bedarf selbst neu starten.

---

## Aktueller Stand (nach S141, 2026-07-12)

S141: mypy-Baseline **48 → 28** (`state`-Contract-Fix, Commits `42af867`/`292b3ad`);
Ork-Transport-Roster `orks_transport.yaml` (`cbaeeb2`); B12b-Suffix verdrahtet (`cdb55e2`);
zwei UI-Verifikations-Bugfixes: Emergency-Disembark-Sichtbarkeit (`f36f1e7`),
Movement-Timing/Abdunkeln (`7fc8b16`). Vollsuite **1783 / 99,15 %**. Zwei weitere gemeldete
Bugs (Insane-Bravery-Ziel, Cross-Player-Leak) diagnostiziert, wegen Korridor nach S142
vertagt — Fix-Orte in `docs/handoff/S141_ui_befunde_group_a.md`.

## Stand nach S140 (2026-07-12)

S140 (Review **GO**, 0 Auflagen; Vollsuite 1772 passed / 99,14 %, mypy **54 → 48**):
**Dynastie↔Protokoll-Kopplung komplett** — Round-Zweig wertet `subfaction_affinity`
jetzt aus: Gate `has_round` auf `bool(active_id)` gelockert + Affinitäts-Check in
`_active_directive_effects` (`abilityEngine.py`) und `active_round_choice_buff_labels`
(`gameState.py`, Unit-Card-Badges); UI-Zweig in `armyCard._render_round_choice_ui`
rendert bei Treffer sofort „… BONUS (BOTH)"-Badge statt Primary/Secondary-Buttons.
Regressionstests je 6 Dynastien in beiden Schichten; Regelzuordnung vom Reviewer gegen
Wahapedia bestätigt. Stakeholder-UI-verifiziert: positiv. Zusätzlich
`gameActionsArea.py` voll typisiert (0 neue `type: ignore`). Backlog: Affinitäts-Punkt
✅, NEU 🔲 „Dynastie-Code je Einheit statt Roster-Ebene" (Konzept-Frage 2,
Stakeholder-Entscheid S140: erfassen, nicht umsetzen).

Frühere Sessions (S60–S139): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt (S142)

**Strategisches Thema (Stakeholder S141) — Gefechtsoptionen-Architektur:** GOs/Stratagems
funktionieren ähnlich wie Abilities, laufen aber vermutlich NICHT über die ability-Engine.
S142-Planning soll die Ist-Architektur erheben (`stratagem.py`, `gameProtocoll.py`,
`abilityEngine.py`) und eine Empfehlung mit Trade-offs geben: über die ability-Engine
vereinheitlichen ODER gesonderte Funktion (auch wenn das etwas Code dupliziert)? Hängt eng
mit FixC/FixD zusammen — beide sitzen in der GO/Stratagem-Verdrahtung; ggf. Fixes im Licht
der Architektur-Entscheidung planen.

**Priorität — S141-Verifikations-Bugs, diagnostiziert & freigegeben, wegen Korridor vertagt
(Fix-Orte in `docs/handoff/S141_ui_befunde_group_a.md`):**

1. **FixC — Insane Bravery erzwingt kein Ziel:** `_effect_gate_met()` (`gameProtocoll.py`
   Z.145-177) kennt nur die Desperate-Breakout-Gate-Form, nicht `auto_pass_morale` →
   „Use" geht mit `unit_key=None` durch, CP gebucht, Effekt verpufft lautlos. Fix +
   `_use_callback` (Z.249-262). Aufwand S.
2. **FixD — Cross-Player-Area-Leak (Whirling Onslaught über beide Spalten):**
   `render_attack_resolution()` in `fightPhase.py` (Z.558-573) + `shootingPhase.py`
   (Z.187) außerhalb der Zwei-Spalten-Struktur (Muster wie S139-E7, nie nachgezogen);
   sekundär `target_name` in `_common.py::render_reactive_stratagem_box` (Z.876-889).
   Stakeholder-Auftrag: Audit ALLER `*Phase.py` auf dasselbe Muster. Aufwand M.

**Vertagte Befunde (S141-Verifikation):**

1. **Insassen-Feature (Emergency-Disembark Teil B):** kein Konzept „Einheit sitzt in
   Transport" (Roster-YAML/State/UI) — eigenes Planning; Design-Fragen (Start-Zustand vs.
   In-Game-UI; Kapazität hart vs. Hinweis) in `docs/handoff/S141_ui_befunde_group_b.md`.
2. **Verwandter `on_declaration`-Befund (analog FixA):** `chargePhase.py:170`/
   `fightPhase.py:460` reichen kein `unit_for_conditions` durch → `efficient_disintegration`
   evtl. betroffen; „unit selected to shoot"-Anker fehlt in `shootingPhase.py`. → `backlog.md`.
3. **Roster-Test-Lücke:** kein Test lädt alle `data/rosters/` durch (`test_loader.py:1259`
   fest 2 Roster). → `backlog.md` §4d.

**Manuelle UI-Verifikation:** FixA (Emergency-Disembark) + FixB (Movement-Abdunkeln)
S141 stakeholder-verifiziert ✅. Offen: B12b-Suffix, Klan-Affinität am Ork-Transport-Roster
(`backlog.md` §3).

**Ratchet/Rest unverändert:** mypy-Baseline 28 weiter Richtung 0 (`uiLayout/` 17 +
`gameMechanic/` 11, `backlog.md` §4); Stil-Nit `undo_stratagem` in-place; R-PROTO-02 offen;
Rand-Design-Konzept; GO-Keyword-Nachpflege (zurückgestellt bis B13, Schema-Befund);
4c-Folge-Split, Fold-Heuristik, Totalvernichtungs-Spielende, Kleinschulden → `backlog.md`.

**Prozess:** Vollsuite bei parallelen Wellen nur EINMAL zentral am Wellen-Ende
(`operating_model.md` Event 3).

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor **99 %**); Architektur: `pytest tests/architecture/ --no-cov -q`; Doku/Akzeptanz: `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor** <150k, ab ~120k Wind-down, spätestens ~135k beenden; Fleißarbeit PROAKTIV an Sonnet-Subagent (Briefs ≤ M).
- **Token-Report + History (Abschluss-PFLICHT):** `python tools/token_report.py --write` + `python tools/rotate_history.py --session <N> --summary "…"`.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt (Ausnahmen: `docs/handoff/`, außerhalb Repo).
