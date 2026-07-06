STATUS: ANSWERED — Freigabe alle 4 Pakete (2026-07-06); 1c gemäß decision_revive_key_s128.md Option B; Zero-Error-Policy mypy (Baseline kontinuierlich Richtung 0, gameMechanic→gameObjects→uiLayout zuletzt).
<!-- Temporär. Löschen nach Freigabe + Übernahme der Pakete in Executor-Briefs. -->

# Planning-Entwurf S128 Teil 2 — Parallelisierter Ledger-Abbau (2026-07-06)

## ⚠️ Blocker VOR dem Parallelstart — mypy-Gate ist aktuell ROT

`python tools/mypy_gate.py` → **exit 1: 135 Fehler > Baseline 134.** Gegenprobe per
`git stash`: HEAD hat 134, der uncommittete Teil-1-Stand 135. Verursacher (einziger Diff):
`src/gameMechanic/game_state.py:431` — `st.session_state.cp_grants: set[tuple[int, str]] = set()`
(Inline-Annotation an non-self-Attribut, `[misc]`). **Fix vor Commit:** Annotation entfernen
(`st.session_state.cp_grants = set()`, Kommentar bleibt) → 134 == Baseline, Gate grün.

**Empfehlung Commit vorab: JA** (wie vom Koordinator vorgeschlagen) — erst Mini-Fix oben,
Gate + Vollsuite grün, dann Teil-1-Stand committen. Sauberer Wiederaufsetzpunkt; Paket 2
editiert dieselbe Datei (`game_state.py`) und braucht die saubere Basis. ~2k Token, Koordinator.

## Pakete (parallel, dateidisjunkt)

### Paket 1 — INV-4b-Abbau komplett (5 DEBT-Tokens → LEDGER nur noch LEGIT)
Bewusst EIN Paket statt drei: alle Cluster müssen `tests/architecture/test_generic_src_vocab.py`
(LEDGER-Dict) editieren — als ein Paket bleibt diese Datei konfliktfrei. Drei Schritte:
- **a) `movementPhase.py` `dynasty`** (Z. 148, 189): Teleport-Relic-Texte („DYNASTY CORE …")
  in `data/wh40k_9e/necrons/relics.yaml` verlagern (neue Felder `prompt_text`/`selector_label`);
  `load_relic_catalog` liefert Raw-Dicts → **kein `loader.py`-Edit nötig** (verifiziert Z. 672-679).
- **b) `psychicPhase.py` `gloom`/`prism`** (Z. 399): Caption „Deny 1 / Gloom Prism: once per
  phase" fraktions-neutral („once per phase per source") oder Quellenname datengetrieben.
- **c) `_common.py` `protocols`/`reanimation`** (Z. 584): YAML-Rule-Key `reanimationProtocols`
  generisch umbenennen — Vorkommen: `_common.py` (2), `necrons/units.yaml`,
  `necrons/faction_abilities.yaml`, 3 Testdateien. **ENTSCHEIDUNG NÖTIG (Konsens lt. Backlog
  §4, „Schema-Urteil"): neuer Key-Name — Vorschlag `revive_roll`.** Bitte mit der Freigabe
  beantworten, sonst Schritt c zurückstellen (a+b bauen 3 von 5 Tokens ab).

Schreibmenge: `src/gameMechanic/movementPhase.py`, `src/gameMechanic/psychicPhase.py`,
`src/uiLayout/_common.py`, `data/wh40k_9e/necrons/{relics,units,faction_abilities}.yaml`,
`tests/architecture/test_generic_src_vocab.py`, `tests/gameObjects/test_ability.py`,
`tests/gameMechanic/{test_ability_engine,test_damage_block_reanimation}.py` + Movement-/Psychic-Tests.
Token ~25-35k · **Tier Sonnet** (Schema-Verlagerung + Rename über Daten/Tests, kein Lookup).
Risiken: a+b sind Render-Text → **manuelle UI-Verifikation** (Veil-of-Darkness-Dialog,
Deny-Caption) am Ende nennen; c bricht bei Tippfehler still das RP-Gate → Regressionstest
`reanimationProtocols`-frei nachziehen (grep-Beleg 0 Treffer in src+data).

### Paket 2 — mypy: `gameMechanic/game_state.py` (35 Fehler, größter Einzelposten)
Fehlerbild: 18× `[misc]` (Inline-Annotationen an `st.session_state.*` → auf annotierte
Zwischenvariable/`cast` umstellen), 9× `[type-arg]`, 6× `[no-any-return]`, Rest Kleinkram.
Schreibmenge: `src/gameMechanic/game_state.py`, ggf. `tests/gameMechanic/test_game_state.py`.
**Kein Edit an `tools/mypy_gate.py`** — Executor meldet nur die neue Fehlerzahl (s. u.).
Token ~20-30k · **Tier Sonnet** (Begründung über Haiku-Default: `SessionStateProxy`-Typing ist
kein Format-Fix; Datei wurde in Teil 1 frisch geändert, Fehlerrisiko teuer).
Risiko: Verhaltensneutralität — nur Annotationen/Casts, keine Logik; Vollsuite als Beleg.

### Paket 3 — mypy: `gameObjects/` komplett (18 Fehler)
`rosz_importer.py` 9 · `loader.py` 5 · `round_choice_ability.py` 2 · `weapon.py` 1 · `ability.py` 1.
Schreibmenge: diese 5 Dateien + ggf. `tests/gameObjects/*`. Kein `tools/mypy_gate.py`-Edit.
Token ~15-25k · **Tier Sonnet** (loader-Typen hängen an Dataclass-Verträgen; Haiku nur bei
reinen `type-arg`-Fixes vertretbar, hier gemischt — Begründung dokumentiert).
Risiko: `loader.py` trägt frische Teil-1-Änderungen → nach Vorab-Commit starten.

### Paket 4 (optional) — Plan 018 Task 18.3: Gretchin Cowardly / Combat-Attrition-Hinweis
Einziger queue-nächster Schritt, der dateidisjunkt bleibt (18.2 berührt `game_state.py` →
kollidiert mit Paket 2; Plan 015 hat Mockup-Gate → nicht für Hintergrund-Parallellauf).
Vorgabe zur Disjunktheit: `_attrition_threshold`-Helper in `moralePhase.py` ansiedeln,
**nicht** in `ability_engine.py` (Plan 018 lässt beides zu).
Schreibmenge: `src/gameMechanic/moralePhase.py`, `data/wh40k_9e/orks/unit_abilities.yaml`,
`docs/spec/faction_abilities.md`, `tests/gameMechanic/test_morale*.py`.
Token ~15-20k · **Tier Sonnet** (Regel-Recherche + Schema + Render-Hinweis).
Risiken: STOP-Bedingung aus Plan übernehmen (Attrition-Wortlaut abweichend → Zitat vorlegen);
Render-Anteil → manuelle UI-Verifikation am Ende.

## Disjunktheits-Nachweis
Paarweiser Schnitt der Schreibmengen = leer: P1 (movementPhase, psychicPhase, _common, Necron-
YAML, vocab-LEDGER, 3 benannte Testdateien) ∩ P2 (game_state + test_game_state) = ∅ ·
P1 ∩ P3 (gameObjects/*, tests/gameObjects außer test_ability.py → **test_ability.py exklusiv
P1 zuweisen**, P3 nutzt die übrigen) = ∅ · P2 ∩ P3 = ∅ · P4 (moralePhase, orks-YAML,
faction_abilities.md, test_morale*) schneidet keines. Doku-Dateien (`architecture_invariants.md`,
`backlog.md`, `plans/README.md`, `next_session.md`) und `tools/mypy_gate.py`: **exklusiv
Koordinator-Abschlussschritt** — Executor-Briefe verbieten diese Pfade explizit (überschreibt
für diesen Lauf die Plan-Status-Pflicht aus agent_scopes.md).

## Koordinator-Abschlussschritt (nach allen Paketen, seriell)
1. Finale Vollsuite + `python tools/mypy_gate.py`; BASELINE in `tools/mypy_gate.py` **einmal**
   auf den gemessenen Endwert senken (erwartet: 134 − 35 − 18 = **81**, im selben Commit —
   erfüllt die Ratchet-Regel, die pro Paket nicht erfüllbar wäre).
2. Doku-Konsolidierung: `architecture_invariants.md` (Schulden-Tabelle: INV-4b 11→6, nur noch
   LEGIT; mypy-Baseline), `backlog.md` (§4-Einträge), `plans/README.md` (018-Teilstatus),
   `next_session.md`. 3. Commits je Paket oder gebündelt nach Review. ~5-8k Token.

## Parallelitäts-Risiken (gemeinsamer Working Tree)
- **`.coverage`-Kollision:** parallele `pytest`-Vollsuiten schreiben dieselbe Coverage-Datei →
  je Executor `COVERAGE_FILE=<scratch>/.coverage.<paket>` setzen ODER Vollsuiten zeitlich
  staffeln (Koordinator taktet: Paket meldet „bereit für Suite", läuft exklusiv).
- **Cross-Paket-Rot:** sieht ein Executor in seiner Vollsuite Failures in Dateien außerhalb
  seiner Schreibmenge → NICHT fixen, melden (Rote-Tests-Regel); Koordinator-Endlauf entscheidet.
- Alternative bei Unbehagen: `isolation: worktree` je Executor — sauberer, aber Merge-Aufwand
  beim Koordinator; bei strikter Datei-Disjunktheit ist der gemeinsame Tree vertretbar.

## Summe & Reihenfolge
Vorab-Fix+Commit (~2k, Koordinator) → P1 ‖ P2 ‖ P3 ‖ P4 parallel (~75-110k Subagent-Token,
isolierte Kontexte — Koordinator-Fenster wächst nur um Briefe+Berichte, ~10-15k) →
Abschlussschritt (~5-8k). Ledger-Erwartung danach: INV-4 3 (nur LEGIT) · INV-4b 6 (nur LEGIT)
· mypy 81 · Plan-018 zu 2/4 erledigt.

**Offene Entscheidungen:** (1) Freigabe Vorab-Fix (Annotation Z. 431 entfernen) + Commit;
(2) Paketumfang: alle 4 oder ohne P4; (3) Konsens neuer Rule-Key-Name für
`reanimationProtocols` (Vorschlag `revive_roll`) — ohne Antwort läuft P1 nur mit a+b.
