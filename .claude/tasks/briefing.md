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

## Aktueller Stand (nach S183, 2026-07-24)

**S183 abgeschlossen.** **B-134 (Stale-UnitCard nach Damage-Apply) gefixt + archiviert:**
3 Inline-Schaden-Mutationen (`DAMAGE`-Apply-Button, Multi-Unit-Panel-Direct-Apply,
±-Wound-Adjustment) in `on_click`/`on_change`-Callbacks verlagert, `st.rerun()` ersatzlos
gestrichen (`src/uiLayout/_common.py`); Regressionstest
`test_damage_block_apply_mutates_before_render_returns_b134`; 2× unabhängiger Playwright-E2E-Beleg
(UnitCard ❤ 3/3 → ❤ 1/3 im selben Frame). Retro-M2 (toter Verweis `design_system.md:154`) + M3
(D2-Assert) mit erledigt. B-128(b)-Verifikation ✔ ausgewertet + gelöscht. Review S183: **GO**
(Auflage A1 = Screenshot mit committen → erfüllt; Minors → Retro M4/M5).
**Entscheide S183:** E1 = M2/M3/M4 angenommen, M1 zurückgestellt; E2 = B-134 vor B-028c3;
E3 = B-135-Fix „sofort" — Ausführung wegen Wind-down nach **S184** verschoben, Entscheid steht.

**Retro-Maßnahmen S183 (Stakeholder-Entscheid am S184-Start):** M1 = pytest-Hintergrund-Vorfall
trotz Foreground-Hook 2× über Executor-Umwege (gestallter T2 + Finisher-Subagent) → B-133 neu
bewerten; M2 = Screenshots `20-58-07`/`21-29-43`/`10-20-01`: Referenzen (u. a.
`backlog_details.md`) umbiegen, dann löschen (S169-M1-Regel); M3 = Planner-Budget unrealistisch
(~116k Ist vs. 60k — Brief enthielt Code-Verifikation); M4 = 1-Zeilen-Regressionstest für
`_wound_adjustment_click` (w-Button-Press, Review-Minor 1); M5 = number_input-„ohne-Enter"-Race =
bewusster Streamlit-Tradeoff, nur Awareness.

Frühere Sessions (S60–S182): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

## Zwischensession (2026-07-24, nach S183): Migrations-Handover erstellt

**Stakeholder-Auftrag (außerplanmäßig, KEINE reguläre Session):** Weiterentwicklung pausiert —
Streamlit stößt an Grenzen, Migration auf andere Technologie wird vorbereitet.
**Ergebnis:** `docs/migration_handover/` (8 MD-Dateien, framework-agnostisch, Englisch) als
Haupt-Input für den Rebuild: 00 Index · 01 Scope · 02 Working Features (nur Implementiertes,
gegen Code+Akzeptanz-Katalog verifiziert) · 03 Design-System (Streamlit-Workarounds markiert) ·
04 Architektur/Flow (portabel vs. Streamlit-Artefakt) · 05 Datenmodell/Loader-Ist-Stand ·
06 Domänen-Gotchas · 07 Streamlit-Pain-Points (7 Befunde → 6 Framework-Anforderungen).
4 Sonnet-Executor parallel + 1 Sonnet-Fact-Checker (~150 Referenzen, ~30 Verhaltens-Stichproben;
2 Befunde gefixt). Commits: `f185d10` + `27ccd90`.
**Wichtiger Befund:** `loader_contract.md`/`army_builder.md` beschreiben nie implementierte
API/Roster-Felder (Army-Dataclass, warlord, arkana, weapon_loadout) — Handover dokumentiert
Ist-Stand, Abweichungen explizit markiert (05 §3/§6.2/§8).
**Konsequenz für Planung:** Nächste Session klären, ob S184 (B-135 unten) noch stattfindet
oder die Migration Vorrang hat — Stakeholder-Entscheid.

### ▶ Nächster Schritt

1. **T4a/T4b aus S183-Plan (Rang 1, E3-Entscheid steht):** B-135 Performance — erst Messung
   (Rerun-Kosten pro Pfeil-Klick, `load_army`-Aufrufe im Hot-Path zählen), dann Caching-Fix
   (`get_wound_reroll_aura_donor_names`/`get_unit_rp_reroll_ability` u. a.); **schließt B-132
   mit ab**, wenn Messung die Hypothese bestätigt.
2. Retro-M1–M5-Entscheid (s. oben); `S183_REVIEW.md` sichten → danach löschen.
3. Danach B-028c-Reihe (c3 `free_attack` als nächstes Fachitem).

**Offene Handoff-Marker:** `Stakeholder_Beobachtungen.md` (STANDING); `S183_REVIEW.md`
(NEEDS-APPROVAL, nach Sichtung löschen); 5 Screenshots (`20-53-48` B-108 offen · `23-44-40`
B-134-Beleg, committet, Referenz jetzt im Archiv · `20-58-07`/`21-29-43`/`10-20-01`
Lösch-Kandidaten nach Referenz-Umbiegen, s. Retro-M2).

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
