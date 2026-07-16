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

## Aktueller Stand (nach S154, 2026-07-16)

S154 (parallelisierte Session, 9 Subagenten in 2 Wellen): Review/Retro S153 nachgeholt
(**GO**). Erledigt + committet: B-019/B-072 (`e7fa4ca`), B-068 (`30da597`; korrekte Werte
Staff 3 / Scythe 4, Backlog nannte sie vertauscht), B-039/061/082 archiviert. B-009:
Testpaar `orks.yaml` vs `necrons_test.yaml` benannt. B-087: Counter-Offensive-Timing-Bug
gefixt (`_enemy_has_fought`), **UNKOMMITTIERT** bis E1-Entscheid (2 Alt-Tests ersetzt =
Verhaltensbruch). B-053: `gretchin_mob` = 8E-Relikt ohne Referenzen, Lösch-Empfehlung (E3).
B-025: strukturell (CLS≈0.29), kein Quick-Fix, bleibt offen (E4). **B-036: Stakeholder-
Entscheid „archivieren" liegt vor, Umsetzung scheiterte 2× an API 529 → S155 Punkt (0).**
Gates: Vollsuite 1878 passed / 99,14 %; Architektur+Doku+Acceptance 31 passed.
Alle offenen Entscheide inkl. Erläuterungen: `docs/handoff/S154_offene_entscheide.md`
(NEEDS-DECISION). Prozess-Lernpunkt (Stakeholder-Rüge): Entscheide SOFORT in die Mailbox,
nicht nur in den Chat → Retro-Kandidat S155.

Frühere Sessions (S60–S153): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt (S155)

Priorität = `docs/goals/backlog.md` (einzige Quelle) + `docs/handoff/S154_offene_entscheide.md`.

- **(0) Entscheide sind da** (`S154_offene_entscheide.md`, ANSWERED): **E1 = neuer Befund
  „Counter-Offensive gar nicht sichtbar"** — Fix liegt in `git stash` (stash@{0},
  „B-087 Counter-Offensive fix – E1"); zuerst reproduzieren (Hypothesen A/B im
  Koordinator-Vermerk der Datei), dann Stash anwenden+nachbessern oder verwerfen.
  Außerdem: B-036-Archivierung nachholen (2× API-529 gescheitert), E3 `gretchin_mob`
  löschen (freigegeben), E4 B-025 umformulieren, R3 VERWORFEN (nicht verregeln; kein
  Formal-Review, wenn in einer Session nichts fertig wurde — Token nicht um der Regel
  willen verschwenden). Kurzes S154-Review als Teil von Punkt 0 (viel wurde fertig).
- **(a) S154-Restpaket (klein):** M1+M2 (`agent_scopes.md`, EIN Brief), B-060
  (CLAUDE.md-Token-Details → operating_model.md Event 6; Stakeholder-freigegeben S154),
  B-027 (unit_key durch spend_stratagem), B-079 (diceHtml DRY-Helper).
- **(b) Engine-Aufgaben (je ~35k, einzeln an M-Obergrenze):** B-056 Quantum Shielding,
  B-028 used-on-Generalisierung (zuerst reaktive Non-Stratagem-GOs ZÄHLEN), B-098 Teil 2
  Kombi-Waffen. Parallelität: B-056∥B-098 möglich (disjunkt); B-028 NICHT parallel zu
  B-056 (beide `_common.py`).

**Offene Handoff-Marker:** `S154_offene_entscheide.md` (**NEEDS-DECISION**, E1–E4);
`S154_planning.md` (ANSWERED, behalten bis Restpaket umgesetzt); `S147_go_audit_ork_abilities.md`
und `S147_go_audit_stratagems.md` (ANSWERED); `S141_ui_befunde_group_a.md` (ANSWERED, behalten
bis FixC + FixD Brief 2/3); `S150_usedon_renderpaths.md` (ANSWERED, behalten bis used-on-
Generalkonzept); `S152_review.md` (ANSWERED, DoD+Retro-Beleg); `S152_offene_ui_verifikationen.md`
(ANSWERED, B-009/B-087 in S154 nachgearbeitet → nach E1-Umsetzung löschbar).

**Offene manuelle UI-Verifikation:**

- Spend-Guard (tisch-aufgelöstes Stratagem ohne Einheit) — blockiert bis Roster-Builder (B-067).
- B12b-Rest (Movement-Advance-Reroll-Randfall) — B-027, spec-konform, kein Bug.
- **Neu S154:** Counter-Offensive-Box erst nach gegnerischem Fight (E1); Silent-King-
  Attacken-Defaults 3/4; PSI-Flow mit `orks.yaml` vs `necrons_test.yaml` (Anleitung in
  `S154_offene_entscheide.md`).

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
