STATUS: ANSWERED

# Planning — Ziel7-Neustrukturierung (2026-07-03)

**Priorität:** P1 (Stufe A / S120 — Fundament + allgemeine Gefechtsoptionen)
**Scope:** Stakeholder-Entscheidungen aus dem S119-Live-Test in eine konkrete, umsetzbare
Struktur bringen: Player-A/B-Split für Gefechtsoptionen, fachliche Reihenfolge (allgemein →
Necrons → Orks → erst dann Ziel8), UX-Pass vor Ziel8, Design-Frage zur Farbunterscheidung.
Grundlage: `backlog.md` §5 „Neue offene Befunde (S119-Live-Test)" — dort bereits als
„wird in Ziel7-Neustrukturierung geplant (`docs/handoff/plan-ziel7-restruktur.md`)" referenziert.

---

## Stand-Check (Pflichtschritt, durchgeführt gegen `git log --oneline` + `backlog.md`)

- **P19/P20/P21 sind bereits committet** (`1f9d82b`, `dde16f3`, `dfebd27`) — `backlog.md` §5 führt
  alle drei korrekt als ERLEDIGT mit Commit-Hash und Vollsuite-Ergebnis (1405 passed / 99,11 %).
  Aktueller Code-Stand von `src/uiLayout/gameProtocoll.py` und `src/gameObjects/stratagem.py`
  wurde gelesen und bestätigt: `used_stratagem_battle_ids` ist bereits ein
  `dict[str, set[str]]` (P19-Fix), `stratagem_undo_visible()` existiert bereits als eigene reine
  Funktion (P21-Fix). Dieser Plan baut **auf diesem bereits gefixten Stand** auf.
- ⚠️ **Stale Checkbox/Stand-Text gefunden:** `.claude/tasks/next_session.md` „Aktueller Stand" +
  „▶ Nächster Schritt" beschreiben noch **S119 als offen** („Planner-Subagent plant gegen
  `backlog.md` §5 … P21 zuerst … Danach P19 … P20") — das ist überholt, S119 ist fertig und
  committet (s. o.). Das gehört beim nächsten Abschluss aktualisiert (nicht Teil dieses Plans,
  da reine Doku-Pflege ohne Freigabe-relevanten Code — als Hinweis an den Koordinator markiert).
- `docs/goals/ziel7.md` enthält ausschließlich den alten §6e/6f/6h-Backlog (subfaction
  Execute-Logik, Ability-Badges, Kat1–3 neue Fraktionen) — **keine** der drei S119-Live-Test-
  Anforderungen (Player-Split, Necron/Ork-Gefechtsoptionen, UX-Pass) ist dort bereits vermerkt.
  Einordnungsvorschlag siehe unten (Datei wird von diesem Plan **nicht** verändert).

---

## Regel-Klassifikation — die 7 Core-Stratagems (eigener Zug / gegnerischer Zug / beide)

Geprüft gegen `docs/work/wahapedia_core_rules/core_rules.txt:3124-3267` (Stratagem-Text) +
`core_rules.txt:1939-1975` (Fight-Phase-Ablauf) + `core_rules.txt:2087-2100` (Morale-Phase-Ablauf)
+ `rules_appendix.txt:2570` (Counter-Offensive, keine zusätzliche Einschränkung). Kein Punkt aus
dem Gedächtnis übernommen.

**Struktureller Befund vorab:** In 9E sind **Movement/Psychic/Shooting/Charge** reine
Aktiv-Spieler-Phasen (nur der Zugspieler bewegt/schießt/manifestiert/deklariert Angriffe; der
Gegner reagiert nur über explizite reaktive Regeln). **Fight** und **Morale** dagegen alternieren
ausdrücklich zwischen beiden Spielern innerhalb derselben Phase (`core_rules.txt:1941`
„Starting with the player whose turn is not taking place, the players must alternate…";
`core_rules.txt:2094` „Starting with the player whose turn is taking place, the players must
alternate…"). Das ist die Erklärung, warum `player: both` nicht nur bei Command Re-Roll/
Emergency Disembarkation auftaucht, sondern strukturell auch für Fight- und Morale-Stratagems
in Frage kommt.

| Stratagem | Phase | YAML `player` | Regeltext-Befund | Bewertung |
|---|---|---|---|---|
| Command Re-Roll | movement/psychic/shooting/charge/fight | `both` | Rerollt Rolls, die je nach Rolltyp im eigenen (Hit/Wound/Damage/Advance/Charge/Psi/Attacken-Zahl) **oder** im gegnerischen Zug (Save, Deny the Witch als Verteidiger) anfallen | ✅ korrekt |
| Cut Them Down | movement | `inactive` | Reagiert auf gegnerisches Fall Back — das passiert in **dessen** (dem Zugspieler-)Movement | ✅ korrekt |
| Desperate Breakout | movement | `active` | „Use this Stratagem in **your** Movement phase" — nur eigener Zug | ✅ korrekt |
| Emergency Disembarkation | any | `both` | Transport kann in beiden Zügen zerstört werden | ✅ korrekt |
| Fire Overwatch | charge | `inactive` | Reagiert auf gegnerisch deklarierten Angriff | ✅ korrekt |
| **Counter-Offensive** | fight | `inactive` | Kein „your turn"-Vorbehalt im Text; Fight Phase alterniert ausdrücklich zwischen **beiden** Spielern (`core_rules.txt:1941`) — jede Seite kann auf ein „enemy unit has fought" reagieren, auch der Zugspieler (wenn zuerst der Gegner dran war) | 🔴 **DRIFT** — sollte `both` sein, nicht `inactive` |
| **Insane Bravery** | morale | `active` | „before you take a Morale test for a unit **in your army**" — Morale Phase alterniert ausdrücklich zwischen **beiden** Spielern (`core_rules.txt:2094`); auch der Nicht-Zugspieler testet in derselben Morale-Phase für eigene Verluste (z. B. aus dem gegnerischen Fight) | 🔴 **DRIFT** — sollte `both` sein, nicht `active` |

**Konsequenz für Stufe A:** Die Anzeige-Logik „aktiv/inaktiv je Spieler" (s. u.) muss unabhängig
von diesem Datenbefund korrekt implementiert werden (sie liest nur das YAML-Feld) — aber die
zwei Drifts sollten **vor oder mit** dem Stufe-A-Umbau in `data/wh40k_9e/_shared/stratagems.yaml`
korrigiert werden, sonst wird eine falsche Regel nur „hübscher falsch" dargestellt. Aufgenommen
als Stufe-A-Task 0 (klein, XS).

**Zusätzlicher struktureller Befund (kein Drift, aber bisher ungetestet):** Die Zuordnung
„welcher Spieler darf dieses Stratagem sehen" (`s.player` gegen aktiv/inaktiv) existiert aktuell
**nur** als Seiteneffekt in `gameProtocoll.py:165` (`spending_faction = inactive_faction if
s.player == "inactive" else active_faction`) — eine reine Entscheidungsfunktion dafür existiert
nicht, ist also nicht unit-getestet, obwohl sie Business-Logik (keine Render-Logik) ist. Stufe A
extrahiert sie (Task 1, s. u.) — das ist zugleich der Fix für Finding #2 (Attributions-Bug) und
schließt eine bisher unbemerkte Testlücke.

---

## Stufe A (S120) — Fundament + allgemeine Gefechtsoptionen

**Ziel:** Stratagems-Tab zeigt zwei feste Bereiche — links `first_player`, rechts
`second_player` (Domänen-Constraint, nie an `active` gebunden — analog `app.py:39-51`, wo die
Army-Sidebars bereits exakt so aufgeteilt sind). Jeder Bereich zeigt ausschließlich die eigenen
ladbaren Stratagems (`_shared` + eigene Fraktion), gefiltert nach „darf DIESER Spieler es gerade
nutzen" (aus `s.player` + ob dieser Spieler aktuell aktiv ist). CP, used-Sets und Undo sind pro
Spieler-Slot getrennt.

| # | Aufgabe | Effort | Token-Schätzung | Modus | Tier | Scope-Zeile / Dateien |
|---|---|---|---|---|---|---|
| 0 | YAML-Drift fixen: Counter-Offensive + Insane Bravery `player: both` | XS | ~4k | Gate | Sonnet | `data/wh40k_9e/_shared/stratagems.yaml`; Test-Fixtures in `test_stratagem.py`, die `player="inactive"`/`"active"` für diese beiden IDs annehmen, prüfen/anpassen |
| 1 | Pure Usability-Funktion + Player-Split-Rendering (Findings #1 + #2) | M | ~30k | Gate | Sonnet | `Stratagem-Effekt umsetzen` (agent_scopes.md) + `src/uiLayout/gameProtocoll.py` |
| 2 | `used_stratagem_ids` auf Player-Slot migrieren (Finding #3) | S/M | ~20k | Gate | Sonnet | `src/gameMechanic/game_state.py`, `src/uiLayout/gameProtocoll.py`, `tests/gameMechanic/test_game_state.py`, `tests/gameMechanic/test_triggered_relics.py` |
| 3 | Manuelle UI-Verifikation (Render-Code, PFLICHT) | — | in 1+2 enthalten | Gate | Stakeholder | siehe Checkliste unten |

**Reihenfolge zwingend:** 0 → 1 → 2 (Task 2 baut auf denselben Zeilen wie Task 1 auf — analog
zum Reihenfolge-Hinweis aus dem S119-Plan (Handoff gelöscht S120): erst Task 1 fertig committen, dann Task 2 beginnen,
nicht parallel im selben Diff).

### Task 0 — YAML-Drift fixen

`data/wh40k_9e/_shared/stratagems.yaml`: `player: inactive` → `player: both` bei
`wh40k_9e.shared.stratagem.counter_offensive`; `player: active` → `player: both` bei
`wh40k_9e.shared.stratagem.insane_bravery`. Betrifft nur Kernregel-Korrektheit, keine
Architektur-Änderung. Regressionstest: bestehende `test_stratagem.py`-Fixtures, die diese beiden
IDs mit dem alten `player`-Wert konstruieren, auf `both` umstellen; falls ein Test explizit
„inactive blockt den aktiven Spieler" für Counter-Offensive/Insane Bravery prüft, muss er neu
geschrieben werden (beide Spieler dürfen jetzt).

### Task 1 — Pure Usability-Funktion + Player-Split-Rendering

**Neue reine Funktion** (Streamlit-frei, testbar, in `src/gameObjects/stratagem.py` neben
`stratagem_visibility`/`stratagem_undo_visible`):

```python
def stratagem_usable_by_player(player_field: str, is_this_player_active: bool) -> bool:
    """Whether a stratagem's `player` field permits use by the given player.

    player_field: Stratagem.player ("active" | "inactive" | "both").
    is_this_player_active: True if the player in question currently holds the turn.
    """
```

**Rendering-Umbau** (`gameProtocoll.py`, `_render_stratagems()`): statt einer verschmolzenen
Liste `stratagems_active + stratagems_inactive` zwei unabhängige Spalten
(`st.columns(2)`, analog `app.py:39` `left, center, right = st.columns(...)` +
`render_army_list(first_player)` / `render_army_list(second_player)`):

- Spalte links = `first_player`, Spalte rechts = `second_player` (fest, nie an `active` gebunden).
- Je Spalte: `load_stratagems(faction_dir_for(player))` **einmal** für den eigenen Spieler (keine
  Konkatenation zweier Listen mehr → Finding #1 strukturell gelöst).
- Je Stratagem: `stratagem_usable_by_player(s.player, player == active_faction)` **vor**
  `stratagem_visibility(...)` filtern. `spending_faction` entfällt als hergeleitete Variable —
  die Spalte selbst IST der spending player (Finding #2 strukturell gelöst, keine Ableitung mehr
  nötig).
- CP-Anzeige je Spalte: `cp.get(player, 0)` direkt (kein `cp_active`/`cp_inactive`-Umweg mehr).

**Betroffene Dateien:**
- `src/gameObjects/stratagem.py` — neue Funktion `stratagem_usable_by_player`
- `src/uiLayout/gameProtocoll.py` — `_render_stratagems()` auf Zwei-Spalten-Struktur umbauen
- `tests/gameObjects/test_stratagem.py` — neue Tests für `stratagem_usable_by_player`
  (alle 3×2-Fälle: `active`/`inactive`/`both` × `is_this_player_active` True/False)

**Testebenen:**
- Unit-Test (PFLICHT): `stratagem_usable_by_player` — 6 Fälle (Wahrheitstabelle oben).
- Regressionstest (PFLICHT): kein Stratagem erscheint doppelt in derselben Spalte (Finding #1);
  ein `player: active`-Stratagem erscheint in der Spalte des aktiven Spielers, nicht in der des
  inaktiven (Finding #2 — Attribution).
- Manuelle UI-Verifikation (Render-Code, PFLICHT, s. Checkliste unten).

**Token-Schätzung:** ~30k. **Tier: Sonnet** (Umbau nach geklärtem Root Cause, aber echte
Render-Logik-Arbeit + neue reine Funktion + Tests, kein reiner Lookup).

### Task 2 — `used_stratagem_ids` auf Player-Slot migrieren

**Root Cause (Finding #3, bereits verifiziert):** `used_stratagem_ids` ist aktuell ein
**einziges globales** `set[str]` (`game_state.py:420`, Reset `game_state.py:531`) — beide Spieler
teilen sich denselben Phasen-Verbrauchs-Status. Sobald Spalte-A und Spalte-B (Task 1) unabhängig
rendern, muss auch dieses Set pro Spieler getrennt sein, sonst „verbraucht" ein Klick von Spieler
A dasselbe Phasenfenster-Flag für Spieler B mit (analog zum P19-Bug, nur auf der Phase- statt der
Battle-Skala).

**Fix-Ansatz:** Konsistent mit dem bereits etablierten Muster **in dieser Datei** —
`cp: dict[str, faction] → int` und `used_stratagem_battle_ids: dict[str, set[str]]` (seit P19)
sind beide bereits Player-Slot-keyed Dicts. `used_stratagem_ids` auf dieselbe Form heben:
`used_stratagem_ids: dict[str, set[str]] = {}`, Key = Player-Slot-Wert (wie `cp`/`battle_ids`).
Das ist der kleinste konsistente Diff (drei parallele Dicts statt zwei Dicts + ein Fremdkörper-
Set). Alternative — eigene `round_choice_state_key`-artige Top-Level-Keys pro Spieler
(`used_stratagem_ids_<player>`) — ist das an anderer Stelle etablierte Muster (Round-Choice-
Direktiven), aber ein Strukturbruch **innerhalb** dieser Datei, wo cp/battle_ids bereits Dicts
sind. **Empfehlung: Dict-Form**, damit `_render_stratagems()` alle drei Player-Slot-Werte
(`cp`, `used_stratagem_ids`, `used_stratagem_battle_ids`) einheitlich mit `.get(player, ...)`
liest — Executor kann bei technischen Einwänden auf `round_choice_state_key` ausweichen, dann
aber **konsistent für alle drei**, nicht gemischt.

**Betroffene Dateien:**
- `src/gameMechanic/game_state.py:420,531` — Init + Reset auf `dict[str, set[str]] = {}` /
  `= {}` (statt `= set()`) umstellen; Reset darf **nur** den Eintrag der laufenden Phase leeren
  (weiterhin **beide** Spieler-Slots bei jedem Phasenwechsel, das Verhalten bleibt: „bei jedem
  Phasenwechsel geleert" — nur jetzt strukturiert pro Spieler statt global)
- `src/uiLayout/gameProtocoll.py` — alle Lese-/Schreibstellen (`used_ids`-Variable) auf
  `used_stratagem_ids_by_player.get(player, set())` umstellen, analog zu `used_battle_ids_by_faction`
- `tests/gameMechanic/test_game_state.py:625,674-677` — Fixtures + `test_resets_used_stratagem_ids`
  auf Dict-Form migrieren (nicht still anpassen — Verhalten bleibt gleich, nur Datentyp; Test bleibt
  ein Regressionstest für „wird bei Phasenwechsel geleert", jetzt pro Spieler geprüft)
- `tests/gameMechanic/test_triggered_relics.py:136` — Fixture `used_stratagem_ids=set()` auf
  Dict-Form migrieren (falls das Modul überhaupt Player-Kontext hat — sonst leeres Dict `{}`
  reicht, da der Test das Feld vermutlich nur als Pflicht-Parameter durchreicht; Executor prüft
  konkret, ob der Test player-scoped Verhalten überhaupt braucht)
- Neuer Test (PFLICHT, Regressionstest): analog zu P19s
  `test_battle_scoped_stratagem_used_by_one_player_does_not_block_other`, aber für die
  **phasen**-scoped Variante — z. B.
  `test_phase_scoped_stratagem_used_by_one_player_does_not_block_other`.

**Testebenen:**
- Unit-Tests wie oben (Fixture-Migration + neuer Cross-Player-Test).
- Manuelle UI-Verifikation (Render-Code, PFLICHT, s. Checkliste unten).

**Token-Schätzung:** ~20k. **Tier: Sonnet.**

### Manuelle UI-Verifikation (PFLICHT vor „fertig", gilt für Task 1 + 2 gemeinsam)

Mit laufender App, zwei verschiedenen Fraktionen (z. B. Necrons vs. Orks):
1. Stratagems-Tab zeigt zwei Bereiche nebeneinander, links = Startspieler, rechts = Zweitspieler
   — Zuordnung bleibt fix, auch nach Spielerwechsel (`active` wechselt, Spalten nicht).
2. Core-Stratagems (`_shared`) erscheinen in **beiden** Spalten je genau einmal (nicht doppelt
   innerhalb einer Spalte, nicht fehlend in einer Spalte).
3. Ein `player: inactive`-Stratagem (z. B. Fire Overwatch) ist nur in der Spalte des gerade
   **nicht**-aktiven Spielers klickbar/sichtbar-relevant; beim Spielerwechsel dreht sich das um.
4. Counter-Offensive (Fight-Phase) und Insane Bravery (Morale-Phase) sind nach Task 0 in
   **beiden** Spalten nutzbar (Regel-Fix sichtbar machen).
5. once_per_phase-Stratagem: Spieler A benutzt eines → nur A's Kopie greyed/„(used)", B's Kopie
   bleibt unberührt (Phase-Scope-Fix aus Task 2).
6. once_per_battle-Stratagem: wie 5, aber battle-scoped (Regressions-Check, dass der bereits
   gefixte P19-Stand nicht durch den Umbau bricht).
7. Undo (P21-Verhalten) funktioniert weiterhin nur im selben Phasenfenster, jetzt pro Spalte
   unabhängig geprüft.

---

## Stufe B — Necron-Gefechtsoptionen (grob, Detailplanung in eigener Session)

**Ist-Stand:** `data/wh40k_9e/necrons/stratagems.yaml` existiert bereits und wird von
`load_stratagems("necrons")` mitgeladen (Loader-Pattern bereits generisch, keine Necron-Logik in
`src/`). Nach Stufe A profitieren Necron-Stratagems automatisch von Player-Split +
korrektem Player-Slot-Tracking — **kein Necron-spezifischer Code nötig**, nur Daten-/Regel-
Review.

**Delta zu prüfen (nächste Session):**
- Vollständigkeitsabgleich `data/wh40k_9e/necrons/stratagems.yaml` gegen
  `docs/work/wahapedia_necrons/` (fehlende Stratagems? falsche `player`/`phase`/`stage`-Felder
  analog zum Core-Drift oben — derselbe Klassifikations-Fehler ist pro Fraktion denkbar).
- `once_per_battle`/`conditions`-Felder gegen Regeltext prüfen (Necron-Stratagems mit
  Keyword-Bedingungen, z. B. dynastie-spezifische).
- Manuelle UI-Verifikation mit echtem Necron-Roster nach dem Delta-Fix.

**Effort-Einschätzung:** S–M je nach Delta-Größe (unbekannt bis Review erfolgt ist).

## Stufe C — Ork-Gefechtsoptionen (grob, Detailplanung in eigener Session)

Analog Stufe B: `data/wh40k_9e/orks/stratagems.yaml` existiert, Loader generisch. Gleicher
Delta-Abgleich gegen `docs/work/wahapedia_orks/` nötig. **Reihenfolge nach Stakeholder-Vorgabe:
erst nach Stufe B abschließen**, da die allgemeine Logik (Stufe A) bereits für beide Fraktionen
gilt und Stufe B als „zweite Anwendung des Musters" den Delta-Prozess für Stufe C schärft.

---

## UX-/UI-Pass vor Ziel8 — Kandidatenliste (Entscheidungsvorlage, keine Priorisierung)

Quellen UI-Pass S118 und Review S113 (Handoffs gelöscht) sind **vollständig abgearbeitet** (17/20 direkt
erfüllt, die restlichen 3 als P19/P20/P21 committet) — daraus gibt es aktuell **keine offenen
Punkte** mehr für diesen Pass. Die folgende Liste sind eigene Beobachtungen aus dem Render-Code
(`gameProtocoll.py`) im Zuge dieser Planung — rein als Sammlung für den Stakeholder, keine
Bewertung/Umsetzung durch diesen Plan:

- **„(inactive)"-Suffix im Label wird durch den Player-Split obsolet** — aktuell hängt
  `gameProtocoll.py:190-191` ein `*({inactive_faction})*` an inaktive Stratagems, um zu zeigen
  „das gehört dem anderen". Nach Stufe A steht das Stratagem bereits in der richtigen Spalte —
  der Suffix wäre redundant und sollte vermutlich entfallen (Teil von Task 1, aber als
  UX-Frage hier vermerkt, falls der Stakeholder ihn bewusst behalten will).
- **Battle Log bleibt global, Stratagems werden pro Spieler gesplittet** — nach Stufe A haben
  die beiden Tabs im selben `gameProtocoll`-Bereich unterschiedliche Layout-Philosophien
  (ein globaler Log vs. zwei Spielerspalten). Bewusste Inkonsistenz oder sollte der Battle Log
  langfristig demselben Muster folgen?
- **Expander-Dichte bei zwei schmaleren Spalten** — mit `st.columns(2)` wird jede Spalte halb so
  breit; lange Stratagem-Namen/CP-Kosten-Zeilen könnten enger umbrechen. Reiner Verifikationspunkt
  für den manuellen UI-Check in Stufe A, kein separates UX-Thema.
- **Kein Hinweis, WANN im Regeltext ein Stratagem greift** (`event`/`timing`-Felder existieren im
  Datenmodell — z. B. `on_declaration`, `after_roll` — werden aber nirgends angezeigt). Könnte für
  Spieler hilfreich sein zu sehen „reagiert auf X", ist aber ein neues Feature, kein Bugfix.

---

## Design-Frage (NEEDS-DECISION — Stakeholder entscheidet, keine Eigenentscheidung)

**Frage:** Innerhalb der neuen Spieler-Bereiche (Stufe A) — sollen allgemeine (Core/`_shared`)
und fraktionsspezifische Stratagems farblich unterschieden werden?

Bezug: `docs/spec/design_colors.md` §4c „Fraktionsfarben: NEIN — einheitliches Gold-Theme" und
§4a-Begründung „damit die Farben nicht ausgehen" (bewusst sparsamer Farbraum, etabliert 2026-06-10).

**Option 1 — Keine Farbunterscheidung, nur Sektions-Header** (z. B. Zwischenüberschrift
„Allgemein" vor den `_shared`-Einträgen, „<Fraktionsname>" vor den fraktionseigenen, innerhalb
derselben Spieler-Spalte). Konsistent mit dem bestehenden Beschluss, keine neue Farbe, geringster
Aufwand.

**Option 2 — Dezente Unterscheidung über bereits definierte Tokens** (kein neuer Hex-Wert): z. B.
`--arb-muted` (`#6b5f44`, gedämpft) als Chip/Label „Core" vor Shared-Stratagems, kein Chip bei
fraktionseigenen (impliziter Kontrast). Nutzt nur bestehende Palette, aber führt einen neuen
visuellen Unterscheidungs-Layer ein, den §4a gerade vermeiden wollte.

**Option 3 — Neuer eigener Farbslot** (z. B. eigene Akzentfarbe nur für Core-Stratagems).
**Nicht empfohlen** — widerspricht der bestehenden „Farben gehen nicht aus"-Linie ohne erkennbaren
neuen Informationsgewinn gegenüber Option 1.

**Empfehlung (mit Begründung, keine Festlegung):** Option 1 — der Player-Split selbst ist bereits
die entscheidende neue Struktur; eine zusätzliche Farbdimension für Core-vs-Fraktion innerhalb
einer Spalte bringt wenig zusätzliche Lesbarkeit, kostet aber einen weiteren Sonderfall im
ohnehin schon sparsamen Farbsystem. Entscheidung liegt beim Stakeholder.

---

## Einordnung — was passiert mit dem bestehenden `ziel7.md`-Inhalt?

**Nur Vorschlag — `ziel7.md` wird von diesem Plan nicht verändert.**

Der aktuelle `ziel7.md`-Inhalt (§6e Execute-Logik, §6f Ability-Badges, §6h Kat1–3 neue
Fraktionen) ist vollständig unabhängig von den drei S119-Live-Test-Anforderungen — keine
Blockierung in beide Richtungen (6e `collect_modifiers_for_phase` betrifft Ability-Modifier,
nicht die Stratagem-Tab-Struktur; `active_modifiers`-Anhängen beim Stratagem-Einsatz
funktioniert in `gameProtocoll.py` bereits unabhängig davon, s. Zeile 230–253).

Vorschlag: `ziel7.md` um einen neuen Abschnitt **„0. Gefechtsoptionen Spieler-Split (S120+,
fachliche Priorität 1)"** vor dem bestehenden „Backlog — eingehende Punkte (aus Ziel 6
ausgelagert)" ergänzen, der Stufe A/B/C aus diesem Plan referenziert (Verweis auf diese Datei,
keine Duplizierung der Task-Tabellen). Der bestehende §6e/6f/6h-Block bleibt als „danach" stehen,
ggf. mit einem Hinweis-Satz „nach Abschluss Stufe A–C" versehen, damit die fachliche Reihenfolge
aus der Stakeholder-Vorgabe auch in der Zieldatei sichtbar ist, nicht nur in diesem Handoff.
Umsetzung dieses Vorschlags selbst ist ein XS-Task (~3k) beim nächsten Abschluss, sobald Stufe A
freigegeben/gestartet ist — kein Blocker für den Start von Stufe A.

---

## Nächster Schritt

Stufe A / Task 0 (YAML-Drift-Fix) + Task 1 (Player-Split-Rendering) — nach Freigabe direkt an
Executor-Subagent (Sonnet). Task 2 erst nach Task 1 committet.

---

## Offene Fragen an den Stakeholder

1. **Design-Frage (s. oben):** Option 1 (nur Sektions-Header, keine Farbe) vs. Option 2 (dezente
   Token-Wiederverwendung) für Core- vs. Fraktions-Stratagems innerhalb einer Spieler-Spalte.
   Empfehlung: Option 1.
   Entscheidung: Option 1

2. **YAML-Drift-Fix (Task 0):** Counter-Offensive und Insane Bravery von `player: inactive`/
   `active` auf `player: both` korrigieren, wie oben hergeleitet — Zustimmung zur Herleitung
   (Fight-/Morale-Phase alternieren zwischen beiden Spielern), oder soll das nochmal separat
   gegen Wahapedia-FAQ/Designer-Kommentar gegengeprüft werden, bevor der Regeltext-Fund
   umgesetzt wird?
   Entscheidung: Wir haben an sich alle Wahapedia-Quellen gezogen und können dagegegen prüfen. Wenn also der Wechsel auf "both player" den Regeln entspricht, dann machen wir es so.

3. **`used_stratagem_ids`-Migration (Task 2):** Dict-Form (konsistent mit `cp`/
   `used_stratagem_battle_ids` in derselben Datei, Empfehlung) vs. `round_choice_state_key`-Form
   (konsistent mit dem an anderer Stelle etablierten Muster) — welche Konvention?
   Entscheidung: Ich folge deiner Empfehlung.

4. **„(inactive)"-Label-Suffix** (UX-Kandidat oben): nach dem Player-Split entfernen (da
   redundant zur Spalten-Zuordnung) oder bewusst behalten?
   Entscheidung: Ich verstehe hier die Frage nicht. Nachgereicht nach Koordinator-Erklärung
   (Retro S119): Suffix nach dem Spalten-Split ENTFERNEN (redundant zur Spalten-Zuordnung).

5. **`ziel7.md`-Restrukturierung** (Einordnung oben): Vorschlag „neuer §0-Block vor dem
   bestehenden §6e/6f/6h-Backlog" übernehmen, oder anderes Vorgehen gewünscht?
   Entscheidung: Ich folge deiner Empfehlung.

6. **Stale `next_session.md`-Stand** (s. Stand-Check oben): beim nächsten Abschluss korrigieren
   (S119 als erledigt markieren, auf diesen Plan verweisen) — Bestätigung, dass das reicht, oder
   soll das vorgezogen werden?
   Entscheidung: Bestätigung, dass es reicht
