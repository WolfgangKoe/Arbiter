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
Tabellenzeile löschen. Letzter Abgleich: **2026-07-16 (S152, B-002+B-099 archiviert,
B-098/B-056/B-028 aktualisiert, B-100/B-101 neu — Stakeholder-Beobachtungen überführt; UI-
Verifikationsrunde: B-008+B-074 positiv → archiviert, B-009+B-087 Nacharbeit → ToDo, Neuvorlage
S153)**.

---

## Die Liste

Einzige Prioritätsquelle — sortiert nach Stakeholder-Priorität (Inventar-Reihenfolge S151).

| ID&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Status | Beschreibung | Abhängigkeiten | Effort | Assignee |
|---|---|---|---|---|---|
| [B-001](backlog_details.md#b-001--fixd-brief-2-und-3-compute-render-folge)     | Blocked | <a id="b-001"></a>FixD Brief 2+3 (Compute/Render-Trennung `_common.py`) — Brief 2 hinter Mockup-Gate, Brief 3 Spec-Nachzug; entblockt mypy-uiLayout.<br><span style="color:#c2410c">**Schuldabbau**</span><br>Blocker: Mockup-Gate | nach Rang 4 (erledigt); sequenziell Brief 2→3 | ~35k | Executor |
| [B-098](backlog_details.md#b-098--boss-nob-7b-kombi-waffenprofile)     | ToDo | <a id="b-098"></a>Boss Nob 7b Teil 2 — Kombi-Waffenprofile (Teil 1 in `orks/weapons.yaml` erledigt S152); `weapon_swap` fehlt + Kombi-Mechanik braucht Engine-Erweiterung (S152-Planner-Befund).<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | Engine-Erweiterung nötig, kein reiner Daten-Fix mehr | ~35k | Executor |
| [B-003](backlog_details.md#b-003--klan-dynastie-k2-plus-novokh-sautekh-nephrekh-und-ork-snakebites)     | ToDo | <a id="b-003"></a>Klan/Dynastie K2+ — Novokh/Sautekh/Nephrekh + Ork Snakebites, Engine-Filter, 4 neue Effekttypen; macht 13 Einträge erstmals wirksam.<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | macht 13 Backlog-Einträge wirksam | ~70k+<br>— vor Vergabe<br>splitten | Planner→Executor |
| [B-004](backlog_details.md#b-004--mypy-ratchet-uilayout)     | Blocked | <a id="b-004"></a>mypy-Ratchet `uiLayout/` — letzte 17 Fehler (armyCard/gameProtocoll/unitCard/armyList/detachmentCard).<br><span style="color:#c2410c">**Schuldabbau**</span><br>Blocker: B-001 | Dateiüberschneidung `_common.py` mit B-001 | ~35k | Executor |
| [B-005](backlog_details.md#b-005--direktiv-lock-rest-ab-bewegungsphase-sperren)     | ToDo | <a id="b-005"></a>Direktiv-Lock-Rest — Protokoll-Direktiven ab der Bewegungsphase sperren (Setup-Leck bereits gefixt).<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | kein akuter Blocker | ~15k | Executor |
| [B-006](backlog_details.md#b-006--abilityengine-refactor-vorplanung)     | Blocked | <a id="b-006"></a>abilityEngine-Refactor-Vorplanung — Planungspaket, kein Code; Split-Trigger erst ab ~800 Zeilen oder DRY-Angang.<br><span style="color:#c2410c">**Schuldabbau**</span><br>Blocker: Schwellwert ~800 Zeilen abilityEngine.py / DRY-Angang | orthogonal zu B-003 (K2 nutzt eigenes Modul) | ~15–20k | Planner |
| [B-007](backlog_details.md#b-007--backlog-restrukturierung)     | In Progress | <a id="b-007"></a>Backlog-Restrukturierung — dieser Auftrag selbst; schließt mit dem S151-Migrations-Handoff.<br><span style="color:#1e3a8a">**Prozess/Doku**</span> | kein Eintrag darf verloren gehen | ~35k | Planner→<br>Stakeholder→<br>Executor |
| [B-009](backlog_details.md#b-009--psi-flow-reset-ui-checks)     | ToDo | <a id="b-009"></a>PSI Flow/Reset — 4 manuelle UI-Checks; S152-Prüfung ergab: Testvoraussetzungen (zwei geeignete Roster) nicht benannt — Nacharbeit + Neuvorlage S153.<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | Roster für den Test klar benennen | ~15k | Executor→<br>Stakeholder |
| [B-010](backlog_details.md#b-010--protokoll-buff-audit-anzeige-rest)     | Blocked | <a id="b-010"></a>Protokoll-Buff-Audit — Anzeige-Rest (Eternal Guardian S SAVE-Hinweis hängt an Plan 015 Overwatch).<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span><br>Blocker: Plan 015 | Engine-Seite komplett verdrahtet (Plan 024) | ~15k | Executor |
| [B-011](backlog_details.md#b-011--wuerfelanzeige-pfeilrichtung-und-badge-breite)     | ToDo | <a id="b-011"></a>Würfelanzeige — Pfeilrichtung/-länge + Badge-Breite; Soll-Bild zuerst als AC in `dice_display.md` fixieren.<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | Soll-Bild → Plan 022 | ~15k | Executor |
| [B-012](backlog_details.md#b-012--inv-4b-cluster-1-dakka-klaw-tesla-yaml-schema)     | ToDo | <a id="b-012"></a>INV-4b Cluster 1 — `dakka`/`klaw`/`tesla` als YAML-`weapon_special`-Schema statt Fraktions-Eigennamen in `src/`.<br><span style="color:#c2410c">**Schuldabbau**</span> | Cluster 3–6 bereits erledigt | ~15k | Executor |
| [B-013](backlog_details.md#b-013--go-ui-paket-3b-before-battle-liste-armysetup)     | ToDo | <a id="b-013"></a>GO-UI Paket 3b — `before_battle`-Liste im ArmySetup macht 13 GOs erstmals sichtbar.<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | Teil der GO-UI-Roadmap (Entscheid S131) | ~35k | Executor |
| [B-014](backlog_details.md#b-014--go-ui-folge-pakete-fuer-10-rest-gos)     | ToDo | <a id="b-014"></a>GO-UI Folge-Pakete für 10 Rest-GOs — generisches `on_destroy` (7 GOs) + `on_set_up`/`on_target`.<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | nach Paket 4 (erledigt); Paket-Nummern neu vergeben | ~35k | Planner→Executor |
| [B-015](backlog_details.md#b-015--go-ui-paket-5-wortlaut-und-sprach-bereinigung)     | ToDo | <a id="b-015"></a>GO-UI Paket 5 — Wortlaut-/Sprachbereinigung (Englisch, Use/Undo/Confirm), eine CP-Anzeige, ein Stepper-Baustein.<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | Teil der Roadmap | ~35k | Executor |
| [B-016](backlog_details.md#b-016--go-ui-paket-6-einheiten-auswahl-und-zielauswahl)     | ToDo | <a id="b-016"></a>GO-UI Paket 6 — Einheiten-Auswahl in die GameActionArea ziehen, Zielauswahl entschlacken.<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | eigenes Konzept-Inkrement | ~35k | Design-Crew→<br>Executor |
| [B-017](backlog_details.md#b-017--go-ui-danach-manuelle-ui-gesamt-verifikation)     | Blocked | <a id="b-017"></a>GO-UI „Danach" — manuelle UI-Gesamt-Verifikation nach Abschluss aller Pakete.<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span><br>Blocker: B-013–B-016 | erst nach B-013…B-016 | ~15k | Stakeholder |
| [B-018](backlog_details.md#b-018--fraktions-stratagems-before-battle-sichtbar-machen)     | Blocked | <a id="b-018"></a>Fraktions-Stratagems `before_battle` sichtbar machen — 6 Necron + 7 Ork, löst über B-013.<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span><br>Blocker: B-013 | löst über B-013 | ~15k | Executor |
| [B-019](backlog_details.md#b-019--alt-fire-chip-unerklaert)     | ToDo | <a id="b-019"></a>„Alt. Fire"-Chip unerklärt — Regel-Wortlaut prüfen (Haiku), dann Kurzerklärung ergänzen.<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | reiner Lookup + Ergänzung | ~5k | Executor<br>(Haiku-Lookup) |
| [B-020](backlog_details.md#b-020--b2-spielvorbereitungsscreen-ueberarbeiten-konzept)     | ToDo | <a id="b-020"></a>B2 — Spielvorbereitungsscreen überarbeiten (Konzept); Struktur = Option C bereits entschieden.<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | Redundanz-Befunde B-021/B-022 einarbeiten | ~35k | Design-Crew |
| [B-021](backlog_details.md#b-021--b4-rest-profilecard-als-datenkarte-setup)     | ToDo | <a id="b-021"></a>B4-Rest — profileCard als Datenkarte im Setup-Screen; App-Design-System + Wahapedia-IA entschieden.<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | nur Setup-Screen | ~35k | Design-Crew→<br>Executor |
| [B-022](backlog_details.md#b-022--b7-redundanter-kopfbereich-und-schwache-hinweise)     | Blocked | <a id="b-022"></a>B7 — Redundanter Kopfbereich + schwache Hinweise; Selbst-Stopp S149 (>4 Dateien).<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span><br>Blocker: Planner-Split (>4-Dateien-Schwelle) | betrifft `_common.py`, 3 `*Phase.py`, `PHASE_RULES` | ~35k<br>— vor Vergabe<br>splitten | Planner→Executor |
| [B-023](backlog_details.md#b-023--b9-subphasen-schritte-unsichtbar-stepper-baustein)     | ToDo | <a id="b-023"></a>B9 — Subphasen-Schritte unsichtbar (Stepper-Baustein); läuft als ein Konzept-Handoff mit B-022.<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | 1 Konzept-Handoff mit B-022 | ~35k | Design-Crew→<br>Executor |
| [B-024](backlog_details.md#b-024--b10-kommentar-hygiene-ratchet-praxis)     | In Progress | <a id="b-024"></a>B10 — Kommentar-Hygiene als laufende Ratchet-Praxis bei jeder Modul-Berührung.<br><span style="color:#1e3a8a">**Prozess/Doku**</span> | Konvention in CLAUDE.md verankert | —<br>(laufend, kein<br>fixer Umfang) | Executor<br>(bei<br>Modul-Berührung) |
| [B-025](backlog_details.md#b-025--b11-rest-wahrnehmung-nach-b1-fix)     | ToDo | <a id="b-025"></a>B11 — Rest-Wahrnehmung nach dem B1-Fix (kurzer Sprung/Zucken beim Slot-Wechsel).<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | B1 selbst gefixt | ~5k | Executor |
| [B-026](backlog_details.md#b-026--b12-go-used-zustand-gesamtkonzept)     | ToDo | <a id="b-026"></a>B12 — GO-„used"-Zustand Gesamtkonzept (Once-per-Phase-Erzwingung phasenübergreifend).<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | B12b (Header-Suffix) bereits erledigt | ~35k<br>— Teil-Briefs<br>≤~35k je Teil | Executor |
| [B-027](backlog_details.md#b-027--b12-optionaler-xs-task-unit-key-durch-spend-stratagem)     | ToDo | <a id="b-027"></a>B12 optional (Vermerk: optional) — `unit_key`/uid durch `spend_stratagem` durchreichen (Advance-Reroll/Overwatch-Randfall).<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | spec-konformer Randfall, kein Bug | ~5k | Executor |
| [B-028](backlog_details.md#b-028--b12-feature-wunsch-used-on-suffix-auf-alle-gos)     | ToDo | <a id="b-028"></a>B12 Feature-Wunsch — „used on ⟨Einheit⟩"-Suffix auf alle reaktiven GOs ausweiten; fest für S153 eingeplant (Stakeholder-Entscheid S152).<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | nach dem BUG-Fix (erledigt) | ~35k | Executor |
| [B-029](backlog_details.md#b-029--b13-go-karte-keyword-badges)     | ToDo | <a id="b-029"></a>B13 — GO-Karte: Keyword-Badges; Schema-Erweiterung + Datenpflege in einem Aufwasch.<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | keine Eil-Prio (Stakeholder) | ~35k | Executor |
| [B-030](backlog_details.md#b-030--b14-badge-kontrast-pass-stationary-khaki)     | Blocked | <a id="b-030"></a>B14 — Badge-Kontrast-Pass (STATIONARY-Khaki zu dunkel); Hex-Vorschläge zuerst dem Stakeholder vorlegen.<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span><br>Blocker: Stakeholder-Entscheid (Hex-Vorschläge) | Farbentscheid beim Stakeholder | ~5k | Stakeholder→<br>Executor |
| [B-031](backlog_details.md#b-031--go-konsistenz-bedingungen-ausgrauen-statt-ausblenden)     | ToDo | <a id="b-031"></a>GO-Konsistenz — nicht erfüllte Bedingungen ausgrauen statt ausblenden (alle GOs).<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | passt zum bestehenden State-Modell | ~35k | Executor |
| [B-032](backlog_details.md#b-032--psychic-ledger-schrumpfen)     | ToDo | <a id="b-032"></a>Psychic-Ledger schrumpfen — Smite-Manifest-Logik aus Render-Code extrahieren, Ledger 15→10.<br><span style="color:#c2410c">**Schuldabbau**</span> | — | ~35k | Executor |
| [B-033](backlog_details.md#b-033--psychic-luecken-r-psychic-23-und-24)     | ToDo | <a id="b-033"></a>Psychic-Lücken R-PSYCHIC-23/24 — Unit-Destroyed-Check nach Perils-Schaden fehlt.<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | beide brauchen denselben Check | ~35k | Executor |
| [B-034](backlog_details.md#b-034--save-block-faehigkeit-und-ap-als-eine-badge)     | ToDo | <a id="b-034"></a>SAVE-Block — Fähigkeit + AP als eine Badge (`Enslaved AP-1`).<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | → Plan 017 | ~15k | Executor |
| [B-035](backlog_details.md#b-035--gretchin-cowardly-attrition-ohne-runtherd)     | ToDo | <a id="b-035"></a>Gretchin Cowardly — −1 Attrition ohne RUNTHERD in 6".<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | → Plan 018 | ~15k | Executor |
| [B-036](backlog_details.md#b-036--battle-log-nach-reset-alte-eintraege)     | ToDo | <a id="b-036"></a>Battle-Log — nach Reset keine alten Einträge mehr.<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | → Plan 018 | ~5k | Executor |
| [B-037](backlog_details.md#b-037--collect-modifiers-for-phase)     | ToDo | <a id="b-037"></a>`collect_modifiers_for_phase()` — Teil von Plan 018 Task 18.4 und ziel7.md §6e.<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | → Plan 018 Task 18.4 | ~35k | Executor |
| [B-038](backlog_details.md#b-038--totalvernichtungs-spielende-r-round-07)     | ToDo | <a id="b-038"></a>Totalvernichtungs-Spielende (R-ROUND-07) — Sieg durch Armee-Vernichtung fehlt als Spielende-Pfad.<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | eigener kleiner Plan | ~35k | Executor |
| [B-040](backlog_details.md#b-040--fold-heuristik-und-subfaction-wiring-roster-zu-unit)     | Blocked | <a id="b-040"></a>Fold-Heuristik nur Hauptfraktion + Subfaction-Wiring Roster→Unit — wartet auf echte Subfraktions-Keywords.<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span><br>Blocker: B-002 / B-003 | wartet auf B-002/B-003 | ~15k | Executor |
| [B-041](backlog_details.md#b-041--operating-model-phase-c-refinement-automatisieren)     | ToDo | <a id="b-041"></a>Operating-Model Phase C — Refinement automatisieren (Sonnet liest `Fotos/` → `docs/inbox/`).<br><span style="color:#1e3a8a">**Prozess/Doku**</span> | — | ~35k | Executor |
| [B-042](backlog_details.md#b-042--gates-und-reports-leser-orientiert-pruefen)     | ToDo | <a id="b-042"></a>Gates/Reports leser-orientiert prüfen (→ ADR-0002).<br><span style="color:#1e3a8a">**Prozess/Doku**</span> | — | ~15k | Executor |
| [B-043](backlog_details.md#b-043--invuln-save-badge-bereich-chaotisch)     | ToDo | <a id="b-043"></a>Invuln-SAVE-Badge-Bereich chaotisch — drei Teile zu einer klaren Badge zusammenfassen.<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | überschneidet Plan 017 | ~15k | Executor |
| [B-044](backlog_details.md#b-044--dice-display-modifier-geometrie)     | ToDo | <a id="b-044"></a>Dice-Display Modifier-Geometrie — Debuff-Spreizung + Slot-1-Invariante fehlen.<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | eigener Plan | ~35k | Executor |
| [B-045](backlog_details.md#b-045--silent-king-zielaufteilung-fernkampf)     | ToDo | <a id="b-045"></a>Silent-King-Zielaufteilung Fernkampf — zwei Fernkampfwaffen brauchen Ziel-pro-Waffe (regelwidrig aktuell).<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | Regel bereits geklärt (S80) | ~35k | Executor |
| [B-046](backlog_details.md#b-046--off-scale-sieben-plus-save-grenze)     | ToDo | <a id="b-046"></a>Off-Scale-/„7+"-Save-Grenze — 7-Augen-Würfel + Erfolgsgrenze in der Dice-Spec ergänzen.<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | verwandt B-044 | ~15k | Executor |
| [B-047](backlog_details.md#b-047--ap-und-save-modifier-magnitude-position)     | ToDo | <a id="b-047"></a>AP-/SAVE-Modifier-Magnitude-Position — Zahl gehört unter die Erfolgsgrenz-Spalte.<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | eng verwandt B-044 | ~15k | Executor |
| [B-048](backlog_details.md#b-048--lethal-hits)     | ToDo | <a id="b-048"></a>Lethal Hits (R-CMB-XX) — unmod. Treffer-6 = direkter Schaden ohne Wundwurf.<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | eigener Plan nach Plan 014 | ~35k | Executor |
| [B-049](backlog_details.md#b-049--deadly-demise)     | ToDo | <a id="b-049"></a>Deadly Demise (R-CMB-YY) — YAML-Daten vorhanden, Handler fehlt.<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | eigener Plan | ~35k | Executor |
| [B-050](backlog_details.md#b-050--voice-of-the-triarch)     | ToDo | <a id="b-050"></a>Voice of the Triarch (R-CMD-XX, Silent King) — Handler fehlt, YAML-Basis fertig.<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | → Plan 016 oder eigener Plan | ~15k | Executor |
| [B-051](backlog_details.md#b-051--failsafe-arkana-aktivator-ui-fehlt)     | ToDo | <a id="b-051"></a>Failsafe/Arkana-Aktivator-UI fehlt — `activated`-Fraktionsfähigkeiten bei `round_choice`-Fraktionen nie aktivierbar.<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | generischer Aktivator + CANOPTEK-Picker | ~35k | Executor |
| [B-052](backlog_details.md#b-052--condition-prompt-applies-when-first-class-felder)     | ToDo | <a id="b-052"></a>`condition_prompt`/`applies_when` als First-Class-Felder statt Roh-Dict.<br><span style="color:#c2410c">**Schuldabbau**</span> | erst wenn 2. Konsument auftaucht | ~15k | Executor |
| [B-053](backlog_details.md#b-053--daten-altlast-gretchin-mob)     | ToDo | <a id="b-053"></a>Daten-Altlast `gretchin_mob` — 8E-Formulierung gegen 9E-Regel prüfen.<br><span style="color:#c2410c">**Schuldabbau**</span> | — | ~5k | Executor<br>(Haiku-Lookup) |
| [B-054](backlog_details.md#b-054--custodes-rendax-kath-secondary-toter-pfad)     | ToDo | <a id="b-054"></a>Custodes Rendax Ka'tah Secondary — toter `strength_modifier`-Pfad auf `strength_if_charged` umstellen.<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | Engine-Fn existiert bereits | ~15k | Executor |
| [B-055](backlog_details.md#b-055--army-list-ux-weniger-scrollen)     | ToDo | <a id="b-055"></a>Army-List-UX „weniger Scrollen" — Auto-Ende, Fokus, Umsortieren; Streamlit-Machbarkeit zuerst klären.<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | eigener Plan | ~35k<br>— Machbarkeit<br>zuerst klären | Executor |
| [B-056](backlog_details.md#b-056--quantum-shielding-fester-invuln-wert)     | ToDo | <a id="b-056"></a>Quantum Shielding — fester Invuln-Wert 4+ statt additivem Modifier + S148-Anzeige-Bug; Scope S152 (b) fest für S153 geplant.<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | überschneidet Plan 017 | ~35k | Executor |
| [B-057](backlog_details.md#b-057--waffen-block-rapid-fire-count-und-range-anzeigen)     | ToDo | <a id="b-057"></a>Waffen-Block — Rapid-Fire-Count + Reichweite je Waffe anzeigen.<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | eigener Plan | ~15k | Executor |
| [B-058](backlog_details.md#b-058--dynastie-code-je-einheit-statt-roster-ebene)     | ToDo | <a id="b-058"></a>Dynastie-Code je Einheit statt Roster-Ebene (Mixed-Dynasty) — eigenes Konzept zuerst.<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | betrifft `subfaction_value_for`-Konsumenten | ~35k<br>— Konzept zuerst | Planner→Executor |
| [B-059](backlog_details.md#b-059--regel-index-fuer-wahapedia-texte)     | ToDo | <a id="b-059"></a>Regel-Index für Wahapedia-Texte — beschleunigt künftige Haiku-Lookups.<br><span style="color:#1e3a8a">**Prozess/Doku**</span> | — | ~15k | Executor |
| [B-060](backlog_details.md#b-060--claude-md-token-disziplin-entschlacken)     | ToDo | <a id="b-060"></a>CLAUDE.md Token-Disziplin entschlacken — Details nach `operating_model.md` verlagern.<br><span style="color:#1e3a8a">**Prozess/Doku**</span> | CLAUDE.md-Änderung | ~5k<br>—<br>freigabepflichtig | Stakeholder→<br>Executor |
| [B-062](backlog_details.md#b-062--audit-plaene-bereinigen)     | ToDo | <a id="b-062"></a>Audit-Pläne bereinigen (`docs/audit/plans/` + README-Queue), Tier Sonnet.<br><span style="color:#1e3a8a">**Prozess/Doku**</span> | — | ~35k | Executor |
| [B-063](backlog_details.md#b-063--boarding-actions-stratagems-laden)     | Blocked | <a id="b-063"></a>Boarding-Actions-Stratagems laden (NANOSCARAB VIRUS + MINDSHACKLE SCARABS).<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span><br>Blocker: B-003 | → ziel7 Stufe C, hängt an B-003 | ~15k | Executor |
| [B-064](backlog_details.md#b-064--variable-cp-kosten-in-der-ui-anzeigen)     | ToDo | <a id="b-064"></a>Variable CP-Kosten in der UI anzeigen (5 Necron-Stratagems).<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | UI-Design für Stratagem-Karte nötig | ~15k | Design-Crew→<br>Executor |
| [B-065](backlog_details.md#b-065--improve-session-vorbereiten)     | ToDo | <a id="b-065"></a>`/improve`-Session vorbereiten — bereinigte Plan-Queue + grüne Vollsuite als Baseline.<br><span style="color:#1e3a8a">**Prozess/Doku**</span> | B-062 zuerst | ~15k<br>(Vorbereitung) | Stakeholder→<br>Executor |
| [B-066](backlog_details.md#b-066--transport-insassen-feature-embark-disembark)     | ToDo | <a id="b-066"></a>Transport-Insassen-Feature (Embark/Disembark) (Vermerk: NIEDRIG) — 4 Bausteine, 2 offene Design-Fragen.<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | Voraussetzung für Emergency-Disembarkation-Anzeige | ~15–35k | Planner→Executor |
| [B-067](backlog_details.md#b-067--roster-builder-anforderung-before-battle-stratagems)     | ToDo | <a id="b-067"></a>Roster-Builder-Anforderung — `before_battle`-Stratagems müssen dort auswählbar sein.<br><span style="color:#1e3a8a">**Prozess/Doku**</span> | beim Bau des Roster-Builders berücksichtigen | —<br>(kein<br>Umsetzungsaufwand,<br>Anforderung für<br>später) | Planner |
| [B-068](backlog_details.md#b-068--ux-nit-silent-king-zusatzattacken-default)     | ToDo | <a id="b-068"></a>UX-Nit — Silent-King-Zusatzattacken-Default auf Maximum vorbelegen.<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | — | ~5–15k | Executor |
| [B-069](backlog_details.md#b-069--camelcase-umbenennung)     | ToDo | <a id="b-069"></a>camelCase-Umbenennung — 4 Teil-Briefs laut Mapping-Tabelle in `loader_contract.md` §8.<br><span style="color:#c2410c">**Schuldabbau**</span> | Reihenfolge: Stratagem-Kollision → Rest-Felder → Necron → Ork | 4 Teil-Briefs<br>≤~35k je Teil | Executor |
| [B-070](backlog_details.md#b-070--reanimation-konsistenz-umsetzung)     | ToDo | <a id="b-070"></a>Reanimation-Konsistenz — Stratagem-Variante wie Ability-Variante zählen (Entscheid gefallen).<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | Entscheid bereits gefallen (S148) | ~35–70k<br>(Modell-Auswahl-UI<br>nötig) | Executor |
| [B-071](backlog_details.md#b-071--auto-wound-prueft-keine-gauss-tesla-bedingung)     | ToDo | <a id="b-071"></a>`auto_wound` prüft keine Gauss-/Tesla-Waffenbedingung — tiefere Lücke als der S149-Bedingungsfix.<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | Bedingungs-Lücke bereits gefixt | ~15k | Executor |
| [B-072](backlog_details.md#b-072--roster-daten-konsistenz-recherche)     | ToDo | <a id="b-072"></a>Roster-/Daten-Konsistenz-Recherche — CORE-Keyword Annihilation Barge/Flayed Ones, Ork Boss Nob Waffen.<br><span style="color:#c2410c">**Schuldabbau**</span> | reiner Datenabgleich | ~5k | Executor (Haiku) |
| [B-073](backlog_details.md#b-073--model-groups-union-ungenauigkeit)     | ToDo | <a id="b-073"></a>`model_groups`-Union-Ungenauigkeit — `grantsKeyword` zu breit bei gemischter Bewaffnung.<br><span style="color:#c2410c">**Schuldabbau**</span> | keine Regression, bei nächster `model_groups`-Arbeit mitprüfen | ~15k | Executor |
| [B-075](backlog_details.md#b-075--mypy-rest-gamemechanic)     | ToDo | <a id="b-075"></a>mypy-Rest `gameMechanic/` außerhalb des `state`-Contracts (7 Fehler).<br><span style="color:#c2410c">**Schuldabbau**</span> | eigenständig von B-004 | ~15k | Executor |
| [B-076](backlog_details.md#b-076--layer-kopplung-gamemechanic-importiert-uilayout)     | ToDo | <a id="b-076"></a>Layer-Kopplung — `gameMechanic/*Phase.py` importiert `uiLayout._common`; bewusst noch nicht erzwungen.<br><span style="color:#c2410c">**Schuldabbau**</span> | Aufräum-Pfad: Phasen-Render nach `uiLayout/` | ~70k+ | Planner |
| [B-077](backlog_details.md#b-077--common-py-refactoren)     | ToDo | <a id="b-077"></a>`_common.py` refactoren (2218 Zeilen) — Attackensequenz als eigene Datei.<br><span style="color:#c2410c">**Schuldabbau**</span> | gleicher Render-Hub wie B-076 | ~70k+<br>— vor Vergabe<br>splitten | Planner→Executor |
| [B-078](backlog_details.md#b-078--test-mock-fragilitaet-und-conftest-mock-hack)     | ToDo | <a id="b-078"></a>Test-Mock-Fragilität + conftest-Mock-Hack — geteilte `streamlit`-Fixture statt Modul-Mocks.<br><span style="color:#c2410c">**Schuldabbau**</span> | S110-Retro M1+M2, gemeinsame Lösung | ~35k | Executor |
| [B-079](backlog_details.md#b-079--dry-plus-minus-eins-cap-helper)     | ToDo | <a id="b-079"></a>DRY ±1-Cap-Helper (`diceHtml.py` Hit-/Wound-Block).<br><span style="color:#c2410c">**Schuldabbau**</span> | S110-Retro M1 | ~5k | Executor |
| [B-080](backlog_details.md#b-080--dry-zwei-sechs-cap-quelle)     | ToDo | <a id="b-080"></a>DRY [2,6]-Cap-Quelle (`combat.py` vs. `diceHtml.py`) — Sync-Risiko, kein akuter Bug.<br><span style="color:#c2410c">**Schuldabbau**</span> | S144-Review Befund 2 | ~15k | Executor |
| [B-081](backlog_details.md#b-081--dry-directive-aktiv-logik)     | ToDo | <a id="b-081"></a>DRY Directive-Aktiv-Logik (`gameState.py` vs. `abilityEngine.py`) — braucht drittes Modul.<br><span style="color:#c2410c">**Schuldabbau**</span> | S143-Refactor-Befund Punkt 4 | ~15k | Executor |
| [B-083](backlog_details.md#b-083--architecture-md-doku-session)     | Blocked | <a id="b-083"></a>`architecture.md` Doku-Session — 4 Drift-Befunde + `auto_round_1`-Altlast bereinigen.<br><span style="color:#1e3a8a">**Prozess/Doku**</span><br>Blocker: Stakeholder-Freigabe | freigabepflichtig | ~15k | Stakeholder→<br>Executor |
| [B-084](backlog_details.md#b-084--mortal-wounds-text-match-erkennung)     | ToDo | <a id="b-084"></a>Mortal-Wounds-Text-Match-Erkennung — strukturiertes YAML-Feld statt Text-Match.<br><span style="color:#c2410c">**Schuldabbau**</span> | kein akuter Block | ~15k | Executor |
| [B-085](backlog_details.md#b-085--faction-abilities-md-kategorie-6-veraltet)     | Blocked | <a id="b-085"></a>`faction_abilities.md` Kategorie 6 veraltet — Spec-Nachzug nach K2+ (B-003).<br><span style="color:#1e3a8a">**Prozess/Doku**</span><br>Blocker: B-003 | nach B-003 | ~5k | Executor |
| [B-086](backlog_details.md#b-086--test-schuld-klein-tautologie-tests)     | ToDo | <a id="b-086"></a>§4d Test-Schuld — 2 Tautologie-Tests schärfen + Mock-Konsolidierung (11 Testdateien).<br><span style="color:#c2410c">**Schuldabbau**</span> | kein Blocker, verwandt B-078 | ~15k | Executor |
| [B-087](backlog_details.md#b-087--f4-stufe-a-verifikationspunkte-3-und-4)     | ToDo | <a id="b-087"></a>F4 — Stufe-A-Verifikationspunkte 3+4 (Fire Overwatch/Counter-Offensive) — Plan-015-Blocker entfällt (jetzt prüfbar), S152-Prüfung fand Regelkonformitäts-Zweifel (Trigger-Reihenfolge) + UI-Inkonsistenz (verwandt B-031) — Nacharbeit + Neuvorlage S153.<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | Regelprüfung Trigger-Timing + Refinement mit B-031 | ~15k | Executor |
| [B-088](backlog_details.md#b-088--richtungsentscheid-ziel9-fetcher-vorziehen)     | Blocked | <a id="b-088"></a>Richtungsentscheid ziel9-Fetcher vorziehen? — Stakeholder-Entscheidung steht aus.<br><span style="color:#1e3a8a">**Prozess/Doku**</span><br>Blocker: Stakeholder-Entscheidung | Audit S124, verschoben S129 | —<br>(Entscheidung,<br>kein<br>Umsetzungsaufwand) | Stakeholder |
| [B-089](backlog_details.md#b-089--ziel-8-crusade-erweiterung)     | ToDo | <a id="b-089"></a>Ziel 8 — Crusade-Erweiterung (geplant, noch nicht begonnen).<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | — | ~70k+<br>— bei Aufnahme<br>splitten | Planner |
| [B-090](backlog_details.md#b-090--ziel-9-wahapedia-faction-fetcher)     | ToDo | <a id="b-090"></a>Ziel 9 — Wahapedia Faction Fetcher (geplant, noch nicht begonnen).<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | Richtungsentscheid B-088 offen | ~70k+<br>— bei Aufnahme<br>splitten | Planner |
| [B-091](backlog_details.md#b-091--design-block-ui-theme)     | ToDo | <a id="b-091"></a>Design-Block — UI-Theme (Farbpalette, Badge-Optik, Einheitenkarten-Layout).<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | 3 Teilpunkte, bündeln oder einzeln vergeben | ~35k | Design-Crew |
| [B-100](backlog_details.md#b-100--unitcard-go-rand-design-fuer-spieler-2-spiegeln)     | ToDo | <a id="b-100"></a>unitCard-Rand-Design (heller Streifen links) für Spieler 2 spiegeln (rechts statt links) + Prinzip auf GO-Karten übertragen (weniger grell).<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | Konzept vor Umsetzung nötig (zwei Ziele: unitCard + GO-Karte) | ~35k | Design-Crew→<br>Executor |
| [B-101](backlog_details.md#b-101--tesla-waffen-badge-wortlaut-und-design-fix)     | ToDo | <a id="b-101"></a>Tesla-Waffen-Badge — zeigt „Extra Hits" (10E-Terminologie) statt „TESLA" und hält sich nicht ans Design-System (Soll: wie Vengeful-Stars-Buff-Badge).<br><span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> | Regel-Wortlaut vorher gegen Wahapedia verifizieren | ~15k | Executor |

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
- `Blocked`-Zeilen nennen den Blocker zusätzlich inline in der Beschreibungsspalte (dritte
  `<br>`-Zeile, `Blocker: <ID/Kurzbezeichnung>`).

**Typ (Beschreibungsspalte, gefärbt+fett, S152-Auflage 2+Stakeholder-Farbwahl):**

- <span style="color:#166534">**Fachlichkeit (Ziel 7)**</span> — Schema-Grün (`docs/spec/design_colors.md`).
- <span style="color:#c2410c">**Schuldabbau**</span> — dunkles Orange; Stakeholder-Wahl S152,
  außerhalb des Farbschemas, abgeleitet von IN-MELEE `#e07050`.
- <span style="color:#1e3a8a">**Prozess/Doku**</span> — Schema-Blau (`docs/spec/design_colors.md`).

**Effort (Token-Schätzung statt Zeit-Kategorie, S152-Auflage 4):** ersetzt die frühere Zeit-Einteilung `XS/S/M/L`; Konvention deckt sich bewusst mit den Buckets in
`docs/reference/agent_scopes.md` (`XS`<5k · `S` 5–15k · `M` 15–40k · `L`>40k), damit keine zweite,
abweichende Konvention entsteht — Repräsentativwerte hier: **~5k** (ex-`XS`) · **~15k** (ex-`S`) ·
**~35k** (ex-`M`) · **~70k+** (ex-`L`, wird laut S130-Auflage vor Vergabe in ≤M-Teil-Briefs gesplittet).
**Ist-Verbrauch** je Aufgabe/Session: `tools/token_report.py` schreibt ihn nach jedem Testlauf in
`docs/metrics/overview.md` (Peak-Kontext, Subagent-Anteil, Verlauf) — dort ablesen, kein manuelles
Nachrechnen, kein neues Tool.

**Assignee-Rollen:** `Stakeholder` (Entscheidung/manuelle UI-Prüfung) · `Planner` (Konzept/Split
vor Vergabe) · `Executor` (Umsetzung, Default-Tier Sonnet; reine Lookups per Auftrag explizit auf
Haiku) · `Design-Crew` (UI/UX-Konzept vor Umsetzung). Pfeile (`A→B`) zeigen die Reihenfolge.

**Abhängigkeiten-Notation:** Freitext, der auf blockierende IDs, Dateien oder externe
Entscheidungen verweist — für die volle Begründung immer den Link in der ID-Spalte öffnen
(`backlog_details.md`, Feld „Abhängigkeiten").

**Neues Item aufnehmen:** nächste freie `B-NNN`-ID vergeben, Zeile hier einfügen (Position =
Stakeholder-Priorität), vollen Kontext in `backlog_details.md` unter `## B-NNN — Titel` anlegen
(Feldschema dort dokumentiert).

**Bereinigen:** Item erledigt/verworfen → Detail-Abschnitt aus `backlog_details.md` **inklusive**
Fakten/Links/Commits nach `backlog_archive.md` verschieben (Format der bestehenden Einträge
folgen), Zeile hier löschen. Nie nur die Zeile löschen ohne den Detail-Abschnitt nachzuziehen —
sonst geht die Begründung verloren.
