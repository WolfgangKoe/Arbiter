NEEDS-DECISION

# Planning — Session S119 (2026-07-03)

**Priorität:** P1 (Bugfix P21) → P2 (P19) → P3 (P20, klärungsbedürftig)
**Scope:** Ziel7-Cluster P19/P20/P21 aus `backlog.md` §5 (Stakeholder-Vorgabe: P21 zuerst, Root-Cause
gegen Live-Verhalten abgleichen). Alternative (§6-Cluster `collect_modifiers_for_phase`/6f/6h) geprüft,
Empfehlung: **diese Session** beim Ziel7-Cluster bleiben.

---

## Stand-Check

**Nach S118 (committed, GO):** Carry-over-Cluster abgebaut, DS-2-Rollout fertig, UI-Pass S118 DONE
(17/20 erfüllt). Drei Restpunkte wurden sauber als Ziel7-Anforderungen **P19/P20/P21** in
`backlog.md` §5 überführt — das ist der Auftrag für S119.

### Checkbox-Sync (Pflichtschritt, durchgeführt)

Befehl: `git log --oneline -25` gegen die Haken in `docs/goals/ziel6.md` (6a–6n, Akzeptanzkriterien,
Session-Historie S28–S59 stichprobenartig, da Datei 1219 Zeilen — Vollscan über `grep -n "^\[x\]\|- \[x\]\|- \[ \]"`).

- **Keine neuen stale Checks gefunden.** Alle `- [x]` in 6a–6n tragen entweder ein Commit-Datum/-Hash
  oder einen expliziten Testnamen-Beleg (z. B. P17 „getestet: `test_lock_invariante_*`", P18 „verifiziert
  S117 gegen `git log`, `e6fcdb3`"). Deckt sich mit `git log --oneline -25`: die dort sichtbaren Commits
  `29f4f81`/`3915f8c`/`4bddc28`/`143d848` entsprechen exakt S118/S117/P18-Fix/S116 — keine Lücke.
- **Offene Checkboxen** (`- [ ]`) in ziel6.md sind ausschließlich die bereits nach Ziel7 ausgelagerten
  Punkte (6e Execute-Logik, 6f Badges, 6h Kat1–3, Akzeptanzkriterien Ka'tah/AdMech/Auto-Progression-Badge/
  Ability-Badges) — konsistent mit `ziel7.md`, kein Widerspruch.
- **Nebenbefund (kein Blocker, nicht Teil des Checkbox-Sync-Auftrags):** `docs/goals/ziel7.md` „Fix B —
  WAAAGH! generisch" listet die drei Tasks noch als offen (`- [ ]`), obwohl `ziel6.md` 6h Fix B bereits
  als ✅ erledigt (S113, Commit `e031616`) führt. Doku-Drift zwischen den beiden Zieldateien — für die
  spätere Doku-Pflege vormerken (nicht S119-Scope, da außerhalb des Checkbox-Sync-Auftrags „gegen
  ziel6.md"), aber im Abschluss von S119 kurz nachziehen, falls Zeit bleibt (XS, siehe Carry-over).

---

## Vorgeschlagene Tasks

| # | Aufgabe | Effort | Token-Schätzung | Modus | Tier | Scope-Zeile |
|---|---------|--------|-----------------|-------|------|-------------|
| 1 | P21 — Undo-Lifetime-Bugfix | S | ~18k | Gate | Sonnet | `Phase-UI anpassen` / eigener Fund unten |
| 2 | P19 — per-Spieler-Tracking | S/M | ~24k | Gate | Sonnet | wie 1 |
| 3a | P20 — UX-Klärung (Konsens) | XS | ~3k | Konsens | Opus (Koordinator, kein Subagent) | — |
| 3b | P20 — Implementierung (nach 3a) | M | ~28k | Gate | Sonnet | `Phase-UI anpassen`, `Waffenstärke/Parsing` |

---

### Task 1 — P21: ↺-Undo überlebt Phasenwechsel (BUG, ZUERST)

**Root-Cause-Analyse (bereits durchgeführt, mit Code-Belegen):**

`src/uiLayout/gameProtocoll.py:133-134` liest zwei Sets aus dem Session-State:
```python
used_ids: set[str] = st.session_state.get("used_stratagem_ids", set())            # phase-scoped
used_battle_ids: set[str] = st.session_state.get("used_stratagem_battle_ids", set())  # battle-scoped
```
Zeile 183 verschmilzt beide zu einem einzigen Flag:
```python
is_used = strat.id in used_ids or strat.id in used_battle_ids
```
Zeile 195 nutzt **dasselbe** Flag, um sowohl das Label *(used)* **als auch** den Undo-Button zu steuern:
```python
if is_used:
    if st.button(f"{SYM_RESET} Rückgängig (+{strat.cp_cost} CP)", ...): ...
elif not disabled:
    if st.button(f"Use — spend {strat.cp_cost} CP", ...): ...
```
`used_stratagem_ids` wird bei **jedem** Phasenwechsel geleert (`game_state.py:531` in `_reset_phase_state()`,
aufgerufen von `next_phase()` bei **jedem** Zweig inkl. Spielerwechsel, `game_state.py:609-634`).
`used_stratagem_battle_ids` wird **nie** vor Spielende geleert (das ist der gewollte S113-Fix für
battle-scope). Ein einmal benutztes `once_per_battle`-Stratagem bleibt also bis Spielende in
`used_battle_ids` → sobald sein `phase`/`stage`-Filter in `stratagem_visibility()`
(`src/gameObjects/stratagem.py:71-115`) in einer späteren Phase/Runde/Spielerzug erneut zutrifft
(z. B. „command" tritt für **beide** Spieler jede Runde auf), wird der Eintrag wieder als `visible`
(`greyed`) gelistet, `is_used` ist weiterhin `True` → **der Undo-Button erscheint erneut**, obwohl das
Phasenfenster, in dem das Stratagem benutzt wurde, längst vorbei ist.

**Abgleich Live-Verhalten vs. S113-Code-Analyse (Auftrag):** `review-S113.md` B1 behauptete „laut Code
NICHT [angeboten]" — das war zum S113-Stand (**vor** Commit `4330bdc`) korrekt, wurde aber durch genau
diesen Commit (S113, „Enforce once_per_battle battle-scope; fix stratagem undo/label") **umgedreht**:
der Fix für das Label-Problem (B2, *„(used)"* statt *„(CP insufficient)"*) hat `is_used` um
`used_battle_ids` erweitert — als Nebenwirkung hängt jetzt auch der Undo-Button an diesem erweiterten
Flag. Der S118-UI-Pass hat das live bestätigt (`ui-pass-S118.md` Zeile 18: „Darf im nächsten Zug nicht
mehr angeboten werden!"). Root Cause ist damit eindeutig belegt, keine weitere Exploration nötig.

**Fix-Ansatz:** Label-Anzeige (*(used)*) und Undo-Button-Sichtbarkeit entkoppeln. Undo darf nur
angeboten werden, solange das Stratagem **im aktuellen Phasenfenster** benutzt wurde
(`strat.id in used_ids`), nicht wenn es nur battle-scoped „irgendwann in dieser Partie" benutzt wurde.
Das Label bleibt wie in S113 korrigiert (beide Sets).

Konkret — neue reine Funktion in `src/gameObjects/stratagem.py` (neben `stratagem_visibility`,
Streamlit-frei, testbar; folgt dem S118-Präzedenzfall `_capped_modifier_threshold`):
```python
def stratagem_undo_visible(
    stratagem_id: str,
    used_this_phase: set[str],
    used_in_battle: set[str],
) -> bool:
    """Return True only while the stratagem's own phase-window is still open.

    Undo must disappear once the phase changes, even if the stratagem stays
    battle-greyed afterwards (once_per_battle persists; the undo window does not).
    """
    return stratagem_id in used_this_phase
```
(Trivial genug, dass eine reine Funktion fast überdimensioniert wirkt — aber DRY/Testbarkeit +
Konsistenz mit dem S118-Präzedenzfall rechtfertigen sie; alternativ akzeptabel: Inline-Variable
`is_used_this_phase = strat.id in used_ids` direkt in `gameProtocoll.py`, wenn der Executor das für
klarer hält — dann **keine** neue Funktion, aber trotzdem ein dedizierter Regressionstest via
`stratagem_visibility`-Testmuster in `test_stratagem.py` auf der bestehenden Signatur nachbilden, s. u.)

In `gameProtocoll.py` Zeile ~183/195 die Fallunterscheidung dreiteilen:
1. `is_used_this_phase` (bzw. `stratagem_undo_visible(...)`) → Undo-Button.
2. `is_used` (Label, unverändert wie S113) → *(used)*-Text im Expander-Header.
3. Weder noch, nicht disabled → Use-Button.

**Betroffene Dateien:**
- `src/gameObjects/stratagem.py` — neue Hilfsfunktion (falls Executor sich dafür entscheidet)
- `src/uiLayout/gameProtocoll.py` — Undo-Sichtbarkeit von `is_used` auf phase-scope umstellen
- `tests/gameObjects/test_stratagem.py` — neue Tests für die Hilfsfunktion (falls extrahiert)

**Testebenen:**
- Unit-Test (PFLICHT, Regressionstest für den Bugfix): z. B.
  `test_undo_hidden_after_phase_reset_but_battle_greyed_persists` — Fälle: (a) nur `used_this_phase`
  → Undo sichtbar; (b) nur `used_in_battle` (phase gewechselt) → Undo **nicht** sichtbar, Label bleibt
  *(used)*; (c) beides (gerade erst benutzt) → Undo sichtbar.
- Manuelle UI-Verifikation (Render-Code, PFLICHT, explizit benennen): mit einem echten
  `once_per_battle`-Stratagem (z. B. Necron `stratagems.yaml`) — (1) benutzen → Undo sichtbar,
  CP sinkt; (2) Phase weiterklicken → Stratagem bleibt greyed/*(used)*, **Undo verschwindet**;
  (3) eine Runde später erneut dieselbe Phase erreichen (bzw. Gegnerzug mit gleicher Phase) → weiterhin
  kein Undo; (4) Spielreset → Stratagem wieder clickable.

**Token-Schätzung:** ~18k (Root Cause ist vom Planner bereits vollständig geklärt — Executor
implementiert direkt, kein weiteres Debugging nötig).
**Tier: Sonnet** (Begründung: kein reiner Lookup — Code-Änderung + Testdesign + Wiring-Beleg;
Sonnet ist Default für Executor-Fleißarbeit mit vorab geklärtem Root Cause).

---

### Task 2 — P19: once_per_battle-Gefechtsoption blockt fälschlich beide Spieler

**Regel-Beleg (geprüft, keine weitere Recherche nötig):** `core_rules.txt:3110` — CP-Pools und
Stratagem-Einsatz sind pro Spieler; die „once per battle"-Einschränkung einer Stratagem-**Instanz**
bezieht sich auf den Einsatz **durch diesen Spieler**, nicht auf einen globalen Zähler über beide
Armeen hinweg (kein Textbeleg für eine geteilte Sperre über beide Spieler). Deckt sich mit dem
Stakeholder-Befund in `ui-pass-S118.md` Zeile 16.

**Root Cause (Code):** `used_stratagem_battle_ids` ist ein **einziges globales** `set[str]`
(`game_state.py:421`), nicht nach Spieler partitioniert — anders als das CP-Pool-Pattern
(`cp: dict[str, faction] → int`, bereits in `gameProtocoll.py:127-129` verwendet) oder das bereits
etablierte Per-Spieler-Muster `round_choice_state_key(player, kind)` (`game_state.py`, S52-Fix für
dasselbe Kollisionsproblem bei Command Protocols).

**Fix-Ansatz (folgt dem bestehenden `cp`-Dict-Muster, kein neues Konzept):**
`used_stratagem_battle_ids: dict[str, set[str]] = {}` — Key = Fraktion/Spieler (`spending_faction`,
bereits in `gameProtocoll.py` pro Stratagem berechnet), Value = deren battle-scoped IDs.

**Betroffene Dateien:**
- `src/gameMechanic/game_state.py:421` — Init auf `dict[str, set[str]] = {}` umstellen
- `src/uiLayout/gameProtocoll.py:134/171-172/201-222` — Lesen/Schreiben auf
  `used_battle_ids_by_faction.get(spending_faction, set())` umstellen; an `stratagem_visibility()`
  weiterhin ein **einfaches** `set[str]` (die Slice des jeweiligen Spielers) übergeben —
  `stratagem.py` selbst bleibt unverändert (Signatur, Docstring-Zeile zu „regardless of player turn"
  auf „innerhalb der Battle-Laufzeit dieses Spielers" präzisieren, da sie sonst nach dem Fix
  irreführend ist)
- `tests/gameMechanic/test_game_state.py:701-710` — bestehender Test
  `test_does_not_reset_used_stratagem_battle_ids` auf Dict-Form umstellen
  (`{"Necrons": {"opb.strat_x"}}` statt `{"opb.strat_x"}`)
- Neuer Test (PFLICHT, Regressionstest): z. B.
  `test_battle_scoped_stratagem_used_by_one_player_does_not_block_other` — Necrons benutzen ein
  `once_per_battle`-Stratagem, danach ist dieselbe Stratagem-ID für Orks weiterhin `clickable`.

**Testebenen:**
- Unit-Tests wie oben (game_state Fixture-Update + neuer Cross-Player-Test).
- Manuelle UI-Verifikation (Render-Code, PFLICHT): zwei Spieler, gleiche once_per_battle-Stratagem-ID
  (z. B. ein `_shared`-Stratagem wie Insane Bravery) — Spieler A benutzt es, Spieler B sieht es weiterhin
  clickable; Label zeigt eindeutig erkennbar, dass A (nicht B) es benutzt hat (durch die Fix-Struktur
  automatisch gelöst, da Sichtbarkeit jetzt korrekt pro Spieler berechnet wird — trotzdem im Live-Test
  gegenprüfen, ob das Label für den Stakeholder eindeutig genug ist).

**Token-Schätzung:** ~24k (zwei Dateien + Test-Migration + neuer Test + manuelle Verifikation mit
zwei Fraktionen aufsetzen).
**Tier: Sonnet** (gleiche Begründung wie Task 1 — Root Cause geklärt, Umsetzung folgt einem
etablierten Muster im Code, aber echte Implementierungsarbeit, kein Lookup).

**Reihenfolge-Hinweis:** Task 2 baut auf denselben Zeilen in `gameProtocoll.py` wie Task 1 auf —
**erst Task 1 fertig committen, dann Task 2 beginnen** (nicht parallel im selben Diff), sonst
Merge-Unschärfe zwischen Undo-Scope-Fix und Per-Spieler-Fix.

---

### Task 3 — P20: Rapid-Fire-Attackenzahl bei halber Reichweite

**Regel-Beleg:** `core_rules.txt:1578-1586` — Rapid Fire verdoppelt die Attackenzahl pro Modell, wenn
das Ziel innerhalb der halben Waffenreichweite liegt. Die App hat aktuell nur eine **Caption**
(`_rapid_fire_caption`, `_common.py:539`), die die halbe Reichweite informativ anzeigt — es gibt
**keinen Eingabe-Mechanismus**, wie viele Modelle einer Gruppe innerhalb dieser halben Reichweite
stehen (die App kennt keine Modellpositionen; das muss der Spieler angeben).

**⚠️ Ambiguität — braucht Stakeholder-Entscheidung, bevor implementiert wird (Task 3a):**

Der S118-Befund-Wortlaut ist auf zwei Arten lesbar:
- **Variante A (empfohlen):** Neues Zahlenfeld „Modelle in halber Reichweite" (0…Modellzahl der
  Gruppe). App berechnet `attacks = modelle_volle_reichweite × attacks_je_modell +
  modelle_halbe_reichweite × attacks_je_modell × 2`. Der Cap „10 bei 10 Warriors" ist dann der
  Modell-Cap der Gruppe — bei Gauss Flayer (1 Attacke/Modell) zahlenmäßig deckungsgleich mit der
  Basis-Attackenzahl, was die Formulierung im Befund erklärt, ohne dass die Verdopplungsmechanik
  (der eigentliche Zweck von Rapid Fire) verloren geht.
- **Variante B:** Ein Zahlenfeld überschreibt die Gesamt-Attackenzahl direkt, gecappt auf die
  **unverdoppelte** Basis-Attackenzahl — d. h. **keine** Verdopplung wird abgebildet, das Feld dient
  nur dazu, weniger Modelle als die volle Gruppe feuern zu lassen. Deckt den Wortlaut „gecappt auf …
  bei mehr als der halben Reichweite" wörtlicher, würde aber die Kernregel (Verdopplung bei halber
  Reichweite) gar nicht umsetzen — wirkt wie eine Fehllesung des eigentlichen Feature-Wunsches.

Variante A wird empfohlen (trifft den Regelzweck; der Beispielwert „10 bei 10 Warriors" ergibt sich
zwangsläufig aus 1 Attacke/Modell und ist kein Gegenbeleg). **Trotzdem: bevor Task 3b beginnt, dem
Stakeholder Variante A vorlegen und bestätigen lassen** (CLAUDE.md: „Nur wenn nach Lesen der Regeln
mehrere UI-Varianten möglich sind, den Nutzer nach dem bevorzugten Layout fragen").

**Betroffene Dateien (Task 3b, nach Bestätigung):**
- `src/gameMechanic/attack_math.py` — `_compute_attacks`/`_total_attacks_int` um einen optionalen
  `models_half_range: int | None`-Parameter erweitern (Verdopplungs-Rechnung nur wenn Waffe Rapid Fire
  ist, sonst unverändert)
- `src/uiLayout/_common.py` — Eingabefeld neben der bestehenden `_rapid_fire_caption`-Anzeige in
  `render_group_assignment()` (Zeile ~1706-1713), Wert in den Attacken-Aufruf durchreichen
  (`_total_attacks_int`/`_compute_attacks`-Call-Sites)
- `tests/gameMechanic/test_attack_math.py` (falls vorhanden, sonst passendes Test-Modul für
  `attack_math.py` finden/anlegen) — Verdopplungs-Tests: 0 Modelle halbe Reichweite (unverändert),
  alle Modelle halbe Reichweite (voll verdoppelt), gemischt

**Testebenen:**
- Unit-Tests für die reine Rechenfunktion (PFLICHT, mehrere Fälle wie oben).
- Manuelle UI-Verifikation (Render-Code, PFLICHT): Necron Warriors mit Gauss Flayer (Rapid Fire 1) —
  Feld auf 10 setzen bei 10 Modellen → Attackenzahl verdoppelt sich sichtbar; Feld auf 0 → unverändert;
  Feld-Cap greift bei Eingabe > Modellzahl.

**Token-Schätzung:** ~3k (Task 3a, Klärung — kein Subagent, das ist eine direkte
Stakeholder-Rückfrage über die Mailbox) + ~28k (Task 3b, Implementierung nach Bestätigung).
**Tier Task 3a:** Koordinator/Opus (Stakeholder-Kommunikation läuft nie über einen Subagenten,
ADR-0007 Kanal-Regel). **Tier Task 3b:** Sonnet (Implementierung nach geklärter Spec).

---

## Alternative: §6-Cluster (`collect_modifiers_for_phase`/6f/6h) statt Ziel7-P19/P20/P21

**Geprüft, Empfehlung: NICHT diese Session — beim P19/P20/P21-Cluster bleiben.**

Begründung:
- **Größenordnung:** Das §6-Cluster (`ability_engine.collect_modifiers_for_phase`, `Ability.modifier`-
  Schema, Phase-Handler-Verdrahtung für Shooting/Fight/Charge, danach erst 6f Ability-Badges) ist ein
  mehrschichtiger Architektur-Umbau (Effort **L**, mehrere Sessions) — kein S119-großer Zuschnitt
  („Tasks klein schneiden, sodass eine Aufgabe sicher unter dem Korridor bleibt").
  6h Kat1-3 (AdMech/Tyranids/T'au/SM/Death Guard/Chaos SM) ist zusätzlich **blocked-by-YAML** (kein
  Datenverzeichnis vorhanden) — reine Vorarbeit ohne unmittelbaren Spielwert diese Session.
- **P19/P21 sind echte Regressions-/Regel-Bugs** (blockt fälschlich den Gegner bzw. bietet eine
  ungültige Aktion an) — laut Stakeholder-Live-Test in S118 bestätigt, höhere Priorität als ein
  Architektur-Vorgriff auf neue Fraktionen.
- **Root-Cause-Vorarbeit ist bereits erledigt** (dieser Plan) — die Ziel7-Tasks sind damit ohne
  weitere Exploration startklar; das §6-Cluster bräuchte selbst erst wieder eine eigene
  Root-Cause-/Schema-Design-Phase (siehe `ziel7.md` — noch nicht mal ein Plan-Dokument vorhanden).

Wenn der Stakeholder das §6-Cluster dennoch vorzieht: eigener Planungsschritt nötig
(Schema-Design `Ability.modifier`, Pilot-Fraktion — Necrons+Orks laut `ziel6.md` 6e — vor jeder
Code-Änderung), passt nicht in den bereits vorbereiteten S119-Rahmen.

---

## Carry-over

- **Manuelle UI-Verifikation (Rest aus S113, `review-S113.md`, noch nicht im S118-Pass geprüft):**
  (a) Mirror-Protokoll Necron-vs-Necron Befehlsphase (funktioniert die Direktivwahl korrekt, wenn
  beide Spieler dieselbe Fraktion/dasselbe Protokoll-Set spielen?); (b) stationär+D1 grünes
  +1-Save-Badge in den Würfeln (Eternal Guardian D1 „Light Cover wenn nicht bewegt" — Badge-Anzeige
  im SAVE-Block prüfen). **Empfehlung:** an den ohnehin für Task 1/2 nötigen manuellen UI-Durchgang
  anhängen (App läuft bereits, gleiche Session, geringer Zusatzaufwand) statt separat zu terminieren.
- **Doku-Drift `ziel7.md` „Fix B" stale** (s. Checkbox-Sync-Nebenbefund oben): beim S119-Abschluss
  kurz nachziehen, wenn Zeit bleibt (XS, ~2k Token) — kein Blocker für P19/P20/P21.

---

## Offene Fragen an den Stakeholder

1. **P20 (Task 3a, blockiert Task 3b):** Variante A (Modell-Zähler „in halber Reichweite", App
   verdoppelt automatisch) vs. Variante B (direkter Attacken-Override ohne Verdopplungslogik) —
   siehe Herleitung oben. Empfehlung: Variante A.
   Entscheidung: Ich würde es ganz einfach halten. Wir erhöhen Attackencap ganz einfach auf die maximal mögliche Anzahl an Attacken, wobei als Default die Anzahl an Attacken steht als ob alle Modelle Ziel oberhalb der halben Reichweite wählen. Werden mehrere Ziele gewählt, darf die Gesamtzahl der Attacken die obere Cap nicht überschreiten. Das sollte aber schon implementiert sein (Prüfen!). Letztendlich wird der Schaden am Ende der Attackenfolge unabhängig von der Anzahl der Attacken eingetragen. Die Würfelei wird in der App nicht getrackt. 
2. **Reihenfolge/Umfang für diese Session:** Reicht der Token-Korridor für alle drei Tasks
   (~18k + ~24k + ~3k Klärung + optional ~28k Task 3b ≈ 73k ohne 3b / ~101k mit 3b, jeweils zzgl.
   Review/DoD ~15-20k) — Vorschlag: P21 + P19 fest für S119, P20 nur wenn Klärung (Frage 1) schnell
   beantwortet ist UND Kontext bei Task-3b-Start noch unter ~90k liegt; sonst P20 nach S120 schieben
   (kein Blocker, da unabhängig von P19/P21).
   Entscheidung: Hier folge ich deiner Einschätzung
3. **Carry-over-Bündelung:** Die zwei offenen S113-UI-Checks (Mirror-Protokoll, +1-Save-Badge) wie
   vorgeschlagen an den S119-UI-Durchgang anhängen — Einverstanden, oder lieber separat?
   Entscheidung: Einverstanden
