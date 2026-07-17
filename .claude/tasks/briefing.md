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

## Aktueller Stand (nach S163, 2026-07-17)

**Review S163: GO** (1995 passed, Coverage 99,13 %, Arch 8 grün, Docs+Acceptance 25 grün,
mypy 0 == Baseline 0 — CI-Blocker behoben). Zwei Aufgaben, sequenziell/parallel per Plan:

- **T1 DONE — mypy-Drift-Rückbau (Retro-M1', Stakeholder-Entscheid S162):** 26 → 0, reine
  Typ-Fixes (`dict[str, Any]`/`int()`/`bool(...)`-Annotationen, keine Verhaltensänderung) in
  9 `src/`-Dateien (`attackMath.py`, `unitMutations.py`, `moralePhase.py`, `diceHtml.py`,
  `unitCard.py`, `gameProtocoll.py`, `armyCard.py`, `detachmentCard.py`, `armyList.py`);
  `tools/mypy_gate.py` `BASELINE` 25 → 0 im selben Commit nachgezogen (Ratchet-Regel erfüllt).
- **T2 DONE — B-028b-Rest: gloom_prism auf B-028a-Ability-Infrastruktur migriert:** neue
  `deny_psychic`-Ability für den Canoptek Spyder in `unit_abilities.yaml`, `wargear.yaml` auf
  Katalog-only reduziert, `can_deny()` ohne den alten Wargear-Namens-Gate; rendert jetzt wie
  Noctilith Beacons über `_render_deny_ability_cards` eine reaktive GO-Karte. 4
  neue/angepasste Tests, `processes.md` P-12 + `acceptance/rules.md` R-PSYCHIC-14
  nachgezogen. **B-119 Fall b via D-1 = Variante A mitgelöst** (einheitlicher Rendering-Pfad
  löst die geforderte Quellen-Sichtbarkeit, kein separater Chip nötig) — B-028b und B-119
  beide auf „UI-Verifikation" gesetzt. Handoff `S163_B028b_ui_verifikation.md`
  (AWAITING-VERIFICATION) wartet auf Stakeholder-Sichtprüfung — NICHT anfassen bis geprüft.
- **Review-Befunde (nachrangig, GO-unkritisch):** 1) `conditions: [has_rules: [gloom_prism]]`
  an der neuen Ability ist aktuell inert (kein Aufrufer wertet Conditions aus). 2)
  Ownership-Match statt Rule-Match verengt den Mechanismus (kein aktueller Verhaltensbruch).
  3) `load_deny_wargear_names` in `loader.py` ist jetzt toter Produktionscode (nur Tests
  referenzieren ihn). → Retro M1/M2.
- **mypy-Schuld getilgt:** die S162-Zeile „⚠ Bekannte Schuld: mypy-Gate rot" ist obsolet —
  Baseline steht auf 0, CI auf dev wieder grün.
- **S163-Rüge behoben:** Planner-Pflichtschritt „Vollständige Session-Planung" in
  `agent_scopes.md` + Briefing-Vermerk verankert.

Frühere Sessions (S60–S162): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt (S164)

Priorität = `docs/goals/backlog.md` (einzige Quelle).

1. **Stakeholder-Sichtprüfung** `docs/handoff/S163_B028b_ui_verifikation.md` (Canoptek
   Spyder Deny-Karte im echten Spielverlauf) — danach B-028b/B-119 archivieren.
2. Nächstes offenes Backlog-Item gemäß `docs/goals/backlog.md`.

**S163-Retro abgeschlossen (Nachklapp-Session):** M1 → B-120, M2 → B-121 (Backlog), M3 →
`agent_scopes.md` verankert, M4 war bereits erledigt, M5 vom Stakeholder direkt in der
Mailbox entschieden (Option a — GO/NO-GO-Urteil bleibt im Dateikörper, Review-Datei nach
Durchreichen löschen, keine Allowlist-/README-Änderung nötig). `S163_RETRO.md` auf `DONE`
gesetzt und gelöscht.

**Offene Handoff-Marker:** `Stakeholder_Beobachtungen.md` (STANDING) ·
`S163_B028b_ui_verifikation.md` (AWAITING-VERIFICATION).

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
