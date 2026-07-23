STATUS: NEEDS-APPROVAL

## Planning — 2026-07-23 (S180)

**Priorität:** P1 — S179 sauber committen, dann B-131-Nachbesserung (Stakeholder-Befund) fachlich landen.
**Scope:** Zwei Dreiklänge in einer Session: (A) S179-Abschluss inkl. B-129/B-130/B-131-Verifikations-Integration, (B) B-131-Nachbesserung (Kachel-Breite-Bug + namentliche Aura-Spender via neuem Accessor), (C) S180-Abschluss.

> **Zwei-Commit-Hinweis (Token):** S179-Code ist fertig+grün und muss zuerst committen (Block A, stehend freigegebener Dreiklang). B-131-Nachbesserung ist NEUER Code → eigener Freigabe-/Verifikations-Zyklus → eigener Commit (Block C). Gesamtschätzung ~95k liegt im Korridor, aber eng: **natürliche Sollbruchstelle nach Block-A-Commit** — reißt das Budget Richtung 120k, wird Block B/C in eine frische Session verschoben (briefing.md trägt den Stand).

---

### Block A — S179-Abschluss (Dreiklang stehend freigegeben, operating_model.md Ev.5)

| Aufgabe | Effort | Token | Modus | Subagent + Tier | Scope-Zeile / Dateien |
|---------|--------|-------|-------|-----------------|----------------------|
| **A0 (NEEDS-DECISION, früh):** `S177_retro.md` Marker klären — steht noch auf `NEEDS-DECISION` (nicht ANSWERED). Stakeholder entscheidet: angenommen+erledigt → löschen, oder offene Maßnahme → in S180-Retro ziehen. | XS | ~2k | Konsens | Koordinator | `docs/handoff/S177_retro.md` |
| **A1:** B-129 + B-130 Verifikation (positiv) integrieren: Log-Eintrag je Item in `ui_verification_log.md`, Handoffs `S179_B129`/`S179_B130` löschen, B-129/B-130-Zeilen inkl. Details → `backlog_archive.md` (aus `backlog.md`/`backlog_details.md` raus). | S | ~8k | Gate | Executor + Haiku | Doku-Aufräum-Brief (S158-M3-Satz); `docs/spec/ui_verification_log.md`, `docs/goals/backlog*.md`, `docs/handoff/` |
| **A2:** B-131 Verifikation (positiv MIT 2 Befunden) integrieren: Log-Eintrag „positiv, 2 Follow-ups" in `ui_verification_log.md`; die zwei Befunde als **B-131-Nachbesserung** in `backlog.md`/`_details.md` fixieren (Bug: Kachel-Breite; Anforderung: namentliche Spender-Liste + Accessor-Entscheid); Handoff `S179_B131` löschen (nach Grep-Pflicht S169-M1). | S | ~7k | Gate | Executor + Haiku | Doku-Aufräum-Brief; `docs/spec/ui_verification_log.md`, `docs/goals/backlog*.md`, `docs/handoff/` |
| **A3:** Restliche Handoff-Hygiene ZUERST (vor Vollsuite): `S178_retro`/`S178_B113` (angenommen+umgesetzt) löschen, `S179_planning` → ANSWERED + löschen. Grep-Pflicht je Datei (Voll- + Kurzname) über `docs/`+`src/`. `Stakeholder_Beobachtungen` (STANDING) bleibt. | XS | ~4k | Gate | Executor + Haiku | S169-M1-Satz; `docs/handoff/` |
| **A4:** **Vollsuite als LETZTER Schritt** (schließt B7/B-131 ein — letzte Suite lief davor): `pytest --tb=short` (Floor 99 %) + `tests/architecture/` + `tests/docs/`+`tests/acceptance/`. | S | ~5k | Gate | Koordinator | Messbefehle briefing.md §Gate-Netz |
| **A5:** Review S179 (DoD 7 Punkte, ganzheitlich). | M | ~10k | Konsent | Reviewer + Opus | ganzer S179-Diff |
| **A6:** Retro S179 → nummerierte, entscheidbare Maßnahmen-Liste. | S | ~6k | Konsens | Koordinator moderiert | — |
| **A7:** Commit „Close S179 …" (stehend freigegeben) + `python tools/token_report.py --write` + `python tools/rotate_history.py --session 179 --summary "…"`. | XS | ~4k | — | Koordinator | — |

---

### Block B — S180-Facharbeit: B-131-Nachbesserung (Freigabe-Gate: NEUER Code)

> Der Accessor-vs-generischer-Text-Entscheid ist **bereits gefallen** (Accessor nachrüsten — Stakeholder-Kommentar S179_B131). Das ist die Sach-Entscheidung, **keine Umsetzungs-Freigabe**: Block B startet erst nach Plan-Freigabe.

| Aufgabe | Effort | Token | Modus | Subagent + Tier | Scope-Zeile / Dateien |
|---------|--------|-------|-------|-----------------|----------------------|
| **B1:** B-131-Nachbesserung (**ein Brief, ≤ M**): (a) **Kachel-Breite-Bug** — `st.info` in `_render_wound_reroll_aura_hint` in eine halbbreite `st.columns(2)`-Linksspalte fassen (design_system.md §1.9.1 Breiten-Regel Baustein ③, Vorbild `rp_col`), damit der Hinweis nur die Player-Area statt der vollen gameActionArea belegt. (b) **Namentliche Spender-Liste** — neuer öffentlicher Accessor in `abilityEngine.py` (analog `get_unit_rp_reroll_ability`), der die **lebenden** Aura-Spender-Einheiten liefert (aus den `reroll_wound_1`-Kandidaten + `_aura_source_alive`); `ResolutionContext` bekommt statt/zusätzlich zum `bool` die Spender-Namensliste; `_wound_reroll_aura_hints` baut den Text „…within 6\" of [name1], [name2] or [nameN]." aus `unit.name_en`. Zerstörter Spender → fällt aus der Liste (bestehendes `_aura_source_alive`-Gating). 4 Tests erweitern/ergänzen (Namensliste 1/mehrere/leer, Breite). | M | ~22k | Gate | Executor + Sonnet | `Scope-Tabelle` Z.17 (`_common.py`, `gameActionsArea.py`) **+** Z.19 (`abilityEngine.py`, `ability.py`); `tests/uiLayout/test_common.py`, `tests/gameMechanic/test_ability_engine.py` |

**⚠ INV-4b (PFLICHT im Brief):** Spender-Namen NUR aus `unit.name_en` (YAML-Prosafeld, scanner-ausgenommen) — **nie** ein Eigenname als String-Literal in `src/` (das war exakt der S179-Grund für den generischen Text). Nach dem Step `pytest tests/architecture/ --no-cov -q` grün belegen.

**UI-Verifikations-Roster (verifiziert):** `necrons_test.yaml` enthält `skorpekh_lord` (Aura-Spender) + `skorpekh_destroyers` (Empfänger) → Einzel-Spender-Fall + Gegenprobe (Lord zerstört → Name verschwindet) im Browser prüfbar. **Mehr-Spender-Fall** („[a], [b] or [c]") ist im Browser mit `necrons_test.yaml` nicht darstellbar (nur 1 Lord) → durch Unit-Test abgedeckt; optional zweiten Destroyer-Lord in ein Testroster aufnehmen, sonst als „nur unit-getestet" markieren. `necrons_alpha/beta/1500pts` enthalten ebenfalls Lokhust-/Skorpekh-Lords.

---

### Block C — S180-Abschluss (eigener Dreiklang)

| Aufgabe | Effort | Token | Modus | Subagent + Tier | Scope-Zeile / Dateien |
|---------|--------|-------|-------|-----------------|----------------------|
| **C1:** UI-Verifikations-Handoff `S180_B131b_ui_verifikation.md` anlegen (Klickpfad: Kachel jetzt halbbreit in Player-Area; Hinweis listet „Skorpekh Lord" namentlich; Lord zerstört → verschwindet). Backlog/briefing nachziehen. B-131 bleibt offen bis Browser-Verifikation (Teil-Status). | XS | ~4k | Gate | Executor + Haiku | S155-Satz; `docs/handoff/`, `docs/goals/backlog*.md` |
| **C2:** **Vollsuite als LETZTER Schritt** (schließt B1 ein). | S | ~4k | Gate | Koordinator | Gate-Netz |
| **C3:** Review S180-Nachbesserung (DoD, Fokus INV-4b + §1.9.1-Breite). | M | ~9k | Konsent | Reviewer + Opus | B1-Diff |
| **C4:** Retro S180 → Maßnahmen-Liste; **Backlog-Umsortierung (S155):** offene Zeilen so ordnen, dass B-128 / B-028c3–c5 / B-005 in nächster Bearbeitungsreihenfolge oben stehen. Commit „Close S180 …" (stehend freigegeben) + `token_report --write` + `rotate_history --session 180`. | S | ~8k | Konsens | Koordinator | `docs/goals/backlog.md` |

---

**Nächster Backlog-Rang nach B-131** (falls Budget nach Block A doch reicht statt Block B/C ganz): B-128 (Design-System-Ratchet-Rest, DoR ok, ~15–20k) — bewusst NICHT zusätzlich eingeplant, da zwei Dreiklänge das Budget bereits füllen; B-028c3/c4/c5 + B-005 bleiben Folge-Sessions.

**Nächster Schritt:** Nach Freigabe → Block A0 (S177-Marker-Entscheid) + A1/A2 Verifikations-Integration (Haiku parallel).
**Offene Entscheidungen (NEEDS-DECISION):**
1. **A0:** `S177_retro.md` steht noch auf `NEEDS-DECISION` — angenommen+löschen oder offene Maßnahme in S180-Retro übernehmen? - Kann gelöshct werden.
2. **Block B/C-Timing:** Zwei Dreiklänge in einer Session freigeben, oder nach Block-A-Commit natürliche Sollbruchstelle nutzen und B-131-Nachbesserung in frische Session? Das hängt vom Session-Kontextfenster ab. Wenn Platz ist, los geht's. Soferne es unabhängige Items gibt, bitte immer parallel arbeiten. Ich verstehe bis heute nicht, warum das nicht schon ein gängiges Prinzip ist. 
