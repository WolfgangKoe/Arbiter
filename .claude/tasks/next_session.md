# Startprompt — Nächste Session
<!-- Kanonisch: .claude/tasks/next_session.md — nie ins Root-Verzeichnis anlegen. -->
<!-- Nur „Stand + nächster Schritt + offene Fragen". Historie → ziel6.md; Backlog → backlog.md. -->
<!-- Referenzwissen NICHT hier: Architektur-Muster → architecture.md, Regel-Gotchas →
     rules_insights.md, Constraints → CLAUDE.md. -->

## ⚠️ Session-Regeln
- **Start "start next session" → Planning vorlegen** (Prioritäten + Token-Schätzung), erst nach
  Freigabe los; Shortcut „Plan ist freigegeben" = direkt los. **Lesen:** `CLAUDE.md` (Freigabe,
  bei Unklarheit fragen) + `docs/goals/ziel6.md` (Aufgaben/Historie) + `docs/goals/backlog.md`.
  Einstieg: `LEITSTAND.md`; Rollen/Tier/Events/Modi: `docs/governance/operating_model.md`.
- **Ende:** Review → Retro → **Maßnahmen-Entscheid** (Stakeholder wählt) → Abschluss: Checkboxen
  in `ziel6.md` + Historien-Zeile; **diese Datei** aktualisieren (ZUERST lesen, dann ergänzen).
- **Doku-Gate:** Decke **120** Zeilen (Test rot darüber). Beim Reißen **tief auf ≤ 70**
  kürzen, nicht knapp drunter — Erledigtes → `backlog.md`/`ziel6.md`, Referenz → s. o.
- **Freigabe vor Umsetzung; kein Memory/Skill(datei-ändernd) ohne Freigabe; Subagenten
  = stehende Freigabe (proaktiv, ohne Nachfrage, ADR-0005); rote vorher-grüne Tests =
  STOP + fragen.** Details: `CLAUDE.md`.

## Was ist Arbiter?
Digitaler Spielbegleiter für WH40k 9E, Streamlit (Python). Start:
`streamlit run src/app.py` (Port 8501; **venv aktivieren:** `source .venv/bin/activate`).
Branch `dev` (Arbeit), `main` (nur per PR).

---

## Aktueller Stand (nach S94, 2026-06-25)

**S94 (auf `feature/016`, Commit a7c67a6) — Repo aufgeräumt + Arbeitsweise geschärft.** `Refinement/` geleert
(Logo lag schon in `assets/`); 3 Foto-Ideen → backlog §2; Context-Engineering-Slides → `docs/reference/`;
Subagenten-Roster + gemeinsame Regeln in `operating_model.md`. **Retro-Befund:** Tiering missachtet (Recherche an
Sonnet statt Haiku), weil die Regel nicht im Session-Kontext aktiv war → Carry-over #0.

**S93 (auf `feature/016`) — Wurzel-Fix 1b/1c GEFIXT + UI-verifiziert. Vollsuite 1135 grün, 93,11 %.**
`_active_directive_effects(player)->list` aggregiert runden-zugewiesene + 6.-Protokoll/Affinitäts-Direktiven (alle 5
Engine-Reads); Dynastiebonus dadurch erstmals **wirksam** verdrahtet. +6 Regressionstests. **Offen (keine Regression):**
Eternal Guardian **S** (`reroll_save_1`) SAVE-Hinweis fehlt im Rendering → Plan 016 Group A (gemeinsamer
`_round_choice_reroll_hints`-Helper mit Conquering Tyrant S). Detail → ziel6.md-Historie.

**S92/S91/S90 (historisch):** Branch-Befund (`main` 331 Commits hinter `feature/016`, aktiv = `dev` =016−35; 016-only
`test_round_choice_player_keyed.py` beim 016→dev-Merge nachmigrieren); Mirror-Match-Kollision gefixt
(`round_choice_state_key(player,kind)`); Kontext-Engineering-Initiative gestartet; 3 Direktiv-/State-Bugs gefixt.
Detail → ziel6.md-Historie. Der S92-`chore/...`-Branch entfällt (Stakeholder-Entscheid S94: ein Branch, getrennte Commits).

### ⚠️ Carry-over (offen)
0. **Kontext-Engineering / Regel-Kuratierung (NEU priorisiert, eigene Session; verschmilzt mit Prinzipien-Revision #5).**
   Quelle liegt vor: `docs/reference/context-engineering-slides.md` (Write/Select/Compress/Isolate). Maßnahmen aus S94-Retro:
   - **(a) Session-scoped Regel-Injektion (Kern):** SessionStart-Hook + Regel-Index (Stichwort→Datei:Zeilen, verbatim heilig)
     lädt NUR die fürs aktuelle Session-Ziel relevanten Regeln in den Kontext — je Session andere. Behebt das Tiering-Versäumnis
     (Haiku-für-Lookups muss aktiv präsent sein). = „Select"-Hebel.
   - **(b) Subagent-Ergebnis → Datei statt in den Orchestrator-Kontext kippen:** Vertrag schreibt Ergebnis nach `docs/handoff/`,
     gibt nur Pointer + Kurzfazit zurück. = „Write/Isolate".
   - **(c) Handoff-Datei-Lebenszyklus:** Repo so strukturieren, dass jeder Agent schnell zu den Kernpunkten kommt → relevanten
     Kontext liest → arbeitet → auslagert → Datei löscht, wenn nicht mehr gebraucht (z.B. nach erfolgreicher Implementierung).
   - **(d)** governance-Doc `context_engineering.md` + ziel6.md-Kompression; `docs/handoff/context-audit-S91.md` verarbeiten + löschen.
   Prinzipien-Revision: Slides ↔ CLAUDE.md/operating_model abgleichen. Je eigene Freigabe.
0b. **Manuelle UI-Verifikation S91 (PFLICHT, Render-Code):** Necron-vs-Necron, Befehlsphase — Spieler-1-Protokoll/
   Direktive wählen → Spieler-2-Karte bleibt unverändert (eigene Wahl/Badge). Das war das Original-Symptom.
1. **Manuelle UI-Verifikation (S93-Stand):** (a) Eternal-Guardian-Save „(defender)" ✅; (b) Undying-Legions-P
   RP-Reroll-Hint ✅ (S93, RP-Hint darf optisch *deutlicher* — Design-Crew unten); (c) Living-Metal-S +1 ✅ (S93);
   (d) Bug 5: Runde-2-Fernkampf Zielwahl — **noch nicht geprüft**. **NEU:** (e) Eternal Guardian **S** reroll_save_1
   im SAVE-Block nicht als Buff angezeigt → Plan 016 Group A (siehe #3).
1b. **Vertagter S92-chore-Plan (Branch `chore/context-engineering-and-test-fixture` von `dev`, je Freigabe):**
   *Aufg. 4* Sonnet-Subagent zieht Präsentation (`curl -u andrena:slides4all
   https://peter-wegner-slides.pages.dev/context-engineering-andrena-v2/`, Inhalt = minifiziertes Vue-JS → Text
   extrahieren) → `docs/reference/context-engineering-slides.md` + Ideen für auto-`overview.md`. *Aufg. 3* neuer
   read-only Auditor (Sonnet) → `docs/handoff/context-audit-S92.md` (neue Dateien, NICHT die 8 aus S91); Optimierer
   arbeitet `context-audit-S91.md`-Findings #3/#4/#6/#7 ab (XS/S) + danach S91-Datei löschen; #1 ziel6.md-Kompression
   (L) eigener Slot. *Aufg. 1* Mock-Fixture: geteilte streamlit-Fixture in `tests/conftest.py`, 17 Testdateien von
   `_st_mock` auf `module.st` (Opus-Pilot 1 Datei → Sonnet-Subagent Rest → Opus-Review). Reihenfolge: 1b/1c-Fix zuerst.
2. **Bug 3 — Zweitspieler-Direktiv-Wahl (NEUER Plan-016-Step, Stakeholder „später"):** Direktive nur für
   aktiven Spieler in Befehlsphase wählbar (armyCard.py:296,307). Zweitspieler kann am Rundenanfang
   (= Gegner-Befehlsphase) nicht wählen. Step: Direktiv-Buttons entkoppeln (wählbar sobald Protokoll aktiv
   + Direktive offen, jede Phase) — neue UI-Logik, **eigene Freigabe**.
3. **Plan 016 Anzeige-Rest (Subagent-Slicing → `docs/audit/plans/016`):** *Group A* (~35k) Eternal Guardian S
   + Conquering Tyrant S reroll-Captions, gemeinsamer `_round_choice_reroll_hints`-Helper (Muster: `_rp_directive_hints`).
   *Group C* (~20k) Sudden Storm P „+N\" Move"-Badge (movementPhase) + Conquering Tyrant P Morale (Morale-UI fehlt evtl. → prüfen).
   **Steps 4/5 (Hungry Void S +1S, Vengeful Stars S AP-1) → Plan 017** (Stakeholder-Entscheid: Mathe+Anzeige
   unverdrahtet, überschneidet SAVE-AP-Badge). Dynastiebonus-Anzeige bereits erledigt (`_render_extra_round_choice`).
   Voice of the Triarch = eigener Plan.
4. **Reihenfolge:** Plan 016 Anzeige-Rest (Group A → C) → 018 → 015 → 017 (017 nimmt Steps 4/5 auf).

### Offene Fragen / Retro-Vormerke
- **S93-Maßnahme — Design-System-Crew (Stakeholder, eigene Session):** Subagenten-Gespann für *Designsystem +
  UI-Komponenten-Vereinheitlichung* (Opus plant/reviewt, Sonnet sucht Inkonsistenzen, Sonnet setzt um — oder 2×Sonnet).
  Erster konkreter Auftrag = einheitliche **Buff-/Direktiv-Hinweis-Komponente** (RP-Hint deutlicher, konsistent mit
  MWBD/SAVE-Badges); deckt zugleich Plan 016 Group A (reroll-Hints) ab. Code-Edits bleiben freigabepflichtig.
- **S93-Lehre Resolver-Blick:** bei „Engine oder Verdrahtung?" zuerst prüfen, *welche State-Klassen der zentrale
  Resolver liest* — `_active_directive_effect` ignorierte die ganze `extra_directive`-Klasse. Statische Analyse
  ersparte hier die freigegebene Debug-Probe + 1 Repro-Zyklus (ergänzt die S92-Lehre „Repro-zuerst", ersetzt sie nicht).
- **S93-Frage Freigabe-Gate:** Gate re-armte mitten in freigegebener Umsetzung (nach Kontext-Summarization/Continuation)
  und blockierte den Test-Edit. Prüfen, ob der Re-Arm nur bei echtem SessionStart statt bei Continuation feuern soll.
- **S92-Lehre Repro-zuerst:** bei „Engine oder Verdrahtung?" sofort Isolations-Repro schreiben statt langer statischer Analyse (spart Kontext).
- **S92-Lehre Branch-Check:** vor `git checkout -b … <base>` den aktiven Branch prüfen (`main` war 331 zurück; aktiv = `dev`).
- **S92-Lehre Plan-Realismus:** nicht 4 Aufgaben + Pflicht-Verifikation in einen Korridor; konservativer schneiden.
- **Doku-Sync ausstehend:** backlog #2 / ziel6 6e um Bug-3-Step + „Reset kampfrunden-weit" ergänzen (in S90 nur
  in dieser Datei). Bei nächstem Full-Wind-down nachziehen.
- **ADR-0006-Verweis (S86):** `CLAUDE.md` Token-Disziplin um Verweis auf ADR-0006 ergänzen (Subagent-Großausgaben als Datei).
- **INV-4b Restschuld:** `dynasty` (movementPhase), `gloom/prism` (psychicPhase → Cluster 5), `necrons`-Defaults
  (game_state/loader). Ratchet weiter schrumpfen.
- **Mock-Fragilität (backlog §4):** geteilte streamlit-Fixture (conftest) statt per-Datei-Mock.

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor 90 %, `pyproject.toml`).
- **Schulden-Scoreboard** nach jedem `pytest` (`tests/conftest.py`).
- Architektur (INV-1..4b): `pytest tests/architecture/ --no-cov -q`.
- Doku/Akzeptanz (INV-5): `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor:** <150k, bei ~135k Session beenden; Fleißarbeit PROAKTIV an Sonnet-Subagent.
- **Token-Report:** `python tools/token_report.py --write` → `docs/metrics/overview.md`.
- **History-Rotation:** `python tools/rotate_history.py --session <N> --summary "…"`.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt.
