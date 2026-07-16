# Backlog — zentraler Index

Arbiter ist ein digitaler Spielbegleiter für WH40k 9. Edition (Streamlit): er führt zwei Spieler
durch eine Partie — Phasen anzeigen, Einheitenstatus verwalten, Würfe berechnen.

**Aktives Ziel:** [Ziel 7 — Gefechtsoptionen + subfaction-Mechanik](ziel7.md) (🟨 aktiv, §0 Stufe A
erledigt S121, Rest offen). Bündelt (a) `collect_modifiers_for_phase`-Execute-Logik (§6e), (b) 6f
Ability-Badges, (c) 6h Kat1–3 neue Fraktionen (AdMech, Tyranids, T'au, Space Marines …).

**Geplant:** [Ziel 8 — Crusade-Erweiterung](ziel8.md) (⬜ noch nicht begonnen) ·
[Ziel 9 — Wahapedia Faction Fetcher](ziel9.md) (⬜ noch nicht begonnen, Richtungsentscheid B-088 offen).

Detailplanungen erledigter Ziele (1A–6): [archive/](archive/). Ausführliche Item-Begründungen:
[backlog_details.md](backlog_details.md). Erledigtes/Verworfenes: [backlog_archive.md](backlog_archive.md).

**Pflege-Regel:** Bereinigung an jedem Session-Start/-Ende — erledigte Items MIT ihrem
Details-Abschnitt aus `backlog_details.md` nach `backlog_archive.md` verschieben, hier die
Tabellenzeile löschen. Letzter Abgleich: **2026-07-16 (S151)**.

---

## Die Liste

Einzige Prioritätsquelle — sortiert nach Stakeholder-Priorität (Inventar-Reihenfolge S151).
B-092…B-097 (Klärungsfälle) stehen am Ende.

| ID | Status | Beschreibung | Abhängigkeiten | Effort | Assignee |
|---|---|---|---|---|---|
| [B-099](backlog_details.md#b-099--backlog-feinschliff-stakeholder-auflagen-s151) | ToDo | Backlog-Feinschliff (Stakeholder-Auflagen S151): Stale-Kandidaten B-092–B-097 löschen, Beschreibungs-/Spalten-/Effort-Format, Details-Template-Überarbeitung. | — | S | Executor |
| [B-001](backlog_details.md#b-001--fixd-brief-2-und-3-compute-render-folge) | Blocked | FixD Brief 2+3 (Compute/Render-Trennung `_common.py`) — Brief 2 hinter Mockup-Gate, Brief 3 Spec-Nachzug; entblockt mypy-uiLayout. | nach Rang 4 (erledigt); sequenziell Brief 2→3 | M | Executor |
| [B-002](backlog_details.md#b-002--klan-dynastie-brief-k1-wortlaut-bugfix-nihilakh-und-mephrit) | ToDo | Klan/Dynastie K1 — Wortlaut-Fix Nihilakh+Mephrit in `subfaction_abilities.yaml`; Entscheid bereits kanonisiert (S150). | Daten-Fix, kein Code-Blocker | S | Executor |
| [B-098](backlog_details.md#b-098--boss-nob-7b-kombi-waffenprofile) | ToDo | Boss Nob 7b — Kombi-Waffenprofile fehlen in `orks/weapons.yaml`; zweigeteilt: erst Profile ergänzen, dann ODER-Gruppe. | Daten-Fix, kein Code-Blocker | S | Executor |
| [B-003](backlog_details.md#b-003--klan-dynastie-k2-plus-novokh-sautekh-nephrekh-und-ork-snakebites) | ToDo | Klan/Dynastie K2+ — Novokh/Sautekh/Nephrekh + Ork Snakebites, Engine-Filter, 4 neue Effekttypen; macht 13 Einträge erstmals wirksam. | macht 13 Backlog-Einträge wirksam | L — vor Vergabe splitten | Planner→Executor |
| [B-004](backlog_details.md#b-004--mypy-ratchet-uilayout) | Blocked | mypy-Ratchet `uiLayout/` — letzte 17 Fehler (armyCard/gameProtocoll/unitCard/armyList/detachmentCard). | Dateiüberschneidung `_common.py` mit B-001 | M | Executor |
| [B-005](backlog_details.md#b-005--direktiv-lock-rest-ab-bewegungsphase-sperren) | ToDo | Direktiv-Lock-Rest — Protokoll-Direktiven ab der Bewegungsphase sperren (Setup-Leck bereits gefixt). | kein akuter Blocker | S | Executor |
| [B-006](backlog_details.md#b-006--abilityengine-refactor-vorplanung) | Blocked | abilityEngine-Refactor-Vorplanung — Planungspaket, kein Code; Split-Trigger erst ab ~800 Zeilen oder DRY-Angang. | orthogonal zu B-003 (K2 nutzt eigenes Modul) | S (~15–20k Token) | Planner |
| [B-007](backlog_details.md#b-007--backlog-restrukturierung) | In Progress | Backlog-Restrukturierung — dieser Auftrag selbst; schließt mit dem S151-Migrations-Handoff. | kein Eintrag darf verloren gehen | M | Planner→Stakeholder→Executor |
| [B-008](backlog_details.md#b-008--on-target-anker-option-a-ui-pruefung) | UI-Verifikation | on_target-Anker Option A — Code seit S146 fertig, nur die Stakeholder-UI-Prüfung steht noch aus. | Code erledigt (Rang 2) | XS | Stakeholder |
| [B-009](backlog_details.md#b-009--psi-flow-reset-ui-checks) | UI-Verifikation | PSI Flow/Reset — 4 manuelle UI-Checks (Undo-Deny, aktiv-Reset, Skip-Deny-Budget, Undo nach Fail-Deny); Code+Tests grün seit S65. | gemeinsamer Commit mit Token-Gauge-Hook geplant | S | Stakeholder |
| [B-010](backlog_details.md#b-010--protokoll-buff-audit-anzeige-rest) | Blocked | Protokoll-Buff-Audit — Anzeige-Rest (Eternal Guardian S SAVE-Hinweis hängt an Plan 015 Overwatch). | Engine-Seite komplett verdrahtet (Plan 024) | S | Executor |
| [B-011](backlog_details.md#b-011--wuerfelanzeige-pfeilrichtung-und-badge-breite) | ToDo | Würfelanzeige — Pfeilrichtung/-länge + Badge-Breite; Soll-Bild zuerst als AC in `dice_display.md` fixieren. | Soll-Bild → Plan 022 | S | Executor |
| [B-012](backlog_details.md#b-012--inv-4b-cluster-1-dakka-klaw-tesla-yaml-schema) | ToDo | INV-4b Cluster 1 — `dakka`/`klaw`/`tesla` als YAML-`weapon_special`-Schema statt Fraktions-Eigennamen in `src/`. | Cluster 3–6 bereits erledigt | S | Executor |
| [B-013](backlog_details.md#b-013--go-ui-paket-3b-before-battle-liste-armysetup) | ToDo | GO-UI Paket 3b — `before_battle`-Liste im ArmySetup macht 13 GOs erstmals sichtbar. | Teil der GO-UI-Roadmap (Entscheid S131) | M | Executor |
| [B-014](backlog_details.md#b-014--go-ui-folge-pakete-fuer-10-rest-gos) | ToDo | GO-UI Folge-Pakete für 10 Rest-GOs — generisches `on_destroy` (7 GOs) + `on_set_up`/`on_target`. | nach Paket 4 (erledigt); Paket-Nummern neu vergeben | M | Planner→Executor |
| [B-015](backlog_details.md#b-015--go-ui-paket-5-wortlaut-und-sprach-bereinigung) | ToDo | GO-UI Paket 5 — Wortlaut-/Sprachbereinigung (Englisch, Use/Undo/Confirm), eine CP-Anzeige, ein Stepper-Baustein. | Teil der Roadmap | M | Executor |
| [B-016](backlog_details.md#b-016--go-ui-paket-6-einheiten-auswahl-und-zielauswahl) | ToDo | GO-UI Paket 6 — Einheiten-Auswahl in die GameActionArea ziehen, Zielauswahl entschlacken. | eigenes Konzept-Inkrement | M | Design-Crew→Executor |
| [B-017](backlog_details.md#b-017--go-ui-danach-manuelle-ui-gesamt-verifikation) | Blocked | GO-UI „Danach" — manuelle UI-Gesamt-Verifikation nach Abschluss aller Pakete. | erst nach B-013…B-016 | S | Stakeholder |
| [B-018](backlog_details.md#b-018--fraktions-stratagems-before-battle-sichtbar-machen) | Blocked | Fraktions-Stratagems `before_battle` sichtbar machen — 6 Necron + 7 Ork, löst über B-013. | löst über B-013 | S | Executor |
| [B-019](backlog_details.md#b-019--alt-fire-chip-unerklaert) | ToDo | „Alt. Fire"-Chip unerklärt — Regel-Wortlaut prüfen (Haiku), dann Kurzerklärung ergänzen. | reiner Lookup + Ergänzung | XS | Executor (Haiku-Lookup) |
| [B-020](backlog_details.md#b-020--b2-spielvorbereitungsscreen-ueberarbeiten-konzept) | ToDo | B2 — Spielvorbereitungsscreen überarbeiten (Konzept); Struktur = Option C bereits entschieden. | Redundanz-Befunde B-021/B-022 einarbeiten | M | Design-Crew |
| [B-021](backlog_details.md#b-021--b4-rest-profilecard-als-datenkarte-setup) | ToDo | B4-Rest — profileCard als Datenkarte im Setup-Screen; App-Design-System + Wahapedia-IA entschieden. | nur Setup-Screen | M | Design-Crew→Executor |
| [B-022](backlog_details.md#b-022--b7-redundanter-kopfbereich-und-schwache-hinweise) | Blocked | B7 — Redundanter Kopfbereich + schwache Hinweise; Selbst-Stopp S149 (>4 Dateien). | betrifft `_common.py`, 3 `*Phase.py`, `PHASE_RULES` | M — vor Vergabe splitten | Planner→Executor |
| [B-023](backlog_details.md#b-023--b9-subphasen-schritte-unsichtbar-stepper-baustein) | ToDo | B9 — Subphasen-Schritte unsichtbar (Stepper-Baustein); läuft als ein Konzept-Handoff mit B-022. | 1 Konzept-Handoff mit B-022 | M | Design-Crew→Executor |
| [B-024](backlog_details.md#b-024--b10-kommentar-hygiene-ratchet-praxis) | In Progress | B10 — Kommentar-Hygiene als laufende Ratchet-Praxis bei jeder Modul-Berührung. | Konvention in CLAUDE.md verankert | — (laufend) | Executor (bei Modul-Berührung) |
| [B-025](backlog_details.md#b-025--b11-rest-wahrnehmung-nach-b1-fix) | ToDo | B11 — Rest-Wahrnehmung nach dem B1-Fix (kurzer Sprung/Zucken beim Slot-Wechsel). | B1 selbst gefixt | XS | Executor |
| [B-026](backlog_details.md#b-026--b12-go-used-zustand-gesamtkonzept) | ToDo | B12 — GO-„used"-Zustand Gesamtkonzept (Once-per-Phase-Erzwingung phasenübergreifend). | B12b (Header-Suffix) bereits erledigt | M — Teil-Briefs ≤M | Executor |
| [B-027](backlog_details.md#b-027--b12-optionaler-xs-task-unit-key-durch-spend-stratagem) | ToDo | B12 optional (Vermerk: optional) — `unit_key`/uid durch `spend_stratagem` durchreichen (Advance-Reroll/Overwatch-Randfall). | spec-konformer Randfall, kein Bug | XS | Executor |
| [B-028](backlog_details.md#b-028--b12-feature-wunsch-used-on-suffix-auf-alle-gos) | ToDo | B12 Feature-Wunsch — „used on ⟨Einheit⟩"-Suffix auf alle reaktiven GOs ausweiten. | nach dem BUG-Fix (erledigt) | M | Executor |
| [B-029](backlog_details.md#b-029--b13-go-karte-keyword-badges) | ToDo | B13 — GO-Karte: Keyword-Badges; Schema-Erweiterung + Datenpflege in einem Aufwasch. | keine Eil-Prio (Stakeholder) | M | Executor |
| [B-030](backlog_details.md#b-030--b14-badge-kontrast-pass-stationary-khaki) | Blocked | B14 — Badge-Kontrast-Pass (STATIONARY-Khaki zu dunkel); Hex-Vorschläge zuerst dem Stakeholder vorlegen. | Farbentscheid beim Stakeholder | XS | Stakeholder→Executor |
| [B-031](backlog_details.md#b-031--go-konsistenz-bedingungen-ausgrauen-statt-ausblenden) | ToDo | GO-Konsistenz — nicht erfüllte Bedingungen ausgrauen statt ausblenden (alle GOs). | passt zum bestehenden State-Modell | M | Executor |
| [B-032](backlog_details.md#b-032--psychic-ledger-schrumpfen) | ToDo | Psychic-Ledger schrumpfen — Smite-Manifest-Logik aus Render-Code extrahieren, Ledger 15→10. | — | M | Executor |
| [B-033](backlog_details.md#b-033--psychic-luecken-r-psychic-23-und-24) | ToDo | Psychic-Lücken R-PSYCHIC-23/24 — Unit-Destroyed-Check nach Perils-Schaden fehlt. | beide brauchen denselben Check | M | Executor |
| [B-034](backlog_details.md#b-034--save-block-faehigkeit-und-ap-als-eine-badge) | ToDo | SAVE-Block — Fähigkeit + AP als eine Badge (`Enslaved AP-1`). | → Plan 017 | S | Executor |
| [B-035](backlog_details.md#b-035--gretchin-cowardly-attrition-ohne-runtherd) | ToDo | Gretchin Cowardly — −1 Attrition ohne RUNTHERD in 6". | → Plan 018 | S | Executor |
| [B-036](backlog_details.md#b-036--battle-log-nach-reset-alte-eintraege) | ToDo | Battle-Log — nach Reset keine alten Einträge mehr. | → Plan 018 | XS | Executor |
| [B-037](backlog_details.md#b-037--collect-modifiers-for-phase) | ToDo | `collect_modifiers_for_phase()` — Teil von Plan 018 Task 18.4 und ziel7.md §6e. | → Plan 018 Task 18.4 | M | Executor |
| [B-038](backlog_details.md#b-038--totalvernichtungs-spielende-r-round-07) | ToDo | Totalvernichtungs-Spielende (R-ROUND-07) — Sieg durch Armee-Vernichtung fehlt als Spielende-Pfad. | eigener kleiner Plan | M | Executor |
| [B-039](backlog_details.md#b-039--tote-produktionsfunktion-build-aura-range-hint-text-entfernen) | ToDo | Tote Produktionsfunktion `build_aura_range_hint_text` entfernen — mit Tests gemeinsam. | mit Tests gemeinsam entfernen | XS | Executor |
| [B-040](backlog_details.md#b-040--fold-heuristik-und-subfaction-wiring-roster-zu-unit) | Blocked | Fold-Heuristik nur Hauptfraktion + Subfaction-Wiring Roster→Unit — wartet auf echte Subfraktions-Keywords. | wartet auf B-002/B-003 | S | Executor |
| [B-041](backlog_details.md#b-041--operating-model-phase-c-refinement-automatisieren) | ToDo | Operating-Model Phase C — Refinement automatisieren (Sonnet liest `Fotos/` → `docs/inbox/`). | — | M | Executor |
| [B-042](backlog_details.md#b-042--gates-und-reports-leser-orientiert-pruefen) | ToDo | Gates/Reports leser-orientiert prüfen (→ ADR-0002). | — | S | Executor |
| [B-043](backlog_details.md#b-043--invuln-save-badge-bereich-chaotisch) | ToDo | Invuln-SAVE-Badge-Bereich chaotisch — drei Teile zu einer klaren Badge zusammenfassen. | überschneidet Plan 017 | S | Executor |
| [B-044](backlog_details.md#b-044--dice-display-modifier-geometrie) | ToDo | Dice-Display Modifier-Geometrie — Debuff-Spreizung + Slot-1-Invariante fehlen. | eigener Plan | M | Executor |
| [B-045](backlog_details.md#b-045--silent-king-zielaufteilung-fernkampf) | ToDo | Silent-King-Zielaufteilung Fernkampf — zwei Fernkampfwaffen brauchen Ziel-pro-Waffe (regelwidrig aktuell). | Regel bereits geklärt (S80) | M | Executor |
| [B-046](backlog_details.md#b-046--off-scale-sieben-plus-save-grenze) | ToDo | Off-Scale-/„7+"-Save-Grenze — 7-Augen-Würfel + Erfolgsgrenze in der Dice-Spec ergänzen. | verwandt B-044 | S | Executor |
| [B-047](backlog_details.md#b-047--ap-und-save-modifier-magnitude-position) | ToDo | AP-/SAVE-Modifier-Magnitude-Position — Zahl gehört unter die Erfolgsgrenz-Spalte. | eng verwandt B-044 | S | Executor |
| [B-048](backlog_details.md#b-048--lethal-hits) | ToDo | Lethal Hits (R-CMB-XX) — unmod. Treffer-6 = direkter Schaden ohne Wundwurf. | eigener Plan nach Plan 014 | M | Executor |
| [B-049](backlog_details.md#b-049--deadly-demise) | ToDo | Deadly Demise (R-CMB-YY) — YAML-Daten vorhanden, Handler fehlt. | eigener Plan | M | Executor |
| [B-050](backlog_details.md#b-050--voice-of-the-triarch) | ToDo | Voice of the Triarch (R-CMD-XX, Silent King) — Handler fehlt, YAML-Basis fertig. | → Plan 016 oder eigener Plan | S | Executor |
| [B-051](backlog_details.md#b-051--failsafe-arkana-aktivator-ui-fehlt) | ToDo | Failsafe/Arkana-Aktivator-UI fehlt — `activated`-Fraktionsfähigkeiten bei `round_choice`-Fraktionen nie aktivierbar. | generischer Aktivator + CANOPTEK-Picker | M | Executor |
| [B-052](backlog_details.md#b-052--condition-prompt-applies-when-first-class-felder) | ToDo | `condition_prompt`/`applies_when` als First-Class-Felder statt Roh-Dict. | erst wenn 2. Konsument auftaucht | S | Executor |
| [B-053](backlog_details.md#b-053--daten-altlast-gretchin-mob) | ToDo | Daten-Altlast `gretchin_mob` — 8E-Formulierung gegen 9E-Regel prüfen. | — | XS | Executor (Haiku-Lookup) |
| [B-054](backlog_details.md#b-054--custodes-rendax-kath-secondary-toter-pfad) | ToDo | Custodes Rendax Ka'tah Secondary — toter `strength_modifier`-Pfad auf `strength_if_charged` umstellen. | Engine-Fn existiert bereits | S | Executor |
| [B-055](backlog_details.md#b-055--army-list-ux-weniger-scrollen) | ToDo | Army-List-UX „weniger Scrollen" — Auto-Ende, Fokus, Umsortieren; Streamlit-Machbarkeit zuerst klären. | eigener Plan | M — Machbarkeit zuerst klären | Executor |
| [B-056](backlog_details.md#b-056--quantum-shielding-fester-invuln-wert) | ToDo | Quantum Shielding — fester Invuln-Wert 4+ statt additivem Modifier + S148-Anzeige-Bug. | überschneidet Plan 017 | M | Executor |
| [B-057](backlog_details.md#b-057--waffen-block-rapid-fire-count-und-range-anzeigen) | ToDo | Waffen-Block — Rapid-Fire-Count + Reichweite je Waffe anzeigen. | eigener Plan | S | Executor |
| [B-058](backlog_details.md#b-058--dynastie-code-je-einheit-statt-roster-ebene) | ToDo | Dynastie-Code je Einheit statt Roster-Ebene (Mixed-Dynasty) — eigenes Konzept zuerst. | betrifft `subfaction_value_for`-Konsumenten | M — Konzept zuerst | Planner→Executor |
| [B-059](backlog_details.md#b-059--regel-index-fuer-wahapedia-texte) | ToDo | Regel-Index für Wahapedia-Texte — beschleunigt künftige Haiku-Lookups. | — | S | Executor |
| [B-060](backlog_details.md#b-060--claude-md-token-disziplin-entschlacken) | ToDo | CLAUDE.md Token-Disziplin entschlacken — Details nach `operating_model.md` verlagern. | CLAUDE.md-Änderung | XS — freigabepflichtig | Stakeholder→Executor |
| [B-061](backlog_details.md#b-061--backlog-paragraph-0-hygiene) | ToDo | Backlog-§0-Hygiene — durch die Restrukturierung (B-007) strukturell bereits erledigt. | überlappt B-007, bei Umsetzung zusammenlegen | XS | Executor |
| [B-062](backlog_details.md#b-062--audit-plaene-bereinigen) | ToDo | Audit-Pläne bereinigen (`docs/audit/plans/` + README-Queue), Tier Sonnet. | — | M | Executor |
| [B-063](backlog_details.md#b-063--boarding-actions-stratagems-laden) | Blocked | Boarding-Actions-Stratagems laden (NANOSCARAB VIRUS + MINDSHACKLE SCARABS). | → ziel7 Stufe C, hängt an B-003 | S | Executor |
| [B-064](backlog_details.md#b-064--variable-cp-kosten-in-der-ui-anzeigen) | ToDo | Variable CP-Kosten in der UI anzeigen (5 Necron-Stratagems). | UI-Design für Stratagem-Karte nötig | S | Design-Crew→Executor |
| [B-065](backlog_details.md#b-065--improve-session-vorbereiten) | ToDo | `/improve`-Session vorbereiten — bereinigte Plan-Queue + grüne Vollsuite als Baseline. | B-062 zuerst | S (Vorbereitung) | Stakeholder→Executor |
| [B-066](backlog_details.md#b-066--transport-insassen-feature-embark-disembark) | ToDo | Transport-Insassen-Feature (Embark/Disembark) (Vermerk: NIEDRIG) — 4 Bausteine, 2 offene Design-Fragen. | Voraussetzung für Emergency-Disembarkation-Anzeige | S–M | Planner→Executor |
| [B-067](backlog_details.md#b-067--roster-builder-anforderung-before-battle-stratagems) | ToDo | Roster-Builder-Anforderung — `before_battle`-Stratagems müssen dort auswählbar sein. | beim Bau des Roster-Builders berücksichtigen | — | Planner |
| [B-068](backlog_details.md#b-068--ux-nit-silent-king-zusatzattacken-default) | ToDo | UX-Nit — Silent-King-Zusatzattacken-Default auf Maximum vorbelegen. | — | XS/S | Executor |
| [B-069](backlog_details.md#b-069--camelcase-umbenennung) | ToDo | camelCase-Umbenennung — 4 Teil-Briefs laut Mapping-Tabelle in `loader_contract.md` §8. | Reihenfolge: Stratagem-Kollision → Rest-Felder → Necron → Ork | 4 Teil-Briefs ≤M | Executor |
| [B-070](backlog_details.md#b-070--reanimation-konsistenz-umsetzung) | ToDo | Reanimation-Konsistenz — Stratagem-Variante wie Ability-Variante zählen (Entscheid gefallen). | Entscheid bereits gefallen (S148) | M/L (Modell-Auswahl-UI) | Executor |
| [B-071](backlog_details.md#b-071--auto-wound-prueft-keine-gauss-tesla-bedingung) | ToDo | `auto_wound` prüft keine Gauss-/Tesla-Waffenbedingung — tiefere Lücke als der S149-Bedingungsfix. | Bedingungs-Lücke bereits gefixt | S | Executor |
| [B-072](backlog_details.md#b-072--roster-daten-konsistenz-recherche) | ToDo | Roster-/Daten-Konsistenz-Recherche — CORE-Keyword Annihilation Barge/Flayed Ones, Ork Boss Nob Waffen. | reiner Datenabgleich | XS | Executor (Haiku) |
| [B-073](backlog_details.md#b-073--model-groups-union-ungenauigkeit) | ToDo | `model_groups`-Union-Ungenauigkeit — `grantsKeyword` zu breit bei gemischter Bewaffnung. | keine Regression, bei nächster `model_groups`-Arbeit mitprüfen | S | Executor |
| [B-074](backlog_details.md#b-074--ziel7-stufe-c-vorbereitung-emergency-disembarkation) | UI-Verifikation | Ziel7 Stufe C-Vorbereitung — Emergency Disembarkation am Ork-Transport-Roster real prüfen. | jetzt möglich (`orks_transport.yaml`) | XS | Stakeholder |
| [B-075](backlog_details.md#b-075--mypy-rest-gamemechanic) | ToDo | mypy-Rest `gameMechanic/` außerhalb des `state`-Contracts (7 Fehler). | eigenständig von B-004 | S | Executor |
| [B-076](backlog_details.md#b-076--layer-kopplung-gamemechanic-importiert-uilayout) | ToDo | Layer-Kopplung — `gameMechanic/*Phase.py` importiert `uiLayout._common`; bewusst noch nicht erzwungen. | Aufräum-Pfad: Phasen-Render nach `uiLayout/` | L | Planner |
| [B-077](backlog_details.md#b-077--common-py-refactoren) | ToDo | `_common.py` refactoren (2218 Zeilen) — Attackensequenz als eigene Datei. | gleicher Render-Hub wie B-076 | L — vor Vergabe splitten | Planner→Executor |
| [B-078](backlog_details.md#b-078--test-mock-fragilitaet-und-conftest-mock-hack) | ToDo | Test-Mock-Fragilität + conftest-Mock-Hack — geteilte `streamlit`-Fixture statt Modul-Mocks. | S110-Retro M1+M2, gemeinsame Lösung | M | Executor |
| [B-079](backlog_details.md#b-079--dry-plus-minus-eins-cap-helper) | ToDo | DRY ±1-Cap-Helper (`diceHtml.py` Hit-/Wound-Block). | S110-Retro M1 | XS | Executor |
| [B-080](backlog_details.md#b-080--dry-zwei-sechs-cap-quelle) | ToDo | DRY [2,6]-Cap-Quelle (`combat.py` vs. `diceHtml.py`) — Sync-Risiko, kein akuter Bug. | S144-Review Befund 2 | S | Executor |
| [B-081](backlog_details.md#b-081--dry-directive-aktiv-logik) | ToDo | DRY Directive-Aktiv-Logik (`gameState.py` vs. `abilityEngine.py`) — braucht drittes Modul. | S143-Refactor-Befund Punkt 4 | S | Executor |
| [B-082](backlog_details.md#b-082--executor-auftrags-checkliste-haerten) | ToDo | Executor-Auftrags-Checkliste härten — `ruff` vor „grün"-Claim + Token-/Zeit-Cap. | betrifft `agent_scopes.md` | XS | Planner |
| [B-083](backlog_details.md#b-083--architecture-md-doku-session) | Blocked | `architecture.md` Doku-Session — 4 Drift-Befunde + `auto_round_1`-Altlast bereinigen. | freigabepflichtig | S | Stakeholder→Executor |
| [B-084](backlog_details.md#b-084--mortal-wounds-text-match-erkennung) | ToDo | Mortal-Wounds-Text-Match-Erkennung — strukturiertes YAML-Feld statt Text-Match. | kein akuter Block | S | Executor |
| [B-085](backlog_details.md#b-085--faction-abilities-md-kategorie-6-veraltet) | Blocked | `faction_abilities.md` Kategorie 6 veraltet — Spec-Nachzug nach K2+ (B-003). | nach B-003 | XS | Executor |
| [B-086](backlog_details.md#b-086--test-schuld-klein-tautologie-tests) | ToDo | §4d Test-Schuld — 2 Tautologie-Tests schärfen + Mock-Konsolidierung (11 Testdateien). | kein Blocker, verwandt B-078 | S | Executor |
| [B-087](backlog_details.md#b-087--f4-stufe-a-verifikationspunkte-3-und-4) | Blocked | F4 — Stufe-A-Verifikationspunkte 3+4 (Fire Overwatch/Counter-Offensive) — braucht Plan 015. | Plan 015 Priorität P2 | XS (reine Prüfung) | Stakeholder |
| [B-088](backlog_details.md#b-088--richtungsentscheid-ziel9-fetcher-vorziehen) | Blocked | Richtungsentscheid ziel9-Fetcher vorziehen? — Stakeholder-Entscheidung steht aus. | Audit S124, verschoben S129 | — (Entscheidung) | Stakeholder |
| [B-089](backlog_details.md#b-089--ziel-8-crusade-erweiterung) | ToDo | Ziel 8 — Crusade-Erweiterung (geplant, noch nicht begonnen). | — | L — bei Aufnahme splitten | Planner |
| [B-090](backlog_details.md#b-090--ziel-9-wahapedia-faction-fetcher) | ToDo | Ziel 9 — Wahapedia Faction Fetcher (geplant, noch nicht begonnen). | Richtungsentscheid B-088 offen | L — bei Aufnahme splitten | Planner |
| [B-091](backlog_details.md#b-091--design-block-ui-theme) | ToDo | Design-Block — UI-Theme (Farbpalette, Badge-Optik, Einheitenkarten-Layout). | 3 Teilpunkte, bündeln oder einzeln vergeben | M | Design-Crew |
| [B-092](backlog_details.md#b-092--go-ui-paket-1-go-karten-baustein-stale-glyph-verdacht) | Blocked | GO-UI Paket 1 — GO-Karten-Baustein; Glyph-Stand widerspricht Paket 3a, Stale-Verdacht. | Klärung vor Zuweisung | — | Planner |
| [B-093](backlog_details.md#b-093--go-ui-paket-2-command-re-roll-stale-glyph-verdacht) | Blocked | GO-UI Paket 2 — Command-Re-Roll; `git log` deutet auf Erledigung hin, Stale-Verdacht. | Klärung vor Zuweisung | — | Planner |
| [B-094](backlog_details.md#b-094--go-buttons-kontextuell-in-gameactionarea) | Blocked | GO-Buttons kontextuell in gameActionArea statt Liste — evtl. durch GO-UI-Roadmap überholt. | Klärung vor Zuweisung | — | Planner |
| [B-095](backlog_details.md#b-095--necron-command-phase-regelkasten-immer-oben) | Blocked | Necron Command Phase — Regelkasten immer ganz oben (alle Phasen prüfen). | Klärung vor Zuweisung | — | Planner |
| [B-096](backlog_details.md#b-096--bug-aktive-go-effekte-ohne-badge-am-wirkort) | Blocked | Bug — aktive GO-Effekte ohne Badge am Wirkort (4 GOs) — Abdeckung durch S148-Fixes unklar. | Klärung vor Zuweisung | — | Planner |
| [B-097](backlog_details.md#b-097--command-protocol-direktiven-nicht-regelkonform-s95-befund) | Blocked | Command-Protocol-Direktiven nicht regelkonform (S95) — Plan 025 ist archiviert, Glyph wirkt stale. | Klärung vor Zuweisung | — | Planner |

---

## Legende

**Status:**

- `ToDo` — bereit, wartet auf Einplanung.
- `In Progress` — läuft aktuell.
- `Review` — Umsetzung fertig, wartet auf Review/Freigabe.
- `UI-Verifikation` — Code+Tests grün, manuelle Stakeholder-Prüfung des Render-Codes steht aus
  (Render-Code ist von der Coverage ausgenommen, s. `CLAUDE.md`).
- `Blocked` — wartet auf eine Abhängigkeit, einen Stakeholder-Entscheid oder eine Klärung.
- `Done` erscheint hier **nie** — erledigte Items wandern sofort samt Detail-Abschnitt ins Archiv
  (s. Pflege-Regel oben).

**Effort:** `XS` < 1h · `S` ≤ halber Tag · `M` ≤ 1 Tag · `L` > 1 Tag — **L wird vor Vergabe in
≤ M-Briefs gesplittet** (S130-Auflage, s. `feedback_executor_briefs_max_m` im Memory).

**Assignee-Rollen:** `Stakeholder` (Entscheidung/manuelle UI-Prüfung) · `Planner` (Konzept/Split
vor Vergabe) · `Executor` (Umsetzung, Default-Tier Sonnet; reine Lookups per Auftrag explizit auf
Haiku) · `Design-Crew` (UI/UX-Konzept vor Umsetzung). Pfeile (`A→B`) zeigen die Reihenfolge.

**Abhängigkeiten-Notation:** Freitext, der auf blockierende IDs, Dateien oder externe
Entscheidungen verweist — für die volle Begründung immer den Link in der ID-Spalte öffnen
(`backlog_details.md`, Feld „Abhängigkeiten (Begründung)").

**Neues Item aufnehmen:** nächste freie `B-NNN`-ID vergeben, Zeile hier einfügen (Position =
Stakeholder-Priorität), vollen Kontext in `backlog_details.md` unter `## B-NNN — Titel` anlegen
(Feldschema dort dokumentiert).

**Bereinigen:** Item erledigt/verworfen → Detail-Abschnitt aus `backlog_details.md` **inklusive**
Fakten/Links/Commits nach `backlog_archive.md` verschieben (Format der bestehenden Einträge
folgen), Zeile hier löschen. Nie nur die Zeile löschen ohne den Detail-Abschnitt nachzuziehen —
sonst geht die Begründung verloren.
