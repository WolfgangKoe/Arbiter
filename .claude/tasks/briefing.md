# Koordinator-Briefing

<!-- Kanonisch: .claude/tasks/briefing.md — nie ins Root-Verzeichnis anlegen. -->
<!-- Zweck: Koordinator-Briefing bei Session-Start + Kontext-Zwischenspeicher -->
<!-- über Kontextfenster-Grenzen hinweg. Regeln → CLAUDE.md/operating_model.md/agent_scopes.md. -->

## Was ist Arbiter?

Digitaler Spielbegleiter WH40k 9E, Streamlit (Python). Start: `streamlit run src/app.py`
(Port 8501; **venv:** `source .venv/bin/activate`). Branch `dev` (Arbeit), `main` (nur PR).

**Die App muss dauerhaft laufen** (Stakeholder-Anweisung S152): bei Session-Start prüfen
(`curl -s -o /dev/null -w "%{http_code}" http://localhost:8501` → 200) und andernfalls im
Hintergrund starten (`streamlit run src/app.py --server.headless true`) — nicht beenden.

---

## Session-Routine — nur Verweise

- **Workflow/Freigabe-Gates/Session-Ablauf:** `CLAUDE.md`
- **Rollen/Model-Tier/Events:** `docs/governance/operating_model.md`
- **Scopes + Brief-Pflichten je Aufgabentyp:** `docs/reference/agent_scopes.md`
- **Einstieg für den Stakeholder:** `LEITSTAND.md`
- **Retro-Maßnahmen-Entscheid am Session-Start:** docs/governance/operating_model.md Event 1 (§ev1)

---

## Aktueller Stand (nach S176, 2026-07-21)

**S176 committet:** **B-127 umgesetzt** — die beiden RP-Reroll-Hinweise im RP-Block
(`_render_rp_block`, `src/uiLayout/_common.py` ~Z.2614-2617) rendern jetzt als blauer
`st.info`-Kasten (§3-Hinweis-Konvention) statt schwacher `st.caption`; Wortlaut unverändert, reine
Class-B-Anzeige-Migration. 3 Tests angepasst (`test_common.py`, Helper
`_render_rp_block_captions`→`_render_rp_block_info_texts`, Monkeypatch `st.caption`→`st.info`).
**UI-Verifikation positiv** (Stakeholder): beide Hinweise — „Their Number is Legion" + „Undying
Legions Direktive 2" (`rp_reroll`) — als blauer Kasten inkl. Koexistenz. B-127 nach
`backlog_archive.md` verschoben. **B-113 Scope-Discovery** (read-only) durchgeführt, Umsetzung auf
**S177 verschoben** (Details s. „Nächster Schritt"). Review S176: **GO** (nach Handoff-Aufräumung);
Gates **2151 passed, Coverage 99,20 %, Architektur 8 passed**.

**Retro-Maßnahmen S176 (alle vier vom Stakeholder übernommen) — Umsetzung durch S177-Planner:**
- **M1:** Koordinator setzt in Handoffs nur **gültige** Status-Marker
  (NEEDS-APPROVAL/NEEDS-DECISION/ANSWERED/DONE/STANDING/AWAITING-VERIFICATION) — kein erfundenes
  „RESOLVED" o. ä. (S176 selbst verursacht).
- **M2:** Planner liest zuerst die **tatsächliche `backlog.md`-Rangfolge**, das Briefing-
  „Nächster Schritt"-Hint ist nachrangig (S176: Briefing nannte B-005, echte Priorität war
  B-124/B-028c/B-113).
- **M3 (Doku-Drift, für S177-Planner):** (a) `src/gameState.py` → `src/gameMechanic/gameState.py`
  in den B-028c4/c5-Detail-Einträgen korrigieren; (b) Annahme „reroll bereits im WOUND-Block
  verdrahtet" (B-113/B-116-Texte) korrigieren — die B-113-Discovery hat sie **widerlegt**
  (`reroll_hit`/`reroll_wound_1` engine-seitig komplett unkonsumiert, `reroll_marker_row_html`
  0 Call-Sites → Erstanwendung, nicht Analogiefall).
- **M4:** „Discovery vor Schätzung" bewährt (B-113 falsche Scope-Annahme gekippt) — Muster
  beibehalten, keine Doku-Änderung nötig.

**Zwei Prozess-Doku-Korrekturen vom Stakeholder (S177-Planner setzt sie in die Prozess-Docs um):**
- (a) **Subagenten schreiben ihre Handoff-Artefakte selbst** (nicht der Koordinator) — S176 mussten
  Planner/Reviewer/Discovery ihre Ausgaben zurückgeben, weil sie keinen Write-Zugriff auf
  `docs/handoff/` hatten; `agent_scopes.md` (Scopes/Tool-Zugriff je Rolle) anpassen, sodass
  Planner/Reviewer nach `docs/handoff/` schreiben dürfen.
- (b) **Orchestrator-/Koordinator-Tier = Opus** (Fable steht nicht zur Verfügung) — in
  `docs/governance/operating_model.md` (Rollen & Model-Tier) prüfen/korrigieren, wo Fable als
  Orchestrator-Tier steht.

Frühere Sessions (S60–S175): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt (S177)

0. **Retro-Maßnahmen S176 umsetzen** (s. o.): M1–M3 + die zwei Prozess-Doku-Korrekturen (a)/(b)
   in `agent_scopes.md`/`operating_model.md`/`backlog_details.md` einarbeiten.
1. **B-113 — Reroll-Fähigkeiten verdrahten** (Discovery-Ergebnis, war `S176_B113_discovery.md`):
   Skorpekh-Destroyer-**Hit-Reroll** (`reroll_hit`, YAML liegt in `subfaction_abilities.yaml:150`,
   anderer Ladepfad als Unit-Abilities → offene Sub-Recherche) und **beide** DESTROYER-CULT-Lords
   (**Lokhust Lord** *und* **Skorpekh Lord** — Stakeholder-Entscheid, „Destroyer Lord" = beide;
   Profil + `united_in_destruction`-Ability existieren bereits in `units.yaml`/`unit_abilities.yaml`,
   fehlen nur im Roster) mit **Wound-Reroll** (`reroll_wound_1`, Aura, Reichweiten-Bedingung).
   **Kernbefund:** `reroll_hit`/`reroll_wound_1` werden nirgends im Combat-/Ability-Code konsumiert,
   `reroll_marker_row_html` (`diceCompose.py:451`) hat 0 Call-Sites → B-113 ist Erstanwendung des
   ganzen Reroll-auf-Angriffswürfe-Pfads. Split: Teil (a) Skorpekh-Hit inkl. generischem
   Reroll-Effect-Konsument (Vorlage), dann Teil (b) Lord-Aura. Beide **M** → je eigener Teil-Brief.
2. **B-028c3/c4/c5** (backlog.md Rang 2–4) — **DoR NICHT erfüllt** (Feld „Benötigte Regeln-Scopes"
   leer, wie B-005): vor jeder Umsetzung Regel-Scope befüllen; B-028c3 zusätzlich „höchstes
   Restrisiko / Scope-Check vor Beauftragung".
3. **B-005 Direktiv-Lock-Rest** — nachrangig, DoR ebenfalls leer.

**Offene Handoff-Marker:** `Stakeholder_Beobachtungen.md` (STANDING).

---

## Gate-Netz (Messbefehle)

- Tests + Coverage: `pytest --tb=short` (Floor **99 %**); Architektur:
  `pytest tests/architecture/ --no-cov -q`; Doku/Akzeptanz:
  `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor** <150k, ab ~120k Wind-down, spätestens ~135k beenden; ab ~100k nichts
  Neues bei ausstehendem Review.
- **Abschluss-PFLICHT:** `python tools/token_report.py --write` +
  `python tools/rotate_history.py --session <N> --summary "…"`.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt
  (Ausnahmen: `docs/handoff/`, außerhalb Repo).
