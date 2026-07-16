STATUS: ANSWERED

# S151 — Backlog-Inventar (vollständig, read-only)

Quellen: `docs/goals/backlog.md` (793 Zeilen), `docs/goals/index.md` (62 Zeilen).
Zweck: lückenlose Grundlage für die freigegebene Backlog-Restrukturierung (Rang 11,
Stakeholder-Auftrag S150). Keine Datei außer dieser wurde verändert.

---

## Zählblock

| Kategorie | Anzahl |
|---|---|
| Erfasste Einträge insgesamt | 143 |
| davon OFFEN (ID vergeben, B-001…B-091) | 91 |
| davon ERLEDIGT/VERWORFEN → Archiv-Kandidat | 46 |
| davon UNKLAR | 6 |

**Plausibilisierung (Glyphen-Rohzählung in `backlog.md`, `grep -o`):**

| Glyph | Vorkommen | Erklärung der Differenz zu „Anzahl Items" |
|---|---|---|
| 🔲 | 53 | 52 reale Items + 1 Meta-Zitat (Z.109 zitiert nur das Label „🔲 SAVE-Hinweis" aus der Tabellenzeile Z.90, kein eigener Eintrag) |
| 🟡 | 8 | 8 Items, 1:1 |
| 🟢 | 20 | 20 Items, 1:1 |
| ✅ | 40 | verteilt auf ~24 Zeilen — die Protokoll-Tabelle (Z.89–100) trägt bis zu 3 ✅ pro Zeile (Engine-Spalte + Anzeige-Spalte, teils 2×); die Prioritätenliste nutzt ✅ zusätzlich als „parallelisierbar mit Rang X"-Marker (Z.39/40/42/44/47, NICHT „erledigt" — Erledigt-Status dort über `~~Strikethrough~~` + Text) |
| 🔴 | 1 | 1 Item (Command-Protocol-Direktiven, S95) — Status unklar, s. Tabelle 3 |
| `- [x]` | 10 | 10 abgeschlossene UI-Verifikationspunkte (§3) |
| `- [ ]` | 1 | 1 offener UI-Verifikationspunkt (§3, Ziel7 Stufe C) |

Dazu kommen glyphenlose Einträge, die ein reiner Glyphen-Scan übersieht (Anlass des
Auftrags — bekannter Fall §4c):
- §4c „Design-System" (ganzer Abschnitt, S116–S118, keine ✅-Glyphen) — 1 Archiv-Kandidat.
- §2-Beobachtungen ohne Glyph: B2, B4-Rest, B7, B9, B10 (5 Items).
- §4 „Layer-Kopplung" + „Test-Mock-Fragilität" (2 Items ohne Glyph).
- §4b: 4 Doku-Drift-Befunde ohne Glyph (session_state-Schema, Colour System, uiLayout
  „No game logic", Refactoring-Plan/Open-Design-Questions) + `auto_round_1`-Altlast,
  zusammengeführt zu 1 Sammel-Item (teilen dieselbe Abschluss-Empfehlung: „architecture.md-
  Doku-Session, vor Änderung freigeben"); „Mortal Wounds Text-Match" separat, ebenfalls ohne Glyph.
- §4d „Test-Schuld (klein)" (Abschnittsüberschrift ohne Glyph, bündelt 2 Unterpunkte).
- §5: `ziel8.md`/`ziel9.md`-Pointer ohne Glyph, dedupliziert mit `index.md`-Tabellenzeilen.
- `index.md`: „Design-Block — UI-Theme" (3 Checkboxen `- [ ]`, kein Emoji-Glyph).

Summenkontrolle: 52+8+20+1(🔴, siehe Tabelle 3)+10+1 = 92 glyphenbasierte Items (roh, vor
Merges) + ~16 glyphenlose Items = 108 rohe Fundstellen. Nach Zusammenführen von Duplikaten
(gleiches Thema in Prioritätenliste **und** §-Abschnitt, z. B. Rang 10 = §0 #2b; ∥ = §4
abilityEngine-Vorplanung; Sudden-Storm-S-Zeile Z.96 = Auflösungsnotiz Z.419) auf **143**
Gesamt-Items verdichtet (91 offen + 46 erledigt + 6 unklar).

---

## Selbstprüfung

- **(a) Glyphen-Grep vs. erfasste Items:** oben dokumentiert — jede der 53/8/20/1-Zeilen
  wurde einzeln gegen die Tabellen unten abgeglichen (keine Zeile ohne Zuordnung).
- **(b) Alle 11 Ränge der Prioritätenliste:** Rang 1–11 + Zusatzzeile „∥" = 12 Zeilen
  geprüft. Erledigt (Strikethrough+Text): Rang 1, 2, 3, 4, 8. Offen: Rang 5, 6, 7, 9, 10,
  11, ∥ → B-001…B-007.
- **(c) Abschnitt 4c erfasst:** ja, als Archiv-Kandidat A-023 (kein ✅-Glyph, genau der im
  Auftrag genannte Anlassfall).
- **(d) `index.md`-Punkte erfasst:** ja — Design-Block/UI-Theme → B-091; Ziel 8/Ziel 9
  → B-089/B-090 (dedupliziert mit `backlog.md` §5-Pointern, beide Quellen zitiert).
- **(e) `git status`:** geprüft, zeigt außer dieser neuen Handoff-Datei keine Änderung
  (siehe Kommando-Output unten).

```
git status --porcelain
docs/handoff/S151_backlog_inventar.md  (neu, untracked)
```

---

## Tabelle 1 — Offene Items (B-001…B-091)

Reihenfolge: zuerst offene Ränge der Prioritätenliste (Stakeholder-Prio, unverändert),
danach übrige offene Items in Dokument-Reihenfolge, zuletzt `index.md`.

| ID | Titel | Status | Effort | Abhängigkeiten | Assignee | Quelle |
|---|---|---|---|---|---|---|
| B-001 | FixD Brief 2 + 3 (Compute/Render-Folge) | Blocked (Brief 2 hinter Mockup-Gate) | M | nach Rang 4 (erledigt); Brief 3 = Spec-Nachzug | Executor | Prio-Rang 5, Z.41 |
| B-002 | Klan/Dynastie Brief K1 — Wortlaut-Bugfix Nihilakh + Mephrit | ToDo | S | Entscheid kanonisiert S150 (`ziel7.md` §K1); `subfaction_abilities.yaml` unverändert | Executor | Prio-Rang 6, Z.42 |
| B-003 | Klan/Dynastie K2+ — Novokh/Sautekh/Nephrekh + Ork Snakebites, Engine-Filter, `subfaction_passive`-Migration, 4 neue Effekttypen, Badge, Spec-Nachzug `faction_abilities.md` Kat.6 | ToDo | L — **vor Vergabe in ≤M-Briefs splitten** | macht 13 Einträge erstmals wirksam; Details `ziel7.md` Stufe C §K1 | Planner→Executor | Prio-Rang 7, Z.43 |
| B-004 | mypy-Ratchet `uiLayout/` (17 Fehler: `armyCard.py`/`gameProtocoll.py`/`unitCard.py`/`armyList.py`/`detachmentCard.py`) | Blocked (⛔ erst nach Rang 5/B-001) | M | Dateiüberschneidung `_common.py` mit FixD | Executor | Prio-Rang 9, Z.45; §4 Z.580 |
| B-005 | #2b Direktiv-Lock-Rest — Direktive ab Bewegungsphase sperren | ToDo | S | Setup-Leck bereits gefixt (2026-06-20); reiner Rest | Executor | Prio-Rang 10, Z.46; §0 Z.72–80 |
| B-006 | abilityEngine-Refactor-Vorplanung (Planungspaket, kein Code) | Blocked (Schwellwert-gegated: erst ab ~800 Zeilen `abilityEngine.py` ODER DRY-Schuld-Angang) | S (~15–20k Token) | orthogonal zu Klan/Dynastie (K2 nutzt bereits eigenes Modul `subfactionPassives.py`) | Planner | Prio-Rang ∥, Z.47; §4 Z.593–613 |
| B-007 | **Backlog-Restrukturierung** — schlanke Kopf-Liste + Auslagerung Detailtexte (dieser Auftrag selbst, Teil 1 von 2) | In Progress (S151 = Inventar-Schritt) | M | Kein Eintrag darf verloren gehen; Abschnitt 4c mit archivieren | Planner→Stakeholder-Freigabe→Executor | Prio-Rang 11, Z.48 |
| B-008 | on_target-Anker Option A — Stakeholder-UI-Prüfung ausstehend | UI-Verifikation | XS | Code seit S146 erledigt (Rang 2), nur Prüfung offen | Stakeholder | Prio-Rang 2, Z.38 |
| B-009 | #PSI Flow/Reset — 4 manuelle UI-Checks (Undo-Deny, aktiv-Reset, Skip-Deny-Budget, Undo nach Fail-Deny) | UI-Verifikation | S | Code+Tests grün seit S65; gemeinsamer Commit mit Token-Gauge-Hook geplant | Stakeholder | §0, Z.60–71 |
| B-010 | #2 Protokoll-Buff-Audit — Anzeige-Rest (Eternal Guardian S SAVE-Hinweis; Sudden Storm P Bewegungs-Badge) | Blocked (Eternal Guardian S hängt an Plan 015 Overwatch) | S | Engine-Seite komplett verdrahtet (Plan 024); Sudden Storm S-Teil bereits durch generischen Block abgedeckt (s. Archiv A-020) | Executor | §0, Z.81–122 |
| B-011 | #3/#4 Würfelanzeige — Pfeilrichtung/-länge + Badge-Breite | ToDo | S | Soll-Bild in `docs/spec/dice_display.md` fixieren → Plan 022 | Executor | §0, Z.123–128 |
| B-012 | #INV-4b Cluster 1 — `dakka`/`klaw`/`tesla` YAML-Schema (`weapon_special`) | ToDo | S | Cluster 3–6 bereits erledigt (Archiv A-006–A-009) | Executor | §0, Z.129–133 |
| B-013 | GO-UI Paket 3b — `before_battle`-Liste im ArmySetup (13 GOs erstmals sichtbar) | ToDo | M | Teil der GO-UI-Design-System-Roadmap (Entscheid S131) | Executor | §2, Z.160–162 |
| B-014 | GO-UI Folge-Pakete für 10 Rest-GOs — generisches `on_destroy` (7 GOs) + `on_set_up`+`on_target` | ToDo | M — **Paket-Nummern bei Einplanung NEU vergeben** (Kollision mit bestehenden Paket 5/6) | nach Paket 4 (erledigt); Vorschlag bereits in `design_system.md` §6.2 skizziert (dort „Paket 5/6" ≠ Backlog-Paket 5/6) | Planner→Executor | §2, Z.171–173; `design_system.md` §6.2 Z.320–321 |
| B-015 | GO-UI Paket 5 — Wortlaut-/Sprach-Bereinigung (Englisch durchgehend, Use/Undo/Confirm), eine CP-Anzeige, ein Stepper-Baustein | ToDo | M | Teil der Roadmap | Executor | §2, Z.174–175 |
| B-016 | GO-UI Paket 6 — Einheiten-Auswahl in GameActionArea ziehen, Zielauswahl entschlacken | ToDo | M | eigenes Konzept-Inkrement | Design-Crew→Executor | §2, Z.176–178 |
| B-017 | GO-UI „Danach" — manuelle UI-Gesamt-Verifikation (S130-Checkliste + neues Design) | Blocked (erst nach Abschluss aller Pakete) | S | s. o. Pakete | Stakeholder | §2, Z.179 |
| B-018 | Fraktions-Stratagems `before_battle` sichtbar machen (6 Necron + 7 Ork) | Blocked (löst über B-013/Paket 3b) | S | danach §6e-Modifier-Engine für ~56 teilintegrierte proaktive Stratagems | Executor | §2, Z.180–183 |
| B-019 | „Alt. Fire"-Chip unerklärt (`diceHtml.py:70`) | ToDo | XS | Regel-Wortlaut gegen `docs/work/` verifizieren (Haiku), dann Kurzerklärung ergänzen | Executor | §2, Z.184–187 |
| B-020 | B2 — Spielvorbereitungsscreen überarbeiten (Konzept) | ToDo | M | Struktur = Option C entschieden (S135); Redundanz-Befunde B5/B7 einarbeiten | Design-Crew | §2, Z.194–209 |
| B-021 | B4-Rest — profileCard als Datenkarte (Setup) | ToDo | M | App-Design-System + Wahapedia-IA entschieden (S135); nur Setup-Screen | Design-Crew→Executor | §2, Z.200–209 |
| B-022 | B7 — Redundanter Kopfbereich + schwache Hinweise | Blocked (Selbst-Stopp S149: >4 Dateien Scope) | M — **vor Vergabe splitten** (Vorschlag B7a Faktions-Zeile+Mini-Header / B7b Hinweis-Baustein) | betrifft `_common.py`, `psychicPhase.py`, `fightPhase.py`, `commandPhase.py`, `PHASE_RULES` | Planner→Executor | §2, Z.213–232 |
| B-023 | B9 — Subphasen-Schritte unsichtbar (Stepper-Baustein) | ToDo | M | Zwischenlösung C entschieden; läuft als 1 Konzept-Handoff mit B7 (B-022) | Design-Crew→Executor | §2, Z.235–242 |
| B-024 | B10 — Kommentar-Hygiene Ratchet-Praxis | In Progress (laufende Praxis, kein Enddatum) | — (laufend) | Konvention in CLAUDE.md bereits verankert (Teil a erledigt) | Executor (bei jeder Modul-Berührung) | §2, Z.243–249 |
| B-025 | B11 — Rest-Wahrnehmung nach B1-Fix (kurzer Sprung/Zucken beim Slot-Wechsel) | ToDo (Beobachtung) | XS | B1 selbst gefixt; optionaler 2. Schritt aus `S136_B1_probe.md` | Executor | §2, Z.250–253 |
| B-026 | B12 — GO-„used"-Zustand Gesamtkonzept (Rest über B12b hinaus: Once-per-Phase-Erzwingung phasenübergreifend) | ToDo | M — Teil-Briefs ≤M | B12b (Header-Suffix) bereits erledigt (Archiv A-018); Konzept in `docs/handoff/S137_B12_konzept.md` | Executor | §2, Z.254–259 |
| B-027 | B12 optionaler XS-Task — `unit_key`/uid durch `spend_stratagem` durchreichen (Advance-Reroll/Fire-Overwatch-Randfall) | ToDo (optional, „falls je gewünscht") | XS | spec-konformer Randfall, kein Bug | Executor | §2, Z.267–269 |
| B-028 | B12 Feature-Wunsch — „used on ⟨Einheit⟩"-Suffix auf ALLE reaktiven GOs ausweiten | ToDo | M | nach BUG-Fix (erledigt, Archiv A-019) | Executor | §2, Z.284–286 |
| B-029 | B13 — GO-Karte: Keyword-Badges | ToDo (Stakeholder: „ins Backlog", keine Eil-Prio) | M | Schema-Erweiterung (`keywords:` fehlt in allen 3 Stratagem-YAMLs + Dataclass) **plus** Datenpflege in einem Aufwasch | Executor | §2, Z.287–295 |
| B-030 | B14 — Badge-Kontrast-Pass (STATIONARY-Khaki zu dunkel) | Blocked (Hex-Vorschläge → Stakeholder-Entscheid zuerst) | XS | danach mechanischer Edit `design_colors.md`+`unitCard.py` | Stakeholder→Executor | §2, Z.296–300 |
| B-031 | GO-Konsistenz — nicht erfüllte Bedingungen ausgrauen statt ausblenden (alle GOs) | ToDo | M | passt kollisionsfrei zum bestehenden State-Modell (Review-Befund `S149_review.md`) | Executor | §2, Z.304–310 |
| B-032 | Psychic-Ledger schrumpfen — Smite-Manifest-Logik aus Render-Code extrahieren | ToDo | M | Ledger 15→10 | Executor | §2, Z.311–314 |
| B-033 | Psychic-Lücken R-PSYCHIC-23/24 (Perils zerstört Psyker / Perils-Splash D3) | ToDo | M | beide brauchen Unit-Destroyed-Check nach Perils-Schaden | Executor | §2, Z.315–317 |
| B-034 | SAVE-Block: Fähigkeit + AP als eine Badge (`Enslaved AP-1`) | ToDo | S | → Plan 017 | Executor | §2, Z.320 |
| B-035 | Gretchin Cowardly — −1 Attrition ohne RUNTHERD in 6" | ToDo | S | → Plan 018 | Executor | §2, Z.321 |
| B-036 | Battle-Log — nach Reset keine alten Einträge | ToDo | XS | → Plan 018 | Executor | §2, Z.322 |
| B-037 | `collect_modifiers_for_phase()` | ToDo | M | → Plan 018 Task 18.4; laut §5 zusätzlich Teil von `ziel7.md` §6e | Executor | §2, Z.323; §5 Z.730 |
| B-038 | Totalvernichtungs-Spielende (R-ROUND-07 „army destroyed") | ToDo | M | eigener kleiner Plan | Executor | §2, Z.324–327 |
| B-039 | Tote Produktionsfunktion `build_aura_range_hint_text` entfernen | ToDo | XS | mit Tests gemeinsam entfernen, `acceptance/rules.md` nachziehen | Executor | §2, Z.328–333 |
| B-040 | Fold-Heuristik nur Hauptfraktion + Subfaction-Wiring Roster→Unit | Blocked (wartet auf echte Subfraktions-Keywords, s. B-002/B-003) | S | in einem Aufwasch mit Klan/Dynastie-Arbeit prüfen | Executor | §2, Z.334–340 |
| B-041 | Operating-Model Phase C — Refinement automatisieren (Sonnet liest `Fotos/` → `docs/inbox/`) | ToDo | M | — | Executor | §2, Z.341–342 |
| B-042 | Gates/Reports leser-orientiert prüfen (→ ADR-0002) | ToDo | S | Debt-Scoreboard, Rule-Catalog-Prozente | Executor | §2, Z.343–345 |
| B-043 | Invuln-SAVE-Badge-Bereich chaotisch (3 Teile → 1 Badge) | ToDo | S | überschneidet Plan 017 | Executor | §2, Z.346 |
| B-044 | Dice-Display Modifier-Geometrie (Befund B/C: Debuff-Spreizung, Slot-1-Invariante) | ToDo | M | eigener Plan, `modifier_die_pair_html` | Executor | §2, Z.347 |
| B-045 | Silent-King-Zielaufteilung Fernkampf (2 Fernkampfwaffen → nur 1 Ziel wählbar, regelwidrig) | ToDo | M | Regel bereits geklärt (S80); Detail `docs/inbox/finding-silent-king-target-split.md` | Executor | §2, Z.348 |
| B-046 | Off-Scale-/„7+"-Save-Grenze (7-Augen-Würfel + Erfolgsgrenze) | ToDo | S | `docs/spec/dice_display.md` ergänzen; verwandt B-044 | Executor | §2, Z.349 |
| B-047 | AP-/SAVE-Modifier-Magnitude-Position | ToDo | S | eng verwandt B-044 | Executor | §2, Z.350 |
| B-048 | Lethal Hits (R-CMB-XX) | ToDo | M | Eigener Plan nach Plan 014 | Executor | §2, Z.351 |
| B-049 | Deadly Demise (R-CMB-YY) | ToDo | M | YAML-Daten vorhanden, Handler fehlt | Executor | §2, Z.352 |
| B-050 | Voice of the Triarch (R-CMD-XX, Silent King) | ToDo | S | YAML-Basis fertig (`alter_command_protocol`); → Plan 016 oder eigener Plan | Executor | §2, Z.353 |
| B-051 | Failsafe/Arkana-Aktivator-UI fehlt (Necrons/Custodes `round_choice`-Fraktionen) | ToDo | M | generischer Aktivator für `activated`-`faction_abilities` + CANOPTEK-Target-Picker | Executor | §2, Z.354–365 |
| B-052 | `condition_prompt`/`applies_when` als First-Class-Felder | ToDo | S | Plan 018 Task 18.3; erst wenn 2. Konsument auftaucht | Executor | §2, Z.366–370 |
| B-053 | Daten-Altlast `gretchin_mob` (8E-Formulierung Morale Test) | ToDo | XS | gegen `docs/work/wahapedia_orks/` prüfen | Executor (Haiku-Lookup) | §2, Z.371–375 |
| B-054 | Custodes Rendax Ka'tah Secondary — toter `strength_modifier`-Pfad → `strength_if_charged` | ToDo | S | Engine-Fn existiert bereits, nur Konsum+Test; analog Hungry Void D2 | Executor | §2, Z.376–382 |
| B-055 | Army-List-UX „weniger Scrollen" (auto-Ende, Fokus, Umsortieren) | ToDo | M — Streamlit-Machbarkeit zuerst klären | eigener Plan | Executor | §2, Z.384–389 |
| B-056 | Quantum Shielding — fester Invuln-Wert 4+ (kein additiver Modifier) + S148-Anzeige-Bug (Wound 1–3 kein Debuff/Buff sichtbar) | ToDo | M | Regel gegen `docs/work/wahapedia_necrons/` prüfen; überschneidet Plan 017 | Executor | §2, Z.390–398 |
| B-057 | Waffen-Block: Rapid-Fire-Count + Range anzeigen | ToDo | S | eigener Plan | Executor | §2, Z.399–403 |
| B-058 | Dynastie-Code je Einheit statt Roster-Ebene (Mixed-Dynasty) | ToDo | M — eigenes Konzept zuerst | betrifft `subfaction_value_for`-Konsumenten; verwandt B-002/B-003 | Planner→Executor | §2, Z.404–408 |
| B-059 | Regel-Index für Wahapedia-Texte (`docs/work/rule_index.md`) | ToDo | S | beschleunigt Haiku-Lookups | Executor | §2, Z.409–412 |
| B-060 | CLAUDE.md Token-Disziplin entschlacken (nach `operating_model.md` verlagern) | ToDo | XS — freigabepflichtig | CLAUDE.md-Änderung | Stakeholder→Executor | §2, Z.413–416 |
| B-061 | Backlog-§0-Hygiene (Überschrift datieren, ✅-Einträge auslagern) | ToDo | XS | **überlappt inhaltlich mit B-007 (Rang 11) — bei Umsetzung zusammenlegen** | Executor | §2, Z.417–418 |
| B-062 | Audit-Pläne bereinigen (`docs/audit/plans/` + README-Queue) | ToDo | M | Tier: Sonnet | Executor | §2, Z.426–430 |
| B-063 | Boarding-Actions-Stratagems laden (NANOSCARAB VIRUS + MINDSHACKLE SCARABS) | Blocked (→ ziel7 Stufe C, hängt an B-003) | S | Bereinigung anderer BA-only-Einträge bereits erledigt (S134) | Executor | §2, Z.431–440 |
| B-064 | Variable CP-Kosten in der UI anzeigen (5 Necron-Stratagems) | ToDo | S | UI-Design für Stratagem-Karte nötig | Design-Crew→Executor | §2, Z.441–444 |
| B-065 | /improve-Session vorbereiten | ToDo | S (Vorbereitung) | bereinigte Plan-Queue (B-062) zuerst, grüne Vollsuite als Baseline | Stakeholder→Executor | §2, Z.445–450 |
| B-066 | Transport-Insassen-Feature (Embark/Disembark) | ToDo (Stakeholder: NIEDRIG-Prio) | S–M | 4 Bausteine, 2 offene Design-Fragen | Planner→Executor | §2, Z.451–462 |
| B-067 | Roster-Builder-Anforderung — `before_battle`-Stratagems auswählbar | ToDo (Anforderung für künftigen Builder, kein akuter Task) | — | beim Bau des Roster-Builders berücksichtigen | Planner | §2, Z.463–466 |
| B-068 | UX-Nit — Silent-King-Zusatzattacken-Default auf Maximum | ToDo | XS/S | — | Executor | §2, Z.467–470 |
| B-069 | camelCase-Umbenennung (Mapping-Tabelle fertig, `loader_contract.md` §8) | ToDo | 4 Teil-Briefs ≤M | Reihenfolge: (1) Stratagem-Kollision, (2) Rest-Stratagem-Felder, (3) Necron-Scope (6 Dateien), (4) Ork-Scope (5 Dateien)+Custodes-Zusatzfund | Executor | §2, Z.482–491 |
| B-070 | Reanimation-Konsistenz — Stratagem-Variante gleich zählen (Umsetzung) | ToDo | M/L (Modell-Auswahl-UI nötig) | Entscheid bereits gefallen (S148) | Executor | §2, Z.492–499 |
| B-071 | auto_wound prüft keine Gauss-/Tesla-Waffenbedingung (tiefere Lücke, nicht in Brief 6/S149 mitgefixt) | ToDo | S | Bedingungs-Lücke (WER darf nutzen) bereits gefixt; dies ist die Waffen-Ist-Prüfung | Executor | §2, Z.500–507 |
| B-072 | Roster-/Daten-Konsistenz-Recherche (CORE-Keyword Annihilation Barge/Flayed Ones, Ork Boss Nob Waffen) | ToDo | XS | Haiku-Task, reiner Datenabgleich | Executor (Haiku) | §2, Z.508–512 |
| B-073 | `model_groups`-Union-Ungenauigkeit (grantsKeyword zu breit bei gemischter Bewaffnung) | ToDo (keine Regression, bei nächster `model_groups`-Arbeit mitprüfen) | S | geerbt von Brief 4 | Executor | §2, Z.513–518 |
| B-074 | Ziel7 Stufe C-Vorbereitung — Emergency Disembarkation am Ork-Transport-Roster real prüfen | UI-Verifikation | XS | war zuvor mangels TRANSPORT-Roster blockiert, jetzt möglich (`orks_transport.yaml`) | Stakeholder | §3, Z.549–553 (Checkbox `- [ ]`) |
| B-075 | mypy-Rest `gameMechanic/` außerhalb `state`-Contract (7 Fehler: `attackMath.py` type-arg, `moralePhase.py`/`unitMutations.py` no-any-return/arg-type) | ToDo | S | eigenständig von B-004 (uiLayout-Teil); Baseline in `tools/mypy_gate.py` je Schritt senken | Executor | §4, Z.568–586 |
| B-076 | Layer-Kopplung: `gameMechanic/*Phase.py` importiert `uiLayout._common` | ToDo (bewusst noch nicht erzwungen) | L | Aufräum-Pfad: Phasen-Render nach `uiLayout/` ziehen (Audit-Plan 008); verwandt B-077/B-088 | Planner | §4, Z.587–589 |
| B-077 | `_common.py` refactoren (2218 Zeilen zerlegen, Attackensequenz eigene Datei) | ToDo | L — vor Vergabe splitten | Stakeholder-Auftrag S132; gleicher Render-Hub wie B-076 | Planner→Executor | §4, Z.590–592 |
| B-078 | Test-Mock-Fragilität + conftest-Mock-Hack — geteilte `streamlit`-Fixture statt Modul-Mocks | ToDo | M | S110-Retro M1+M2, gemeinsame Lösung | Executor | §4, Z.614–621, Z.639–642 |
| B-079 | DRY ±1-Cap-Helper (`diceHtml.py` Hit-/Wound-Block) | ToDo | XS | S110-Retro M1 | Executor | §4, Z.622–624 |
| B-080 | DRY [2,6]-Cap-Quelle (`combat.py` vs. `diceHtml.py`) | ToDo (kein akuter Bug, niedrige Prio) | S | S144-Review Befund 2 | Executor | §4, Z.625–631 |
| B-081 | DRY Directive-Aktiv-Logik (`gameState.py` vs. `abilityEngine.py`) | ToDo (kein akuter Bug, niedrige Prio) | S | S143-Refactor Punkt 4; braucht drittes Modul | Executor | §4, Z.632–638 |
| B-082 | Prozess: Executor-Auftrags-Checkliste härten (`ruff` vor „grün"-Claim, Token-/Zeit-Cap) | ToDo | XS | betrifft `docs/reference/agent_scopes.md`; bei nächster Scope-Pflege einarbeiten | Planner | §4, Z.643–647 |
| B-083 | `architecture.md` Doku-Session (4 Drift-Befunde: session_state-Schema, Colour System, uiLayout „No game logic", Refactoring-Plan/Open-Design-Questions + `auto_round_1`-Altlast) | Blocked (freigabepflichtig) | S | eigene kleine Doku-Session | Stakeholder→Executor | §4b, Z.651–674 |
| B-084 | Mortal Wounds Text-Match-Erkennung (`"mortal wound" in abilities.lower()`) | ToDo (kein akuter Block) | S | strukturiertes YAML-Feld statt Text-Match | Executor | §4b, Z.676 |
| B-085 | `faction_abilities.md` Kategorie 6 „Passive/Persistent" veraltet | Blocked (nach B-003/K2+) | XS | Spec-Nachzug | Executor | §4b, Z.677–682 |
| B-086 | §4d Test-Schuld (klein) — 2 Tautologie-Tests schärfen + Mock-Konsolidierung (11 Testdateien) | ToDo (kein Blocker, opportunistisch) | S | Follow-up S118-M2; verwandt B-078 | Executor | §4d, Z.712–723 |
| B-087 | F4 — Stufe-A-Verifikationspunkte 3+4 (Fire Overwatch/Counter-Offensive UI) | Blocked (braucht Plan 015) | XS (reine Prüfung) | Plan 015 Priorität P2 | Stakeholder | §5, Z.770–774 |
| B-088 | Richtungsentscheid ziel9-Fetcher vorziehen? | Blocked (Stakeholder-Entscheid nötig) | — (Entscheidung) | Audit S124, verschoben S129 | Stakeholder | §5, Z.777–779 |
| B-089 | Ziel 8 — Crusade-Erweiterung (geplant) | ToDo (noch nicht begonnen) | L — bei Aufnahme splitten | — | Planner | §5 Z.775; `index.md` Z.45 |
| B-090 | Ziel 9 — Wahapedia Faction Fetcher (geplant) | ToDo (noch nicht begonnen) | L — bei Aufnahme splitten | Richtungsentscheid B-088 offen | Planner | §5 Z.776; `index.md` Z.45 |
| B-091 | Design-Block — UI-Theme (Farbpalette/Goldtöne, Badge-Optik/Spacing, Einheitenkarten-Layout) | ToDo (eigene Session, noch nicht begonnen) | M | 3 Teilpunkte, bündeln oder einzeln vergeben | Design-Crew | `index.md` Z.46, Z.52–56 |

---

## Tabelle 2 — Archiv-Kandidaten (ERLEDIGT/VERWORFEN)

| # | Titel | Quelle (§/Zeilen) | Erledigt-Vermerk |
|---|---|---|---|
| A-001 | Rang 1 — Klan/Dynastie-Entscheid (Frage 3 + Prioritätenliste) | Prio-Rang 1, Z.37 | kanonisiert S150, `ziel7.md` Stufe C §K1 |
| A-002 | Rang 2 — on_target-Anker Option A | Prio-Rang 2, Z.38 | erledigt S146 (Code); UI-Prüfung separat offen → B-008 |
| A-003 | Rang 3 — Vigilus-Warlord-Traits entfernen | Prio-Rang 3, Z.39 | erledigt S146 |
| A-004 | Rang 4 — FixD Brief 1 (Compute/Render-Trennung) | Prio-Rang 4, Z.40 | erledigt S150 |
| A-005 | Rang 8 — Stufe-B-Rest: Necron-Roster-UI-Verifikation | Prio-Rang 8, Z.44 | erledigt S146, alle 7 Schritte bestanden |
| A-006 | INV-4b Cluster 3 | §0, Z.131–133 | erledigt, Plan 020 |
| A-007 | INV-4b Cluster 4/5 | §0, Z.131–133 | erledigt, XS-Fix |
| A-008 | INV-4b Cluster 6 | §0, Z.131–133 | erledigt, Plan 021/024 |
| A-009 | INV-4 Default-Roster | §0, Z.131 (Verweis) | erledigt S128, Details `backlog_archive.md` |
| A-010 | GO-UI-Design-System — Entscheidung selbst (Wertesatz/Struktur) | §2, Z.146–153 | ENTSCHIEDEN S131 (Roadmap-Pakete separat offen, s. Tabelle 1) |
| A-011 | GO-UI Paket 3a — Reaktive Boxen → GO-Karte migriert | §2, Z.158–159 | erledigt S133 |
| A-012 | GO-UI §6.2 statisches Modell | §2, Z.163–167 | erledigt S134 |
| A-013 | GO-UI Paket 4 — Inline-Anker Hit/Wound/Save + Reroll-Ablösung | §2, Z.168–173 | erledigt S135, Commits `d66755e`/`0aa7dc6`/`96e7997` (Folge-Arbeit → B-014) |
| A-014 | B1 — Scroll-Sprung bei Command-Protocol-Wahl | §2, Z.192–193 | erledigt S136, Details `backlog_archive.md` |
| A-015 | B5 — First-Player-Block Redundanz | §2, Z.210 | erledigt S134, Details `backlog_archive.md` |
| A-016 | B6 — Faction-Ability-Wahl auf Player-Ebene | §2, Z.211–212 | erledigt S135, Details `backlog_archive.md` |
| A-017 | B8 — Redundanter Statusbereich in jeder Phase | §2, Z.233–234 | erledigt S149, Details `backlog_archive.md` |
| A-018 | B12b — Header-Suffix „used on ⟨Einheit⟩" verdrahtet | §2, Z.260–269 | verdrahtet S141 (Commit `cdb55e2f`), UI-Verifikation abgeschlossen S148 |
| A-019 | B12-BUG — Insane-Bravery-Repro Moralphase (live `target_name` statt Anker) | §2, Z.270–283 | erledigt S150, UI-verifiziert |
| A-020 | Sudden Storm S — B-Hinweis anzeigen (`shoot_during_action`) | §2, Z.419–422 | abgedeckt durch generischen Direktiv-Hinweisblock (Plan 025 Step 2b), nicht mehr separat nachzuziehen — **🔲-Glyph an dieser Stelle ist stale, sollte bei Umsetzung entfernt/korrigiert werden** |
| A-021 | Boarding-Actions Bereinigung (Rapid Reanimation, Shield-Piercer Projectors, Flensing Capacitors, `resurrection_protocols_character` aus YAML entfernt) | §2, Z.434–440 | erledigt S134 (Teil-Erledigung von B-063; die eigentliche NANOSCARAB/MINDSHACKLE-Ladung bleibt offen) |
| A-022 | Generic-src (INV-4 DEBT) | §4, Z.561–565 | komplett aufgelöst, Details `backlog_archive.md` + `architecture_invariants.md` INV-4 |
| A-023 | Generic-src Vokabular (INV-4b DEBT) | §4, Z.566–567 | komplett aufgelöst S128 |
| A-024 | §4c Design-System (ganzer Abschnitt) | §4c, Z.702–708 | ERLEDIGT S116–S118, Doku-Abgleich S120 — **kein ✅-Glyph, exakt der im Auftrag genannte Anlassfall** |
| A-025 | Ziel7 P17 — Pre-Apply-Zielauswahl + Wounded-Lock | §5, Z.733–735 | erledigt S115 |
| A-026 | Ziel7 P18 — einheitlicher Deklarations-Flow | §5, Z.736–738 | erledigt bereits S43 (`e6fcdb3`), Checkbox war stale-offen, verifiziert S117 |
| A-027 | Ziel7 P19 — once_per_battle pro Spieler | §5, Z.739–742 | erledigt 2026-07-03, Commit `1f9d82b` |
| A-028 | Ziel7 P20 — Rapid Fire halbe Reichweite | §5, Z.743–746 | erledigt 2026-07-03, Commit `dfebd27` |
| A-029 | Ziel7 P21 — Stratagem-Undo überlebt Phasenwechsel (Bug) | §5, Z.747–751 | erledigt 2026-07-03, Commit `dde16f3` |
| A-030 | Ziel7 Stufe A Task 1 — Stratagem-Doppelanzeige | §5, Z.754–756 | erledigt, Commit `8c124c3` |
| A-031 | Ziel7 Stufe A Task 1 — Stratagem-Attributions-Bug | §5, Z.757–758 | erledigt, Commit `8c124c3` |
| A-032 | Ziel7 Stufe A Task 2 — `used_stratagem_ids` global statt Spieler-Slot | §5, Z.759–760 | erledigt, Commit `396fdec` |
| A-033 | Ziel7 Stufe A — Findings F1–F3 | §5, Z.770–771 | erledigt S121/S122, Details `backlog_archive.md` |
| A-034 | §3-Checkliste: WAAAGH Boss-Nob | §3, Z.526 | verifiziert `[x]` |
| A-035 | §3-Checkliste: Cover Option B | §3, Z.527 | verifiziert `[x]` |
| A-036 | §3-Checkliste: Veil aus Nahkampf | §3, Z.528 | verifiziert `[x]` |
| A-037 | §3-Checkliste: Skorpekh-Roster | §3, Z.529–530 | verifiziert `[x]` S146 |
| A-038 | §3-Checkliste: S48 H1–H7 | §3, Z.531–532 | verifiziert `[x]` |
| A-039 | §3-Checkliste: S147 B1-Fix | §3, Z.533–536 | verifiziert `[x]` S148 |
| A-040 | §3-Checkliste: S147 MWBD-Fix | §3, Z.537–539 | verifiziert `[x]` S148 |
| A-041 | §3-Checkliste: B12b zentrale Stratagems-Liste (Insane-Bravery-Kontext) | §3, Z.540–543 | verifiziert `[x]` S150 |
| A-042 | §3-Checkliste: B12b Charge-Phase Fire Overwatch | §3, Z.544–546 | verifiziert `[x]` S148 |
| A-043 | §3-Checkliste: B12b Movement Advance-Reroll | §3, Z.547–548 | verifiziert `[x]` S148 |

*(43 Archiv-Kandidaten oben + 3 weitere kleine, im Fließtext mitgeführte Erledigt-Vermerke
ohne eigene Zeile — Rang 4 „✅ mit Rang 6" etc. sind KEINE Erledigt-Marker sondern
Parallelisierbarkeits-Flags in der Prioritätenliste, s. Zählblock — zählen daher nicht als
eigene Archiv-Kandidaten.)*

---

## Tabelle 3 — Unklare Einträge (nicht raten, an Planner zurückgeben)

| # | Titel | Quelle | Warum unklar |
|---|---|---|---|
| U-001 | GO-UI Paket 1 — GO-Karten-Baustein (4 Zustände, Voll/Kompakt, Akkordeon-Fix) | §2, Z.154–155 | Glyph 🟢 (offen), aber Paket 3a (baut direkt auf dem Baustein auf) ist bereits ✅ erledigt S133 — logisch unmöglich ohne fertigen Paket-1-Baustein. Verdacht: stale Glyph. Vor Weiterverarbeitung gegen `src/uiLayout/goCard.py`/`design_system.md` §6.1 verifizieren. |
| U-002 | GO-UI Paket 2 — Command Re-Roll für Advance/Charge | §2, Z.156–157 | Glyph 🟢 (offen), aber `git log` zeigt Commit `35cc2a2` „Close S136: … command re-roll 9/9 …" — deutet auf vollständige Umsetzung hin. Verdacht: stale Glyph. |
| U-003 | GO-Buttons kontextuell in gameActionArea (aktiver + inaktiver Spieler) statt Liste | §2, Z.318 | Kein Session-Anker, keine Datei-Referenz; Thema klingt bereits durch die GO-UI-Design-System-Roadmap (Pakete 1–6) abgedeckt/überholt. Nicht sicher, ob noch eigenständig relevant. |
| U-004 | Necron Command Phase: Regelkasten immer ganz oben (alle Phasen prüfen) | §2, Z.319 | Ebenso kein Session-Anker/Datei-Referenz — Alter/Aktualität nicht bestimmbar. |
| U-005 | Bug — aktive GO-Effekte ohne Badge am Wirkort (Techno-Oracular Targeting, Disintegration Capacitors, Relentless Onslaught, Solar Pulse) | §2, Z.471–481 | Text sagt „geht als Teilmenge im GO-Audit auf … Umsetzung über die Audit-Fixing-Pläne in S148" — nicht belegt, ob die 4 konkreten GOs durch die S148-Fixes tatsächlich abgedeckt wurden oder ob ein Rest bleibt. |
| U-006 | 🔴 Command-Protocol-Direktiven nicht regelkonform (S95-Befund) | §4b, Z.683–700 | Beschreibt den Ausgangsbefund zu Plan 025, der laut Pfadangabe bereits **archiviert** ist (`../audit/plans/archive/025-protocol-9e-conformance.md`) und dessen Einzelschritte an anderer Stelle im selben Dokument (§0-Tabelle Z.89–100) bereits mit ✅ als erledigt markiert sind. Der 🔴-Glyph wirkt stale; vor Archivierung verifizieren, dass alle 6 Plan-025-Steps tatsächlich abgeschlossen sind. |
