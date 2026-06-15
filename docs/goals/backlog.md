# Backlog — zentraler Index

> **Ein Ort für „was ist offen".** Dieser Index führt die bisher verstreuten Quellen
> zusammen (Executor-Pläne, offene Tasks, manuelle Verifikation, Architektur-Schulden).
> **Details bleiben in den verlinkten Artefakten** — hier wird nicht dupliziert, nur verwiesen.
>
> Pflege: Wird ein Punkt erledigt, hier abhaken **und** in der Detailquelle. Neue Arbeit
> entweder als Plan in [../audit/plans/](../audit/plans/) oder als Task-Zeile hier.

Letzter Abgleich: 2026-06-15

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
- **Layer-Kopplung:** `gameMechanic/*Phase.py` importiert `uiLayout._common` (Render-Hub).
  Aufräum-Pfad: Phasen-Render nach `uiLayout/` ziehen (vgl. Audit-Plan 008). Bewusst (noch)
  nicht als Wächter erzwungen.

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
