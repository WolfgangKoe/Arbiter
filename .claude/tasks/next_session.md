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

## Aktueller Stand (nach S60, 2026-06-19)

**S60 — Regel-Katalog: Bereiche Charge Phase + Morale Phase ausgerollt.** 13 `R-CHARGE-01..13`
+ 13 `R-MORALE-01..13` (Sonnet-Subagent erfasst die Fleißarbeit aus `core_rules.txt` Charge
Z. 1768–1935 / Morale Z. 2087–2161 + Appendix, Opus reviewt gegen echten Code + Regeln/finalisiert)
in `rules.md`. Nenner jetzt **87** (34 Combat + 14 Command + 13 Movement + 13 Charge + 13 Morale).
Scoreboard: A 28/58 (48%) · B 0/19 · C **8/10 (80%)**; Konsistenz grün (0 fehlende Testnamen).
**Ledger 7→10**: 3 neue implementiert-aber-ungetestet-Einträge surfacen bestehende Render-Schuld
(`R-CHARGE-09`/`R-CHARGE-10` = HI-Eligibility/Once-per-Phase in `chargephase._render_hi_phase`;
`R-MORALE-02` = Verlust-Filter in `moralePhase._render_faction_morale`). **Befund** (→ backlog):
`R-COMBAT-32` („charged fight first") ist als `offen` markiert, aber real implementiert+getestet
(`fightPhase.can_fight`, `test_charged_can_fight`/`test_charged_takes_priority_over_advanced`) →
Doku-Drift, im Combat-Bereich nachzuziehen. Fight-First aus Charge-Bereich auf R-COMBAT-32
referenziert statt dupliziert. Doku-only, kein `src/`. 875 Tests grün, Coverage 88.45 %.

**S59 — Regel-Katalog: Bereich Movement Phase ausgerollt.** 13 Einträge `R-MOVE-01..13`
(Sonnet-Subagent erfasst die Fleißarbeit aus `core_rules.txt` Z. 702–970, Opus reviewt gegen Code +
Regeln/finalisiert) in `rules.md`. Nenner jetzt **61** (34 Combat + 14 Command + 13 Movement).
Alle 6 implementierten Movement-Regeln haben **echte Tests** → **kein neuer Ledger-Eintrag**
(bleibt 7). Scoreboard: A 23/43 (53%) · B 0/12 · C **6/6 (100%)**; Konsistenz grün.
FLY/Transport als Klasse B (raum-/tischgemessen, analog R-COMBAT-27..29). Doku-only, kein `src/`.

**S58 — Token-Report v3: Effizienz statt Menge.** `tools/token_report.py` zur Effizienz-Anzeige
umgebaut (ADR-0002, Akzeptanz a–f aus `backlog.md`): Fokus-Block letzte Session + 6-Session-Verlauf
(theme-sichere Unicode-Balken, Modell-Mix, Trends) + auto-Hinweise + Subagenten-Tabelle; All-Time-
Torte entfernt. Bewusster Test-Vertragswechsel (23 Tool-Tests neu). Details → `backlog.md` §2.

**S57 — Operating-Model Phase B: Token-Report (v1+v2).** `tools/token_report.py` (neu) führt
Haupt-Session- und Subagent-Verbrauch **getrennt** zusammen (je Modell-Tier + je Session) →
`docs/metrics/overview.md`, aus `LEITSTAND.md` verlinkt; getestet `tests/tools/`. **Retro →
ADR-0002 + [[feedback_session_close_routine]]:** stakeholder-Artefakte müssen Leserfragen
beantworten; Token-Report beim Test-Start teilen. Details → `backlog.md` §2.

**S56 — Operating Model etabliert** (Governance-Schicht: `operating_model.md` Rollen/Model-Tier/
7 Events/4 Entscheidungsmodi; `LEITSTAND.md` Einstiegstür; ADR-Log + ADR-0001; `docs/inbox/`
Refinement). Details → `ziel6.md` Historie.

**S55 — Regel-Katalog: Bereich Command Phase ausgerollt.** 14 Einträge `R-CMD-01..14`
(Sonnet-Subagent erfasst die Fleißarbeit, Opus reviewt/finalisiert) in `rules.md`. Nenner jetzt
**48** (34 Combat + 14 Command). Scoreboard: A 22/41 (54%) · B 0/6 · C 1/1; Ledger **7** (2 Combat
+ 5 neu: R-CMD-03/04/10/11/12); Konsistenz grün. Befund R-CMD-03 (CP-Grant ohne Battle-forged-
Gating) → `backlog.md`. Doku-Drift: 6e-Task `cp_granted_this_phase` war erledigt, jetzt abgehakt.
852 Tests grün, Coverage 88.45 %.

**S54/S53 — Regel-Katalog + Gate verankert** (Nenner-Vorlage, Scoreboard-Verdrahtung, Parser
`tests/acceptance/_rules.py`); **S52 — INV-4b `protocol`→`round_choice`.** Details: `ziel6.md`.

### ▶ ZUERST (S61, vor allem anderen): Token-Report-Hook einrichten

**Pflicht, kein „frei wählbar".** In S60 ist die Session-Abschluss-Routine (Token-Report beim
Test-Start, [[feedback_session_close_routine]]) **nicht automatisch** gegriffen, weil sie nur als
Memory vorlag, nicht an einen Auslöser gekoppelt war. Lösung: **Hook in `settings.json`**
(via `update-config`-Skill, Freigabe nötig), der beim `pytest`-Start `python tools/token_report.py
--write` mitlaufen lässt bzw. am Sessionende an Peak-Kontext/Korridor-% erinnert — maschinell
durchsetzbar statt „Gedächtnis". Erst danach den gewählten Strang beginnen.

### ▶ Danach — frei wählbar (je eigene Freigabe)

Token-Report-Reihe (v1→v3) ist abgeschlossen. Offene Stränge, je eigene Freigabe:
1. **Gates/Reports leser-orientiert prüfen (→ ADR-0002):** Debt-Scoreboard + Rule-Catalog-Prozente
   daraufhin durchsehen, ob sie dem Stakeholder *seine* Fragen beantworten (backlog §2). Optional:
   `docs/metrics/session_notes.yaml` anlegen (Session-ID → Backlog-Link) für sprechende Aufgaben.
2. **Regel-Katalog weiter ausrollen** — **Movement ✅ S59**, **Charge/Morale ✅ S60**; nächster
   Bereich **Psychic Phase** (Sonnet-Subagent, eigene Session). `rules.md`: Combat 34 + Command 14
   + Movement 13 + Charge 13 + Morale 13, Nenner **87**.
3. **Ledger schrumpfen** (jetzt 10: 5 R-CMD + 2 Combat + R-CHARGE-09/10 + R-MORALE-02 als Tests)
   — Ratchet. Plus **Befund R-COMBAT-32** (als implementiert+getestet nachziehen, → backlog §0).
4. **Operating-Model Phase C:** Refinement automatisieren (`Fotos/` → `docs/inbox/`, backlog §2).

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
