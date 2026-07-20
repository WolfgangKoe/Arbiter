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

## Aktueller Stand (nach S174, 2026-07-20)

**S174 committet:** **S173-Retro M1/M2/M3 überführt** — M1 als Sichtbarkeits-Schärfung
(neuer Standardsatz-Block „Test-/Gate-Executor-Briefs" + Quittungspflicht in `agent_scopes.md`,
KEINE Regel-Dopplung); M2 (Koordinator fährt keine Gate-Vollsuite im Vordergrund) in
`operating_model.md` §ev6 + `agent_scopes.md` Parallel-Block; M3 (~110k-Marke) in §ev6, ergänzt
die Korridor-Marken. `S173_RETRO.md` gelöscht. **B-125 + B-126 archiviert** (verlustfrei →
`backlog_archive.md`; stale Funktionsname → `_render_explode_target_panel()` in beiden Blöcken
gefixt); `S173_explode_panel_verifikation.md` gelöscht. **B-122 bewusst NICHT archiviert**
(Careen!-UI-Verifikation offen). **Neue S174-Retro verankert** (`agent_scopes.md` Planner-Pflichten):
„Fachlicher Fortschritt hat Vorrang" (Stakeholder-Rüge gegen Plan-/Retro-Drift). **B-028c2-Konzept
freigegeben (Class B)** — Spec in `S174_B028c2_konzept.md`, Umsetzung S175.
Review S174: **GO**; Gates Doku+Arch **25 passed** (reine Markdown-Edits, Coverage-Suite fachlich
nicht betroffen). **Token-Lehre S174:** Koordinator lief erneut > 135k (großer `backlog.md`-Read
+ umfangreiche Subagent-Rückmeldungen); Konsequenz: große Index-Reads künftig delegieren.

Frühere Sessions (S60–S173): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt (S175)

1. **B-028c2 `reroll_rp` umsetzen** — Konzept freigegeben (Class B), Spec in
   `S174_B028c2_konzept.md`: zweiter Hinweis-Produzent für Unit-Ability `reroll_rp` in
   `abilityEngine.py` (analog `get_after_attack_revive_ability`) + Caption in `_render_rp_block`
   (`_common.py`), Anker design_system §3/§3.1. Tests: mit/ohne `theirNumberIsLegion`, Direktiv-
   Pfad-Regression. XS–S ~10–15k. **Fachitem mit Code-Wirkung → erster Zug (neue S174-Retro).**
2. **Careen!-UI-Verifikation** (`S173_careen_verifikation.md`, AWAITING-VERIFICATION) — inkl.
   Fenster-Entscheid GO-Karte sichtbar VOR vs. AB Wurf (Review-F1). Danach B-122 archivieren.
3. **Review-Nachzüge S173:** F1 §7.1-Careen!-Zitat an YAML/P-16 angleichen; F2 stale §1.7-Marker
   (Zeilen 197/253/276) entfernen; F3 überlange Baustein-②-Docstrings verschlanken.
4. Danach Spyder-Konzept / weitere Ziel-7-Items laut `backlog.md`.

**Offene Handoff-Marker:** `Stakeholder_Beobachtungen.md` (STANDING);
`S173_careen_verifikation.md` (AWAITING-VERIFICATION);
`S174_B028c2_konzept.md` (AWAITING-VERIFICATION, Class B freigegeben → beim Umsetzen in S175 abräumen).

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
