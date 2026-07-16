STATUS: ANSWERED (S154: Freigabe erteilt; B-060 in S154 aufgenommen, B-039/061/082 archiviert, B-056/B-028/B-098 → S155 — Parallelitäts-Hinweis: B-056∥B-098 möglich, B-028 nicht parallel zu B-056 wegen _common.py)

# S154 — Planning-Entwurf

Quelle: `.claude/tasks/briefing.md` (S153-Stand) + `docs/goals/backlog.md` (Prioritätsquelle) +
`docs/reference/agent_scopes.md` (Scopes/Brief-Pflichten). Alle Dateipfade unten per `grep`/`ls`
verifiziert, keine Vermutungen. Checkbox-Sync gegen `git log --oneline -30` durchgeführt (Ergebnis
in der Selbstprüfliste unten).

---

## Punkt 0 — Review/Retro-Nachholung S153 (zuerst)

S153 war eine Kurz-Session (Wind-down ~115k Kontext, Reviewer API-limit-blockiert) — **kein
`docs/handoff/S153_review.md` existiert**, keine Retro fand statt. Bevor S154 neue Umsetzung
beginnt, muss dieser Rückstand geschlossen werden — sonst häuft sich ein zweiter unreviewter
Session-Sprung an (Analogie zum S142/S143-Befund: „Review zweimal nachholen").

| Schritt | Ausführender | Tier | Token-Schätzung |
|---|---|---|---|
| DoD-Review S153 (Backlog-Feinschliff: ID-Spalte-Breite, Effort/Assignee-`<br>`-Verschmälerung 91 Zeilen, Typ-Feld-Färbung 91×) — Prüfgegenstand ist der Commit `974403a` + Vorgänger `c59f3a3`/`441862b` seit dem letzten Review (S152). Reviewer prüft: (1) Doku/Acceptance-Gate weiterhin grün, (2) `test_backlog_structure`-Regex durch die ID-Spalten-Änderung nicht gebrochen, (3) M2-Werkzeug-Klausel-Offenlegung (script-gestützter Edit ohne Einzel-Executor) korrekt dokumentiert. Ergebnis als `docs/handoff/S154_review_s153.md`. | Reviewer-Subagent | Opus (ADR-0007: finales Review immer Opus) | ~15k |
| Retro S153 (getrennter Schritt) — Kernfrage: Warum blockierte das API-Limit sowohl Executor- als auch Reviewer-Start? Ist das ein wiederkehrendes Risiko (Tageszeit-abhängig, Reset 20 Uhr laut Briefing) das eine Prozessanpassung braucht (z. B. Session-Start früher am Tag, oder Fallback-Tier bei Limit)? Maßnahmen-Liste nummeriert, entscheidbar. | Koordinator moderiert (kein Subagent — Retro ist Stakeholder-Dialog) | — | ~5k |

**Reihenfolge-Begründung:** Modus `Konsens`/Entscheidungs-Timing-Regel (agent_scopes.md) — Reviews
mit möglichem Befund gehören früh in die Session, solange Kontext-Headroom groß ist.

---

## Priorisierte Aufgabenliste (a)–(f)

### (a) UI-Nacharbeiten aus S152 — B-009 + B-087

Beide sind reine **Recherche-/Korrektur-Aufträge**, keine Neu-Features — passen gut hintereinander
in einen Sonnet-Executor-Brief (getrennte Teil-Schritte, gemeinsamer Commit möglich).

| Task | Betroffene Dateien (verifiziert) | Ausführender/Tier | Token |
|---|---|---|---|
| **B-009** — zwei geeignete Rosters für den PSI-Flow-Test benennen. Geprüft: `data/rosters/` enthält 9 Roster-Dateien (`necrons_1500pts_silent_king.yaml`, `necrons_alpha.yaml`, `necrons_b1_verification.yaml`, `necrons_beta.yaml`, `necrons_test.yaml`, `orks_test.yaml`, `orks_transport.yaml`, `orks.yaml`, `zarekhan_sol_kampf_2.yaml`) — kein Ork/Custodes-Roster mit Deny-Fähigkeit vorhanden; Necron-Seite braucht einen Psi-fähigen Charakter (z. B. Silent King), Gegenseite muss deny-fähig sein (nur Fraktionen mit Psychic Interrogation/Anti-Psyker-Wargear). Aufgabe: die 9 Rosters gegen Deny-Fähigkeit prüfen, zwei passende benennen oder eine fehlende Kombination ergänzen. Code selbst ist grün seit S65 — reiner Recherche-Schritt vor Neuvorlage an den Stakeholder. Datei: `src/gameMechanic/psychicPhase.py` (Kontext, keine Änderung nötig). | Executor (Sonnet — Roster-Regelwissen nötig, kein reiner Format-Lookup) | ~10k |
| **B-087** — Fire-Overwatch/Counter-Offensive-Trigger-Timing gegen `docs/work/wahapedia_core_rules/` verifizieren. Betroffene Dateien: `src/gameMechanic/chargePhase.py` (`_inactive_charge`, Zeile 154), `src/gameMechanic/fightPhase.py` (`_apply_counter_offensive`, Zeile 105, Aufruf Zeile 458). Nach Regel-Check ggf. Korrektur + Re-Test. UI-Ausgrauen-Fix **nicht** hier lösen — nur als Beleg für B-031 mitnehmen (S152-Entscheid: B-087-UI-Teil ist ein Teilfall von B-031, wird dort gelöst). | Executor (Sonnet — Regelrecherche + Korrektur, kein reiner Lookup) | ~15k |

### (b) B-056 — Quantum Shielding Scope (b)

Betroffene Dateien (verifiziert): `data/wh40k_9e/necrons/unit_abilities.yaml:905` (Fähigkeit
„Quantum Shielding", `has_rules: [quantumShielding]`), `data/wh40k_9e/necrons/stratagems.yaml:459`
(Stratagem „Quantum Deflection", 4+ Invuln temporär), `src/gameMechanic/stratagemEngine.py:32`
(`invuln_save`-Mechanik-Kommentar), `src/uiLayout/_common.py` (Save-Block-Rendering,
Zeile ~2188). Aufgabe: (1) Anzeige-Bug der Fähigkeit fixen (unmod. Wound 1–3 = Auto-Fail wird
weder als Debuff in der Wound-Zeile noch als Buff im Save-Block angezeigt), (2) neuer
Mechanik-Typ „Invuln auf festen Wert setzen" (nicht additiv) für das Stratagem. Zwei
unterschiedliche Mechaniken mit demselben Namen — Verwechslungsgefahr, deshalb im Brief explizit
beide YAML-IDs nennen. **Effort M (~35k) — an der Obergrenze für einen Einzel-Brief; falls der
Executor beim Anlegen des neuen Mechanik-Typs über ~50k läuft, Selbst-Stopp-Klausel greift.**

| Ausführender | Tier | Token |
|---|---|---|
| Executor | Sonnet (Engine-Erweiterung, kein Lookup) | ~35k |

### (c) B-028 — used-on-Suffix auf alle reaktiven GOs ausweiten

**Ist-Bestand gezählt (nicht geschätzt):** Aktuell gibt es `grep -c "render_go_card("` → **4
Call-Sites** (`src/gameMechanic/movementPhase.py:325`, `:455`, `src/uiLayout/_common.py:869`,
`src/uiLayout/gameProtocoll.py:368`) + **6 Aufrufer** von `render_reactive_stratagem_box()` laut
`docs/handoff/S150_usedon_renderpaths.md` (fightPhase.py:460, chargePhase.py:174,
movementPhase.py:663, psychicPhase.py:192+527, `_common.py:1190`). **Alle 10 Stellen sind
Stratagem-spezifisch verdrahtet** — die Datenquelle ist ausschließlich
`stratagem_use_anchors`/`stratagem_used_elsewhere_unit_name()` (`src/uiLayout/_common.py:552`,
einziger Fund für `use_anchor` im ganzen `src/`-Baum). Es gibt **keine** äquivalente
Anker-Verfolgung für nicht-Stratagem-GOs (Fähigkeiten). B-028 ist damit **keine reine
Mengen-Erweiterung bestehender Stellen**, sondern verlangt: (1) `stratagem_use_anchors` zu einem
generischen `go_use_anchors` verallgemeinern (Schema unverändert, nur Schlüsselraum erweitern),
(2) Schreibpfad für reaktive Fähigkeiten identifizieren (wo werden reaktive Abilities aktuell
ausgelöst — `abilityEngine.py` statt `spend_stratagem()`) und dort ebenfalls den Anker setzen,
(3) die 10 bestehenden Call-Sites unverändert lassen (sie funktionieren bereits generisch über
den verallgemeinerten Anker), nur die YAML-Quelle der Fähigkeiten prüfen, wie viele reaktive
(`timing: phase_reactive`) Nicht-Stratagem-GOs es überhaupt gibt (diese Zahl hat der Planner NICHT
gezählt — **Selbst-Stopp-Punkt 1 des Executor-Briefs:** zuerst zählen, dann erst Umsetzung
beginnen, bei Überraschung Zwischenstand zurückgeben statt weiterzuarbeiten).

| Ausführender | Tier | Token |
|---|---|---|
| Executor | Sonnet (Architektur-Verallgemeinerung, kein Lookup) | ~35k (Effort M — bereits an der Obergrenze; falls die Ist-Bestandsaufnahme mehr reaktive Non-Stratagem-GOs findet als erwartet, **hier splitten statt überziehen**) |

### (d) Ex-XS-Items (12 Stück, Stakeholder-Auftrag: einplanen + erledigen)

Alle 12 Items gegen `backlog_details.md` verifiziert — Status/Beschreibung stimmen mit
`backlog.md` überein. **Befund vorab:** B-039 ist bereits erledigt (s. Selbstprüfliste unten,
Punkt „stale Backlog-Einträge") — aus der S154-Liste gestrichen, stattdessen Archivierungs-Hinweis
im Fazit.

| ID | Aufgabe (verifiziert) | Datei(en) | Tier | Token |
|---|---|---|---|---|
| B-019 | „Alt. Fire"-Chip unerklärt — Regelwortlaut „Alternating Fire" gegen `docs/work/` prüfen, dann Kurzerklärung analog „Extra Hits" ergänzen. | `src/uiLayout/diceHtml.py:70` (`special_die_html`) | **Haiku** (reiner Lookup + Format-Ergänzung analog Bestandsmuster) | ~5k |
| B-025 | Rest-Wahrnehmung nach B1-Fix — kurzer Sprung/Zucken beim Slot-Wechsel; Fenster bleibt an Ort, aber optisches Zucken bleibt. Beobachten, ggf. Dropdown-Höhen stabilisieren. | UI-Render, kein fixer Dateipfad — Playwright-Probe nötig (Standardwerkzeug seit S136) | Sonnet (Playwright-Beobachtung + CSS-Fix, kein reiner Lookup) | ~5k |
| B-027 | `unit_key`/uid durch `spend_stratagem` durchreichen (Advance-Reroll/Fire-Overwatch-Randfall) — optional, spec-konform, kein Bug. | Aufrufer von `spend_stratagem` (Advance-Reroll in `movementPhase.py`, Fire-Overwatch in `chargePhase.py`) | Sonnet (Signatur-Änderung über mehrere Call-Sites) | ~5k |
| B-036 | Battle-Log zeigt nach Reset alte Einträge — Bug, Teil von Plan 018. | `src/gameMechanic/gameLog.py`, `gameState.py` (Reset-Pfad) | Sonnet (Bugfix + Regressionstest) | ~5k |
| B-053 | `gretchin_mob`-Regeltext prüfen — 8E-Formulierung „must take a Morale test if it suffers any casualties" gegen 9E-Bedingung (Verlust UND unter Half-Strength?). | `data/wh40k_9e/orks/unit_abilities.yaml:260` (`gretchin_mob`) | **Haiku** (Regel-Lookup, ja/nein-Vergleich gegen Wahapedia-Text) | ~5k |
| B-060 | Token-Disziplin-Implementierungsdetails (Transcript-Pfad, Regex-Fallstrick) aus `CLAUDE.md` nach `operating_model.md` Event 6 verlagern. **Verifiziert:** Event 6 (`operating_model.md:193`) verweist aktuell bewusst NICHT-dupliziert auf CLAUDE.md — die Details stehen noch in CLAUDE.md. **Freigabepflichtig (CLAUDE.md-Änderung) — vor Umsetzung Stakeholder-Freigabe einholen**, nicht nur Plan zeigen. | `CLAUDE.md` (Token-Disziplin-Abschnitt), `docs/governance/operating_model.md` (§ev6) | Sonnet (Doku-Verschiebung, aber freigabepflichtig) | ~5k |
| B-061 | Backlog-§0-Hygiene — durch B-007-Restrukturierung strukturell bereits erledigt (§0 existiert in der Neufassung nicht mehr). **Empfehlung: sofort archivieren, kein Umsetzungsaufwand.** | `docs/goals/backlog.md` (Struktur bereits migriert) | — (nur Archivierung) | ~1k |
| B-068 | Silent-King-Zusatzattacken-Default (Staff of Stars 4 / Scythe of Dust 3) auf Maximum vorbelegen statt niedrigerem Startwert. | `data/wh40k_9e/necrons/weapons.yaml:835` (Staff of Stars), `:861` (Scythe of Dust) + zugehöriger Input-Widget-Code (UI, `src/uiLayout/` — genaue Zeile im Brief vom Executor per grep zu ermitteln) | Sonnet (UI-Default-Wert, kein reiner Lookup) | ~5k |
| B-072 | CORE-Keyword-Abgleich Annihilation Barge/Flayed Ones (`necrons/units.yaml`) + Ork-Boss-Nob-Waffen-Zweifel („wirklich nur Stikkbomb?") gegen Wahapedia. **Verifiziert:** Boss Nob führt laut YAML bereits `slugga`+`choppa`+`stikkbombz` plus Swap-Optionen (3 Varianten in `orks/units.yaml`, Zeilen 542/833/1095) — Stakeholder-Zweifel könnte bereits durch bestehende Swaps beantwortet sein; trotzdem gegen Wahapedia verifizieren. | `data/wh40k_9e/necrons/units.yaml` (Zeilen 494/1155-Umfeld), `data/wh40k_9e/orks/units.yaml` (Zeilen 542/833/1095) | **Haiku** (reiner Datenabgleich) | ~5k |
| B-079 | DRY ±1-Cap-Helper — `_render_dice_roll_block` (Zeile 34) und `_render_dice_wound_block` (Zeile 97) in `diceHtml.py` teilen identische Cap-Logik, gemeinsamen Helper extrahieren. | `src/uiLayout/diceHtml.py` | Sonnet (Refactor, Tests müssen grün bleiben) | ~5k |
| B-082 | Executor-Auftrags-Checkliste härten (`ruff`/pre-commit vor „grün"-Claim, Token-/Zeit-Cap). **Befund: bereits erfüllt** — `agent_scopes.md` enthält bereits „Format: `pre-commit run --files <geänderte Dateien>` ausgeführt und sauber (nicht nur `ruff check`)" (Selbstprüf-Checkliste) UND die „Selbst-Stopp-Klausel" mit Budget+Schwelle (S130-Retromaßnahme, Commit `1861d9d`). **Empfehlung: als erledigt archivieren, kein Umsetzungsaufwand** — im Review/Retro (Punkt 0) dem Stakeholder zur Bestätigung vorlegen. | `docs/reference/agent_scopes.md` (bereits vorhanden) | — (nur Archivierung nach Bestätigung) | ~1k |

**Von der S154-Liste entfernt (stale, bereits erledigt):**
- **B-039** (`build_aura_range_hint_text` entfernen) — `grep -rn "build_aura_range_hint_text" src/ tests/` liefert **0 Treffer**; laut `docs/spec/acceptance/rules.md:1240` wurde die Funktion bereits **in S139** entfernt. Backlog-Zeile ist stale — empfohlen: direkt nach `backlog_archive.md` verschieben, kein Executor-Aufwand nötig.

### (e) B-098 Teil 2 — Kombi-Waffen-Engine-Erweiterung

Betroffene Dateien (verifiziert): `data/wh40k_9e/orks/units.yaml` (Boss-Nob-Einträge Zeilen
542–565 und 833–850 — **nicht** die Warbike-Variante Zeile 1095, dort laut Backlog-Vermerk
explizit ausgenommen), `data/wh40k_9e/orks/weapons.yaml:1099` (`kombi_rokkit`),
`:1123` (`kombi_skorcha`). Bestehendes `weapon_swaps`-Schema (`scope: group`, `pick: N`,
`replaces`, `options`) ist im Repo etabliert (10 Vorkommen in `orks/units.yaml`) — Teil (a) neuer
`weapon_swap`-Eintrag für Boss Nob ist ein Muster-Fit. Teil (b), die „eines oder beide Profile,
bei beiden −1 to hit"-Mechanik, ist mit dem aktuellen `WeaponProfile`-Schema **nicht** abbildbar
(kein bestehendes Feld für ODER-Gruppen mit Modifier-Kopplung) — braucht echte Engine-Erweiterung
in `src/gameObjects/weapon.py` + Konsument in `src/gameMechanic/combat.py`/`attackMath.py`.
**Effort M (~35k), an der Obergrenze — wenn die Engine-Erweiterung beim Anfassen mehr als die
Boss-Nob-Kombi-Waffen betrifft (z. B. andere generische ODER-Gruppen-Fälle), Executor stoppt und
meldet Scope-Überraschung statt zu erweitern.**

| Ausführender | Tier | Token |
|---|---|---|
| Executor | Sonnet (Engine-Erweiterung) | ~35k |

### (f) Retro-Maßnahmen M1 + M2 umsetzen

| Maßnahme | Betroffene Datei | Tier | Token |
|---|---|---|---|
| **M1** — Planner-Briefs müssen Item-Mengen bei Format-Umbauten zählen (grep/wc), nicht schätzen. Ergänzung in `docs/reference/agent_scopes.md` Planning-Abschnitt (Pflichtschritte-Liste, nach „Checkbox-Vollständigkeit"). | `docs/reference/agent_scopes.md` | Sonnet (Doku-Ergänzung, kurz) | ~5k |
| **M2** — Werkzeug-Klausel präzisieren: script-gestützte Massen-Edits zulässig bei Offenlegung + grünem Gate-Beleg (B-099b als akzeptierter Präzedenzfall referenzieren). Ergänzung in der „Werkzeug-Klausel (S123)"-Zeile (`agent_scopes.md:125`). | `docs/reference/agent_scopes.md` | Sonnet | ~5k |

Beide M1+M2 betreffen dieselbe Datei im selben Abschnitt — **ein gemeinsamer Brief statt zwei**,
um Doppel-Edits zu vermeiden.

---

## Empfehlung: was passt in den S154-Korridor (<150k, Review/Retro-Budget ~45k)

Korridor-Rechnung: Punkt 0 (~20k) + Review/Retro-Budget-Reserve laut CLAUDE.md (~45k) lässt
**~85k** für neue Umsetzung, wenn die Session bis ~135k (Wind-down-Schwelle) laufen soll — nicht
bis 150k, das ist bereits die rote Zone.

**Empfohlene Reihenfolge für S154 (Budget ~85k, mit Puffer):**

1. Punkt 0 (Review + Retro S153) — ~20k, **zuerst, volles Headroom nutzen**
2. (d) Ex-XS-Items, die Haiku-fähig sind: B-019, B-053, B-072 — ~15k gesamt (billig, schnell weg)
3. (a) B-009 + B-087 Nacharbeit — ~25k
4. (d) restliche Sonnet-Ex-XS-Items: B-025, B-027, B-036, B-068, B-079 — ~25k
5. (f) M1+M2 gemeinsamer Brief — ~10k

**Summe bis hier: ~95k** inkl. Punkt 0 — passt in den Korridor mit Puffer bis zum
Wind-down-Punkt (~120k).

**Explizit NICHT diese Session (auf S155 verschieben):**
- **(b) B-056** (~35k) — Quantum-Shielding-Engine-Erweiterung, würde den Korridor sprengen, wenn
  vorher schon (a)+(d)+(f) liefen.
- **(c) B-028** (~35k) — used-on-Generalisierung, gleicher Grund; zusätzlich unklarer Umfang
  (Ist-Bestandsaufnahme reaktiver Non-Stratagem-GOs steht noch aus) — sollte ohnehin nicht am
  Ende einer vollen Session starten (S121-Lehre: Aufgaben mit Überraschungspotential brauchen
  Headroom).
- **(e) B-098 Teil 2** (~35k) — Engine-Erweiterung, gleicher Grund.
- **B-060** (freigabepflichtig, CLAUDE.md) — sollte trotz geringem Aufwand nicht in der zweiten
  Hälfte einer engen Session laufen, weil eine Freigabe-Rückfrage Kontext-Zeit kostet; auf S155
  verschieben oder als erster Punkt nach Punkt 0, falls der Stakeholder sofort zustimmt.
- **B-061, B-082** — kein Umsetzungsaufwand, nur Archivierungs-Bestätigung; kann direkt im
  Review/Retro-Schritt (Punkt 0) mitentschieden werden, kein separater Slot nötig.

Falls der Stakeholder B-056/B-028/B-098 dennoch vorzieht: einzeln vergeben (jeweils eigene
Session oder eigener später Slot mit vollem Headroom), nicht alle drei in einer Session — jedes
ist bereits einzeln an der M-Obergrenze.

---

## Offene Fragen an den Stakeholder

1. **B-060 Freigabe:** Soll die CLAUDE.md-Kürzung (Token-Disziplin-Details → operating_model.md)
   in S154 überhaupt versucht werden, oder auf einen Slot mit mehr Headroom verschieben (da
   freigabepflichtig)?
2. **B-061 + B-082 Archivierung:** Beide Items scheinen bereits strukturell/inhaltlich erledigt
   (s. Befunde oben). Bestätigung erbeten, dann Archivierung ohne Executor-Aufwand im selben
   Schritt wie Punkt 0.
3. **B-039 Archivierung:** Funktion bereits in S139 entfernt — Zeile aus `backlog.md` streichen
   und Detail-Abschnitt nach `backlog_archive.md` verschieben? (Reine Bestätigung, kein Aufwand.)
4. **Reihenfolge (b)/(c)/(e) für S155:** Alle drei sind ~35k-Engine-Aufgaben — welche Priorität
   zuerst, falls S155 nicht für alle drei reicht?

---

## Selbstprüf-Checkliste

- [x] Alle Backlog-IDs gegen `backlog.md` verifiziert (existieren, Status stimmt) — B-009, B-087,
      B-056, B-028, B-098 sowie alle 12 Ex-XS-IDs (B-019, B-025, B-027, B-036, B-039, B-053,
      B-060, B-061, B-068, B-072, B-079, B-082) einzeln in `backlog_details.md` gelesen und mit
      der Tabellenzeile in `backlog.md` abgeglichen.
- [x] Betroffene Dateien per grep/ls belegt, nicht geraten — alle Datei:Zeile-Angaben oben stammen
      aus `grep -n`/`ls`-Läufen in diesem Planning-Schritt (siehe Belege in den Task-Zellen).
- [x] Item-Mengen bei Massen-Edits gezählt (Befehl + Zahl angeben) — B-028:
      `grep -c "render_go_card("` → 4 Call-Sites; `render_reactive_stratagem_box()`-Aufrufer laut
      `S150_usedon_renderpaths.md` → 6 Stellen; `grep -rn "use_anchor" src/` → nur
      `stratagem_use_anchors` existiert, 0 generische Non-Stratagem-Anker. B-098:
      `grep -c "weapon_swaps:" data/wh40k_9e/orks/units.yaml` → 10 bestehende Vorkommen (Muster-
      Referenz). B-039: `grep -rn "build_aura_range_hint_text" src/ tests/` → 0 Treffer (bereits
      entfernt).
- [x] Checkbox-Sync gegen `git log` durchgeführt, Ergebnis genannt — `git log --oneline -30`
      geprüft; letzter Commit `974403a` (S153-Backlog-Feinschliff) deckt sich mit dem
      briefing.md-Stand. `ziel7.md`-Checkboxen enthalten keine neu gesetzten Haken ohne
      Commit-Beleg (§6e–6h bleiben unverändert `[ ]`, ältere `[x]`-Zeilen sind alle mit
      Session-Referenzen belegt — kein Stale-Fund in `ziel7.md`). **Stale-Fund stattdessen im
      Backlog selbst:** B-039 als „ToDo" gelistet, obwohl Code+Tests laut `acceptance/rules.md`
      bereits S139 entfernt wurden — siehe Abschnitt (d) oben und Frage 3.
- [x] Token-Schätzungen pro Aufgabe vorhanden — s. Tabellen oben (jede Zeile trägt eine
      `~Nk`-Spalte).
- [x] Datei unter `docs/handoff/S154_planning.md` abgelegt.
