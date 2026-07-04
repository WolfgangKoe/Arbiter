# Startprompt — Nächste Session
<!-- Kanonisch: .claude/tasks/next_session.md — nie ins Root-Verzeichnis anlegen. -->
<!-- Nur „Stand + nächster Schritt + offene Fragen". Historie → session_archive.md; Backlog → backlog.md. -->
<!-- Referenz NICHT hier: Architektur → architecture.md, Regel-Gotchas → rules_insights.md, Constraints → CLAUDE.md. -->

## ⚠️ Session-Regeln
- **Start „start next session" → Planner-Subagent beauftragen** (liest `CLAUDE.md` + `docs/goals/archive/ziel6.md`
  + `docs/goals/backlog.md`, Scope aus `docs/reference/agent_scopes.md`); Entwurf als Datei, Koordinator
  legt vor, erst nach Freigabe los. Shortcut „Plan ist freigegeben" = direkt los. Einstieg `LEITSTAND.md`;
  Rollen/Tier/Modi: `docs/governance/operating_model.md`.
- **ADR-0007 (verbindlich seit S102):** Koordinator routet — liest keine Quelldateien/Vollergebnisse;
  Detail-Planung → Planner-Subagent; finales Review → Reviewer-Subagent. Asynchrone Stakeholder-
  Entscheidungen über Mailbox (`docs/handoff/`, NEEDS-DECISION → ANSWERED), nicht Chat.
  Details: `docs/governance/operating_model.md` [#events].
- **Ende:** Review (Reviewer-SA) → Retro → **Maßnahmen-Entscheid** (Stakeholder wählt) →
  Abschluss: **diese Datei** aktualisieren (ZUERST lesen, dann ergänzen) + ggf. Ziel-Checkboxen.
- **Doku-Gate:** Decke **120** Zeilen (Test rot darüber). Beim Reißen **tief auf ≤ 70** kürzen —
  Erledigtes → `backlog.md`/`session_archive.md`, Referenz → s. o.
- **Freigabe vor Umsetzung; kein Memory/Skill(datei-ändernd) ohne Freigabe; Subagenten =
  stehende Freigabe (proaktiv, ADR-0005); rote vorher-grüne Tests = STOP + fragen.** → `CLAUDE.md`.
- **Checkbox-Sync prüft auch Commit-Behauptungen:** Session-Start-Sync nicht nur gegen Ziel-Checkboxen,
  sondern auch Titel wie „archive/close" gegen Datei-Realität verifizieren (b3ebfd5 behauptete
  Archivierung ohne Vollzug, S119→S120-Befund). Restrisiko bewusst nicht test-bewacht — Kompensation:
  Reviewer-Pflicht + dieser Sync.

## Was ist Arbiter?
Digitaler Spielbegleiter WH40k 9E, Streamlit (Python). Start: `streamlit run src/app.py`
(Port 8501; **venv:** `source .venv/bin/activate`). Branch `feature/016` (Arbeit), `main` (nur PR).
**App permanent laufen lassen:** bei Session-Start nur kurz prüfen (`curl -s -o /dev/null -w "%{http_code}" http://localhost:8501` → 200), nur bei Bedarf neu starten — nicht den Nutzer fragen.

---

## Aktueller Stand (nach S122, 2026-07-04)

**S122:** F3 (nat. 1 = Miss + Save-Floor 2+, `8ae7252`; Nachfix Eff.-Anzeige 2+/grün + Mini-
Zeilen-×, `abc4256`) · F1 (Disruption Fields = Stärke-Modifier, `0c54fe7`) · Plan 015 Step 1
war bereits durch Ziel7 Stufe A abgedeckt (`4effd99`, Steps 2–4 offen). Stufe-B-Scoping:
59/59 Stratagems, Conditions nur STICHPROBE → Pflichtauftrag (a). Mehrphasen-Verdrahtung
geprüft: korrekt. Review **GO**, UI-Verifikation F1+F3 bestätigt ✅. Retro M1 (Anzeige-
Pfad-Beleg) in `agent_scopes.md`.

Frühere Sessions (S60–S121): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt

Planungskandidaten S123 (Stakeholder priorisiert im Planning):
(a) **PFLICHT (Stakeholder: „AUF JEDEN FALL"): vollständiger Feld-Abgleich der modifier-/
Effekt-Semantik** aller Necron-Stratagems gegen Wahapedia — Stichproben reichen nicht, jede
Diskrepanz finden (Anlass: F1 war genau so ein Fall; Review-Befund: `stratagem_strength_bonus`
summiert ohne `unit_key`-Scoping — mitprüfen);
(b) **Audit-Pläne bereinigen** (Backlog §2, Sonnet-Durchgang, vor /improve);
(c) **/improve-Session vorbereiten** (Backlog §2, eigene Session);
(d) **Plan 015 Steps 2–4** (Mockup-Gate VOR Step 2) / ziel7 **Stufe B** Umsetzung, **C** (Orks;
inkl. Boarding-Actions-Entscheid + variable CP-Kosten-UI, Backlog §2).

**Merksatz S122:** Bei UI-relevanten Fixes den *angezeigten* Wert belegen (HTML-Output-Test) —
Anzeige-Code kann lokal neu rechnen und den Mechanik-Fix ignorieren (Eff.-1+-Wiring-Gap).

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor **99 %**, `pyproject.toml`); **Schulden-Scoreboard** danach.
- Architektur: `pytest tests/architecture/ --no-cov -q`. Doku/Akzeptanz: `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor** <150k, bei ~135k beenden; Fleißarbeit PROAKTIV an Sonnet-Subagent.
- **Token-Report + History (M4, PFLICHT beim Abschluss):** `python tools/token_report.py --write` + `python tools/rotate_history.py --session <N> --summary "…"` — Koordinator stößt an.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt.
