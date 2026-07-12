# Ziel 7 — Gefechtsoptionen + subfaction-Mechanik 🟨

**Voraussetzung:** Ziel 6 abgeschlossen (inkl. 6e Execute-Logik-Grundlage).

Bündelt zwei eng verwandte Bereiche aus Ziel 6, die blockiert oder bewusst ausgelagert wurden:
(1) die vollständige **subfaction Execute-Logik** (`collect_modifiers_for_phase` + Ability.modifier + Phase-Handler-Verdrahtung) und
(2) die **generischen Fraktionsfähigkeiten** für weitere Armeen (alle aktuell blocked-by-YAML).

**Crusade-Erweiterung ist jetzt Ziel 8.**

---

## Status

🟨 Aktiv. Ziel 6 ist abgeschlossen (`docs/goals/archive/ziel6.md`). §0 Stufe A (Gefechtsoptionen
Spieler-Split) ist erledigt (S120/S121); Stufe B (Necrons), Stufe C (Orks), UX-Pass und der
bestehende §6e/6f/6h-Backlog sind offen.

---

## 0. Gefechtsoptionen Spieler-Split (S120+, fachliche Priorität 1)

**Kontext:** Aus dem S119-Live-Test hervorgegangen (Player-A/B-Split für Gefechtsoptionen;
fachliche Reihenfolge allgemein → Necrons → Orks, danach UX-Pass vor Ziel8). Ursprünglich
detailliert in `docs/handoff/plan-ziel7-restruktur.md` — Handoff nach Abschluss der Stufe A
gelöscht (S121, Lifecycle-Regel), Inhalt (inkl. Stufe B/C und UX-Kandidatenliste) hierher
überführt, damit nichts verloren geht.

### Stufe A (S120/S121) — Fundament + allgemeine Gefechtsoptionen — ERLEDIGT

- [x] Task 0 — YAML-Drift: Counter-Offensive + Insane Bravery von `player: inactive`/`active`
  auf `player: both` korrigiert (Fight-/Morale-Phase alternieren laut Regeltext zwischen beiden
  Spielern, `core_rules.txt:1941`/`2094`). Commit `f9279fe`.
- [x] Task 1 — reine Funktion `stratagem_usable_by_player()` + Zwei-Spalten-Rendering
  (`first_player` links / `second_player` rechts, fix, nie an `active` gebunden). Löst
  Stratagem-Doppelanzeige und Attributions-Bug strukturell (keine Konkatenation/Ableitung mehr).
  Commit `8c124c3`.
- [x] Task 2 — `used_stratagem_ids` von globalem `set[str]` auf `dict[str, set[str]]` pro
  Spieler-Slot migriert, analog `cp`/`used_stratagem_battle_ids`. Commit `396fdec`.
- [x] Manuelle UI-Verifikation (S121): Checklisten-Punkte 1, 2, 5–7 bestätigt. Punkte 3+4
  (Fire Overwatch/Counter-Offensive, `timing: phase_reactive`) NICHT prüfbar — brauchen die
  reaktive Stratagem-UI aus Plan 015 (offen, s. Stufe A unten in `docs/audit/plans/README.md`).
- [x] **S130: alle 7 `_shared`-Stratagems integriert** (`b5c774b`, `2e3aa98`): 4 reaktive
  anwählbar (Plan 015 teilweise), Insane Bravery auto-pass (R-MORALE-09), Desperate Breakout
  (R-MOVE-14), Command Re-Roll inline für Damage/Psychic/Deny (R-CMD-12, 3/9 Wurf-Arten —
  Rest = Stakeholder-Auflage im Backlog). Manuelle UI-Prüfung inkl. Punkte 3+4 jetzt OFFEN
  und prüfbar (7-Punkte-Checkliste in `.claude/tasks/next_session.md`).
- Nebenbei gefixt (nicht Teil der ursprünglichen Stufe-A-Tasks, im selben Zug behoben): CCW-
  Fallback-Crash `ap="0"` → `ap=0` in der Save-Resolution (Gretchin). Commit `464bb40`.

**Design-Entscheidung (getroffen, S119/S121):** Option 1 — keine Farbunterscheidung zwischen
Core- (`_shared`) und Fraktions-Stratagems, nur Sektions-Header innerhalb der Spieler-Spalte
(`docs/spec/design_colors.md` §4c bleibt gültig, kein neuer Farbslot). Das „(inactive)"-Label-
Suffix wurde nach dem Split entfernt (redundant zur Spaltenzuordnung).

**Neue Findings aus der S121-Verifikation:** siehe `docs/goals/backlog.md` §5 „Neue Findings
(S121-UI-Verifikation, noch offen)" — F1 (Disruption Fields Effekt-Semantik falsch), F2
(Weirdboy-Stab-Verifikation gegen Wahapedia), F3 (natürliche 1 in der Würfel-UI bei
modifizierten Zielwerten), F4 (Plan 015 als Voraussetzung für Punkte 3+4 der Checkliste).

### Stufe B — Necron-Gefechtsoptionen (offen, Detailplanung in eigener Session)

`data/wh40k_9e/necrons/stratagems.yaml` existiert bereits und wird von `load_stratagems`
generisch mitgeladen — **kein Necron-spezifischer Code nötig**, nur Daten-/Regel-Review:

- [x] Vollständigkeitsabgleich `data/wh40k_9e/necrons/stratagems.yaml` gegen
  `docs/work/wahapedia_necrons/` (fehlende Stratagems? falsche `player`/`phase`/`stage`-Felder —
  derselbe Klassifikationsfehler wie beim Core-Drift ist pro Fraktion denkbar). S123-Vollabgleich
  aller 59 (jetzt 60) Stratagems durchgeführt, 27 Befunde gefunden; die per Schema sauber
  abbildbaren HOCH-Befunde sind gefixt, Restarbeit → Plan 032.
- [x] `once_per_battle`/`conditions`-Felder gegen Regeltext prüfen (Necron-Stratagems mit
  Keyword-Bedingungen, z. B. dynastie-spezifisch). Abgleich erledigt (S123); mehrere `conditions`-
  Felder sind OR-Bedingungen, die das aktuelle AND-only-Schema nicht abbilden kann (z. B.
  `extermination_protocols`, `efficient_disintegration`, `whirling_onslaught`,
  `resurrection_protocols`) — offene Modellierung → Plan 032.
- [ ] Manuelle UI-Verifikation mit echtem Necron-Roster nach dem Delta-Fix.

Effort-Einschätzung: S–M je nach Delta-Größe (unbekannt bis Review erfolgt ist).

### Stufe C — Ork-Gefechtsoptionen (offen, Detailplanung in eigener Session)

Analog Stufe B: `data/wh40k_9e/orks/stratagems.yaml` existiert, Loader generisch. Gleicher
Delta-Abgleich gegen `docs/work/wahapedia_orks/` nötig. **Reihenfolge nach Stakeholder-Vorgabe:
erst nach Abschluss Stufe B** — die allgemeine Logik (Stufe A) gilt bereits für beide
Fraktionen, Stufe B als „zweite Anwendung des Musters" schärft den Delta-Prozess für Stufe C.

**S141-Vorarbeit:** neues Roster `data/rosters/orks_transport.yaml` (Evil Sunz, Gunwagon
TRANSPORT, Warboss, 10 Boyz, 10 Gretchin, 330 Pkt., Commit `cbaeeb2`) entblockt die manuelle
Verifikation von Emergency Disembarkation an einem echten Ork-Roster mit TRANSPORT-Unit —
zuvor scheiterte das mangels geeignetem Roster (S139-Befund). Manuelle UI-Verifikation dazu
noch offen (s. `docs/goals/backlog.md` §3).

**Klan-Affinität existiert regelseitig nicht (S143-Stakeholder-Klärung, Commit `3602ddb`) —
als Verifikationspunkt gestrichen.** Stattdessen offener Scope: **Klan-Fähigkeiten (Ork
Kulturs) + Dynastie-Fähigkeiten (Necron Dynastic Codes)** (Datenlage: kein `klan`-Schlüssel
in Rosters, kein Fähigkeits-Block in `data/wh40k_9e/orks/`). Konzept dafür entsteht in S144;
Umsetzung als eigener Plan ab S145.

### UX-/UI-Pass vor Ziel8 — Kandidatenliste (Entscheidungsvorlage, keine Priorisierung)

Beobachtungen aus dem Render-Code (`gameProtocoll.py`), gesammelt während der Stufe-A-Planung —
reine Sammlung für den Stakeholder, keine Bewertung/Umsetzung:

- **Battle Log bleibt global, Stratagems sind jetzt pro Spieler gesplittet** — die beiden Tabs
  im selben `gameProtocoll`-Bereich haben dadurch unterschiedliche Layout-Philosophien (ein
  globaler Log vs. zwei Spielerspalten). Bewusste Inkonsistenz oder soll der Battle Log
  langfristig demselben Muster folgen?
- **Expander-Dichte bei zwei schmaleren Spalten** — mit `st.columns(2)` ist jede Spalte halb so
  breit; lange Stratagem-Namen/CP-Kosten-Zeilen könnten enger umbrechen (war Teil der Stufe-A-
  Verifikation, kein separates UX-Thema).
- **Kein Hinweis, WANN im Regeltext ein Stratagem greift** (`event`/`timing`-Felder existieren im
  Datenmodell — z. B. `on_declaration`, `after_roll` — werden aber nirgends angezeigt). Könnte für
  Spieler hilfreich sein zu sehen „reagiert auf X", ist aber ein neues Feature, kein Bugfix.

---

## Backlog — eingehende Punkte (aus Ziel 6 ausgelagert)

### 6e — subfaction Execute-Logik

- [ ] `gameMechanic/abilityEngine.py`: `collect_modifiers_for_phase(phase, attacker_unit, weapon, target_unit)` — sammelt alle aktiven Modifier aus allen Quellen
- [ ] `gameObjects/ability.py`: Ability-Schema um `modifier`-Felder erweitern (analog zu Stratagem in 6c)
- [ ] `data/wh40k_9e/*/unit_abilities.yaml` + `faction_abilities.yaml`: Modifier-Felder für relevante Fähigkeiten nachtragen (Pilot: Necrons + Orks)
- [ ] Phase-Handler (Shooting, Fight, Charge): rufen `collect_modifiers_for_phase()` auf und übergeben Ergebnis an Attackensequenz-Renderer

### 6f — Ability-Badges + Keyword-Highlighting

Abhängig von `collect_modifiers_for_phase` (6e Execute-Logik):

- [ ] `uiLayout/unitCard.py`: `active_modifiers` aus Session-State lesen, Badges für betroffene Einheit rendern
- [ ] `uiLayout/unitCard.py`: Keyword-Highlighting wenn `active_modifiers` ein Keyword-Condition-Modifier betrifft
- [ ] `gameMechanic/gameState.py`: `active_modifiers` Datenstruktur definieren: `{unit_key, source, effect, expires_at_phase, expires_at_round}`

### 6h — Kat1–3 neue Fraktionen (alle blocked-by-YAML)

**Kategorie 1 — Runden-Wahl:**

- [ ] AdMech: `data/wh40k_9e/adeptus_mechanicus/faction_abilities.yaml` + `CommandProtocol.secondary` optional + `armyCard._render_protocol_ui()` anpassen
- [ ] Tyranids: `data/wh40k_9e/tyranids/faction_abilities.yaml` + Pool-Check ob Synapse-Unit noch lebt
- [ ] `tests/test_faction_abilities_admech.py`, `tests/test_faction_abilities_tyranids.py`

**Kategorie 2 — Einmalig-Deklariert:**

- [ ] T'au: `data/wh40k_9e/tau_empire/faction_abilities.yaml` (`montka` + `kauyon` mit `active_rounds`)
- [ ] `armyCard._render_waaagh_ui()`: `active_rounds`-Feld aus YAML auslesen
- [ ] `tests/test_faction_abilities_tau.py`

**Kategorie 3 — Auto-Progression (kein Player-Input):**

- [ ] `abilityEngine.py`: `get_auto_progression_modifier(faction_dir, phase, round)`
- [ ] `armyCard.py`: `_render_auto_progression_badge(faction)` — Info-Badge ohne Button
- [ ] YAML-Schema `ability_type: auto_progression` + YAML für Space Marines, Death Guard, Chaos SM
- [ ] `tests/test_auto_progression.py`

**Fix B — WAAAGH! generisch:**

- [x] `armyCard.py:_render_waaagh_ui`: Ability-Suche, WARBOSS-Keyword und Effekttexte vollständig generisch (via YAML `active_text`-Feld) (S113, e031616 — Drift-Nachzug S119)
- [x] `gameObjects/ability.py`: optionales `active_text: str | None` (S113, e031616 — Drift-Nachzug S119)
- [x] `data/wh40k_9e/orks/faction_abilities.yaml`: `active_text` ergänzen (S113, e031616 — Drift-Nachzug S119)
