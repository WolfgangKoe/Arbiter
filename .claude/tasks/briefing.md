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

## Aktueller Stand (nach S168, 2026-07-18)

**B-123 komplett** (Core-Fix T2 + UI-Nachzug T3, Stakeholder-verifiziert, archiviert): Root
Cause war ein per UI erzwungener directed-Zweig, der Schaden über den Restpool der gewählten
Gruppe hinaus verwarf (S166-Nachdiagnose). T2 (`src/gameMechanic/unitMutations.py`) lässt
Überschuss jetzt generisch über `_apply_group_wound_damage` spillen und generalisiert
`get_locked_group` um einen Zwangs-Lock für Einheiten mit `unit.has_per_group_wounds()` (im
YAML-Bestand nur der Silent King — Szarekh kann nicht mehr vor den Menhirs gewählt werden).
T3 (`src/uiLayout/_common.py`) bildet den Zwangs-Lock in `_render_subgroup_selector`/
`_render_damage_block` ab. Stakeholder-Verifikation S168 bestätigt Regelkonformität, äußert
aber deutliche Kritik an Design-System-Spec-Qualität (§1 keine schematische Bauform-Darstellung)
und am Warnhinweis-Wortlaut/Apply-Damage-Uneinheitlichkeit — beides bei **B-124** verankert
(`backlog_details.md`, Herkunft „T3-V S168"), nicht verloren. Details/Belege:
`docs/goals/backlog_archive.md` Abschnitt „migriert S168".

**§7-Explodes-Entwurf steht:** Pflicht-Trigger-Kachel-Spec für `design_system.md` liegt vor
(`docs/handoff/S168_SPEC7_ABNAHME.md`, NEEDS-DECISION) — Abnahme durch Stakeholder steht noch
aus, danach erst B-028c1-Code planen.

**Review S168: GO** (Pflicht-Korrektur aus diesem Abschluss eingelöst: B-123-Stale-Status in
`backlog_details.md` korrigiert + archiviert). Retro-Maßnahmen liegen als Entscheidungsvorlage
in `docs/handoff/S168_RETRO.md` (NEEDS-DECISION), noch nicht übernommen.

Frühere Sessions (S60–S167): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt (S169)

1. **Retro-Entscheid** (`docs/handoff/S168_RETRO.md`) — Maßnahmen-Liste sichten, auswählen,
   übernehmen.
2. **§7-Abnahme-Entscheid** (`docs/handoff/S168_SPEC7_ABNAHME.md`) — bei Abnahme
   B-028c1-Code planen (L-Effort → vorher splitten: Schema+Daten / Kachel-UI /
   auto_explode-GO als eigene Teil-Briefs) + Mockup-Dateien (`S166_MOCKUP_EXPLODES.md`,
   `S167_MOCKUP_EXPLODES_V3.html`, `_V2.html`, zugehörige Screenshots) löschen.
3. Weiteres laut `docs/goals/backlog.md`.

**Offene Handoff-Marker:** `Stakeholder_Beobachtungen.md` (STANDING); `S168_SPEC7_ABNAHME.md`,
`S168_REVIEW.md`, `S168_RETRO.md` je NEEDS-DECISION — Sichtung/Entscheid im S169-Planning.
Mockup-Dateien S166/S167 (`S166_MOCKUP_EXPLODES.md` + `S167_MOCKUP_EXPLODES_V3.html` + `_V2.html`
+ Screenshots) bleiben liegen bis zur §7-Abnahme.

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
