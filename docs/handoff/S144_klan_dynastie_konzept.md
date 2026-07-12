STATUS: NEEDS-DECISION

# S144 — Konzept: Ork Klan Kulturs + Necron Dynastic Codes als Subfraktions-Passiv

**Auftrag:** S144-Plan Aufgabe 7 (Ziel 7, Stufe C-Umfeld). Recherche + Konzept — kein Code,
keine YAML-Änderung.

---

## 0. Kern-Befund vor allem anderen: Die Prämisse des Auftrags stimmt nur teilweise

Der Auftrag ging davon aus, dass die **Rohtexte der 7 Klan-Kulturs und 6 Dynastic Codes lokal
fehlen** und komplett neu recherchiert werden müssen. Das ist **falsch** — mit einer wichtigen
Einschränkung:

- `data/wh40k_9e/orks/subfaction_abilities.yaml` und
  `data/wh40k_9e/necrons/subfaction_abilities.yaml` existieren bereits **seit 2026-06-03**,
  enthalten alle 7 Klans bzw. 6 Dynastien, mit `rule_text`, `ability_type: triggered`,
  `source: subfaction_rule` / `source: dynastic_code`, generisch geladen über
  `load_subfaction_abilities()` (`src/gameObjects/loader.py:605`).
- Diese Daten sind sogar bereits **in die Engine eingehängt**:
  `abilityEngine.get_triggered_abilities()` (`src/gameMechanic/abilityEngine.py:512–543`)
  liest sie per `all_abilities.extend(load_subfaction_abilities(faction_dir))` mit ein.
- **Aber:** Beim Wortlaut-Abgleich mit Wahapedia (WebFetch, s. §2) zeigt sich, dass **4 von 6
  Necron-Dynastic-Codes inhaltlich falsch oder stark unvollständig** sind (Nihilakh, Sautekh,
  Mephrit, Nephrekh), 1 von 7 Ork-Kulturs eine fehlende Ausnahmeklausel hat (Snakebites), und
  dass **kein einziger** der 13 Einträge aktuell im Spiel sichtbar/wirksam wird — trotz Laden
  in `all_abilities`. Details zu „warum unsichtbar" in §3.

**Der tatsächliche Auftrag für S144+ ist also dreiteilig, nicht nur „Konzept für Neues":**

1. **Daten-Korrektur** an 5 von 13 bestehenden Einträgen (Wortlaut-Fehler, s. §2) —
   das ist kein neues Feature, sondern ein Bugfix an vorhandener, aber falscher Datenlage.
2. **Engine-Lücke** schließen: die Einträge werden geladen, aber nie mit passendem
   `timing`/`phase` abgefragt und nie gegen die tatsächliche Klan-/Dynastie-Wahl des Rosters
   gefiltert (s. §3) — jede Klan-/Dynastie-Fähigkeit gilt aktuell für **jede** Einheit der
   Fraktion, sobald sie triggerbar wäre (ist sie aber mangels Query-Pfad nicht).
3. **UI-Sichtbarkeit** — kein Konsument rendert diese Fähigkeiten irgendwo.

Diese Korrektur ist der wichtigste Teil dieses Konzepts. Bitte als **Grundannahme 0**
bestätigen, bevor der Rest gelesen wird — er baut darauf auf.

---

## 1. Grundannahmen (bestätigungspflichtig)

1. **App würfelt nicht.** Wie bei jeder Regel-Umsetzung in Arbiter: die App zeigt Schwellwerte/
   Modifikatoren an und lässt den Spieler am Tisch würfeln; keine Zufallszahlengeneratoren für
   Spielwürfe.
2. **Scope ist ausschließlich die fixe Subfraktions-Wahl** (Klan bei Rosteranlage / Dynastie bei
   Rosteranlage), **nicht** die pro-Runde rotierenden Command Protocols/Ka'tahs. Diese beiden
   Mechaniken sind unabhängig voneinander aktiv (s. §4 Abgrenzung) — eine Necron-Armee hat
   **gleichzeitig** einen fixen Dynastic Code (dieses Konzept) und wählt **zusätzlich** pro
   Runde ein Command Protocol (`round_choice`, bereits gebaut).
3. **Bestehende Datei-Struktur wird wiederverwendet**, nicht neu angelegt:
   `data/wh40k_9e/<faction>/subfaction_abilities.yaml` ist bereits der korrekte Ort
   (`subfaction_field`/`subfaction_label` in `faction_abilities.yaml` verweisen bereits
   darauf, `load_subfaction_meta()` bindet `clan`/`dynasty` generisch ans Roster-Feld).
4. **Die 5 identifizierten Wortlaut-Fehler (§2) sind ein separater Befund**, keine
   Interpretationssache — sie werden hier nur dokumentiert, nicht in diesem Schritt behoben
   (Auftrag: kein Code/YAML). Korrektur wäre ein eigener, kleiner Executor-Auftrag.
5. **Nihilakhs exakter Sekundäreffekt bleibt als offene Frage** stehen (widersprüchliche
   Quellen, s. §2) — wird **nicht** hier entschieden.
6. **Klasse-A/B/C-Einordnung (§5) folgt der bestehenden Systematik** aus
   `docs/spec/acceptance/rules.md` — keine neue Klassifikation erfunden.
7. **Kein Fraktionsname in `src/`.** Jeder Vorschlag in §6 ist so gehalten, dass Necrons/Orks
   nur über YAML-Daten unterschieden werden (Generic-src-Invariante).

---

## 2. Wortlaut-Tabelle — Soll (Wahapedia 9E) vs. Ist (lokale YAML)

Quelle: WebFetch `https://wahapedia.ru/wh40k9ed/factions/orks/` und
`https://wahapedia.ru/wh40k9ed/factions/necrons/` (S144, 2026-07-12), Necron-Nihilakh/Sautekh
zusätzlich per WebSearch gegengeprüft (Ergebnisse teils widersprüchlich, s. Anmerkung).

### 2a. Ork Klan Kulturs (7)

| Klan | Wahapedia-Name | Soll (Kurzfassung) | Ist (`subfaction_abilities.yaml`) | Delta |
|---|---|---|---|---|
| Bad Moons | Armed to da Teef | +6" Range auf Dakka/Heavy; ungemod. Wound-6 im Fernkampf → AP+1 | identisch | keins |
| Blood Axes | Taktiks | Light Cover wenn Angreifer >18" weg; nach Fall Back: schießen ODER chargen (nicht beides) | identisch | keins |
| Deathskulls | Lucky Blue Gitz | 1 Reroll (Hit oder Wound) pro Aktivierung; Mortal Wound auf 5+ negiert; INFANTRY → ObjSec | identisch | keins |
| Evil Sunz | Red Ones Go Fasta | +1" Move (+2" bei SPEED FREEKS); +1 Advance; kein Assault-Malus nach Advance | identisch | keins |
| Freebooterz | Competitive Streak | Nach Vernichtung eines Gegners: +1 Hit für andere FREEBOOTERZ bis Phasenende | identisch | keins |
| Goffs | No Mukkin' About | Ungemod. Hit-6 im Nahkampf = 1 Extra-Hit; +1 Strength nach Charge/HI | identisch (Ist bindet die Strength-Klausel enger an „Pile-in/Consolidate", Soll an „Angriff generell" — kleine Präzisierungsdifferenz, kein Fehler) | gering |
| Snakebites | Da Old Ways | Ungemod. Wound-Wurf 1–3 scheitert immer, **außer die Attacke hat Stärke 8+** | Ist: „Wound 1–3 scheitert immer" — **ohne die S8+-Ausnahme** | **Fehler: Ausnahmeklausel fehlt** |

### 2b. Necron Dynastic Codes (6)

| Dynastie | Wahapedia-Name | Soll (Kurzfassung) | Ist (`subfaction_abilities.yaml`) | Delta |
|---|---|---|---|---|
| Szarekhan | Uncanny Artificers | Mortal-Wound-Verlust auf 5+ negiert; 1 Wound-Reroll pro Aktivierung; „beide Direktiven"-Klausel bei reinem Dynastie-Heer | identisch (bereits in einer früheren Session korrigiert, s. Kommentar in der YAML) | keins |
| Novokh | Awakened by Murder | +1 Charge-Wurf; bei Charge/Charged/HI: **AP+1** im Nahkampf | Ist: „Savage Hunters", +1 Charge-Wurf, aber **+1 Hit-Wurf statt AP+1** | **Fehler: falscher Effekt-Typ (Hit statt AP)** |
| Nephrekh | Translocation Beams | 6+ Invuln; **zusätzlich** Advance kann durch „Translokation" ersetzt werden (kein Advance-Wurf, +6" Move, danach Schießverbot bis Rundenende); Fall Back/Translokation ignoriert Modelle/Terrain für Bewegung | Ist: **nur** die 6+ Invuln-Zeile — Translokations-Mechanik komplett fehlend | **Fehler: Kernmechanik fehlt (nur Teilzitat)** |
| Sautekh | Relentless Advance | Morale-Reroll; Rapid-Fire-Waffen verdoppeln Attacken auf ≤18"; (laut Zweitquelle zusätzlich: nach Advance werden Waffen wie Assault behandelt) | Ist: „Relentless Expansionists" — +3" Advance-Wurf, Assault-Waffen bei Advance als „stationär" behandelt | **Fehler: komplett andere Fähigkeit/anderer Name** |
| Nihilakh | Aggressively Territorial | Objective Secured (bzw. +1 Modell-Zählung wenn bereits vorhanden); **Sekundärklausel widersprüchlich belegt** — Quelle 1 (WebFetch): AP-(-1)-Angriffe werden zu AP-0 im eigenen Deployment Zone; Quelle 2 (WebSearch): Hit-Reroll von 1 beim Schießen, wenn die Einheit sich nicht bewegt hat | Ist: „Acquisitive Grasp" — Einheit darf nicht Fall Back solange sie in Reichweite eines eigenen Objective Markers ist | **Fehler: komplett andere Fähigkeit/anderer Name; Sekundärklausel selbst zwischen Zweitquellen uneinheitlich → offene Frage, s. Entscheidungsfrage 1** |
| Mephrit | Solar Fury | +3" Range auf Fernkampfwaffen (außer Pistols); ungemod. Wound-6 auf halbe Reichweite → AP+1; „beide Direktiven"-Klausel | Ist: „Talent for Annihilation" — nur die AP+1-auf-halbe-Reichweite-Zeile, **Range-Bonus fehlt**, falscher Name | **Fehler: Name falsch + Range-Bonus fehlt** |

**Einordnung:** 1 von 7 Ork-Einträgen und 4 von 6 Necron-Einträgen weichen vom 9E-Wortlaut ab.
Die „beide Direktiven bei reinem Dynastie-Heer"-Klausel, die bei **allen 6** Necron-Codes im
Originaltext steht, ist inhaltlich bereits durch den bestehenden `subfaction_affinity`-
Mechanismus (Kategorie 1, `round_choice`) abgedeckt — dort aber an „aktiv gewählte Dynastie"
geknüpft, nicht wortwörtlich an „jede Einheit im Heer trägt den Code" (Unterschied nur bei
Bündnis-/Mehrdynastie-Listen relevant, kein Fix nötig für Standard-Mono-Dynastie-Rosters).

**Doku-Drift-Nebenbefund:** `docs/spec/faction_abilities.md` Kategorie 6 („Passive/Persistent")
behauptet „Größtenteils abgedeckt durch `triggered`-Abilities in `faction_abilities.yaml`" —
das ist falsch/veraltet: Klan-Kulturs/Dynastic Codes liegen in `subfaction_abilities.yaml`
(anderer Datei-Scope, s. Datei-Scope-Tabelle oben in derselben Spec) und sind, wie in §3 gezeigt,
nicht wirksam. Spec-Nachzug empfohlen, sobald dieses Konzept umgesetzt ist.

---

## 3. Warum die 13 Einträge trotz Laden aktuell unsichtbar bleiben

Drei unabhängige Lücken, alle in `src/gameMechanic/abilityEngine.py`:

1. **Kein Subfraktions-Filter.** `check_conditions()` (Zeile 49–66) kennt `has_rules`,
   `has_keywords`, `unit_not_destroyed`, `needs_healing` — aber **keine** Prüfung „gehört diese
   Fähigkeit zur Klan-/Dynastie-Wahl dieses Rosters?". Da die meisten Einträge `conditions: []`
   haben, würden sie — sobald sie überhaupt abgefragt würden — für **jede** Einheit der Fraktion
   gelten, unabhängig vom gewählten `clan`/`dynasty`-Feld im Roster. `klan_keyword` in
   `orks/subfaction_abilities.yaml` (z. B. `BAD MOONS`) wird nirgends in `src/` gelesen
   (verifiziert per `grep -rn klan_keyword src/`).
2. **Kein passender Abfrage-Pfad.** `get_triggered_abilities()` ist die einzige Funktion, die
   `load_subfaction_abilities()` einliest — aber ihr einziger Aufrufer
   (`commandPhase.py:31`) fragt fest `phase="command", timing="phase_start"` ab. Die
   Subfraktions-Einträge haben fast durchgehend `timing: persistent, phase: any` (oder
   `shooting`/`fight`/`movement`) — das matcht `check_trigger()` (Zeile 37–46) nie mit
   `timing="phase_start"`. Damit landen die 13 Einträge in `all_abilities`, aber der
   Trigger-Check verwirft sie in jedem tatsächlichen Aufruf.
3. **4 von 6 Necron-Effekte zeigen auf einen nicht existierenden Handler.** `effect.type: complex`
   + `handler: novokhSavageHunters` / `sautekh_advance` / `uncannyArtificersMortal` /
   `uncannyArtificersReroll` — das `.handler`-Dispatch-Muster existiert im gesamten `src/`-Baum
   nur für `effect.handler == "fall_back_through_models"` (`stratagemEngine.py`). Diese vier
   Necron-Handler sind unverdrahtete Verweise auf nichts.
4. **Kein UI-Konsument.** Keine Datei unter `src/uiLayout/` referenziert
   `load_subfaction_abilities` oder `klan_keyword` — es gibt keine Karte/Badge/Sektion, die
   diese Fähigkeiten überhaupt anzeigen würde, selbst wenn Punkt 1–3 gelöst wären.

**Fazit:** Das ist kein Wortlaut-Problem allein — die Engine-Verdrahtung fehlt komplett. Das
erklärt auch die S143-Stakeholder-Beobachtung „Klan-Fähigkeiten fehlen als Feature" — subjektiv
korrekt beobachtet, auch wenn die Daten formal vorhanden sind.

---

## 4. Abgrenzung zum bestehenden `subfaction_affinity`-Schema (Command Protocols)

| | `subfaction_affinity` (bestehend, `round_choice`) | Klan Kultur / Dynastic Code (dieses Konzept) |
|---|---|---|
| Datei | `faction_abilities.yaml`, Feld auf einer `round_choice`-Direktive | `subfaction_abilities.yaml`, eigener Eintrag pro Subfraktion |
| Aktivierung | Spielerwahl pro Runde (1 von 6 Protokollen); Affinität schaltet **beide** Direktiven gleichzeitig frei, wenn die Wahl zur Subfraktion passt | **Immer aktiv**, sobald das Roster diese Klan-/Dynastie-Wahl trägt — kein Aktivierungsschritt, kein Verbrauch |
| Reichweite der Wirkung | Nur während das Protokoll aktiv/gewählt ist (rundenbegrenzt) | Permanent ab Listenerstellung, ganze Partie |
| Session-State | `active_protocol_id`, `active_directive`, `round_choice_assignments` | **Keiner nötig** — reiner Ableitungswert aus `roster.clan`/`roster.dynasty`, kein Verbrauchs-Tracking |
| Engine-Funktion | `get_active_round_choice_modifier()` u. a. (bereits gebaut) | **Fehlt** — Gegenstand dieses Konzepts |
| Wiederverwendbar? | `subfaction_value_for(player)` (`gameState.py:180`) — liest das Roster-Feld — **ja, direkt wiederverwendbar** für den neuen Filter | — |

**Wichtig:** Diese beiden Mechaniken sind **additiv**, nicht alternativ. Ein Necron-Roster mit
`dynasty: sautekh` hat (a) den Sautekh-Dynastic-Code permanent aktiv **und** (b) kann in der
Command-Phase weiterhin jedes der 6 Command Protocols wählen — nur bei Wahl von „Protocol of the
Conquering Tyrant" (Sautekhs zugeordnetes Protokoll) schaltet zusätzlich die
Affinitäts-Bonus-Regel („beide Direktiven") frei. Ein Missverständnis hier wäre der klassische
Scope-Fehler à la „Necron-Check entfernen ≠ für alle öffnen" (`feedback_ask_before_assuming_scope`,
User-Memory) — deshalb explizit als eigene Zeile in der Tabelle.

---

## 5. Datenschema-Vorschlag

### 5a. Entscheidung: bestehenden `ability_type: triggered` reparieren vs. neuen Typ einführen

Zwei Optionen, beide generisch (kein Fraktionsname in `src/`):

**Option A — bestehenden `ability_type: triggered` beibehalten, nur Engine-Lücken schließen.**
Kleinster Diff: `check_conditions()` bekommt ein neues, optionales `Condition`-Feld
(`subfaction_id: str | None`), das gegen `subfaction_value_for(player)` geprüft wird — nur
wenn gesetzt. Ein neuer Query-Pfad `get_active_subfaction_passives(faction_dir, player)` (analog
`get_active_round_choice_modifier`) fragt mit `timing="persistent"` statt nur
`command`/`phase_start` ab. Die 4 `complex`-Handler brauchen trotzdem echte Dispatch-Fälle.

**Option B — neuer `ability_type: subfaction_passive`.** Semantisch sauberer: trennt „reaktive,
event-getriggerte Fähigkeit" (`triggered`, z. B. Living Metal) von „dauerhaft aktiver Passiv-
Bonus, gebunden an eine feste Listenwahl" (neue Kategorie, deckt sich mit der bereits in
`docs/spec/faction_abilities.md` vordefinierten, aber leeren **Kategorie 6 — Passive/Persistent**).
Eigener Loader-Filter, eigene Engine-Funktion, kein Risiko einer Verwechslung mit reaktiven
`triggered`-Abilities in `unit_abilities.yaml`/`faction_abilities.yaml` (die über
`get_triggered_abilities` per Ereignis abgefragt werden). Erfordert einen Migrationsschritt:
13 bestehende Einträge von `ability_type: triggered` auf `subfaction_passive` umstellen (reiner
Feldwert-Change, keine Struktur-Änderung).

→ **Empfehlung (nicht Freigabe-relevant, nur Vorschlag):** Option B — sie deckt sich mit der
bereits dokumentierten, aber bislang leeren Kategorie 6 und vermeidet, dass künftige
`triggered`-Abfragen (z. B. neue reaktive Fähigkeiten) versehentlich Subfraktions-Passiv-Einträge
mit einsammeln. Entscheidung liegt beim Stakeholder (Entscheidungsfrage 3).

### 5b. Beispiel-YAML (Option B, generisch)

```yaml
# data/wh40k_9e/orks/subfaction_abilities.yaml — Auszug, 1 Klan
subfactions:
  - id: bad_moons
    name_en: Bad Moons
    klan_keyword: BAD MOONS
    abilities:
      - id: wh40k_9e.orks.klan.bad_moons.armed_to_da_teef
        name_en: "Kultur — Armed to da Teef"
        ability_type: subfaction_passive
        source: subfaction_rule
        rule_text: "Add 6\" to the Range characteristic of Dakka and Heavy weapons models
          with this kultur are equipped with. Each time a model with this kultur makes a
          ranged attack, on an unmodified wound roll of 6, improve the AP characteristic
          of that attack by 1."
        conditions:
          - subfaction_id: bad_moons   # NEU: bindet die Fähigkeit an roster.clan == "bad_moons"
        effect:
          type: multi
          effects:
            - type: buff_stat
              target: self
              stat: range
              modifier: 6
              weapon_types: [Dakka, Heavy]
            - type: buff_ap
              target: self
              modifier: 1
              condition: unmodified_wound_roll_6
```

```yaml
# data/wh40k_9e/necrons/subfaction_abilities.yaml — Auszug, 1 Dynastie (korrigierter Wortlaut)
subfactions:
  - id: mephrit
    name_en: Mephrit
    abilities:
      - id: necrons.dynasty.mephrit.solar_fury
        name_en: Solar Fury                 # korrigiert (war: Talent for Annihilation)
        ability_type: subfaction_passive
        source: dynastic_code
        rule_text: "Add 3\" to the Range characteristic of ranged weapons (excluding
          Pistols) that models with this code are equipped with. Each time a model with
          this code makes a ranged attack that targets a unit within half range, improve
          the AP characteristic of that attack by 1."
        conditions:
          - subfaction_id: mephrit
        effect:
          type: multi
          effects:
            - type: buff_stat
              target: self
              stat: range
              modifier: 3
              weapon_types: [ranged]
              excludes_weapon_types: [Pistol]
            - type: buff_ap
              target: self
              modifier: 1
              condition: half_range
```

### 5c. Engine-/UI-Stellen, die den neuen Typ konsumieren müssten

| Stelle | Änderung |
|---|---|
| `gameObjects/ability.py` | `Condition.subfaction_id: str \| None = None` ergänzen |
| `gameMechanic/abilityEngine.py` | `check_conditions()`: neue Prüfung `cond.subfaction_id and cond.subfaction_id != subfaction_value_for(player)` → False. Neue Funktion `get_active_subfaction_passives(faction_dir, player) -> list[Ability]`, analog zu `get_active_round_choice_modifier` — filtert `load_subfaction_abilities()` auf `ability_type == "subfaction_passive"` + `subfaction_id`-Match, ohne Event-/Timing-Bezug (permanent) |
| `gameMechanic/combat.py` (o. ä. Phase-Handler) | Konsumiert `get_active_subfaction_passives()` für numerische Effekte (`buff_stat`, `buff_ap`, …) — analog zum bestehenden `_WIRED_EFFECT_TYPES`-Muster für `round_choice` |
| `uiLayout/armyCard.py` | Neue generische Render-Funktion `_render_subfaction_passive_badge()` — zeigt `rule_text`/Kurzfassung der aktiven Klan-/Dynastie-Fähigkeit als Info-Badge (kein Aktivierungsbutton, analog Kategorie 3 „Auto-Progression") |
| `uiLayout/unitCard.py` | Optional: Badge auf Unit-Ebene, wenn ein `buff_stat`/`buff_ap`-Effekt konkret diese Einheit betrifft (Muster aus Kategorie 6f-Backlog, noch nicht gebaut — gleiche Abhängigkeit wie dort) |
| Necron `complex`-Handler | 4 Einträge (Novokh, Sautekh, Nephrekh-Translokation, Szarekhan bereits gelöst) brauchen echte `effect.type`-Werte statt `complex`+`handler` — jeweils eigener kleiner Engine-Baustein (z. B. `ap_on_charge_or_charged`, `rapid_fire_double_within_range`, `advance_replace_with_translocate`, `morale_reroll`) |

---

## 6. Klassen-Einordnung (A/B/C nach `docs/spec/acceptance/rules.md`-Systematik)

| Fähigkeit | Klasse | Begründung |
|---|---|---|
| Bad Moons, Evil Sunz, Deathskulls (Reroll/ObjSec-Teil), Freebooterz, Goffs (Hit-6-Teil) | **A** | Reine Zahlen-Modifikatoren/Reroll, App kann direkt rechnen/anzeigen |
| Blood Axes (Light Cover >18") | **C** | AP/Cover-Teil rechenbar (App kennt Range-Werte der Waffe), aber „>18" Distanz zum Schützen" ist eine Tisch-Messung → Hybrid wie bestehendes `ignore_cover_half_range`-Muster |
| Snakebites (Wound-Fail-Schwelle mit S8+-Ausnahme) | **A** | Reine Zahlenregel, App kennt Waffenstärke (`_parse_strength`) |
| Deathskulls (Mortal-Wound-Negierung 5+) | **A** | Zahlenregel |
| Szarekhan (beide Klauseln) | **A** | Bereits als funktionierendes Muster vorhanden (Undying-Legions-P/S-Analogie) |
| Novokh (Charge-Reroll + AP-Bonus) | **A** | Zahlenregel, `charged`-Flag existiert bereits im Unit-State |
| Mephrit (Range-Bonus + Half-Range-AP) | **A** | Beide Teile rein rechnerisch, Half-Range ist bereits als Muster vorhanden (Vengeful-Stars-Direktive) |
| Nephrekh (6+ Invuln) | **A** | Zahlenregel |
| Nephrekh (Translokations-Bewegung) | **C** | Der „kein Advance-Wurf, +6" Move"-Teil ist rechenbar; „durch Modelle/Terrain hindurchbewegen" ist räumliches Tracking → Tisch-Anteil (gleiche Einstufung wie andere Bewegungsregeln in der App) |
| Sautekh (Morale-Reroll, RF-Verdopplung ≤18") | **C** | Morale-Reroll ist A-tauglich; „RF verdoppelt auf ≤18"" braucht Zielentfernung → Tisch-Anteil (App kann nur den Hinweis zeigen, wie bei Half-Range-Cover) |
| Nihilakh (ObjSec-Teil) | **A** | Deckt sich mit bestehendem `objective_secured`-Effekttyp (Deathskulls-Analogie) |
| Nihilakh (Sekundärklausel) | **offen** | Klassifikation hängt an der ungeklärten Quellenlage (§2) — erst nach Klärung einstufbar |

---

## 7. Aufwandsschätzung (grob, S/M/L je Teilbereich)

| Fraktion | Daten (Korrektur + neues Feld) | Engine (Filter + Query-Pfad + Handler) | UI (Badge) | Tests |
|---|---|---|---|---|
| **Orks** (7 Klans, 1 Delta) | **S** — 1 Textkorrektur (Snakebites) + `ability_type`/`subfaction_id`-Feld für 7 Einträge | **S** — kein `complex`-Handler-Rückstand bei Orks, nur Filter + Query-Pfad (gemeinsam mit Necrons, s. u.) | **S** — 1 generische Badge-Funktion, faktoriert Klan-Text aus YAML | **S** — 7 Loader-Tests + 3–4 Engine-Tests |
| **Necrons** (6 Dynastien, 4 Deltas) | **M** — 4 Textkorrekturen (teils komplette Neufassung: Nihilakh, Sautekh, Mephrit-Name, Nephrekh-Ergänzung) + Klärung Nihilakh-Sekundärklausel vor Umsetzung nötig | **M** — gleicher Filter/Query-Pfad wie Orks (geteilter Aufwand) **plus** 4 neue Effekttypen für die bisherigen `complex`-Handler (Novokh AP-on-charge, Sautekh RF-double + Morale-Reroll, Nephrekh Translokation) | **S** — nutzt dieselbe Badge-Funktion wie Orks | **M** — 6 Loader-Tests + Effekttyp-Tests je neuer Handler (4×) + Regressionstest für die Wortlaut-Korrektur |
| **Engine-Grundgerüst** (Filter + `get_active_subfaction_passives`, faktionsunabhängig) | — | **S** (einmalig, deckt beide Fraktionen ab) | — | **S** — generischer Test „subfaction_id-Filter schließt fremde Klans/Dynastien aus" |

**Gesamt grob:** S–M über beide Fraktionen, wenn Option B (neuer `ability_type`) gewählt wird
und die Necron-Wortlautkorrektur vorab freigegeben ist. Größter Einzelposten: die 4 fehlenden
Necron-Effekttypen (Sautekh/Novokh/Nephrekh) — das sind neue, bisher nicht existierende
Mechanik-Bausteine, kein reiner Datenfix.

---

## 8. Entscheidungsfragen an den Stakeholder

1. **Nihilakh-Sekundärklausel:** Zwei widersprüchliche Quellen (§2) — AP-(-1)→AP-0 im eigenen
   Deployment Zone vs. Hit-Reroll-1 beim Schießen ohne Bewegung. Soll vor der Umsetzung eine
   Primärquelle (Codex-PDF/offizielles FAQ) geprüft werden, oder reicht eine der beiden
   Wahapedia-Fassungen als Arbeitsgrundlage (mit Markierung als „ungeklärt, ggf. Korrektur
   nötig")?
2. **Reihenfolge:** Erst die 5 Wortlaut-Fehler an den **bestehenden** 13 Einträgen korrigieren
   (kleiner, unabhängiger Bugfix-Auftrag), dann erst die Engine-/UI-Verdrahtung? Oder beides in
   einem Rutsch, weil Korrektur und Schema-Wechsel (`triggered` → `subfaction_passive`) ohnehin
   dieselben Zeilen anfassen?
3. **Option A vs. Option B (§5a):** neuer `ability_type: subfaction_passive` (Empfehlung) oder
   bestehenden `triggered`-Typ nur reparieren (kleinerer Diff, aber Vermischung mit reaktiven
   Fähigkeiten bleibt)?
4. **Scope der Klasse-C-Fälle:** Sollen Blood Axes (Light-Cover-Distanz), Nephrekh (Translokations-
   Bewegung) und Sautekh (RF-Reichweitenprüfung) im ersten Schritt nur als Tisch-Hinweis (Klasse
   C, kein Engine-Rechenanteil außer dem A-tauglichen Teil) umgesetzt werden, oder soll die
   räumliche Prüfung zurückgestellt werden bis ein generisches Distanz-Tracking existiert (vgl.
   die bereits zurückgestellten Necron-Arkana mit „räumliches Proximity-Tracking fehlt")?
5. **`docs/spec/faction_abilities.md`-Nachzug:** Der Doku-Drift-Befund (Kategorie 6 fälschlich
   „größtenteils abgedeckt") — soll die Spec-Korrektur Teil desselben Auftrags sein oder separat
   nachgezogen werden?
6. **Priorität gegenüber restlichem S144/Ziel-7-Backlog:** Wo reiht sich dieser Auftrag ein
   (vor/nach FixD, mypy-Ratchet, on_target-Anker — s. `next_session.md` „Nächste Schritte")?
