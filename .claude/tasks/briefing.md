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

## Aktueller Stand (nach S182, 2026-07-23)

**S182 abgeschlossen.** B-128(b) DAMAGE-Block vereinheitlicht (`_render_damage_block`,
`src/uiLayout/_common.py`): D1 Label „Total damage dealt" → „Damage dealt", D2 neuer
leichtgewichtiger Sub-Header `caption("Enter damage taken")` in beiden Eingabepfaden, D3
`max_value=def_unit.models_max` für „Models lost" (fehlte vorher). D4 entschieden: **zwei
Eingabe-Konzepte bleiben** (nicht invertierbar wegen 9E-Schaden-Verfall). Spec
`design_system.md` §1.4.1 mit vollständigem DAMAGE-Block-Schema (ASCII + D1–D4) ergänzt,
neuer Render-Pfad-Test. **B-128 damit vollständig erledigt + archiviert.** M4 (zweiter
Aura-Spender Lokhust Lord) im Browser verifiziert → Marker geschlossen. Review: GO (1 Minor
M1 = toter Verweis `design_system.md:154` auf gelöschte Mockup-Datei; Nits N1–N3).

Vollsuite S182: **2188 passed, Coverage 99.08 %**; mypy 0==baseline; Doku-Gate 25 passed.

**Retro-Maßnahmen S182 (Stakeholder-Entscheid offen):** M1 = B-133 um `run_in_background`-
pytest-Blocker für Subagenten erweitern (Executor schlief erneut mit Hintergrund-pytest ein,
S172/S173-Muster); M2 = toten Verweis `design_system.md:154` angleichen/streichen; M3 =
group_wounds-Pfad-D2 im Test explizit assertieren; M4 = Screenshot-Bestand `docs/handoff/`
sichten + briefing-Zeile angleichen (N3: „2" genannt, 4 PNGs vorhanden).

Frühere Sessions (S60–S181): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt

1. **Stakeholder verifiziert im Browser:** B-128(b) DAMAGE-Block
   (`docs/handoff/S182_B128b_verifikation.md`, 2 Testfälle — group_wounds Silent King +
   Multi-Modell Lokhust Heavy Destroyers).
2. **B-028c-Reihe aufnehmen** (Rang 1–3: c3 `free_attack`, c4 `mark_target`, c5 `buff_roll`
   — alle nach B-028c1, parallel zueinander) bzw. neuer Rang-1 nach Stakeholder-Priorität.
3. B-132 (Loader-Caching-Prüfung) und B-133 (Git-Commit-Blockier-Hook) stehen als kleinere
   Schuldabbau-/Prozess-Items bereit, falls zwischengeschoben werden soll.

**Offene Handoff-Marker:** `Stakeholder_Beobachtungen.md` (STANDING);
`S182_B128b_verifikation.md` (AWAITING-VERIFICATION); 2 behaltene Screenshots (`20-53-48`
B-108 offen, `10-20-01` orphaned).

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
