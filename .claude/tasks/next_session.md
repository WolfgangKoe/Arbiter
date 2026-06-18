# Startprompt — Nächste Session
<!-- Kanonisch: .claude/tasks/next_session.md — nie ins Root-Verzeichnis anlegen. -->
<!-- „Was next" + Stand. Erledigte Session-Historie → ziel6.md; offener Backlog → backlog.md. -->

## ⚠️ Session-Regeln (immer beachten)

**Session-Start:** `CLAUDE.md` (Workflow, Freigabe-Pflicht, Unklarheiten zuerst fragen)
+ `docs/goals/ziel6.md` (Aufgaben/Historie) + `docs/goals/backlog.md` (offener Backlog).
Einstieg/Gesamtübersicht: `LEITSTAND.md`; Rollen/Model-Tier/Events/Modi: `docs/governance/operating_model.md`.

**Session-Ende:** Checkboxen in `ziel6.md` abhaken + Zeile in die Session-Historie;
**diese Datei** aktualisieren (ZUERST lesen, dann ergänzen — nie blind überschreiben).
Doku-Gate hält diese Datei unter 160 Zeilen — Erledigtes nach `backlog.md`/`ziel6.md` auslagern.

---

## Was ist Arbiter?

Digitaler Spielbegleiter für Warhammer 40.000 9. Edition, Streamlit (Python).
Start: `streamlit run src/app.py` (Port 8501). Branch `dev` (Entwicklung), `main` (nur per PR).

---

## Aktueller Stand (nach S57, 2026-06-18)

**S57 — Operating-Model Phase B: Token-Report.** `tools/token_report.py` (neu) führt
Haupt-Session- und Subagent-Verbrauch **getrennt** zusammen — parst `*.jsonl` (main) +
`*/subagents/*.jsonl` (sidechain) aus dem Projekt-Transcript-Verzeichnis, summiert je
Modell-Tier (Opus/Sonnet/Haiku/Fable) und je Session, rendert Markdown. CLI:
`python tools/token_report.py [--session <id>] [--write]`. Report → `docs/metrics/overview.md`
(neu), aus `LEITSTAND.md` Feld 4 verlinkt. Reine Aggregation getestet
(`tests/tools/test_token_report.py`, 6 Tests — tools/ ist nicht coverage-gemessen,
Netz trotzdem da). Generic-src/Arch-Gate/UI: n/a (Tool außerhalb `src/`, kein Streamlit).
**Retro → ADR-0002:** stakeholder-gerichtete Artefakte (Leitstand/Reports/Gates) sind für den
Leser, müssen seine Fragen beantworten; Retro fester Teil von Event 5. Folge im Backlog:
**Token-Report v2** (lesbare Labels, jüngste oben, Σ-Beschriftung, Subagenten + Aufgabe, Diagramm)
+ „Gates leser-orientiert prüfen".

**S56 — Operating Model etabliert (Aufbau-/Ablauforganisation).** Governance-Schicht nach
Luhmann/integraler Sicht: `docs/governance/operating_model.md` (Rollen, Model-Tier inkl. Haiku-
Lookup, 7 Events, 4 Entscheidungsmodi Gate/Konsent/Konsens/Veto, Eskalationswege + 2 Diagramme).
`LEITSTAND.md` = Einstiegstür (verlinkt alles, dupliziert nichts). ADR-Log `docs/governance/
decisions/` + ADR-0001 (explizites „Ja" bleibt Probe-Session, Review in Retro). `docs/inbox/`
Refinement-Fluss für `Fotos/`. CLAUDE.md: Artefakt-Landkarte + Haiku-Tiering ergänzt. Doku-only
(keine Tests berührt). **Manuell zu prüfen:** Mermaid-Diagramme im Viewer. Sonnet-Subagent schrieb
die 4 Doku-Dateien (28,9k Token, isoliert), Opus reviewte + finalisierte ADR-0001/CLAUDE.md.

**S55 — Regel-Katalog: Bereich Command Phase ausgerollt.** 14 Einträge `R-CMD-01..14`
(Sonnet-Subagent erfasst die Fleißarbeit, Opus reviewt/finalisiert) in `rules.md`. Nenner jetzt
**48** (34 Combat + 14 Command). Scoreboard: A 22/41 (54%) · B 0/6 · C 1/1; Ledger **7** (2 Combat
+ 5 neu: R-CMD-03/04/10/11/12); Konsistenz grün. Befund R-CMD-03 (CP-Grant ohne Battle-forged-
Gating) → `backlog.md`. Doku-Drift: 6e-Task `cp_granted_this_phase` war erledigt, jetzt abgehakt.
852 Tests grün, Coverage 88.45 %.

**S54 — Regel-Katalog Phase 1 Gate (read-only).** `rules.md` ins Schulden-Scoreboard
verdrahtet: Abdeckung % je Klasse (A 16/29 · B 0/4 · C 1/1), Ledger-Größe (2: R-COMBAT-09,
R-COMBAT-17) und Konsistenz-Check (jeder `getestet: ja`-Testname existiert in `tests/`).
Parser `tests/acceptance/_rules.py` (regex/disk, keine Test-Collection, mirror `_acceptance.py`).
Reine Messung — kein hart-roter Gate-Test (auf Ansage). 852 Tests grün, Coverage 88.45 %.

**S53 — Regel-Abdeckung (Akzeptanz-Katalog) + Arbeitsweise verankert.** Neuer Nenner
`docs/spec/acceptance/rules.md`: Combat-Katalog als verbindliche Vorlage (34 Regeln, Klasse
A/B/C, stabile `datei:funktion`-Refs + Testnamen). Arbeitsweise in `CLAUDE.md` festgehalten:
Token-Korridor <150k / 90%-Wind-down, Subagent-für-Fleißarbeit (Sonnet) + Opus-Review,
getrennte Messung. Noch kein Gate verdrahtet (pytest unverändert).

**S52 — INV-4b: `protocol`/`protocols`-Vokabular aus `src/` entfernt.** Verifizierte Umbenennung
auf `round_choice` (kein Verhaltenswechsel); Details in `ziel6.md`/`architecture_invariants.md`.

### ✅ S56 erledigt — Operating Model statt loser Prämissen

Der S55-Wunsch „Arbeitsmuster formalisieren" ist umgesetzt: nicht nur Prämissen-Stichworte,
sondern eine ganze Governance-Schicht (`docs/governance/operating_model.md` + `LEITSTAND.md` +
ADR-Log). Rollen/Tier/Modi/Events/Eskalation dort kanonisch. Offen (optional, erst auf Ansage):
hartes Gate für Prämissen-Konformität (analog Scoreboard). Phase B/C siehe `backlog.md`.

### ▶ Nächster Schritt — Regel-Katalog weiter ausrollen / Ledger abbauen

Stand: `rules.md` deckt **Combat** (34, R-COMBAT-01..34) + **Command Phase** (14, R-CMD-01..14)
ab; Nenner **48**, Phase-1-Gate read-only im Scoreboard (Abdeckung %, Ledger, Konsistenz). Vorlage
steht, Sonnet-Subagent-Muster erprobt (S55). Fixe Entscheidungen: Granularität = **Mechanik-Schritt**;
Klasse A (App rechnet) / B (nur Tisch → Hinweis) / C (Hybrid).

Offene Optionen (je eigene Freigabe): (1) **weiterer Bereich** per Sonnet-Subagent — Movement /
Charge / Morale (~30–80k/Bereich); (2) **Ledger schrumpfen**: 5 R-CMD-Schulden
(R-CMD-03/04/10/11/12) + 2 Combat (R-09/R-17) als Tests nachziehen (Ratchet → nur kleiner).
Phase 3 (Token-Report) ✅ S57. Optional: Phase-1-Gate **hart-rot** (Konsistenz + Ledger-Ratchet
als echte Tests) — erst auf Ansage. Findings: `backlog.md`.

### ▶ Danach — Schulden weiter abbauen + offene Findings (`backlog.md`)

1. **INV-4b Ledger weiter schrumpfen:** benannte Items (`orb`, `overlord`, `phaeron`, `irongob`,
   `gloom`, `prism`, `dakka`, `klaw`, `tesla`, `reanimation`, `arkana`, `dynasty`) aus Phasen-/
   Render-Modulen in YAML/Daten ziehen (`protocol`/`protocols` ✅ S52).
2. **INV-4 Allowlist schrumpfen** (`test_generic_src.py`): Default-Roster/`faction_dir`-Default/
   Spielerlabels aus den gewählten Armeen ableiten statt hartkodieren.
3. **Test-Mock-Fragilität** (backlog §4): geteilte `streamlit`-Fixture (conftest) + `module.st`.
- **Phase 3 — #2 Buff-Audit:** 9 nicht-verdrahtete Direktiv-Effekte einzeln anzeigen (backlog §0).
- **Phase 4 — #3/#4 Würfel:** Soll-Bild **erst als AC mit Nutzer** abstimmen.
- **Coverage-Fahrplan:** Floor 88 %. Pure Logik aus `omit`-Modulen in getestete Helfer ziehen.

---

## Gate-Netz (Messbefehle)

- Tests + Coverage: `pytest --tb=short` (Floor 88 %, `pyproject.toml`).
- **Schulden-Scoreboard**: erscheint nach jedem `pytest`-Lauf (Hook in `tests/conftest.py`) —
  Fraktions-Vokabular-Tokens, Namen-Allowlist, AC-IDs, next_session-Zeilen. Baseline 2026-06-16
  in `architecture_invariants.md`. Ziel: Vokabular-/Allowlist-Zahlen sinken pro Session.
- Architektur (INV-1..4b): `pytest tests/architecture/ --no-cov -q` · Ledger: `architecture_invariants.md`.
- Doku + Akzeptanz (INV-5): `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- Neues Akzeptanzkriterium: AC in `docs/spec/acceptance/index.md` + `@acceptance("AC-…")`-Test (README dort).
- **Regel-Katalog** (Nenner): `docs/spec/acceptance/rules.md` — Klasse A/B/C, `getestet: ja — <testname>`.
  Seit S54 im Scoreboard (read-only): Abdeckung % je Klasse, Ledger, Konsistenz-Check. Parser:
  `tests/acceptance/_rules.py`. Noch kein hart-roter Gate-Test (auf Ansage scharfschalten).
- **Token-Korridor:** <150k, bei ~135k Session beenden. Fleißarbeit an Sonnet-Subagent (CLAUDE.md).
- **Token-Report:** `python tools/token_report.py --write` → `docs/metrics/overview.md` (Haupt vs. Subagent, je Tier/Session).

---

## Wichtige Constraints (unveränderlich)

- **Freigabe vor Umsetzung** — Plan + Dateiliste zeigen, auf „ja" warten. **Planergänzung ≠ Freigabe.**
- **Kein Memory/Subagent/Skill ohne Freigabe.** dev-Branch, kein direktes Committen auf main.
- **Rote vorher-grüne Tests = STOP + Nutzer fragen** (nie still anpassen).
- Seitenleisten: `first_player` links, `second_player` rechts (unveränderlich).
- Keywords immer `UPPERCASE` in YAML. Regelreferenz: immer erst lokal (`docs/work/wahapedia_*/`), nie Nutzer fragen.
- **Generisch:** keine Fraktions-Checks/-Vokabeln in `src/` — alle Fraktions-Entscheidungen über YAML (INV-4/4b).
- Waffenstärke: `_parse_strength(raw, unit_strength)` — nie `int(strength)` direkt. YAML: int = fest,
  `"+N"` = User+N, `"×N"` = User×N, `"User"` = User.

---

## Architekturmuster

- **ModelGroup (6m):** strukturell verschiedene Modelle via `model_groups` in `units.yaml`
  (homogen / strukturell gemischt `count: remainder` / per-Model-Split). State:
  `group_models`/`group_wounds`; Tod nach `priority`. Per-Gruppe-Stat-Overrides (`attacks`/`strength`/`ws`/`bs`).
- **Reset-Button-Pattern:** fähigkeits-gesetzter Zustand braucht Undo solange der Zug läuft —
  `turn_flags["<ability>_locked"]`, Phase-UI zeigt Undo, nach Zugwechsel fällt `_locked` weg.
  Beispiel: Veil of Darkness (`movement_locked`).

---

## Regelerkenntnisse (nicht-offensichtlich)

- **WAAAGH! Stage 1:** ORKS CORE/CHARACTER dürfen nach Advance chargen; +1 S/+1 A für ALLE ORKS.
- **Cover:** Dense (−1 Hit) + Light (+1 Save) nur Shooting; Heavy (+1 Save) nur Melee, außer Verteidiger hat gechargt.
- **Resurrection Orb / RP:** keine KERN-Einschränkung; `<DYNASTY>`-Einheiten; RP-Gate über `unit.rules`.
- **FNP:** normale UND tödliche Wunden; pro Wunde nur eine Ignore-Regel.
- **Fight Phase:** startet mit inaktivem Spieler; CHARGED zuerst, dann abwechselnd.
- **Heroic Intervention:** Schritt 2 Charge Phase, nur CHARACTER, ≤3", näher zum Feind enden.
- **extra_attacks — zwei Klassen:** „+N additional" → `unit.attacks + N`; „+N AND no more than N"
  → fester Cap N (`max_attacks`). Boss-Nob-Waffen: nur der Boss Nob trägt Spezialwaffen.
- **Skorpekh Destroyers:** feste Komposition 1 Reap-Blade je 3 Modelle (kein Wahl-Wargear).
