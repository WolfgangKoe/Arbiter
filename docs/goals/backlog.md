# Backlog — zentraler Index

> **Ein Ort für „was ist offen".** Dieser Index führt die bisher verstreuten Quellen
> zusammen (Executor-Pläne, offene Tasks, manuelle Verifikation, Architektur-Schulden).
> **Details bleiben in den verlinkten Artefakten** — hier wird nicht dupliziert, nur verwiesen.
>
> Pflege: Wird ein Punkt erledigt, hier abhaken **und** in der Detailquelle. Neue Arbeit
> entweder als Plan in [../audit/plans/](../audit/plans/) oder als Task-Zeile hier.

Letzter Abgleich: 2026-06-18

---

## 0. Aktuelle Findings (S51 — Badge / Protokoll / Würfel)

Aus manueller UI-Verifikation. Vorgehen phasenweise, je Finding eigener Plan +
Freigabe. Akzeptanzkriterien (testbar) unter [../spec/acceptance/index.md](../spec/acceptance/index.md).

- ✅ **#1 Faktion-/Subfaction-Badge** (S51): Faktion-Badge zeigt Faktionsnamen
  (nicht Roster-Titel); Subfaction-Badge generisch + **immer sichtbar** (Wert /
  „No <Label>" / „No Subfaction"); helles Blau `#a5b4fc`. Alle Roster mit Pflicht-
  Subfaction. Pins: `AC-SUBFACTION-01..05`. „dynasty"-Vokabular aus `src/` entfernt.
- 🔲 **#2b Direktiv-Lock** (Phase 2, S52 Root-Cause): Direktive darf **nur in der
  Kommandophase** wählbar sein — **nicht im Setup** (`faction_overview.txt` Z. 568:
  Direktive „at the start of each battle round"; Setup = nur Zuweisung zu Runden, Z. 546)
  und ab Bewegungsphase gesperrt. **Bug (S52 manuell entdeckt):**
  `armyCard._render_round_choice_ui` läuft auch im Setup (Seitenleiste in allen Phasen),
  aktiviert per Auto-Block (`if not active_id`) das Runde-1-Protokoll + zeigt Direktiven-
  Buttons; das gepinnte `round_choice_active`/`_directive` blockiert zudem die nachträgliche
  Rundenzuweisung. **Fix:** in `_render_round_choice_ui` früh `return`, wenn
  `phase_key == "setup"` (einziger Setup-Einstieg ist `_render_round_choice_assignment`);
  zusätzlich Direktiven-Buttons (`_render_directive_buttons`/`_render_extra_round_choice`)
  an `phase_key == "command"` koppeln. Render-Code → manuelle Verifikation. AC + ggf.
  reiner Gating-Helfer als Regressionstest.
- 🔲 **#2 Protokoll-Buff-Audit** (Phase 3): **9 von 12** Direktiv-Effekten sind in
  `ability_engine.get_active_round_choice_modifier` **nicht verdrahtet** → unsichtbar.
  Jeden einzeln verdrahten/anzeigen, je eigener AC. Soll-Tabelle:

  | Protokoll · Direktive | Effekt | Ziel-Anzeige |
  |---|---|---|
  | Eternal Guardian · P | save_modifier +1 ✅ | SAVE-Block grün |
  | Eternal Guardian · S | reroll_save_1 ❌ | SAVE-Hinweis |
  | Hungry Void · P | hit_modifier +1 (Shooting) ✅ | HIT-Block |
  | Hungry Void · S | strength_modifier +1 (Shooting) ❌ | WOUND-Block S+1 |
  | Conquering Tyrant · P | leadership_bonus +1 ❌ | Morale |
  | Conquering Tyrant · S | reroll_hit_wound_1 (Melee) ❌ | HIT+WOUND Melee |
  | Sudden Storm · P | move_bonus +1 ❌ | Bewegungs-Badge |
  | Sudden Storm · S | advance_and_charge ❌ | Charge-Phase |
  | Undying Legions · P/S | rp_reroll / rp_bonus +1 ❌ | Reanimation-UI |
  | Vengeful Stars · P | wound_modifier +1 (Shooting) ✅ | WOUND-Block |
  | Vengeful Stars · S | ap_bonus -1 (Shooting) ❌ | SAVE-Block AP |

  Buff-Badge grün (`design_colors.md` §3), nur bei betroffenen Einheiten + im
  Phasen-Block (wie MWBD). Überschneidet sich mit Plan 016.
- 🔲 **#3/#4 Würfelanzeige** (Phase 4): Pfeilrichtung/-länge der Modifier-Zeile +
  Badge-Text (`+1` raus, da Pfeil das ausdrückt) + Badge-Breite (ragt in Würfel
  „1"). **Soll-Bild zuerst mit Nutzer als AC festlegen**, dann fixen, dann
  per AC einrasten (Lehre aus Finding 9.2 — nie still ändern).
- 🔲 **R-CMD-03 — CP-Grant ohne Battle-forged-Gating** (S55, aus Regel-Katalog):
  Der „Grant +1 CP"-Button in `commandPhase._render_faction_actions` erscheint für die
  aktive Seite **unabhängig von `game_mode`/Battle-forged** → eine Unbound-Armee könnte
  den Command-Phase-Bonus ebenfalls erhalten (Regel: nur Battle-forged). Fix-Ort:
  `_render_faction_actions` an Battle-forged koppeln + Regressionstest. Ledger-Eintrag
  `R-CMD-03` in [../spec/acceptance/rules.md](../spec/acceptance/rules.md).

---

## 1. Aktive Implementierungs-Pläne (Executor-Queue)

Detailpläne + Abhängigkeiten: [../audit/plans/README.md](../audit/plans/README.md). Pläne 001–013 = DONE.

| Plan | Titel | Prio | Status |
|------|-------|------|--------|
| [014](../audit/plans/014-p17-defender-loss-allocation.md) | P17: Verteidiger-Korrektur Schadenszuweisung (Gruppen) | HOCH | TODO |
| [016](../audit/plans/016-necron-protocol-effects.md) | Protokoll-Effekte auf RP/Living Metal + Dynastiebonus | MITTEL | TODO |
| [018](../audit/plans/018-low-prio-cleanup.md) | Kleinkram: CP-Doppelvergabe, Battle-Log-Reset, Gretchin, Modifier | NIEDRIG | TODO |
| [015](../audit/plans/015-contextual-reactive-stratagems.md) | Reaktive Stratagems: Overwatch, Counter-Offensive, HI-Hook | MITTEL | TODO |
| [017](../audit/plans/017-ability-ap-combined-badge.md) | SAVE-Block: Fähigkeit+AP kombinierte Badge | MITTEL | TODO |

**Empfohlene Reihenfolge: 014 → 016 → 018 → 015 → 017.** 014/015 haben Mockup-STOPPs
(UI erst vorlegen). 014 zwingend nach 013, beide ändern `_common.py` flächig — nie parallel.

---

## 2. Offene Tasks (kleiner als ein Plan)

Quelle + Details: [../../.claude/tasks/next_session.md](../../.claude/tasks/next_session.md) „Offene Tasks".

- 🟡 GO-Buttons kontextuell in gameActionArea (aktiver + inaktiver Spieler) statt Liste
- 🟡 Necron Command Phase: Regelkasten immer ganz oben (alle Phasen prüfen)
- 🟡 SAVE-Block: Fähigkeit + AP als eine Badge (`Enslaved AP-1`) — YAML-Erweiterung (→ Plan 017)
- 🟢 Gretchin Cowardly: −1 Attrition ohne RUNTHERD in 6" (→ Plan 018)
- 🟢 Battle-Log: nach Reset keine alten Einträge (→ Plan 018)
- 🟢 CP-Doppelvergabe-Fix + `collect_modifiers_for_phase()` (→ Plan 018)
- 🟢 **Operating-Model Phase B:** `tools/token_report.py` — Token-/Wer-leistete-was-Report,
  führt Haupt- + Subagent-Verbrauch zusammen; füttert Leitstand-Feld 4 (`LEITSTAND.md`).
- 🟢 **Operating-Model Phase C:** Refinement automatisieren — Sonnet-Subagent liest neue
  Bilder aus `Fotos/`, extrahiert die Idee als Text nach `docs/inbox/` (Format dort dokumentiert).

---

## 3. Offene manuelle UI-Verifikation (PFLICHT vor „fertig")

Render-Code ist von der Coverage ausgenommen → muss manuell geprüft werden.
Vollständige Checkliste: [../../.claude/tasks/next_session.md](../../.claude/tasks/next_session.md)
(„Manuelle UI-Verifikation" + S48 H1–H7).

- [ ] WAAAGH Boss-Nob: 4 Attacken auf Power Klaw, Wound-Block S 11
- [ ] Cover Option B: Dense im HIT-, Light/Heavy im SAVE-Block, je Tab
- [ ] Veil aus Nahkampf: kein „IN MELEE" danach; Undo stellt wieder her
- [ ] Skorpekh-Roster: 2× Threshers + 1× Reap-Blade getrennt
- [ ] S48 H1–H7 (Big Mek Wargear, Silent King Waffen, Living Metal, MWBD 2×, Badge-Farben, RP)

---

## 4. Architektur-Schulden

Messbar über das Architektur-Gate → [../spec/architecture_invariants.md](../spec/architecture_invariants.md).

- **Generic-src (INV-4 DEBT):** hartcodierte Fraktions-Defaults aus `src/` entfernen —
  Default-Roster in `game_state.py`, `faction_dir`-Default in `loader.py`, Spielerlabels
  in `gameHeader.py`/`gameProtocoll.py`, Caption in `setupScreen.py`. Ziel: Allowlist leeren.
- **Generic-src Vokabular (INV-4b DEBT, S51; `protocol` erledigt S52):** datengetriebenes
  Gate (`test_generic_src_vocab.py`) listet Fraktions-Eigennamen in `src/`. ✅ **S52:**
  `protocol`/`protocols` faktion-neutral als `round_choice` umbenannt (Klasse
  `RoundChoiceAbility`, Session-Keys `round_choice_*`, Datei `round_choice_ability.py`),
  Ledger-Einträge entfernt; Reste LEGIT (`typing.Protocol` in `phase_handler`) bzw. zur
  `reanimation`-Schuld (`reanimationProtocols`). Verbleibend: benannte Items (`orb`, `overlord`,
  `phaeron`, `irongob`, `gloom`, `prism`, `dakka`, `klaw`, `tesla`, `reanimation`, `arkana`,
  `dynasty`) aus Phasen-/Render-Modulen in YAML/Daten ziehen. Ziel: Ledger schrumpfen (Ratchet).
- **Layer-Kopplung:** `gameMechanic/*Phase.py` importiert `uiLayout._common` (Render-Hub).
  Aufräum-Pfad: Phasen-Render nach `uiLayout/` ziehen (vgl. Audit-Plan 008). Bewusst (noch)
  nicht als Wächter erzwungen.
- **Test-Mock-Fragilität (S51 entdeckt):** Mehrere `src`-Module lesen das globale
  `st.session_state` und rufen einander auf (`unit_mutations.set_movement_status` →
  `game_state.units_key_for`; `ability_engine` → `game_state`/`unit_mutations`). Tests mocken
  `streamlit` **pro Datei**; wer ein Modul zuerst importiert, bindet dessen `st`. Reihenfolge-
  abhängig → leicht zerbrechlich (S51: ein neuer Test als erster Importer brach 15 Movement-Tests).
  Workaround: Akzeptanztest importiert `game_state` lazy. Saubere Lösung: **eine geteilte
  `streamlit`-Fixture** (conftest) + Tests auf `module.st` statt lokalem `_st_mock` umstellen.
  Tieferliegend ein Smell: viel globaler `session_state`-Zugriff quer durch die Logik-Module.

---

## 4b. Doku-Drift-Befunde (Abgleich 2026-06-15) — zur Klärung, nicht still ändern

`docs/spec/architecture.md` ist teils veraltet (Gesamtbild stimmt, Details nicht):

- **session_state-Schema** (architecture.md): nennt `unit_state` ohne `group_models`/`group_wounds`
  (per-Gruppe-Wunden, real in `game_state.py`); Armee ohne `dynasty`/`protocol_order` (real vorhanden);
  „Owned by `gameMechanic/state.py`" → Datei heißt `game_state.py`.
- **Colour System** (architecture.md §Colour): beschreibt `COLOR_*`-Aliase „als CSS in app.py" —
  das **Live-Theme** sind aber `--arb-*`-Variablen in `gameHeader.py`. Kanonisch ist
  [../spec/design_colors.md](../spec/design_colors.md); die `COLOR_*` (Tailwind-Extrakte in
  `constants/colors.py`) existieren noch, treiben das Theme aber nicht.
- **uiLayout „No game logic in this layer"** (architecture.md): widerlegt durch `_common.py`
  (Attack-Mathe wurde gerade deshalb nach `attack_math.py` ausgelagert) → siehe Layer-Kopplung (§4).
- **Refactoring Plan / Open Design Questions** (architecture.md): historisch, alle Phasen erledigt,
  viele Fragen beantwortet (Stratagems implementiert, CP-Werte bekannt) → als Historie kennzeichnen.

Vorschlag: architecture.md in einer eigenen kleinen Doku-Session aktualisieren (Schema +
Colour-Verweis auf design_colors.md + Historien-Markierung). **Vor Änderung freigeben.**

## 5. Größere geplante Ziele

- [ziel7.md](ziel7.md) — Crusade-Erweiterung (geplant)
- [ziel8.md](ziel8.md) — Wahapedia Faction Fetcher (geplant)
- [index.md](index.md) — Ziel-Gesamtübersicht 1–8

---

## Wo was steht (Artefakt-Verweise)

| Frage | Artefakt |
|---|---|
| Was mache ich als Nächstes? | [next_session.md](../../.claude/tasks/next_session.md) |
| Was ist insgesamt offen? | **dieser Index** |
| Detailplan eines Features? | [../audit/plans/](../audit/plans/) |
| Architektur-Bild + Invarianten? | [../spec/architecture.md](../spec/architecture.md) · [../spec/architecture_invariants.md](../spec/architecture_invariants.md) |
| Ziel-Historie / Changelog? | [ziel6.md](ziel6.md) „Session-Historie" |
