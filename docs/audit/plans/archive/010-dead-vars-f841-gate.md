# Plan 010: Tote Variablen entfernen und das F841-Lint-Gate scharf schalten

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `docs/audit/plans/README.md`.
>
> **Drift check (run first)**:
> `git diff --stat 225d13b..HEAD -- src/uiLayout/_common.py src/gameMechanic/combat.py pyproject.toml`
> Wenn sich die Dateien geändert haben, prüfe zuerst, ob die 5 unten gelisteten
> Fundstellen noch existieren:
> `ruff check src/ --select F841 --config "lint.per-file-ignores={}" --no-cache`
> Erwartet: genau die 5 gelisteten Treffer. Bei Abweichung: Liste anpassen und
> melden, bei strukturellen Überraschungen STOP.

## Status

- **Priority**: P2
- **Effort**: S
- **Risk**: LOW
- **Depends on**: none — aber VOR Plan 008 ausführen (der verschiebt Code, in dem
  eine der Leichen liegt)
- **Category**: dx / bug
- **Planned at**: commit `225d13b`, 2026-06-11

## Why this matters

`pyproject.toml` ignoriert die ruff-Regel **F841** („local variable assigned but
never used") pauschal für ganz `src/`. Dadurch ist der Linter strukturell blind
für genau die Restmüll-Klasse, die Refactorings hinterlassen — und das ist bereits
passiert: Die WAAAGH-Zentralisierung (Plan 003, Commit `8f81293`) hat an allen
drei Call-Sites die alte `waaagh`-Zuweisung stehen lassen. Insgesamt finden sich
5 tote Variablen, davon eine mit echtem Bug-Verdacht: `combat.py` berechnet
`hit_mod` (Hit-Modifier inkl. MWBD, gekappt auf ±1), und der Docstring verspricht
„capped at ±1 **(logged**, not enforced on input)" — der Wert landet aber nie im
Log. Dieser Plan räumt die 5 Stellen auf und entfernt `F841` aus den
per-file-ignores, damit der Fall nicht wieder eintritt.

## Current state

`pyproject.toml`, Zeilen 16–17:

```toml
[tool.ruff.lint.per-file-ignores]
"src/*" = ["E501", "F841"]
```

Die 5 Fundstellen (verifiziert via
`ruff check src/ --select F841 --config "lint.per-file-ignores={}" --no-cache`):

**1.–3. `src/uiLayout/_common.py:1447, 1560, 1797`** — identisches Muster,
Reste der Plan-003-Zentralisierung. Die Variable `waaagh` wird zugewiesen und
nie verwendet; die Folgezeilen nutzen nur noch `waaagh_attack_bonus(...)`:

```python
    waaagh = st.session_state.get("waaagh_state", {}).get(atk_faction)   # ← tot
    from gameMechanic.ability_engine import waaagh_attack_bonus  # noqa: PLC0415

    waaagh_bonus = waaagh_attack_bonus(atk_faction, atk_unit)
```

**4. `src/uiLayout/_common.py:861`** — in `_render_dice_save_block`:

```python
    armour_eff = save["armour_eff"]
    invuln = save["invuln"]
    effective = save["effective"]          # ← tot
    using_invuln = save["using_invuln"]
```

**5. `src/gameMechanic/combat.py:105`** — in `resolve_attack`; Docstring der
Funktion (Zeile ~98) sagt: „hit_modifier and wound_modifier capped at ±1
(logged, not enforced on input)":

```python
    # Hit phase
    hit_mod = min(1, max(-1, params.hit_modifier + (1 if params.mwbd_active else 0)))  # ← berechnet, nie genutzt
    mwbd_note = " (MWBD +1)" if params.mwbd_active else ""
    log.append(f"Hits: {hits_rolled}{mwbd_note} — skill {params.skill}+")
```

Kein Test asserted die exakte „Hits:"-Logzeile
(`grep -rn '"Hits:' tests/` → 0 Treffer).

Hinweis: `E501` bleibt in den ignores (20 bestehende Verstöße; separate
Entscheidung, nicht Teil dieses Plans).

## Commands you will need

| Zweck | Befehl | Erwartet |
|-------|--------|----------|
| venv | `source .venv/bin/activate` | `(.venv)` |
| F841-Kontrolle | `ruff check src/ --select F841 --no-cache` | nach dem Fix: passt |
| Lint komplett | `ruff check src/ && black --check src/ && isort --check-only src/` | passt |
| Combat-Tests | `python -m pytest tests/gameMechanic/test_combat.py -q` | grün (Datei ggf. anders benannt — `ls tests/gameMechanic/`) |
| Vollsuite + Coverage | `pytest --tb=short` | grün, ≥80 % |

## Scope

**In scope**:
- `src/uiLayout/_common.py` — nur die 4 toten Zuweisungen (Zeilen 1447, 1560, 861, 1797)
- `src/gameMechanic/combat.py` — `hit_mod` ins Log aufnehmen (Zeilen ~104–107)
- `pyproject.toml` — `F841` aus den per-file-ignores entfernen
- ggf. Test-Ergänzung für die neue Logzeile (siehe Test plan)

**Out of scope** (NICHT anfassen):
- `E501` in den per-file-ignores — bleibt.
- Die `# noqa: PLC0415`-Kommentare und Funktions-lokalen Imports — Repo-Konvention.
- Jede inhaltliche Änderung an der Kampflogik — `hit_mod` wird NUR geloggt,
  nirgends verrechnet (die Hits sind vom Nutzer bereits gewürfelt).

## Git workflow

- Branch: `advisor/010-dead-vars-f841`.
- Commit-Stil imperativ Englisch, z. B. `Remove dead locals and enforce F841 in src`.
- Nicht pushen/PR ohne Anweisung.

## Steps

### Step 1: Die 4 toten Zuweisungen in `_common.py` löschen

An den Zeilen 1447, 1560 und 1797 jeweils NUR die Zeile
`waaagh = st.session_state.get("waaagh_state", {}).get(atk_faction)` entfernen
(Import-Zeile und `waaagh_bonus`-Zeile bleiben). In Zeile 861 die Zeile
`effective = save["effective"]` entfernen.

**Verify**:
`grep -n 'waaagh = st.session_state' src/uiLayout/_common.py` → 0 Treffer;
`grep -c 'effective = save\["effective"\]' src/uiLayout/_common.py` → 0;
`python -m pytest tests/uiLayout/ -q` → grün.

### Step 2: `hit_mod` in `combat.py` ins Log aufnehmen

Ersetze die Hits-Logzeile so, dass der Modifier nur bei ≠ 0 erscheint
(Default-Ausgabe bleibt byte-identisch — kein bestehendes Verhalten ändert sich):

```python
    hit_mod = min(1, max(-1, params.hit_modifier + (1 if params.mwbd_active else 0)))
    mwbd_note = " (MWBD +1)" if params.mwbd_active else ""
    mod_note = f" (hit mod {hit_mod:+d})" if hit_mod else ""
    log.append(f"Hits: {hits_rolled}{mwbd_note}{mod_note} — skill {params.skill}+")
```

Damit hält der Code, was der Docstring verspricht („logged, not enforced").

**Verify**: `python -m pytest tests/gameMechanic/ -q` → grün.

### Step 3: F841-Gate scharf schalten

In `pyproject.toml`:

```toml
[tool.ruff.lint.per-file-ignores]
"src/*" = ["E501"]
```

**Verify**: `ruff check src/ --no-cache` → passt (0 Fehler — beweist, dass alle
5 Stellen erwischt wurden und keine weiteren existieren).

### Step 4: Regressionstest für die Logzeile

Ergänze in der Combat-Testdatei (`ls tests/gameMechanic/` — die Datei, die
`resolve_attack` bereits testet; deren bestehende Tests als Strukturvorlage):

```python
def test_resolve_attack_logs_hit_modifier_when_nonzero() -> None:
    # params mit hit_modifier=1 bauen (bestehende Test-Factory/Fixtures nutzen)
    ...
    assert any("hit mod +1" in line for line in log)


def test_resolve_attack_log_unchanged_without_modifier() -> None:
    ...
    assert not any("hit mod" in line for line in log)
```

Nutze die in der Datei vorhandenen Hilfskonstrukte zum Erzeugen von
`params`/`defender` — KEINE neuen Fixtures erfinden, wenn welche da sind.

**Verify**: `python -m pytest tests/gameMechanic/ -q` → grün inkl. 2 neuer Tests.

### Step 5: Vollsuite

**Verify**: `pytest --tb=short` → alle Tests grün (Baseline bei Plan-Erstellung 767,
+2 neue aus diesem Plan; durch andere abgeschlossene Pläne kann die Zahl höher liegen),
Coverage ≥ 80 %.

## Test plan

- `test_resolve_attack_logs_hit_modifier_when_nonzero`: `hit_modifier=1` →
  Logzeile enthält `hit mod +1`.
- `test_resolve_attack_log_unchanged_without_modifier`: ohne Modifier → kein
  `hit mod` im Log (beweist Byte-Identität des Default-Outputs).
- Alle bestehenden Tests grün — insbesondere kein Test asserted die alte
  „Hits:"-Zeile (vorab verifiziert).

## Done criteria

ALLE müssen gelten:

- [ ] `grep -n '"F841"' pyproject.toml` → 0 Treffer
- [ ] `ruff check src/ --no-cache` → passt (mit F841 aktiv)
- [ ] `grep -n "mod_note" src/gameMechanic/combat.py` → 2 Treffer (Definition + Verwendung)
- [ ] 2 neue Tests vorhanden und grün
- [ ] `pytest --tb=short` → alle grün, Coverage-Gate erfüllt
- [ ] `black --check src/ && isort --check-only src/` → passt
- [ ] Keine Dateien außerhalb der In-scope-Liste geändert (`git status`)
- [ ] Status-Zeile in `docs/audit/plans/README.md` aktualisiert

## STOP conditions

Stoppen und zurückmelden, wenn:

- `ruff check src/ --no-cache` nach Step 3 MEHR Fehler meldet als die bekannten 5
  Stellen erklärbar machen — dann sind seit Plan-Erstellung neue F841-Verstöße
  dazugekommen; auflisten und melden statt blind löschen (eine „ungenutzte"
  Variable kann ein vergessener Bug sein, siehe `hit_mod`).
- Ein bestehender Test durch Step 2 rot wird (asserted doch jemand die Logzeile?)
  — Repo-Regel: rote Tests = STOP, Nutzer fragen.
- Eine der 4 `_common.py`-Zeilen anders aussieht als zitiert (Drift durch
  parallel gelaufene Pläne) — Funktionsnamen prüfen, melden.

## Maintenance notes

- Ab jetzt schlägt CI bei toten Variablen in `src/` fehl — wer absichtlich einen
  Wert verwerfen will, nutzt `_` als Namen oder ein gezieltes `# noqa: F841`
  mit Begründung.
- `E501` (20 Verstöße) bleibt bewusst ignoriert — separates, rein kosmetisches
  Thema; bei Gelegenheit mit `black`-Zeilenlänge harmonisieren.
- Plan 008 verschiebt `_render_dice_save_block` nach `dice_html.py` — dieser
  Plan muss daher VORHER laufen, sonst wandert die `effective`-Leiche mit um.
