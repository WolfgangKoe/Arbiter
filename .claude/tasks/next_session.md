# Startprompt — Nächste Session
<!-- Kanonisch: .claude/tasks/next_session.md — nie ins Root-Verzeichnis anlegen. -->
<!-- Nur „Stand + nächster Schritt + offene Fragen". Historie → session_archive.md; Backlog → backlog.md. -->
<!-- Referenz NICHT hier: Architektur → architecture.md, Regel-Gotchas → rules_insights.md, Constraints → CLAUDE.md. -->

## ⚠️ Session-Regeln
- **Start „start next session" → Planner-Subagent beauftragen** (liest `CLAUDE.md` + `docs/goals/ziel6.md`
  + `docs/goals/backlog.md`, Scope aus `docs/reference/agent_scopes.md`); Entwurf als Datei, Koordinator
  legt vor, erst nach Freigabe los. Shortcut „Plan ist freigegeben" = direkt los. Einstieg `LEITSTAND.md`;
  Rollen/Tier/Modi: `docs/governance/operating_model.md`.
- **ADR-0007 (verbindlich seit S102):** Koordinator routet — liest keine Quelldateien/Vollergebnisse;
  Detail-Planung → Planner-Subagent; finales Review → Reviewer-Subagent. Asynchrone Stakeholder-
  Entscheidungen über Mailbox (`docs/handoff/`, NEEDS-DECISION → ANSWERED), nicht Chat.
  Details: `docs/governance/operating_model.md` [#events].
- **Ende:** Review (Reviewer-SA) → Retro → **Maßnahmen-Entscheid** (Stakeholder wählt) →
  Abschluss: **diese Datei** aktualisieren (ZUERST lesen, dann ergänzen) + ggf. ziel6-Checkboxen.
- **Doku-Gate:** Decke **120** Zeilen (Test rot darüber). Beim Reißen **tief auf ≤ 70** kürzen —
  Erledigtes → `backlog.md`/`session_archive.md`, Referenz → s. o.
- **Freigabe vor Umsetzung; kein Memory/Skill(datei-ändernd) ohne Freigabe; Subagenten =
  stehende Freigabe (proaktiv, ADR-0005); rote vorher-grüne Tests = STOP + fragen.** → `CLAUDE.md`.

## Was ist Arbiter?
Digitaler Spielbegleiter WH40k 9E, Streamlit (Python). Start: `streamlit run src/app.py`
(Port 8501; **venv:** `source .venv/bin/activate`). Branch `feature/016` (Arbeit), `main` (nur PR).
**App permanent laufen lassen:** bei Session-Start nur kurz prüfen (`curl -s -o /dev/null -w "%{http_code}" http://localhost:8501` → 200), nur bei Bedarf neu starten — nicht den Nutzer fragen.

---

## Aktueller Stand (nach S111, 2026-06-30)

**S111 — Coverage-Sprint + Plan-016-Linie abgeschlossen + Protokoll-Bugs identifiziert.**

- **game_state.py 92 → 100 %** (+17 Tests). **ability_engine.py 94 → 100 %** (+9 Tests).
- **Toter Reroll-Loop entfernt:** `get_active_round_choice_rerolls` + `_REROLL_DIRECTIVE_FLAGS`
  aus `ability_engine.py` gelöscht (kein Necron-Protokoll gibt Reroll; war Dead Code).
- **Plan 016 — generischer `get_active_protocol_effects()`-Helper (Step 2) + RP-Hints (Step 3)**
  weitgehend verdrahtet. Plan-Drift: `rp_bonus`-`max_value` NICHT auf „Modelle verloren" gesetzt —
  regelwidrig wäre es; D1=`heal_bonus`, D2=`rp_reroll`; `max_value=models_lost` ist korrekt.
  Step 4 Dynasty-Badge war bereits vollständig. LEDGER-Eintrag `protocol` in
  `test_generic_src_vocab.py` (LEGIT — generischer Funktionsname, kein Fraktions-String).
- **Vollsuite:** 1294 passed / 99,09 %, Architektur 8/8 grün, ruff+black sauber.
- **Coverage-Gate auf 99 % angehoben** (`pyproject.toml` `fail_under`); 0,09 % Puffer —
  neue Bugfixes können es brechen (Ratchet: dann Tests nachziehen).
- **oD-6 (Wound-Block 2× −1, base 4+ → Eff. 5+) ✅** vom Stakeholder visuell verifiziert (Carry-over S110).
- **Doku-Drift offen:** „92 %"-Erwähnungen in CLAUDE.md/backlog.md/operating_model.md/
  agent_scopes.md/architecture_invariants.md auf 99 % nachziehen (nur Gate-Bezug, nicht jede Erwähnung).

**Protokoll-Bugs identifiziert (regelwidrig, dokumentiert in Plan 031):**
- **Bug 1:** Direktiven-Wahl an `is_active` gekoppelt → zweiter Spieler wählt erst nach
  vollständigem ersten Zug (unerlaubter Informationsvorteil). Soll: Pending-Flag am Rundenanfang.
- **Bug 2:** „Change extra directive"-Button erlaubt nachträgliche Änderung in jeder Phase →
  reaktive Anpassung regelwidrig. Soll: Block entfernen; Wahl ab Fix auf Rundenanfang-Fenster begrenzt.

### ▶ Nächster Schritt — Prioritäten (S112)

**1. Plan 031 (NEU, P-hoch) — Protokoll-Meta-Timing-Bugs fixen** (regelwidrig).
   Step 1: „Change extra directive"-Block (`armyCard.py` Z. 219–225) entfernen (XS).
   Step 2: Pending-Flag-Mechanik in `game_state.py:_reset_round_choice_state()` + `is_active`-
   Entkoppelung in `armyCard.py:_render_round_choice_ui()` (S–M). GENERISCH, Regressionstests + manuelle UI-Prüfung.

**2. Ziel6.md konsolidieren/abschließen:** großer offener Backlog (6e/6f/6g/6h Kat1–3,
   Relics, T'au/AdMech/Tyranids) — je Punkt entscheiden: erledigt / bewusst-offen (daten-first) /
   in aktivem Plan. Nichts verlieren; viele Punkte sind bewusst zurückgestellt (YAML fehlt).

**3. subfaction-Buffs mechanisch (Plan 018/§6e):** Infrastruktur + Badge fertig & generisch,
   aber Execute-Logik fehlt (`collect_modifiers_for_phase`). Stakeholder erwägt Bündelung in Ziel7.

### ⚠️ Carry-over (offen)

- **ADR-0007-Reste:** (c) `docs/handoff/context-audit-S91.md` verarbeiten + löschen; (e) SessionStart-Regel-Injektion.
- **Manuelle UI-Verifikation (PFLICHT):** (a) Mirror-Protokoll Necron-vs-Necron Befehlsphase;
  (c) stationär+D1 grünes +1-Save-Badge in den Würfeln.
- **Retro-Maßnahmen (S110):** (1) DRY-Helper Hit/Wound ±1-Cap in `dice_html.py`; (2) st-Mock-Fixture.
- **Plan-029-Datei fehlt** (in README.md als Divergenz markiert) — vor Beauftragung anlegen oder REJECTED.

### ⚠️ OFFENE ENTSCHEIDUNG (Stakeholder beim Session-Start)

„Gefechtsoptionen" sind NICHT Teil von Ziel6 (nur Vorwärtsverweis auf Ziel7/Crusade).
Die gewünschte „Auslagerung als Ziel7" ist eine NEU-DEFINITION, kein Verschieben.
**Frage:** Ziel7 = Gefechtsoptionen + subfaction-Mechanik bündeln? Renumbering der Folge-Ziele bestätigen?
→ NICHT selbst umsetzen, nur als Entscheidung vormerken.

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor **99 %**, `pyproject.toml`); **Schulden-Scoreboard** danach.
- Architektur: `pytest tests/architecture/ --no-cov -q`. Doku/Akzeptanz: `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor** <150k, bei ~135k beenden; Fleißarbeit PROAKTIV an Sonnet-Subagent.
- **Token-Report + History (M4, PFLICHT beim Abschluss):** `python tools/token_report.py --write` + `python tools/rotate_history.py --session <N> --summary "…"` — Koordinator stößt an.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt.
