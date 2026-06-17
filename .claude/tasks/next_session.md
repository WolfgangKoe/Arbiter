# Startprompt — Nächste Session
<!-- Kanonisch: .claude/tasks/next_session.md — nie ins Root-Verzeichnis anlegen. -->
<!-- „Was next" + Stand. Erledigte Session-Historie → ziel6.md; offener Backlog → backlog.md. -->

## ⚠️ Session-Regeln (immer beachten)

**Session-Start:** `CLAUDE.md` (Workflow, Freigabe-Pflicht, Unklarheiten zuerst fragen)
+ `docs/goals/ziel6.md` (Aufgaben/Historie) + `docs/goals/backlog.md` (offener Backlog).

**Session-Ende:** Checkboxen in `ziel6.md` abhaken + Zeile in die Session-Historie;
**diese Datei** aktualisieren (ZUERST lesen, dann ergänzen — nie blind überschreiben).
Doku-Gate hält diese Datei unter 160 Zeilen — Erledigtes nach `backlog.md`/`ziel6.md` auslagern.

---

## Was ist Arbiter?

Digitaler Spielbegleiter für Warhammer 40.000 9. Edition, Streamlit (Python).
Start: `streamlit run src/app.py` (Port 8501). Branch `dev` (Entwicklung), `main` (nur per PR).

---

## Aktueller Stand (nach S53, 2026-06-17)

**S53 — Regel-Abdeckung (Akzeptanz-Katalog) + Arbeitsweise verankert.** Neuer Nenner
`docs/spec/acceptance/rules.md`: Combat-Katalog als verbindliche Vorlage (34 Regeln, Klasse
A/B/C, stabile `datei:funktion`-Refs + Testnamen). Arbeitsweise in `CLAUDE.md` festgehalten:
Token-Korridor <150k / 90%-Wind-down, Subagent-für-Fleißarbeit (Sonnet) + Opus-Review,
getrennte Messung. Noch kein Gate verdrahtet (pytest unverändert).

**S52 — INV-4b: `protocol`/`protocols`-Vokabular aus `src/` entfernt.** Reine, verifizierte
Umbenennung auf den etablierten Begriff `round_choice` (kein Verhaltenswechsel): Klasse
`CommandProtocol`→`RoundChoiceAbility` (Datei `round_choice_ability.py`), Session-Keys
`protocol_*`→`round_choice_*`, Helfer/Funktionen, Roster-Feld `protocol_order`→`round_choice_order`,
UI-Strings datengetrieben via `load_round_choice_label()`. Ledger-Einträge entfernt (Ratchet);
Reste LEGIT (`typing.Protocol` in `phase_handler`) bzw. `reanimation`-Schuld (`reanimationProtocols`).
852 Tests grün, Coverage 88.45 %. Manuell verifiziert (Command-UI, Setup-Swap, Battle-Log-Tab).

**S51 — Organisations-Schuld + Finding #1 + Gate-Netz.** Badge generisch; `dynasty`-Vokabular raus;
datengetriebenes Vokabular-Gate + Doku-/Akzeptanz-Gate. Details: `ziel6.md`/`backlog.md`.

### ▶ Nächster Schritt — Regel-Abdeckung (Akzeptanz-Katalog) ausrollen

Phase 0 Schritt 1 fertig: Combat-Katalog (`docs/spec/acceptance/rules.md`) als **verbindliche
Vorlage** (34 Regeln; Klasse A/B/C; stabile `datei:funktion`-Refs + Testnamen). Fixe
Entscheidungen: Granularität = **Mechanik-Schritt**; Klasse **C** (Hybrid) eingeführt; Referenzen
stabil+verifizierbar. Combat-Ledger = **2** (R-09 mehrfach-Invuln, R-17 Rapid Fire: implementiert
ohne Test). Klasse B = 0 % (App zeigt keine Tisch-Hinweise).

Optionen (je eigene Freigabe): (1) **Rollout** weiterer Bereiche per Sonnet-Subagent mit der
Vorlage (~30–80k/Bereich); (2) **Phase 1 Gate read-only** — `rules.md` ins Schulden-Scoreboard
(Abdeckung % je Klasse, Ledger-Größe) + Konsistenz-Check (jeder `getestet: ja`-Testname existiert),
hart-rot erst auf Ansage; (3) **Phase 3** `tools/token_report.py` + `docs/metrics/overview.md`.
**Empfehlung: erst (2) read-only, dann (1).** Bug #2b u. a. offene Findings bleiben in `backlog.md`.

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
- **Token-Korridor:** <150k, bei ~135k Session beenden. Fleißarbeit an Sonnet-Subagent (CLAUDE.md).

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
