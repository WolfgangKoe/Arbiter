# Startprompt — Nächste Session
<!-- Kanonisch: .claude/tasks/next_session.md — nie ins Root-Verzeichnis anlegen. -->
<!-- Nur „Stand + nächster Schritt + offene Fragen". Historie → session_archive.md; Backlog → backlog.md. -->
<!-- Referenz NICHT hier: Architektur → architecture.md, Regel-Gotchas → rules_insights.md, Constraints → CLAUDE.md. -->

## ⚠️ Session-Regeln
- **Start „start next session" → Planner-Subagent beauftragen** (liest `CLAUDE.md` + `docs/goals/ziel7.md`
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
- **Start-Sync prüft auch `docs/handoff/` auf liegengebliebene ANSWERED/DONE-Dateien** (r-proto-02
  lag seit S116).
- **Executor-Aufträge enthalten die Klausel:** Dateiänderungen nur über Edit/Write-Tools, Bash nur
  lesend/git/pytest (Freigabe-Gate-Umgehung S123).
- **Zero-Error-Policy mypy:** Baseline sinkt jede Session weiter Richtung 0; Abweichung nach oben
  nur mit Begründung im selben Commit (z. B. mypy-Upgrade).
- **Parallel-Modus ist Standard für Ledger-Abbau:** dateidisjunkte Pakete + Koordinator-
  Konsolidierung (S128: 4 Pakete erfolgreich).
- **Parallel-Briefs:** Vorher-Messungen nur gegen `git show HEAD:` — **kein `git stash`** im
  geteilten Baum.
- **Jede Executor-Selbstprüfliste enthält `python tools/mypy_gate.py`** (S128: 18.1-Executor riss
  das Gate unbemerkt).

## Was ist Arbiter?
Digitaler Spielbegleiter WH40k 9E, Streamlit (Python). Start: `streamlit run src/app.py`
(Port 8501; **venv:** `source .venv/bin/activate`). Branch `feature/016` (Arbeit), `main` (nur PR).
**App permanent laufen lassen:** bei Session-Start nur kurz prüfen (`curl -s -o /dev/null -w "%{http_code}" http://localhost:8501` → 200), nur bei Bedarf neu starten — nicht den Nutzer fragen.

---

## Aktueller Stand (nach S128, 2026-07-06)

S128 (2026-07-06, 2 Commits: af3bc5a + Abschluss-Commit folgt): INV-4-Allowlist 5→3 (Roster-
Pflichtparameter statt necrons-Defaults); Plan 018.1 CP-Doppelvergabe gefixt (`cp_grants`-Set);
danach 4 PARALLELE Executor-Pakete: INV-4b-Ledger 11→6 nur LEGIT (inkl. Option B:
reanimationProtocols komplett aus src/, RP-Block YAML-getrieben via ability_engine-Helper),
mypy game_state 34→0 + gameObjects 18→0, Baseline 134→82; Plan 018.3 Gretchin
Cowardly/Attrition-Hinweis (Klasse C). Vollsuite 1496 passed, Coverage 99,12 %, Architektur
8/8, Review GO. UI Teil 2 vom Stakeholder verifiziert (bis auf Deny-Caption-Mini-Check, s. u.).

Frühere Sessions (S60–S127): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt

1. **BUG (Planungsgegenstand S129, Stakeholder-Auftrag):** Psychic-Phase-State-Blocker — Ork
   Weirdboy manifestiert (z. B. Smite, „Roll 7 — Manifested! Waiting for deny attempt… (W3
   mortal wounds)"), aber Gegner (Necrons) hat keine Deny-Fähigkeit („No PSYKER or deny
   wargear — cannot deny"): Das Spiel wartet trotzdem auf den Deny-Versuch, Schaden kann nicht
   angewendet werden; nur „Reset (skip Smite)" möglich. Erwartung: ohne gegnerische
   Deny-Fähigkeit den Deny-Wartezustand automatisch überspringen. Vermutlich
   `psychicPhase.py`-State-Machine. Regressionstest Pflicht.
2. Ledger-Abbau-Schritt (stehende Regel): mypy weiter senken — Reihenfolge gameMechanic/ →
   gameObjects/ (fertig) → uiLayout/ zuletzt.
3. Queue: Plan 018.2+18.4 offen, dann 015 → 026 → 017; 041 erst nach 015/026.

**Offene Verifikation (VOR Merge nach `main`):**
- **037 Docker**: `docker build` + `docker run --rm arbiter-test id -u` → 1000 +
  Port-7860-Smoke beim nächsten HF-Spaces-Deploy (lokal kein Docker).

**Offene Punkte / Merksätze:**
(b) ADR-0006:32 referenziert alten Pfad des 024-Digests (kosmetisch, bei Gelegenheit).
(c) Merkposten `hand_of_the_phaeron`/ExtraUses steht in Plan 032.
(d) Direction-Entscheide offen (Audit S124): ziel9-Fetcher vorziehen? Deployment-Phase
bauen oder ADR „bleibt am Tisch"? Mission-Scoring (eine Mission end-to-end)?
(e) Merkposten: 6 ungenutzte Loader-Funktionen (`load_points` u. a.) — Intent klären
(ziel9-Scaffolding?), dann löschen/behalten (Rejected-Liste plans/README).
(f) Retro S124: ab ~6 Plänen splitten oder Entwürfe an Sonnet delegieren.
(g) Retro S126: Lösch-Pläne → Executor-Selbstprüfliste MUSS entfernte Bezeichner
auch über `docs/spec/` greppen (S126-Blocker: 2 Specs beschrieben Gelöschtes).
(h) Retro S126: App VOR jeder UI-Verifikation neu starten (alter Prozess/State
lieferte 4 falsche ❌); UI-Prüfanleitungen vorher gegen Roster-Realität validieren
(Flayed-Ones-Check ohne Roster-Deckung, „Szenario-UI" existiert nicht — nur
`?scenario=`-Query-Param).
(i) Deny-Caption-Mini-Check (Psychic-Phase): 2. Deny-Versuch → neutrale Caption „one deny
attempt per phase per source" — einziger unbestätigter UI-Punkt aus S128, risikoarm.
(j) Fehlender R-Eintrag RP-Mechanik in `rules.md` (Akzeptanz-Katalog) — Planning klären.

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor **99 %**, `pyproject.toml`); **Schulden-Scoreboard** danach.
- Architektur: `pytest tests/architecture/ --no-cov -q`. Doku/Akzeptanz: `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor** <150k, bei ~135k beenden; Fleißarbeit PROAKTIV an Sonnet-Subagent.
- **Token-Report + History (M4, PFLICHT beim Abschluss):** `python tools/token_report.py --write` + `python tools/rotate_history.py --session <N> --summary "…"` — Koordinator stößt an.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt.
