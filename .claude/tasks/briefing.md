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

## Aktueller Stand (nach S175, 2026-07-20)

**S175 committet:** **B-028c2 `reroll_rp` umgesetzt** — Class-B-Hinweis (App erinnert,
würfelt/rechnet nicht) für die Necron-Unit-Ability „Their Number is Legion": neue Funktion
`get_unit_rp_reroll_ability()` (`abilityEngine.py`, `load_unit_abilities` + `check_conditions`,
analog `_wound_auto_fail_ability`) + Caption-Funktion `_rp_unit_ability_hints()`
(`uiLayout/_common.py`), eingehängt in `_render_rp_block` neben dem unveränderten Direktiv-Pfad.
UI-Verifikation **positiv** bestätigt (`S175_B028c2_verifikation.md`, gelöscht nach Abschluss).
**B-121 + B-110 Schuldabbau**: toter `load_deny_wargear_names`-Produktionscode (`loader.py`) samt
Cache + zugehöriger Tests entfernt; latenter `p.name`→`p.name_en`-Bug im Melee-Profil-Zweig
(`_common.py:3905`) konsistent zum bereits gefixten Ranged-Zweig korrigiert. **B-122 Careen!
verifiziert + archiviert**: Stakeholder-Befund S173 positiv, F1-Fensterentscheid (GO-Karte
bleibt sichtbar, erzwingt nichts, P-16 „vor-Wurf-GO") verankert, §7.1-Zitat auf den wörtlichen
Orks-Regelwortlaut korrigiert; D6-Umgebungsschaden-Rückfrage geklärt (läuft über B-049, außerhalb
Scope). Alle vier Items (B-028c2, B-121, B-110, B-122) samt Detail-Abschnitten nach
`backlog_archive.md` verschoben. **Retro-Maßnahmen S174→S175:** M1 (Stakeholder-Wunsch: RP-Hinweise
als blauer §3-Hinweis-Block statt schwacher `st.caption`) als neues Item **B-127** aufgenommen;
M2 (Konzept-Vorlagen sollen den realen Datenort/Loader per `grep` verifizieren statt aus dem
Gedächtnis benennen, S175-F1-Lehre) in `agent_scopes.md` Planner-Pflichten ergänzt.
Review S175: **GO**; Gates **2151 passed, Coverage 99,20 %, Architektur 8 passed**.

Frühere Sessions (S60–S174): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt (S176)

1. **B-005 Direktiv-Lock-Rest** — sobald DoR (Regel-Scope in `backlog_details.md`) befüllt ist;
   Protokoll-Direktiven ab der Bewegungsphase sperren, reiner Render-Pfad (`armyCard.py`),
   erneute manuelle UI-Verifikation nötig.
2. **B-127** — RP-Hinweise (Direktiv + `reroll_rp`) von `st.caption` auf den blauen
   §3-Hinweis-Block umstellen (XS, Stakeholder-Wunsch aus der B-028c2-Verifikation).
3. Weitere Ziel-7-Items laut `backlog.md`-Priorität (z. B. B-028c3/c4/c5, B-113, B-107/B-077/B-006).

**Offene Handoff-Marker:** `Stakeholder_Beobachtungen.md` (STANDING).

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
