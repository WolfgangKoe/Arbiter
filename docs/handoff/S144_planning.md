STATUS: ANSWERED

# S144 Planning-Entwurf

## Stakeholder-Antworten (2026-07-12)

1. **FixD-Plan: FREIGEGEBEN** — Aufgabe 9 (Brief 1) darf bei Kapazität laufen.
2. **Ork-Vigilus-Stratagems: ENTFERNEN** — Aufgabe 6 ist beauftragt (analog Necron-Kodex-Filter).
3. **Klan-/Dynastie-Fähigkeiten: NUR KONZEPT** (Aufgabe 7); Umsetzung als eigener Plan ab S145.
4. **Plan insgesamt: FREIGEGEBEN** — Reihenfolge 3 → 4+5 → 6 → 7 → 8 → 9 wie vorgeschlagen.

## Ausgangslage

Ziel 7 (Gefechtsoptionen + subfaction-Mechanik) bleibt aktives Ziel. Stufe A ist
verifiziert erledigt (alle 6 referenzierten Commits in der Historie bestätigt:
`f9279fe`, `8c124c3`, `396fdec`, `b5c774b`, `2e3aa98`, `464bb40` — kein stale Check).
Stufe B (Necrons) ist bis auf die finale manuelle UI-Verifikation erledigt; Stufe C
(Orks) wartet laut Ziel-Reihenfolge weiter auf Stufe B. S143 endete mit einem
Wind-down ohne Review/Retro und drei ANSWERED-Konzepten, die jetzt zur Umsetzung
anstehen. Branch bleibt `feature/016-protocol-rp-effects` — das ist die seit S123
gelebte Praxis (in `next_session.md` explizit dokumentiert) und **kein neuer
Befund**, steht aber weiterhin im Widerspruch zu `CLAUDE.md` §Projekt-Kontext
(„Branch: dev (aktiv)") — reiner Doku-Drift-Hinweis, keine Handlungsempfehlung
für diese Session.

## Befunde

**Checkbox-Sync (`ziel7.md`):** Alle gesetzten Haken in Stufe A + Stufe B
gegen `git log --oneline --all` verifiziert — sämtliche referenzierten Commit-Hashes
existieren. **Kein stale Check gefunden.** Offene Boxen (Stufe B manuelle
UI-Verifikation, Stufe C komplett) sind korrekt als offen markiert.

**Handoff-Marker:** Alle sechs S143-Dateien in `docs/handoff/` tragen bereits
`STATUS: ANSWERED` (`S143_planning.md`, `S143_abilityengine_refactor.md`,
`S143_on_target_anker_konzept.md`, `S143_stratagem_kodex_abgleich.md`,
`S142_planning.md`, `S141_*`). Keine offenen `NEEDS-DECISION`-Marker vorgefunden —
die drei Konzepte enthalten aber je eine **bereits getroffene** Stakeholder-Antwort,
die diese Session nur noch umsetzen muss (s. Tabelle unten). `S141_ui_befunde_group_a.md`
bleibt laut eigenem Status bewusst offen, bis Befund 3 (FixD) UND Befund 5 (FixC)
erledigt sind — noch nicht löschen.

**`docs/audit/plans/README.md`:** `S142-FixD` (Resolution-Tabs, P1 HOCH, 3
Teil-Briefe M+M+S) steht als **„WARTET AUF FREIGABE"** — der Plan selbst ist noch
nicht final freigegeben, obwohl er inhaltlich detailliert vorliegt. Das ist eine
frühe Entscheidungsfrage (s. u.), kein stiller Blocker.

**`Stakeholder_Beobachtungen.md`:** Keine neuen unbearbeiteten Beobachtungen —
alle fünf Einträge im Eingang sind bereits mit einem Verweis auf ihr Zielartefakt
versehen (B7/B8/B14/B13/Backlog §2 Paket 6), nichts zusätzlich zu überführen.

**Neuer Planungsgegenstand (S143-Nachtrag, s. `next_session.md`):** Klan-Affinität
als Verifikationspunkt ist gestrichen (existiert regelseitig nicht). Stattdessen
fehlen **Ork Klan-Kultur-Fähigkeiten** und **Necron-Dynastic-Code-Fähigkeiten** als
eigenständiges Feature — geprüft: `orks/faction_abilities.yaml` und
`necrons/faction_abilities.yaml` haben zwar bereits `subfaction_field`/
`subfaction_affinity` für die **Command-Protocol-Rundenwahl**, aber keine
eigenständigen **passiven** Fähigkeiten pro Dynastie/Klan (im echten 9E-Regelwerk
zwei getrennte Mechaniken: Command Protocols rotieren pro Runde, Dynastic
Code/Klan Kultur ist ein fixer Passiv-Bonus, der mit der Listenerstellung feststeht).
Kein `klan`-Schlüssel in den meisten Rostern außer `orks_transport.yaml`/`orks_test.yaml`/
`orks.yaml`; keine Wahapedia-Rohtexte lokal für Dynastic Codes/Klan Kulturs vorhanden
(nur die bereits verarbeiteten `faction_abilities.yaml`-Einträge). Braucht **Recherche +
Konzept mit Grundannahmen-Block**, bevor implementiert wird — zu groß und zu
unscharf für einen direkten Executor-Auftrag.

## Priorisierte Aufgabenliste (S144)

| # | Aufgabe | Effort | Token-Schätzung | Modus | Subagent(en) + Tier | Scope-Zeile / Dateien |
|---|---------|--------|-----------------|-------|---------------------|------------------------|
| 1 | **Entscheidung: FixD-Plan freigeben?** — Plan liegt vollständig vor (`S142_fixD_resolution_tabs.md`), Status „WARTET AUF FREIGABE". Ohne Freigabe bleiben Aufgaben 7/9 blockiert. | XS | ~1k (nur Rückfrage, kein Subagent) | Gate | — (Koordinator fragt direkt) | `docs/audit/plans/S142_fixD_resolution_tabs.md` |
| 2 | **Entscheidung: Ork-Vigilus-Scope** — 8 Stratagems (Blitz Brigade/Dread Waaagh!/Kult of Speed/Stompa Mob + Folge-Stratagems) sind Vigilus-Defiant-Kampagnenbuch, nicht Codex: Orks. Gilt der Necron-Kodex-Filter analog für Orks (entfernen) oder zählen Specialist-Detachments als „kodex-integriert" (behalten)? | XS | ~1k (nur Rückfrage) | Konsens | — (Koordinator fragt direkt) | `docs/handoff/S143_stratagem_kodex_abgleich.md` §Orks |
| 3 | **Review + Retro S143 nachholen** — regulär am Session-Ende S143 durch Wind-down entfallen (analog S142-Nachholung). DoD-Review über S143-Diff (Wound/Hit-Cap-Fix, Morale-Selektion-Fix, `is_unit_scoped_effect`, Roster-Loader-Test) + Retro-Maßnahmenliste. | M | ~45k | Gate (Ergebnis dem Stakeholder vorlegen) | Reviewer, **Opus** (DoD-Review, Ganzheitlichkeit — Begründung: Opus-Standardtier für Reviews laut operating_model.md) | `Scope-Tabelle` — Review liest Diff seit `3a191e8`, `tests/`, `docs/spec/` |
| 4 | **Necron-Stratagem-Datenpflege: 16 White-Dwarf-Supplement-Einträge entfernen** (Cult of the Cryptek 8 + Annihilation Legion 8, laut ANSWERED-Liste in `S143_stratagem_kodex_abgleich.md`). Header-Kommentar (Total-Zahl, EXCLUDED-Block) nachziehen; keine Test-Referenzen betroffen (grep-verifiziert: 0 Treffer in `tests/`). | S | ~12k | Konsent | Executor, **Sonnet** (mechanische Datenpflege, Format vorgegeben) | `data/wh40k_9e/necrons/stratagems.yaml`; optional `docs/spec/acceptance/rules.md` falls Ledger-Zeilen existieren (prüfen) |
| 5 | **mypy-Ratchet gameMechanic: Option A + B** (freigegeben in `S143_abilityengine_refactor.md`). A: bare `dict`/`list[dict]` → `dict[str, Any]` in `abilityEngine.py` (Z. 89,98,131,156,171,318,408,419,270) + `stratagemEngine.py:134`, `# type: ignore[type-arg]` entfernen — löst 4 von 11 Fehlern. B: gemeinsamer Accumulate-Helfer (`_sum_effect_value` o. ä.) mit `combine`-Parameter (Pflicht wegen `ability_invuln_save`s `min`-Sonderfall) für 6 Call-Sites inkl. `stratagemEngine.stratagem_strength_bonus`; je Call-Site Regressionstest gegen den Helfer. | S | ~25k | Konsent | Executor, **Sonnet** (mechanischer Typ-/Extract-Refactor, Risiko laut Konzept „niedrig-mittel") | `Scope-Tabelle` Z. 21/24 — `src/gameMechanic/abilityEngine.py`, `src/gameMechanic/stratagemEngine.py`, `tests/gameMechanic/test_ability_engine.py` |
| 6 | **Ork-Vigilus-Stratagems entfernen** (nur falls Aufgabe 2 = „entfernen" entschieden wird) — 8 Einträge analog Aufgabe 4. | S | ~10k | Konsent | Executor, **Sonnet** | `data/wh40k_9e/orks/stratagems.yaml` |
| 7 | **Klan-/Dynastie-Fähigkeiten — Recherche + Konzept (Grundannahmen-Block Pflicht)**: Wahapedia-Wortlaut für Ork Klan Kulturs (7 Klans) und Necron Dynastic Codes (6 Dynastien) beschaffen (WebFetch, da lokal keine Rohtexte vorhanden — **Subagent macht den Fetch, nie das Hauptfenster**, ADR-0004), gegen bestehendes `subfaction_affinity`-Schema (Command Protocols) abgrenzen, Datenschema-Vorschlag (neuer `ability_type` z. B. `subfaction_passive`, generisch, kein Fraktionscode in `src/`) + Aufwandsschätzung je Fraktion. Kein Code, nur Konzept-Datei mit Grundannahmen + Entscheidungsfragen. | S–M | ~30k | Gate (Konzept dem Stakeholder vorlegen, Grundannahmen bestätigungspflichtig) | Planner/Recherche, **Sonnet** (Recherche + Strukturvorschlag, kein reiner Lookup mehr Begründung für >Haiku) | `docs/goals/ziel7.md`, `data/wh40k_9e/orks/faction_abilities.yaml`, `data/wh40k_9e/necrons/faction_abilities.yaml`, `docs/spec/faction_abilities.md`; WebFetch `wahapedia.ru/wh40k9ed/factions/orks/` + `.../necrons/` |
| 8 | **on_target-Anker Option A umsetzen** (freigegeben in `S143_on_target_anker_konzept.md`): neuer `render_reactive_stratagem_box(def_faction, phase, event="on_target", …)`-Aufruf in `render_group_assignment` (Schleife über `tgts`, `_common.py:~2506`), inkl. Verschwinde-Regel bei Ziel-Toggle (Karte nur sichtbar, solange `def_uid` in `group_targets[gid]` steht — JEDES Rerun neu geprüft). Kollisionsfrei mit FixD (andere Funktion). | S–M | ~28k | Konsent | Executor, **Sonnet** | `Scope-Tabelle` Z. 17 — `src/uiLayout/_common.py`, `tests/uiLayout/test_common.py` |
| 9 | **FixD Brief 1** (Compute/Render-Trennung ohne Layout-Änderung) — NUR falls Aufgabe 1 = Freigabe erteilt. Reiner Struktur-Refactor in `_common.py`, kein Verhaltens-/Layout-Change; 6-8 neue Tests für extrahierte Compute-Funktion. | M | ~35k | Gate (Plan-Freigabe Voraussetzung) | Executor, **Sonnet** | `S142_fixD_resolution_tabs.md` §Brief 1 — `src/uiLayout/_common.py` |
| 10 | **mypy-Ratchet uiLayout (17 Fehler)** — NICHT parallel zu Aufgabe 9 (beide ändern `_common.py`); erst nach FixD Brief 1–3 oder in einer separaten Session-Welle ohne FixD einplanen. | M | ~30k | Konsent | Executor, **Sonnet** | `src/uiLayout/` (laut mypy-Fehlerliste), `tools/mypy_gate.py` |

**Reihenfolge-Empfehlung:** 1 + 2 (Entscheidungen, XS, sofort) → 3 (Review/Retro,
danach erst neue Arbeit) → 4 + 5 (kleine, unabhängige Datenpflege/Refactor-Tasks,
parallelisierbar da unterschiedliche Dateien) → 6 (falls 2 = entfernen) → 7
(Konzept, danach eigener Freigabe-Zyklus) → 8 (unabhängig von FixD) → 9 (nur bei
Freigabe 1) → 10 (separat von 9 halten).

**Korridor-Hinweis:** Aufgaben 1–6 zusammen liegen bei ~95k Token (inkl. Review),
passen in eine Session-Hälfte. Aufgaben 7–10 zusammen weitere ~120k — eher **nicht
alle in derselben Session** wie 1–6; Windown-Schwelle (~120k) im Auge behalten und
nach Aufgabe 6 zwischenbilanzieren, ob 7/8 noch reinpassen oder auf S145 verschoben
werden.

## Offene Entscheidungsfragen an den Stakeholder

1. **FixD-Plan freigeben?** (`docs/audit/plans/S142_fixD_resolution_tabs.md`) —
   Status seit S142 „WARTET AUF FREIGABE". Ja/Nein/Änderungswunsch nötig, bevor
   Aufgabe 9 (Brief 1) starten kann.
2. **Ork-Vigilus-Stratagems:** entfernen (analog Necron-Kodex-Filter) oder
   behalten (Specialist-Detachments zählen als kodex-integriert)? Betrifft 8
   Einträge in `orks/stratagems.yaml` (Blitz Brigade/Dread Waaagh!/Kult of
   Speed/Stompa Mob + Folge-Stratagems).
3. **Klan-/Dynastie-Fähigkeiten — Scope für S144:** Reicht ein reines
   Recherche-Konzept (Aufgabe 7) diese Session, oder soll direkt eine Fraktion
   (vermutlich Orks, da Ziel7 Stufe C ohnehin ansteht) bis zur Umsetzung
   getrieben werden? Empfehlung: Konzept zuerst (Grundannahmen bestätigen),
   Umsetzung als eigener Plan in S145+.
