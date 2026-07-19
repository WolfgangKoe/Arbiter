STATUS: NEEDS-DECISION

# S169 — Planning (Planner-Entwurf, Opus)

Lebensdauer: bis Stakeholder-Freigabe des Plans. Der Koordinator legt diesen Entwurf vor,
holt die Entscheidungen zu §A ein, startet erst danach Executor. Nach Session-Abschluss löschen.

> **Grundannahme (bitte bestätigen):** Die vom Stakeholder selbst korrigierte §7 in
> `docs/spec/design_system.md` (uncommitteter Diff) ist die **maßgebliche, faktisch
> abgenommene** §7-Fassung. `S168_SPEC7_ABNAHME.md` ist damit erledigt. Alle Tasks bauen
> auf dieser Fassung auf, nicht auf dem alten Entwurf.

---

## §A — Offene Entscheidungsfragen (früh, bei vollem Kontext-Headroom entscheiden)

### A1 — Retro-Maßnahmen S168 (`S168_RETRO.md`, 3 Maßnahmen)

Empfehlung: **alle drei übernehmen** (so auch die Reviewer-/Retro-Empfehlung).

- **M1 — Bauform-Registrierung mit Pflicht-Schema** (`docs/reference/agent_scopes.md`,
  B-124-Ratchet schärfen): jede §1-Registrierung braucht ein ASCII/Markdown-Mini-Schema,
  nicht nur Prosa. → **übernehmen**, kleiner `agent_scopes.md`-Edit (Task 1).
- **M2 — Wortlaut-Budget für UI-Hinweise** (`design_system.md`): Hinweis-/Warntexte max.
  ein kurzer Imperativ-Satz, Regelbegründung gehört in die Spec. → **übernehmen**,
  **wird direkt in Task 2 (Spec-Umbau) integriert** (überschneidet sich mit der
  Design-System-Arbeit; erledigt zugleich B-124(a), s. A4).
- **M3 — Bash-Allowlist Session-Routine** (`.claude/settings.json`): `rm docs/handoff/*`
  und `curl http://localhost:8501` freischalten. → **übernehmen**, Task 1
  (`update-config`-Skill). **Muss VOR dem Aufräum-Task (Task 6) laufen**, sonst hängt
  `rm` erneut am Classifier (S168-Befund).

**Frage A1:** M1 + M2 + M3 alle wie empfohlen übernehmen? Abweichung bitte je Maßnahme nennen. M1 und M2 übernehmen, wobei wir bei M2 zwischen Anforderungen an das Design-System und Anforderungen definiert durch eine Spec unterscheiden müssen. §7 ist die abgenommene Fassung, gehört aber nicht ins Design-System, sondern in eine Spec. Entsprechend §6. Die Eigenschaften der Würfeldarstellungen aus dice_dispplays gehören ins Design_system, aber die konkrete Darstellung der spec für die Attackenabfolge bleibt dort. M3 verstehe ich nicht, aber es klingt so, dass du hier Ausnahmen schaffen möchtest, um handoff-Dateien zu löschen, und die App starten zu können. Ist in Ordnung. Bitte dabei auch inzwischen überflüssig gewordene Screenshots in handoff entfernen.

### A2 — Ziel-Artefakt für den Feature-Spec-Anteil von §7 (Stakeholder-Input a)

Der Stakeholder-Befund: §7 in `design_system.md` vermischt **generische Bausteine** (Job
dieser Datei laut Artefakt-Landkarte: „UI-Design-System — GO-Karte, Bausteine, Wortlaut")
mit **feature-spezifischem Inhalt** (Explodes: Schwelle 4+, Radius 2D6", D6 MW, welche
Einheiten, `auto_explode`-Stratagem, konkreter Ablauf). Das ist die Struktur-Korrektur.

**Planner-Empfehlung (respektiert Artefakt-Landkarte, kein neues Parallel-Artefakt):**

| Inhalt | Zielort | Begründung (Artefakt-Landkarte) |
|---|---|---|
| Generische Bausteine: Pflicht-Trigger-Kachel (GO-Karte ohne `[Use]`/CP), Binär-Wurf-Baustein (zwei Buttons statt Zahlenfeld), Multi-Unit-Ziel-Auswahl-Panel beider Armeen, Info-Hinweiskasten-Wiederverwendung, Layout-Invariante (Effekt-Ausführung rendert in `center`, Sidebars bleiben `first/second_player`) | **`design_system.md`** — in §1-Inventar registrieren (+ generisches §7, das die Bausteine abstrakt definiert, ohne Explodes-Zahlen) | „UI-Design-System (GO-Karte, Bausteine, Wortlaut)" |
| Feature-Ablauf Explodes: Einheit zerstört → Pflicht-Kachel → Tischwurf gegen YAML-Schwelle → Erfolg: Multi-Select betroffener Einheiten → Schaden je Einheit → anwenden; Fehlschlag: „does not explode"; `auto_explode`-GO | **`docs/spec/processes.md`** — neuer Abschnitt **P-16 „Explodes / Pflicht-Trigger bei Zerstörung"**, referenziert die generischen Bausteine aus `design_system.md` | „Prozess-/Phasen-Specs (Attackenabfolge etc.)" |
| Regel-/Datenbasis (Wahapedia-Explodes-Träger, Schwellen/Radius/Schaden, „App würfelt nicht"-Gotcha) | **`docs/spec/acceptance/rules.md`** (R-COMBAT-38..40, bereits angelegt) + YAML; Gotcha ggf. `rules_insights.md` | vorhandene kanonische Orte |

**Frage A2:** Aufteilung wie in der Tabelle (Bausteine → `design_system.md` §1/§7 generisch;
Feature-Ablauf → `processes.md` P-16)? Oder anderer Zielort?

Ja, sollte so passen. Habe ich schon unter A1 wiederholt.

### A3 — Session-Scope-Tiefe für B-028c1 (Realismus vs. „endlich App-Wert")

**Konflikt, den ich offen benenne:** B-028c1 ist **L-Effort** (Detail-Schätzung 135–155k
Subagent-Token für den Gesamt-Re-Scope) und zerfällt regelkonform in ≤M-Teil-Briefs. Der
Ablauf Schema → UI → Stakeholder-Verifikation ist **sequenziell**; es gibt keinen kurzen
Pfad zu sichtbarem App-Wert. Zusammen mit Task 2 (Spec-Umbau, ebenfalls groß), dem
Aufräum-Task und dem Abschluss-Dreiklang passt **nicht alles** in einen
Koordinator-Korridor <150k. Der Stakeholder will laut Input (b) ausdrücklich **sichtbaren
Mehrwert in der App**, nicht „nur Text in einer Datei".

Teil-Brief-Schnitt B-028c1 (jeder ≤M, eigenständig grün):

- **b1 — Schema + Daten + Engine-Rückbau:** `effect.type: explode` (`roll_threshold`/
  `radius`/`damage`) + Schema-Achse `mandatory`; Rückbau des Engine-Selbstwurfs in
  `resolve_mortal_wounds_effect` (Verstoß „App würfelt nicht"); Wahapedia-Nacherfassung der
  im Roster vorhandenen Explodes-Träger (v. a. Silent King). **Kein sichtbares UI**, voll
  testbar. ~M.
- **b2 — Pflicht-Trigger-Kachel-UI:** Kachel + Binär-Wurf + Ziel-Auswahl-Panel beider
  Armeen + Info-Kasten + Schaden-je-Einheit-anwenden, verdrahtet gegen b1-Schema.
  **Sichtbarer App-Wert.** ~M. Braucht Live-UI-Verifikation (eigener Handoff,
  `AWAITING-VERIFICATION`).
- **b3 — `auto_explode`-GO** (eigene GO mit CP-Kosten, dockt an die Explode-Mechanik). ~M.

**Planner-Empfehlung:** Priorität auf App-Wert. S169 zielt auf
**Task 1 → Task 2 (Spec-Umbau) → b1 → b2**, damit die Kachel sichtbar wird; **b3 +
Aufräumen-Rest + volle P-16-Migration** rutschen bei Korridor-Knappheit sauber nach S170
(geordnetes Wind-down ab ~120k). Falls App-Wert absolute Priorität hat, kann Task 2 auf
das **schlanke Minimum** reduziert werden (nur §1-Registrierung + M2-Wortlaut als
Spec-first-Anker; die vollständige `processes.md`-P-16-Migration dann S170).

**Frage A3:** Bei Token-Knappheit — Reihenfolge (i) **Struktur-Korrektur (Task 2) vollständig
zuerst**, App-Wert ggf. S170; oder (ii) **App-Wert (b1+b2) zuerst**, Task 2 schlank/teilweise?
(Empfehlung: (ii)-nah — Task 2 als schlanken Spec-first-Anker, dann b1+b2.)

### A4 — B-124-Abgrenzung: was erledigt a/b mit, was bleibt offen

- **B-124(a) Warnhinweis-Text im Subgruppen-Selector kürzen** → durch **M2 (Wortlaut-Budget)
  + Task 2** miterledigt (Ratchet bei Berührung von §1.4 / `_common.py`-Warnhinweis).
- **§1-Schema-Qualität** (Stakeholder-Kritik „keine schematische Darstellung") → §1.4 hat
  jetzt ein Schema (committet); **M1** verankert die Schema-Pflicht dauerhaft. Damit ist
  die *Prozess*-Wurzel adressiert.
- **B-124(b) Apply-Damage-Bereich vereinheitlichen** → **bleibt offen** im Backlog.
  Größerer, eigener Design-Pass (nicht durch a/b gelöst — betrifft die gesamte
  Apply-Damage-Fläche, nicht nur den Explodes-Randfall). B-124 bleibt „In Progress"
  (laufender Ratchet) mit b) als konkreter Rest-Substanz.

**Frage A4:** Einverstanden, dass B-124(a)+Schema-Prozess in S169 miterledigt werden und
B-124(b) (Apply-Damage-Vereinheitlichung) als eigener Rest im Backlog bleibt?

### A5 — Handoff-Aufräumen: Lösch-Liste bestätigen (Entscheidung bleibt beim Stakeholder)

Lösch-Whitelist-Vorschlag (Executor darf **nur** namentlich Genanntes löschen,
`agent_scopes.md`-Standardsatz). Vorschlag gegründet auf `grep` je Datei:

**Löschen (Handoff-Marker/Mockups):**
- `S168_REVIEW.md` (GO, „bis Sichtung im S169-Planning" — hiermit gesichtet).
- `S168_RETRO.md` (nach Übernahme der A1-Entscheidungen in die Artefakte).
- `S168_SPEC7_ABNAHME.md` (obsolet — Abnahme durch Stakeholder-Korrektur erfüllt).
- `S166_MOCKUP_EXPLODES.md`, `S166_MOCKUP_EXPLODES_V2.html`, `S167_MOCKUP_EXPLODES_V3.html`
  — **erst NACHDEM** Task 2 die verbindlichen Screenshot-Referenzen (Psi-Flow/
  Heroic-Intervention/Damage-Input) aus `S166_MOCKUP_EXPLODES.md` in die neue Spec
  (P-16 / §1-Registrierung) übernommen hat (Screenshot-Konvention `agent_scopes.md` §e).
  Sonst geht die verbindliche Bauform-Referenz für den noch nicht gebauten Code verloren.

**Screenshots — 7 ohne jede Referenz (Lösch-Kandidaten):**
`2026-07-09 21-29-43.png`, `2026-07-11 09-52-56.png`, `2026-07-11 12-03-17.png`,
`2026-07-12 17-48-56.png`, `2026-07-12 21-11-35.png`, `2026-07-12 21-13-42.png`,
`2026-07-18 11-52-32.png`.

**Screenshots — BEHALTEN (referenziert):**
- `2026-07-09 20-53-48.png` + `…20-58-07.png` (backlog_details B-020; 20-58-07 nur als
  Kurzform `…20-58-07.png` referenziert — **Gotcha:** die automatische Zählung übersieht
  solche Kurzformen, daher pro Datei manuell prüfen).
- `2026-07-11 11-54-31.png` (B-100), `2026-07-16 18-44-05.png` (B-101),
  `2026-07-18 10-20-01.png` (B-028c1 UI-Verif. Runde 1).
- Die 5 Explodes-Referenz-Screenshots (`11-51-02`, `11-51-51`, `11-54-10`, `12-01-39`,
  `12-07-09`) — **verbindliche Bauform-Referenz für B-028c1-Code**; behalten und in P-16
  referenzieren; erst nach b2 + Stakeholder-Verifikation löschen.

**Frage A5:** Lösch-Liste (Marker/Mockups + 7 Screenshots) so bestätigen? Die
Mockup-Löschung ist bewusst an „Screenshot-Refs vorher in die Spec migriert" gekoppelt.

---

## §B — Task-Plan (Reihenfolge, Tier, Dateien, Token)

Verifiziert gegen `git log --oneline`: B-028c1 T1/T2 (S164), selektionsunabhängiger Scan
(S165), §7-Entwurf (S168) sind committet; **keine** B-028c1-Umsetzung (Schema/UI) committet
→ b1/b2/b3 korrekt als offen eingeplant, kein stale Check.

| # | Aufgabe | Effort | Token-Schätzung | Modus | Subagent + Tier | Dateien / Scope |
|---|---------|--------|-----------------|-------|-----------------|-----------------|
| 0 | **Session-Start** (Koordinator): App-Health `curl :8501`, `briefing.md`+`ziel7.md`+`backlog.md` lesen, Backlog-Prio nach S169-Fokus umsortieren (B-028c1/B-124 nach oben, S155) | XS | ~5k | — | Koordinator | `backlog.md` |
| 1 | **Retro-Apply M1+M3** (nach A1-Freigabe): M1 = Schema-Pflicht in Ratchet-Klausel; M3 = `settings.json`-Allowlist `rm docs/handoff/*` + `curl :8501` | XS | ~10k | Gate | Executor Haiku (M1-Doku) + `update-config`-Skill (M3) | `docs/reference/agent_scopes.md`, `.claude/settings.json` |
| 2 | **Spec-Struktur-Umbau (A2)**: generische Bausteine aus §7 → `design_system.md` §1-Registrierung + generisches §7; Feature-Ablauf → `processes.md` **P-16**; M2-Wortlaut-Budget einarbeiten (+ B-124(a) Warnhinweis-Kürzung); Screenshot-Refs aus Mockup in P-16 übernehmen | M | ~150k | Gate | Executor Sonnet (großes Schreib-Artefakt, ADR-0009-Ausnahme) — ggf. 2 Teil-Briefe a1=`design_system.md`, a2=`processes.md` | `design_system.md`, `processes.md`, ggf. `rules_insights.md` |
| 3 | **b1 — Schema+Daten+Engine-Rückbau**: `effect.type: explode`+`mandatory`; Rückbau `resolve_mortal_wounds_effect`-Selbstwurf; Wahapedia-Nacherfassung Roster-Träger | M | ~180k | Gate | Executor Sonnet | `gameObjects/ability.py`, `gameObjects/loader.py`, `gameMechanic/abilityEngine.py`, `data/wh40k_9e/necrons/unit_abilities.yaml`, `tests/` |
| 4 | **b2 — Pflicht-Trigger-Kachel-UI** (verdrahtet gegen b1): Kachel + Binär-Wurf + Ziel-Auswahl-Panel + Info-Kasten + Schaden-anwenden | M | ~190k | Gate | Executor Sonnet | `src/uiLayout/_common.py`, ggf. `*Phase.py`-Render-Anker, `tests/uiLayout/`, `tests/gameMechanic/` |
| 5 | **UI-Verifikation b2** (getrennter Auftrag, max. 2 Runden): Handoff `AWAITING-VERIFICATION` mit Voraussetzungen/Klickpfad/Erwartung + 3 Pflicht-Checkpunkte (regelkonform / Komponente+Anker §-Verweis / Wortlaut-Familie) | S | ~15k Executor + Stakeholder | Konsens | Executor Sonnet (Handoff schreiben) → Stakeholder | `docs/handoff/S169_b2_ui_verifikation.md` |
| 6 | **Handoff-Aufräumen (A5)**: bestätigte Lösch-Whitelist (Marker + Mockups nach Ref-Migration + 7 Screenshots); Lösch-Whitelist-Standardsatz PFLICHT | XS | ~10k | Gate | Executor Haiku | `docs/handoff/` |
| 7 | **Artefakt-Pflege** (im selben Schritt je Task, nicht am Ende): B-028c1-Status/Checkbox nur bei committetem Code; B-124(a) abhaken, B-124(b) als Rest schärfen; `ziel7.md`; `briefing.md` | XS | ~10k | — | Koordinator/Executor | `backlog.md`, `backlog_details.md`, `ziel7.md`, `briefing.md` |
| 8 | **Abschluss-Dreiklang**: Review (Opus, eigenes Fenster, DoD) → Retro (moderiert, nummerierte Maßnahmen) → Commit (stehend freigegeben, S161) + `token_report.py --write` + `rotate_history.py` | M | ~40k Koordinator + Reviewer | Konsens/Konsent | Reviewer Opus → Koordinator | `briefing.md`, Commit |

**Split-Hinweis (S130):** Kein Brief > M. b1/b2 sind je ≤M und einzeln grün; Task 2 bei
Bedarf in a1/a2 schneiden. Core-Logik+UI+Test-Mix (b1+b2) ist bewusst in **zwei** Briefs
getrennt (Retro-M4 S158). Jeder Brief: Test-Budget (gezielt während Entwicklung, **eine**
Vollsuite im Vordergrund `timeout: 600000`), Selbst-Stopp bei ~1,5× Budget,
Selbstprüf-Checkliste (DoD Punkt 7), `pre-commit run --files`.

---

## §C — DoD-Bezug je Umsetzungs-Task

- **Regelkonform (DoD 1):** b1/b3 gegen `docs/work/wahapedia_necrons/` + `wahapedia_orks/`
  belegen (wörtliche Zitate mit Zeilennummern); Ability-Brief-Pflicht (`agent_scopes.md`
  §b): fachliche Einordnung „Pflicht-Trigger" mit Wahapedia-Zitat.
- **Generisch (DoD 2):** keine Fraktions-Strings in `src/` — Explodes-Werte aus YAML;
  Namenswahl gegen INV-4b-Vokabular (`test_generic_src_vocab.py`), Fraktions-Wörter meiden.
- **Tests grün / Coverage ≥ 99 % (DoD 3):** je Bugfix Regressionstest; b2-Render über
  HTML-Output-Test des Render-Einstiegspfads mit realistischem `session_state`-Fixture
  (S164-Lehre), nicht nur isolierte Render-Fn.
- **Architektur-Gate (DoD 4):** `pytest tests/architecture/ --no-cov -q` grün; b2 darf
  Layer-Richtung nicht verletzen.
- **Clean Code (DoD 5):** `pre-commit run --files <geänderte>` sauber (nicht nur `ruff`).
- **UI manuell (DoD 6):** b2 → Task 5 Live-Verifikation (Render-Code coverage-ausgenommen);
  b1 hat keinen sichtbaren UI-Effekt (n/a, begründet).
- **Artefakte aktuell (DoD 7):** Task 7 im selben Schritt; Handoff-Marker + Lifecycle
  (DONE = löschen) in Task 6.
- **UI-Brief-Pflicht (`agent_scopes.md` §a):** b2-Brief nennt Komponente + Anker mit
  §-Verweis auf die (in Task 2 umgebaute) `design_system.md` bzw. P-16.

---

## §D — Token-Budget Gesamtsession

- **Koordinator-Korridor <150k** (Wind-down ~120k, Ende ~135k). Subagent-Token zählen
  separat, aber jede Dispatch + Report-Relay kostet Koordinator-Kontext.
- Realistisch pro Session: **2–3 schwere Executor-Dispatches** + Entscheidungen + Triad.
  Deshalb A3: Task 2 + b1 + b2 sind bereits grenzwertig; **b3 + Aufräum-Rest + volle
  P-16-Migration slippen bei Bedarf nach S170** (geordnetes Wind-down, nichts Neues ab ~120k).
- Abschluss-Pflicht: `python tools/token_report.py --write` +
  `python tools/rotate_history.py --session 169 --summary "…"`.

---

## §E — Aufgefallene Widersprüche / Lücken

1. **Scope-Realismus (Kernrisiko):** Stakeholder will in S169 *beides* — Struktur-Korrektur
   (a) UND sichtbaren App-Wert (b). Beides voll + Aufräumen + Triad passt nicht in einen
   <150k-Korridor. Deshalb Frage A3 als Prioritäts-Entscheid — sonst droht erneut das
   S168-Muster („nur Doku, kein App-Wert").
2. **Mockup-Löschung vs. Bauform-Referenz:** `S168_SPEC7_ABNAHME.md`/Briefing sagen
   „Mockups bei §7-Abnahme löschen". Aber `S166_MOCKUP_EXPLODES.md` enthält die 5
   verbindlichen Screenshot-Referenzen für den noch nicht gebauten Code. Löschen VOR der
   Ref-Migration (Task 2) würde die Screenshot-Konvention (`agent_scopes.md` §e) verletzen.
   Deshalb: Mockup-Löschung an „Refs vorher migriert" gekoppelt (A5).
3. **Screenshot-Referenz-Kurzformen:** die automatische Referenzzählung übersieht
   Kurzformen wie `…20-58-07.png` (backlog_details Z.462). Der Aufräum-Executor muss je
   Datei manuell grep-prüfen, nicht nur die Vollnamen — sonst wird eine referenzierte
   Datei gelöscht.
4. **§7-Diff-Rest:** Im korrigierten §7 zeigen einzelne Querverweise noch auf die alte
   Nummerierung (z. B. §7.1-Schema verweist auf „§7.3"/„§7.4" nach dem Tausch
   Ziel-Auswahl-Panel ↔ Hinweiskasten; §7.4-Text verweist auf „7.5", das jetzt der
   Zwei-Button-Abschnitt ist). Beim Spec-Umbau (Task 2) mitkorrigieren — Querverweise
   gegen die neue Struktur konsistent ziehen.
5. **`design_system.md` uncommittet:** Der Stakeholder-Diff ist noch nicht committet. Task 2
   baut darauf auf; der Abschluss-Commit (Task 8) nimmt Stakeholder-Korrektur + Umbau
   gemeinsam auf — sicherstellen, dass die Korrektur nicht versehentlich verworfen wird.
6. **`Stakeholder_Beobachtungen.md`:** keine offenen Beobachtungen — kein Überführungs-Bedarf.
