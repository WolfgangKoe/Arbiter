# Backlog — Details

> **Zweck:** Diese Datei trägt die ausführliche Begründung/Herkunft je Backlog-Item, damit
> [backlog.md](backlog.md) eine schlanke Ein-Zeile-pro-Item-Liste bleiben kann. Jeder Abschnitt
> ist über die ID verlinkt (`backlog.md` verweist per Anker hierher, `## B-NNN` verlinkt per
> `[↩ Zeile in backlog.md]` zurück — bidirektional, S152-Auflage 5) — Änderungen an einem Item
> immer hier vornehmen, `backlog.md` nur die Kurzzeile pflegen.

## Feldschema (Template)

Jedes Item trägt genau diese neun Felder, in dieser Reihenfolge, mit einer Leerzeile
zwischen den Feldern (Sichtbarkeit, S152-Auflage 5):

- **Typ:** `Schuldabbau` | `Fachlichkeit (Ziel 7)` | `Prozess/Doku` — identisch mit dem
  gefärbten Typ-Tag in der Beschreibungsspalte von `backlog.md`, inklusive desselben
  Farb-Spans (Farb-Zuordnung in der Legende dort).
- **Status:** identisch mit der Status-Spalte in `backlog.md` (Werte aus `_VALID_STATUSES`).
- **Tier:** Rolle + Modell-Tier (Haiku-Default bei reinem Lookup, Sonnet sonst, Opus nur mit
  Begründung).
- **Effort:** Token-Schätzung, identisch mit der Effort-Spalte in `backlog.md`
  (Umrechnungs-Konvention dort in der Legende dokumentiert).
- **Detail-Beschreibung:** Ausführlicher, aus der Alt-`backlog.md` übernommener Text
  (verlustfrei kondensiert — Fakten, Links, Entscheide, betroffene Dateien, Code-Referenzen).
- **Abhängigkeiten:** Was blockiert/parallelisiert dieses Item und warum.
- **Belege:** Links auf Handoffs/Screenshots/Specs — verweist, dupliziert nicht.
- **Benötigte Regeln-Scopes:** Verweis auf `operating_model.md`/`agent_scopes.md`, nur wenn
  bekannt.
- **Herkunft:** Session/Anlass/Foto-Referenz, aus der das Item entstand.

Unbekannte Felder tragen `—` (kein Platzhaltertext). Jede `## B-NNN`-Überschrift trägt direkt
darunter `[↩ Zeile in backlog.md](backlog.md#b-nnn)` — Ziel-Anker sitzt dort als `<a id="b-nnn">`
am Anfang der Beschreibungsspalte.

---

## B-001 — FixD Brief 2 und 3 Compute Render Folge

[↩ Zeile in backlog.md](backlog.md#b-001)

**Typ:** <span style="color:#c2410c">**Schuldabbau**</span>

**Status:** Blocked

**Tier:** Executor

**Effort:** ~35k

**Detail-Beschreibung:** Betroffene Dateien: `src/uiLayout/_common.py` (gleiche Datei wie Rang 2/9, daher Serie). Teil der FixD-Serie (Compute/Render-Trennung in `_common.py`). Brief 1 (Rang 4) ist S150 erledigt und entblockt Brief 2+3 sowie den mypy-uiLayout-Abbau (B-004). Brief 2 wartet auf ein Mockup, Brief 3 zieht nur die zugehörige Spec nach.

**Abhängigkeiten:** Brief 2 hinter einem Mockup-Gate; Brief 3 ist reiner Spec-Nachzug; beide sequenziell nach Brief 1 (Dateikonflikt `_common.py`).

**Belege:** `docs/audit/plans/README.md` (Plan-Status), Prioritätenliste-Herleitung in Alt-`backlog.md` Z.23–33.

**Benötigte Regeln-Scopes:** —

**Herkunft:** Prio-Rang 5 (S145-Prioritätenliste), Folge von Rang 4 (Brief 1, erledigt S150).

## B-003 — Klan Dynastie K2 Plus Novokh Sautekh Nephrekh und Ork Snakebites

[↩ Zeile in backlog.md](backlog.md#b-003)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Planner → Executor

**Effort:** ~70k+ — vor Vergabe splitten

**Detail-Beschreibung:** Betroffene Dateien: `subfaction_abilities.yaml` (Necron+Ork), Engine-Filter (Modul analog `subfactionPassives.py`). Wortlaut-Fix für Novokh/Sautekh/Nephrekh (Necron-Dynastien) + Ork Snakebites, dazu Engine-Filter, `subfaction_passive`-Migration, 4 neue Effekttypen, ein Badge, und der Spec-Nachzug in `faction_abilities.md` Kategorie 6. Größter offener Klan/Dynastie-Block.

**Abhängigkeiten:** Macht 13 Backlog-Einträge erstmals wirksam; Effort L — **vor Vergabe in ≤ M-Briefs splitten** (S130-Auflage). **S152-Review-Befund (Retro-Maßnahme M4):** B-002 (K1-Wortlaut-Fix) hat bereits neue deklarative `effect`-Subtypen in die YAML-Daten eingeführt (`multi`, `range_bonus`, `buff_ap`, `objective_secured`, `ap_override_if_neg1`, s. `data/wh40k_9e/necrons/subfaction_abilities.yaml` Nihilakh/Mephrit) — diese Subtypen haben noch **keinen Engine-Handler**, sind also aktuell wirkungslos. B-003 (K2+) muss diese Handler mit aufnehmen, nicht nur die 4 dort genannten neuen Effekttypen isoliert betrachten.

**Belege:** `docs/goals/ziel7.md` Stufe C §K1; `docs/spec/faction_abilities.md` Kategorie 6 (Spec-Nachzug nötig, s. B-085).

**Benötigte Regeln-Scopes:** `docs/reference/agent_scopes.md` (Split-Zuschnitt vor Vergabe).

**Herkunft:** Prio-Rang 7 (S145-Prioritätenliste).

## B-004 — mypy Ratchet uiLayout

[↩ Zeile in backlog.md](backlog.md#b-004)

**Typ:** <span style="color:#c2410c">**Schuldabbau**</span>

**Status:** Blocked

**Tier:** Executor

**Effort:** ~35k

**Detail-Beschreibung:** Betroffene Dateien: `src/uiLayout/armyCard.py`, `gameProtocoll.py`, `unitCard.py`, `armyList.py`, `detachmentCard.py` (17 Fehler gesamt). Letzter Rest des mypy-Abbaus (Baseline 24, Stand S144) — der `uiLayout/`-Teil (17 Fehler) braucht manuelle Render-Verifikation, da Render-Code außerhalb der Coverage-Messung liegt. Pro Schritt Baseline in `tools/mypy_gate.py` im selben Commit senken (Ratchet-Regel).

**Abhängigkeiten:** Blockiert bis Rang 5 (B-001) fertig ist — Dateiüberschneidung `_common.py` mit FixD.

**Belege:** `docs/spec/architecture_invariants.md` (Typ-Ratchet), `tools/mypy_gate.py`.

**Benötigte Regeln-Scopes:** —

**Herkunft:** Prio-Rang 9 (S145-Prioritätenliste); §4 Alt-`backlog.md` Z.580.

## B-005 — Direktiv Lock Rest ab Bewegungsphase sperren

[↩ Zeile in backlog.md](backlog.md#b-005)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~15k

**Detail-Beschreibung:** Betroffene Dateien: `src/uiLayout/armyCard.py` (`_render_round_choice_ui`, `_render_once_per_battle_ability_ui`). Bug (Nutzer-Screenshots): Protokoll-Direktiven-Buttons + WAAAGH-Status erschienen im Setup und wurden über den First-Player-Toggle (`active` gesetzt) sogar wählbar; Auto-Block `if not active_id` schrieb `round_choice_active_*` schon im Setup. Setup-Teil ist gefixt; offen bleibt, die Direktive nach der Bewegungsphase zu sperren. Render-Code → manuelle Verifikation nötig.

**Abhängigkeiten:** Das Setup-Leck (Protokoll-Direktiven im Setup wählbar) ist bereits am 2026-06-20 gefixt (Helfer `_ability_section_visible`, Regressionstest `test_ability_sections_hidden_in_setup_only`); dies ist nur noch der Rest — Direktive ab Bewegungsphase sperren.

**Belege:** Root-Cause-Analyse S52 (§0 im Alt-Backlog).

**Benötigte Regeln-Scopes:** —

**Herkunft:** Prio-Rang 10 (S145-Prioritätenliste); §0 Alt-`backlog.md` Z.72–80 (#2b).

## B-006 — abilityEngine Refactor Vorplanung

[↩ Zeile in backlog.md](backlog.md#b-006)

**Typ:** <span style="color:#c2410c">**Schuldabbau**</span>

**Status:** Blocked

**Tier:** Planner

**Effort:** ~15–20k

**Detail-Beschreibung:** Betroffene Dateien: `src/gameMechanic/abilityEngine.py` (594 Zeilen, 29 Funktionen). Analog zu `stratagemEngine.py` wurde erwogen, `abilityEngine.py` nach Aktivierungsmodus (passiv/aktiv/triggered) in ein Paket zu zerlegen. Kritische Bewertung: der Modus-Schnitt trägt die reale Struktur nicht — der dominante Block (~52 %) ist Direktiv-/Protokoll-Logik, weder klar „passiv" noch „triggered"; die natürlichen Nähte sind **Direktiven/Protokolle | Unit-Buffs+Revive | Queries+Dispatch**. 594 Zeilen sind (noch) kein Kohäsionsproblem — das reale Problem ist Duplikation (s. B-081 DRY Directive-Aktiv-Logik). **Konsent-Entscheid (S145): zurückgestellt, mit Schwellwert statt „nie".** Split-Trigger: `abilityEngine.py` überschreitet ~800 Zeilen ODER die DRY-Schuld wird angegangen → dann eigener Refactor-Brief, Schnitt entlang der realen Nähte (nicht passiv/aktiv/triggered). Effort S, ~15–20k Token, re-exportierendes `__init__.py` als Kompatibilitätsschicht; nicht parallel zu Briefs mit `abilityEngine`-Importänderungen.

**Abhängigkeiten:** Orthogonal zur Klan/Dynastie-Arbeit — K2 (B-003) legt seine neue Logik bereits in ein eigenes Modul (`gameMechanic/subfactionPassives.py`), `abilityEngine.py` wächst dadurch nicht.

**Belege:** `S145_planning.md` §Option C (migriert S147).

**Benötigte Regeln-Scopes:** —

**Herkunft:** Prio-Rang ∥ (S145-Prioritätenliste, jederzeit parallel startbar); §4 Alt-`backlog.md` Z.593–613.

## B-007 — Backlog Restrukturierung

[↩ Zeile in backlog.md](backlog.md#b-007)

**Typ:** <span style="color:#1e3a8a">**Prozess/Doku**</span>

**Status:** In Progress

**Tier:** Planner → Stakeholder-Freigabe → Executor

**Effort:** ~35k

**Detail-Beschreibung:** Betroffene Dateien: `backlog.md`, `backlog_details.md`, `backlog_archive.md`, `index.md` (gelöscht). `backlog.md` bekam eine schlanke Kopf-Liste, die zugleich als Index dient; ausführliche Herleitungen/Detailtexte wurden in diese separate Datei ausgelagert. Vorgehen: Inventar (S151, dieser Schritt: Planner-Subagent-Brief → Stakeholder-Freigabe → Executor-Umsetzung). Dieser Eintrag selbst schließt sich mit Abschluss der Migration (S151).

**Abhängigkeiten:** Kein Eintrag darf verloren gehen; Abschnitt 4c (Design-System, erledigt S116–S118, ohne ✅-Glyphen) muss mit archiviert werden — ein reiner Glyphen-Scan hätte ihn übersehen.

**Belege:** `docs/handoff/S151_backlog_inventar.md` (Inventar-Schritt), `docs/handoff/S151_backlog_migration.md` (dieser Umsetzungs-Schritt).

**Benötigte Regeln-Scopes:** —

**Herkunft:** Prio-Rang 11 (Stakeholder-Auftrag S150); dieser Auftrag selbst (S151).

## B-009 — PSI Flow Reset UI Checks

[↩ Zeile in backlog.md](backlog.md#b-009)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Executor → Stakeholder (Nacharbeit + Neuvorlage)

**Effort:** ~15k

**Detail-Beschreibung:** Betroffene Dateien: `src/gameMechanic/psychicPhase.py` (Helfer `refund_deny`/`cleared_deny`, `_reset_active_power()`, `_render_undo_deny_button`). Generische Flow-/Reset-Struktur für die Psychic Phase: `_reset_active_power()` refundiert das Deny-Budget der inaktiven Fraktion (fixt: denied + reset = permanent verbranntes Budget); symmetrisches „Undo deny"-Button; „Skip Deny" verbraucht kein Budget; `deny_faction`-Feld in `psi_result`. **4 manuelle UI-Checks:** (a) „Undo deny" nach erfolgreichem Deny; (b) aktiv-Reset → nächste Power denybar; (c) Skip Deny = kein Budgetverbrauch; (d) Undo nach fehlgeschlagenem Deny — danach gemeinsamer Commit mit dem Token-Gauge-Hook. Verwandt (separater Task): `can_deny` via `rules` statt `wargear_ids`+`handler` (Gloom Prism als echter Wargear-Choice).

**S152-Befund (Nacharbeit):** Stakeholder konnte die 4 Checks nicht durchführen — es fehlten zwei konkret benannte, tatsächlich verfügbare Rosters mit Psychic-Phase-Fähigkeit (Necron-Seite braucht einen Psi-fähigen Charakter, Gegenseite muss deny-fähig sein). Vor Neuvorlage S153: zwei geeignete Rosters aus `data/rosters/` benennen (oder ergänzen, falls keins existiert) und in den Prüfschritten explizit auflisten, damit die Voraussetzung real erfüllbar ist.

**Abhängigkeiten:** Code + Tests grün seit S65 (+8 Tests, `TestRefundDeny`/`TestClearedDeny`); gemeinsamer Commit mit dem Token-Gauge-Hook geplant; Nacharbeit + Neuvorlage S153 (Roster-Benennung).

**Belege:** Commits `cc75490`/`1d8b8ba`; `docs/handoff/S152_offene_ui_verifikationen.md` (S152-Befund).

**Benötigte Regeln-Scopes:** —

**Herkunft:** §0 Alt-`backlog.md` Z.60–71 (S64-Befund, S65-Code); Nacharbeit S152.

## B-010 — Protokoll Buff Audit Anzeige Rest

[↩ Zeile in backlog.md](backlog.md#b-010)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** Blocked

**Tier:** Executor

**Effort:** ~15k

**Detail-Beschreibung:** Betroffene Dateien: `src/uiLayout/_common.py`, `src/gameMechanic/abilityEngine.py`. Engine-Wiring ist komplett (Plan 024, alle 12 Direktiv-Effekte engine-seitig verdrahtet, vorher 3/12). Offen bleibt nur noch die **Anzeige**: Eternal Guardian **S** (Hold Steady/Set to Defend) braucht einen eigenen Plan nach Plan 015 (Overwatch). S93-Engine-Befund (beide Direktiv-Quellen — 6. immer-aktives Protokoll + Dynastie-Affinitäts-Fall — waren zuvor ignoriert) ist gefixt (`_active_directive_effects` aggregiert alle 5 Reads). S97-Befund (Reroll-of-1-Save-Hinweis fehlte im SAVE-Block; `strength_modifier`/`ap_bonus` wurden von keinem UI-Konsumenten gelesen) ist über Plan 025 Steps 2/3 gelöst (Hungry-S → `strength_if_charged`, Vengeful-S → `ignore_cover_half_range`). Wurzel-Lösung S98: kein genereller Caption-Block mehr, Direktiv-Effekte gehen ins Dice-UI (S blau wie WAAAGH, `value_triggered_die_row_html`) — Anzeige ist ab S97 Pflichtteil jedes 025-Steps.

**Abhängigkeiten:** Eternal Guardian S SAVE-Hinweis hängt an einem eigenen Plan (abhängig von Plan 015 Overwatch); Sudden Storm S-Teil ist über den generischen Direktiv-Hinweisblock (Plan 025 Step 2b) bereits abgedeckt (s. Archiv A-020).

**Belege:** Plan 024 (Engine-Wiring), Plan 025 Steps 2–6 (Anzeige/Konformität), 016/017 (Anzeige-Rest-Gebiet).

**Benötigte Regeln-Scopes:** —

**Herkunft:** §0 Alt-`backlog.md` Z.81–122 (#2, Phase 3).

## B-011 — Wuerfelanzeige Pfeilrichtung und Badge Breite

[↩ Zeile in backlog.md](backlog.md#b-011)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~15k

**Detail-Beschreibung:** Pfeilrichtung/-länge der Modifier-Zeile stimmt nicht, Badge ragt in Würfel „1". Der Badge-Wert selbst bleibt (`AP-1`/`AP-2`, Stakeholder-Entscheid 2026-06-21: Gewohnheit + Konsistenz zu anderen Profilwerten; Pfeil ist bewusst redundant) — Labels nur **kürzen** (truncate/ellipsis), nicht den Wert entfernen.

**Abhängigkeiten:** Soll-Bild muss erst als Acceptance Criterion in `dice_display.md` fixiert werden → dann Plan 022, dann per AC einrasten.

**Belege:** `docs/spec/dice_display.md` (Soll-Bild als AC festlegen); Finding 9.2 (Lehre: nie still ändern).

**Benötigte Regeln-Scopes:** —

**Herkunft:** §0 Alt-`backlog.md` Z.123–128 (#3/#4, Phase 4).

## B-012 — INV 4b Cluster 1 dakka klaw tesla YAML Schema

[↩ Zeile in backlog.md](backlog.md#b-012)

**Typ:** <span style="color:#c2410c">**Schuldabbau**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~15k

**Detail-Beschreibung:** Betroffene Dateien: YAML-Schema `weapon_special`. `dakka`/`klaw`/`tesla` sollen YAML-gesteuert über ein `weapon_special`-Schema abgebildet werden, statt als Fraktions-Eigennamen in `src/` zu leben. Teil von Plan 022 oder eigenständig umsetzbar.

**Abhängigkeiten:** Cluster 3 (Plan 020), Cluster 4/5 (XS-Fix), Cluster 6 (Plan 021/024) sind bereits erledigt (Archiv A-006–A-009) — Cluster 1 ist der letzte offene INV-4b-Vokabular-Cluster.

**Belege:** `docs/spec/architecture_invariants.md` INV-4b.

**Benötigte Regeln-Scopes:** —

**Herkunft:** §0 Alt-`backlog.md` Z.129–133 (Refinement 2026-06-20).

## B-013 — GO UI Paket 3b before battle Liste ArmySetup

[↩ Zeile in backlog.md](backlog.md#b-013)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~35k

**Detail-Beschreibung:** Betroffene Dateien: ArmySetup-Screen. `before_battle`-Liste im ArmySetup macht 13 bisher nie matchende GOs erstmals sichtbar — löst den S131-Kandidaten „`before_battle` sichtbar machen" (s. B-018) ab.

**Abhängigkeiten:** Teil der 6-Pakete-GO-UI-Design-System-Roadmap (jedes Paket geht einzeln durchs Freigabe-Gate).

**Belege:** `docs/spec/design_system.md` §6, `docs/reference/go_klassifikation.md` (95 GOs, 3 Achsen). Entscheid S131.

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.160–162; S131-Kandidat, Paket 3b (S134).

## B-014 — GO UI Folge Pakete fuer 10 Rest GOs

[↩ Zeile in backlog.md](backlog.md#b-014)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Planner → Executor

**Effort:** ~35k

**Detail-Beschreibung:** Generisches `on_destroy` (7 GOs) + `on_set_up`+`on_target` für die verbleibenden 10 der ursprünglich 14 `phase_reactive`-GOs, die bis Paket 4 nirgends aktivierbar waren. Vorschlag bereits in `design_system.md` §6.2 skizziert (dort „Paket 5/6" ≠ die Backlog-Pakete 5/6 unten — Nummern-Kollision beim Einplanen vermeiden).

**Abhängigkeiten:** Nach Paket 4 (erledigt S135, Archiv A-013). Effort L — **Paket-Nummern bei Einplanung NEU vergeben** (Kollision mit den bereits vergebenen Paket-5/6-Nummern unten, s. B-015/B-016).

**Belege:** `docs/spec/design_system.md` §6.2 (Schuld-Tabelle).

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.171–173; `design_system.md` §6.2 Z.320–321.

## B-015 — GO UI Paket 5 Wortlaut und Sprach Bereinigung

[↩ Zeile in backlog.md](backlog.md#b-015)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~35k

**Detail-Beschreibung:** Englisch durchgehend, eine Vokabel-Familie Use/Undo/Confirm, eine CP-Anzeige, ein Stepper-Baustein.

**Abhängigkeiten:** Teil der 6-Pakete-Roadmap.

**Belege:** `docs/spec/design_system.md` §6 (Wortlaut-Konventionen).

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.174–175; Paket 5 (S134+).

## B-016 — GO UI Paket 6 Einheiten Auswahl und Zielauswahl

[↩ Zeile in backlog.md](backlog.md#b-016)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Design-Crew → Executor

**Effort:** ~35k

**Detail-Beschreibung:** Betroffene Dateien: GameActionArea. Einheiten-Auswahl in die GameActionArea ziehen (Heroische-Intervention-Muster verallgemeinern), Zielauswahl entschlacken.

**Abhängigkeiten:** Eigenes Konzept-Inkrement innerhalb der Roadmap.

**Belege:** —

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.176–178; Paket 6 (S134+, eigenes Konzept-Inkrement).

## B-017 — GO UI Danach manuelle UI Gesamt Verifikation

[↩ Zeile in backlog.md](backlog.md#b-017)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** Blocked

**Tier:** Stakeholder

**Effort:** ~15k

**Detail-Beschreibung:** Manuelle UI-Gesamt-Verifikation nach der S130-Checkliste plus dem neuen GO-Card-Design, sobald die Pakete abgeschlossen sind.

**Abhängigkeiten:** Erst nach Abschluss aller GO-UI-Pakete (B-013 bis B-016).

**Belege:** S130-Checkliste.

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.179.

## B-018 — Fraktions Stratagems before battle sichtbar machen

[↩ Zeile in backlog.md](backlog.md#b-018)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** Blocked

**Tier:** Executor

**Effort:** ~15k

**Detail-Beschreibung:** Betroffene Dateien: `PHASES`-Konstante (kennt kein `before_battle`). 6 Necron- + 7 Ork-Stratagems matchen nie, weil `PHASES` kein `before_battle` kennt — wird durch die neue ArmySetup-Liste aus B-013 gelöst.

**Abhängigkeiten:** Löst über B-013 (Paket 3b); danach folgt die §6e-Modifier-Engine für ~56 teilintegrierte proaktive Stratagems.

**Belege:** `docs/goals/ziel7.md` §6e (Modifier-Engine für proaktive Stratagems).

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.180–183; S131-Kandidat.

## B-019 — Alt Fire Chip unerklaert

[↩ Zeile in backlog.md](backlog.md#b-019)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Executor (Haiku-Lookup für die Regel-Verifikation)

**Effort:** ~5k

**Detail-Beschreibung:** Betroffene Dateien: `src/uiLayout/diceHtml.py:70`. `special_die_html("Alt. Fire")` rendert ohne Erklärtext (anders als „Extra Hits" mit „unmod. 6 = +2 Hits"). Vorgehen: Regel-Wortlaut gegen `docs/work/` verifizieren, dann Kurzerklärung analog Extra-Hits ergänzen. Effort XS.

**Abhängigkeiten:** Reiner Lookup + Kurzergänzung, keine Blocker.

**Belege:** `docs/work/` (Regel-Wortlaut „Alternating Fire" verifizieren).

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.184–187; S132-Befund 5, überführt S134.

## B-020 — B2 Spielvorbereitungsscreen ueberarbeiten Konzept

[↩ Zeile in backlog.md](backlog.md#b-020)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Design-Crew

**Effort:** ~35k

**Detail-Beschreibung:** Noch kein Konzept. Vorgehen: Screen-Inventar erstellen (Sonnet, read-only), Redundanz-Befunde einarbeiten, Konzept-Handoff mit Grundannahmen-Block → Stakeholder-Entscheid → eigener Plan. Faction-Ability-Wahl (B6, erledigt) läuft unabhängig vom B2-Konzept. Hinweis: der frühere Punkt „Start-Game-Button-Position" wurde S133 aus der Beobachtungsdatei entfernt/erledigt.

**Abhängigkeiten:** Struktur = Option C bereits entschieden (S135: Option A jetzt, Wizard-Zielbild erst mit B4-Datenkarte/B-021); Redundanz-Befunde B5/B7 (B-022) einarbeiten.

**Belege:** `S134_offene_punkte.md`.

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.194–209 (Stakeholder-Beobachtungen S131).

## B-021 — B4 Rest profileCard als Datenkarte Setup

[↩ Zeile in backlog.md](backlog.md#b-021)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Design-Crew → Executor

**Effort:** ~35k

**Detail-Beschreibung:** Doppel-Zoll + Profilwert-Reihenfolge bereits S133 gefixt; offen: tabellarische Waffenanzeige + „schöne Datenkarte" nur mit der echten Roster-Auswahl. **Entschieden S135:** App-Design-System mit Wahapedia-Informationsarchitektur, nur 9E-Datasheet-Spalten (keine berechneten Werte), Wargear/Relic als Chip. Vorgehen: profileCard als definierten Baustein in `design_system.md` spezifizieren (Refinement: Spalten, Waffen-Tabelle, Abgrenzung zur unitCard), danach eigener Plan.

**Abhängigkeiten:** Bereitet den künftigen Armybuilder vor; nur Setup-Screen, In-Game-Anzeige bleibt unverändert (Stakeholder-Entscheid S135).

**Belege:** Screenshots `Bildschirmfoto vom 2026-07-09 20-53-48.png` (Ist) / `…20-58-07.png` (Wahapedia-Anmutung als Inspiration, NICHT 1:1); `S134_offene_punkte.md`.

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.200–209 (Stakeholder-Beobachtungen S131).

## B-022 — B7 Redundanter Kopfbereich und schwache Hinweise

[↩ Zeile in backlog.md](backlog.md#b-022)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** Blocked

**Tier:** Planner → Executor

**Effort:** ~35k — vor Vergabe splitten

**Detail-Beschreibung:** Betroffene Dateien: `src/uiLayout/_common.py` (`render_player_column`), `psychicPhase.py`, `fightPhase.py`, `commandPhase.py`, `PHASE_RULES` (`_common.py`/`gameActionsArea.py`). Rot markierter Bereich ist redundant; wichtige Hinweise darunter („Select unit", „No PSYKER unit available") zu schwach sichtbar. **Entschieden S135:** Kopfbereich → Mini-Header (nur Phasenname, Option B, solange kein B9-Stepper existiert); Hinweis-Konvention → eigener Design-System-Baustein (Option B); B7+B9 als EIN Konzept-Handoff. **S149-Selbst-Stopp-Befund:** der rote Bereich ist die Faktions-Zeile (`**▶/◀ {faction}**`), dupliziert in `_common.py::render_player_column` UND separat in `psychicPhase.py`/`fightPhase.py`/`commandPhase.py` (DRY-Lücke, je eigene Kopie); die Mini-Header-Umstellung betrifft zusätzlich `PHASE_RULES` und der Hinweis-Baustein müsste in mindestens 6 Produktivdateien verdrahtet werden — über der ~4-Dateien-Schwelle. B8 (Archiv A-017) wurde isoliert umgesetzt; B7 bleibt für einen kleiner geschnittenen Folge-Auftrag offen. Screenshot bleibt liegen, bis der Punkt DONE ist.

**Abhängigkeiten:** Effort M — **vor Vergabe splitten** (Vorschlag B7a Faktions-Zeile+Mini-Header / B7b Hinweis-Baustein); betrifft >4 Dateien, über der Selbst-Stopp-Schwelle aus dem S149-Auftrag.

**Belege:** `S134_offene_punkte.md`.

**Benötigte Regeln-Scopes:** `docs/reference/agent_scopes.md` (Split-Zuschnitt vor Vergabe).

**Herkunft:** §2 Alt-`backlog.md` Z.213–232 (Stakeholder-Beobachtungen S131, Screenshot `…21-29-43.png`); Selbst-Stopp S149.

## B-023 — B9 Subphasen Schritte unsichtbar Stepper Baustein

[↩ Zeile in backlog.md](backlog.md#b-023)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Design-Crew → Executor

**Effort:** ~35k

**Detail-Beschreibung:** Je Phase die Unterschritte explizit anzeigen (z. B. Movement: erst alle Feldbewegungen, dann Reinforcements), während redundante Texte (B7/B8) verschwinden. **Entschieden:** Zwischenlösung C (statischer Hinweistext, kein Zustand), Zielbild vertikale Checkliste statt horizontaler Chips (Stakeholder-Kommentar).

**Abhängigkeiten:** Läuft als EIN Konzept-Handoff gemeinsam mit B7 (B-022); die B7/B8-Entfernungen schaffen erst den Platz dafür.

**Belege:** `S134_offene_punkte.md`.

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.235–242 (Stakeholder-Beobachtungen S131).

## B-024 — B10 Kommentar Hygiene Ratchet Praxis

[↩ Zeile in backlog.md](backlog.md#b-024)

**Typ:** <span style="color:#1e3a8a">**Prozess/Doku**</span>

**Status:** In Progress

**Tier:** Executor (bei jeder Modul-Berührung)

**Effort:** — (laufend, kein fixer Umfang)

**Detail-Beschreibung:** Betroffene Dateien: Alle bei Modul-Berührung. Soll: Erklärung in der Spec, Code selbsterklärend (Clean Code), höchstens ein Verweis-Kommentar auf die zuständige Spec. (a) Konvention im CLAUDE.md-Clean-Code-Abschnitt geschärft — erledigt S135. (b) läuft als Ratchet-Praxis weiter: bei jeder Modul-Berührung Kommentare in die zuständige Spec verschieben, kein Big-Bang-Durchgang.

**Abhängigkeiten:** Teil (a) bereits erledigt — Konvention in `CLAUDE.md` verankert; Teil (b) ist eine dauerhafte Ratchet-Praxis ohne Enddatum.

**Belege:** `CLAUDE.md` §Clean Code.

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.243–249 (Stakeholder-Beobachtungen S131).

## B-025 — Strukturelle Verbesserung Skeleton Platzhalter Fixe Hoehe oder Fragment Isolierung

[↩ Zeile in backlog.md](backlog.md#b-025)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~5k

**Detail-Beschreibung:** Strukturelle Verbesserung: Skeleton-Platzhalter mit fixer Höhe oder Streamlit-Fragment-Isolierung. Playwright-Probe (S154) reproduziert das Zucken beim Slot-Wechsel — 7 Layout-Shift-Events, CLS≈0.29; der B1-Scroll-Fix wirkt weiter (kein Scroll-Delta mehr). Ursache ist strukturell: Streamlit rendert den Einheiten-Datenblock inkrementell, jedes Element löst einen Reflow aus — eine feste `min-height` je Einheit wäre falsch dimensioniert. Priorität niedrig (rein kosmetisch).

**Abhängigkeiten:** B1 selbst ist gefixt (Archiv A-014); dies ist der optionale 2. Schritt aus der B1-Probe.

**Belege:** `docs/handoff/S136_B1_probe.md` (Playwright-Beleg B1); `docs/handoff/S154_offene_entscheide.md` E4 (CLS-Befund + Umformulierungs-Vorschlag).

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.250–253 (Stakeholder-Beobachtung S136); umformuliert S155 (E4, Stakeholder-Vorschlag S154).

## B-026 — B12 GO used Zustand Gesamtkonzept

[↩ Zeile in backlog.md](backlog.md#b-026)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~35k — Teil-Briefs ≤~35k je Teil

**Detail-Beschreibung:** Undo-Button nur bei der Einheit, bei der die GO angewendet wurde; an allen anderen Angebotsstellen der Phase Einsatz unterbinden, Button-Text „Used". Inline-Angebote (Attacken-/Charge-Sequenz) zeigen NIE Undo; Once-per-Phase wird erzwungen (nach Hit-Einsatz zeigen Wound/Save „used"). Größerer Eingriff: Umsetzung als Teil-Briefs ≤ M.

**Abhängigkeiten:** B12b (Header-Suffix) ist bereits erledigt (Archiv A-018); dieser Eintrag ist der Rest darüber hinaus — Once-per-Phase-Erzwingung phasenübergreifend.

**Belege:** `docs/handoff/S137_B12_konzept.md`.

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.254–259 (Stakeholder-Entscheid S137).

## B-028 — B12 Feature Wunsch used on Suffix auf alle GOs

[↩ Zeile in backlog.md](backlog.md#b-028)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~35k

**Detail-Beschreibung:** „used on ⟨Einheit⟩"-Suffix soll auf **alle** reaktiven GOs ausgeweitet werden (aktuell nur die zentrale Stratagems-Liste betroffen).

**Abhängigkeiten:** Nach dem BUG-Fix (Archiv A-019, Insane-Bravery-Repro Moralphase). Fest für S153 eingeplant (Stakeholder-Entscheid S152).

**Belege:** —

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.284–286 (Stakeholder-Wunsch S148).

## B-029 — B13 GO Karte Keyword Badges

[↩ Zeile in backlog.md](backlog.md#b-029)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~35k

**Detail-Beschreibung:** Betroffene Dateien: `src/gameObjects/stratagem.py` (Dataclass ohne `keywords`-Feld); Stratagem-YAMLs (`_shared`/`necrons`/`orks` — 0 Treffer für `keywords:`). GO-Karten zeigen keine Schlüsselwort-Chips (nur Name/CP/Regeltext). Neues Feature, keine Eil-Priorität (Stakeholder-Entscheid S137: „ins Backlog"). Stakeholder-Entscheid S141: zurückstellen, bis B13 selbst geplant wird — dann Schema+Loader+Daten in einem Aufwasch.

**Abhängigkeiten:** S141-Nachtrag: Vorziehen der Daten-Nachpflege geprüft und zurückgestellt — ist Schema-Erweiterung **plus** Datenpflege, kein reiner YAML-Task. **S152-Nachtrag:** Stakeholder bekräftigt die Beobachtung erneut (GO-Karten zeigen weiterhin keine Schlüsselwörter, obwohl der Regeltext welche vorgibt) und schlägt vor, bei Umsetzung einen Subagenten die Schlüsselwörter systematisch in der YAML-Struktur nachpflegen zu lassen (Fleißarbeit, Sonnet-Tier) — kein neuer Scope, nur Verstärkung der bestehenden Priorität.

**Belege:** `docs/spec/design_system.md` §6 (GO-Card-Baustein).

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.287–295 (Stakeholder-Beobachtung S137); Stakeholder-Beobachtung, überführt S152.

## B-030 — B14 Badge Kontrast Pass Stationary Khaki

[↩ Zeile in backlog.md](backlog.md#b-030)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** Blocked

**Tier:** Stakeholder → Executor

**Effort:** ~5k

**Detail-Beschreibung:** Betroffene Dateien: `docs/spec/design_colors.md`, `src/uiLayout/unitCard.py`. Badges schwer erkennbar, v. a. STATIONARY (`--arb-muted` `#6b5f44`) zu dunkel. Vorschlag: heller Khaki `#9c8f6a`; prüfen, ob weitere gedämpfte Badges mit angehoben werden müssen (Stakeholder S137: „ins Backlog").

**Abhängigkeiten:** Farbschema-Entscheidung liegt beim Stakeholder — Hex-Vorschläge müssen zuerst vorgelegt werden, danach mechanischer Edit.

**Belege:** —

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.296–300 (Stakeholder-Beobachtung S137).

## B-031 — GO Konsistenz Bedingungen ausgrauen statt ausblenden

[↩ Zeile in backlog.md](backlog.md#b-031)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~35k

**Detail-Beschreibung:** Betroffene Dateien: `stratagem_visibility()`, `src/uiLayout/_common.py:1134`. Durchgehend für **alle** GOs: `stratagem_visibility()` soll bei Keyword-/Bedingungs-Nichterfüllung statt `"hidden"` einen sichtbaren-aber-gesperrten Zustand (`dormant`/`locked`) zurückgeben.

**Abhängigkeiten:** Passt laut Review kollisionsfrei zum bestehenden GO-State-Modell ready/locked/used — diese Zustände rendern den Button bereits deaktiviert/ausgegraut.

**Belege:** `docs/handoff/S149_review.md` Befund 3.

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.304–310 (Stakeholder-Wunsch S149, anlässlich GAUSS/TESLA-Gates).

## B-032 — Psychic Ledger schrumpfen

[↩ Zeile in backlog.md](backlog.md#b-032)

**Typ:** <span style="color:#c2410c">**Schuldabbau**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~35k

**Detail-Beschreibung:** Betroffene Dateien: `_render_smite_flow`/`_render_psi_result`/`_render_deny_column` (Render-Code, policy-ungetestet). Smite-Manifest-Logik lebt aktuell im Render-Code. Reine Funktionen extrahieren (Schwelle `roll≥wc`, Warp-Charge-Eskalation, Perils-Schaden, Deny-once) + Tests, um die Business-Logik testbar aus dem Render-Code zu lösen.

**Abhängigkeiten:** Ledger soll von 15 auf 10 schrumpfen.

**Belege:** `docs/spec/acceptance/rules.md` (R-PSYCHIC-11/16/17/18/22).

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.311–314 (S62).

## B-033 — Psychic Luecken R PSYCHIC 23 und 24

[↩ Zeile in backlog.md](backlog.md#b-033)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~35k

**Detail-Beschreibung:** `R-PSYCHIC-23` (Perils zerstört Psyker ⇒ Power schlägt fehl; App revidiert `manifested` aktuell nicht) und `R-PSYCHIC-24` (Perils-Splash D3 an Einheiten in 6") sind implementiert-offen.

**Abhängigkeiten:** Beide brauchen einen Unit-Destroyed-Check nach Perils-Schaden.

**Belege:** `docs/spec/acceptance/rules.md` (`status: offen`).

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.315–317 (S62, aus Regel-Katalog).

## B-034 — SAVE Block Faehigkeit und AP als eine Badge

[↩ Zeile in backlog.md](backlog.md#b-034)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~15k

**Detail-Beschreibung:** Betroffene Dateien: YAML-Erweiterung nötig. Fähigkeit + AP als eine kombinierte Badge darstellen, z. B. „Enslaved AP-1", statt getrennter Elemente.

**Abhängigkeiten:** Überschneidet Plan 017 (Invuln-Badge chaotisch, B-043) und B-047.

**Belege:** → Plan 017.

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.320.

## B-035 — Gretchin Cowardly Attrition ohne RUNTHERD

[↩ Zeile in backlog.md](backlog.md#b-035)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~15k

**Detail-Beschreibung:** Betroffene Dateien: `orks/unit_abilities.yaml` (Gretchin-Cowardly-Eintrag). −1 Attrition, wenn keine RUNTHERD-Einheit innerhalb 6" ist — Teil von Plan 018.

**Abhängigkeiten:** —

**Belege:** → Plan 018.

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.321.

## B-037 — collect modifiers for phase

[↩ Zeile in backlog.md](backlog.md#b-037)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~35k

**Detail-Beschreibung:** `collect_modifiers_for_phase()` — Plan-018-Task 18.4, noch offen.

**Abhängigkeiten:** Laut §5 zusätzlich Teil von `ziel7.md` §6e (Modifier-Engine für proaktive Stratagems).

**Belege:** → Plan 018 Task 18.4; `docs/goals/ziel7.md` §6e.

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.323; §5 Z.730.

## B-038 — Totalvernichtungs Spielende R ROUND 07

[↩ Zeile in backlog.md](backlog.md#b-038)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~35k

**Detail-Beschreibung:** Der „army destroyed"-Teil von R-ROUND-07 ist bewusst NICHT implementiert — Sieg durch vollständige Vernichtung der gegnerischen Armee vor Ende Runde 5 fehlt als eigener Spielende-Pfad. Eigener kleiner Plan.

**Abhängigkeiten:** Stakeholder: eigener Punkt.

**Belege:** `docs/spec/acceptance/rules.md` R-ROUND-07.

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.324–327 (S138-Befund).

## B-040 — Fold Heuristik und Subfaction Wiring Roster zu Unit

[↩ Zeile in backlog.md](backlog.md#b-040)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** Blocked

**Tier:** Executor

**Effort:** ~15k

**Detail-Beschreibung:** Betroffene Dateien: `src/uiLayout/unitCard.py` (`_fold_faction_keyword`). `_fold_faction_keyword` filtert aktuell nur das Hauptfraktions-Keyword (Trailing-„S"-Fold); Subfraktions-Keywords werden nicht gefoldet, weil der Loader den `<DYNASTY>`/`<CLAN>`-Platzhalter mangels Roster→Unit-Wiring aktuell droppt. Sobald echte Subfraktions-Keywords in die Unit-Listen kommen (Klan-Chip statt Drop), muss die Fold-Filterung erneut geprüft werden.

**Abhängigkeiten:** Blockiert, bis echte Subfraktions-Keywords existieren (s. B-002/B-003) — beide Teile in einem Aufwasch prüfen.

**Belege:** —

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.334–340 (S138-Retro-Maßnahme 3).

## B-041 — Operating Model Phase C Refinement automatisieren

[↩ Zeile in backlog.md](backlog.md#b-041)

**Typ:** <span style="color:#1e3a8a">**Prozess/Doku**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~35k

**Detail-Beschreibung:** Betroffene Dateien: `Fotos/` → `docs/inbox/`. Refinement automatisieren — ein Sonnet-Subagent liest neue Bilder aus `Fotos/`, extrahiert die Idee als Text nach `docs/inbox/` (Format dort dokumentiert).

**Abhängigkeiten:** —

**Belege:** `docs/governance/operating_model.md`.

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.341–342.

## B-042 — Gates und Reports leser orientiert pruefen

[↩ Zeile in backlog.md](backlog.md#b-042)

**Typ:** <span style="color:#1e3a8a">**Prozess/Doku**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~15k

**Detail-Beschreibung:** Betroffene Dateien: Debt-Scoreboard, Rule-Catalog-Prozente. Gates/Reports dahingehend durchsehen, ob sie dem Stakeholder *seine* Fragen verständlich beantworten — nicht nur maschinen-orientiert zählen.

**Abhängigkeiten:** —

**Belege:** ADR-0002.

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.343–345 (→ ADR-0002).

## B-043 — Invuln SAVE Badge Bereich chaotisch

[↩ Zeile in backlog.md](backlog.md#b-043)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~15k

**Detail-Beschreibung:** Betroffene Dateien: SAVE-Block-Render. Zeigt drei Teile („Inv 4+", „active", „AP/Cover N/A"), die teils keinen Sinn ergeben. Soll: **eine** klare Badge, z. B. „Invuln 4+" — dort mitlösen oder eigener kleiner Task.

**Abhängigkeiten:** Überschneidet sich mit Plan 017 (SAVE-Block Fähigkeit+AP kombinierte Badge, B-034).

**Belege:** —

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.346 (S78).

## B-044 — Dice Display Modifier Geometrie

[↩ Zeile in backlog.md](backlog.md#b-044)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~35k

**Detail-Beschreibung:** Betroffene Dateien: `modifier_die_pair_html`. HIT/WOUND-**Debuff** spreizt nicht mit der Magnitude — `modifier_die_pair_html` zeigt immer `from-1 → from` (−1/−2/−3 sehen identisch aus), Spec §3.1 will den farbigen Würfel mit der Magnitude nach rechts wandern lassen. Zusätzlich verletzt HIT-**Buff** die Slot-1-Invariante (grauer Würfel rutscht auf Spalte 1, §3.3 will min. 2). SAVE-Geometrie ist korrekt.

**Abhängigkeiten:** Eigener Plan (eigenes Test-Netz); die Pfeil-**Zahl** (Befund A) ist bereits umgesetzt (S78).

**Belege:** `docs/spec/dice_display.md` §3.1/§3.3.

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.347 (Befund B/C, S78).

## B-045 — Silent King Zielaufteilung Fernkampf

[↩ Zeile in backlog.md](backlog.md#b-045)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~35k

**Detail-Beschreibung:** Betroffene Dateien: Ziel-Auswahl-UI Schussphase. Ein Modell mit **zwei** Fernkampfwaffen (Silent King: Sceptre of Eternal Glory / Staff of Stars) kann aktuell nur **eine** Feind-Einheit als Ziel wählen — regelwidrig. Alle Attacken **einer** Waffe gehen auf dieselbe Einheit. → UI auf **Ziel-pro-Waffe** umbauen + alle Ziele vor dem ersten Wurf deklarieren; Staff-of-Stars-Sperre ≤8 W beachten; Regressionstest. Eigener Plan.

**Abhängigkeiten:** Regel bereits geklärt (S80); reine Umsetzung.

**Belege:** `docs/inbox/finding-silent-king-target-split.md`; Core Rules-Zitat: „If a model has more than one ranged weapon, it can split the weapons between different enemy units."

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.348 (S79-UI-Befund; Regel S80 GEKLÄRT).

## B-046 — Off Scale Sieben Plus Save Grenze

[↩ Zeile in backlog.md](backlog.md#b-046)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~15k

**Detail-Beschreibung:** Sv 7+ (z. B. Gretchin) bzw. durch AP jenseits 6 verschlechterte Saves brauchen einen „7-Augen"-Würfel **plus** Erfolgsgrenze `|`. Soll lt. Stakeholder: Kopfzeile `[6] | [✕]`; Cover-Randfall `[6] 1→[7]`; AP-Fall `[6] ←4 [✕]` (konsequente Fortschreibung der D5-Spec). Alle Fälle mit Tests.

**Abhängigkeiten:** Verwandt mit Befund B/C (B-044).

**Belege:** `docs/spec/dice_display.md` (Ergänzung nötig).

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.349 (S79-UI-Befund).

## B-047 — AP und SAVE Modifier Magnitude Position

[↩ Zeile in backlog.md](backlog.md#b-047)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~15k

**Detail-Beschreibung:** Die Magnitude-Zahl (`-N`/`←N`) gehört in die **Erfolgsgrenz-Spalte** unter `|` (Screenshot AP-2: „-2" unter die Grenze; Basis-AP: erwartetes `-`/Marker in Spalte Würfel „6"). Spec prüfen, für **alle** Fälle (Buff/Debuff, HIT/WOUND/SAVE) Tests hinterlegen.

**Abhängigkeiten:** Eng verwandt mit Befund B/C-Geometrie (B-044).

**Belege:** —

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.350 (S79-UI-Befund).

## B-048 — Lethal Hits

[↩ Zeile in backlog.md](backlog.md#b-048)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~35k

**Detail-Beschreibung:** Unmodifizierter Treffer-6 = kein Wundwurf, Schaden direkt mit Overflow (wie Mortal Wounds). Nicht implementiert.

**Abhängigkeiten:** Eigener Plan nach Plan 014.

**Belege:** Regel-Katalog R-CMB-XX.

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.351 (Refinement 2026-06-20).

## B-049 — Deadly Demise

[↩ Zeile in backlog.md](backlog.md#b-049)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~35k

**Detail-Beschreibung:** Modell zerstört → Mortal Wounds auf Einheiten in X". Eigener Plan.

**Abhängigkeiten:** YAML-Daten vorhanden, Handler fehlt.

**Belege:** Regel-Katalog R-CMB-YY.

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.352 (Refinement 2026-06-20).

## B-050 — Voice of the Triarch

[↩ Zeile in backlog.md](backlog.md#b-050)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~15k

**Detail-Beschreibung:** Betroffene Dateien: `alter_command_protocol` (YAML-Basis fertig). Silent King — `voiceOfTheTriarch`-Handler fehlt.

**Abhängigkeiten:** → Plan 016 oder eigener Plan.

**Belege:** Regel-Katalog R-CMD-XX.

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.353 (Refinement 2026-06-20).

## B-051 — Failsafe Arkana Aktivator UI fehlt

[↩ Zeile in backlog.md](backlog.md#b-051)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~35k

**Detail-Beschreibung:** Betroffene Dateien: `src/uiLayout/armyCard.py:356-364` (`_render_once_per_battle_ability_ui`), `faction_abilities.yaml`. `activated`-Einträge aus `faction_abilities.yaml` mit `once_per_battle: false` werden bei `round_choice`-Fraktionen (Necrons/Custodes) **nirgends** als Aktivator gerendert — `_render_once_per_battle_ability_ui` returnt früh, wenn die Fraktion `round_choice`-Fähigkeiten hat, und surface-t nur eine `once_per_battle: true`-Fähigkeit; die commandPhase-Pfade lesen nur `unit_abilities.yaml`+`wargear.yaml`, nie `faction_abilities.yaml`. Folge: Failsafe Overcharger ist engine-dispatchbar (`buff_stat_bonus`, unit-getestet) **aber nie aktivierbar**. Fix: generischer Aktivator für `activated`-`faction_abilities` (unabhängig von `once_per_battle`/`round_choice`) + CANOPTEK-Target-Picker (9").

**Abhängigkeiten:** Kein Regressions-Bug (Picker war Plan-024-Scope-Out), aber generische Lücke für künftige aktivierbare Fraktionsfähigkeiten.

**Belege:** INV-4b-Memory-Lehre („Engine-Test-grün ≠ UI-verdrahtet").

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.354–365 (S88-Befund).

## B-052 — condition prompt applies when First Class Felder

[↩ Zeile in backlog.md](backlog.md#b-052)

**Typ:** <span style="color:#c2410c">**Schuldabbau**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~15k

**Detail-Beschreibung:** Betroffene Dateien: `gameObjects/ability.py`, `gameObjects/loader.py`. `condition_prompt`/`applies_when` reiten aktuell als Roh-Dict in der `effects`-Subliste mit, weil `Ability`/`Effect` keine eigenen Felder dafür haben. Sauberere Modellierung, sobald ein zweiter Konsument auftaucht.

**Abhängigkeiten:** Erst wenn ein zweiter Konsument auftaucht.

**Belege:** Kommentar in `orks/unit_abilities.yaml` (Gretchin-Cowardly-Eintrag).

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.366–370 (S128-Folge, Plan 018 Task 18.3).

## B-054 — Custodes Rendax Kath Secondary toter Pfad

[↩ Zeile in backlog.md](backlog.md#b-054)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~15k

**Detail-Beschreibung:** Betroffene Dateien: `data/wh40k_9e/adeptus_custodes/faction_abilities.yaml` (Protokoll `rendax_kath`, `secondary`-Effekt). Der `secondary`-Effekt `type: strength_modifier` (Zielwert „+1 S nach Charge") wurde bei Plan 025 Step 6 aus der Engine entfernt (war toter Pfad, nie konsumiert). Braucht eigene `strength_if_charged`-Verdrahtung analog Hungry Void D2 (auch Charge-bedingt). YAML → `type: strength_if_charged, value: 1, phase: melee`.

**Abhängigkeiten:** Engine-Fn (`strength_if_charged`) existiert bereits; nur Konsum + Test nötig.

**Belege:** S97/S98-Befund (analog Hungry Void D2).

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.376–382 (Plan 025 Step 6).

## B-055 — Army List UX weniger Scrollen

[↩ Zeile in backlog.md](backlog.md#b-055)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~35k — Machbarkeit zuerst klären

**Detail-Beschreibung:** Drei Bausteine: (a) abgehandelte Unit-Card automatisch ans **Ende** der Armeeliste schieben; (b) nach **Phasenwechsel** den Fokus auf die nächste relevante Unit-Card setzen; (c) optionales manuelles **Umsortieren/Switch** von Cards. Eigener Plan, zuerst Streamlit-Machbarkeit klären.

**Abhängigkeiten:** Offene technische Frage: Reorder/Auto-Scroll in Streamlit überhaupt sauber umsetzbar? → zuerst klären.

**Belege:** IMG_4051.

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.384–389 (Refinement-Skizze IMG_4051, S94 gesichert).

## B-056 — Quantum Shielding fester Invuln Wert

[↩ Zeile in backlog.md](backlog.md#b-056)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~35k

**Detail-Beschreibung:** Setzt den Rettungswurf (Invuln) auf einen **festen Wert (4+)** — keine additive Modifikation, kein Modifier-Pfeil in der Würfelanzeige. Eigener Mechanik-Typ „Invuln auf festen Wert setzen" (vs. der bestehenden additiven Modifier-Logik) nötig. **S148-UI-Befund (Annihilation Barge):** unmod. Wound 1–3 misslingt bei Quantum-Shielding-Einheiten immer — wird aktuell **nicht** als Debuff in der Wound-Zeile (3× ✕) noch als Buff im Save-Block angezeigt. Regeltext vorher gegen `docs/work/wahapedia_necrons` verifizieren. S152-Planner-Befund: zwei gleichnamige Mechaniken liegen vor - das Stratagem "Quantum Shielding" gibt einen temporären festen 4+ Invuln, die Fahrzeug-Fähigkeit "Quantum Shielding" gibt einen dauerhaften 5+ Invuln + unmod. Wound 1-3 auto-fail. Stakeholder-Entscheid S152 = Scope (b): den Anzeige-Bug der Fähigkeit fixen UND einen neuen Mechanik-Typ "Invuln auf festen Wert" für das Stratagem einführen; geplant für S153.

**Abhängigkeiten:** Überschneidet sich mit dem SAVE-/Invuln-Badge-Bereich (Plan 017 / B-043).

**Belege:** `docs/handoff/S148_ui_verifikation.md` Prüfblock 1; `docs/work/wahapedia_necrons/`.

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.390–398 (Refinement-Skizze IMG_4041, S94 gesichert; S148-UI-Befund).

## B-057 — Waffen Block Rapid Fire Count und Range anzeigen

[↩ Zeile in backlog.md](backlog.md#b-057)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~15k

**Detail-Beschreibung:** Betroffene Dateien: Waffen-Auswahl-Block Schussphase. Je Waffe die **Anzahl Attacken inkl. Rapid Fire** sowie die **Reichweite** anzeigen; eligible vs. nicht-eligible Waffen visuell absetzen (durchgestrichen/ausgegraut statt nur ausgeblendet). Eigener Plan.

**Abhängigkeiten:** Verwandt mit der Eligibility-Anzeige der Schussphase und dem Silent-King-Ziel-pro-Waffe-Finding (B-045).

**Belege:** IMG_4038.

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.399–403 (Refinement-Skizze IMG_4038, S94 gesichert).

## B-058 — Dynastie Code je Einheit statt Roster Ebene

[↩ Zeile in backlog.md](backlog.md#b-058)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Planner → Executor

**Effort:** ~35k — Konzept zuerst

**Detail-Beschreibung:** Betroffene Dateien: `subfaction_value_for`-Konsumenten (`abilityEngine`, `gameState`, `armyCard`). `subfaction_value_for` liest die Subfaction heute auf **Roster-Ebene**; regelseitig trägt jede Einheit den Dynastie-Code. Prüfen, ob Einheiten-Ebene nötig ist (Mixed-Dynasty-Roster) und die Konsumenten entsprechend umstellen.

**Abhängigkeiten:** Eigenes Konzept vor Umsetzung nötig; verwandt B-002/B-003.

**Belege:** `S139_dynastie_protokoll_konzept.md`.

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.404–408 (Konzept-Frage 2 aus `S139_dynastie_protokoll_konzept.md`, Stakeholder-Entscheid S140).

## B-059 — Regel Index fuer Wahapedia Texte

[↩ Zeile in backlog.md](backlog.md#b-059)

**Typ:** <span style="color:#1e3a8a">**Prozess/Doku**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~15k

**Detail-Beschreibung:** Betroffene Dateien: `docs/work/rule_index.md` (neu). Additiver Stichwort→`datei:zeilenbereich`-Index (Format: `Lethal Hits → core_rules.txt:1420-1435`) — ~23k Zeilen Regeltext sind nur per `grep` durchsuchbar; kein Wortlaut wird dabei berührt.

**Abhängigkeiten:** Beschleunigt künftige Haiku-Lookups.

**Belege:** —

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.409–412 (context-audit-S91, verarbeitet S118).

## B-062 — Audit Plaene bereinigen

[↩ Zeile in backlog.md](backlog.md#b-062)

**Typ:** <span style="color:#1e3a8a">**Prozess/Doku**</span>

**Status:** ToDo

**Tier:** Executor — **Tier: Sonnet** (Abgleich mit Bewertung, kein reiner Lookup)

**Effort:** ~35k

**Detail-Beschreibung:** Betroffene Dateien: `docs/audit/plans/` + README-Queue. Subagent-Durchgang über `docs/audit/plans/` + README-Queue — erledigte/überholte Pläne archivieren bzw. Status korrigieren.

**Abhängigkeiten:** Jeden Plan gegen Code + `git log` verifizieren, nicht nur Statuszeilen lesen.

**Belege:** Anlass Plan-015-Step-1-Befund S122.

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.426–430 (Stakeholder-Auftrag S122, für S123+).

## B-063 — Boarding Actions Stratagems laden

[↩ Zeile in backlog.md](backlog.md#b-063)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** Blocked

**Tier:** Executor

**Effort:** ~15k

**Detail-Beschreibung:** Betroffene Dateien: `necrons/stratagems.yaml`. NANOSCARAB VIRUS + MINDSHACKLE SCARABS in `necrons/stratagems.yaml` aufnehmen, sobald die Hatchway-Abhängigkeit geklärt ist (Entscheid: JA, laden — nicht dauerhaft ausschließen). Nebenbefund (Merkposten für Paket 4/Stufe C): `phase: any` + `event: after_roll` fehlmatcht jeden Advance-/after_roll-Anker — Events künftig wurfspezifisch wählen.

**Abhängigkeiten:** Blockiert bis ziel7 Stufe C (hängt an B-003); Bereinigung anderer BA-only-Einträge bereits erledigt S134 (Archiv A-021).

**Belege:** `docs/handoff/S147_go_audit_stratagems.md` (Lücken-Tabelle).

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.431–440 (Stakeholder-Entscheid S122, → ziel7 Stufe C).

## B-064 — Variable CP Kosten in der UI anzeigen

[↩ Zeile in backlog.md](backlog.md#b-064)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Design-Crew → Executor

**Effort:** ~15k

**Detail-Beschreibung:** Betroffene Dateien: Stratagem-Karte (UI-Design nötig). 5 Necron-Stratagems haben variable Kosten (z. B. „3/1 CP"); YAML trägt bewusst das Minimum, `rule_text` erklärt. UI soll die Variabilität zeigen (z. B. „1 CP (3 CP für TITANIC)") — es wird mit titanischen Einheiten gespielt.

**Abhängigkeiten:** —

**Belege:** —

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.441–444 (Stakeholder-Entscheid S122).

## B-065 — improve Session vorbereiten

[↩ Zeile in backlog.md](backlog.md#b-065)

**Typ:** <span style="color:#1e3a8a">**Prozess/Doku**</span>

**Status:** ToDo

**Tier:** Stakeholder → Executor

**Effort:** ~15k (Vorbereitung)

**Detail-Beschreibung:** Eigene Session für den `/improve`-Skill (read-only Codebase-Audit → priorisierte, in sich geschlossene Umsetzungspläne für Executor-Subagenten). Vorbereitung: bereinigte Plan-Queue, grüne Vollsuite, Scope-Entscheid des Stakeholders (Bugs/Tech-Debt/UX/Roadmap) einholen; Ergebnis-Pläne in die `docs/audit/plans/`-Queue einsortieren. Token-intensiv → eigene Session.

**Abhängigkeiten:** Bereinigte Plan-Queue (B-062) zuerst, grüne Vollsuite als Baseline.

**Belege:** `/improve`-Skill.

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.445–450 (Stakeholder-Auftrag S122, für S123+).

## B-066 — Transport Insassen Feature Embark Disembark

[↩ Zeile in backlog.md](backlog.md#b-066)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Planner → Executor

**Effort:** ~15–35k

**Detail-Beschreibung:** Betroffene Dateien: Roster-Schema, Loader, Game-State (`embarked_units` analog `melee_with`), Movement-Phase-UI. Insassen-Zuordnung („Einheit X sitzt in Transport Y") fehlt vollständig. 4 Bausteine: (1) Roster-Schema-Feld `embarked_in` pro Unit-Eintrag; (2) Loader liest das Feld + validiert gegen Transportkapazität (heute nur Freitext in der `ABIL`-Zeile); (3) Game-State-Feld `embarked_units` + Embark/Disembark-Mutationen (Movement 3", Destroyed-Fall 3"/6" je Stratagem); (4) UI: Embark/Disembark-Buttons in der Movement-Phase + „eingestiegen in ⟨Transport⟩" auf der Unit-Karte. 2 offene Design-Fragen: (a) nur Start-Zustand im Roster-YAML deklarierbar vs. In-Game-Embark/Disembark über die UI; (b) Kapazität hart durchsetzen vs. nur Text-Hinweis (Klasse B/C). Aufwand S–M.

**Abhängigkeiten:** Voraussetzung, damit die Emergency-Disembarkation-GO-Karte zeigen kann, WELCHE Einheiten aussteigen.

**Belege:** `docs/handoff/S141_ui_befunde_group_b.md` §3–§5 (S141/S142).

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.451–462; Stakeholder-Entscheid S142 (NIEDRIG-Prio).

## B-067 — Roster Builder Anforderung before battle Stratagems

[↩ Zeile in backlog.md](backlog.md#b-067)

**Typ:** <span style="color:#1e3a8a">**Prozess/Doku**</span>

**Status:** ToDo

**Tier:** Planner

**Effort:** — (kein Umsetzungsaufwand, Anforderung für später)

**Detail-Beschreibung:** `before_battle`-Stratagems (z. B. „Hand of the Phaeron") sind im laufenden Spiel nicht nutzbar — beim Bau des künftigen Roster-Builders berücksichtigen: dort müssen `before_battle`-Stratagems auswählbar/abhandelbar sein.

**Abhängigkeiten:** Anforderung für einen künftigen Roster-Builder, kein akuter Task.

**Belege:** —

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.463–466 (Stakeholder-Verifikation S146).

## B-068 — UX Nit Silent King Zusatzattacken Default

[↩ Zeile in backlog.md](backlog.md#b-068)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~5–15k

**Detail-Beschreibung:** Eingabe der zusätzlichen Attacken (Staff of Stars 4 / Scythe of Dust 3) soll wie bei anderen Einheiten üblich per Default auf dem Maximum vorbelegt sein; aktuell startet der Wert niedriger, was beim Spielen nervt.

**Abhängigkeiten:** —

**Belege:** —

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.467–470 (Stakeholder-Verifikation S146).

## B-069 — camelCase Umbenennung

[↩ Zeile in backlog.md](backlog.md#b-069)

**Typ:** <span style="color:#c2410c">**Schuldabbau**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** 4 Teil-Briefs ≤~35k je Teil

**Detail-Beschreibung:** Betroffene Dateien: YAML + Loader-Code, Necron-Scope (6 Dateien), Ork-Scope (5 Dateien), `adeptus_custodes/faction_abilities.yaml:96`. Migrationsplan + vollständige Mapping-Tabelle liegen fertig unter `loader_contract.md` §8. Die eigentliche Umbenennung in YAML + Loader-Code ist noch offen, in Teil-Briefs ≤ Effort M zu schneiden.

**Abhängigkeiten:** 4 Teil-Briefs ≤ Effort M: (1) Stratagems `modifier`/`target`-Kollision zuerst (höchstes Risiko bei naivem Rename), (2) restliche Stratagem-Felder, (3) Necron-Ability-Scope, (4) Ork-Ability-Scope inkl. `target_keyword`-Bereinigung + Custodes-Zusatzfund.

**Belege:** `docs/spec/loader_contract.md` §8 (Mapping-Tabelle: 107 Felder + 3 aufgelöste Kollisionen `modifier`/`target`/`target_keyword`).

**Benötigte Regeln-Scopes:** Executor-Briefs max. Effort M (S130-Auflage).

**Herkunft:** §2 Alt-`backlog.md` Z.482–491 (S148 Brief 7 hat nur die Grundlage gelegt).

## B-070 — Reanimation Konsistenz Umsetzung

[↩ Zeile in backlog.md](backlog.md#b-070)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~35–70k (Modell-Auswahl-UI nötig)

**Detail-Beschreibung:** Betroffene Dateien: `necrons/stratagems.yaml:291-303,438-451`, `abilityEngine.py:413`, `armyCard.py:109`. Stakeholder-Entscheid: Stratagem-`reanimate` (Reanimation Prioritisation, Resurrection Protocols) wird künftig **genauso** mitgezählt wie die Ability-Variante (Reanimation Protocols) — keine Sonderbehandlung der Stratagem-Variante. Umsetzung als eigenes Ticket.

**Abhängigkeiten:** Entscheid bereits gefallen (S148: keine Sonderbehandlung mehr); Effort M/L wegen nötiger Modell-Auswahl-UI.

**Belege:** `docs/handoff/S147_go_audit_stratagems.md` (Lücken-Tabelle „Reanimation Prioritisation / Resurrection Protocols" + Fixing-Plan-Punkt 7).

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.492–499; Entscheid S148.

## B-071 — auto wound prueft keine Gauss Tesla Bedingung

[↩ Zeile in backlog.md](backlog.md#b-071)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~15k

**Detail-Beschreibung:** Betroffene Dateien: `auto_wound`-Effekt-Handler. Der `auto_wound`-Effekt selbst (Techno-Oracular Targeting, Disintegration Capacitors) prüft nicht, ob der konkrete Angriff tatsächlich mit einer Gauss-/Tesla-Waffe geführt wurde.

**Abhängigkeiten:** Die WER-darf-nutzen-Bedingungslücke (`conditions: [GAUSS]`/`[TESLA]`) ist bereits gefixt (Brief 6, S149); dies ist die tiefere, verbleibende Lücke.

**Belege:** `docs/handoff/S147_go_audit_stratagems.md` Zeile 41 (Lücken-Tabelle) + Fixing-Plan Punkt 5; `docs/handoff/S147_go_audit_necron_abilities.md` §2; Plan 032 Punkt 5.

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.500–507 (S147-Audit-Restlücke, bewusst nicht in Brief 6/S149 mitgefixt).

## B-072 — Roster Daten Konsistenz Recherche

[↩ Zeile in backlog.md](backlog.md#b-072)

**Typ:** <span style="color:#c2410c">**Schuldabbau**</span>

**Status:** ToDo

**Tier:** Executor (Haiku)

**Effort:** ~5k

**Detail-Beschreibung:** Betroffene Dateien: `necrons/units.yaml` (CORE-Keyword Annihilation Barge/Flayed Ones), Ork Boss Nob Waffen. Stakeholder hat das Test-Roster als fehlerhaft befunden — Annihilation Barge war als MWBD-Ziel wählbar, ist laut Stakeholder aber **nicht** CORE. Aufgabe: CORE-Keyword-Abgleich `necrons/units.yaml` vs. `docs/work/wahapedia_necrons` (Annihilation Barge + Flayed Ones mitprüfen) **und** Ork Boss Nob Waffen (Stakeholder-Zweifel: „wirklich nur Stikkbomb?").

**Abhängigkeiten:** Reiner Datenabgleich.

**Belege:** `docs/work/wahapedia_necrons`.

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.508–512 (S148-UI-Befund, Prüfblock 2).

## B-073 — model groups Union Ungenauigkeit

[↩ Zeile in backlog.md](backlog.md#b-073)

**Typ:** <span style="color:#c2410c">**Schuldabbau**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~15k

**Detail-Beschreibung:** Betroffene Dateien: `derived_keywords`-Ableitungsmechanismus. Der generische `derived_keywords`-Mechanismus bildet die Vereinigung über alle `model_groups` einer Einheit statt pro Gruppe zu differenzieren — bei gemischter Bewaffnung (z. B. nicht jedes Modell trägt die Gauss-Waffe) zeigt die Einheit das Keyword ggf. zu breit.

**Abhängigkeiten:** Keine Regression; bei nächster `model_groups`-Arbeit mitprüfen.

**Belege:** —

**Benötigte Regeln-Scopes:** —

**Herkunft:** §2 Alt-`backlog.md` Z.513–518 (S148-Folge, geerbt von `grantsKeyword`/Brief 4).

## B-075 — mypy Rest gameMechanic

[↩ Zeile in backlog.md](backlog.md#b-075)

**Typ:** <span style="color:#c2410c">**Schuldabbau**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~15k

**Detail-Beschreibung:** Betroffene Dateien: `attackMath.py` (`type-arg`), `moralePhase.py`/`unitMutations.py` (`no-any-return`/`arg-type`). 7 verbleibende Fehler in `gameMechanic/` außerhalb des `state`-Contracts. Baseline in `tools/mypy_gate.py` im selben Commit senken (Ratchet-Regel).

**Abhängigkeiten:** Eigenständig von B-004 (uiLayout-Teil) — kein `state: dict`-Fall mehr, andere Fehlerklassen.

**Belege:** `tools/mypy_gate.py` (Baseline 24, Stand S144).

**Benötigte Regeln-Scopes:** —

**Herkunft:** §4 Alt-`backlog.md` Z.568–586.

## B-076 — Layer Kopplung gameMechanic importiert uiLayout

[↩ Zeile in backlog.md](backlog.md#b-076)

**Typ:** <span style="color:#c2410c">**Schuldabbau**</span>

**Status:** ToDo

**Tier:** Planner

**Effort:** ~70k+

**Detail-Beschreibung:** Betroffene Dateien: `gameMechanic/*Phase.py` (importiert `uiLayout._common`). Aufräum-Pfad: Phasen-Render nach `uiLayout/` ziehen.

**Abhängigkeiten:** Bewusst (noch) nicht als Architektur-Wächter erzwungen; verwandt B-077/B-088 (gleicher Render-Hub).

**Belege:** `docs/audit/plans/008-*` (Audit-Plan 008).

**Benötigte Regeln-Scopes:** —

**Herkunft:** §4 Alt-`backlog.md` Z.587–589.

## B-077 — common py refactoren

[↩ Zeile in backlog.md](backlog.md#b-077)

**Typ:** <span style="color:#c2410c">**Schuldabbau**</span>

**Status:** ToDo

**Tier:** Planner → Executor

**Effort:** ~70k+ — vor Vergabe splitten

**Detail-Beschreibung:** Betroffene Dateien: `src/uiLayout/_common.py` (2218 Zeilen). `_common.py` in logische Teile zerlegen; die Attackensequenz sollte eine eigene Datei werden.

**Abhängigkeiten:** Effort L — **vor Vergabe splitten**; gleicher Render-Hub wie B-076.

**Belege:** —

**Benötigte Regeln-Scopes:** `docs/reference/agent_scopes.md` (Split-Zuschnitt vor Vergabe).

**Herkunft:** §4 Alt-`backlog.md` Z.590–592 (Stakeholder-Auftrag S132).

## B-078 — Test Mock Fragilitaet und conftest Mock Hack

[↩ Zeile in backlog.md](backlog.md#b-078)

**Typ:** <span style="color:#c2410c">**Schuldabbau**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~35k

**Detail-Beschreibung:** Betroffene Dateien: `tests/gameMechanic/conftest.py` (`sys.modules`-Re-Pointing). Mehrere `src`-Module lesen das globale `st.session_state` und rufen einander auf (`unitMutations.set_movement_status` → `gameState.units_key_for`; `abilityEngine` → `gameState`/`unitMutations`). Tests mocken `streamlit` **pro Datei**; wer ein Modul zuerst importiert, bindet dessen `st` — reihenfolge-abhängig und zerbrechlich (S51: ein neuer Test als erster Importer brach 15 Movement-Tests). Workaround: Akzeptanztest importiert `gameState` lazy. Saubere Lösung: **eine geteilte `streamlit`-Fixture** (conftest) + Tests auf `module.st` statt lokalem `_st_mock` umstellen — ersetzt zugleich den reihenfolge-abhängigen `conftest.py`-Quick-Fix durch eine **session-scoped Streamlit-Mock-Fixture**, die alle `gameMechanic`-Tests einheitlich nutzen.

**Abhängigkeiten:** Gemeinsame Lösung für beide Retro-Maßnahmen.

**Belege:** S110-Retro.

**Benötigte Regeln-Scopes:** —

**Herkunft:** §4 Alt-`backlog.md` Z.614–621, Z.639–642 (S51 entdeckt; S110-Retro M1+M2).

## B-080 — DRY Zwei Sechs Cap Quelle

[↩ Zeile in backlog.md](backlog.md#b-080)

**Typ:** <span style="color:#c2410c">**Schuldabbau**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~15k

**Detail-Beschreibung:** Betroffene Dateien: `src/gameMechanic/combat.py:207,213` (`resolve_attack_modifiers`), `src/uiLayout/diceHtml.py:31` (`_capped_modifier_threshold`). Der 9E-Cap (Hit/Wound: unmod. 6 immer Erfolg, unmod. 1 immer Fehlschlag) existiert doppelt. Aktuell konsistent gefixt. Langfristig `_capped_modifier_threshold` als dünnen Wrapper um die combat-Cap-Logik führen oder die Zwischen-Modifier-Zeilen ebenfalls aus `atk_result` speisen (eine Cap-Quelle).

**Abhängigkeiten:** Kein akuter Bug, niedrige Priorität — Sync-Risiko bei künftigen Änderungen.

**Belege:** —

**Benötigte Regeln-Scopes:** —

**Herkunft:** §4 Alt-`backlog.md` Z.625–631 (S144-Review Befund 2).

## B-081 — DRY Directive Aktiv Logik

[↩ Zeile in backlog.md](backlog.md#b-081)

**Typ:** <span style="color:#c2410c">**Schuldabbau**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~15k

**Detail-Beschreibung:** Betroffene Dateien: `src/gameMechanic/gameState.py:242-283` (`active_round_choice_buff_labels`), `abilityEngine._active_directive_effects`. `gameState.active_round_choice_buff_labels` (UI-Labels) dupliziert einen Teil der „welches Directive ist aktiv"-Logik aus `abilityEngine._active_directive_effects` (Rechen-Seite) — Sync-Risiko analog Cap-DRY (B-080): Regeländerung an einer Stelle ⇒ Anzeige ≠ Rechnung.

**Abhängigkeiten:** Wiederverwendung scheitert am Import-Zyklus (`abilityEngine` importiert bereits aus `gameState`); braucht ein drittes, tieferliegendes Modul. Kein akuter Bug, niedrige Priorität.

**Belege:** —

**Benötigte Regeln-Scopes:** —

**Herkunft:** §4 Alt-`backlog.md` Z.632–638 (S143-Refactor-Befund Punkt 4, Entscheid S144).

## B-083 — architecture md Doku Session

[↩ Zeile in backlog.md](backlog.md#b-083)

**Typ:** <span style="color:#1e3a8a">**Prozess/Doku**</span>

**Status:** Blocked

**Tier:** Stakeholder → Executor

**Effort:** ~15k

**Detail-Beschreibung:** Betroffene Dateien: `docs/spec/architecture.md`. `architecture.md` ist teils veraltet (Gesamtbild stimmt, Details nicht): (1) **session_state-Schema** nennt `unit_state` ohne `group_models`/`group_wounds` (real in `gameState.py`), Armee ohne `dynasty`/`protocol_order` (real vorhanden), Datei-Name-Drift „`state.py`" → real `gameState.py`. (2) **Colour System** beschreibt `COLOR_*`-Aliase „als CSS in app.py" — das Live-Theme sind aber `--arb-*`-Variablen in `gameHeader.py`; kanonisch ist `design_colors.md`, die `COLOR_*` (Tailwind-Extrakte in `constants/colors.py`) existieren noch, treiben das Theme aber nicht. (3) **uiLayout „No game logic in this layer"** ist widerlegt durch `_common.py` (Attack-Mathe wurde deshalb nach `attackMath.py` ausgelagert, s. Layer-Kopplung B-076). (4) **Refactoring Plan / Open Design Questions** ist historisch, alle Phasen erledigt, viele Fragen beantwortet → als Historie kennzeichnen. Dazu zwei Doku-Altlasten mitzuziehen: `faction_abilities.md` Z.42/197 referenziert noch das entfernte `auto_round_1`-Flag (6e Bug 1, Regeln erlauben freie Verteilung der Protokolle auf Runden 1–5).

**Abhängigkeiten:** Freigabepflichtig — vor Änderung freigeben.

**Belege:** `docs/spec/design_colors.md` (kanonisch für Colour System).

**Benötigte Regeln-Scopes:** —

**Herkunft:** §4b Alt-`backlog.md` Z.651–674 (Abgleich 2026-06-15).

## B-084 — Mortal Wounds Text Match Erkennung

[↩ Zeile in backlog.md](backlog.md#b-084)

**Typ:** <span style="color:#c2410c">**Schuldabbau**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~15k

**Detail-Beschreibung:** Betroffene Dateien: `_detect_weapon_special` (`"mortal wound" in abilities.lower()`). Nutzt Text-Match statt eines strukturierten YAML-Feldes. Technische Schuld.

**Abhängigkeiten:** Kein akuter Block.

**Belege:** —

**Benötigte Regeln-Scopes:** —

**Herkunft:** §4b Alt-`backlog.md` Z.676.

## B-085 — faction abilities md Kategorie 6 veraltet

[↩ Zeile in backlog.md](backlog.md#b-085)

**Typ:** <span style="color:#1e3a8a">**Prozess/Doku**</span>

**Status:** Blocked

**Tier:** Executor

**Effort:** ~5k

**Detail-Beschreibung:** Betroffene Dateien: `docs/spec/faction_abilities.md` Kategorie 6. Behauptet „Größtenteils abgedeckt durch `triggered`-Abilities in `faction_abilities.yaml`" — das ist falsch: Klan-Kulturs/Dynastic Codes liegen in `subfaction_abilities.yaml` (anderer Datei-Scope) und sind laut `ziel7.md` Stufe C §K1 Kern-Befund aktuell nicht wirksam. Spec-Nachzug empfohlen, sobald K2+ umgesetzt ist.

**Abhängigkeiten:** Blockiert, bis K2+ (B-003) umgesetzt ist.

**Belege:** `docs/goals/ziel7.md` Stufe C §K1.

**Benötigte Regeln-Scopes:** —

**Herkunft:** §4b Alt-`backlog.md` Z.677–682 (S144-Fund, migriert S150).

## B-086 — Test Schuld klein Tautologie Tests

[↩ Zeile in backlog.md](backlog.md#b-086)

**Typ:** <span style="color:#c2410c">**Schuldabbau**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~15k

**Detail-Beschreibung:** Betroffene Dateien: `tests/gameMechanic/test_damage_block_reanimation.py` (Z.394–401, Z.403–417); 11 Testdateien mit Modul-Level-`sys.modules["streamlit"]`-Mocks. Zwei Tautologie-Tests: Z.394–401 rechnet `4*2==8` selbst nach (kein echter System-Under-Test-Nachweis); Z.403–417 prüft nur Fixtures statt RP-Gate-Logik. Zusätzlich: `tests/gameMechanic/conftest.py` hat inzwischen die session-scoped Fixture `_canonical_streamlit_mock`, die per-File-Mocks vor dem ersten src-Import sind aber noch in 11 Testdateien dezentral — konsolidieren.

**Abhängigkeiten:** Kein Blocker; bei Gelegenheit/bei nächster Test-Infra-Arbeit mitnehmen. Verwandt B-078.

**Belege:** —

**Benötigte Regeln-Scopes:** —

**Herkunft:** §4d Alt-`backlog.md` Z.712–723 (DoD-Review S114, Follow-up S118-M2).

## B-088 — Richtungsentscheid Ziel9 Fetcher vorziehen

[↩ Zeile in backlog.md](backlog.md#b-088)

**Typ:** <span style="color:#1e3a8a">**Prozess/Doku**</span>

**Status:** Blocked

**Tier:** Stakeholder

**Effort:** — (Entscheidung, kein Umsetzungsaufwand)

**Detail-Beschreibung:** Ziel9-Fetcher vorziehen? Eigene Deployment-Phase bauen oder ADR „bleibt am Tisch"? Mission-Scoring (eine Mission end-to-end)? Noch nicht entschieden, Stakeholder-Input nötig. Blockiert indirekt B-090 (Ziel 9).

**Abhängigkeiten:** Stakeholder-Entscheidung nötig, bisher nicht gefallen.

**Belege:** —

**Benötigte Regeln-Scopes:** —

**Herkunft:** §5 Alt-`backlog.md` Z.777–779 (Audit S124, aus `next_session.md` verschoben S129).

## B-089 — Ziel 8 Crusade Erweiterung

[↩ Zeile in backlog.md](backlog.md#b-089)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> — *tatsächlich Ziel 8, kein Ziel-7-Scope; Typ-Enum kennt keine eigene „geplantes Ziel"-Kategorie, daher hier eingeordnet.*

**Status:** ToDo

**Tier:** Planner

**Effort:** ~70k+ — bei Aufnahme splitten

**Detail-Beschreibung:** Crusade-Erweiterung (geplant). Details in `ziel8.md`.

**Abhängigkeiten:** Noch nicht begonnen; Effort L — bei Aufnahme splitten.

**Belege:** `docs/goals/ziel8.md`.

**Benötigte Regeln-Scopes:** —

**Herkunft:** §5 Alt-`backlog.md` Z.775; `index.md` Z.45.

## B-090 — Ziel 9 Wahapedia Faction Fetcher

[↩ Zeile in backlog.md](backlog.md#b-090)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> — *tatsächlich Ziel 9, kein Ziel-7-Scope; s. Anmerkung bei B-089.*

**Status:** ToDo

**Tier:** Planner

**Effort:** ~70k+ — bei Aufnahme splitten

**Detail-Beschreibung:** Wahapedia Faction Fetcher (geplant). Details in `ziel9.md`.

**Abhängigkeiten:** Noch nicht begonnen; Effort L — bei Aufnahme splitten; Richtungsentscheid B-088 offen.

**Belege:** `docs/goals/ziel9.md`.

**Benötigte Regeln-Scopes:** —

**Herkunft:** §5 Alt-`backlog.md` Z.776; `index.md` Z.45.

## B-091 — Design Block UI Theme

[↩ Zeile in backlog.md](backlog.md#b-091)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> — *eigenständiger Design-Block, kein Ziel-7-Scope; s. Anmerkung bei B-089.*

**Status:** ToDo

**Tier:** Design-Crew

**Effort:** ~35k

**Detail-Beschreibung:** Betroffene Dateien: Farbpalette/Goldtöne, Badges, Einheitenkarten-Layout. Eigene Session, noch nicht begonnen: (1) Farbpalette überarbeiten — Goldtöne, Primärfarbe, Kontraste; (2) Badge-Optik und Spacing prüfen; (3) Einheitenkarten-Layout verfeinern.

**Abhängigkeiten:** 3 Teilpunkte, bündeln oder einzeln vergeben.

**Belege:** —

**Benötigte Regeln-Scopes:** —

**Herkunft:** `index.md` Z.46, Z.52–56.

## B-098 — Boss Nob 7b Kombi Waffenprofile

[↩ Zeile in backlog.md](backlog.md#b-098)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~35k

**Detail-Beschreibung:** Betroffene Dateien: `data/wh40k_9e/orks/weapons.yaml`, `data/wh40k_9e/orks/units.yaml`. Teil 1 (Kombi-Waffenprofile in `weapons.yaml` + Tests) ist erledigt (S152). Teil 2 ist offen — S152-Planner-Befund: (a) `units.yaml` Boss-Nob braucht einen neuen `weapon_swap` (pick 1: `kombi_rokkit`/`kombi_skorcha`, replaces `slugga`+`choppa`; NICHT für Warbike-Nobs); (b) die Kombi-Mechanik "eines oder beide Profile, bei beiden -1 to hit" ist mit dem aktuellen `WeaponProfile`-Schema nicht generisch abbildbar -> Engine-Erweiterung nötig.

**Abhängigkeiten:** Teil 1 war reiner Daten-Fix (erledigt); Teil 2 ist kein reiner Daten-Fix mehr, sondern braucht eine Engine-Erweiterung für die ODER-Gruppen-Mechanik.

**Belege:** `docs/work/wahapedia_orks/` (Kombi-Waffenprofile gegen Wahapedia geprüft, S152).

**Benötigte Regeln-Scopes:** —

**Herkunft:** `next_session.md` (S150, Punkt 5) / Stakeholder-Verifikation S146-Umfeld; als Waisen-Item ohne Backlog-ID im S151-C-Umbau gefunden (`docs/handoff/S151_briefing_umbau.md`), nachgetragen S151; Teil 2 S152-Planner-Befund.

## B-100 — unitCard GO Rand-Design fuer Spieler 2 spiegeln

[↩ Zeile in backlog.md](backlog.md#b-100)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Design-Crew → Executor

**Effort:** ~35k

**Detail-Beschreibung:** Betroffene Dateien: unitCard-Rand-CSS, GO-Karten-CSS. Der unitCard-Rand (heller Streifen links, Rest dunkler) gefällt dem Stakeholder gut - Wunsch: bei Spieler 2 vertikal spiegeln (heller Streifen rechts statt links), damit das Design zur Spielerseite passt statt fest links zu kleben. Zusätzlich soll dasselbe Rand-Prinzip auf GO-Karten übertragen werden - dort wirkt die aktuelle Gestaltung nach Stakeholder-Eindruck zu grell. Zwei Ziele (unitCard + GO-Karte), Konzept vor Umsetzung nötig (Rand-Design als eigener Design-System-Baustein?).

**Abhängigkeiten:** Konzept-Schritt zuerst (Design-Crew), da zwei Bausteine (unitCard, GO-Karte) betroffen sind; ggf. gemeinsam mit B-091 (Design-Block UI-Theme) einplanen.

**Belege:** Bildschirmfoto vom 2026-07-11 11-54-31 (Ist-Design unitCard-Rand).

**Benötigte Regeln-Scopes:** —

**Herkunft:** Stakeholder-Beobachtung, überführt S152.

## B-101 — Tesla Waffen Badge Wortlaut und Design Fix

[↩ Zeile in backlog.md](backlog.md#b-101)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~15k

**Detail-Beschreibung:** Betroffene Dateien: `src/uiLayout/diceHtml.py` (`special_die_html("Extra Hits", "unmod. 6 = +2 Hits")`, konsumiert `weapon_special.extra_hits` aus `necrons/weapons.yaml`, ausschließlich Tesla-Waffen). Stakeholder-Befund (Bildschirmfoto vom 2026-07-16 18-44-05): die Tesla-Fähigkeit (unmod. 6+ = 2 zusätzliche Treffer) wird als generische Weapon-Special-Badge "Extra Hits" gerendert statt im Design-System-konformen Buff-Badge-Stil (Vorbild: Vengeful-Stars-Buff-Badge, `value_triggered_die_row_html`). Zwei Korrekturen nötig: (a) Badge-Beschriftung auf "TESLA" ändern - "Extra Hits" ist erst 10E-Terminologie; (b) Badge-Optik an den Buff-Badge-Stil angleichen statt der aktuellen Weapon-Special-Optik.

**Abhängigkeiten:** Regel-Wortlaut vorher gegen `docs/work/wahapedia_necrons/` verifizieren (Tesla-Kartentext); Berührungspunkt mit B-012 (INV-4b Cluster 1 `weapon_special`-Schema für `dakka`/`klaw`/`tesla`) - falls B-012 zuerst läuft, im selben Aufwasch prüfen.

**Belege:** Bildschirmfoto vom 2026-07-16 18-44-05; `docs/spec/design_system.md` (Buff-Badge-Konvention).

**Benötigte Regeln-Scopes:** —

**Herkunft:** Stakeholder-Beobachtung, überführt S152.

## B-102 — Counter Offensive Box selten erreichbar

[↩ Zeile in backlog.md](backlog.md#b-102)

**Typ:** <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span>

**Status:** ToDo

**Tier:** Executor

**Effort:** ~M (15–35k, nach Lösungsansatz)

**Detail-Beschreibung:** Betroffene Dateien: `src/gameMechanic/fightPhase.py` (`_advance_fight_turn_if_needed`), `src/uiLayout/_common.py` (Counter-Offensive-Box-Render). In einfachen 1-gegen-1-Kampfsequenzen kippt `_advance_fight_turn_if_needed` den `fight_current_player` sofort auf die berechtigte Seite zurück, sobald eine Seite fertig ist (Spieler A → Spieler B → Spieler A). Dies führt dazu, dass `is_my_turn` True wird und die reaktive Counter-Offensive-Box (die an `is_my_turn == False` gebunden ist) gar nicht rendert. Das Phänomen ist nur dann sichtbar, wenn die Alternierung nicht sofort zurückspringt — etwa im Group-Assignment-Flow mit mehreren Gruppen, wo zwischen den Alternierungsschritten UI-Render stattfindet. **S155-Zusatzbefund:** Regelkonformität selbst ist korrekt (Counter-Offensive triggert tatsächlich erst NACH gegnerischem Fight), Hinweistext zur Verfügbarkeit wurde ergänzt (S155, Commit ab36b80). Hypothesis A (Triggermechanik OK) ist bestätigt — das Problem ist ein Timing-Issue bei der Box-Sichtbarkeit. **Zu klären:** Soll die Box in diesen Sequenzen anders angeboten werden (z. B. eigener Moment vor dem Rücksprung, oder über B-031 ausgrauen statt ausblenden)?

**Abhängigkeiten:** Abhängig von Architektur-Entscheid (Render-Moment vs. State-Change). Kann mit B-031 (GO-Konsistenz ausgrauen statt ausblenden) gelöst werden, falls dieser Ansatz verfolgt wird.

**Belege:** S155 E1-Befund, `docs/audit/plans/015-contextual-reactive-stratagems.md` (Counter-Offensive), Commit ab36b80 (Regel-Verifikation + Hinweistext).

**Benötigte Regeln-Scopes:** —

**Herkunft:** E1-Zusatzbefund S155 (Counter-Offensive-Verifikation, Hypothesis A bestätigt).
