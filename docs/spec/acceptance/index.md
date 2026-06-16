# Akzeptanzkriterien — Registry

> Format + Gate: siehe [README.md](README.md). Jede `### AC-…`-Überschrift wird
> von `tests/acceptance/` angepinnt. IDs sind stabil — nie wiederverwenden.

---

## Bereich: Subfaction- & Faktion-Badge (Finding #1)

Quelle: `gameMechanic/game_state.subfaction_badge_for` /
`faction_display_name_for`; Farben: `docs/spec/design_colors.md` §2a.
Grundregel: Das Subfaction-Badge wird **immer** gerendert — nie unsichtbar.

### AC-SUBFACTION-01
- **Given** ein Spieler der Fraktion `necrons`, dessen Roster `dynasty: szarekhan` setzt
- **When** `subfaction_badge_for` aufgerufen wird
- **Then** `state == "set"` und `text == "Szarekhan"` (Title-Case des Roster-Werts)

### AC-SUBFACTION-02
- **Given** ein Spieler der Fraktion `orks`, dessen Roster `clan: bad_moons` setzt
- **When** `subfaction_badge_for` aufgerufen wird
- **Then** `state == "set"` und `text == "Bad Moons"` (generisch, anderes Roster-Feld)

### AC-SUBFACTION-03
- **Given** ein Spieler der Fraktion `necrons`, dessen Roster **keine** Dynastie setzt
- **When** `subfaction_badge_for` aufgerufen wird
- **Then** `state == "missing"` und `text == "No Dynasty"` (sichtbarer Platzhalter, keine Buffs)

### AC-SUBFACTION-04
- **Given** ein Spieler, dessen Fraktion **kein** `subfaction_field` deklariert (Datenlücke)
- **When** `subfaction_badge_for` aufgerufen wird
- **Then** `state == "error"` und `text == "No Subfaction"` (sichtbares Fehler-Badge)

### AC-SUBFACTION-05
- **Given** ein Spieler der Fraktion `necrons` (Roster-Anzeigename ist beliebig)
- **When** `faction_display_name_for` aufgerufen wird
- **Then** Ergebnis `== "Necrons"` (Faktion-Anzeigename aus YAML, **nicht** der Roster-Titel)
