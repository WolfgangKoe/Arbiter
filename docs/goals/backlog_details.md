# Backlog — Details

> **Zweck:** Diese Datei trägt die ausführliche Begründung/Herkunft je Backlog-Item, damit
> [backlog.md](backlog.md) eine schlanke Ein-Zeile-pro-Item-Liste bleiben kann. Jeder Abschnitt
> ist über die ID verlinkt (`backlog.md` verweist per Anker hierher) — Änderungen an einem Item
> immer hier vornehmen, `backlog.md` nur die Kurzzeile pflegen.

## Feldschema (Template)

Jedes Item trägt genau diese acht Felder, in dieser Reihenfolge:

- **Herkunft:** Session/Anlass/Foto-Referenz, aus der das Item entstand.
- **Typ:** `Schuldabbau` | `Fachlichkeit (Ziel 7)` | `Prozess/Doku`.
- **Belege/Recherche:** Links auf Handoffs/Screenshots/Specs — verweist, dupliziert nicht.
- **Betroffene Dateien:** Konkrete Pfade, falls bekannt; sonst `—`.
- **Abhängigkeiten (Begründung):** Was blockiert/parallelisiert dieses Item und warum.
- **Agent/Tier:** Rolle + Modell-Tier (Haiku-Default bei reinem Lookup, Sonnet sonst, Opus nur
  mit Begründung).
- **Benötigte Regeln/Scopes:** Verweis auf `operating_model.md`/`agent_scopes.md`, nur wenn bekannt.
- **Detail:** Der bisherige, aus der Alt-`backlog.md` übernommene Beschreibungstext (verlustfrei
  kondensiert — Fakten, Links, Entscheide, Code-Referenzen bleiben erhalten).

Unbekannte Felder tragen `—` (kein Platzhaltertext). Items B-092…B-097 sind die im Inventar
(`docs/handoff/S151_backlog_inventar.md`, Tabelle 3) als UNKLAR markierten Fälle — Status
`Blocked`, Detail-Feld trägt den Stale-Verdacht + Beleg + Klärungs-Vermerk.

---

## B-001 — FixD Brief 2 und 3 Compute Render Folge

**Herkunft:** Prio-Rang 5 (S145-Prioritätenliste), Folge von Rang 4 (Brief 1, erledigt S150).
**Typ:** Schuldabbau
**Belege/Recherche:** `docs/audit/plans/README.md` (Plan-Status), Prioritätenliste-Herleitung in Alt-`backlog.md` Z.23–33.
**Betroffene Dateien:** `src/uiLayout/_common.py` (gleiche Datei wie Rang 2/9, daher Serie).
**Abhängigkeiten (Begründung):** Brief 2 hinter einem Mockup-Gate; Brief 3 ist reiner Spec-Nachzug; beide sequenziell nach Brief 1 (Dateikonflikt `_common.py`).
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Teil der FixD-Serie (Compute/Render-Trennung in `_common.py`). Brief 1 (Rang 4) ist S150 erledigt und entblockt Brief 2+3 sowie den mypy-uiLayout-Abbau (B-004). Brief 2 wartet auf ein Mockup, Brief 3 zieht nur die zugehörige Spec nach.

## B-002 — Klan Dynastie Brief K1 Wortlaut Bugfix Nihilakh und Mephrit

**Herkunft:** Prio-Rang 6 (S145-Prioritätenliste); Entscheid kanonisiert S150.
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** `docs/goals/ziel7.md` §K1 (Stufe C).
**Betroffene Dateien:** `data/wh40k_9e/necrons/subfaction_abilities.yaml` (unverändert, Fix ausstehend).
**Abhängigkeiten (Begründung):** Reiner Daten-Fix, keine Code-Abhängigkeit; parallelisierbar mit Rang 4/5 (disjunkte Dateien).
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Scope S150 auf **Nihilakh + Mephrit** begrenzt — 2 fachlich falsche Einträge, reine Datenkorrektur, Quelle lokal in `ziel7.md` Stufe C §K1 belegt. Entscheid ist gefallen, der eigentliche Daten-Fix in `subfaction_abilities.yaml` steht noch aus.

## B-003 — Klan Dynastie K2 Plus Novokh Sautekh Nephrekh und Ork Snakebites

**Herkunft:** Prio-Rang 7 (S145-Prioritätenliste).
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** `docs/goals/ziel7.md` Stufe C §K1; `docs/spec/faction_abilities.md` Kategorie 6 (Spec-Nachzug nötig, s. B-085).
**Betroffene Dateien:** `subfaction_abilities.yaml` (Necron+Ork), Engine-Filter (Modul analog `subfactionPassives.py`).
**Abhängigkeiten (Begründung):** Macht 13 Backlog-Einträge erstmals wirksam; Effort L — **vor Vergabe in ≤ M-Briefs splitten** (S130-Auflage).
**Agent/Tier:** Planner → Executor
**Benötigte Regeln/Scopes:** `docs/reference/agent_scopes.md` (Split-Zuschnitt vor Vergabe).
**Detail:** Wortlaut-Fix für Novokh/Sautekh/Nephrekh (Necron-Dynastien) + Ork Snakebites, dazu Engine-Filter, `subfaction_passive`-Migration, 4 neue Effekttypen, ein Badge, und der Spec-Nachzug in `faction_abilities.md` Kategorie 6. Größter offener Klan/Dynastie-Block.

## B-004 — mypy Ratchet uiLayout

**Herkunft:** Prio-Rang 9 (S145-Prioritätenliste); §4 Alt-`backlog.md` Z.580.
**Typ:** Schuldabbau
**Belege/Recherche:** `docs/spec/architecture_invariants.md` (Typ-Ratchet), `tools/mypy_gate.py`.
**Betroffene Dateien:** `src/uiLayout/armyCard.py`, `gameProtocoll.py`, `unitCard.py`, `armyList.py`, `detachmentCard.py` (17 Fehler gesamt).
**Abhängigkeiten (Begründung):** Blockiert bis Rang 5 (B-001) fertig ist — Dateiüberschneidung `_common.py` mit FixD.
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Letzter Rest des mypy-Abbaus (Baseline 24, Stand S144) — der `uiLayout/`-Teil (17 Fehler) braucht manuelle Render-Verifikation, da Render-Code außerhalb der Coverage-Messung liegt. Pro Schritt Baseline in `tools/mypy_gate.py` im selben Commit senken (Ratchet-Regel).

## B-005 — Direktiv Lock Rest ab Bewegungsphase sperren

**Herkunft:** Prio-Rang 10 (S145-Prioritätenliste); §0 Alt-`backlog.md` Z.72–80 (#2b).
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** Root-Cause-Analyse S52 (§0 im Alt-Backlog).
**Betroffene Dateien:** `src/uiLayout/armyCard.py` (`_render_round_choice_ui`, `_render_once_per_battle_ability_ui`).
**Abhängigkeiten (Begründung):** Das Setup-Leck (Protokoll-Direktiven im Setup wählbar) ist bereits am 2026-06-20 gefixt (Helfer `_ability_section_visible`, Regressionstest `test_ability_sections_hidden_in_setup_only`); dies ist nur noch der Rest — Direktive ab Bewegungsphase sperren.
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Bug (Nutzer-Screenshots): Protokoll-Direktiven-Buttons + WAAAGH-Status erschienen im Setup und wurden über den First-Player-Toggle (`active` gesetzt) sogar wählbar; Auto-Block `if not active_id` schrieb `round_choice_active_*` schon im Setup. Setup-Teil ist gefixt; offen bleibt, die Direktive nach der Bewegungsphase zu sperren. Render-Code → manuelle Verifikation nötig.

## B-006 — abilityEngine Refactor Vorplanung

**Herkunft:** Prio-Rang ∥ (S145-Prioritätenliste, jederzeit parallel startbar); §4 Alt-`backlog.md` Z.593–613.
**Typ:** Schuldabbau
**Belege/Recherche:** `S145_planning.md` §Option C (migriert S147).
**Betroffene Dateien:** `src/gameMechanic/abilityEngine.py` (594 Zeilen, 29 Funktionen).
**Abhängigkeiten (Begründung):** Orthogonal zur Klan/Dynastie-Arbeit — K2 (B-003) legt seine neue Logik bereits in ein eigenes Modul (`gameMechanic/subfactionPassives.py`), `abilityEngine.py` wächst dadurch nicht.
**Agent/Tier:** Planner
**Benötigte Regeln/Scopes:** —
**Detail:** Analog zu `stratagemEngine.py` wurde erwogen, `abilityEngine.py` nach Aktivierungsmodus (passiv/aktiv/triggered) in ein Paket zu zerlegen. Kritische Bewertung: der Modus-Schnitt trägt die reale Struktur nicht — der dominante Block (~52 %) ist Direktiv-/Protokoll-Logik, weder klar „passiv" noch „triggered"; die natürlichen Nähte sind **Direktiven/Protokolle | Unit-Buffs+Revive | Queries+Dispatch**. 594 Zeilen sind (noch) kein Kohäsionsproblem — das reale Problem ist Duplikation (s. B-081 DRY Directive-Aktiv-Logik). **Konsent-Entscheid (S145): zurückgestellt, mit Schwellwert statt „nie".** Split-Trigger: `abilityEngine.py` überschreitet ~800 Zeilen ODER die DRY-Schuld wird angegangen → dann eigener Refactor-Brief, Schnitt entlang der realen Nähte (nicht passiv/aktiv/triggered). Effort S, ~15–20k Token, re-exportierendes `__init__.py` als Kompatibilitätsschicht; nicht parallel zu Briefs mit `abilityEngine`-Importänderungen.

## B-007 — Backlog Restrukturierung

**Herkunft:** Prio-Rang 11 (Stakeholder-Auftrag S150); dieser Auftrag selbst (S151).
**Typ:** Prozess/Doku
**Belege/Recherche:** `docs/handoff/S151_backlog_inventar.md` (Inventar-Schritt), `docs/handoff/S151_backlog_migration.md` (dieser Umsetzungs-Schritt).
**Betroffene Dateien:** `backlog.md`, `backlog_details.md`, `backlog_archive.md`, `index.md` (gelöscht).
**Abhängigkeiten (Begründung):** Kein Eintrag darf verloren gehen; Abschnitt 4c (Design-System, erledigt S116–S118, ohne ✅-Glyphen) muss mit archiviert werden — ein reiner Glyphen-Scan hätte ihn übersehen.
**Agent/Tier:** Planner → Stakeholder-Freigabe → Executor
**Benötigte Regeln/Scopes:** —
**Detail:** `backlog.md` bekam eine schlanke Kopf-Liste, die zugleich als Index dient; ausführliche Herleitungen/Detailtexte wurden in diese separate Datei ausgelagert. Vorgehen: Inventar (S151, dieser Schritt: Planner-Subagent-Brief → Stakeholder-Freigabe → Executor-Umsetzung). Dieser Eintrag selbst schließt sich mit Abschluss der Migration (S151).

## B-008 — on target Anker Option A UI Pruefung

**Herkunft:** Prio-Rang 2 (S145-Prioritätenliste); Code erledigt S146.
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** S143-Freigabe (Konzept), `docs/spec/design_system.md` §6.2/6.3.
**Betroffene Dateien:** `src/uiLayout/_common.py`.
**Abhängigkeiten (Begründung):** ⛔ Nicht parallel zu Rang 4/5 (gleiche Datei `_common.py`); reiner UX-Fix, S143 freigegeben.
**Agent/Tier:** Stakeholder (reine Bildschirm-Prüfung)
**Benötigte Regeln/Scopes:** —
**Detail:** Code-Teil (Ziel-Kachel als einziger Ort für on_target-GOs, Hit-/Save-Anker entfernt) ist seit S146/S147 umgesetzt und getestet; nur die manuelle Stakeholder-UI-Prüfung steht noch aus.

## B-009 — PSI Flow Reset UI Checks

**Herkunft:** §0 Alt-`backlog.md` Z.60–71 (S64-Befund, S65-Code).
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** Commits `cc75490`/`1d8b8ba`.
**Betroffene Dateien:** `src/gameMechanic/psychicPhase.py` (Helfer `refund_deny`/`cleared_deny`, `_reset_active_power()`, `_render_undo_deny_button`).
**Abhängigkeiten (Begründung):** Code + Tests grün seit S65 (+8 Tests, `TestRefundDeny`/`TestClearedDeny`); gemeinsamer Commit mit dem Token-Gauge-Hook geplant.
**Agent/Tier:** Stakeholder (4 manuelle UI-Checks)
**Benötigte Regeln/Scopes:** —
**Detail:** Generische Flow-/Reset-Struktur für die Psychic Phase: `_reset_active_power()` refundiert das Deny-Budget der inaktiven Fraktion (fixt: denied + reset = permanent verbranntes Budget); symmetrisches „Undo deny"-Button; „Skip Deny" verbraucht kein Budget; `deny_faction`-Feld in `psi_result`. **Noch offen (4 manuelle UI-Checks):** (a) „Undo deny" nach erfolgreichem Deny; (b) aktiv-Reset → nächste Power denybar; (c) Skip Deny = kein Budgetverbrauch; (d) Undo nach fehlgeschlagenem Deny — danach gemeinsamer Commit mit dem Token-Gauge-Hook. Verwandt (separater Task): `can_deny` via `rules` statt `wargear_ids`+`handler` (Gloom Prism als echter Wargear-Choice).

## B-010 — Protokoll Buff Audit Anzeige Rest

**Herkunft:** §0 Alt-`backlog.md` Z.81–122 (#2, Phase 3).
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** Plan 024 (Engine-Wiring), Plan 025 Steps 2–6 (Anzeige/Konformität), 016/017 (Anzeige-Rest-Gebiet).
**Betroffene Dateien:** `src/uiLayout/_common.py`, `src/gameMechanic/abilityEngine.py`.
**Abhängigkeiten (Begründung):** Eternal Guardian S SAVE-Hinweis hängt an einem eigenen Plan (abhängig von Plan 015 Overwatch); Sudden Storm S-Teil ist über den generischen Direktiv-Hinweisblock (Plan 025 Step 2b) bereits abgedeckt (s. Archiv A-020).
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Engine-Wiring ist komplett (Plan 024, alle 12 Direktiv-Effekte engine-seitig verdrahtet, vorher 3/12). Offen bleibt nur noch die **Anzeige**: Eternal Guardian **S** (Hold Steady/Set to Defend) braucht einen eigenen Plan nach Plan 015 (Overwatch). S93-Engine-Befund (beide Direktiv-Quellen — 6. immer-aktives Protokoll + Dynastie-Affinitäts-Fall — waren zuvor ignoriert) ist gefixt (`_active_directive_effects` aggregiert alle 5 Reads). S97-Befund (Reroll-of-1-Save-Hinweis fehlte im SAVE-Block; `strength_modifier`/`ap_bonus` wurden von keinem UI-Konsumenten gelesen) ist über Plan 025 Steps 2/3 gelöst (Hungry-S → `strength_if_charged`, Vengeful-S → `ignore_cover_half_range`). Wurzel-Lösung S98: kein genereller Caption-Block mehr, Direktiv-Effekte gehen ins Dice-UI (S blau wie WAAAGH, `value_triggered_die_row_html`) — Anzeige ist ab S97 Pflichtteil jedes 025-Steps.

## B-011 — Wuerfelanzeige Pfeilrichtung und Badge Breite

**Herkunft:** §0 Alt-`backlog.md` Z.123–128 (#3/#4, Phase 4).
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** `docs/spec/dice_display.md` (Soll-Bild als AC festlegen); Finding 9.2 (Lehre: nie still ändern).
**Betroffene Dateien:** —
**Abhängigkeiten (Begründung):** Soll-Bild muss erst als Acceptance Criterion in `dice_display.md` fixiert werden → dann Plan 022, dann per AC einrasten.
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Pfeilrichtung/-länge der Modifier-Zeile stimmt nicht, Badge ragt in Würfel „1". Der Badge-Wert selbst bleibt (`AP-1`/`AP-2`, Stakeholder-Entscheid 2026-06-21: Gewohnheit + Konsistenz zu anderen Profilwerten; Pfeil ist bewusst redundant) — Labels nur **kürzen** (truncate/ellipsis), nicht den Wert entfernen.

## B-012 — INV 4b Cluster 1 dakka klaw tesla YAML Schema

**Herkunft:** §0 Alt-`backlog.md` Z.129–133 (Refinement 2026-06-20).
**Typ:** Schuldabbau
**Belege/Recherche:** `docs/spec/architecture_invariants.md` INV-4b.
**Betroffene Dateien:** YAML-Schema `weapon_special`.
**Abhängigkeiten (Begründung):** Cluster 3 (Plan 020), Cluster 4/5 (XS-Fix), Cluster 6 (Plan 021/024) sind bereits erledigt (Archiv A-006–A-009) — Cluster 1 ist der letzte offene INV-4b-Vokabular-Cluster.
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** `dakka`/`klaw`/`tesla` sollen YAML-gesteuert über ein `weapon_special`-Schema abgebildet werden, statt als Fraktions-Eigennamen in `src/` zu leben. Teil von Plan 022 oder eigenständig umsetzbar.

## B-013 — GO UI Paket 3b before battle Liste ArmySetup

**Herkunft:** §2 Alt-`backlog.md` Z.160–162; S131-Kandidat, Paket 3b (S134).
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** `docs/spec/design_system.md` §6, `docs/reference/go_klassifikation.md` (95 GOs, 3 Achsen). Entscheid S131.
**Betroffene Dateien:** ArmySetup-Screen.
**Abhängigkeiten (Begründung):** Teil der 6-Pakete-GO-UI-Design-System-Roadmap (jedes Paket geht einzeln durchs Freigabe-Gate).
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** `before_battle`-Liste im ArmySetup macht 13 bisher nie matchende GOs erstmals sichtbar — löst den S131-Kandidaten „`before_battle` sichtbar machen" (s. B-018) ab.

## B-014 — GO UI Folge Pakete fuer 10 Rest GOs

**Herkunft:** §2 Alt-`backlog.md` Z.171–173; `design_system.md` §6.2 Z.320–321.
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** `docs/spec/design_system.md` §6.2 (Schuld-Tabelle).
**Betroffene Dateien:** —
**Abhängigkeiten (Begründung):** Nach Paket 4 (erledigt S135, Archiv A-013). Effort L — **Paket-Nummern bei Einplanung NEU vergeben** (Kollision mit den bereits vergebenen Paket-5/6-Nummern unten, s. B-015/B-016).
**Agent/Tier:** Planner → Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Generisches `on_destroy` (7 GOs) + `on_set_up`+`on_target` für die verbleibenden 10 der ursprünglich 14 `phase_reactive`-GOs, die bis Paket 4 nirgends aktivierbar waren. Vorschlag bereits in `design_system.md` §6.2 skizziert (dort „Paket 5/6" ≠ die Backlog-Pakete 5/6 unten — Nummern-Kollision beim Einplanen vermeiden).

## B-015 — GO UI Paket 5 Wortlaut und Sprach Bereinigung

**Herkunft:** §2 Alt-`backlog.md` Z.174–175; Paket 5 (S134+).
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** `docs/spec/design_system.md` §6 (Wortlaut-Konventionen).
**Betroffene Dateien:** —
**Abhängigkeiten (Begründung):** Teil der 6-Pakete-Roadmap.
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Englisch durchgehend, eine Vokabel-Familie Use/Undo/Confirm, eine CP-Anzeige, ein Stepper-Baustein.

## B-016 — GO UI Paket 6 Einheiten Auswahl und Zielauswahl

**Herkunft:** §2 Alt-`backlog.md` Z.176–178; Paket 6 (S134+, eigenes Konzept-Inkrement).
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** —
**Betroffene Dateien:** GameActionArea.
**Abhängigkeiten (Begründung):** Eigenes Konzept-Inkrement innerhalb der Roadmap.
**Agent/Tier:** Design-Crew → Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Einheiten-Auswahl in die GameActionArea ziehen (Heroische-Intervention-Muster verallgemeinern), Zielauswahl entschlacken.

## B-017 — GO UI Danach manuelle UI Gesamt Verifikation

**Herkunft:** §2 Alt-`backlog.md` Z.179.
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** S130-Checkliste.
**Betroffene Dateien:** —
**Abhängigkeiten (Begründung):** Erst nach Abschluss aller GO-UI-Pakete (B-013 bis B-016).
**Agent/Tier:** Stakeholder
**Benötigte Regeln/Scopes:** —
**Detail:** Manuelle UI-Gesamt-Verifikation nach der S130-Checkliste plus dem neuen GO-Card-Design, sobald die Pakete abgeschlossen sind.

## B-018 — Fraktions Stratagems before battle sichtbar machen

**Herkunft:** §2 Alt-`backlog.md` Z.180–183; S131-Kandidat.
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** `docs/goals/ziel7.md` §6e (Modifier-Engine für proaktive Stratagems).
**Betroffene Dateien:** `PHASES`-Konstante (kennt kein `before_battle`).
**Abhängigkeiten (Begründung):** Löst über B-013 (Paket 3b); danach folgt die §6e-Modifier-Engine für ~56 teilintegrierte proaktive Stratagems.
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** 6 Necron- + 7 Ork-Stratagems matchen nie, weil `PHASES` kein `before_battle` kennt — wird durch die neue ArmySetup-Liste aus B-013 gelöst.

## B-019 — Alt Fire Chip unerklaert

**Herkunft:** §2 Alt-`backlog.md` Z.184–187; S132-Befund 5, überführt S134.
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** `docs/work/` (Regel-Wortlaut „Alternating Fire" verifizieren).
**Betroffene Dateien:** `src/uiLayout/diceHtml.py:70`.
**Abhängigkeiten (Begründung):** Reiner Lookup + Kurzergänzung, keine Blocker.
**Agent/Tier:** Executor (Haiku-Lookup für die Regel-Verifikation)
**Benötigte Regeln/Scopes:** —
**Detail:** `special_die_html("Alt. Fire")` rendert ohne Erklärtext (anders als „Extra Hits" mit „unmod. 6 = +2 Hits"). Vorgehen: Regel-Wortlaut gegen `docs/work/` verifizieren, dann Kurzerklärung analog Extra-Hits ergänzen. Effort XS.

## B-020 — B2 Spielvorbereitungsscreen ueberarbeiten Konzept

**Herkunft:** §2 Alt-`backlog.md` Z.194–209 (Stakeholder-Beobachtungen S131).
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** `S134_offene_punkte.md`.
**Betroffene Dateien:** —
**Abhängigkeiten (Begründung):** Struktur = Option C bereits entschieden (S135: Option A jetzt, Wizard-Zielbild erst mit B4-Datenkarte/B-021); Redundanz-Befunde B5/B7 (B-022) einarbeiten.
**Agent/Tier:** Design-Crew
**Benötigte Regeln/Scopes:** —
**Detail:** Noch kein Konzept. Vorgehen: Screen-Inventar erstellen (Sonnet, read-only), Redundanz-Befunde einarbeiten, Konzept-Handoff mit Grundannahmen-Block → Stakeholder-Entscheid → eigener Plan. Faction-Ability-Wahl (B6, erledigt) läuft unabhängig vom B2-Konzept. Hinweis: der frühere Punkt „Start-Game-Button-Position" wurde S133 aus der Beobachtungsdatei entfernt/erledigt.

## B-021 — B4 Rest profileCard als Datenkarte Setup

**Herkunft:** §2 Alt-`backlog.md` Z.200–209 (Stakeholder-Beobachtungen S131).
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** Screenshots `Bildschirmfoto vom 2026-07-09 20-53-48.png` (Ist) / `…20-58-07.png` (Wahapedia-Anmutung als Inspiration, NICHT 1:1); `S134_offene_punkte.md`.
**Betroffene Dateien:** —
**Abhängigkeiten (Begründung):** Bereitet den künftigen Armybuilder vor; nur Setup-Screen, In-Game-Anzeige bleibt unverändert (Stakeholder-Entscheid S135).
**Agent/Tier:** Design-Crew → Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Doppel-Zoll + Profilwert-Reihenfolge bereits S133 gefixt; offen: tabellarische Waffenanzeige + „schöne Datenkarte" nur mit der echten Roster-Auswahl. **Entschieden S135:** App-Design-System mit Wahapedia-Informationsarchitektur, nur 9E-Datasheet-Spalten (keine berechneten Werte), Wargear/Relic als Chip. Vorgehen: profileCard als definierten Baustein in `design_system.md` spezifizieren (Refinement: Spalten, Waffen-Tabelle, Abgrenzung zur unitCard), danach eigener Plan.

## B-022 — B7 Redundanter Kopfbereich und schwache Hinweise

**Herkunft:** §2 Alt-`backlog.md` Z.213–232 (Stakeholder-Beobachtungen S131, Screenshot `…21-29-43.png`); Selbst-Stopp S149.
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** `S134_offene_punkte.md`.
**Betroffene Dateien:** `src/uiLayout/_common.py` (`render_player_column`), `psychicPhase.py`, `fightPhase.py`, `commandPhase.py`, `PHASE_RULES` (`_common.py`/`gameActionsArea.py`).
**Abhängigkeiten (Begründung):** Effort M — **vor Vergabe splitten** (Vorschlag B7a Faktions-Zeile+Mini-Header / B7b Hinweis-Baustein); betrifft >4 Dateien, über der Selbst-Stopp-Schwelle aus dem S149-Auftrag.
**Agent/Tier:** Planner → Executor
**Benötigte Regeln/Scopes:** `docs/reference/agent_scopes.md` (Split-Zuschnitt vor Vergabe).
**Detail:** Rot markierter Bereich ist redundant; wichtige Hinweise darunter („Select unit", „No PSYKER unit available") zu schwach sichtbar. **Entschieden S135:** Kopfbereich → Mini-Header (nur Phasenname, Option B, solange kein B9-Stepper existiert); Hinweis-Konvention → eigener Design-System-Baustein (Option B); B7+B9 als EIN Konzept-Handoff. **S149-Selbst-Stopp-Befund:** der rote Bereich ist die Faktions-Zeile (`**▶/◀ {faction}**`), dupliziert in `_common.py::render_player_column` UND separat in `psychicPhase.py`/`fightPhase.py`/`commandPhase.py` (DRY-Lücke, je eigene Kopie); die Mini-Header-Umstellung betrifft zusätzlich `PHASE_RULES` und der Hinweis-Baustein müsste in mindestens 6 Produktivdateien verdrahtet werden — über der ~4-Dateien-Schwelle. B8 (Archiv A-017) wurde isoliert umgesetzt; B7 bleibt für einen kleiner geschnittenen Folge-Auftrag offen. Screenshot bleibt liegen, bis der Punkt DONE ist.

## B-023 — B9 Subphasen Schritte unsichtbar Stepper Baustein

**Herkunft:** §2 Alt-`backlog.md` Z.235–242 (Stakeholder-Beobachtungen S131).
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** `S134_offene_punkte.md`.
**Betroffene Dateien:** —
**Abhängigkeiten (Begründung):** Läuft als EIN Konzept-Handoff gemeinsam mit B7 (B-022); die B7/B8-Entfernungen schaffen erst den Platz dafür.
**Agent/Tier:** Design-Crew → Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Je Phase die Unterschritte explizit anzeigen (z. B. Movement: erst alle Feldbewegungen, dann Reinforcements), während redundante Texte (B7/B8) verschwinden. **Entschieden:** Zwischenlösung C (statischer Hinweistext, kein Zustand), Zielbild vertikale Checkliste statt horizontaler Chips (Stakeholder-Kommentar).

## B-024 — B10 Kommentar Hygiene Ratchet Praxis

**Herkunft:** §2 Alt-`backlog.md` Z.243–249 (Stakeholder-Beobachtungen S131).
**Typ:** Prozess/Doku
**Belege/Recherche:** `CLAUDE.md` §Clean Code.
**Betroffene Dateien:** Alle bei Modul-Berührung.
**Abhängigkeiten (Begründung):** Teil (a) bereits erledigt — Konvention in `CLAUDE.md` verankert; Teil (b) ist eine dauerhafte Ratchet-Praxis ohne Enddatum.
**Agent/Tier:** Executor (bei jeder Modul-Berührung)
**Benötigte Regeln/Scopes:** —
**Detail:** Soll: Erklärung in der Spec, Code selbsterklärend (Clean Code), höchstens ein Verweis-Kommentar auf die zuständige Spec. (a) Konvention im CLAUDE.md-Clean-Code-Abschnitt geschärft — erledigt S135. (b) läuft als Ratchet-Praxis weiter: bei jeder Modul-Berührung Kommentare in die zuständige Spec verschieben, kein Big-Bang-Durchgang.

## B-025 — B11 Rest Wahrnehmung nach B1 Fix

**Herkunft:** §2 Alt-`backlog.md` Z.250–253 (Stakeholder-Beobachtung S136).
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** `docs/handoff/S136_B1_probe.md` (Playwright-Beleg B1).
**Betroffene Dateien:** —
**Abhängigkeiten (Begründung):** B1 selbst ist gefixt (Archiv A-014); dies ist der optionale 2. Schritt aus der B1-Probe.
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Beim Slot-Wechsel geschieht optisch noch ein kurzer Sprung/Zucken, aber das Fenster bleibt an derselben Stelle (kein Scroll-Delta mehr). Beobachten, ggf. Dropdown-Höhen stabilisieren.

## B-026 — B12 GO used Zustand Gesamtkonzept

**Herkunft:** §2 Alt-`backlog.md` Z.254–259 (Stakeholder-Entscheid S137).
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** `docs/handoff/S137_B12_konzept.md`.
**Betroffene Dateien:** —
**Abhängigkeiten (Begründung):** B12b (Header-Suffix) ist bereits erledigt (Archiv A-018); dieser Eintrag ist der Rest darüber hinaus — Once-per-Phase-Erzwingung phasenübergreifend.
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Undo-Button nur bei der Einheit, bei der die GO angewendet wurde; an allen anderen Angebotsstellen der Phase Einsatz unterbinden, Button-Text „Used". Inline-Angebote (Attacken-/Charge-Sequenz) zeigen NIE Undo; Once-per-Phase wird erzwungen (nach Hit-Einsatz zeigen Wound/Save „used"). Größerer Eingriff: Umsetzung als Teil-Briefs ≤ M.

## B-027 — B12 optionaler XS Task unit key durch spend stratagem

**Herkunft:** §2 Alt-`backlog.md` Z.267–269 (B12-Unterpunkt).
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** —
**Betroffene Dateien:** `spend_stratagem`-Aufrufer (Advance-Reroll, Fire Overwatch).
**Abhängigkeiten (Begründung):** Spec-konformer Randfall, kein Bug — rein optional „falls je gewünscht".
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Advance-Reroll-/Inline-Spends übergeben konstruktionsbedingt kein `unit_key` an `spend_stratagem` → der „used on ⟨Einheit⟩"-Suffix bleibt dort leer, ebenso bei Fire Overwatch (Charge-Phase-Anker). S148 als PASS verifiziert (spec-konformer Randfall). Optionaler Folge-Task: `unit_key`/uid durchreichen.

## B-028 — B12 Feature Wunsch used on Suffix auf alle GOs

**Herkunft:** §2 Alt-`backlog.md` Z.284–286 (Stakeholder-Wunsch S148).
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** —
**Betroffene Dateien:** —
**Abhängigkeiten (Begründung):** Nach dem BUG-Fix (Archiv A-019, Insane-Bravery-Repro Moralphase).
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** „used on ⟨Einheit⟩"-Suffix soll auf **alle** reaktiven GOs ausgeweitet werden (aktuell nur die zentrale Stratagems-Liste betroffen).

## B-029 — B13 GO Karte Keyword Badges

**Herkunft:** §2 Alt-`backlog.md` Z.287–295 (Stakeholder-Beobachtung S137).
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** `docs/spec/design_system.md` §6 (GO-Card-Baustein).
**Betroffene Dateien:** `src/gameObjects/stratagem.py` (Dataclass ohne `keywords`-Feld); Stratagem-YAMLs (`_shared`/`necrons`/`orks` — 0 Treffer für `keywords:`).
**Abhängigkeiten (Begründung):** S141-Nachtrag: Vorziehen der Daten-Nachpflege geprüft und zurückgestellt — ist Schema-Erweiterung **plus** Datenpflege, kein reiner YAML-Task.
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** GO-Karten zeigen keine Schlüsselwort-Chips (nur Name/CP/Regeltext). Neues Feature, keine Eil-Priorität (Stakeholder-Entscheid S137: „ins Backlog"). Stakeholder-Entscheid S141: zurückstellen, bis B13 selbst geplant wird — dann Schema+Loader+Daten in einem Aufwasch.

## B-030 — B14 Badge Kontrast Pass Stationary Khaki

**Herkunft:** §2 Alt-`backlog.md` Z.296–300 (Stakeholder-Beobachtung S137).
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** —
**Betroffene Dateien:** `docs/spec/design_colors.md`, `src/uiLayout/unitCard.py`.
**Abhängigkeiten (Begründung):** Farbschema-Entscheidung liegt beim Stakeholder — Hex-Vorschläge müssen zuerst vorgelegt werden, danach mechanischer Edit.
**Agent/Tier:** Stakeholder → Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Badges schwer erkennbar, v. a. STATIONARY (`--arb-muted` `#6b5f44`) zu dunkel. Vorschlag: heller Khaki `#9c8f6a`; prüfen, ob weitere gedämpfte Badges mit angehoben werden müssen (Stakeholder S137: „ins Backlog").

## B-031 — GO Konsistenz Bedingungen ausgrauen statt ausblenden

**Herkunft:** §2 Alt-`backlog.md` Z.304–310 (Stakeholder-Wunsch S149, anlässlich GAUSS/TESLA-Gates).
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** `docs/handoff/S149_review.md` Befund 3.
**Betroffene Dateien:** `stratagem_visibility()`, `src/uiLayout/_common.py:1134`.
**Abhängigkeiten (Begründung):** Passt laut Review kollisionsfrei zum bestehenden GO-State-Modell ready/locked/used — diese Zustände rendern den Button bereits deaktiviert/ausgegraut.
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Durchgehend für **alle** GOs: `stratagem_visibility()` soll bei Keyword-/Bedingungs-Nichterfüllung statt `"hidden"` einen sichtbaren-aber-gesperrten Zustand (`dormant`/`locked`) zurückgeben.

## B-032 — Psychic Ledger schrumpfen

**Herkunft:** §2 Alt-`backlog.md` Z.311–314 (S62).
**Typ:** Schuldabbau
**Belege/Recherche:** `docs/spec/acceptance/rules.md` (R-PSYCHIC-11/16/17/18/22).
**Betroffene Dateien:** `_render_smite_flow`/`_render_psi_result`/`_render_deny_column` (Render-Code, policy-ungetestet).
**Abhängigkeiten (Begründung):** Ledger soll von 15 auf 10 schrumpfen.
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Smite-Manifest-Logik lebt aktuell im Render-Code. Reine Funktionen extrahieren (Schwelle `roll≥wc`, Warp-Charge-Eskalation, Perils-Schaden, Deny-once) + Tests, um die Business-Logik testbar aus dem Render-Code zu lösen.

## B-033 — Psychic Luecken R PSYCHIC 23 und 24

**Herkunft:** §2 Alt-`backlog.md` Z.315–317 (S62, aus Regel-Katalog).
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** `docs/spec/acceptance/rules.md` (`status: offen`).
**Betroffene Dateien:** —
**Abhängigkeiten (Begründung):** Beide brauchen einen Unit-Destroyed-Check nach Perils-Schaden.
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** `R-PSYCHIC-23` (Perils zerstört Psyker ⇒ Power schlägt fehl; App revidiert `manifested` aktuell nicht) und `R-PSYCHIC-24` (Perils-Splash D3 an Einheiten in 6") sind implementiert-offen.

## B-034 — SAVE Block Faehigkeit und AP als eine Badge

**Herkunft:** §2 Alt-`backlog.md` Z.320.
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** → Plan 017.
**Betroffene Dateien:** YAML-Erweiterung nötig.
**Abhängigkeiten (Begründung):** Überschneidet Plan 017 (Invuln-Badge chaotisch, B-043) und B-047.
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Fähigkeit + AP als eine kombinierte Badge darstellen, z. B. „Enslaved AP-1", statt getrennter Elemente.

## B-035 — Gretchin Cowardly Attrition ohne RUNTHERD

**Herkunft:** §2 Alt-`backlog.md` Z.321.
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** → Plan 018.
**Betroffene Dateien:** `orks/unit_abilities.yaml` (Gretchin-Cowardly-Eintrag).
**Abhängigkeiten (Begründung):** —
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** −1 Attrition, wenn keine RUNTHERD-Einheit innerhalb 6" ist — Teil von Plan 018.

## B-036 — Battle Log nach Reset alte Eintraege

**Herkunft:** §2 Alt-`backlog.md` Z.322.
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** → Plan 018.
**Betroffene Dateien:** —
**Abhängigkeiten (Begründung):** —
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Bug — nach Reset zeigt das Battle-Log noch alte Einträge. Teil von Plan 018.

## B-037 — collect modifiers for phase

**Herkunft:** §2 Alt-`backlog.md` Z.323; §5 Z.730.
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** → Plan 018 Task 18.4; `docs/goals/ziel7.md` §6e.
**Betroffene Dateien:** —
**Abhängigkeiten (Begründung):** Laut §5 zusätzlich Teil von `ziel7.md` §6e (Modifier-Engine für proaktive Stratagems).
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** `collect_modifiers_for_phase()` — Plan-018-Task 18.4, noch offen.

## B-038 — Totalvernichtungs Spielende R ROUND 07

**Herkunft:** §2 Alt-`backlog.md` Z.324–327 (S138-Befund).
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** `docs/spec/acceptance/rules.md` R-ROUND-07.
**Betroffene Dateien:** —
**Abhängigkeiten (Begründung):** Stakeholder: eigener Punkt.
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Der „army destroyed"-Teil von R-ROUND-07 ist bewusst NICHT implementiert — Sieg durch vollständige Vernichtung der gegnerischen Armee vor Ende Runde 5 fehlt als eigener Spielende-Pfad. Eigener kleiner Plan.

## B-039 — Tote Produktionsfunktion build aura range hint text entfernen

**Herkunft:** §2 Alt-`backlog.md` Z.328–333 (S138-Retro-Maßnahme 2).
**Typ:** Schuldabbau
**Belege/Recherche:** `docs/spec/acceptance/rules.md` (Code-Referenz nachziehen).
**Betroffene Dateien:** `src/gameMechanic/abilityEngine.py:324` (`build_aura_range_hint_text`), `tests/*/test_ability_engine.py`.
**Abhängigkeiten (Begründung):** Einziger Produktions-Konsument (`armyCard._render_aura_range_hint`) wurde S138 entfernt (Conquering-Tyrant-Aura-Hinweis raus) — Funktion wird nur noch von Tests referenziert.
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Mit Tests gemeinsam entfernen, `acceptance/rules.md`-Eintrag nachziehen (Code-Referenz wird sonst stale). Effort XS.

## B-040 — Fold Heuristik und Subfaction Wiring Roster zu Unit

**Herkunft:** §2 Alt-`backlog.md` Z.334–340 (S138-Retro-Maßnahme 3).
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** —
**Betroffene Dateien:** `src/uiLayout/unitCard.py` (`_fold_faction_keyword`).
**Abhängigkeiten (Begründung):** Blockiert, bis echte Subfraktions-Keywords existieren (s. B-002/B-003) — beide Teile in einem Aufwasch prüfen.
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** `_fold_faction_keyword` filtert aktuell nur das Hauptfraktions-Keyword (Trailing-„S"-Fold); Subfraktions-Keywords werden nicht gefoldet, weil der Loader den `<DYNASTY>`/`<CLAN>`-Platzhalter mangels Roster→Unit-Wiring aktuell droppt. Sobald echte Subfraktions-Keywords in die Unit-Listen kommen (Klan-Chip statt Drop), muss die Fold-Filterung erneut geprüft werden.

## B-041 — Operating Model Phase C Refinement automatisieren

**Herkunft:** §2 Alt-`backlog.md` Z.341–342.
**Typ:** Prozess/Doku
**Belege/Recherche:** `docs/governance/operating_model.md`.
**Betroffene Dateien:** `Fotos/` → `docs/inbox/`.
**Abhängigkeiten (Begründung):** —
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Refinement automatisieren — ein Sonnet-Subagent liest neue Bilder aus `Fotos/`, extrahiert die Idee als Text nach `docs/inbox/` (Format dort dokumentiert).

## B-042 — Gates und Reports leser orientiert pruefen

**Herkunft:** §2 Alt-`backlog.md` Z.343–345 (→ ADR-0002).
**Typ:** Prozess/Doku
**Belege/Recherche:** ADR-0002.
**Betroffene Dateien:** Debt-Scoreboard, Rule-Catalog-Prozente.
**Abhängigkeiten (Begründung):** —
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Gates/Reports dahingehend durchsehen, ob sie dem Stakeholder *seine* Fragen verständlich beantworten — nicht nur maschinen-orientiert zählen.

## B-043 — Invuln SAVE Badge Bereich chaotisch

**Herkunft:** §2 Alt-`backlog.md` Z.346 (S78).
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** —
**Betroffene Dateien:** SAVE-Block-Render.
**Abhängigkeiten (Begründung):** Überschneidet sich mit Plan 017 (SAVE-Block Fähigkeit+AP kombinierte Badge, B-034).
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Zeigt drei Teile („Inv 4+", „active", „AP/Cover N/A"), die teils keinen Sinn ergeben. Soll: **eine** klare Badge, z. B. „Invuln 4+" — dort mitlösen oder eigener kleiner Task.

## B-044 — Dice Display Modifier Geometrie

**Herkunft:** §2 Alt-`backlog.md` Z.347 (Befund B/C, S78).
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** `docs/spec/dice_display.md` §3.1/§3.3.
**Betroffene Dateien:** `modifier_die_pair_html`.
**Abhängigkeiten (Begründung):** Eigener Plan (eigenes Test-Netz); die Pfeil-**Zahl** (Befund A) ist bereits umgesetzt (S78).
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** HIT/WOUND-**Debuff** spreizt nicht mit der Magnitude — `modifier_die_pair_html` zeigt immer `from-1 → from` (−1/−2/−3 sehen identisch aus), Spec §3.1 will den farbigen Würfel mit der Magnitude nach rechts wandern lassen. Zusätzlich verletzt HIT-**Buff** die Slot-1-Invariante (grauer Würfel rutscht auf Spalte 1, §3.3 will min. 2). SAVE-Geometrie ist korrekt.

## B-045 — Silent King Zielaufteilung Fernkampf

**Herkunft:** §2 Alt-`backlog.md` Z.348 (S79-UI-Befund; Regel S80 GEKLÄRT).
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** `docs/inbox/finding-silent-king-target-split.md`; Core Rules-Zitat: „If a model has more than one ranged weapon, it can split the weapons between different enemy units."
**Betroffene Dateien:** Ziel-Auswahl-UI Schussphase.
**Abhängigkeiten (Begründung):** Regel bereits geklärt (S80); reine Umsetzung.
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Ein Modell mit **zwei** Fernkampfwaffen (Silent King: Sceptre of Eternal Glory / Staff of Stars) kann aktuell nur **eine** Feind-Einheit als Ziel wählen — regelwidrig. Alle Attacken **einer** Waffe gehen auf dieselbe Einheit. → UI auf **Ziel-pro-Waffe** umbauen + alle Ziele vor dem ersten Wurf deklarieren; Staff-of-Stars-Sperre ≤8 W beachten; Regressionstest. Eigener Plan.

## B-046 — Off Scale Sieben Plus Save Grenze

**Herkunft:** §2 Alt-`backlog.md` Z.349 (S79-UI-Befund).
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** `docs/spec/dice_display.md` (Ergänzung nötig).
**Betroffene Dateien:** —
**Abhängigkeiten (Begründung):** Verwandt mit Befund B/C (B-044).
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Sv 7+ (z. B. Gretchin) bzw. durch AP jenseits 6 verschlechterte Saves brauchen einen „7-Augen"-Würfel **plus** Erfolgsgrenze `|`. Soll lt. Stakeholder: Kopfzeile `[6] | [✕]`; Cover-Randfall `[6] 1→[7]`; AP-Fall `[6] ←4 [✕]` (konsequente Fortschreibung der D5-Spec). Alle Fälle mit Tests.

## B-047 — AP und SAVE Modifier Magnitude Position

**Herkunft:** §2 Alt-`backlog.md` Z.350 (S79-UI-Befund).
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** —
**Betroffene Dateien:** —
**Abhängigkeiten (Begründung):** Eng verwandt mit Befund B/C-Geometrie (B-044).
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Die Magnitude-Zahl (`-N`/`←N`) gehört in die **Erfolgsgrenz-Spalte** unter `|` (Screenshot AP-2: „-2" unter die Grenze; Basis-AP: erwartetes `-`/Marker in Spalte Würfel „6"). Spec prüfen, für **alle** Fälle (Buff/Debuff, HIT/WOUND/SAVE) Tests hinterlegen.

## B-048 — Lethal Hits

**Herkunft:** §2 Alt-`backlog.md` Z.351 (Refinement 2026-06-20).
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** Regel-Katalog R-CMB-XX.
**Betroffene Dateien:** —
**Abhängigkeiten (Begründung):** Eigener Plan nach Plan 014.
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Unmodifizierter Treffer-6 = kein Wundwurf, Schaden direkt mit Overflow (wie Mortal Wounds). Nicht implementiert.

## B-049 — Deadly Demise

**Herkunft:** §2 Alt-`backlog.md` Z.352 (Refinement 2026-06-20).
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** Regel-Katalog R-CMB-YY.
**Betroffene Dateien:** —
**Abhängigkeiten (Begründung):** YAML-Daten vorhanden, Handler fehlt.
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Modell zerstört → Mortal Wounds auf Einheiten in X". Eigener Plan.

## B-050 — Voice of the Triarch

**Herkunft:** §2 Alt-`backlog.md` Z.353 (Refinement 2026-06-20).
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** Regel-Katalog R-CMD-XX.
**Betroffene Dateien:** `alter_command_protocol` (YAML-Basis fertig).
**Abhängigkeiten (Begründung):** → Plan 016 oder eigener Plan.
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Silent King — `voiceOfTheTriarch`-Handler fehlt.

## B-051 — Failsafe Arkana Aktivator UI fehlt

**Herkunft:** §2 Alt-`backlog.md` Z.354–365 (S88-Befund).
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** INV-4b-Memory-Lehre („Engine-Test-grün ≠ UI-verdrahtet").
**Betroffene Dateien:** `src/uiLayout/armyCard.py:356-364` (`_render_once_per_battle_ability_ui`), `faction_abilities.yaml`.
**Abhängigkeiten (Begründung):** Kein Regressions-Bug (Picker war Plan-024-Scope-Out), aber generische Lücke für künftige aktivierbare Fraktionsfähigkeiten.
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** `activated`-Einträge aus `faction_abilities.yaml` mit `once_per_battle: false` werden bei `round_choice`-Fraktionen (Necrons/Custodes) **nirgends** als Aktivator gerendert — `_render_once_per_battle_ability_ui` returnt früh, wenn die Fraktion `round_choice`-Fähigkeiten hat, und surface-t nur eine `once_per_battle: true`-Fähigkeit; die commandPhase-Pfade lesen nur `unit_abilities.yaml`+`wargear.yaml`, nie `faction_abilities.yaml`. Folge: Failsafe Overcharger ist engine-dispatchbar (`buff_stat_bonus`, unit-getestet) **aber nie aktivierbar**. Fix: generischer Aktivator für `activated`-`faction_abilities` (unabhängig von `once_per_battle`/`round_choice`) + CANOPTEK-Target-Picker (9").

## B-052 — condition prompt applies when First Class Felder

**Herkunft:** §2 Alt-`backlog.md` Z.366–370 (S128-Folge, Plan 018 Task 18.3).
**Typ:** Schuldabbau
**Belege/Recherche:** Kommentar in `orks/unit_abilities.yaml` (Gretchin-Cowardly-Eintrag).
**Betroffene Dateien:** `gameObjects/ability.py`, `gameObjects/loader.py`.
**Abhängigkeiten (Begründung):** Erst wenn ein zweiter Konsument auftaucht.
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** `condition_prompt`/`applies_when` reiten aktuell als Roh-Dict in der `effects`-Subliste mit, weil `Ability`/`Effect` keine eigenen Felder dafür haben. Sauberere Modellierung, sobald ein zweiter Konsument auftaucht.

## B-053 — Daten Altlast gretchin mob

**Herkunft:** §2 Alt-`backlog.md` Z.371–375 (S128-Fund).
**Typ:** Schuldabbau
**Belege/Recherche:** `docs/work/wahapedia_orks/`.
**Betroffene Dateien:** `orks/unit_abilities.yaml`.
**Abhängigkeiten (Begründung):** —
**Agent/Tier:** Executor (Haiku-Lookup)
**Benötigte Regeln/Scopes:** —
**Detail:** `rule_text` klingt nach einer 8E-Formulierung („must take a Morale test if it suffers any casualties") — gegen `docs/work/wahapedia_orks/` prüfen, ob die 9E-Bedingung abweicht (9E: Morale Test nur bei Verlusten UND unter Half-strength, sonst optional?), ggf. korrigieren.

## B-054 — Custodes Rendax Kath Secondary toter Pfad

**Herkunft:** §2 Alt-`backlog.md` Z.376–382 (Plan 025 Step 6).
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** S97/S98-Befund (analog Hungry Void D2).
**Betroffene Dateien:** `data/wh40k_9e/adeptus_custodes/faction_abilities.yaml` (Protokoll `rendax_kath`, `secondary`-Effekt).
**Abhängigkeiten (Begründung):** Engine-Fn (`strength_if_charged`) existiert bereits; nur Konsum + Test nötig.
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Der `secondary`-Effekt `type: strength_modifier` (Zielwert „+1 S nach Charge") wurde bei Plan 025 Step 6 aus der Engine entfernt (war toter Pfad, nie konsumiert). Braucht eigene `strength_if_charged`-Verdrahtung analog Hungry Void D2 (auch Charge-bedingt). YAML → `type: strength_if_charged, value: 1, phase: melee`.

## B-055 — Army List UX weniger Scrollen

**Herkunft:** §2 Alt-`backlog.md` Z.384–389 (Refinement-Skizze IMG_4051, S94 gesichert).
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** IMG_4051.
**Betroffene Dateien:** —
**Abhängigkeiten (Begründung):** Offene technische Frage: Reorder/Auto-Scroll in Streamlit überhaupt sauber umsetzbar? → zuerst klären.
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Drei Bausteine: (a) abgehandelte Unit-Card automatisch ans **Ende** der Armeeliste schieben; (b) nach **Phasenwechsel** den Fokus auf die nächste relevante Unit-Card setzen; (c) optionales manuelles **Umsortieren/Switch** von Cards. Eigener Plan, zuerst Streamlit-Machbarkeit klären.

## B-056 — Quantum Shielding fester Invuln Wert

**Herkunft:** §2 Alt-`backlog.md` Z.390–398 (Refinement-Skizze IMG_4041, S94 gesichert; S148-UI-Befund).
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** `docs/handoff/S148_ui_verifikation.md` Prüfblock 1; `docs/work/wahapedia_necrons/`.
**Betroffene Dateien:** —
**Abhängigkeiten (Begründung):** Überschneidet sich mit dem SAVE-/Invuln-Badge-Bereich (Plan 017 / B-043).
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Setzt den Rettungswurf (Invuln) auf einen **festen Wert (4+)** — keine additive Modifikation, kein Modifier-Pfeil in der Würfelanzeige. Eigener Mechanik-Typ „Invuln auf festen Wert setzen" (vs. der bestehenden additiven Modifier-Logik) nötig. **S148-UI-Befund (Annihilation Barge):** unmod. Wound 1–3 misslingt bei Quantum-Shielding-Einheiten immer — wird aktuell **nicht** als Debuff in der Wound-Zeile (3× ✕) noch als Buff im Save-Block angezeigt. Regeltext vorher gegen `docs/work/wahapedia_necrons` verifizieren.

## B-057 — Waffen Block Rapid Fire Count und Range anzeigen

**Herkunft:** §2 Alt-`backlog.md` Z.399–403 (Refinement-Skizze IMG_4038, S94 gesichert).
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** IMG_4038.
**Betroffene Dateien:** Waffen-Auswahl-Block Schussphase.
**Abhängigkeiten (Begründung):** Verwandt mit der Eligibility-Anzeige der Schussphase und dem Silent-King-Ziel-pro-Waffe-Finding (B-045).
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Je Waffe die **Anzahl Attacken inkl. Rapid Fire** sowie die **Reichweite** anzeigen; eligible vs. nicht-eligible Waffen visuell absetzen (durchgestrichen/ausgegraut statt nur ausgeblendet). Eigener Plan.

## B-058 — Dynastie Code je Einheit statt Roster Ebene

**Herkunft:** §2 Alt-`backlog.md` Z.404–408 (Konzept-Frage 2 aus `S139_dynastie_protokoll_konzept.md`, Stakeholder-Entscheid S140).
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** `S139_dynastie_protokoll_konzept.md`.
**Betroffene Dateien:** `subfaction_value_for`-Konsumenten (`abilityEngine`, `gameState`, `armyCard`).
**Abhängigkeiten (Begründung):** Eigenes Konzept vor Umsetzung nötig; verwandt B-002/B-003.
**Agent/Tier:** Planner → Executor
**Benötigte Regeln/Scopes:** —
**Detail:** `subfaction_value_for` liest die Subfaction heute auf **Roster-Ebene**; regelseitig trägt jede Einheit den Dynastie-Code. Prüfen, ob Einheiten-Ebene nötig ist (Mixed-Dynasty-Roster) und die Konsumenten entsprechend umstellen.

## B-059 — Regel Index fuer Wahapedia Texte

**Herkunft:** §2 Alt-`backlog.md` Z.409–412 (context-audit-S91, verarbeitet S118).
**Typ:** Prozess/Doku
**Belege/Recherche:** —
**Betroffene Dateien:** `docs/work/rule_index.md` (neu).
**Abhängigkeiten (Begründung):** Beschleunigt künftige Haiku-Lookups.
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Additiver Stichwort→`datei:zeilenbereich`-Index (Format: `Lethal Hits → core_rules.txt:1420-1435`) — ~23k Zeilen Regeltext sind nur per `grep` durchsuchbar; kein Wortlaut wird dabei berührt.

## B-060 — CLAUDE md Token Disziplin entschlacken

**Herkunft:** §2 Alt-`backlog.md` Z.413–416 (context-audit-S91, verarbeitet S118).
**Typ:** Prozess/Doku
**Belege/Recherche:** `docs/governance/operating_model.md` Event 6.
**Betroffene Dateien:** `CLAUDE.md`.
**Abhängigkeiten (Begründung):** Freigabepflichtig (CLAUDE.md-Änderung).
**Agent/Tier:** Stakeholder → Executor
**Benötigte Regeln/Scopes:** —
**Detail:** `session_context.py`-Implementierungsdetails (Transcript-Pfad, Regex-Fallstrick S65) aus dem Token-Disziplin-Abschnitt nach `operating_model.md` Event 6 verlagern; in CLAUDE.md nur 2-Zeilen-Verweis.

## B-061 — Backlog Paragraph 0 Hygiene

**Herkunft:** §2 Alt-`backlog.md` Z.417–418 (context-audit-S91, verarbeitet S118).
**Typ:** Prozess/Doku
**Belege/Recherche:** —
**Betroffene Dateien:** `backlog.md` (durch diese Migration bereits obsolet).
**Abhängigkeiten (Begründung):** **Überlappt inhaltlich mit B-007 (Backlog-Restrukturierung) — bei Umsetzung zusammenlegen.** Mit der S151-Migration effektiv erledigt (§0 existiert in der Neufassung nicht mehr).
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** §0-Überschrift „S51" datieren; erledigte ✅-Einträge inline nach `session_archive.md`-Historie auslagern statt stehen lassen. Durch die Backlog-Restrukturierung (B-007, dieser Auftrag) strukturell überholt — §0 als Abschnitt existiert in der Neufassung nicht mehr.

## B-062 — Audit Plaene bereinigen

**Herkunft:** §2 Alt-`backlog.md` Z.426–430 (Stakeholder-Auftrag S122, für S123+).
**Typ:** Prozess/Doku
**Belege/Recherche:** Anlass Plan-015-Step-1-Befund S122.
**Betroffene Dateien:** `docs/audit/plans/` + README-Queue.
**Abhängigkeiten (Begründung):** Jeden Plan gegen Code + `git log` verifizieren, nicht nur Statuszeilen lesen.
**Agent/Tier:** Executor — **Tier: Sonnet** (Abgleich mit Bewertung, kein reiner Lookup)
**Benötigte Regeln/Scopes:** —
**Detail:** Subagent-Durchgang über `docs/audit/plans/` + README-Queue — erledigte/überholte Pläne archivieren bzw. Status korrigieren.

## B-063 — Boarding Actions Stratagems laden

**Herkunft:** §2 Alt-`backlog.md` Z.431–440 (Stakeholder-Entscheid S122, → ziel7 Stufe C).
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** `docs/handoff/S147_go_audit_stratagems.md` (Lücken-Tabelle).
**Betroffene Dateien:** `necrons/stratagems.yaml`.
**Abhängigkeiten (Begründung):** Blockiert bis ziel7 Stufe C (hängt an B-003); Bereinigung anderer BA-only-Einträge bereits erledigt S134 (Archiv A-021).
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** NANOSCARAB VIRUS + MINDSHACKLE SCARABS in `necrons/stratagems.yaml` aufnehmen, sobald die Hatchway-Abhängigkeit geklärt ist (Entscheid: JA, laden — nicht dauerhaft ausschließen). Nebenbefund (Merkposten für Paket 4/Stufe C): `phase: any` + `event: after_roll` fehlmatcht jeden Advance-/after_roll-Anker — Events künftig wurfspezifisch wählen.

## B-064 — Variable CP Kosten in der UI anzeigen

**Herkunft:** §2 Alt-`backlog.md` Z.441–444 (Stakeholder-Entscheid S122).
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** —
**Betroffene Dateien:** Stratagem-Karte (UI-Design nötig).
**Abhängigkeiten (Begründung):** —
**Agent/Tier:** Design-Crew → Executor
**Benötigte Regeln/Scopes:** —
**Detail:** 5 Necron-Stratagems haben variable Kosten (z. B. „3/1 CP"); YAML trägt bewusst das Minimum, `rule_text` erklärt. UI soll die Variabilität zeigen (z. B. „1 CP (3 CP für TITANIC)") — es wird mit titanischen Einheiten gespielt.

## B-065 — improve Session vorbereiten

**Herkunft:** §2 Alt-`backlog.md` Z.445–450 (Stakeholder-Auftrag S122, für S123+).
**Typ:** Prozess/Doku
**Belege/Recherche:** `/improve`-Skill.
**Betroffene Dateien:** —
**Abhängigkeiten (Begründung):** Bereinigte Plan-Queue (B-062) zuerst, grüne Vollsuite als Baseline.
**Agent/Tier:** Stakeholder → Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Eigene Session für den `/improve`-Skill (read-only Codebase-Audit → priorisierte, in sich geschlossene Umsetzungspläne für Executor-Subagenten). Vorbereitung: bereinigte Plan-Queue, grüne Vollsuite, Scope-Entscheid des Stakeholders (Bugs/Tech-Debt/UX/Roadmap) einholen; Ergebnis-Pläne in die `docs/audit/plans/`-Queue einsortieren. Token-intensiv → eigene Session.

## B-066 — Transport Insassen Feature Embark Disembark

**Herkunft:** §2 Alt-`backlog.md` Z.451–462; Stakeholder-Entscheid S142 (NIEDRIG-Prio).
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** `docs/handoff/S141_ui_befunde_group_b.md` §3–§5 (S141/S142).
**Betroffene Dateien:** Roster-Schema, Loader, Game-State (`embarked_units` analog `melee_with`), Movement-Phase-UI.
**Abhängigkeiten (Begründung):** Voraussetzung, damit die Emergency-Disembarkation-GO-Karte zeigen kann, WELCHE Einheiten aussteigen.
**Agent/Tier:** Planner → Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Insassen-Zuordnung („Einheit X sitzt in Transport Y") fehlt vollständig. 4 Bausteine: (1) Roster-Schema-Feld `embarked_in` pro Unit-Eintrag; (2) Loader liest das Feld + validiert gegen Transportkapazität (heute nur Freitext in der `ABIL`-Zeile); (3) Game-State-Feld `embarked_units` + Embark/Disembark-Mutationen (Movement 3", Destroyed-Fall 3"/6" je Stratagem); (4) UI: Embark/Disembark-Buttons in der Movement-Phase + „eingestiegen in ⟨Transport⟩" auf der Unit-Karte. 2 offene Design-Fragen: (a) nur Start-Zustand im Roster-YAML deklarierbar vs. In-Game-Embark/Disembark über die UI; (b) Kapazität hart durchsetzen vs. nur Text-Hinweis (Klasse B/C). Aufwand S–M.

## B-067 — Roster Builder Anforderung before battle Stratagems

**Herkunft:** §2 Alt-`backlog.md` Z.463–466 (Stakeholder-Verifikation S146).
**Typ:** Prozess/Doku
**Belege/Recherche:** —
**Betroffene Dateien:** —
**Abhängigkeiten (Begründung):** Anforderung für einen künftigen Roster-Builder, kein akuter Task.
**Agent/Tier:** Planner
**Benötigte Regeln/Scopes:** —
**Detail:** `before_battle`-Stratagems (z. B. „Hand of the Phaeron") sind im laufenden Spiel nicht nutzbar — beim Bau des künftigen Roster-Builders berücksichtigen: dort müssen `before_battle`-Stratagems auswählbar/abhandelbar sein.

## B-068 — UX Nit Silent King Zusatzattacken Default

**Herkunft:** §2 Alt-`backlog.md` Z.467–470 (Stakeholder-Verifikation S146).
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** —
**Betroffene Dateien:** —
**Abhängigkeiten (Begründung):** —
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Eingabe der zusätzlichen Attacken (Staff of Stars 4 / Scythe of Dust 3) soll wie bei anderen Einheiten üblich per Default auf dem Maximum vorbelegt sein; aktuell startet der Wert niedriger, was beim Spielen nervt.

## B-069 — camelCase Umbenennung

**Herkunft:** §2 Alt-`backlog.md` Z.482–491 (S148 Brief 7 hat nur die Grundlage gelegt).
**Typ:** Schuldabbau
**Belege/Recherche:** `docs/spec/loader_contract.md` §8 (Mapping-Tabelle: 107 Felder + 3 aufgelöste Kollisionen `modifier`/`target`/`target_keyword`).
**Betroffene Dateien:** YAML + Loader-Code, Necron-Scope (6 Dateien), Ork-Scope (5 Dateien), `adeptus_custodes/faction_abilities.yaml:96`.
**Abhängigkeiten (Begründung):** 4 Teil-Briefs ≤ Effort M: (1) Stratagems `modifier`/`target`-Kollision zuerst (höchstes Risiko bei naivem Rename), (2) restliche Stratagem-Felder, (3) Necron-Ability-Scope, (4) Ork-Ability-Scope inkl. `target_keyword`-Bereinigung + Custodes-Zusatzfund.
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** Executor-Briefs max. Effort M (S130-Auflage).
**Detail:** Migrationsplan + vollständige Mapping-Tabelle liegen fertig unter `loader_contract.md` §8. Die eigentliche Umbenennung in YAML + Loader-Code ist noch offen, in Teil-Briefs ≤ Effort M zu schneiden.

## B-070 — Reanimation Konsistenz Umsetzung

**Herkunft:** §2 Alt-`backlog.md` Z.492–499; Entscheid S148.
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** `docs/handoff/S147_go_audit_stratagems.md` (Lücken-Tabelle „Reanimation Prioritisation / Resurrection Protocols" + Fixing-Plan-Punkt 7).
**Betroffene Dateien:** `necrons/stratagems.yaml:291-303,438-451`, `abilityEngine.py:413`, `armyCard.py:109`.
**Abhängigkeiten (Begründung):** Entscheid bereits gefallen (S148: keine Sonderbehandlung mehr); Effort M/L wegen nötiger Modell-Auswahl-UI.
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Stakeholder-Entscheid: Stratagem-`reanimate` (Reanimation Prioritisation, Resurrection Protocols) wird künftig **genauso** mitgezählt wie die Ability-Variante (Reanimation Protocols) — keine Sonderbehandlung der Stratagem-Variante. Umsetzung als eigenes Ticket.

## B-071 — auto wound prueft keine Gauss Tesla Bedingung

**Herkunft:** §2 Alt-`backlog.md` Z.500–507 (S147-Audit-Restlücke, bewusst nicht in Brief 6/S149 mitgefixt).
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** `docs/handoff/S147_go_audit_stratagems.md` Zeile 41 (Lücken-Tabelle) + Fixing-Plan Punkt 5; `docs/handoff/S147_go_audit_necron_abilities.md` §2; Plan 032 Punkt 5.
**Betroffene Dateien:** `auto_wound`-Effekt-Handler.
**Abhängigkeiten (Begründung):** Die WER-darf-nutzen-Bedingungslücke (`conditions: [GAUSS]`/`[TESLA]`) ist bereits gefixt (Brief 6, S149); dies ist die tiefere, verbleibende Lücke.
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Der `auto_wound`-Effekt selbst (Techno-Oracular Targeting, Disintegration Capacitors) prüft nicht, ob der konkrete Angriff tatsächlich mit einer Gauss-/Tesla-Waffe geführt wurde.

## B-072 — Roster Daten Konsistenz Recherche

**Herkunft:** §2 Alt-`backlog.md` Z.508–512 (S148-UI-Befund, Prüfblock 2).
**Typ:** Schuldabbau
**Belege/Recherche:** `docs/work/wahapedia_necrons`.
**Betroffene Dateien:** `necrons/units.yaml` (CORE-Keyword Annihilation Barge/Flayed Ones), Ork Boss Nob Waffen.
**Abhängigkeiten (Begründung):** Reiner Datenabgleich.
**Agent/Tier:** Executor (Haiku)
**Benötigte Regeln/Scopes:** —
**Detail:** Stakeholder hat das Test-Roster als fehlerhaft befunden — Annihilation Barge war als MWBD-Ziel wählbar, ist laut Stakeholder aber **nicht** CORE. Aufgabe: CORE-Keyword-Abgleich `necrons/units.yaml` vs. `docs/work/wahapedia_necrons` (Annihilation Barge + Flayed Ones mitprüfen) **und** Ork Boss Nob Waffen (Stakeholder-Zweifel: „wirklich nur Stikkbomb?").

## B-073 — model groups Union Ungenauigkeit

**Herkunft:** §2 Alt-`backlog.md` Z.513–518 (S148-Folge, geerbt von `grantsKeyword`/Brief 4).
**Typ:** Schuldabbau
**Belege/Recherche:** —
**Betroffene Dateien:** `derived_keywords`-Ableitungsmechanismus.
**Abhängigkeiten (Begründung):** Keine Regression; bei nächster `model_groups`-Arbeit mitprüfen.
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Der generische `derived_keywords`-Mechanismus bildet die Vereinigung über alle `model_groups` einer Einheit statt pro Gruppe zu differenzieren — bei gemischter Bewaffnung (z. B. nicht jedes Modell trägt die Gauss-Waffe) zeigt die Einheit das Keyword ggf. zu breit.

## B-074 — Ziel7 Stufe C Vorbereitung Emergency Disembarkation

**Herkunft:** §3 Alt-`backlog.md` Z.549–553 (Checkbox `- [ ]`).
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** `data/rosters/orks_transport.yaml` (Evil Sunz, Gunwagon TRANSPORT).
**Betroffene Dateien:** —
**Abhängigkeiten (Begründung):** War zuvor mangels TRANSPORT-Roster blockiert, jetzt möglich (Commit `cbaeeb2`).
**Agent/Tier:** Stakeholder
**Benötigte Regeln/Scopes:** —
**Detail:** Emergency Disembarkation am neuen Ork-Transport-Roster real prüfen. (Klan-Affinität existiert regelseitig nicht, S143-Stakeholder-Klärung, Commit `3602ddb` — als Verifikationspunkt gestrichen; neuer Scope Klan-/Dynastie-Fähigkeiten s. `ziel7.md` Stufe C.)

## B-075 — mypy Rest gameMechanic

**Herkunft:** §4 Alt-`backlog.md` Z.568–586.
**Typ:** Schuldabbau
**Belege/Recherche:** `tools/mypy_gate.py` (Baseline 24, Stand S144).
**Betroffene Dateien:** `attackMath.py` (`type-arg`), `moralePhase.py`/`unitMutations.py` (`no-any-return`/`arg-type`).
**Abhängigkeiten (Begründung):** Eigenständig von B-004 (uiLayout-Teil) — kein `state: dict`-Fall mehr, andere Fehlerklassen.
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** 7 verbleibende Fehler in `gameMechanic/` außerhalb des `state`-Contracts. Baseline in `tools/mypy_gate.py` im selben Commit senken (Ratchet-Regel).

## B-076 — Layer Kopplung gameMechanic importiert uiLayout

**Herkunft:** §4 Alt-`backlog.md` Z.587–589.
**Typ:** Schuldabbau
**Belege/Recherche:** `docs/audit/plans/008-*` (Audit-Plan 008).
**Betroffene Dateien:** `gameMechanic/*Phase.py` (importiert `uiLayout._common`).
**Abhängigkeiten (Begründung):** Bewusst (noch) nicht als Architektur-Wächter erzwungen; verwandt B-077/B-088 (gleicher Render-Hub).
**Agent/Tier:** Planner
**Benötigte Regeln/Scopes:** —
**Detail:** Aufräum-Pfad: Phasen-Render nach `uiLayout/` ziehen.

## B-077 — common py refactoren

**Herkunft:** §4 Alt-`backlog.md` Z.590–592 (Stakeholder-Auftrag S132).
**Typ:** Schuldabbau
**Belege/Recherche:** —
**Betroffene Dateien:** `src/uiLayout/_common.py` (2218 Zeilen).
**Abhängigkeiten (Begründung):** Effort L — **vor Vergabe splitten**; gleicher Render-Hub wie B-076.
**Agent/Tier:** Planner → Executor
**Benötigte Regeln/Scopes:** `docs/reference/agent_scopes.md` (Split-Zuschnitt vor Vergabe).
**Detail:** `_common.py` in logische Teile zerlegen; die Attackensequenz sollte eine eigene Datei werden.

## B-078 — Test Mock Fragilitaet und conftest Mock Hack

**Herkunft:** §4 Alt-`backlog.md` Z.614–621, Z.639–642 (S51 entdeckt; S110-Retro M1+M2).
**Typ:** Schuldabbau
**Belege/Recherche:** S110-Retro.
**Betroffene Dateien:** `tests/gameMechanic/conftest.py` (`sys.modules`-Re-Pointing).
**Abhängigkeiten (Begründung):** Gemeinsame Lösung für beide Retro-Maßnahmen.
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Mehrere `src`-Module lesen das globale `st.session_state` und rufen einander auf (`unitMutations.set_movement_status` → `gameState.units_key_for`; `abilityEngine` → `gameState`/`unitMutations`). Tests mocken `streamlit` **pro Datei**; wer ein Modul zuerst importiert, bindet dessen `st` — reihenfolge-abhängig und zerbrechlich (S51: ein neuer Test als erster Importer brach 15 Movement-Tests). Workaround: Akzeptanztest importiert `gameState` lazy. Saubere Lösung: **eine geteilte `streamlit`-Fixture** (conftest) + Tests auf `module.st` statt lokalem `_st_mock` umstellen — ersetzt zugleich den reihenfolge-abhängigen `conftest.py`-Quick-Fix durch eine **session-scoped Streamlit-Mock-Fixture**, die alle `gameMechanic`-Tests einheitlich nutzen.

## B-079 — DRY Plus Minus Eins Cap Helper

**Herkunft:** §4 Alt-`backlog.md` Z.622–624 (S110-Retro-M1).
**Typ:** Schuldabbau
**Belege/Recherche:** —
**Betroffene Dateien:** `src/uiLayout/diceHtml.py` (`_render_dice_roll_block`, `_render_dice_wound_block`).
**Abhängigkeiten (Begründung):** Kleiner Refactor, kein Verhaltenswechsel.
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Hit- und Wound-Block teilen identische ±1-Cap-Logik → gemeinsamen Helper extrahieren; Tests müssen weiter grün bleiben.

## B-080 — DRY Zwei Sechs Cap Quelle

**Herkunft:** §4 Alt-`backlog.md` Z.625–631 (S144-Review Befund 2).
**Typ:** Schuldabbau
**Belege/Recherche:** —
**Betroffene Dateien:** `src/gameMechanic/combat.py:207,213` (`resolve_attack_modifiers`), `src/uiLayout/diceHtml.py:31` (`_capped_modifier_threshold`).
**Abhängigkeiten (Begründung):** Kein akuter Bug, niedrige Priorität — Sync-Risiko bei künftigen Änderungen.
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Der 9E-Cap (Hit/Wound: unmod. 6 immer Erfolg, unmod. 1 immer Fehlschlag) existiert doppelt. Aktuell konsistent gefixt. Langfristig `_capped_modifier_threshold` als dünnen Wrapper um die combat-Cap-Logik führen oder die Zwischen-Modifier-Zeilen ebenfalls aus `atk_result` speisen (eine Cap-Quelle).

## B-081 — DRY Directive Aktiv Logik

**Herkunft:** §4 Alt-`backlog.md` Z.632–638 (S143-Refactor-Befund Punkt 4, Entscheid S144).
**Typ:** Schuldabbau
**Belege/Recherche:** —
**Betroffene Dateien:** `src/gameMechanic/gameState.py:242-283` (`active_round_choice_buff_labels`), `abilityEngine._active_directive_effects`.
**Abhängigkeiten (Begründung):** Wiederverwendung scheitert am Import-Zyklus (`abilityEngine` importiert bereits aus `gameState`); braucht ein drittes, tieferliegendes Modul. Kein akuter Bug, niedrige Priorität.
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** `gameState.active_round_choice_buff_labels` (UI-Labels) dupliziert einen Teil der „welches Directive ist aktiv"-Logik aus `abilityEngine._active_directive_effects` (Rechen-Seite) — Sync-Risiko analog Cap-DRY (B-080): Regeländerung an einer Stelle ⇒ Anzeige ≠ Rechnung.

## B-082 — Executor Auftrags Checkliste haerten

**Herkunft:** §4 Alt-`backlog.md` Z.643–647 (S110-Retro-M4).
**Typ:** Prozess/Doku
**Belege/Recherche:** Lehre aus S110-Lauf 2b (161k Token/66 min ohne Cap).
**Betroffene Dateien:** `docs/reference/agent_scopes.md`.
**Abhängigkeiten (Begründung):** Bei nächster Scope-Pflege einarbeiten.
**Agent/Tier:** Planner
**Benötigte Regeln/Scopes:** `docs/reference/agent_scopes.md` (Executor-Brief-Checkliste).
**Detail:** Executor-Brief muss echtes `ruff`/pre-commit **VOR** dem „grün"-Claim verlangen (nicht nur pytest). Außerdem: Token-/Zeit-Budget-Cap im Auftrag gegen Rabbit-Holes; Schätzung + harter Stop-Punkt obligatorisch.

## B-083 — architecture md Doku Session

**Herkunft:** §4b Alt-`backlog.md` Z.651–674 (Abgleich 2026-06-15).
**Typ:** Prozess/Doku
**Belege/Recherche:** `docs/spec/design_colors.md` (kanonisch für Colour System).
**Betroffene Dateien:** `docs/spec/architecture.md`.
**Abhängigkeiten (Begründung):** Freigabepflichtig — vor Änderung freigeben.
**Agent/Tier:** Stakeholder → Executor
**Benötigte Regeln/Scopes:** —
**Detail:** `architecture.md` ist teils veraltet (Gesamtbild stimmt, Details nicht): (1) **session_state-Schema** nennt `unit_state` ohne `group_models`/`group_wounds` (real in `gameState.py`), Armee ohne `dynasty`/`protocol_order` (real vorhanden), Datei-Name-Drift „`state.py`" → real `gameState.py`. (2) **Colour System** beschreibt `COLOR_*`-Aliase „als CSS in app.py" — das Live-Theme sind aber `--arb-*`-Variablen in `gameHeader.py`; kanonisch ist `design_colors.md`, die `COLOR_*` (Tailwind-Extrakte in `constants/colors.py`) existieren noch, treiben das Theme aber nicht. (3) **uiLayout „No game logic in this layer"** ist widerlegt durch `_common.py` (Attack-Mathe wurde deshalb nach `attackMath.py` ausgelagert, s. Layer-Kopplung B-076). (4) **Refactoring Plan / Open Design Questions** ist historisch, alle Phasen erledigt, viele Fragen beantwortet → als Historie kennzeichnen. Dazu zwei Doku-Altlasten mitzuziehen: `faction_abilities.md` Z.42/197 referenziert noch das entfernte `auto_round_1`-Flag (6e Bug 1, Regeln erlauben freie Verteilung der Protokolle auf Runden 1–5).

## B-084 — Mortal Wounds Text Match Erkennung

**Herkunft:** §4b Alt-`backlog.md` Z.676.
**Typ:** Schuldabbau
**Belege/Recherche:** —
**Betroffene Dateien:** `_detect_weapon_special` (`"mortal wound" in abilities.lower()`).
**Abhängigkeiten (Begründung):** Kein akuter Block.
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Nutzt Text-Match statt eines strukturierten YAML-Feldes. Technische Schuld.

## B-085 — faction abilities md Kategorie 6 veraltet

**Herkunft:** §4b Alt-`backlog.md` Z.677–682 (S144-Fund, migriert S150).
**Typ:** Prozess/Doku
**Belege/Recherche:** `docs/goals/ziel7.md` Stufe C §K1.
**Betroffene Dateien:** `docs/spec/faction_abilities.md` Kategorie 6.
**Abhängigkeiten (Begründung):** Blockiert, bis K2+ (B-003) umgesetzt ist.
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Behauptet „Größtenteils abgedeckt durch `triggered`-Abilities in `faction_abilities.yaml`" — das ist falsch: Klan-Kulturs/Dynastic Codes liegen in `subfaction_abilities.yaml` (anderer Datei-Scope) und sind laut `ziel7.md` Stufe C §K1 Kern-Befund aktuell nicht wirksam. Spec-Nachzug empfohlen, sobald K2+ umgesetzt ist.

## B-086 — Test Schuld klein Tautologie Tests

**Herkunft:** §4d Alt-`backlog.md` Z.712–723 (DoD-Review S114, Follow-up S118-M2).
**Typ:** Schuldabbau
**Belege/Recherche:** —
**Betroffene Dateien:** `tests/gameMechanic/test_damage_block_reanimation.py` (Z.394–401, Z.403–417); 11 Testdateien mit Modul-Level-`sys.modules["streamlit"]`-Mocks.
**Abhängigkeiten (Begründung):** Kein Blocker; bei Gelegenheit/bei nächster Test-Infra-Arbeit mitnehmen. Verwandt B-078.
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Zwei Tautologie-Tests: Z.394–401 rechnet `4*2==8` selbst nach (kein echter System-Under-Test-Nachweis); Z.403–417 prüft nur Fixtures statt RP-Gate-Logik. Zusätzlich: `tests/gameMechanic/conftest.py` hat inzwischen die session-scoped Fixture `_canonical_streamlit_mock`, die per-File-Mocks vor dem ersten src-Import sind aber noch in 11 Testdateien dezentral — konsolidieren.

## B-087 — F4 Stufe A Verifikationspunkte 3 und 4

**Herkunft:** §5 Alt-`backlog.md` Z.770–774 (S121-UI-Verifikation Findings).
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** `docs/audit/plans/015-contextual-reactive-stratagems.md` (Priorität P2), `docs/audit/plans/README.md`.
**Betroffene Dateien:** —
**Abhängigkeiten (Begründung):** Braucht Plan 015 (reaktive Stratagem-UI).
**Agent/Tier:** Stakeholder (reine Prüfung)
**Benötigte Regeln/Scopes:** —
**Detail:** Punkte 3+4 der Ziel7-Stufe-A-Checkliste (Fire Overwatch/Counter-Offensive, `timing: phase_reactive`) waren NICHT prüfbar — sie brauchen die reaktive Stratagem-UI aus Plan 015. Schaltet damit auch die Reaktiv-UI-Prüfung frei.

## B-088 — Richtungsentscheid Ziel9 Fetcher vorziehen

**Herkunft:** §5 Alt-`backlog.md` Z.777–779 (Audit S124, aus `next_session.md` verschoben S129).
**Typ:** Prozess/Doku
**Belege/Recherche:** —
**Betroffene Dateien:** —
**Abhängigkeiten (Begründung):** Stakeholder-Entscheidung nötig, bisher nicht gefallen.
**Agent/Tier:** Stakeholder
**Benötigte Regeln/Scopes:** —
**Detail:** Ziel9-Fetcher vorziehen? Eigene Deployment-Phase bauen oder ADR „bleibt am Tisch"? Mission-Scoring (eine Mission end-to-end)? Noch nicht entschieden, Stakeholder-Input nötig. Blockiert indirekt B-090 (Ziel 9).

## B-089 — Ziel 8 Crusade Erweiterung

**Herkunft:** §5 Alt-`backlog.md` Z.775; `index.md` Z.45.
**Typ:** Fachlichkeit (Ziel 7) — *tatsächlich Ziel 8, kein Ziel-7-Scope; Typ-Enum kennt keine eigene „geplantes Ziel"-Kategorie, daher hier eingeordnet.*
**Belege/Recherche:** `docs/goals/ziel8.md`.
**Betroffene Dateien:** —
**Abhängigkeiten (Begründung):** Noch nicht begonnen; Effort L — bei Aufnahme splitten.
**Agent/Tier:** Planner
**Benötigte Regeln/Scopes:** —
**Detail:** Crusade-Erweiterung (geplant). Details in `ziel8.md`.

## B-090 — Ziel 9 Wahapedia Faction Fetcher

**Herkunft:** §5 Alt-`backlog.md` Z.776; `index.md` Z.45.
**Typ:** Fachlichkeit (Ziel 7) — *tatsächlich Ziel 9, kein Ziel-7-Scope; s. Anmerkung bei B-089.*
**Belege/Recherche:** `docs/goals/ziel9.md`.
**Betroffene Dateien:** —
**Abhängigkeiten (Begründung):** Noch nicht begonnen; Effort L — bei Aufnahme splitten; Richtungsentscheid B-088 offen.
**Agent/Tier:** Planner
**Benötigte Regeln/Scopes:** —
**Detail:** Wahapedia Faction Fetcher (geplant). Details in `ziel9.md`.

## B-091 — Design Block UI Theme

**Herkunft:** `index.md` Z.46, Z.52–56.
**Typ:** Fachlichkeit (Ziel 7) — *eigenständiger Design-Block, kein Ziel-7-Scope; s. Anmerkung bei B-089.*
**Belege/Recherche:** —
**Betroffene Dateien:** Farbpalette/Goldtöne, Badges, Einheitenkarten-Layout.
**Abhängigkeiten (Begründung):** 3 Teilpunkte, bündeln oder einzeln vergeben.
**Agent/Tier:** Design-Crew
**Benötigte Regeln/Scopes:** —
**Detail:** Eigene Session, noch nicht begonnen: (1) Farbpalette überarbeiten — Goldtöne, Primärfarbe, Kontraste; (2) Badge-Optik und Spacing prüfen; (3) Einheitenkarten-Layout verfeinern.

## B-098 — Boss Nob 7b Kombi Waffenprofile

**Herkunft:** `next_session.md` (S150, Punkt 5) / Stakeholder-Verifikation S146-Umfeld; als Waisen-Item ohne Backlog-ID im S151-C-Umbau gefunden (`docs/handoff/S151_briefing_umbau.md`), nachgetragen S151.
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** `docs/work/wahapedia_orks/` (Kombi-Waffenprofile gegen Wahapedia prüfen).
**Betroffene Dateien:** `data/wh40k_9e/orks/weapons.yaml`
**Abhängigkeiten (Begründung):** Daten-Fix, kein Code-Blocker; stand in der alten next_session-Priorisierung (Punkt 5) zusammen mit dem K1-Daten-Fix (B-002) und Quantum Shielding (B-056) — daher direkt hinter B-002 einsortiert.
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Boss Nob 7b — Kombi-Waffenprofile fehlen in `orks/weapons.yaml`. Zweigeteiltes Vorgehen: (1) erst die fehlenden Profile ergänzen, (2) dann die ODER-Gruppe (alternative Profile derselben Waffe) modellieren.

---

## B-092 — GO UI Paket 1 GO Karten Baustein stale Glyph Verdacht

**Herkunft:** Inventar Tabelle 3, U-001; Alt-`backlog.md` §2, Z.154–155.
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** `src/uiLayout/goCard.py`, `docs/spec/design_system.md` §6.1.
**Betroffene Dateien:** —
**Abhängigkeiten (Begründung):** Logisch widersprüchlich mit Paket 3a (baut direkt auf diesem Baustein auf und ist bereits ✅ erledigt S133).
**Agent/Tier:** Planner (Klärung vor Zuweisung)
**Benötigte Regeln/Scopes:** —
**Detail:** ⚠ Stale-Verdacht (Inventar-Beleg): Glyph 🟢 (offen), aber Paket 3a (baut direkt auf dem Baustein auf) ist bereits ✅ erledigt S133 — logisch unmöglich ohne fertigen Paket-1-Baustein. Vor Weiterverarbeitung gegen `src/uiLayout/goCard.py`/`design_system.md` §6.1 verifizieren, ob der Baustein längst existiert (dann → Archiv) oder ob der Titel nur unvollständig eingelöst wurde. Stakeholder-Klärung bei nächster Bereinigung.

## B-093 — GO UI Paket 2 Command Re Roll stale Glyph Verdacht

**Herkunft:** Inventar Tabelle 3, U-002; Alt-`backlog.md` §2, Z.156–157.
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** Commit `35cc2a2` („Close S136: … command re-roll 9/9 …").
**Betroffene Dateien:** —
**Abhängigkeiten (Begründung):** —
**Agent/Tier:** Planner (Klärung vor Zuweisung)
**Benötigte Regeln/Scopes:** —
**Detail:** ⚠ Stale-Verdacht (Inventar-Beleg): Glyph 🟢 (offen), aber `git log` zeigt Commit `35cc2a2` „Close S136: … command re-roll 9/9 …" — deutet auf vollständige Umsetzung hin (Command Re-Roll für Advance/Charge). Vor Weiterverarbeitung gegen Commit + `backlog_archive.md`-Eintrag „Command Re-Roll auf alle 9 Wurf-Arten ausweiten" abgleichen — vermutlich bereits Teilmenge davon. Stakeholder-Klärung bei nächster Bereinigung.

## B-094 — GO Buttons kontextuell in gameActionArea

**Herkunft:** Inventar Tabelle 3, U-003; Alt-`backlog.md` §2, Z.318.
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** GO-UI-Design-System-Roadmap (Pakete 1–6, B-013 bis B-016).
**Betroffene Dateien:** GameActionArea.
**Abhängigkeiten (Begründung):** —
**Agent/Tier:** Planner (Klärung vor Zuweisung)
**Benötigte Regeln/Scopes:** —
**Detail:** ⚠ Stale-Verdacht (Inventar-Beleg): kein Session-Anker, keine Datei-Referenz im Alt-Backlog; Thema klingt bereits durch die GO-UI-Design-System-Roadmap (Pakete 1–6, insbesondere Paket 6 „Einheiten-Auswahl in GameActionArea ziehen", B-016) abgedeckt/überholt. Nicht sicher, ob noch eigenständig relevant. Ursprungstext: „GO-Buttons kontextuell in gameActionArea (aktiver + inaktiver Spieler) statt Liste." Stakeholder-Klärung bei nächster Bereinigung.

## B-095 — Necron Command Phase Regelkasten immer oben

**Herkunft:** Inventar Tabelle 3, U-004; Alt-`backlog.md` §2, Z.319.
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** —
**Betroffene Dateien:** —
**Abhängigkeiten (Begründung):** —
**Agent/Tier:** Planner (Klärung vor Zuweisung)
**Benötigte Regeln/Scopes:** —
**Detail:** ⚠ Stale-Verdacht (Inventar-Beleg): kein Session-Anker, keine Datei-Referenz — Alter/Aktualität nicht bestimmbar. Ursprungstext: „Necron Command Phase: Regelkasten immer ganz oben (alle Phasen prüfen)." Stakeholder-Klärung bei nächster Bereinigung.

## B-096 — Bug aktive GO Effekte ohne Badge am Wirkort

**Herkunft:** Inventar Tabelle 3, U-005; Alt-`backlog.md` §2, Z.471–481.
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** `docs/handoff/S147_go_audit_stratagems.md` (Befundkatalog, alle 4 GOs).
**Betroffene Dateien:** —
**Abhängigkeiten (Begründung):** —
**Agent/Tier:** Planner (Klärung vor Zuweisung)
**Benötigte Regeln/Scopes:** —
**Detail:** ⚠ Stale-Verdacht (Inventar-Beleg): (a) Auto-Wound-GOs „Techno-Oracular Targeting" (kein Wound-Wurf, automatischer Wound) und „Disintegration Capacitors" (Gauss, unmodifizierte 6 beim Hit → Auto-Wound) zeigen keinen Badge/Hinweis am Wound-Block; (b) „Relentless Onslaught" (Rapid Fire, 6 beim Hit → Zusatztreffer) und „Solar Pulse" (Ziel verliert Cover) ohne Badge am Hit- bzw. Save-Block. Text im Alt-Backlog sagt „geht als Teilmenge im GO-Audit auf … Umsetzung über die Audit-Fixing-Pläne in S148" — nicht belegt, ob die 4 konkreten GOs durch die S148-Fixes tatsächlich abgedeckt wurden oder ob ein Rest bleibt. Gegen den aktuellen Stand von B-071 (auto_wound-Gauss/Tesla-Lücke) und die S148-Fixing-Pläne verifizieren. Stakeholder-Klärung bei nächster Bereinigung.

## B-097 — Command Protocol Direktiven nicht regelkonform S95 Befund

**Herkunft:** Inventar Tabelle 3, U-006; Alt-`backlog.md` §4b, Z.683–700.
**Typ:** Fachlichkeit (Ziel 7)
**Belege/Recherche:** `docs/audit/plans/archive/025-protocol-9e-conformance.md` (archiviert); §0-Tabelle (Alt-`backlog.md` Z.89–100, Protokoll-Buff-Audit).
**Betroffene Dateien:** `data/wh40k_9e/necrons/faction_abilities.yaml`.
**Abhängigkeiten (Begründung):** —
**Agent/Tier:** Planner (Klärung vor Zuweisung)
**Benötigte Regeln/Scopes:** —
**Detail:** ⚠ Stale-Verdacht (Inventar-Beleg, 🔴-Glyph): Beschreibt den Ausgangsbefund zu Plan 025 (Command-Protocol-Direktiven weichen von den echten 9E-Protokollen ab, `docs/work/wahapedia_necrons/faction_overview.txt` Z.583 ff.), doch Plan 025 ist laut Pfadangabe bereits **archiviert** (`docs/audit/plans/archive/025-protocol-9e-conformance.md`) und dessen Einzelschritte sind an anderer Stelle im selben Alt-Dokument (§0-Tabelle, B-010) bereits mit ✅ als erledigt markiert. Der 🔴-Glyph wirkt stale; vor Archivierung verifizieren, dass alle 6 Plan-025-Steps tatsächlich abgeschlossen sind (insbesondere Eternal Guardian S, die laut B-010 noch offen ist). Stakeholder-Klärung bei nächster Bereinigung.

## B-099 — Backlog Feinschliff Stakeholder Auflagen S151

**Herkunft:** Stakeholder-Chat S151, 2026-07-16.
**Typ:** Prozess/Doku
**Belege/Recherche:** `docs/handoff/S151_backlog_inventar.md` (Stale-Verdachtskandidaten B-092–B-097).
**Betroffene Dateien:** `docs/goals/backlog.md`, `docs/goals/backlog_details.md`.
**Abhängigkeiten (Begründung):** Kein Blocker; Punkt (4) braucht vorab einen Blick in `tools/token_report.py` als Basis für die Tokenverbrauch-Ausweisung.
**Agent/Tier:** Executor
**Benötigte Regeln/Scopes:** —
**Detail:** Fünf Stakeholder-Auflagen (S151) für den nächsten Backlog-Feinschliff, wörtlich sinngetreu festgehalten:
(1) Stale-Verdachtskandidaten B-092–B-097 ersatzlos aus Liste+Details löschen — „kommt wieder, wenn etwas fehlt".
(2) Beschreibung-Spalte mehrzeilig: nach Zeilenumbruch (`<br>`) unter der Beschreibung den Typ der Aufgabe angeben; nach weiterem Umbruch bei Status Blocked den Blocker (z. B. ID eines anderen Items).
(3) Erste Spalte (ID) ~30–40 % breiter, sodass die ID einzeilig bleibt.
(4) Effort-Angabe von Zeit-Kategorien auf Token umstellen (z. B. „Mio. Token") für Kostenabschätzung; zusätzlich nach Abschluss jeder Aufgabe/Session den tatsächlichen Gesamt-Tokenverbrauch ausweisen (explizit verbrauchte Token, nicht nur Kontextfenster — `tools/token_report.py` als Basis prüfen).
(5) Details-Template: Zeilenumbrüche zwischen den Feldern (Sichtbarkeit), ID-Überschrift verlinkt zurück auf die Backlog-Liste (bidirektional); neue Feld-Reihenfolge: Typ / Status / Tier / Effort / Detail-Beschreibung / Abhängigkeiten / Belege / Benötigte Regeln-Scopes / Herkunft.
