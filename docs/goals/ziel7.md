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
- [x] Manuelle UI-Verifikation mit echtem Necron-Roster nach dem Delta-Fix. (S146,
  Stakeholder-Verifikation 2026-07-14, alle 7 Prüfschritte bestanden)

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

### K1 — Klan/Dynastie-Konzept kanonisiert (S150, Entscheid S145)

Konzept ursprünglich aus S144 (`docs/handoff/S144_klan_dynastie_konzept.md`, nach
Kanonisierung hierher S150 gelöscht — Lifecycle-Regel). Stakeholder-Entscheide S145
(Herleitung migriert nach `docs/goals/backlog.md` §4; Session-Historie S145/S147 in
`docs/metrics/session_archive.md`).

**Kern-Befund — Daten existieren, sind aber wirkungslos:** `data/wh40k_9e/orks/subfaction_abilities.yaml`
und `data/wh40k_9e/necrons/subfaction_abilities.yaml` bestehen bereits seit 2026-06-03 (alle 7
Klans/6 Dynastien, `rule_text`, `ability_type: triggered`, generisch geladen über
`load_subfaction_abilities()`, `src/gameObjects/loader.py:646`) und werden sogar bereits in
`abilityEngine.get_triggered_abilities()` (`src/gameMechanic/abilityEngine.py:582–609`)
eingelesen — aber **keiner der 13 Einträge wird aktuell im Spiel wirksam**, aus vier
unabhängigen Lücken (alle in `abilityEngine.py`):

1. **Kein Subfraktions-Filter** — `check_conditions()` prüft nicht, ob die Fähigkeit zur
   gewählten Klan-/Dynastie-Wahl des Rosters (`roster.clan`/`roster.dynasty`) gehört; sie
   würde für **jede** Einheit der Fraktion gelten.
2. **Kein passender Abfrage-Pfad** — `get_triggered_abilities()`s einziger Aufrufer
   (`commandPhase.py:31`) fragt fest `phase="command", timing="phase_start"` ab; die
   Subfraktions-Einträge haben `timing: persistent, phase: any/shooting/fight/movement` —
   matcht nie.
3. **4 Necron-Effekte zeigen auf einen nicht existierenden Handler** — `effect.type: complex`
   mit `handler: novokhSavageHunters`/`sautekh_advance`/`uncannyArtificersMortal`/
   `uncannyArtificersReroll`; das `.handler`-Dispatch-Muster existiert im gesamten `src/`-Baum
   nur für `fall_back_through_models` (`stratagemEngine.py`).
4. **Kein UI-Konsument** — keine Datei unter `src/uiLayout/` rendert `load_subfaction_abilities`
   oder `klan_keyword` irgendwo.

Diese Engine-/UI-Verdrahtung erklärt die S143-Stakeholder-Beobachtung „Klan-Fähigkeiten fehlen
als Feature" — die Daten sind formal vorhanden, wirken aber nicht.

**Wortlaut-Delta gegen Wahapedia 9E** (Quelle: WebFetch S144 2026-07-12, Necron-Nihilakh/Sautekh
zusätzlich per WebSearch gegengeprüft; Nihilakh + Mephrit S150 zusätzlich gegen die lokale
Primärquelle `docs/work/wahapedia_necrons/faction_overview.txt` verifiziert):

*Ork Klan Kulturs (7) — 1 Delta:*

| Klan | Ist (`subfaction_abilities.yaml`) | Delta |
|---|---|---|
| Bad Moons, Blood Axes, Deathskulls, Evil Sunz, Freebooterz | — | keins |
| Goffs | Strength-Klausel enger an „Pile-in/Consolidate" gebunden statt „Angriff generell" | gering, kein Fehler |
| **Snakebites** | „Wound 1–3 scheitert immer" — **ohne die S8+-Ausnahme** | **Fehler: Ausnahmeklausel fehlt** |

*Necron Dynastic Codes (6) — 5 von 6 weichen ab:*

| Dynastie | Wahapedia-Soll (Kurzfassung) | Ist (`subfaction_abilities.yaml`) | Delta |
|---|---|---|---|
| Szarekhan | Uncanny Artificers — bereits korrekt (früher korrigiert) | identisch | keins |
| Novokh | Awakened by Murder: +1 Charge-Wurf; bei Charge/Charged/HI **AP+1** im Nahkampf | „Savage Hunters", +1 Charge-Wurf, aber **+1 Hit-Wurf statt AP+1** | **Fehler: falscher Effekt-Typ** |
| Nephrekh | Translocation Beams: 6+ Invuln **zusätzlich** Advance→Translokation (kein Advance-Wurf, +6" Move, Schießverbot bis Rundenende, ignoriert Modelle/Terrain) | **nur** 6+ Invuln — Translokations-Mechanik fehlt komplett | **Fehler: Kernmechanik fehlt** |
| Sautekh | Relentless Advance: Morale-Reroll; Rapid-Fire-Waffen verdoppeln Attacken ≤18" | „Relentless Expansionists" — +3" Advance-Wurf, Assault-Waffen bei Advance „stationär" | **Fehler: komplett andere Fähigkeit** |
| **Nihilakh** | Aggressively Territorial — s. Entscheidung unten | „Acquisitive Grasp" — kein Fall Back in Objective-Reichweite | **Fehler: komplett andere Fähigkeit** |
| **Mephrit** | Solar Fury — s. Entscheidung unten | „Talent for Annihilation" — nur AP+1-Halbreichweite-Zeile, Range-Bonus fehlt, falscher Name | **Fehler: Name + Range-Bonus fehlt** |

Nebenbefund: Die „beide Direktiven bei reinem Dynastie-Heer"-Klausel (im 9E-Original bei
**allen 6** Codes vorhanden) ist inhaltlich bereits über `subfaction_affinity`/`round_choice`
abgedeckt (an „aktiv gewählte Dynastie" geknüpft statt wortwörtlich „jede Einheit trägt den
Code" — nur bei Mehrdynastie-Rosters relevant, kein Fix für Standard-Mono-Dynastie-Rosters
nötig).

**Doku-Drift-Nebenbefund (noch offen, kein Teil dieses Schritts):** `docs/spec/faction_abilities.md`
Kategorie 6 („Passive/Persistent") behauptet „Größtenteils abgedeckt durch `triggered`-Abilities
in `faction_abilities.yaml`" — das ist veraltet: Klan-Kulturs/Dynastic Codes liegen in
`subfaction_abilities.yaml` (anderer Datei-Scope) und sind laut obigem Kern-Befund nicht
wirksam. Spec-Nachzug empfohlen, sobald K2+ umgesetzt ist.

**Entscheide (Stakeholder S145):**

- **Frage 3 (Datenschema) = Option B:** neuer `ability_type: subfaction_passive` (statt den
  bestehenden `triggered`-Typ nur zu reparieren) — trennt „reaktive, event-getriggerte
  Fähigkeit" von „dauerhaft aktiver Passiv-Bonus, gebunden an eine feste Listenwahl" und deckt
  sich mit der in `docs/spec/faction_abilities.md` bereits vordefinierten, aber leeren
  **Kategorie 6**. Migration der 13 Bestandseinträge `triggered` → `subfaction_passive` ist
  Teil von K2+ (reiner Feldwert-Change, keine Struktur-Änderung).
- **Nihilakh-Sekundärklausel — geklärt:** Primärquelle
  `docs/work/wahapedia_necrons/faction_overview.txt:917` bestätigt die WebFetch-Fassung aus
  S144: „Each time an attack with an Armour Penetration characteristic of -1 is allocated to
  a model with this code, if that model's unit is wholly within its controller's deployment
  zone, that attack has an Armour Penetration characteristic of 0 instead." — **nicht** die
  Hit-Reroll-1-Fassung aus der WebSearch-Zweitquelle. Aggressively Territorial = Objective
  Secured (+1 Modell-Zählung wenn bereits vorhanden) **plus** diese AP-(-1)→AP-0-Klausel im
  eigenen Deployment Zone.
- **Mephrit zur Kontrolle ebenfalls primärquellen-verifiziert:**
  `faction_overview.txt:849–852` bestätigt Solar Fury wortgleich zum S144-Vergleich (+3" Range
  auf Fernkampfwaffen außer Pistols; unmod. Wound auf halbe Reichweite → AP+1).
- **Klasse-C-Fälle:** nach Bestandsmuster gelöst, kein neues Konzept nötig — Blood Axes
  (Light-Cover-Distanz), Nephrekh-Translokationsbewegung, Sautekh-RF-Reichweite bleiben
  Tisch-Hinweis (Klasse C, analog bestehendem `ignore_cover_half_range`-Muster) statt auf ein
  generisches Distanz-Tracking zurückgestellt zu werden.
- **Reihenfolge:** Wortlaut-Korrektur zuerst (kleiner, unabhängiger Bugfix), Engine-/UI-
  Verdrahtung danach — Ergebnis dieser Reihenfolge ist der K1/K2+-Split unten.
- **Modul-Ort für die neue Passiv-Logik:** eigenes Modul `gameMechanic/subfactionPassives.py`
  statt Erweiterung von `abilityEngine.py` (Konsent-Entscheid S145, Details
  `docs/goals/backlog.md` §4 „abilityEngine-Refactor-Vorplanung").

**Abgrenzung zu `subfaction_affinity`/Command Protocols (wichtig für K2+, additiv nicht
alternativ):** Klan-Kultur/Dynastic Code (dieses Konzept) und `round_choice`-Command-Protocols
sind zwei unabhängige, gleichzeitig aktive Mechaniken — kein Ersatz füreinander:

| | `subfaction_affinity` (bestehend, `round_choice`) | Klan-Kultur/Dynastic Code (dieses Konzept) |
|---|---|---|
| Datei | `faction_abilities.yaml` | `subfaction_abilities.yaml` |
| Aktivierung | Spielerwahl pro Runde (1 von 6 Protokollen) | Immer aktiv, sobald das Roster die Klan-/Dynastie-Wahl trägt — kein Aktivierungsschritt |
| Reichweite | Nur solange das Protokoll aktiv ist (rundenbegrenzt) | Permanent ab Listenerstellung, ganze Partie |
| Session-State | `active_protocol_id`/`active_directive`/`round_choice_assignments` | Keiner nötig — reiner Ableitungswert aus `roster.clan`/`roster.dynasty` |
| Engine-Funktion | `get_active_round_choice_modifier()` (bereits gebaut) | `get_active_subfaction_passives()` — Gegenstand von K2+ |

Beispiel: Ein Necron-Roster mit `dynasty: sautekh` hat den Sautekh-Dynastic-Code **permanent**
aktiv **und** kann in der Command-Phase weiterhin jedes der 6 Command Protocols wählen — nur
bei Wahl des Sautekh-zugeordneten Protokolls schaltet zusätzlich die Affinitäts-Bonus-Regel
(„beide Direktiven") frei. `subfaction_value_for(player)` (`gameMechanic/gameState.py:180`) ist
in beiden Fällen dieselbe Quelle und direkt wiederverwendbar für den neuen K2+-Filter.

**Scope-Split — K1 (dieser Schritt, Backlog-Prioritätenliste Rang 6) vs. K2+ (Rang 7):**

- **K1 = nur Nihilakh + Mephrit Wortlaut-Korrektur** in
  `data/wh40k_9e/necrons/subfaction_abilities.yaml` (data-only, kein Engine-/UI-Code) —
  Nihilakh: „Acquisitive Grasp" → „Aggressively Territorial" (Objective Secured + AP-(-1)→0-
  Klausel); Mephrit: „Talent for Annihilation" → „Solar Fury" (Name + fehlenden 3"-Range-
  Bonus ergänzen). Beide Wortlaute oben mit Zeilenbeleg zitiert.
- **K2+ (eigener Plan, vor Vergabe in ≤M-Briefs splitten):**
  - Wortlaut-Korrektur **Novokh, Sautekh, Nephrekh** (3 verbleibende Necron-Deltas) + **Ork
    Snakebites** (S8+-Ausnahme ergänzen) — beide data-only, aber bewusst nicht in K1, da der
    Stakeholder den Sofort-Scope auf Nihilakh+Mephrit begrenzt hat (S150).
  - Migration aller 13 Einträge `ability_type: triggered` → `subfaction_passive` (Option B).
  - Engine: `Condition.subfaction_id: str | None` (`gameObjects/ability.py`) +
    `check_conditions()`-Prüfung gegen `subfaction_value_for(player)`
    (`gameMechanic/gameState.py:180`, bereits vorhanden/wiederverwendbar) + neue Funktion
    `get_active_subfaction_passives(faction_dir, player)` in
    `gameMechanic/subfactionPassives.py` (permanent, kein Timing-Bezug, analog
    `get_active_round_choice_modifier`).
  - 4 neue Effekttypen für die toten `complex`-Handler: `ap_on_charge_or_charged` (Novokh),
    `rapid_fire_double_within_range` + `morale_reroll` (Sautekh),
    `advance_replace_with_translocate` (Nephrekh).
  - UI: `uiLayout/armyCard.py` generische `_render_subfaction_passive_badge()` (Info-Badge,
    kein Aktivierungsbutton, analog Kategorie-3-Muster); optional Unit-Ebene-Badge in
    `unitCard.py`.
  - `docs/spec/faction_abilities.md` Kategorie-6-Doku-Drift nachziehen (s. o.).
  - Aufwandsschätzung (S144-Grobschätzung, noch gültig): Orks S über alle Teilbereiche (kein
    `complex`-Rückstand); Necrons S/M/S/M (Daten/Engine/UI/Tests, 4 neue Effekttypen sind der
    größte Einzelposten); Engine-Grundgerüst S (einmalig, deckt beide Fraktionen ab). Gesamt
    grob S–M über beide Fraktionen.
  - Klassen-Einordnung A/B/C je Fähigkeit (nach `docs/spec/acceptance/rules.md`-Systematik):
    fast alle Zahlen-Modifikatoren = **Klasse A**; Blood Axes/Nephrekh-Translokationsbewegung/
    Sautekh-RF-Reichweite = **Klasse C** (Tisch-Anteil); Nihilakh/Mephrit sind nach der
    Wortlaut-Klärung oben jetzt vollständig A-tauglich (keine offene Klassifikation mehr).

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
