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

---

## Aktueller Stand (nach S155, 2026-07-17)

S155: Punkt 0 + Restpaket (a) komplett, 5 Commits (`ab36b80`…`ee6eb15`). E1 = Hypothese A
(Counter-Offensive regelkonform, core_rules.txt:3256) — Fix + UI-Hinweis committet, Stash
gedroppt. B-027 erledigt; `gretchin_mob` gelöscht; B-036/053/060/079/087 archiviert (B-079
war stale seit S118); B-025 umformuliert; M1+M2+R3 + neue Ablaufregeln verankert (Planner-
Prio-Sortierung, UI-Verifikationen immer als Handoff); **B-102 neu** (Box-Erreichbarkeit,
E1-Zusatzbefund). Gates: 1880 passed / 99,14 %; Arch+Doku+Acceptance 31 passed.
**S155-Review/Retro steht aus → Punkt 0 in S156 (R3-Regel, operating_model Event 1).**

Frühere Sessions (S60–S154): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt (S156)

Priorität = `docs/goals/backlog.md` (einzige Quelle, S156-Items stehen oben).

- **(0) S155-Review/Retro nachholen** (R3-Regel) — viel wurde fertig, Formal-Review lohnt.
  Außerdem: Ergebnis der Stakeholder-UI-Verifikationen einsammeln
  (`docs/handoff/S155_ui_verifikationen.md`, NEEDS-DECISION).
- **(a) Engine-Welle (je ~35k, einzeln an M-Obergrenze):** B-056 Quantum Shielding ∥
  B-098 Teil 2 Kombi-Waffen (disjunkt, aus S155 verschoben — Budget-Punkt 4 des
  freigegebenen S155-Plans). Danach B-028 used-on-Generalisierung (zuerst reaktive
  Non-Stratagem-GOs ZÄHLEN; NICHT parallel zu B-056, beide `_common.py`).

**Offene Handoff-Marker:** `S155_ui_verifikationen.md` (**NEEDS-DECISION**, 4 Prüfblöcke);
`S155_planning.md` (ANSWERED, behalten bis B-056/B-098/B-028 umgesetzt);
`S154_offene_entscheide.md` (ANSWERED, behalten bis PSI-Flow-Verifikation erledigt);
`S154_planning.md` (ANSWERED, Restpaket in S155 umgesetzt → löschbar nach S155-Review);
`S147_go_audit_ork_abilities.md` und `S147_go_audit_stratagems.md` (ANSWERED);
`S141_ui_befunde_group_a.md` (ANSWERED, behalten bis FixC + FixD Brief 2/3);
`S150_usedon_renderpaths.md` (ANSWERED, behalten bis B-028); `S152_review.md` (ANSWERED).

**Offene manuelle UI-Verifikation:** vollständig in `docs/handoff/S155_ui_verifikationen.md`
(neue Ablaufregel: immer dort, nie nur hier) — Counter-Offensive-Hinweis, used-on-Suffix
Advance-Reroll + Overwatch, Silent-King-Defaults, PSI-Flow; Spend-Guard weiter blockiert
bis Roster-Builder (B-067).

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
