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

---

## Workflow-Regeln (PFLICHT)

### Freigabe vor Umsetzung
- **Niemals Code schreiben oder Dateien bearbeiten ohne vorherige explizite Freigabe**
- Vor jeder Umsetzung: Plan beschreiben + **alle betroffenen Dateien auflisten**
- Warten bis der Nutzer explizit zustimmt (z.B. „ja", „mach es", „ok")
- Ausnahme: expliziter „freier Lauf" für mehrere Schritte

### Was NIEMALS ohne explizite Freigabe passiert
Dieselbe Pflicht wie für Code gilt auch für:
- Memory-Einträge schreiben oder ändern
- Subagents starten
- Skills aufrufen, die Dateien oder Einstellungen ändern (z.B. `update-config`)

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
2. **Plan zeigen** → Freigabe einholen → Implementieren
3. **Session-Ende:** `.claude/tasks/next_session.md` aktualisieren (Stand, nächster Schritt, offene Fragen)
4. `docs/goals/<aktives_ziel>.md` Checkboxen abhaken

**Kritisch beim Update:** `.claude/tasks/next_session.md` ZUERST lesen, dann ergänzen — niemals blind überschreiben. Erkenntnisse aus früheren Sessions dürfen nicht verloren gehen. Keine zweite Datei anlegen (nicht im Root, nicht in `docs/`).

### Standard-Prompts (Kurzschrift)

**Session starten** (Plan aus `next_session.md` ist bereits freigegeben):
> Beginne mit der nächsten Session. Der Plan ist freigegeben.

→ `next_session.md` + Zieldatei lesen, direkt mit der ersten Aufgabe starten — kein erneuter Plan nötig.  
Ausnahme: Wenn der Nutzer zusätzlich ein konkretes Thema oder einen Bug nennt, hat dieses Vorrang.

**Session beenden + committen:**
> Bereite die nächste Session vor. Committen.

→ `next_session.md` aktualisieren (Stand, nächster Schritt, neue Erkenntnisse) + `docs/goals/<aktives_ziel>.md` Checkboxen abhaken + Commit erstellen.

### Commit-Punkte
- Nach jeder abgeschlossenen, in sich sinnvollen Änderung auf Commit hinweisen
- Nachricht: kurz, imperativ, Englisch (`Add shooting phase UI`, `Fix slider crash`)
- Kein Commit mitten in einer halbfertigen Änderung

---

## Clean Code

- Bedeutungsvolle Namen — Name erklärt *Was*, Kommentar höchstens das *Warum*
- Funktionen tun **genau eine Sache**; keine magischen Zahlen/Strings
- Kein tiefes Verschachteln — Early Returns bevorzugen
- DRY: erst ab der **dritten** Wiederholung abstrahieren
- **Type Hints** überall; Formatter: `black` + `isort`; Linter: `ruff`

---

## Testing

### Messbefehl (IMMER so messen)

```bash
pytest --tb=short
```

Die Coverage-Konfiguration steht in `pyproject.toml` (`[tool.coverage.run]`). Sie schließt Streamlit-Render-Code aus, der keine eigenständige Business-Logik enthält (siehe unten). Der Gate liegt bei **80 %** auf dem so gemessenen Code — darunter schlägt der Build fehl. Gleiches Gate gilt im CI (`deploy.yml`).

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

---

## Core Principles

| Principle | Description |
|-----------|-------------|
| **Simplicity First** | Make every change as simple as possible. Minimal code impact. |
| **No Laziness** | Find root causes. No temporary fixes. Senior developer standards. |
| **Minimal Impact** | Only touch what's necessary. No side effects with new bugs. |
| **No Placeholders — Ever** | Never write `...`, `TODO`, `<value>`, or any placeholder in deployed files. |
| **Generic src/** | Keine Fraktions-spezifische Logik in `src/` — alle Entscheidungen über Necrons, Orks etc. kommen aus den YAML-Daten. Hardcoded Fraktion-Checks in `src/` sind ein Bug. `src/`-Dateien werden regelmäßig auf versehentlich eingeschlichene Fraktions-Logik geprüft. |
