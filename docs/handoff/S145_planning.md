STATUS: ANSWERED

# S145 Planning-Entwurf — v2 (2026-07-14)

Überarbeitung nach Stakeholder-Rückgabe der v1. Struktur: Stand → Frage-1-Klärung →
Entscheidungen/Konzepte zu Fragen 2–5 → Prioritäten-Konsolidierung (Frage 6) →
S145-Aufgabenliste → verbleibende Entscheidungsfragen.

## Stand (unverändert zur v1, gekürzt)

Ziel 7 aktiv; Branches zu S145-Beginn konsolidiert (nur noch `dev` + `main`, `dev` gepusht,
Stand `942e1ba`). S144: Review S143 nachgeholt, Stratagem-Datenpflege (Necrons 56→40, Orks
28→17), mypy 28→24. Kernbefund S144: Klan-/Dynastie-Daten existieren seit ~S100
(`subfaction_abilities.yaml`), sind aber teils fachlich falsch und mangels Engine-Filter
komplett wirkungslos — Bugfix+Engine-Lücke, kein neues Feature. Freigegeben und baubereit:
`on_target`-Anker Option A (S143), FixD Brief 1 (S144), Vigilus-Warlord-Traits-Entfernung (S144).

---

## Frage 1 — Nihilakh: FAKTISCH GEKLÄRT, keine Entscheidung mehr nötig

Die 9E-Primärquelle liegt lokal vor: `docs/work/wahapedia_necrons/faction_overview.txt`,
Dynastie-Codes vollständig ab Z. 847 (Mephrit 847, Nephrekh 872, **Nihilakh 908–936**,
Novokh 937, Sautekh 972, Szarekhan 1011 — per grep verifiziert). Wortlaut
„Aggressively Territorial" (Z. 908 ff.):

1. Objective Secured; Modelle, die ObjSec bereits haben, zählen als **+1 Modell** bei
   Objective-Kontrolle.
2. AP-1-Attacken gegen Modelle, deren Einheit **vollständig in der eigenen Deployment Zone**
   steht, werden **AP 0**.
3. Bei reiner Nihilakh-Armee (exkl. DYNASTIC AGENT / C'TAN SHARD): **beide Direktiven** beim
   Protocol of the Eternal Guardian.

Die „widersprüchliche Zweitquelle" (Hit-Reroll 1 stationär) war der 8E-Code — erledigt.
**Lessons Learned (für alle Folgeaufträge verbindlich):** lokalen Korpus prüfen, BEVOR eine
Frage als offen markiert wird. Alle weiteren Necron-Wortlaut-Prüfungen gegen
`faction_overview.txt` Z. 761 ff., nicht gegen Web-Quellen. (Damit sind auch die
Soll-Wortlaute für Sautekh/Novokh/Nephrekh/Mephrit aus dem S144-Konzept lokal bestätigt —
stichprobengeprüft in diesem Planning.)

---

## Frage 2 — Reihenfolge Wortlaut-Fixes vs. Engine: ENTSCHIEDEN (delegiert)

**Entscheidung dieses Plans: zweistufig — erst Daten-Bugfix, dann Engine/UI.**

- **Brief K1 (Daten, Effort S):** Nur die 5 Wortlaut-Fehler in den bestehenden 13 Einträgen
  korrigieren (`rule_text` + `name_en`; Snakebites-S8+-Klausel, Novokh AP statt Hit, Nephrekh
  Translokations-Text, Sautekh komplette Neufassung, Nihilakh gemäß Frage-1-Klärung inkl.
  Mephrit-Name „Solar Fury"). Quelle jetzt lokal: `faction_overview.txt` Z. 847–1035.
  Kein Schema-Change, kein `src/`-Edit.
- **Brief K2+ (Engine/UI, nach Schema-Entscheid Frage 3):** Subfraktions-Filter, Query-Pfad,
  Effekttypen, Badge.

**Begründung:** (a) Kleine Schritte, jeder einzeln grün/committbar (Projektprinzip) — der
Textfix ist unabhängig vom Schema-Entscheid korrekt und wertvoll (die `rule_text`-Zeilen sind
das, was die UI später anzeigt); (b) der Datenwächter `tests/gameObjects/test_data_quality.py`
liefert das Testmuster für Daten-Briefs; (c) K1 berührt NUR `data/…/subfaction_abilities.yaml`
— dateidisjunkt zu FixD/on_target (`_common.py`), also parallelisierbar; (d) das
Gegenargument „dieselben Zeilen zweimal anfassen" wiegt gering: der spätere Schema-Wechsel
ändert pro Eintrag nur die `ability_type`-/`conditions`-Zeilen, nicht die in K1 korrigierten
Texte — kein echter Doppel-Aufwand, kein Konfliktpotenzial.

---

## Frage 3 — Datenschema: Erläuterung + Empfehlung

Begriffsklärung (Benennung wie im Konzept `S144_klan_dynastie_konzept.md` §5a):
**Option A = bestehenden `ability_type: triggered` behalten und reparieren.
Option B = neuer `ability_type: subfaction_passive`.**

**Was heute in der YAML steht** (`data/wh40k_9e/necrons/subfaction_abilities.yaml:22–40`,
Mephrit, gekürzt — `ability_type: triggered` ist Z. 27):

```yaml
- id: necrons.dynasty.mephrit.talent_for_annihilation   # Name falsch (soll: Solar Fury)
  ability_type: triggered
  source: dynastic_code
  trigger: { timing: persistent, phase: shooting, stage: active, player: active }
  conditions: []            # ← KEINE Bindung an die Dynastie-Wahl des Rosters!
  effect: { type: buff_ap, target: self, modifier: 1 }
```

Zwei Fehler unabhängig vom Schema: `conditions: []` bindet nichts an `roster.dynasty`, und
`timing: persistent` wird vom einzigen Abfrage-Pfad (`get_triggered_abilities`, nur
`timing="phase_start"` via `commandPhase.py:31`) nie gematcht.

**Derselbe Eintrag unter Option A** (triggered bleibt, nur Lücken schließen):

```yaml
  ability_type: triggered                # unverändert
  conditions:
    - subfaction_id: mephrit             # NEU: Filter gegen roster.dynasty
  # trigger/effect unverändert; NEUE Engine-Funktion fragt timing=persistent ab
```

**Derselbe Eintrag unter Option B** (neuer Typ):

```yaml
  ability_type: subfaction_passive       # NEU: eigener Typ
  conditions:
    - subfaction_id: mephrit             # NEU: identisch zu Option A
  # trigger-Block kann entfallen (permanent per Definition)
```

**Konsequenzen im Vergleich:**

| | Option A (`triggered` reparieren) | Option B (`subfaction_passive`) |
|---|---|---|
| YAML-Migration | keine (nur `conditions`-Zeile je Eintrag) | 13× `ability_type`-Feldwert ändern + `conditions`-Zeile (mechanisch, 1 Brief) |
| Loader (`loader.py`) | unverändert | unverändert (lädt `ability_type` als String; ggf. 1 Validierungszeile) |
| Engine | neue Funktion `get_active_subfaction_passives()` + `subfaction_id`-Check in `check_conditions()`; **Risiko:** die 13 Einträge bleiben im `triggered`-Pool — jede künftige `get_triggered_abilities`-Erweiterung (neue Timings/Phasen) kann sie **versehentlich einsammeln** | gleiche neue Funktion + gleicher Check; die 13 Einträge fallen aus dem `triggered`-Pool heraus — saubere Trennung „reaktiv-event-getrieben" vs. „permanent-listengebunden" |
| Tests | Bestand unverändert; neue Filter-/Query-Tests | dito + 1 Loader-Test „subfaction_passive wird geladen" |
| Spec-Passung | Kategorie 6 (`faction_abilities.md:288`) bleibt ohne eigenen Typ | deckt sich exakt mit der dokumentierten, bislang leeren Kategorie 6 „Passive/Persistent" |
| Diff-Größe | kleiner | geringfügig größer (mechanischer Feldwert-Change) |

**Empfehlung: Option B.** Der Mehraufwand ist ein mechanischer Feldwert-Change in einer Datei
pro Fraktion; dafür ist das Verwechslungsrisiko mit echten reaktiven `triggered`-Abilities
(Living Metal u. a. in `unit_abilities.yaml`) dauerhaft ausgeschlossen, und die Spec-Kategorie 6
bekommt endlich ihre reale Entsprechung. → **Verbleibende Stakeholder-Entscheidung 1.**

### Option C — abilityEngine als Paket aufdröseln (Stakeholder-Rückfrage)

Rückfrage: Ability-Logik analog zur bewusst separat gehaltenen `stratagemEngine.py` nach
passiv/aktiv/triggered trennen und als Ordner/Paket `abilityEngine/` organisieren?
Kritische Bewertung wie erbeten:

**Ist-Struktur** (`src/gameMechanic/abilityEngine.py`, 594 Zeilen, 29 Funktionen —
Zeilennummern per grep erhoben):

| Cluster | Funktionen (Auswahl, Zeile) | Zeilen | Anteil |
|---|---|---|---|
| Generische Dispatch-Primitiven | `check_trigger` (37), `check_conditions` (49), `execute_effect` (69) | 37–84 | ~8 % |
| **round_choice-/Direktiv-Logik (Protokolle)** | `_tagged_effect` (90), `_extra_directive_effects` (99), `_active_directive_effects` (134), `_sum_effect_value` (184), 7× `get_active_round_choice_*` (224–341), `get_active_protocol_effects` (365), `get_active_rp_modifiers` (379) | 85–392 | **~52 %** |
| Revive/Heal (RP, Living Metal) | `get_after_attack_revive_ability` (393), `revive_dice_count` (422), `get_active_heal_bonus` (434) | 393–454 | ~10 % |
| `active_buffs`-Konsumenten (Unit-Buffs) | `buff_stat_bonus` (481), `ability_invuln_save` (498), `ability_badge_label` (510), `charge_after_advance_allowed` (531) | 455–547 | ~16 % |
| activated-/triggered-Queries | `get_activated_command_abilities` (548), `get_triggered_abilities` (563) | 548–594 | ~8 % |

Aufrufer (grep über `src/` + `tests/`): 7 src-Dateien (`commandPhase.py`, `chargePhase.py`,
`shootingPhase.py`, `stratagemEngine.py`, `_common.py`, `armyCard.py`, `unitCard.py`),
6 Test-Dateien. Zum Vergleich `stratagemEngine.py` (180 Z., 4 Funktionen): dort wurde NICHT
nach Aktivierungsmodus geschnitten, sondern nach **Quell-Objekttyp** — alles, was ein
`Stratagem`-Objekt anwendet/gated (`_apply_stratagem_effect` Z. 25, `_effect_gate_met`
Z. 107); sie importiert selbst aus `abilityEngine` (`buff_stat_bonus`,
`ability_invuln_save`). Die faktische Trennlinie ist „Stratagem vs. Ability", nicht
„aktiv vs. passiv".

**Kritische Bewertung:**

1. **Der Schnitt passiv/aktiv/triggered trägt die reale Struktur nicht.** Der dominante
   Block (~52 %) ist round_choice-/Direktiv-Logik — weder klar „passiv" noch „triggered",
   sondern „pro Runde gewählt". „Triggered" ist heute winzig (47 Zeilen, genau 1 Aufrufer:
   `commandPhase.py:31`), und „passiv" existiert noch gar nicht — das ist erst der
   K2-Zuwachs. Ein Modus-Schnitt läge quer zu den tatsächlichen Verantwortlichkeiten;
   die natürlichen Nähte sind **Direktiven/Protokolle | Unit-Buffs+Revive |
   Queries+Dispatch**.
2. **594 Zeilen sind (noch) kein Kohäsionsproblem.** Die Datei ist um eine Frage kohäsiv
   („welche Ability-Effekte sind für diesen Konsumenten gerade aktiv?"). Simplicity First +
   DRY-Regel (CLAUDE.md: erst ab dritter Wiederholung abstrahieren) sprechen gegen einen
   Umbau auf Vorrat. Das reale Problem im großen Block ist ohnehin nicht Größe, sondern
   Duplikation — dafür existiert bereits die gezieltere Schuld „DRY Directive-Aktiv-Logik"
   (`docs/goals/backlog.md:534`, S143-Befund, Entscheid S144). Erst DRY, dann ggf. schneiden.
3. **Architektur-Gate: unkritisch.** `tests/architecture/test_layer_imports.py` prüft nur
   die Import-Richtung zwischen Schichten (gameObjects importiert nie
   gameMechanic/uiLayout, Z. 21–32) — ein Paket `gameMechanic/abilityEngine/` bliebe
   innerhalb der Schicht. Migrationsaufwand rein mechanisch: 7 src- + 6 Test-Importstellen;
   mit re-exportierendem `__init__.py` sogar null Call-Site-Änderungen. `tools/mypy_gate.py`
   zählt Gesamtfehler, keine Modulpfade — ebenfalls unkritisch.
4. **Orthogonal zu Frage 3.** YAML-Schema (A/B) und Code-Organisation (C) sind unabhängig —
   C ersetzt den Schema-Entscheid NICHT. Risikoärmste Reihenfolge: **B jetzt entscheiden →
   K1 → K2 → C nur bei Bedarf.** Ein Paket-Umbau VOR K2 legte Refactor-Diffs genau in die
   Phase, in der die `_common.py`-Serie (on_target → FixD) läuft, ohne ein aktuelles
   Problem zu lösen.

**Empfehlung: Option C zurückstellen — mit konkretem Schwellwert statt „nie", plus ein
kostenloses Zugeständnis sofort:**

- **Jetzt:** K2 legt die neue Subfraktions-Passiv-Logik von Anfang an in ein **eigenes
  Modul** (z. B. `gameMechanic/subfactionPassives.py`) statt in `abilityEngine.py` —
  das erfüllt das Stakeholder-Anliegen (Trennung nach Logik, Präzedenz stratagemEngine)
  für den Neuzugang, ohne Bestand anzufassen; `abilityEngine.py` wächst durch K2 nicht.
- **Split-Trigger:** Überschreitet `abilityEngine.py` dennoch ~800 Zeilen ODER wird die
  DRY-Schuld (`backlog.md:534`) angegangen, dann Paket-Split als eigener Refactor-Brief —
  Schnitt entlang der realen Nähte (Direktiven | Unit-Buffs/Revive | Queries/Dispatch),
  NICHT passiv/aktiv/triggered. Effort S, ~15–20k Token, re-exportierendes `__init__.py`
  als Kompatibilitätsschicht; nicht parallel zu Briefs mit `abilityEngine`-Importänderungen.

---

## Frage 4 — Klasse-C-Fälle: bestehendes Muster reicht, kein neues Konzept

Der Stakeholder hat recht — die Konvention existiert und ist konsistent belegt:

- **Definition:** `docs/spec/acceptance/rules.md:8–12` — Klasse A (App rechnet/erzwingt),
  B (nur Tisch), C (Hybrid: App-Anteil + Tisch-Anteil).
- **Muster 1 — Hinweis-Caption für Reichweiten-Bedingung:** Rapid Fire ist als **Klasse C**
  geführt (`rules.md:169`): App zeigt Caption `[RAPID FIRE · <range>" · ½ = <half>"]`
  (`src/uiLayout/_common.py:1402`, `_rapid_fire_caption`), die Verdopplung selbst rechnet die
  App bewusst NICHT (range-agnostisch).
- **Muster 2 — Badge an bestehender Checkbox:** `ignore_cover_half_range` (Vengeful Stars S):
  Engine-Flag `abilityEngine.py:295` (`get_active_round_choice_ignores_cover_half_range`),
  grüne Badge an der Light-Cover-Checkbox `_common.py:2095–2097` — die Distanzprüfung bleibt
  Tisch.
- **Muster 3 — Nutzer-Checkbox für Tisch-Bedingung:** Combat Attrition / Gretchin Cowardly
  (`rules.md:761`): App zeigt Schwellwert, die Tisch-Bedingung („RUNTHERD in 6"?") hakt der
  Spieler selbst ab.
- **Muster 4 — Datenfeld für reine B-Anteile:** `enforcement: table`
  (`necrons/faction_abilities.yaml:74,112`; Schema-Kommentar
  `_schema/round_choice.example.yaml:63–64`).

**Anwendung auf die drei Fälle — exakt nach diesen Mustern, nichts Neues:**

| Fall | A-Anteil (App rechnet) | Tisch-Anteil (Muster) |
|---|---|---|
| **Blood Axes** (Light Cover wenn Angreifer >18") | keiner — Distanz unbekannt | Muster 3: Spieler hakt die bestehende Light-Cover-Checkbox selbst; zusätzlich Badge „TAKTIKS >18"" daneben (Muster 2), damit die Regel sichtbar ist. Fall-Back-Teil (schießen ODER chargen): Hinweis-Caption |
| **Nephrekh** (Translokation) | 6+ Invuln (bereits Klasse A, Effekt existiert); „kein Advance-Wurf, +6" Move, Schießverbot bis Zugende" als Movement-Choice-Variante | „durch Modelle/Terrain hindurch": Hinweis-Caption (Muster 1) |
| **Sautekh** (RF-Verdopplung ≤18") | Morale-Reroll (Klasse A, Reroll-Hint-Muster wie Undying Legions P) | RF-Verdopplung: exakt das Rapid-Fire-Muster 1 — die bestehende Caption `_rapid_fire_caption` um den Sautekh-Fall erweitern („double attacks if target ≤18"") — App rechnet weiterhin nicht |

**Konsequenz:** Frage 4 braucht keinen Stakeholder-Entscheid mehr — die Klasse-C-Fälle werden
im ersten Schritt als App-Anteil + Tisch-Hinweis nach bestehendem Muster umgesetzt; ein
generisches Distanz-Tracking bleibt wie bisher außerhalb des Scopes (konsistent mit den
zurückgestellten Necron-Arkana).

---

## Frage 5 — Spec-Nachzug `faction_abilities.md`: erübrigt sich als eigene Frage

**Was nachzuziehen wäre:** genau ein kleiner Abschnitt — Kategorie 6
(`docs/spec/faction_abilities.md:288–293`, 6 Zeilen). Die Status-Zeile Z. 293
(„Größtenteils abgedeckt durch `triggered`-Abilities in `faction_abilities.yaml`") ist
falsch/veraltet: die Einträge liegen in `subfaction_abilities.yaml` und sind (bis zur
Umsetzung) wirkungslos. Nachzug = Status-Zeile korrigieren + 5–10 Zeilen zum neuen
Schema/Query-Pfad. Die Datei-Scope-Tabelle (Z. 15) ist bereits korrekt.

**Empfehlung:** Kein separater Auftrag. DoD-Punkt 7 (CLAUDE.md) verlangt Artefakt-Nachzug
**im selben Schritt** wie die Umsetzung — der Spec-Nachzug wird Pflichtbestandteil des
Engine-Briefs (K2), analog FixD Brief 3. Damit ist Frage 5 beantwortet, keine Entscheidung nötig.

---

## Frage 6 — Prioritäten-Konsolidierung (Kernanliegen)

### 6.1 Befund: JA, die drei Artefakte driften

Vier Prioritäts-Aussagen existieren nebeneinander:

1. **`.claude/tasks/next_session.md` § „Nächster Schritt (S145, Reihenfolge)"** — aktuelle
   5er-Liste (Klan/Dynastie-Entscheid → on_target → FixD Brief 1 → Vigilus → mypy-uiLayout).
   Frisch (S144), in sich konsistent.
2. **`docs/goals/backlog.md` §0 (Z. 31)** — trägt das Tag `🔴 [PRIO-NÄCHSTE] #2b
   Direktiv-Lock` mit dem offenen Rest „Direktive ab Bewegungsphase sperren" als „nächste
   größere Aufgabe". Das Tag stammt aus der S52-Ära und **widerspricht** der
   next_session-Liste, in der #2b gar nicht vorkommt — **stale Prio-Tag**.
3. **`docs/audit/plans/README.md` Z. 42** — „Empfohlene Reihenfolge (akt. S123): 018 → 015 →
   026 → 017" nennt FixD **nicht**, obwohl FixD in derselben Tabelle (Z. 40) als einziger
   P1-(HOCH)-Plan steht. Pikant: `backlog.md` §1 (Z. 108) erklärt genau diese README als
   **„kanonisch"** für Plan-Status & Reihenfolge — der kanonische Ort trägt also eine
   veraltete Reihenfolge. **Direkter Widerspruch** zu next_session.md.
4. **`docs/goals/ziel7.md`** — fachliche Reihenfolge „allgemein → Stufe B (Necrons) → Stufe C
   (Orks), danach UX-Pass" (§0-Kontext Z. 22–24; Stufe-C-Gate „erst nach Abschluss Stufe B"
   Z. 83–85). Spannung (kein harter Widerspruch): Stufe B hat noch eine offene Checkbox
   (Necron-Roster-UI-Verifikation, Z. 76), während next_session.md Stufe-C-Arbeit (Vigilus,
   Klan/Dynastie) vorzieht. Auflösung: die offene B-Checkbox ist manuelle **Verifikation**
   (Stakeholder am Bildschirm), keine Implementierung — sie blockiert Datenpflege-Arbeit an
   Stufe C nicht, sollte aber sichtbar eingeplant bleiben.

### 6.2 Konsolidierte Prioritätenliste (nächste 2–3 Sessions)

| Rang | Arbeitspaket | Begründung | Dateien (Kern) | Parallel? |
|---|---|---|---|---|
| 1 | **Klan/Dynastie-Entscheid** (nur noch Frage 3 Option A/B + diese Liste) | blockiert Rang 6–7; Konsens-Entscheid gehört an den Session-Anfang (Planner-Pflichtregel) | keine | — |
| 2 | **on_target-Anker Option A** | S143 freigegeben; löst einen bestätigten Stakeholder-UX-Befund (Whirling Onslaught); klein | `src/uiLayout/_common.py` | ⛔ nicht mit Rang 4/5 (gleiche Datei) |
| 3 | **Vigilus-Warlord-Traits entfernen** | S144 entschieden; Datenqualitäts-Schuld, XS-Restrisiko | `data/wh40k_9e/orks/warlord_traits.yaml` | ✅ mit Rang 2 (disjunkt) |
| 4 | **FixD Brief 1** (Compute/Render-Trennung) | einziger P1-Plan; Brief 2+3 und mypy-uiLayout hängen dahinter | `src/uiLayout/_common.py` | ⛔ nach Rang 2 (gleiche Datei); ✅ mit Rang 6 |
| 5 | **FixD Brief 2 + 3** | Brief 2 hinter Mockup-Gate (Stakeholder), Brief 3 = Spec-Nachzug | `_common.py`, `fightPhase.py`, `shootingPhase.py`, `gameState.py`; Doku | ⛔ sequenziell nach Brief 1 |
| 6 | **Klan/Dynastie Brief K1** (Wortlaut-Bugfix, Frage-2-Entscheid) | 5 fachlich falsche Einträge = Schuld; data-only, lokal belegte Quelle | `data/wh40k_9e/*/subfaction_abilities.yaml` | ✅ mit Rang 4/5 (disjunkt) |
| 7 | **Klan/Dynastie K2+** (Engine-Filter, Query-Pfad, 4 Necron-Effekttypen, Badge, Spec-Nachzug) | macht 13 Einträge erstmals wirksam; L → vor Vergabe in ≤ M-Briefs splitten | `abilityEngine.py`, `ability.py`, `armyCard.py`, Spec | teils; Detailschnitt im Umsetzungsplan |
| 8 | **Stufe-B-Rest: Necron-Roster-UI-Verifikation** (+ offene manuelle Checks §3 backlog) | hält das ziel7-Stufengate ehrlich; reine Stakeholder-Bildschirmzeit | keine (manuell) | ✅ jederzeit |
| 9 | **mypy-Ratchet uiLayout (17)** | explizit hinter FixD Brief 1–3 (Datei-Überschneidung `_common.py`) | `src/uiLayout/*` | ⛔ erst nach Rang 5 |
| 10 | **#2b Direktiv-Lock-Rest** („ab Bewegungsphase sperren") | stale-Tag-Klärung: entweder neu einreihen oder Prio-Tag entfernen — Stakeholder-Votum in der Listen-Freigabe | `armyCard.py` o. ä. | nach Einreihung |

**Parallel-Kriterium** (disjunkte Dateien): Rang 2∥3, Rang 4∥6, Rang 8 jederzeit. Der bekannte
`_common.py`-Konflikt erzwingt die Serie 2 → 4 → 5 → 9.

### 6.3 Kanonischer Ort der Reihenfolge (Vorschlag, freigabepflichtig)

**Vorschlag:** Die Gesamt-Priorität lebt künftig **ausschließlich in `docs/goals/backlog.md`**
als neuer, kompakter Kopfabschnitt „Prioritätenliste" (die Tabelle aus 6.2, nur Rang +
Paket + Verweis — keine Details). Das passt zur CLAUDE.md-Artefakt-Landkarte („Was ist
insgesamt offen? → backlog.md") und schafft keine zweite Datei. Daraus folgt:

- **`next_session.md`** führt nur noch den **nächsten Schritt** (1–3 Punkte) + Verweis auf
  die Backlog-Prioritätenliste — keine eigene Langliste mehr.
- **`docs/audit/plans/README.md`** führt nur noch **Status je Plan**; die beiden
  „Empfohlene Reihenfolge"-Zeilen (Z. 42, Z. 77) werden entfernt, ebenso beansprucht die
  README nicht mehr „kanonisch für Reihenfolge" (backlog.md Z. 108 entsprechend anpassen:
  kanonisch nur für *Status*).
- **Inline-Prio-Tags** wie `[PRIO-NÄCHSTE]` (backlog.md Z. 31) entfallen — Priorität steht
  nur in der Liste.
- **`ziel7.md`** behält seine *fachlichen* Stufen-Gates (B vor C) — das ist Ziel-Logik, keine
  Session-Priorität; die Prioritätenliste referenziert sie.

Umsetzung = kleiner Doku-Brief (Effort S, freigabepflichtig), siehe Aufgabe 2 unten.

---

## Abgeleitete S145-Aufgabenliste

| # | Aufgabe | Dateien | Token | Effort | Modus |
|---|---|---|---|---|---|
| 1 | Stakeholder-Entscheid: Frage 3 (Option A/B) + Freigabe Prioritätenliste 6.2/6.3 (inkl. #2b-Votum) | keine | ~2k | XS | Konsens |
| 2 | Prioritäten-Konsolidierung umsetzen: backlog.md-Kopfabschnitt, next_session.md kürzen, plans/README-Reihenfolge-Zeilen raus, `[PRIO-NÄCHSTE]`-Tag raus | `docs/goals/backlog.md`, `.claude/tasks/next_session.md`, `docs/audit/plans/README.md` | ~10k | S | Gate |
| 3 | Vigilus-Warlord-Traits entfernen (5 Einträge, grep-Absicherung, Datenwächter-Test) | `data/wh40k_9e/orks/warlord_traits.yaml`, Tests | ~12k | S | Gate |
| 4 | on_target-Anker Option A (Verschwinde-Regel bei Ziel-Toggle, Regressionstests) | `src/uiLayout/_common.py` (`render_group_assignment` ~Z. 2506), `tests/uiLayout/` | ~30k | S–M | Gate |
| 5 | Klan/Dynastie Brief K1: 5 Wortlaut-Fixes gegen `faction_overview.txt` Z. 847–1035 | `data/wh40k_9e/necrons/subfaction_abilities.yaml`, `data/wh40k_9e/orks/subfaction_abilities.yaml`, Tests | ~15k | S | Gate |
| 6 | FixD Brief 1 (Compute/Render-Trennung; nur wenn Kontext-Korridor es nach 1–5 noch erlaubt — Review-Budget-Regel ab ~100k beachten) | `src/uiLayout/_common.py` | ~38k | M | Gate |

Aufgabe 3∥4 und 5 sind dateidisjunkt (parallelisierbar); 4 vor 6 zwingend (`_common.py`).
Tier-Vorschlag: Executor Sonnet für 2–6; Aufgabe 5 mit Haiku-Vorprüfung der Wortlaute möglich.

## Verbleibende Entscheidungsfragen an den Stakeholder

1. **Frage 3 — Datenschema:** Option B (`ability_type: subfaction_passive`, Empfehlung) oder
   Option A (`triggered` reparieren)? — Option C (Paket-Split) ist hierzu orthogonal und
   ersetzt diese Entscheidung nicht.
2. **Option C — Zurückstellung bestätigen (Konsent, kein Widerspruch reicht):** K2-Neucode
   in eigenes Modul, Paket-Split erst ab Schwellwert (~800 Z. oder DRY-Schuld-Angang) und
   dann entlang der realen Nähte statt passiv/aktiv/triggered — einverstanden?
3. **Prioritätenliste 6.2 + kanonischer Ort 6.3 freigeben?** Inklusive Votum zu #2b
   Direktiv-Lock-Rest (Rang 10): neu einreihen (wo?) oder Prio-Tag ersatzlos entfernen?
4. *(optional, Terminfrage)* **Stufe-B-Verifikation (Rang 8):** in S145 als
   Stakeholder-Bildschirmzeit einplanen oder auf S146 legen?

Fragen 1, 2, 4, 5 des S144-Konzepts sind mit diesem Dokument geklärt bzw. entschieden
(Q1 faktisch, Q2 delegiert entschieden, Q4 per Bestandsmuster, Q5 via DoD-7).

---

## Selbstprüf-Checkliste

- [x] Alle Zitate mit Datei+Zeile belegt (faction_overview.txt 847/872/908/937/972/1011 per
      grep; rules.md 8–12/169/761; `_common.py` 1402/2095–2097; abilityEngine.py 295;
      faction_abilities.yaml 74/112; faction_abilities.md 15/288–293; backlog.md 31/108;
      plans/README.md 40/42/77; ziel7.md 76/83–85; subfaction_abilities.yaml 22–40)
- [x] Jede Behauptung über bestehende Konventionen per grep/Read verifiziert (nicht aus dem
      Gedächtnis) — inkl. Klasse-A/B/C-Definition, Rapid-Fire-Caption, enforcement:table,
      Option-C-Erhebung (abilityEngine.py Funktionsliste per grep, Aufrufer per grep über
      src/+tests/, stratagemEngine.py 25/107, test_layer_imports.py 21–32, backlog.md 534)
- [x] Checkbox-Sync gegen git log (v1, unverändert gültig — kein stale Check)
- [x] Jede vorgeschlagene Aufgabe hat Dateiliste + Token-Schätzung + Effort ≤ M
- [x] Keine Datei außer S145_planning.md geschrieben

---

## Stakeholder-Entscheide (2026-07-14)

1. **Frage 3 — Datenschema:** **Option B** (`ability_type: subfaction_passive`). Zusätzlich im
   K2-Scope: YAML-Struktur aufräumen (totes `source`-Feld u. ä. — im K2-Brief per grep zu
   verifizieren), UI-Sichtbarkeit der passiven Effekte (z. B. Nephrekh 6+-Invuln, Nihilakh
   AP-1→0 als Badge/Hinweis), Doppel-Direktiven-Klausel muss für alle 6 Dynastien-Protokolle
   funktionieren.
2. **Option C — Zurückstellung bestätigt** (Konsent): mit Schwellwert (~800 Zeilen
   `abilityEngine.py` oder DRY-Schuld-Angang); K2-Neucode in eigenes Modul
   `subfactionPassives.py`. Zusätzlich neu aufgenommen: „abilityEngine-Refactor-Vorplanung"
   als paralleles Planungspaket in die Prioritätenliste (analog FixD-Vorplanung — nur
   Planung/Handoff-Dokument, kein Code, kann parallel zu allem laufen).
3. **Prioritätenliste 6.2 + kanonischer Ort 6.3: FREIGEGEBEN.** #2b Direktiv-Lock-Rest bleibt
   Rang 10 (eingereiht), der Inline-Tag `[PRIO-NÄCHSTE]` wird entfernt.
4. **Stufe-B-Verifikation:** Stakeholder macht sie laufend; Anleitung entsteht parallel als
   `docs/handoff/S145_stufeB_verifikation.md`.
