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

## Aktueller Stand (nach S51, 2026-06-16)

**S51 — Organisations-Schuld + Finding #1 + Gate-Netz.** Freigegeben Phase 0+1, dann (a)+(b).

- **Finding #1 (Badge) ✅** — Faktion-Badge zeigt Faktionsnamen aus YAML (nicht Roster-Titel);
  Subfaction-Badge **generisch + immer sichtbar** (Wert / „No <Label>" / „No Subfaction"),
  helles Blau `#a5b4fc`. Roster-Pflichtfeld je Faktion (`dynasty`/`clan`/`shield_host`),
  in `faction_abilities.yaml` deklariert (`subfaction_field`/`subfaction_label`). Alle Roster gesetzt.
- **(a) `dynasty`-Vokabular aus `src/` entfernt** → generisches `subfaction` (Wunsch aus /btw).
- **(b) Datengetriebenes Generic-src-Vokabular-Gate** (`tests/architecture/test_generic_src_vocab.py`
  + `_vocab.py`): erntet Fraktions-Eigennamen aus den YAMLs, Ledger = aktuelle Schuld, Ratchet.
- **Doku-Gate** (`tests/docs/`) + **Akzeptanz-Gate** (`tests/acceptance/`, `docs/spec/acceptance/`):
  AC-IDs ↔ Tests im Gleichtakt; `next_session.md` Zeilenbudget; INV ↔ Wächter-Korrelation.
  Invarianten-Doku: INV-4b + INV-5 ergänzt (`architecture_invariants.md`).

### ▶ Nächster Schritt — SCHULDEN BESEITIGEN (Priorität, Nutzer-Auftrag S51)

Die Gates machen die Schuld jetzt **messbar** — also abbauen, nicht wachsen lassen. Reihenfolge:

1. **INV-4b Vokabular-Ledger schrumpfen** (`tests/architecture/test_generic_src_vocab.py` LEDGER):
   - Größter Brocken: **`protocol`/`protocols`** als generischer Round-Choice-Begriff (Necron-Wort)
     faktion-neutral umbenennen (z. B. `round_choice`/`directive`) quer durch `src/` → Ledger-Einträge raus.
   - Danach benannte Items (`orb`, `overlord`, `phaeron`, `irongob`, `gloom`, `prism`, `dakka`,
     `klaw`, `tesla`, `reanimation`, `arkana`, `dynasty`) aus Phasen-/Render-Modulen in YAML/Daten ziehen.
   - Jeder entfernte Eintrag = Ratchet (Ledger nur kleiner). Test bricht rot, wenn ein Eintrag
     veraltet → genau dann Ledger-Zeile löschen.
2. **INV-4 Allowlist schrumpfen** (`test_generic_src.py`): Default-Roster/`faction_dir`-Default/Spielerlabels
   aus den gewählten Armeen ableiten statt hartkodieren.
3. **Test-Mock-Fragilität sauber lösen** (backlog §4, S51 entdeckt): geteilte `streamlit`-Fixture
   (conftest) + Tests auf `module.st` statt lokalem `_st_mock` umstellen. Tieferliegend: globalen
   `session_state`-Zugriff in den Logik-Modulen reduzieren.

### ▶ Danach — offene Findings (Phasen 2–4, `backlog.md` §0, je eigener Plan + Freigabe)

- **Phase 2 — #2b Direktiv-Lock:** Protokoll-Direktive nur in Kommandophase wählbar.
- **Phase 3 — #2 Buff-Audit:** 9 nicht-verdrahtete Protokoll-Effekte einzeln anzeigen (Tabelle backlog §0).
- **Phase 4 — #3/#4 Würfel:** Pfeil/Badge-Text/-Breite — Soll-Bild **erst als AC mit Nutzer** abstimmen.
- **Coverage-Fahrplan:** Floor 88 %. Pure Logik aus `omit`-Modulen in getestete Helfer ziehen, Floor nachziehen.

---

## Gate-Netz (Messbefehle)

- Tests + Coverage: `pytest --tb=short` (Floor 88 %, `pyproject.toml`).
- **Schulden-Scoreboard**: erscheint nach jedem `pytest`-Lauf (Hook in `tests/conftest.py`) —
  Fraktions-Vokabular-Tokens, Namen-Allowlist, AC-IDs, next_session-Zeilen. Baseline 2026-06-16
  in `architecture_invariants.md`. Ziel: Vokabular-/Allowlist-Zahlen sinken pro Session.
- Architektur (INV-1..4b): `pytest tests/architecture/ --no-cov -q` · Ledger: `architecture_invariants.md`.
- Doku + Akzeptanz (INV-5): `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- Neues Akzeptanzkriterium: AC in `docs/spec/acceptance/index.md` + `@acceptance("AC-…")`-Test (README dort).

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
