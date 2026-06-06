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
1. **Session-Start:** `next_session.md` lesen → `docs/goals/<aktives_ziel>.md` lesen
2. **Plan zeigen** → Freigabe einholen → Implementieren
3. **Session-Ende:** `next_session.md` aktualisieren (Stand, nächster Schritt, offene Fragen)
4. `docs/goals/<aktives_ziel>.md` Checkboxen abhaken

**Kritisch beim `next_session.md`-Update:** Datei ZUERST lesen, dann ergänzen — niemals blind überschreiben. Erkenntnisse aus früheren Sessions dürfen nicht verloren gehen.

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

- Coverage-Schwelle: **80 %** — darunter wird der Build rot
- Keine geteilten Zustände zwischen Tests — jeder Test vollständig isoliert
- Testnamen beschreiben Verhalten: `test_overlord_resurrection_orb_heals_destroyed_warrior` ✓
- Jeder Bugfix bekommt einen Regressionstest
- **Streamlit-UI kann nicht automatisch getestet werden** — wenn UI geändert wird, explizit nennen was manuell verifiziert werden muss; nie behaupten ein UI-Feature sei fertig ohne manuelle Prüfung

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
