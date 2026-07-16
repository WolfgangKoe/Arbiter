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

## Aktueller Stand (nach S153, 2026-07-16)

S153 (Kurz-Session, Wind-down bei ~115k Kontext): Backlog-Feinschliff-Nachträge auf
Stakeholder-Zuruf — ID-Spalte einzeilig (nbsp-verbreiterter Tabellenkopf; Link-Syntax wegen
`test_backlog_structure`-Regex unangetastet), Effort-/Assignee-Spalten per `<br>` verschmälert
(91 Zeilen), Typ-Feld in `backlog_details.md` gefärbt (91×, Farben = Tabellen-Legende,
Zusatz-Anmerkungen B-089/090/091 ungefärbt; Template-Hinweis ergänzt). Docs+Acceptance-Gate
23 passed; Stakeholder hat die Struktur abgenommen. Umsetzung als offengelegter M2-Skript-Edit
(API-Session-Limit blockierte Subagent-Starts, Reset 20 Uhr; Marker-Selbst-Setzung vom
Klassifizierer design-konform verweigert, s. `tools/freigabe_gate.py`). **NICHT begonnen:**
das Arbeitspaket (a)–(f) unten — der Planner-Entwurf scheiterte am Session-Limit.
**Review/Retro der Kurz-Session steht aus** (Reviewer ebenfalls limit-blockiert) → S154.

Frühere Sessions (S60–S152): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt (S154 — Arbeitspaket aus S153 unverändert übernommen)

Priorität = `docs/goals/backlog.md` (einzige Quelle).

- **(0) Session-Start S154:** Planner-Entwurf für dieses Paket neu starten (S153-Versuch am
  API-Limit gescheitert, kein Entwurf entstanden) + Review/Retro-Nachholung S153 einplanen.

- **(a) UI-Nacharbeiten aus S152:** B-009 (zwei geeignete Rosters für PSI-Flow-Test benennen,
  dann Neuvorlage), B-087 (Fire-Overwatch/Counter-Offensive-Trigger-Timing gegen
  `docs/work/wahapedia_core_rules/` verifizieren, danach Neuvorlage; UI-Ausgrauen-Fix mit
  B-031 zusammen denken).
- **(b) B-056** Scope (b): Quantum Shielding Anzeige-Bug + neuer Mechanik-Typ „fester Invuln"
  fürs Stratagem.
- **(c) B-028** used-on-Suffix-Ausweitung auf alle reaktiven GOs (fest eingeplant).
- **(d) Ex-XS-Items, nicht blockiert (Stakeholder-Auftrag: einplanen + erledigen):** B-008 [erledigt,
  s.o.] — verbleibend: B-019, B-025, B-027, B-036, B-039, B-053, B-060, B-061, B-068, B-072,
  B-074 [erledigt, s.o.] — verbleibend: B-079, B-082.
- **(e) B-098 Teil 2** (Kombi-Waffen-Engine-Erweiterung: `weapon_swap` + Kombi-Mechanik).
- **(f) Retro-Maßnahmen umsetzen:** **M1** Planner-Briefs müssen Item-Mengen bei Format-
  Umbauten zählen (grep/wc), nicht schätzen → `docs/reference/agent_scopes.md`-Ergänzung.
  **M2** Werkzeug-Klausel präzisieren — script-gestützte Massen-Edits zulässig bei Offenlegung
  und grünem Gate-Beleg (B-099b-Vorfall als akzeptierter Präzedenzfall referenzieren).

**Offene Handoff-Marker:** `S147_go_audit_ork_abilities.md` + `S147_go_audit_stratagems.md`
(ANSWERED); `S141_ui_befunde_group_a.md` (ANSWERED, behalten bis FixC + FixD Brief 2/3);
`S150_usedon_renderpaths.md` (ANSWERED, behalten bis used-on-Generalkonzept);
`S152_review.md` (ANSWERED, DoD+Retro-Beleg); `S152_offene_ui_verifikationen.md` (ANSWERED,
Nacharbeiten B-009/B-087 offen, s.o.).

**Offene manuelle UI-Verifikation:**

- Spend-Guard (tisch-aufgelöstes Stratagem ohne Einheit) — blockiert bis Roster-Builder (B-067).
- B12b-Rest (Movement-Advance-Reroll-Randfall) — B-027, spec-konform, kein Bug.
- B-009 / B-087 — Nacharbeit + Neuvorlage S154 (s. oben).

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
