# Plan 004: `lookup()` wirft klare Fehlermeldung statt nacktem `StopIteration`

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `docs/audit/plans/README.md`.
>
> **Drift check (run first)**:
> `git diff --stat c5bc891..HEAD -- src/uiLayout/_common.py`
> Wenn die unten zitierte `lookup`-Funktion vom Live-Code abweicht: STOP.

## Status

- **Priority**: P2
- **Effort**: S
- **Risk**: LOW
- **Depends on**: 001 (empfohlen — Verifikations-Gates; technisch nicht zwingend)
- **Category**: bug
- **Planned at**: commit `c5bc891`, 2026-06-11

## Why this matters

`lookup()` löst die `Unit` zu einem State-Key auf. Es nutzt `next(generator)` **ohne
Default**: passt kein Unit zur ID, wirft Python ein nacktes `StopIteration`. In Streamlit
erscheint das als generischer, kontextloser Fehler — schwer zu debuggen. Der Fall tritt
auf, wenn Session-State und geladener Unit-Katalog divergieren (z. B. Roster mitten im
Spiel neu geladen, verwaister State-Key). Dieser Plan ersetzt den nackten Crash durch
eine **explizite, aussagekräftige** Exception, die das Problem benennt.

## Current state

Datei `src/uiLayout/_common.py`, Zeilen 160–170:

```python
def lookup(faction: str, uid: str) -> tuple[Unit, dict]:  # type: ignore[type-arg]
    """Return (Unit, unit_state_dict) for the given faction + state_key (uid).

    uid may be a bare unit ID or a deduplicated state key ('unit.id#N').
    """
    from gameMechanic.game_state import unit_id_from_state_key

    unit_id = unit_id_from_state_key(uid)
    units = units_list_for(faction)
    unit = next(u for u in units if u.id == unit_id)   # ← Zeile 169: kein Default
    return unit, st.session_state[units_key_for(faction)][uid]
```

`units_list_for` und `units_key_for` sind in derselben Datei verfügbar (oben importiert
bzw. definiert). `unit_id_from_state_key` wird funktions-lokal importiert (Repo-Konvention).

Bestehende Tests: `tests/uiLayout/test_common.py` mockt Streamlit komplett
(`sys.modules["streamlit"] = MagicMock()`), testet aber bisher `lookup` nicht.

## Commands you will need

| Zweck   | Befehl | Erwartet |
|---------|--------|----------|
| venv    | `source .venv/bin/activate` | `(.venv)` |
| Lint    | `ruff check src/` | passt |
| Tests   | `python -m pytest tests/uiLayout/test_common.py -q` | grün |
| Vollsuite | `python -m pytest tests/ -q` | grün |

## Scope

**In scope**:
- `src/uiLayout/_common.py` — nur die Funktion `lookup` (Zeilen 160–170)
- `tests/uiLayout/test_common.py` — Regressionstest ergänzen

**Out of scope** (NICHT anfassen):
- Andere `next(...)`-Aufrufe im Repo.
- Die Aufrufer von `lookup` — ihr Verhalten bleibt gleich (Exception statt Exception,
  nur klarer). Kein Aufrufer soll auf einen `None`-Rückgabewert umgestellt werden.

## Git workflow

- Branch: `advisor/004-lookup-stopiteration-fallback`.
- Commit-Stil imperativ Englisch, z. B. `Raise clear error when lookup finds no unit`.
- Nicht pushen/PR ohne Anweisung.

## Steps

### Step 1: Default + explizite Exception einbauen

Ersetze in `lookup` die Zeile 169 durch eine Variante mit Default und klarer Meldung:

```python
    unit = next((u for u in units if u.id == unit_id), None)
    if unit is None:
        raise KeyError(
            f"No unit with id {unit_id!r} in catalog for faction {faction!r} "
            f"(state key {uid!r}). Session state and unit catalog are out of sync."
        )
```

Der Rückgabewert-Typ `tuple[Unit, dict]` bleibt korrekt: nach dem `raise` ist `unit`
garantiert ein `Unit`. Die zweite Zeile (`return unit, st.session_state[...][uid]`)
bleibt unverändert.

**Verify**: `grep -n "out of sync" src/uiLayout/_common.py` → 1 Treffer;
`ruff check src/` → passt.

### Step 2: Regressionstest

Ergänze in `tests/uiLayout/test_common.py` einen Test, der belegt, dass eine unbekannte
ID einen `KeyError` (mit erklärender Meldung) wirft — **nicht** `StopIteration`. Da
Streamlit gemockt ist, patche `units_list_for` und `unit_id_from_state_key`, sodass die
`next`-Suche erreicht wird, bevor `st.session_state` zum Tragen kommt:

```python
from types import SimpleNamespace

import uiLayout._common as common


def test_lookup_raises_keyerror_for_unknown_unit(monkeypatch) -> None:
    fake_units = [SimpleNamespace(id="known.unit")]
    monkeypatch.setattr(common, "units_list_for", lambda faction: fake_units)
    monkeypatch.setattr(
        "gameMechanic.game_state.unit_id_from_state_key", lambda uid: "missing.unit"
    )
    with pytest.raises(KeyError, match="out of sync"):
        common.lookup("Necrons", "missing.unit")
```

Stelle sicher, dass `import pytest` oben in der Testdatei vorhanden ist (sonst ergänzen).

**Verify**: `python -m pytest tests/uiLayout/test_common.py -q` → grün inkl. neuem Test.

### Step 3: Gesamte Suite

**Verify**: `python -m pytest tests/ -q` → alle grün.

## Test plan

- Neuer Test `test_lookup_raises_keyerror_for_unknown_unit` in `tests/uiLayout/test_common.py`:
  unbekannte ID → `KeyError` mit „out of sync"; **kein** `StopIteration`.
- Strukturvorlage: bestehende Tests derselben Datei (Streamlit-Mock-Setup); `monkeypatch`
  für `units_list_for` und `unit_id_from_state_key`.
- Verifikation: `python -m pytest tests/uiLayout/test_common.py -q` → grün.

## Done criteria

ALLE müssen gelten:

- [ ] `grep -n "next((u for u in units if u.id == unit_id), None)" src/uiLayout/_common.py` → 1 Treffer
- [ ] `grep -n "out of sync" src/uiLayout/_common.py` → 1 Treffer
- [ ] Neuer Test vorhanden und grün; Test prüft auf `KeyError`, nicht `StopIteration`
- [ ] `python -m pytest tests/ -q` → alle grün
- [ ] `ruff check src/` → passt
- [ ] Keine Dateien außerhalb der In-scope-Liste geändert (`git status`)
- [ ] Status-Zeile in `docs/audit/plans/README.md` aktualisiert

## STOP conditions

Stoppen und zurückmelden, wenn:

- Die `lookup`-Funktion im Live-Code anders aussieht als der zitierte Auszug.
- Der Test sich nicht ohne echtes Streamlit-Runtime schreiben lässt (z. B. `units_list_for`
  ist nicht als modulglobaler Name in `_common` patchbar) — melde das, statt das
  Test-Setup grundlegend umzubauen.
- Ein Aufrufer von `lookup` sich auf das alte (Crash-)Verhalten verlässt und nun bricht —
  unwahrscheinlich, aber dann melden.

## Maintenance notes

- Die saubere Langfrist-Lösung wäre, verwaiste State-Keys an den Phasengrenzen aktiv zu
  bereinigen (statt nur beim Zugriff zu scheitern) — bewusst aus diesem Plan ausgeklammert
  (Audit-Finding #4 nennt das als optionale Erweiterung).
- Reviewer: prüfen, dass die Exception-Meldung keine Geheimnisse/Pfade leakt (tut sie nicht —
  nur IDs und Fraktionsname).
