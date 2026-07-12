STATUS: ANSWERED (S141 — Teil A=FixA; Teil B Insassen → S142-Backlog, dann löschen)

# S141 — Befund Gruppe B: Emergency Disembarkation erscheint nicht (Gunwagon)

Stakeholder-Befund 4 (manuelle Verifikation): Gunwagon zerstört → Emergency-Disembarkation-GO
erschien nicht. Zusätzlich: Insassen-Zuordnung (welche Einheit sitzt im Transport) fehlt.

## 1. Regel — Emergency Disembarkation (Quelle)

- **Destroyed Transports (Core-Regel, kein Stratagem):** `docs/work/wahapedia_core_rules/core_rules.txt`
  Z. 1023–1052. Ist ein TRANSPORT zerstört, müssen alle eingestiegenen Einheiten **sofort**
  aussteigen (3" vom Modell, nicht in Engagement Range), bevor das Modell entfernt wird; pro
  ausgestiegenem Modell 1 W6 — auf 1 stirbt ein Modell. Kein Charge/Heroic Intervention diese
  Runde. Das ist verpflichtend, unabhängig von Stratagems.
- **Emergency Disembarkation (Stratagem, 1CP):** Z. 3214–3234. Ersetzt obige Werte durch 6"
  (statt 3") und würfelt auf 1 **oder 2** (statt nur 1) — mehr Fluchtdistanz, höheres Sterberisiko.
  Genau dieser Stratagem-Text ist bereits 1:1 in `data/wh40k_9e/_shared/stratagems.yaml`
  (`wh40k_9e.shared.stratagem.emergency_disembarkation`, Z. 58–71) hinterlegt: `conditions:
  [TRANSPORT]`, `timing: phase_reactive`, `event: on_destroy`.
- **Gunwagon** (`docs/work/wahapedia_orks/units_all.txt` Z. 963–981): Keywords u. a.
  `TRANSPORT`, `WAGON`, `GUNWAGON`; Kapazität 12 `<CLAN>`-INFANTRY oder Flash Gitz; eigene
  `Explodes`-Fähigkeit (separat von Emergency Disembarkation).

## 2. Ist-Zustand Code/Daten

**GO-Infrastruktur existiert bereits vollständig** (Plan 015, S138/S139/S141-Vorarbeit) — das ist
kein Blindfleck, sondern ein Bug in einer schon gebauten Kette:

- `_maybe_flag_transport_destroyed()` (`src/uiLayout/_common.py:1154`) setzt
  `st.session_state.pending_transport_destroyed = {faction, uid}`, sobald ein Unit mit Keyword
  `TRANSPORT` neu auf `destroyed` wechselt. Aufgerufen aus `wound_adjustment_buttons` (Z. 305)
  und aus `_render_damage_block` (Z. 1729) — Letzteres hängt an `render_attack_resolution()`, das
  sowohl `shootingPhase.py` als auch `fightPhase.py` nutzen. Deckt also Shooting- und Fight-Phase
  ab; Psychic-Phase-Mortal-Wounds (Smite/Perils) sind laut eigenem Docstring (Z. 1163–1165)
  bewusst **nicht** abgedeckt (dokumentierte Lücke aus S138/139, kein neuer Befund).
- `_render_pending_emergency_disembarkation()` (Z. 1174) wird generisch aus
  `render_player_column()` (Z. 382) aufgerufen — läuft also in jeder Phase, die diese
  Standard-Spalte nutzt (movement/shooting/charge/fight).

**Root Cause des gemeldeten Bugs** liegt in genau dieser Funktion, Z. 1197–1203:

```python
render_reactive_stratagem_box(
    faction,
    phase=PHASES[st.session_state.get("phase_idx", 0)][1],
    event="on_destroy",
    decline_key=marker["uid"],
    context_caption=f"{unit.name_en} (TRANSPORT) was destroyed.",
)
```

`unit_for_conditions` wird **nicht** übergeben, obwohl `unit` (der zerstörte Gunwagon) direkt
zuvor per `lookup()` geholt wird (Z. 1193). `render_reactive_stratagem_box()` reicht
`unit_for_conditions` (Default `None`) an `stratagem_conditions_met(strat.conditions, unit)`
weiter (`src/gameObjects/stratagem.py:87–103`): bei nicht-leerer `conditions`-Liste und
`unit=None` liefert die Funktion **immer** `False` (Z. 101–102, bewusstes Fail-Safe-Verhalten,
kein Bug in `stratagem_conditions_met` selbst). `stratagem_visibility()`
(`src/gameObjects/stratagem.py:119` ff.) prüft `conditions_met` **zuerst** (Z. 157–158) und
gibt bei `False` sofort `"hidden"` zurück — vor jeder Phase-/CP-/Timing-Prüfung. Da Emergency
Disembarkation `conditions: [TRANSPORT]` hat (im Gegensatz zu Cut Them Down/Fire
Overwatch/Counter-Offensive, die alle `conditions: []` führen), ist sie die **einzige** reaktive
GO, die dieses Loch trifft — genau die Konstellation, vor der der Docstring von
`render_reactive_stratagem_box` selbst warnt (Z. 800–807: "a future keyword-gated reactive GO
with no unit_for_conditions passed is hidden rather than shown for every unit") — die Warnung kam
zu spät, denn die einzige *heutige* Nutzung mit Keyword-Bedingung (`_render_pending_emergency_
disembarkation`) verletzt sie bereits.

**Warum die Testsuite grün blieb:** `tests/uiLayout/test_common.py:1549`
(`test_pending_transport_destroyed_for_own_faction_renders_box`) mockt
`render_reactive_stratagem_box` komplett weg (`MagicMock`) und prüft nur `faction`, `event`,
`decline_key`, `context_caption` — nicht, ob `unit_for_conditions` mitgegeben wird. Der eigentliche
Bug liegt also unterhalb der Mock-Grenze und ist durch den bestehenden Test strukturell nicht
sichtbar.

**Fix-Umfang:** eine Zeile (`unit_for_conditions=unit` in Z. 1197 ergänzen) + ein Regressionstest,
der den echten `render_reactive_stratagem_box`-Pfad (nicht gemockt) mit einem TRANSPORT-Unit und
`conditions_met` durchläuft und die GO als `"ready"`/sichtbar verifiziert. **XS**, kein Datenmodell
nötig für diesen Teil.

## 3. Insassen-Zuordnung — fehlt vollständig

Recherche (breit, `src/`, `data/rosters/*.yaml`, `game_state.py`): **kein** Treffer für
embark/passenger/cargo/inside/transport_uid als Zustandsfeld. Es gibt:

- kein Feld im Roster-YAML-Schema, das "Einheit X startet eingestiegen in Transport Y" ausdrückt
  (`data/rosters/orks_transport.yaml` listet Warboss/Gunwagon/Boyz/Gretchin als vier unabhängige,
  unverknüpfte Einträge — Kommentar Z. 4–6 nennt Emergency Disembarkation als Testzweck, aber das
  Roster selbst kann keine Einstiegs-Relation kodieren).
- kein Zustandsfeld in `game_state.py`/`unit_mutations.py` für "eingestiegen in" — nur
  `melee_with` als vergleichbares Beziehungs-Array zwischen Einheiten existiert (Vorbild-Muster,
  kein Transport-Äquivalent).
- keine Embark/Disembark-Aktion in der Movement-Phase-UI (`movementPhase.py`): der einzige Treffer
  dort ist ein Kommentarverweis auf `_render_pending_emergency_disembarkation` (Z. 626), keine
  Embark-Logik.
- `context_caption` in `_render_pending_emergency_disembarkation` nennt daher nur den Namen des
  Transports ("Gunwagon (TRANSPORT) was destroyed."), niemals die Insassen — es gibt schlicht
  keine Daten, aus denen sich "Boyz saßen drin" ableiten ließe, selbst nach dem Bugfix aus
  Abschnitt 2.

**Gap-Analyse — minimal nötig, damit Insassen sichtbar würden:**
1. Roster-Schema-Erweiterung: Feld (z. B. `embarked_in: <unit-id-im-selben-Roster>`) pro Unit-Eintrag.
2. Loader-Anpassung (`gameObjects/loader.py`), das Feld zu lesen und gegen Transportkapazität zu
   validieren (Kapazitäts-Text steht nur als Freitext in der `ABIL`-Zeile, aktuell nicht
   strukturiert erfasst — auch das fehlt).
3. Game-State-Feld analog `melee_with`, z. B. `embarked_units: list[(faction, uid)]` auf dem
   Transport-Unit-State, plus Embark/Disembark-Mutationen (`unit_mutations.py`) für die
   Movement-Phase (3" normale Regel) und für den Destroyed-Fall (3"/6" je nach Stratagem).
   Diese Insassen-Liste ist Voraussetzung dafür, dass die Emergency-Disembarkation-GO-Karte
   überhaupt korrekt anzeigen kann, WELCHE Einheiten aussteigen — heute zeigt sie nur den
   Transport-Namen.
4. UI: Embark/Disembark-Buttons in der Movement-Phase (analog Break-Button bei `melee_with`),
   sowie Anzeige "eingestiegen in ⟨Transport⟩" auf der Unit-Karte.

## 4. Aufwands-/Scope-Einschätzung

- **Teil A (GO erscheint nicht):** XS-Bugfix — 1 Zeile + 1 Regressionstest. Kein
  Datenmodell-Eingriff, keine Design-Entscheidung nötig. Sofort umsetzbar.
- **Teil B (Insassen-Zuordnung):** eigenständiges Feature mit Datenmodell-Erweiterung
  (Roster-Schema + Loader + Game-State + Movement-Phase-UI) — S bis M, nicht in einer Executor-
  Session mit XS-Fix kombinierbar. Betrifft auch andere TRANSPORT-Einheiten (Night Scythe bei
  Necrons ist laut S141-Planning bereits in einem Roster vorhanden, aber ohne Insassen-Feld
  ebenso unvollständig).

## 5. Offene Design-Fragen an den Stakeholder

1. **Roster-Zeitpunkt:** Soll "eingestiegen in Transport X" nur als **Start-Zustand** im
   Roster-YAML deklarierbar sein (einfacher, deckt "startet eingestiegen" ab, core_rules.txt
   Z. 912–921), oder soll Embarken/Disembarken auch **während des Spiels** über die UI möglich
   sein (Movement-Phase-Buttons, deutlich größerer Scope wegen Kapazitätsprüfung pro Zug)?
2. **Kapazität automatisch geprüft oder nur Hinweis?** Der Kapazitätstext ("12 `<CLAN>` … INFANTRY
   models") ist aktuell Freitext in der `ABIL`-Spalte — soll die App die Kapazität hart
   durchsetzen (strukturiertes Datenfeld nötig) oder nur als Text-Hinweis anzeigen (App zeigt,
   Tisch prüft — Klasse B/C im Akzeptanz-Katalog)?

**Vor Fix von Teil A empfehle ich einen kurzen Blick, ob weitere `conditions`-gegatete reaktive
GOs (aktuell keine außer Emergency Disembarkation) denselben Fehler tragen — laut Recherche ist
sie aktuell die einzige mit nicht-leerer `conditions`-Liste unter den reaktiven Boxen.**
