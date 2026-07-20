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

## Aktueller Stand (nach S173, 2026-07-20)

**S173 committet:** **Retro-M3** überführt (Budget-Baustein „Backlog-Archivierung" in
`agent_scopes.md`; S172-Retro-M1/M2 laut §ev1 verworfen). **B-125 + B-126** (ein Brief):
B-125 `value=entry["damage"]`-Seed gegen Nach-Confirm-Nullung (Streamlit-Widget-Unmount-Gotcha);
B-126 neuer Helfer `dice_notation_max` → `max_value` datengetrieben aus `ability.effect.damage`
(D6→6/D3→3/N→N/unbekannt→None). **Stakeholder-verifiziert positiv** (beide Testfälle).
**B-122 „Careen!"** (Option A): neuer faktions-neutraler Effekttyp **`pre_explode_stratagem`**
(orks/stratagems.yaml), GO-Karte an Baustein ②, bucht CP via `cp_overrides` (WAGON/TITANIC→2),
löst den Explosions-Wurf NICHT aus; §7.1 + P-16 nachgezogen. Review: **GO, keine Blocker**.
Gates: **2144 passed, 99,20 %, Arch 8/8**, black/isort/ruff sauber.
**Token-Lehre (S173):** Brief-1-Executor ignorierte „Vollsuite synchron" → Background-pytest-Hänger
(S172-Muster!), Koordinator fuhr die Suite selbst 7 min im Vordergrund → Kontext-Überlauf > 135k.
Maßnahmen 1–3 in `S173_RETRO.md` (u. a. Retro-M1 doch übernehmen).

Frühere Sessions (S60–S172): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt (S174)

1. **S173-Retro entscheiden** (`S173_RETRO.md` NEEDS-DECISION): M1 (Vollsuite synchron doch
   übernehmen), M2 (Koordinator fährt keine Vordergrund-Gate-Suiten), M3 (Wind-down ab ~110k).
2. **Backlog-Archivierung** B-125/B-126/B-122 — eigener ~100k-Brief laut Retro-M3 (bewusst noch
   NICHT erledigt); stale B-125-Funktionsnamen in `backlog_details.md:604` beim Verschieben fixen.
3. **Careen!-UI-Verifikation** (`S173_careen_verifikation.md`, AWAITING-VERIFICATION) — inkl.
   Fenster-Entscheid GO-Karte sichtbar VOR vs. AB Wurf (Review-F1).
4. **Review-Nachzüge:** F1 §7.1-Careen!-Zitat an YAML/P-16 angleichen; F2 stale §1.7-Marker
   (Zeilen 197/253/276) entfernen; F3 überlange Baustein-②-Docstrings verschlanken.
5. Danach B-028c2 (`reroll_rp`) / Spyder-Konzept laut `backlog.md`.

**Offene Handoff-Marker:** `Stakeholder_Beobachtungen.md` (STANDING);
`S173_RETRO.md` (NEEDS-DECISION); `S173_careen_verifikation.md` (AWAITING-VERIFICATION);
`S173_explode_panel_verifikation.md` (verifiziert positiv → beim Archivieren abräumen).

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
