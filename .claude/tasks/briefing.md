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

## Aktueller Stand (nach S169, 2026-07-19)

**Spec-Struktur-Korrektur (Stakeholder-Entscheid S169):** `design_system.md` definiert nur
noch GENERISCHE Bausteine — neu §1.5–1.9 (Pflicht-Trigger-Kachel, Binär-Wurf, Multi-Unit-
Ziel-Panel, Info-Hinweiskasten, Layout-Invariante; je mit Pflicht-ASCII-Schema, Retro-M1 in
`agent_scopes.md` verankert), §3.1 Wortlaut-Budget (M2), generisches §7. Feature-Spezifisches
in `processes.md`: **P-16 Explodes** (inkl. 5 Referenz-Screenshots) + P-08-Ergänzung (aus
§4.4 migriert — Stakeholder sagte „§6", T2 interpretierte §4.4; Bestätigung offen, s. Retro).

**B-028c1 b1+b2 GEBAUT (In Progress, nicht abgehakt):** b1 = `effect.type: explode`
(`roll_threshold`/`radius`/`damage`) + `mandatory`-Achse, `resolve_explode_effect` ohne
Engine-Selbstwurf, 5 Träger Wahapedia-belegt (Silent King, Triarch Stalker, Annihilation
Barge, Night Scythe, Gunwagon; Spyder bewusst ausgelassen — Mehrmodell, eigenes Konzept
nötig). b2 = Pflicht-Trigger-Kachel in allen 5 `*Phase.py` (center, selektionsunabhängig),
Binär-Wurf, Ziel-Panel beider Armeen, B-124(a)-Warnhinweis gekürzt. Gates: 2066 passed,
Coverage 99,18 %, Arch 8/8, Nenner 159/Ledger 0. **UI-Verifikation offen**
(`S169_b2_ui_verifikation.md`). b3 (`auto_explode`-GO) → S170.

**Handoff aufgeräumt:** 12 Dateien gelöscht; Review-NO-GO wegen 3 verwaister Referenzen
noch in S169 per Pflicht-Korrektur ausgeräumt (Lehre → Retro-Maßnahme 1: Referenz-Grep vor
Löschung für ALLE Dateitypen). **Retro-M3 (Bash-Allowlist) wartet auf Stakeholder**
(`S169_M3_ALLOWLIST.md`) — Classifier blockiert Claude-seitige Permission-Änderungen.

Frühere Sessions (S60–S168): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt (S170)

1. **Retro-Entscheid** (`docs/handoff/S169_RETRO.md`) — 3 Maßnahmen + 2 offene
   Stakeholder-Punkte (b2-UI-Verifikation, §6-vs-§4.4-Bestätigung).
2. **b2-UI-Verifikation einlösen** (`S169_b2_ui_verifikation.md`) — bei GO B-028c1
   b1+b2 abhaken; danach **b3 `auto_explode`-GO** (~M, eigener Brief).
3. **M3-Allowlist** (`S169_M3_ALLOWLIST.md`) — Stakeholder trägt selbst ein.
4. Weiteres laut `docs/goals/backlog.md` (B-124(b) Apply-Damage; Spyder-Explodes-Konzept).

**Offene Handoff-Marker:** `Stakeholder_Beobachtungen.md` (STANDING);
`S169_RETRO.md` + `S169_M3_ALLOWLIST.md` (NEEDS-DECISION);
`S169_b2_ui_verifikation.md` (AWAITING-VERIFICATION); `S169_REVIEW.md` (NEEDS-DECISION —
NO-GO-Befund per Pflicht-Korrektur noch in S169 ausgeräumt, nur noch Sichtung);
`S169_PLANNING.md` (nach Sichtung löschen).

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
