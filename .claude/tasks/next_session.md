# Startprompt — Nächste Session
<!-- Kanonisch: .claude/tasks/next_session.md — nie ins Root-Verzeichnis anlegen. -->

## ⚠️ Session-Regeln (immer beachten)

**Zu Beginn jeder Session lesen:**
- `CLAUDE.md` — Workflow, Freigabe-Pflicht, **Unklarheiten IMMER zuerst fragen**
- `docs/goals/ziel6.md` — Aufgabenliste, Checkboxen, **Session-Historie (Changelog)**

**Am Ende jeder Session:**
- Checkboxen in `docs/goals/ziel6.md` abhaken + eine Zeile in die Session-Historie ergänzen
- Diese Datei aktualisieren: Stand + nächster Schritt (ZUERST lesen, dann ergänzen)

> Die vollständige Session-Historie (S28–S45 + Audit-Queue) liegt jetzt in
> `docs/goals/ziel6.md ## Session-Historie` — hier nur noch der aktuelle Stand.

---

## Was ist Arbiter?

Digitaler Spielbegleiter für Warhammer 40.000 9. Edition, Streamlit (Python).
Start: `streamlit run src/app.py` (Port 8501). Branch `dev` (Entwicklung), `main` (nur per PR).

---

## Aktueller Stand (nach S45, 2026-06-13 — 790 Tests grün, 90 % Coverage)

- Ziel 1–5 vollständig; Ziel 6a–6n + Audit-Pläne 001–013 abgeschlossen (Details: ziel6.md).
- Plan 013 (einheitlicher Gruppen-Flow) live; B1–B5 post-013-Bugs gefixt (Commit `46e03f8`).
- **S45: Findings F1–F8 vollständig gegen Code/Daten/Regeln verifiziert** (Ergebnis unten).

---

## Verifizierte Analyse F1–F8 (S45 — korrigiert die alte Doku)

> Geprüft gegen `_common.py`, `dice_html.py`, `ability_engine.py`, Ork-/Necron-YAML,
> `movementPhase.py` und die Core Rules. Mehrere alte F-Befunde waren ungenau.

### WAAAGH (F2 / F4 / F8) — Sichtbarkeit ist da, Architektur fehlt

- **F8 war falsch.** `+1 Strength` wird als blau umrandete S-Badge gerendert
  (`dice_html.py:300`), `str_bonus` korrekt **nach** `_parse_strength` addiert (`_common.py:687`).
  Der WAAAGH-Invuln ist verdrahtet: `ability_invuln_save` → `resolve_save` → eigene „Inv N+"-Zeile
  (`_common.py:748`, `dice_html.py:381`). **Keine UI-Arbeit nötig.**
- **F2 (echter Bug):** `model_groups` tragen keine eigenen Stats. Budget = `alive × (atk_unit.attacks + atk_bonus)`
  (`_common.py:1134/1193`). Boss Nob (real A=3) erbt Boyz `attacks: 2` → mit WAAAGH 3 statt 4
  → „4. Attacke nicht auf Power Klaw legbar".
- **F4 = vermutlich gleicher Root Cause wie F2.** `buff_stat_bonus` matcht `ORK` (Warbikers haben es),
  der +1 greift. **Offene Restfrage:** Bleibt `activated_abilities` über den Zugwechsel hinaus
  erhalten (Invuln „bis Beginn deines nächsten Zuges" im Verteidigerpfad)? → reproduzieren.

### Cover (F1 / F3 / F5)

- Cover wird einmal **oberhalb der Tabs** gerendert (`_common.py:1346`), im Tab unterdrückt.
- **F1/F3 = Layout-Entscheidung getroffen → Option B:** Dense in HIT-Block, Light/Heavy in SAVE-Block.
- **F5 vermutlich kein Bug:** Key-Konsistenz stimmt (`rsplit`); Heavy-Cover-Checkbox erscheint nur
  wenn Verteidiger **nicht selbst gechargt** hat (`_common.py:1358`) = regelkonform. Erst reproduzieren.

### Skorpekh (F6) — Doku-Annahme ungenau

- Einheit **hat** `model_groups` mit `reap_blade_swap`, `limit: per_3` (`necrons/units.yaml:244`),
  aber als **optionaler** Swap. Datasheet verlangt **feste Komposition** (1 Reap-Blade je 3 Modelle).
  → Fix: fester Sub-Gruppen-Split (analog Boss Nob) + Roster prüfen. `src/` unberührt.

### Veil of Darkness (F7) — Root Cause korrekt, Flag-Name falsch

- Flag heißt `movement_locked` (nicht `veil_moved`). Teleport-Confirm setzt `moved`+`movement_locked`
  (`movementPhase.py:223`), **cleart `in_melee` nicht** → „MOVED"+„IN MELEE" gleichzeitig.
  → Fix: `in_melee=False` für Träger + optionale CORE-Einheit beim Confirm; im `_undo_teleport` zurück.

---

## Freigegebener Plan (S45) — Reihenfolge: Doku-Cleanup ✅, dann Findings

**Entscheidungen des Nutzers:**
- Cover-Layout: **Option B** (Cover in die jeweiligen Blöcke einbetten)
- Per-Gruppe-Stats: **volles Override-Schema** (`attacks`/`strength`/`wounds`/`ws`/`bs`)
- Reihenfolge: erst Doku-Cleanup (erledigt), dann Findings, dann Roster-Audit

**Block A — Per-Gruppe-Statarchitektur (F2 + F4, datengetrieben):**
- `orks/units.yaml` + `necrons/units.yaml`: optionales `stats:` pro `model_group` (Boss Nob `attacks: 3`)
- `gameObjects/unit.py`: `ModelGroupSpec`/`ModelGroup` um Stat-Overrides erweitern
- `gameObjects/loader.py`: Stats parsen, Fallback auf Unit-Stat
- `uiLayout/_common.py`: Budget + Wound-Block lesen `group.attacks ?? atk_unit.attacks` (analog Strength)
- Tests: Boss Nob A=3 (+WAAAGH=4); homogener Fallback

**Block B — WAAAGH-Persistenz (F4-Rest):** reproduzieren ob `activated_abilities` über Zugwechsel bleibt; nur fixen falls reproduzierbar.

**Block C — Veil of Darkness (F7):** `movementPhase.py` Teleport-Confirm + `_undo_teleport` `in_melee` clearen; Regressionstest.

**Block D — Skorpekh feste Komposition (F6):** `necrons/units.yaml` Reap-Blade-Swap → fester Sub-Gruppen-Split; Roster prüfen.

**Block E — Cover-Layout Option B (F1/F3):** Refactoring `_render_resolution_tab` — Dense in HIT-, Light/Heavy in SAVE-Block; F5 vorab reproduzieren.

**Danach — Roster-Audit:** alle 6 Rosters in `data/rosters/` gegen Datasheets prüfen (Modellzahl, Pflicht-/Wahlwaffen, Komposition); Abweichungsliste vor Änderung vorlegen; nur YAML, `src/` unberührt.

---

## Plan-Queue (Executor) — nach den Findings

| Plan | Titel | Prio | Status |
|------|-------|------|--------|
| 014 | P17: Verteidiger-Korrektur Schadenszuweisung (±-Counter pro Gruppe, Snapshot, Waffen-Wegfall) | HOCH | TODO |
| 015 | Reaktive Stratagems: Overwatch, Counter-Offensive, HI-Hook, once_per_battle | MITTEL | TODO |
| 016 | Protokoll-Effekte auf RP (`rp_reroll`/`rp_bonus`) + Dynastiebonus-Anzeige | MITTEL | TODO |
| 017 | SAVE-Block: Fähigkeits-AP kombinierte Badge (`ap_modifier`-Schema) | MITTEL | TODO |
| 018 | Kleinkram: CP-Doppelvergabe (Bug!), Battle-Log-Reset, Gretchin Cowardly, Modifier-Konsolidierung | NIEDRIG | TODO |

Empfohlene Reihenfolge: **014 → 016 → 018 → 015 → 017** (Begründung in `docs/audit/plans/README.md`).
Pläne 014/015 enthalten **Mockup-Stopps** — UI-Layout erst vorlegen, dann implementieren.

---

## Offene Tasks (Backlog, nach Prio)

### 🟡 MITTEL — GOs in gameActionArea
- GO-Buttons kontextuell in gameActionArea (aktiver + inaktiver Spieler), nicht als Liste
- Overwatch (Charge Phase) + Counter-Offensive (Fight Phase) als reaktive GOs
- GOs die Non-CHARACTER-HI erlauben (`enslaved_protectors`) → HI-Eligibility erweiterbar

### 🟡 MITTEL — Necron Command Phase
- Protokoll-Effekte auf Living Metal / RP-Verbesserungen
- Dynastiebonus anzeigen wenn Direktive durch Dynastiezugehörigkeit gilt
- Regelkasten immer ganz oben (alle Phasen prüfen)

### 🟡 MITTEL — SAVE-Block
- Fähigkeit + AP kombiniert als eine Badge (`Enslaved AP-1`) — erfordert YAML-Erweiterung (6j/6l)

### 🟢 NIEDRIG
- Gretchin Cowardly: −1 Attrition wenn kein RUNTHERD in 6" (Ld 4)
- Nach Reset keine alten Einträge im Battle Log (6g)
- CP-Doppelvergabe-Fix + `collect_modifiers_for_phase()` (6e)

---

## Wichtige Constraints (unveränderlich)

- **Freigabe vor Umsetzung** — Plan + Dateiliste zeigen, auf „ja" warten
- **Planergänzung ≠ Freigabe** — Plan neu zeigen, nochmal warten
- **Kein Memory/Subagent/Skill ohne Freigabe**
- dev-Branch, kein direktes Committen auf main
- Seitenleisten: `first_player` links, `second_player` rechts (unveränderlich)
- Keywords immer `UPPERCASE` in YAML
- `_parse_strength(raw: int|str, unit_strength)` für Waffenstärke — akzeptiert native YAML-Typen;
  nie `int(strength)`/`str(strength)` direkt. `User×N`/`User+N`/`User-N` werden akzeptiert.
- Weapon strength in YAML: plain int = fest, `"+N"` = User+N, `"×N"` = User×N, `"User"` = User
- Regelreferenz: Immer erst lokal (`docs/work/wahapedia_*/`), nie Nutzer fragen
- **Generisch:** keine Fraktions-Checks in `src/` — alle Fraktions-Entscheidungen über YAML

---

## Architekturmuster

### ModelGroup-Pattern (6m)

Einheiten mit strukturell verschiedenen Modellen (z.B. Boyz: 9 Boys + 1 Boss Nob) via `model_groups`
in `units.yaml`. Drei Typen:
- **Homogen:** synthetische Einzelgruppe im Loader (Plan 013)
- **Strukturell gemischt:** `count: 1` / `count: remainder`; Roster-Swap aufgelöst
- **Per-Model:** `scope: per_model`; Loader splittet in Sub-Gruppen

State: `unit_state["group_models"]: dict[str,int]`; `models` = Summe. Tod: `apply_damage()` reduziert
nach `priority` (1 = stirbt zuerst). UI: subUnitCard pro Gruppe, Gruppe-für-Gruppe-Deklaration.
**Offen (Block A):** per-Gruppe-Stat-Overrides (`attacks`/`strength`/`wounds`/`ws`/`bs`).

### Reset-Button-Pattern für Fähigkeits-gesetzte Zustände

Setzt eine Fähigkeit/ein Relikt einen Zustand (z.B. `turn_flags`), MUSS es eine Undo-Möglichkeit
geben solange der Zug läuft:
- `turn_flags["<ability>_locked"] = True` beim Aktivieren (Unterscheidung zu normalem Zug)
- Phase-UI: bei `_locked` Buttons deaktivieren + Undo-Button zeigen
- Undo löscht `_locked` und setzt betroffene Felder zurück
- Nach Zugwechsel (`reset_turn_flags`): `_locked`-Flags weg → State „fest"
- Beispiel: Veil of Darkness (`movement_locked`) in `movementPhase.py`

---

## Regelerkenntnisse (nicht-offensichtlich)

- **WAAAGH! Stage 1:** Nur ORKS CORE/CHARACTER dürfen nach Advance chargen; +1 S/+1 A für ALLE ORKS.
  Aktivierung erfordert WARBOSS-WARLORD (App prüft pragmatisch nur WARBOSS-Keyword).
- **Cover:** Dense (−1 Hit) + Light (+1 Save) NUR Shooting; Heavy (+1 Save) NUR Melee, außer der
  Verteidiger hat selbst gechargt.
- **Veil of Darkness:** „remove & set up 9"+ weg" — laut RAW auch aus Engagement Range nutzbar;
  danach `in_melee` clearen (F7).
- **Resurrection Orb / RP:** keine KERN-Einschränkung; gilt für `<DYNASTY>`-Einheiten. RP-Gate über
  `unit.rules` (nicht `keywords`).
- **FNP:** gilt für normale UND tödliche Wunden; pro Wunde nur eine Ignore-Regel.
- **Fight Phase:** startet mit **inaktivem** Spieler; CHARGED zuerst, dann abwechselnd.
- **Heroic Intervention:** Schritt 2 der Charge Phase, nur CHARACTER, ≤3", näher zum Feind enden.
- **extra_attacks — zwei Klassen:** „+N additional" → `unit.attacks + N`; „+N AND no more than N"
  → fester Cap N (`max_attacks`): attack_squig (2), squighog_jaws (2), squigosaur's_jaws (3),
  grabbin_klaw (1), wreckin_ball (1), butcha_boyz (4), savage_horns_and_hooves (4).
- **Boss-Nob-Waffen:** nur der Boss Nob trägt Spezialwaffen (power klaw, big choppa, killsaw) — bei
  boyz, warbikers, stormboyz, kommandos. Nobz/meganobz/squighog: alle Modelle gleich.
- **Skorpekh Destroyers:** feste Komposition 1 Reap-Blade je 3 Modelle (Rest Threshers) — kein Wahl-Wargear (F6).
