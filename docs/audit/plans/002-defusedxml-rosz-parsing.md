# Plan 002: `.rosz`/`.ros`-Parsing gegen XML-Entity-Expansion härten

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `docs/audit/plans/README.md`.
>
> **Drift check (run first)**:
> `git diff --stat c5bc891..HEAD -- src/gameObjects/rosz_importer.py requirements.txt`
> Wenn eine dieser Dateien seit dem Planungs-Commit geändert wurde, vergleiche die
> "Current state"-Auszüge mit dem Live-Code, bevor du fortfährst; bei Abweichung
> STOP.

## Status

- **Priority**: P1
- **Effort**: S
- **Risk**: LOW
- **Depends on**: none
- **Category**: security
- **Planned at**: commit `c5bc891`, 2026-06-11

## Why this matters

Arbiter ist öffentlich auf Hugging Face Spaces deployt und nimmt vom Nutzer
hochgeladene BattleScribe-`.rosz`/`.ros`-Dateien entgegen (`st.file_uploader`).
Diese werden mit der Standard-Bibliothek `xml.etree.ElementTree` geparst. Stdlib-
ElementTree ist laut Python-Dokumentation gegen Entity-Expansion-Angriffe
(„billion laughs" / quadratic blowup) verwundbar: Eine kleine, präparierte XML-Datei
kann beim Parsen Speicher und CPU erschöpfen und den Space-Prozess lahmlegen (DoS).
Das 5-MB-Größenlimit verhindert das nicht. Die etablierte Abhilfe ist `defusedxml`,
das die Parser-Eintrittspunkte ersetzt, ohne die übrige Element-API zu ändern.

## Current state

Datei `src/gameObjects/rosz_importer.py`:

- Zeile 10: `import xml.etree.ElementTree as ET`
- Der einzige Parse-Eintrittspunkt ist `_validate_and_parse_xml` (Zeilen 147–151):
  ```python
  def _validate_and_parse_xml(data: bytes) -> ET.Element:
      root = ET.fromstring(data)
      if _BS_NS not in root.tag:
          raise ValueError(f"Not a BattleScribe roster (unexpected root namespace: {root.tag!r})")
      return root
  ```
- Aufgerufen aus `parse_rosz_bytes` (Zeile 166) und `parse_ros_bytes` (Zeile 174).
- `ET.Element` wird zusätzlich als **Typ-Annotation** in vielen Signaturen genutzt
  (z. B. `_extract_units(root: ET.Element)`, `_collect_upgrade_names(element: ET.Element, ...)`).
  → `import xml.etree.ElementTree as ET` muss als Typ-Import **bleiben**; nur der
  `fromstring`-**Aufruf** wird auf den sicheren Parser umgestellt.

`requirements.txt` enthält aktuell nur:
```
streamlit>=1.57
pyyaml>=6.0
```
`defusedxml` ist **nicht** installiert (lokal verifiziert: `import defusedxml` schlägt fehl).

Bestehende Tests: `tests/gameObjects/test_rosz_importer.py` (Importer-Tests, gute Vorlage
für Struktur und sys.path-Setup).

## Commands you will need

| Zweck   | Befehl                                                | Erwartet |
|---------|-------------------------------------------------------|----------|
| venv    | `source .venv/bin/activate`                           | `(.venv)` |
| Install | `pip install defusedxml`                              | exit 0 (lokal, zum Testen) |
| Tests   | `python -m pytest tests/gameObjects/test_rosz_importer.py -q` | grün |
| Vollsuite | `python -m pytest tests/ -q`                        | grün |
| Grep    | `grep -n "ET.fromstring" src/gameObjects/rosz_importer.py` | nach Fix: keine Treffer |

## Scope

**In scope** (nur diese Dateien ändern):
- `requirements.txt` — `defusedxml` ergänzen
- `src/gameObjects/rosz_importer.py` — nur den `fromstring`-Aufruf umstellen
- `tests/gameObjects/test_rosz_importer.py` — Regressionstest ergänzen

**Out of scope** (NICHT anfassen):
- Die `ET.Element`-Typ-Annotationen — bleiben unverändert.
- Die Zip-Behandlung in `parse_rosz_bytes` (kein `extractall`, kein Schreibpfad — bereits sicher).
- `tools/import_rosz.py` und die Scraper-Tools.

## Git workflow

- Branch: `advisor/002-defusedxml-rosz-parsing`.
- Commit-Stil imperativ Englisch, z. B. `Harden rosz XML parsing with defusedxml`.
- Nicht pushen/PR ohne Anweisung.

## Steps

### Step 1: `defusedxml` als Dependency

Ergänze in `requirements.txt` die Zeile `defusedxml>=0.7` (nach `pyyaml>=6.0`).
Installiere lokal zum Testen: `pip install defusedxml`.

**Verify**: `python -c "import defusedxml; print('ok')"` → `ok`.

### Step 2: Sicheren Parser im Parse-Eintrittspunkt verwenden

Füge in `src/gameObjects/rosz_importer.py` nach der bestehenden Zeile 10 einen
zusätzlichen Import hinzu (der stdlib-Import bleibt für die Typen erhalten):

```python
import xml.etree.ElementTree as ET
from defusedxml.ElementTree import fromstring as _safe_fromstring
```

Ersetze in `_validate_and_parse_xml` die Zeile `root = ET.fromstring(data)` durch:

```python
    root = _safe_fromstring(data)
```

Lass alles andere (Namespace-Prüfung, `ET.Element`-Typen) unverändert.

**Verify**: `grep -n "ET.fromstring" src/gameObjects/rosz_importer.py` → **keine Treffer**.
`grep -n "_safe_fromstring" src/gameObjects/rosz_importer.py` → genau zwei Treffer
(Import + Aufruf).

### Step 3: Regressionstest für Entity-Expansion

Ergänze in `tests/gameObjects/test_rosz_importer.py` einen Test, der belegt, dass eine
„billion laughs"-Nutzlast eine Exception auslöst (statt zu hängen/expandieren). Modelliere
das sys.path-/Import-Setup nach den bestehenden Tests in derselben Datei. Beispiel:

```python
import pytest
from gameObjects.rosz_importer import parse_ros_bytes

_BILLION_LAUGHS = b"""<?xml version="1.0"?>
<!DOCTYPE lolz [
  <!ENTITY lol "lol">
  <!ENTITY lol2 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
  <!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;">
]>
<roster xmlns="http://www.battlescribe.net/schema/rosterSchema">&lol3;</roster>"""


def test_parse_ros_rejects_entity_expansion() -> None:
    # defusedxml muss die Entity-Definition ablehnen, statt sie zu expandieren.
    with pytest.raises(Exception):
        parse_ros_bytes(_BILLION_LAUGHS)
```

Hinweis: `defusedxml` wirft hier typischerweise `defusedxml.common.EntitiesForbidden`.
Der Test prüft bewusst nur „eine Exception, kein Hängen / keine Expansion" — das genügt
als Regressionsschutz und bleibt robust gegenüber dem genauen Exception-Typ.

**Verify**: `python -m pytest tests/gameObjects/test_rosz_importer.py -q` → grün,
inklusive des neuen Tests; der Test-Lauf terminiert sofort (kein Hängen).

### Step 4: Gesamte Suite grün

**Verify**: `python -m pytest tests/ -q` → alle grün (594 + 1 neuer Test zum
Planungszeitpunkt).

## Test plan

- Neuer Test in `tests/gameObjects/test_rosz_importer.py`:
  `test_parse_ros_rejects_entity_expansion` — präparierte Entity-Nutzlast → Exception.
- Strukturvorlage: bestehende Tests in derselben Datei (sys.path-Setup, Importweg).
- Verifikation: `python -m pytest tests/gameObjects/test_rosz_importer.py -q` → alle grün.

## Done criteria

ALLE müssen gelten:

- [ ] `grep -n defusedxml requirements.txt` → Treffer
- [ ] `grep -n "ET.fromstring" src/gameObjects/rosz_importer.py` → **keine** Treffer
- [ ] `grep -n "_safe_fromstring" src/gameObjects/rosz_importer.py` → 2 Treffer
- [ ] Neuer Test `test_parse_ros_rejects_entity_expansion` existiert und ist grün
- [ ] `python -m pytest tests/ -q` → alle grün
- [ ] Keine Dateien außerhalb der In-scope-Liste geändert (`git status`)
- [ ] Status-Zeile in `docs/audit/plans/README.md` aktualisiert

## STOP conditions

Stoppen und zurückmelden, wenn:

- `defusedxml.ElementTree.fromstring` valide BattleScribe-`.ros`-Dateien nicht mehr
  parst (bestehende Importer-Tests werden rot) — dann ist mehr als nur der Parser-Tausch
  nötig.
- Der Entity-Test **hängt** statt eine Exception zu werfen — sofort abbrechen und melden
  (deutet darauf hin, dass der sichere Parser nicht greift).
- `ET.fromstring` taucht an weiteren Stellen auf, die nicht in „Current state" beschrieben
  sind — Codebase ist gedriftet.

## Maintenance notes

- Falls künftig weitere XML-Eintrittspunkte hinzukommen (z. B. anderes Import-Format),
  müssen auch sie `_safe_fromstring` / `defusedxml` nutzen, nicht `ET.fromstring`.
- Reviewer: prüfen, dass der stdlib-`ET`-Import nur noch für Typ-Annotationen dient und
  kein Parse-Aufruf mehr darüber läuft.
- `defusedxml` deaktiviert externe Entities/DTDs vollständig — sollte ein legitimes
  Roster jemals eine DTD benötigen (unwahrscheinlich bei BattleScribe), in Review klären.
