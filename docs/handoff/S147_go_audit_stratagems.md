STATUS: ANSWERED (S147-Audit-Befundkatalog — behalten bis Fixing-Plan-Umsetzung S148)

# GO-Audit A — Stratagems (S147)

Reine Recherche, kein Code/Daten geändert. Scope: `data/wh40k_9e/_shared/stratagems.yaml`
(7), `data/wh40k_9e/necrons/stratagems.yaml` (40), `data/wh40k_9e/orks/stratagems.yaml` (17)
↔ `src/gameMechanic/stratagemEngine.py` + Konsumenten in `src/uiLayout/_common.py`,
`src/gameObjects/stratagem.py`, `src/gameObjects/loader.py`, `src/gameMechanic/chargePhase.py`
↔ `docs/work/wahapedia_core_rules/{core_rules,rules_appendix}.txt`.

## 1. Grundannahmen (bitte bestätigen)

1. **App würfelt nicht** — alle Würfe passieren am Tisch. Effekttypen wie `reroll`,
   `mortal_wounds`, `auto_wound`, `reanimate` (D3/D6-Heilung), `auto_explode` sind daher
   grundsätzlich **nicht** dadurch "kaputt", dass die App den Würfel nicht selbst wirft.
2. **Klasse-B/C-Zählregel:** Ein Stratagem zählt nur dann als Lücke, wenn (a) die App eine
   Auswertung verspricht, die sie nicht liefert, **und** (b) kein Tisch-Hinweis existiert.
   Der `rule_text` jedes Stratagems wird immer im GO-Expander angezeigt (verifiziert:
   `gameProtocoll.py` rendert `rule_text` für jede Karte) — das zählt als Tisch-Hinweis.
   Reine "wir tracken das nicht numerisch"-Fälle sind daher **keine** Lücke.
3. **Ausnahme von 2 (der eigentliche Hebel dieses Audits):** Sobald die Engine für **densel­ben
   Effekt-Typ** bei anderen Stratagems bereits automatisch rechnet (z. B. `buff_roll`/
   `debuff_roll`/`buff_stat` über den `modifier:`-Block in `active_modifiers`), ist das
   Klasse A, nicht B — ein Stratagem mit demselben `effect.type`, dem aber der `modifier:`-
   Block fehlt, ist dann eine echte, generische Inkonsistenz und zählt als Befund.
4. **Bedingungen:** `conditions:` ist rein Keyword-basiert (`stratagem_conditions_met`,
   `stratagem.py:87-103`) und die einzige automatisch geprüfte Bedingung außer Phase/CP/Used.
   Waffentyp, Reichweite, "nicht in Engagement Range" etc. werden **nirgends** geprüft —
   das ist laut Auftrag für Waffentyp ein Befund (Engine hat dafür keinerlei Mechanismus,
   obwohl viele `rule_text`e es verlangen), für reine Entfernungsangaben dagegen laut Regel 2
   keine Lücke (Tisch-Sache, Hinweis über `rule_text` vorhanden).
5. Custodes hat keine `stratagems.yaml` — bekannter W1-F-Befund, hier nicht erneut gemeldet.

## 2. Lücken-Tabelle

| Stratagem | Datei:Zeile | Befund-Typ | Klassifikation | Beleg |
|---|---|---|---|---|
| **Hand of the Phaeron** | `necrons/stratagems.yaml:46-48` (`effect: {type: grant_keyword, stat: phaeron}`) | Bug | **bestätigt (Kern), Mechanismus-Zuschreibung im Auftrag falsch** | `grant_keyword` hat in `stratagemEngine._apply_stratagem_effect` (`stratagemEngine.py:42-66`) **gar keinen Dispatch-Zweig** — die eigene Docstring zählt `grant_keyword` explizit zu den absichtlich am Tisch aufgelösten Effekten (`stratagemEngine.py:92-97`). `_apply_persistent_effect` (`loader.py:803-835`, `grant_keyword`-Zweig `loader.py:823-826`, erwartet `effect.get("keyword")`) wird **nur** aus `entry.get("persistent_effects", [])` erreicht (`loader.py:792`, `loader.py:1066` — Relic-/Wargear-Einträge), niemals aus `stratagems.yaml`. Der Feldname `stat` vs. `keyword` ist damit nicht die (einzige) Ursache — selbst mit korrektem Feldnamen würde der Stratagem-Effekt nicht ausgewertet, weil kein Aufrufpfad existiert. Fix braucht **zwei** Teile: neuen Dispatch-Zweig + Feldname vereinheitlichen. |
| **Fire Overwatch** | `_shared/stratagems.yaml:73-85` (`conditions: []`) | Bedingungslücke | bestätigt (weiterhin offen) | `chargePhase.py:154-177` (`_inactive_charge`) bietet die GO-Box für **jede** als Charge-Ziel erklärte Einheit an, ohne Fernkampfwaffen- oder Engagement-Range-Check. Regeltext `core_rules.txt:1906-1932`: Overwatch wird "resolved like a normal shooting attack" (braucht Fernkampfwaffe) **und** "A unit cannot fire Overwatch if there are any enemy units within Engagement Range of it" (`rules_appendix.txt:2319-2323`) — **zwei** fehlende Bedingungen, nicht nur die Waffentyp-Prüfung aus dem bekannten Befund. |
| **Techno-Oracular Targeting** | `necrons/stratagems.yaml:212-222` (`effect: {type: auto_wound}`) | YAML→Engine-Lücke | bestätigt | Kein `modifier:`-Block, keine Registrierung in `active_modifiers`; `_apply_stratagem_effect` hat keinen `auto_wound`-Zweig → Klick spendet CP/markiert "used", aber am Wirkort (Shoot-Sequenz) erscheint keinerlei Hinweis/Badge, dass "auto-wound" aktiv ist. |
| **Disintegration Capacitors** | `necrons/stratagems.yaml:252-263` (`effect: {type: auto_wound, modifier: 6}`) | YAML→Engine-Lücke + Bedingungslücke | bestätigt | Gleiche Lücke wie oben; zusätzlich beschränkt der Regeltext auf "gauss weapon"-Angriffe — kein Waffentyp-Check irgendwo (s. Grundannahme 4). |
| **Relentless Onslaught** | `necrons/stratagems.yaml:277-289` | YAML→Engine-Lücke | bestätigt, bereits bekannte Schuld | Kein `effect:`-Feld überhaupt (Kommentar `necrons/stratagems.yaml:285-288`: "intentionally unmodelled" → `docs/audit/plans/032-necron-stratagem-semantics.md`). Kein neuer Befund, hier nur bestätigt weiterhin offen. |
| **Solar Pulse** | `necrons/stratagems.yaml:305-316` (`effect: {type: restriction, stat: cover}`) | YAML→Engine-Lücke | bestätigt | `restriction` taucht in keinem Dispatch (`grep '"restriction"'` über `gameMechanic/*.py`, `uiLayout/*.py` → 0 Treffer) — Cover-Override wird nirgends verrechnet, kein Badge am Wirkort. |
| **Judgement of the Triarch** | `necrons/stratagems.yaml:344-356` (`effect: buff_roll, stat: hit, modifier: 1`, **kein** `modifier:`-Block) | YAML→Engine-Lücke (neu, generisch) | **neu** | Andere `buff_roll`-Stratagems (z. B. Methodical Destruction `necrons/stratagems.yaml:582-591`) tragen zusätzlich einen `modifier:`-Block, der über `spend_stratagem` (`_common.py:486-506`) in `active_modifiers` landet und von `_collect_atk_modifiers` (`_common.py:1321-1340`, nur `roll_type in ("hit","wound")`) gelesen wird. Judgement of the Triarch hat **nur** `effect:`, keinen `modifier:`-Block → der +1 Hit-Bonus wird nie tatsächlich auf die Trefferwurf-Anzeige angewendet, obwohl CP ausgegeben/"used" markiert wird. |
| **Eternal Protectors** | `necrons/stratagems.yaml:358-370` (`effect: buff_stat, stat: attacks, modifier: 1`, kein `modifier:`-Block) | YAML→Engine-Lücke (neu) | **neu** | `buff_stat`/`stat: attacks` wird nirgends aus `active_modifiers` gelesen (nur `buff_stat_bonus()` aus **Fraktions-Ability**-Effekten, `abilityEngine.py:481-491`, nicht aus Stratagem-`effect`/`modifier`) — die Attacks-Erhöhung hat aktuell keinerlei Zahleneffekt in der App. |
| **Blood Rites** | `necrons/stratagems.yaml:559-571` (`effect: buff_stat, stat: attacks, modifier: 1`, kein `modifier:`-Block) | YAML→Engine-Lücke (neu) | **neu** | Gleiche Lücke wie Eternal Protectors. |
| **Showin' Off** | `orks/stratagems.yaml:184-196` (`effect: buff_roll, stat: hit, modifier: 1`, kein `modifier:`-Block) | YAML→Engine-Lücke (neu) + Bedingungslücke | **neu** | Gleiche Lücke wie Judgement of the Triarch; zusätzlich nur für "Dakka weapon"-Angriffe gedacht — kein Waffentyp-Check. |
| **Unbridled Carnage** | `orks/stratagems.yaml:257-269` (`effect: buff_roll, stat: hit, modifier: 1`, kein `modifier:`-Block) | YAML→Engine-Lücke (neu) + Bedingungslücke | **neu** | Gleiche Lücke; zusätzlich an "No Mukkin' About Clan Kultur" gebunden (Sub-Bedingung jenseits reiner Keywords), nicht geprüft. |
| **Hit 'Em Harder** | `orks/stratagems.yaml:111-129` (`modifier: {roll_type: damage, value: 1}`) | totes Engine-Feature (neu) | **neu** | `modifier:`-Block ist vorhanden und wird korrekt in `active_modifiers` registriert (`spend_stratagem`, `_common.py:486-506`) — sieht "verdrahtet" aus. Aber **kein** Konsument liest `roll_type == "damage"` zurück: `_render_damage_block` (`_common.py:1531-1601`) zeigt `profile.damage` direkt an, ohne je `active_modifiers` abzufragen (`grep 'roll_type' src/` → nur `hit`, `wound`, `save`, `invuln_save`, `strength` werden je gelesen). Der +1 Damage wird also niemals angewendet, obwohl CP ausgegeben wird — Pendant zum Hand-of-the-Phaeron-Muster, aber auf der Modifier- statt der Effect-Seite. `StratagemModifier`s Docstring (`stratagem.py:30`) listet `damage` (und `fnp`, `charge`) explizit als gültige `roll_type`-Werte — das Schema verspricht mehr, als die Engine einlöst. |
| **Wreckaz** | `orks/stratagems.yaml:211-230` (`modifier: {roll_type: wound, value: 1, target: attacker}`) | Bedingungslücke | **neu** | Regeltext gilt nur "when a model ... makes an attack that targets a VEHICLE" — `_collect_atk_modifiers` (`_common.py:1321-1340`) wendet den Bonus auf **jeden** Angriff der Einheit an, ohne Ziel-Keyword-Check (kein Mechanismus für "Ziel hat Keyword VEHICLE" existiert in der Modifier-Pipeline). Zu großzügig verrechnet, sobald verdrahtet. |
| **Tough as Squig-Hide** | `orks/stratagems.yaml:161-180` (`modifier: {roll_type: wound, value: -1, target: defender}`) | Semantik-Hinweis (kein hartes Bug, niedrige Priorität) | **neu, informativ** | Regeltext: "an unmodified wound roll of 1, 2 or 3 ... fails, irrespective of any abilities" (Auto-Fail-Schwelle), umgesetzt als pauschaler −1-Wound-Modifier. Für ungetunte Würfe ähnlich, bei zusätzlichen +/− Wound-Modifiern anderer Quellen mathematisch **nicht** äquivalent (ein −1-Malus lässt sich durch +1 von anderswo neutralisieren, ein "unmodified 1-3 failed" nicht). Kein Fix-Auftrag nötig, nur zur Kenntnis für künftige Semantik-Reviews. |
| **Reanimation Prioritisation** / **Resurrection Protocols** | `necrons/stratagems.yaml:291-303`, `:438-451` (`effect: {type: reanimate}`) | YAML→Engine-Lücke (neu, gruppiert) | **neu** | `effect.type == "reanimate"` wird nur für **Fraktions-Abilities** ausgewertet (`abilityEngine.py:413`, `armyCard.py:109`), nie für `Stratagem.effect` — `stratagemEngine._apply_stratagem_effect` hat keinen `reanimate`-Zweig. Nach Grundannahme 2 wäre das an sich Klasse B (App würfelt nicht) — die eigentliche Reanimations-**Anzahl**-Buchführung (wie viele Modelle zurückkommen) ist aber bei der Ability-Variante bereits Teil der App-Logik, bei der Stratagem-Variante nicht — Inkonsistenz innerhalb derselben Mechanik, daher als Befund gelistet statt stillschweigend übergangen. |
| **Curse of the Phaeron, Careen!** (variable CP: 1/3 bzw. 1/2 je TITANIC/WAGON) | `necrons/stratagems.yaml:468-480`, `orks/stratagems.yaml:56-69` | Bedingungslücke (niedrige Prio) | **neu, informativ** | Variabler CP-Preis je Keyword (`TITANIC`/`WAGON`) steht nur im `rule_text`, `cp_cost` ist fix auf den Normalfall gesetzt — App zieht immer den niedrigeren Betrag ab, auch wenn die Einheit TITANIC/WAGON ist. Keyword-basiert prüfbar (Stakeholder-Präferenz), aber kein Mechanismus für variable `cp_cost` vorhanden. Gehört eher zu einem generischen "variable CP"-Feature als zu diesem Audit — nur als Fund notiert. |

### (b) Engine→YAML: tote Engine-Effekttypen

- Die drei tatsächlich dispatchten `effect.type`-Werte in `stratagemEngine._apply_stratagem_effect`
  (`auto_pass_morale`, `move`+`handler:fall_back_through_models`, `invuln_save`) werden alle von
  mindestens einem YAML-Eintrag genutzt (Insane Bravery, Desperate Breakout, Quantum Deflection) —
  **kein** totes Feature auf dieser Ebene.
- `StratagemModifier.roll_type` (`stratagem.py:30`, Docstring-Aufzählung `hit | wound | save | fnp |
  charge | damage`) deklariert **6** gültige Werte; tatsächlich gelesen werden nur `hit`, `wound`,
  `save` (generisch über `_collect_atk_modifiers`/`_collect_def_save_modifiers`) sowie `invuln_save`
  (eigener Pfad) und `strength` (eigener Pfad `stratagem_strength_bonus`, nicht in der Docstring-Liste
  erwähnt!). **`fnp` und `charge` werden von keinem YAML-Eintrag verwendet und von keinem Code-Pfad
  gelesen** — doppelt totes Feld (Schema verspricht es, niemand nutzt/konsumiert es). `damage` wird
  von einem Eintrag (Hit 'Em Harder) verwendet, aber nicht konsumiert (s. Tabelle oben).
- `Stratagem.detachment` (`stratagem.py:67`) wird von **keinem** der 64 Einträge im Scope gesetzt
  (0 Treffer) — Feld existiert, aktuell ungenutzt auf Datenseite.

## 3. snake_case-Feld-Inventar (Migrationsgrundlage)

Gezählt über alle drei Scope-Dateien (`grep -oE '^\s*[a-z_]+:'`), 64 Stratagems gesamt
(7 shared + 40 Necrons + 17 Orks):

| Feld | Fundstellen gesamt | Ebene | Hinweis |
|---|---|---|---|
| `name_en`, `cp_cost`, `phase`, `stage`, `player`, `conditions`, `once_per_phase`, `rule_text` | 64 je | top-level | Pflichtfelder, auf jedem Eintrag |
| `id` | 64 | top-level | Dotted-Namespace-Identifier, kein Kandidat für camelCase-Rename (ist kein Feldname i.e.S.) |
| `effect` | 61 | top-level (Mapping) | 3 Einträge ohne `effect` (disruption_fields, relentless_onslaught, fractal_targeting — bewusst unmodelliert) |
| `type` (unter `effect`) | 61 | effect-sub | |
| `stat` (unter `effect`) | 25 | effect-sub | z. B. `stat: phaeron`, `stat: hit`, `stat: attacks` |
| `amount` (unter `effect`) | 4 | effect-sub | |
| `target` (unter `effect` **und** unter `modifier`) | 10 | doppelt genutzt | **Namenskollision**: gleicher Key in zwei verschiedenen Blöcken mit leicht unterschiedlicher Bedeutung (effect.target: wer wird beeinflusst grob; modifier.target: attacker/defender/any für die Roll-Pipeline) |
| `modifier` (top-level Block, StratagemModifier) **und** `modifier` (Sub-Feld unter `effect`, int-Wert) | 20 (13 Necrons + 7 Orks) | **überladen** | **Wichtigster Migrationsbefund:** derselbe YAML-Key `modifier` wird für zwei völlig verschiedene Dinge verwendet — als int-Leaf unter `effect:` (z. B. `effect.modifier: 6` bei Disintegration Capacitors) UND als eigener Mapping-Block auf Top-Level (`modifier: {roll_type, value, target, expires_at, source_label}`). Klare Rename-Kandidaten fürs camelCase-Schema: z. B. `effect.modifier` → `effectModifierValue`, Top-Level-Block → `attackModifier`. |
| `roll_type`, `value`, `expires_at`, `source_label` (unter `modifier`-Block) | je 7 (4 Necrons + 3 Orks) | modifier-sub | Kandidaten: `rollType`, `value` (unverändert ok), `expiresAt`, `sourceLabel` |
| `once_per_battle` | 6 (1+3+2) | top-level | Kandidat: `oncePerBattle` |
| `timing` | 17 (6+8+3) | top-level | Kandidat: `timing` (unverändert, schon ein Wort) |
| `event` | 16 (5+8+3) | top-level | unverändert |
| `handler` (unter `effect`) | 1 | effect-sub | nur `fall_back_through_models` |
| `detachment` | 0 | top-level | im Dataclass vorhanden, in keinem Scope-Eintrag gesetzt |

**Empfehlung fürs Migrationsschema:** Die `target`- und `modifier`-Kollisionen zuerst auflösen
(Feld einmal umbenennen, bevor camelCase-Rename automatisiert läuft) — sonst überträgt ein
naives Such-&-Ersetzen die Mehrdeutigkeit 1:1 ins neue Schema.

## 4. Fixing-Plan-Vorschlag für S148 (je ≤ Effort M)

1. **[M] Hand of the Phaeron — Dispatch + Feldname.** Neuen `grant_keyword`-Zweig in
   `stratagemEngine._apply_stratagem_effect` ergänzen (analog zum bestehenden
   `loader._apply_persistent_effect`-Muster: Keyword auf die Ziel-Einheit im
   `session_state`-Unit-Snapshot anwenden — **nicht** über `loader.py`, da Stratagems keine
   `persistent_effects`-Liste haben). YAML-Feld `stat: phaeron` → `keyword: phaeron`
   vereinheitlichen (einziger Vorkommen). Test: Stratagem aktivieren → Ziel-Unit trägt
   PHAERON-Keyword bis Ende Kampagne/Battle (`once_per_battle`). Betrifft nur
   `necrons/stratagems.yaml`, `stratagemEngine.py`.
2. **[S] Fehlende `modifier:`-Blöcke ergänzen (generisch, 5 Stratagems).** Judgement of the
   Triarch, Eternal Protectors, Blood Rites, Showin' Off, Unbridled Carnage bekommen je einen
   `modifier:`-Block nach demselben Muster wie Methodical Destruction/Wreckaz (roll_type
   passend zu `effect.stat`: `hit` bei den ersten/letzten beiden, `attacks` bei den mittleren
   zwei — **Achtung:** `attacks` wird von der Modifier-Pipeline aktuell **nicht** gelesen,
   siehe Punkt 4 unten; für Eternal Protectors/Blood Rites also erst Punkt 4 lösen, sonst
   bleibt der `modifier:`-Block wirkungslos). Reiner Datenfix + Regressionstest je Stratagem
   (Angriffssequenz zeigt den Bonus in der Hit-Modifier-Liste).
3. **[M] Generisches Bedingungs-Modell: Waffentyp als datengetriebene Bedingung.**
   `conditions:` in `stratagem.py`/`stratagemEngine.py` um eine optionale Weapon-Type-Prüfung
   erweitern — **keyword-basiert** (Stakeholder-Präferenz): neues optionales YAML-Feld
   `weapon_conditions: [KEYWORD, ...]` (analog `conditions`, aber gegen `Weapon.keywords`/
   `WeaponProfile` geprüft statt gegen `Unit.keywords`), generische Prüf-Funktion
   `weapon_conditions_met(weapon, conditions)` in `stratagem.py` neben
   `stratagem_conditions_met`. Erste Verdrahtung an **einem** Fall (Fire Overwatch: Unit
   braucht mindestens eine Fernkampfwaffe) statt an allen gleichzeitig — Rest folgt danach
   als eigene kleine Aufgaben, um Effort ≤ M zu halten. Kein Fraktions-String in `src/`.
4. **[S] Fire Overwatch — zweite fehlende Bedingung.** `_inactive_charge` (`chargePhase.py`)
   um einen Engagement-Range-Check der reagierenden Einheit erweitern (`unit_state.get(
   "in_melee")` — dieselbe Quelle, die `_effect_gate_met` für Desperate Breakout schon nutzt)
   — wenn die Einheit selbst in Engagement Range ist, GO-Box nicht anbieten. Regressionstest
   in `tests/gameMechanic/test_charge_phase.py` (Datei ggf. anlegen, falls nicht vorhanden —
   kurz prüfen).
5. **[S] `damage`-Roll-Type verdrahten oder Hit 'Em Harder korrigieren.** Entscheidung nötig
   (NEEDS-DECISION oder pragmatisch: kleinerer Fix zuerst): entweder `_render_damage_block`
   um eine `active_modifiers`-Abfrage (`roll_type == "damage"`) ergänzen (gleiche Struktur wie
   `_collect_atk_modifiers`), oder — falls Damage-Boni bewusst außerhalb des App-Scopes bleiben
   sollen (Klasse B) — den `modifier:`-Block bei Hit 'Em Harder entfernen und stattdessen nur
   auf `rule_text` verlassen, dazu `fnp`/`charge`/`damage` aus der `StratagemModifier`-Docstring
   streichen, wenn die Entscheidung "nicht modelliert" lautet. **Empfehlung:** verdrahten, da
   die Infrastruktur (active_modifiers, Save-Block-Vorbild) bereits für andere roll_types
   existiert — konsistenter als eine Ausnahme.
6. **[S] Wreckaz — Ziel-Typ-Prüfung (VEHICLE).** Kleinster Fall für ein generisches
   "Ziel hat Keyword X"-Feld in `modifier:` (`target_conditions: [VEHICLE]`), geprüft in
   `_collect_atk_modifiers` gegen die Ziel-Unit (`def_uid` liegt dort bereits vor). Guter
   zweiter Kandidat, um das generische Muster aus Punkt 3 zu verproben, bevor es auf alle
   Waffentyp-Fälle ausgerollt wird.
7. **[XS] Reanimation Prioritisation / Resurrection Protocols — Konsistenz-Entscheidung.**
   Nur NEEDS-DECISION-Klärung, kein Code: soll die App künftig auch Stratagem-`reanimate`
   mitzählen (dann eigener Ticket-Schnitt nötig, vermutlich M/L wegen Modell-Auswahl-UI) oder
   bleibt es bewusst Tischsache (dann Docstring/Kommentar ergänzen, warum die Ability-Variante
   anders behandelt wird als die Stratagem-Variante — sonst wirkt es beim nächsten Audit wieder
   wie eine Lücke).

Reihenfolge-Empfehlung: 1 und 2 zuerst (kleinster, klarster Nutzen), 3+4 zusammen (bauen
aufeinander auf), 5+6 danach, 7 ist reine Klärung und kann jederzeit dazwischengeschoben werden.

## 5. Bestandsaufnahme-Nachweis

- `ls data/wh40k_9e/necrons/` → 12 Dateien, genau eine `stratagems.yaml` (keine
  Alternativ-/Zusatzdatei mit Stratagem-Daten).
- `ls data/wh40k_9e/orks/` → 12 Dateien, genau eine `stratagems.yaml`.
- `ls data/wh40k_9e/_shared/` → 4 Dateien, genau eine `stratagems.yaml`.
- `ls data/wh40k_9e/adeptus_custodes/` → 3 Dateien (`faction_abilities.yaml`,
  `placeholder.relics.yaml`, `placeholder.warlord_traits.yaml`), **keine**
  `stratagems.yaml` — bestätigt den bekannten W1-F-Befund, hier nicht als neue Lücke gezählt.
- `find src -iname "*stratagem*"` → genau `gameObjects/stratagem.py` und
  `gameMechanic/stratagemEngine.py` als Produktivcode (plus `.pyc`-Caches).
- Konsumenten außerhalb dieser zwei Dateien identifiziert via `grep -rn "effect.type\|
  \.modifier\b\|active_modifiers" src/`: `uiLayout/_common.py` (spend/undo/collect-Pfade),
  `gameObjects/loader.py` (`_apply_persistent_effect`, nicht stratagem-erreichbar),
  `gameMechanic/chargePhase.py` (Fire-Overwatch-Reaktivfenster).
- `docs/audit/plans/032-necron-stratagem-semantics.md` als bereits bekannte Schuld für
  Fractal Targeting/Relentless Onslaught/Whirling-Onslaught-OR-Bedingung/Resurrection-
  Protocols-OR-Bedingung identifiziert (Kommentare in `necrons/stratagems.yaml` verweisen
  direkt darauf) — hier nicht erneut als "neu" gezählt, nur in der Tabelle als bestätigt
  markiert wo im Scope relevant.

---

**Kernbefunde für den Koordinator (siehe auch Rückgabe-Text):** 4 bereits bekannte YAML→Engine-
Lücken bestätigt (Techno-Oracular Targeting, Disintegration Capacitors, Solar Pulse — offen;
Relentless Onslaught — bereits als Plan-032-Schuld bekannt), Hand-of-the-Phaeron-Bug bestätigt
aber mit korrigierter Ursache (kein Dispatch-Zweig, nicht nur Feldname), 5 neue YAML→Engine-
Lücken bei `buff_roll`/`buff_stat` ohne `modifier:`-Block, 1 neues totes Engine-Feature
(`roll_type: damage` wird registriert, aber nie gelesen — u.a. `fnp`/`charge` komplett unbenutzt),
2 neue Bedingungslücken (Fire Overwatch fehlt zusätzlich der Engagement-Range-Check; Wreckaz
wendet seinen Bonus auf jeden Angriff statt nur gegen VEHICLE an), plus ein überladenes
`modifier`-Feld (zwei Bedeutungen) als größter Einzelbefund fürs camelCase-Migrationsschema.
