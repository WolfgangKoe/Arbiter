# Plan 032 — Necron-Stratagem-Semantik: Restarbeit aus dem S123-Vollabgleich

## Status

- **Priority**: P2 (MITTEL) — betrifft Spielkorrektheit einzelner Stratagems, nicht die
  UI-Infrastruktur (die ist seit Ziel7 Stufe A generisch und funktioniert)
- **Effort**: L (mehrere unabhängige Datenkorrekturen + zwei Schema-Erweiterungen)
- **Depends on**: keine harte Abhängigkeit; profitiert von Plan 015 (reaktive Stratagem-UI),
  falls einzelne `event`-Werte hier erstmals einen echten Konsumenten bekommen sollen
- **Category**: data / schema (Necron-Stratagems, Regelkonformität)
- **Planned at**: 2026-07-04 (S123-Vollabgleich, 59 → 60 Necron-Stratagems gegen
  `docs/work/wahapedia_necrons/stratagems.txt`, 27 Befunde)

---

## Kontext

Der S123-Vollabgleich hat alle Necron-Stratagems in `data/wh40k_9e/necrons/stratagems.yaml`
gegen den Wahapedia-Regeltext geprüft. Die HOCH-priorisierten, mit dem **bestehenden** Schema
sauber abbildbaren Befunde wurden bereits in derselben Session gefixt (siehe Commit-lose
Änderung im selben Arbeitsschritt — `whirling_onslaught`, `resurrection_protocols`,
`efficient_disintegration`, `relentless_onslaught`, `fractal_targeting`). Dieser Plan bündelt
den Rest: Befunde, die entweder eine Schema-Erweiterung brauchen (neue Effekttypen, OR-
Bedingungen, variable Kosten, `min_round`) oder reine Daten-Nacharbeit sind, die aber bewusst
nicht "auf Verdacht" mit einem unpassenden Effekttyp modelliert wurde (falsch ist schlimmer
als unmodelliert, CLAUDE.md-Prinzip).

**Wichtig für den Executor:** Jede Korrektur hier MUSS gegen das Zitat in
`docs/work/wahapedia_necrons/stratagems.txt` geprüft werden, nicht aus dem Gedächtnis.

---

## (a) Schema-Erweiterungen nötig

Diese Befunde brauchen eine Erweiterung von `gameObjects/stratagem.py` (`Stratagem`-Dataclass)
und/oder `gameObjects/ability.py` (`Effect`-Dataclass), bevor die Daten sauber modelliert werden
können. Kein Daten-Fix ohne vorherige Schema-Entscheidung (Stakeholder-Freigabe für den
Code-Anteil einholen, bevor die YAML angefasst wird).

1. **Variable CP-Kosten mit TITANIC-Bedingung** (`stellar_alignment_protocol`:
   1CP normal / 2CP TITANIC; `dimensional_destabilisation`: analog — prüfen). `cp_cost` ist
   aktuell ein einzelner `int`; variable Kosten werden bisher nur in `rule_text` erklärt
   (Konvention, siehe `curse_of_the_phaeron`: `cp_cost: 1 # variable: 1CP normally, 3CP für
   TITANIC`). Vorschlag: Feld bleibt Minimalkosten + `rule_text` beschreibt den Rest (bereits
   Konvention) — prüfen, ob `stellar_alignment_protocol`/`dimensional_destabilisation` diese
   Konvention schon einhalten oder nachgezogen werden müssen.
2. **Missionsabhängiges `once_per_battle` 2×/3×** (`dynastic_heirlooms`, `rarefied_nobility`:
   "once normally, twice in Strike Force, three times in Onslaught"). Aktuelles
   `once_per_battle: bool` kann keine missionsabhängige Zählung abbilden. Braucht entweder ein
   `max_uses_per_battle: int | dict[str, int]`-Feld oder eine explizite Regel im
   Session-State-Tracking, die die Missionsgröße kennt.
3. **`min_round`-Feld für Stratagems** (`prismatic_dimensional_breach`: nicht in Runde 1
   nutzbar). `Ability`/`Condition` (in `ability.py`) hat bereits `min_round: int | None` — die
   `Stratagem`-Dataclass hat kein Äquivalent. Kleinster Fix: `Stratagem.min_round: int | None
   = None` ergänzen + in `stratagem_visibility()` auswerten.
4. **OR in `conditions`** — mehrere Stratagems richten sich an "Einheit A ODER Einheit B", das
   aktuelle Schema ist AND-only (`conditions: list[str]`, siehe Kopfkommentar
   stratagems.yaml Z. 7). Betroffen:
   - `extermination_protocols`: LOKHUST DESTROYERS **or** LOKHUST HEAVY DESTROYERS
   - `efficient_disintegration`: dieselbe OR-Bedingung (bereits mit Kommentar markiert)
   - `whirling_onslaught`: SKORPEKH DESTROYERS **or** SKORPEKH LORD (aktuell overbroad als
     `[DESTROYER CULT]` modelliert, bereits mit Kommentar markiert)
   - `resurrection_protocols` (1 CP-Variante): INFANTRY NOBLE **or** INFANTRY CRYPTEK (aktuell
     overbroad als `[INFANTRY]` modelliert, bereits mit Kommentar markiert)
   Vorschlag: `conditions: list[str] | list[list[str]]` (äußere Liste = OR, innere Liste = AND)
   oder ein separates `conditions_any_of: list[str]`-Feld für den einfacheren Fall
   "eine von mehreren Einheiten, keine weiteren Keyword-Kombination".
5. **Waffenart-Restriktion im Effekt** — kein Feld für "nur Waffen vom Typ X":
   - `disintegration_capacitors`: nur gauss-Waffen
   - `hyperdense_particle_beams`: nur particle beamer/particle caster
   - `relentless_onslaught`: nur Rapid-Fire-Waffen (Effekt aktuell entfernt, siehe unten)
   - `efficient_disintegration`: nur gauss cannon/gauss destructor (bereits mit Kommentar
     markiert)
   Vorschlag: `Effect.weapon_type: str | None` ergänzen (analog zu `Effect.stat`).
6. **Ziel-Bindung „that enemy unit"** (Dauer-Effekt bindet an ein bestimmtes, vorher
   ausgewähltes gegnerisches Ziel, nicht an "irgendein Ziel"):
   - `methodical_destruction`: +1 Hit für andere SAUTEKH-Einheiten gegen dasselbe Ziel
   - `revenge_of_the_doomstalker`: dauerhafter +1-Hit-Bonus gegen dasselbe Ziel bis Spielende
   Kein Konzept für "gemerktes Ziel über Phasengrenzen" im aktuellen Modifier-/Effect-Schema.
7. **Effekttyp „Extra-Treffer auf unmodifizierter 6"** — es gibt zwar `extra_hit_on_6` in
   `data/wh40k_9e/orks/*.yaml` (unparametrisiert, nur `target`/`phase`, kein Waffenart-Filter,
   und ohne Engine-Konsumenten — rein deskriptiv), das reicht für `relentless_onslaught` nicht,
   weil dort zusätzlich die Rapid-Fire-Restriktion (Punkt 5) fehlt. Erst nach Punkt 5 sauber
   modellierbar.
8. **`modifier`-Feld-Semantik uneinheitlich: exakt-6 vs. 5+-Schwelle.** Vergleiche
   `flensing_capacitors` (`modifier: 5`, "unmodified successful hit roll of 5+ automatically
   wounds") mit `disintegration_capacitors` (`modifier` fehlt/anders, "unmodified hit roll of 6
   automatically wounds" — exakt 6). Beide nutzen denselben Effekttyp `auto_wound`, aber mit
   unterschiedlicher Schwellen-Semantik (">=5" vs. "==6"). Braucht ein explizites
   `threshold_mode: "exact" | "at_least"`-Feld oder zwei getrennte Effekttypen.
9. **Wounds≥10-Bedingung** (`stellar_alignment_protocol`: nur NECRONS VEHICLE mit
   Wounds-Charakteristik ≥10). Kein `conditions`-Ausdruck für Statistik-Schwellen (nur
   Keywords). Braucht eine Erweiterung analog zu `Condition.needs_healing` in `ability.py`.

## (b) Reine Daten-Nacharbeit (nach Schema-Erweiterung, kein weiterer Code nötig)

Sobald (a) steht, sind folgende Effektzweige/Parameter reine YAML-Ergänzungen:

- `atavistic_instigation`: "ducks for cover"-Zweig fehlt (aktuell nur der "braces" D3-MW-Zweig
  modelliert?) — gegen `stratagems.txt` Z. 268 prüfen, welcher Zweig aktuell in der YAML steht,
  fehlenden Zweig ergänzen (D3-Angriffe-Malus + Overwatch/Set-to-Defend-Sperre für "ducks for
  cover").
- `self_destruction`: Würfel-Ergebnis 2–5 → D3 MW, 6 → 3 MW (aktuell vermutlich nur ein
  Pauschalwert modelliert) — zweizweigigen Würfeltabellen-Effekt ergänzen.
- `overkill_protocols`: "whip coils"-Zweig (zusätzlicher Trefferwurf) fehlt neben dem
  vicious-claws-AP-Zweig.
- `aggression_overrides`: WS fix auf 2+ (zusätzlich zur Move+2"-Modellierung, falls die
  WS-Änderung noch fehlt).
- `murderous_demise`: Wahl schießen ODER kämpfen (Exklusivität) — aktuell evtl. nur ein Zweig
  oder ohne Exklusivitäts-Constraint modelliert.
- `canoptek_overdrive`: Bedingungen "not fought this phase", "melee attack" als
  Effekt-Constraints ergänzen (nicht nur Trigger-Bedingung).
- `malevolent_arcing`: 4+, 1 MW, 6" Radius, nur bei Tesla-Waffen — Waffenart-Filter (Punkt 5)
  + Bedingungsparameter.
- `reconstitution_protocols`: `amount` korrigieren von "D3" auf "D6" (Ghost Ark Repair Barge
  mit dieser Stratagem heilt D6 statt D3 Modelle) — **das ist ein reiner Wertefehler, kein
  Schema-Problem**, sollte VOR den größeren Posten separat und schnell gefixt werden.
- `fractal_targeting`-Rest: Waffenart-Override (Rapid Fire → Assault 2) + Advance-Malus-Ausnahme
  (siehe Kommentar in der YAML, S123 bereits als unmodelliert markiert).
- `resurrection_protocols`-Rest: OR-Bedingung (siehe a.4), falls Schema das trägt.

## (c) Klasse B — Tisch-Hinweis statt Mechanik

Diese Effekte sind reine räumliche/zähl-basierte Bedingungen, die die App nicht prüfen kann
(kein Koordinatenmodell, keine Tischgeometrie). App zeigt nur den Regeltext als Hinweis:

- `eternal_protectors`: 3"-Nähe zu einem NOBLE-Modell der eigenen Dynastie — räumliche
  Bedingung, nicht app-prüfbar.
- `talent_for_annihilation`: unmodifizierter Wurf von 6 löst 1 MW aus, Cap 3 MW pro Phase über
  diese Stratagem — der Wurf selbst ist prüfbar, aber der Phasen-Cap braucht Session-State-
  Tracking pro Stratagem-Nutzung; als Klasse-B-Hinweis vorerst einfacher als volle Mechanik.

## Merkposten

- `hand_of_the_phaeron`: Die Extra-Nutzung von "My Will Be Done" könnte bereits über
  `Ability.ExtraUses` (siehe `ability.py`) verdrahtet sein (`grant_keyword` → PHAERON-Keyword
  → `ExtraUses.has_keyword`). **Verifizieren**, ob das tatsächlich zusammenspielt (grep nach
  `ExtraUses` + `phaeron` in `src/` und den Necron-YAMLs), bevor dieser Punkt als offen in einen
  neuen Plan-Step übernommen wird — könnte bereits erledigt sein.

---

## Vorgehen (Vorschlag für den nächsten Executor)

1. Schnellfix zuerst: `reconstitution_protocols` `amount` D3→D6 (kein Schema-Bedarf, isoliert).
2. Schema-Entscheidung mit Stakeholder: welche der Punkte (a.1)–(a.9) werden erweitert, welche
   bleiben bewusst Klasse B? (Nicht alle müssen in einem Rutsch — nach Aufwand/Nutzen sortieren,
   OR-Conditions (a.4) und Waffenart-Filter (a.5) sind die mit dem größten Hebel: sie betreffen
   4 bzw. 4 Stratagems.)
3. Je Schema-Erweiterung: Dataclass-Feld + `stratagem_visibility()`/Loader-Anpassung + Test,
   danach die betroffenen YAML-Einträge nachziehen.
4. `hand_of_the_phaeron`-Merkposten vorab klären (kann parallel/vorher passieren, kein
   Schema-Bedarf).

## Verifikation

- `pytest --tb=short` grün, Coverage ≥ 99 %.
- Jede Korrektur mit Zitat aus `docs/work/wahapedia_necrons/stratagems.txt` belegt.
- Manuelle UI-Verifikation für neue `event`-Werte, falls sie erstmals einen echten Konsumenten
  in der reaktiven Stratagem-UI (Plan 015) bekommen.
