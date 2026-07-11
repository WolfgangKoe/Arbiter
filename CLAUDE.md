# CLAUDE.md — Arbiter Workflow

## Projekt-Kontext

**Arbiter** ist ein Streamlit-basierter Spielbegleiter für Warhammer 40.000 9. Edition.

- Start: `streamlit run src/app.py` (Port 8501)
- Datenebene: YAML unter `data/wh40k_9e/<fraktion>/` — Loader ist `gameObjects/loader.py`
- Rosters: `data/rosters/` (YAML, werden beim Start geladen)
- Branch: `dev` (aktiv), `main` (nur per PR, alle Tests grün)

### Regelrecherche — IMMER zuerst selbst nachschlagen

Regelfragen **niemals dem Nutzer stellen** — alle Regeln liegen lokal vor:

| Quelle | Inhalt |
|---|---|
| `docs/work/wahapedia_core_rules/core_rules.txt` | Vollständige 9E-Grundregeln |
| `docs/work/wahapedia_core_rules/rules_appendix.txt` | Regelanhang (Sonderfälle, Glossar) |
| `docs/work/wahapedia_necrons/` | Necron-Regeln und Einheiten |
| `docs/work/wahapedia_orks/` | Ork-Regeln und Einheiten |
| `docs/work/wahapedia_adeptus_custodes/` | Custodes-Regeln |
| `docs/work/schlachtrunde.md` | Übersicht Spielrunden-Ablauf |

Vorgehen: Erst lesen, bevor du den Plan für die Implementierung erstellst. Nur wenn nach Lesen der Regeln mehrere UI-Varianten möglich sind, den Nutzer nach dem bevorzugten Layout fragen. 

### Artefakt-Landkarte — welches Dokument wofür

Damit nichts „verloren" geht: jede Frage hat **genau einen** kanonischen Ort.
Einstiegstür für den Stakeholder ist der **Leitstand** (`LEITSTAND.md`) — er verlinkt alles, dupliziert nichts.

| Frage | Artefakt |
|---|---|
| **Gesamtübersicht / Einstiegstür (Stakeholder)** | `LEITSTAND.md` |
| **Wer entscheidet was? (Rollen, Model-Tier, Events, Modi)** | `docs/governance/operating_model.md` |
| **Warum fiel eine Konsens-Entscheidung so? (ADR)** | `docs/governance/decisions/` |
| **Rohe Ideen → gemeinsames Verständnis (Refinement)** | `Fotos/` → `docs/inbox/` |
| Was mache ich als Nächstes? (aktueller Stand) | `.claude/tasks/next_session.md` |
| Was ist insgesamt offen? (zentraler Backlog) | `docs/goals/backlog.md` |
| Detailplan eines Features (Executor) | `docs/audit/plans/` (+ `README.md` = Queue/Status) |
| Architektur-Gesamtbild | `docs/spec/architecture.md` |
| **Architektur-Invarianten (messbar, grün/rot)** | `docs/spec/architecture_invariants.md` (Wächter: `tests/architecture/`) |
| Prozess-/Phasen-Specs (Attackenabfolge etc.) | `docs/spec/processes.md` |
| Nicht-offensichtliche Regelerkenntnisse (Implementierungs-Gotchas) | `docs/spec/rules_insights.md` |
| Farbschema (verbindlich) | `docs/spec/design_colors.md` |
| UI-Design-System (GO-Karte, Bausteine, Wortlaut) | `docs/spec/design_system.md` |
| Ziel-Übersicht + Historie/Changelog | `docs/goals/index.md` · `docs/metrics/session_archive.md` |
| **Stakeholder-Beobachtungen (stehender Eingang)** | `docs/handoff/Stakeholder_Beobachtungen.md` |

Regel: keine zweite „Stand"- oder „Backlog"-Datei anlegen. Verteilte Notizen gehören in
eines dieser Artefakte — sonst driften sie auseinander.

### Domänen-Constraints (unveränderlich)

- **Seitenleisten:** `first_player` links, `second_player` rechts — Layout nie an `active`
  binden; `first_player`/`second_player` sind unveränderlich.
- **Keywords:** in YAML immer `UPPERCASE`.
- **Waffenstärke:** `_parse_strength(raw, unit_strength)` — nie `int(strength)` direkt.
  YAML: int = fest, `"+N"` = User+N, `"×N"` = User×N, `"User"` = User.

---

## Workflow-Regeln (PFLICHT)

### Haltung — ganzheitlich, konstruktiv-kritisch, lösungsorientiert

Grundhaltung in **Planning** (Session-Start) und **Abschluss** (Review/Retro):

- **Ganzheitlich denken** — Code ↔ App ↔ Spielregeln ↔ Architektur ↔ Doku als ein
  System sehen; eine Änderung nie isoliert bewerten (vgl. DoD-Review).
- **Konstruktiv-kritisch** — Annahmen, Plan und bestehenden Code aktiv hinterfragen;
  Drift, Schuld und blinde Flecken benennen statt übergehen. Kritik immer mit
  Lösungsvorschlag, nie als Selbstzweck.
- **Lösungsorientiert** — Wurzeln statt Symptome adressieren (keine temporären Fixes);
  Vorschläge konkret und umsetzbar halten.
- **Vorausschauend, in kleinen Schritten** — Verbesserungen als kleine Experimente,
  kein großer Umbau; nächste Priorität gegen den Backlog prüfen.
- **Stakeholder-verständlich** — Befunde und Empfehlungen so formulieren, dass der
  Stakeholder sie nachvollziehen und entscheiden kann.

Diese Haltung ersetzt **keine** Freigabe-Pflicht — sie prägt, *wie* geplant, reviewt
und kommuniziert wird, nicht *ob* freigegeben werden muss.

### Freigabe vor Umsetzung
- **Niemals Code schreiben oder Dateien bearbeiten ohne vorherige explizite Freigabe**
- Vor jeder Umsetzung: Plan beschreiben + **alle betroffenen Dateien auflisten**
- Warten bis der Nutzer explizit zustimmt (z.B. „ja", „mach es", „ok")
- Ausnahme: expliziter „freier Lauf" für mehrere Schritte

### Was NIEMALS ohne explizite Freigabe passiert
Dieselbe Pflicht wie für Code gilt auch für:
- Memory-Einträge schreiben oder ändern
- Skills aufrufen, die Dateien oder Einstellungen ändern (z.B. `update-config`)

**Ausnahme — Subagenten: stehende Freigabe.** Subagenten dürfen **ohne Einzel-Freigabe**
eingesetzt werden, wann immer angebracht (Sonnet/Haiku billiger als Opus) — ich schlage sie
proaktiv vor und starte sie selbst, statt pro Fall zu fragen. Pflicht bleibt **Transparenz**
(Auftrag + Tier nennen) und die Freigabe-Pflicht für **datei-/einstellungsändernde** Arbeit:
Code-/Memory-/Skill-Edits laufen weiter durchs Freigabe-Gate, auch wenn ein Subagent sie macht.
Begründung: [ADR-0005](docs/governance/decisions/0005-stehende-subagent-freigabe.md).

### Was „Freigabe" bedeutet
- ✓ Explizit: „ja", „mach es", „ok", „Freigabe", „mach weiter"
- ✗ Rückfrage des Nutzers zum Plan = **keine** Freigabe
- ✗ Ergänzung des Nutzers zum Plan = **keine** Freigabe → Plan aktualisieren, neu zeigen, warten
- ✓ „meinetwegen" / direkter Befehl = Freigabe **nur** für das explizit Genannte

### Bei Unklarheiten IMMER zuerst fragen
- Wenn eine Anforderung mehrdeutig ist — **STOP, Frage stellen, auf Antwort warten**
- Kritisch bei: Scope-Fragen, „X entfernen und nach Y verlagern", Fraktion vs. global
- **Falle:** „Necron-Check entfernen" ≠ „für alle Fraktionen öffnen" — nur der *Ort* des Aufrufs ändert sich, nicht die Logik

### Session-Workflow
1. **Session-Start:** `.claude/tasks/next_session.md` lesen → `docs/goals/<aktives_ziel>.md` lesen
   → **Checkbox-Sync: jeden Haken gegen `git log --oneline` verifizieren** — stale Checks
   (gesetzt, aber Code fehlt) sofort melden, bevor der Plan aufgebaut wird.
2. **Plan zeigen** → Freigabe einholen → Implementieren
3. **Session-Ende:** `.claude/tasks/next_session.md` aktualisieren (Stand, nächster Schritt, offene Fragen)
4. `docs/goals/<aktives_ziel>.md` Checkboxen abhaken — **nur wenn Code committet**; stale Checks
   explizit öffnen und in den nächsten Schritt übernehmen, nicht still stehen lassen.

**Kritisch beim Update:** `.claude/tasks/next_session.md` ZUERST lesen, dann ergänzen — niemals blind überschreiben. Erkenntnisse aus früheren Sessions dürfen nicht verloren gehen. Keine zweite Datei anlegen (nicht im Root, nicht in `docs/`).

### Ganzheitlicher Review-Schritt — Definition of Done

Jede Korrektur/Ergänzung wird **ganzheitlich** betrachtet: Code ↔ App ↔ Spielregeln ↔ Architektur.
Eine Änderung gilt erst als fertig, wenn alle Punkte erfüllt (oder begründet n/a) sind:

1. **Regelkonform** — gegen `docs/work/wahapedia_*/` geprüft (nicht aus dem Gedächtnis).
2. **Generisch** — keine neuen Fraktions-Strings/-Checks in `src/`; Entscheidungen aus YAML.
3. **Tests grün** — `pytest --tb=short`, Coverage ≥ 99 %; jeder Bugfix bekommt einen Regressionstest.
4. **Architektur-Gate grün** — `tests/architecture/` (oder bewusste Änderung +
   `architecture_invariants.md`/`architecture.md` nachgezogen, kein stilles Aufweichen).
5. **Clean Code** — `black`/`isort`/`ruff` sauber; Namen erklären *Was*.
6. **UI manuell verifiziert** — Render-Code (uiLayout, `*Phase.py`) ist nicht von Tests gedeckt →
   explizit nennen, was zu prüfen ist; nie „fertig" ohne manuelle Prüfung.
7. **Artefakte aktuell — im selben Schritt wie die Umsetzung, nicht erst am Session-Ende:**
   Backlog-/Ziel-Checkbox abhaken, Handoff-Marker auf DONE (Datei gemäß Lifecycle-Zeile löschen),
   betroffene Specs nachziehen. Umsetzung ohne Haken + Doku-Nachzug = NICHT fertig → Review NO-GO.
   Jeder Executor-Auftrag führt diesen Punkt in seiner Selbstprüf-Checkliste
   (Anlass: S116–S118-Drift → Wiedervorlage S120).

**Doku-Drift:** Widerspricht Code einer Spec, ist das ein Befund — melden/korrigieren, nicht ignorieren.

### Standard-Prompts (Kurzschrift)

**Session starten — Plan vorlegen** (Default):
> start next session

→ **Planner-Subagent beauftragen** (liest `next_session.md` + Zieldatei + `backlog.md` + Index laut
`agent_scopes.md`, legt Planning-Entwurf als Datei ab); Koordinator legt den Entwurf dem Stakeholder
vor. **Auf Freigabe warten**, dann Executor-Subagent starten.

**Session starten — direkt los** (Plan ist schon freigegeben, Shortcut):
> Beginne mit der nächsten Session. Der Plan ist freigegeben.

→ Koordinator liest `next_session.md` (Pfade/Marker), beauftragt direkt den ersten Executor-Subagent —
kein erneuter Plan nötig.  
Ausnahme: Wenn der Nutzer zusätzlich ein konkretes Thema oder einen Bug nennt, hat dieses Vorrang
**als Planungsgegenstand** — der Planning-Schritt (Planner-Entwurf vorlegen → explizite Freigabe →
erst dann Executor) entfällt dadurch NICHT. Eine mitgelieferte Entscheidung (z. B. „folgt der
Empfehlung" zu einer NEEDS-DECISION-Datei) beantwortet nur die Entscheidungsfrage — sie ist
**keine** Umsetzungs-Freigabe (S120-Befund).

**Session beenden + committen:**
> Bereite die nächste Session vor. Committen.

→ **Review** via Reviewer-Subagent (Opus, DoD + Sessionstand; Befund als Datei, Koordinator reicht
wortgleich durch) → **Retro** (getrennter Schritt, Koordinator moderiert) endet mit einer
**nummerierten, entscheidbaren Maßnahmen-Liste**; der Stakeholder wählt/gibt frei → **Abschluss**
schreibt nur das Freigegebene in die Artefakte: `next_session.md` aktualisieren (Stand, nächster
Schritt, neue Erkenntnisse) + `docs/goals/<aktives_ziel>.md` Checkboxen abhaken + Commit erstellen.
**Freigabe-Gate bleibt:** Plan + Dateiliste zeigen, auf explizite Freigabe warten — nur das "wer tut
die Arbeit" ist delegiert.

### Commit-Punkte
- Nach jeder abgeschlossenen, in sich sinnvollen Änderung auf Commit hinweisen
- Nachricht: kurz, imperativ, Englisch (`Add shooting phase UI`, `Fix slider crash`)
- Kein Commit mitten in einer halbfertigen Änderung

### Token-Disziplin & Arbeitsweise (PFLICHT)

Ziel: insgesamt effektives Arbeiten bei effizientem Tokenverbrauch — nicht Token-Nullsumme.

- **Vorab-Schätzung:** Jeder Plan nennt eine grobe Token-Schätzung pro Aufgabe.
- **Kontext-Korridor < 150k, zweistufig (S135-Retro-GO, präzisiert S136).** Ab **~120k**
  leitet der Koordinator ein **geordnetes Wind-down** ein (laufende Aufgabe abschließen,
  nichts Neues mehr beginnen). Bei **~90 % (~135k)** spätestens die Session **geordnet
  beenden** (`next_session.md` + Commit) und **frisch starten** — nicht in die teure
  >150k-Zone laufen. Messen: Der UserPromptSubmit-Hook `tools/session_context.py` zeigt den Live-
  Kontextstand **automatisch pro Turn** an und eskaliert ab ≥135k ⚠️⛔ Stopp —
  kein manuelles Rechnen nötig. Er liest die letzte `usage`-tragende
  Transcript-Zeile (`~/.claude/projects/<projekt>/<id>.jsonl`), parst sie **als ganzes
  JSON** und summiert `input_tokens + cache_creation_input_tokens +
  cache_read_input_tokens`. Wichtig: **nicht** mit `grep -o '"usage":{[^}]*}'` rechnen —
  das `usage`-Objekt verschachtelt Sub-Objekte (`server_tool_use`, `cache_creation`),
  der Regex trunkiert und liefert falsche Zahlen (S65-Befund). Peak-Kontext, Subagent-
  Anteil und Verlauf stehen zusätzlich in `docs/metrics/overview.md` (der pytest-Hook
  schreibt sie bei jedem Lauf) — dort prompt-frei nachlesen.
- **Tasks klein schneiden**, sodass *eine* Aufgabe sicher unter dem Korridor bleibt.
- **Subagent-Muster für Fleißarbeit:** mechanische, eindeutige Arbeit (viel Lesen,
  Entwürfe nach festgelegtem Format) an einen **Subagenten mit `model: sonnet`** geben —
  läuft im **isolierten Kontext**, hält das Opus-Hauptfenster schlank. Opus reviewt +
  finalisiert. Design/Mehrdeutiges bleibt bei Opus in der Hauptsession. **Jeder Auftrag
  enthält eine Selbstprüf-Checkliste** (u. a. Verdrahtung per `grep` belegen) — „Subagent-
  grün" ≠ „verdrahtet"; Details: `docs/governance/operating_model.md` Event 3 (Sprint).
- **Skill-/Claude-Inhalte über die API NUR per Subagent ziehen (PFLICHT):** Skill-Definitionen
  oder andere Inhalte über die Claude-/Skill-API **nie direkt im Opus-Hauptfenster** laden —
  immer einen Subagenten den Fetch machen lassen, der nur das Ergebnis zurückgibt. Direktes
  Laden kostete einmalig **~300k Token** und flutete den Kontext (S69-Befund, ADR-0004).
- **Tiering (MUST, O2):** Reine Lookups (gebundene Regelsuche, formatfixe Extraktion, ja/nein
  gegen expliziten Text) laufen als **Default mit `model: haiku`**. Eine Abweichung **nach oben**
  (Sonnet/Opus) braucht eine **explizite Begründung im Auftrag** — sonst Haiku. Tier im Chat
  transparent nennen. Je geschlossener das Konditionalprogramm → desto niedriger das Tier.
  Grund: ohne harten Default wird das Tiering ignoriert (S103). Vollständige Rollen-/Tier-/Modus-
  Regeln: `docs/governance/operating_model.md`.
- **Messung getrennt ausweisen:** Subagent-Verbrauch separat (Agent-`usage` bzw.
  `isSidechain` im Transcript). Subagent-Transcripts liegen in **eigener** Datei →
  `tools/token_report.py` führt beide Quellen zusammen (`--write` → `docs/metrics/overview.md`).
- **Subagenten = stehende Freigabe (PROAKTIV):** keine Einzel-Freigabe nötig — bei Fleißarbeit
  selbst einen Subagenten vorschlagen + starten (s. „Was NIEMALS ohne Freigabe"). Freigabe-Pflicht
  bleibt nur für **datei-/einstellungsändernde** Arbeit (Code/Memory/Skill) — auch via Subagent
  ([ADR-0005](docs/governance/decisions/0005-stehende-subagent-freigabe.md),
  [ADR-0006](docs/governance/decisions/0006-subagent-grossausgaben-als-datei.md)).
- **Dünner Koordinator (ADR-0007):** Detail-Planung + finales Review laufen als Subagenten; der
  Koordinator routet, hält Gates, liest nur **Pfade/Marker** — nicht volle Ergebnisse. Subagent↔
  Stakeholder asynchron über **Mailbox-Datei** (`docs/handoff/`, Marker `NEEDS-DECISION`/`ANSWERED`/
  `DONE`), Resumption per `SendMessage` (intakter Kontext). Scoping je Aufgabe über den Index
  `docs/reference/agent_scopes.md`. Verfassung: `docs/governance/operating_model.md` (ADR-0007, seit S102 verbindlich).
- **Kanal-Regel:** Inhaltliche Subagenten (Planner/Executor/Reviewer) kommunizieren mit dem
  Stakeholder NIE direkt im Chat, sondern über die Mailbox-Datei (`docs/handoff/`, Marker
  `NEEDS-DECISION`/`ANSWERED`/`DONE`) via Koordinator (operating_model.md, ADR-0007).

---

## Clean Code

- Bedeutungsvolle Namen — Name erklärt *Was*, Kommentar höchstens das *Warum*
- Funktionen tun **genau eine Sache**; keine magischen Zahlen/Strings
- Kein tiefes Verschachteln — Early Returns bevorzugen
- DRY: erst ab der **dritten** Wiederholung abstrahieren
- **Type Hints** überall; Formatter: `black` + `isort`; Linter: `ruff`
- **Kommentar-Konvention:** Code erklärt sich selbst (sprechende Namen, kleine
  Funktionen); Regel- und Design-Erklärungen gehören in die zuständige Spec unter
  `docs/spec/`, nicht in Kommentare. Erlaubt sind nur: (a) ein kurzer
  Verweis-Kommentar auf die Spec (`# → docs/spec/<datei>.md §<n>`), (b) ein
  *Warum*-Kommentar für nicht offensichtliche Entscheidungen (Gotchas,
  Regel-Randfälle) mit Quellenangabe. Docstrings bleiben für die öffentliche API,
  erzählen aber keine Spec nach. Abbau bestehender Erklär-Kommentare als Ratchet:
  bei jeder Modul-Berührung in die Spec verschieben — kein Big-Bang-Durchgang.

---

## Testing

### Messbefehl (IMMER so messen)

```bash
pytest --tb=short
```

Die Coverage-Konfiguration steht in `pyproject.toml` (`[tool.coverage.run]`). Sie schließt Streamlit-Render-Code aus, der keine eigenständige Business-Logik enthält (siehe unten). Der Gate liegt bei **99 %** auf dem so gemessenen Code — darunter schlägt der Build fehl. Gleiches Gate gilt im CI (`deploy.yml`).

### Regel-Abdeckung — Akzeptanz-Katalog (fachliches Sicherheitsnetz)

`docs/spec/acceptance/rules.md` ist der **Nenner**: die Gesamtheit der 9E-Regeln, gegen die
Implementierungs- und Test-Abdeckung als Prozent gemessen wird. Drei Klassen:
**A** (App rechnet/erzwingt), **B** (nur am Tisch prüfbar → App zeigt Hinweis),
**C** (Hybrid: App-Anteil + Tisch-Anteil). Konvention je Regel: `status`
(implementiert|offen), `getestet: ja — <testname>` | `nein`, `code: datei:funktion`
(keine Zeilennummern). Wächst **pro Bereich**, Granularität = **Mechanik-Schritt**.
Ziel-Gate (hart, sobald Ledger=0): jede `status: implementiert`-Regel hat einen Test —
`getestet: nein` bei `implementiert` ist eine **Schuld** (Ratchet → nur schrumpfen).

### Architektur-Gate — zweite messbare Schranke

Neben der Coverage prüft `tests/architecture/` vier Architektur-Invarianten (gameObjects
Streamlit-frei, YAML nur über Loader, Layer-Richtung, Generic-src). Bricht ein Wächter, bricht
der Build (läuft im normalen `pytest` mit). Schnellmessung: `pytest tests/architecture/ --no-cov -q`.
Status + Schulden-Ledger: `docs/spec/architecture_invariants.md`. Eine Invariante bewusst ändern
heißt: Wächter + Doku gemeinsam anpassen — nie still aufweichen.

### Sicherheitsnetz-Regel — PFLICHT

**Wenn nach einer Änderung vorher grüne Tests rot werden: STOP.**  
Nicht weitermachen, nicht den Test still anpassen. Dem Nutzer die failing Tests auflisten und explizit fragen, ob der Verhaltensbruch beabsichtigt war. Erst nach Bestätigung fortfahren.

Diese Regel ist der Hauptzweck der Tests: Ein fehlschlagender Test ist eine Nachricht aus einer früheren Session — „diese Funktionalität war bewusst so entworfen."

**Kein Commit mit roten Tests** — auch nicht als „temporärer Fix".

### Weitere Regeln

- Keine geteilten Zustände zwischen Tests — jeder Test vollständig isoliert
- Testnamen beschreiben Verhalten: `test_overlord_resurrection_orb_heals_destroyed_warrior` ✓
- Jeder Bugfix bekommt einen Regressionstest

### Warum Render-Code aus der Messung ausgeschlossen ist

Streamlit-Render-Funktionen (in `uiLayout/` und den `*Phase.py`-Dateien) sind technisch testbar. Sie werden aber aus der Coverage-Messung ausgeschlossen, weil Button-Order-Mocks bei jeder UI-Änderung brechen — hoher Aufwand, niedriger Informationsgewinn. Ihre Business-Logik (State-Mutationen, Berechnungen) ist in den direkt getesteten Modulen (`combat.py`, `unit_mutations.py`, `game_state.py` etc.) abgedeckt. Render-Code wird **manuell verifiziert** — wenn UI geändert wird, explizit nennen was zu prüfen ist; nie behaupten ein UI-Feature sei fertig ohne manuelle Prüfung.

---

## Streamlit CSS — Bekannte Selektoren (Streamlit 1.57)

Vor CSS-Overrides immer JS-Source prüfen:
```bash
find .venv -name "*.js" | xargs grep -l "<Komponentenname>" | head -3
# dann im Minified-JS nach data-testid suchen
```

| Komponente | Korrekte Selektoren |
|---|---|
| NumberInput Container | `[data-testid="stNumberInputContainer"]` |
| NumberInput Step-Buttons | `[data-testid="stNumberInputStepUp"]`, `[data-testid="stNumberInputStepDown"]` |
| Buttons allgemein | `button[data-testid="stBaseButton-{kind}"]` (nicht `baseButton-{kind}`) |
| Container `border=True` | `.e1rw0b1u3` (Emotion-Klasse — prüfen bei Streamlit-Update!) |
| Selectbox | `.stSelectbox [data-baseweb="select"] > div` |

`section[data-testid="stMain"]` ist der Scroll-Container der App (nicht `window`) —
Scroll-Sprünge entstehen durch Chrome Scroll-Anchoring bei Layout-Shifts oberhalb des
sichtbaren Bereichs → Fix: `overflow-anchor: none` auf `stMain` (B1-Fix S136, Beleg
`docs/handoff/S136_B1_probe.md`).

---

## Core Principles

| Principle | Description |
|-----------|-------------|
| **Simplicity First** | Make every change as simple as possible. Minimal code impact. |
| **No Laziness** | Find root causes. No temporary fixes. Senior developer standards. |
| **Minimal Impact** | Only touch what's necessary. No side effects with new bugs. |
| **No Placeholders — Ever** | Never write `...`, `TODO`, `<value>`, or any placeholder in deployed files. |
| **Generic src/** | Keine Fraktions-spezifische Logik in `src/` — alle Entscheidungen über Necrons, Orks etc. kommen aus den YAML-Daten. Hardcoded Fraktion-Checks in `src/` sind ein Bug. `src/`-Dateien werden regelmäßig auf versehentlich eingeschlichene Fraktions-Logik geprüft. |
