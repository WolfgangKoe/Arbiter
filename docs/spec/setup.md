# Setup — Spec

> Ziel 5a. Beschreibt den Setup-Screen und die Spielmodi (Matched / Open / Crusade).
> Crusade-Details: Ziel 6.

---

## Spielmodi

| Modus | Einheitenwahl | Punkte | CP | Crusade-Mechaniken |
|-------|--------------|--------|----|--------------------|
| **Matched Play** | Armeeliste (Punkte) | Pflicht | Detachment-Regeln | nein |
| **Open Play** | Beliebig | optional (Power Level) | fest: 3 CP | nein |
| **Crusade** | Crusade Roster | Versorgungslimit | wie Matched | ja (Ziel 6) |

---

## Matched Play

### Spielgrößen

| Größe | Punkte | Detachments | Start-CP |
|-------|--------|-------------|----------|
| Patrol | ≤ 500 | 1 | 3 |
| Incursion | 501–1000 | max. 2 | 6 |
| Strike Force | 1001–2000 | max. 3 | 12 |
| Onslaught | 2001–3000 | max. 4 | 18 |

Quelle: WH40k 9E Matched Play Regeln.

### CP-Regeln

- Start-CP wie in Tabelle oben (Spielgröße)
- +1 CP pro Runde zu Beginn der Befehlsphase (Battle-Forged Bonus)
- CP-Kosten für Stratagems werden aus dem Pool abgezogen

### Detachment-Regeln (Battle-Forged)

| Detachment | HQ | Troops | Elites | Fast Attack | Heavy Support | Flyer | Dedicated Transport | Lord of War |
|------------|----|----|--------|-------------|---------------|-------|---------------------|-------------|
| Patrol | 1–2 | 1–2 | 0–2 | 0–2 | 0–2 | 0–2 | 0–2 | — |
| Battalion | 2–3 | 3–6 | 0–6 | 0–3 | 0–3 | 0–2 | 0–3 | — |
| Brigade | 3–5 | 3–6 | 3–8 | 3–5 | 3–5 | 0–2 | 0–3 | — |
| Outrider | 1–2 | 0–3 | 0–3 | 3–6 | 0–3 | 0–2 | 0–2 | — |
| Spearhead | 1–2 | 0–3 | 0–3 | 0–3 | 3–6 | 0–2 | 0–2 | — |
| Vanguard | 1–2 | 0–3 | 3–6 | 0–3 | 0–3 | 0–2 | 0–2 | — |
| Super-Heavy | — | — | — | — | — | — | — | 1–3 |
| Super-Heavy Auxiliary | — | — | — | — | — | — | — | 1 |

Quelle: `data/wh40k_9e/_shared/detachment_types.yaml`

### Punkte-Validierung

- Roster-Gesamtpunkte müssen ≤ Spielgröße-Limit sein
- Der Setup-Screen zeigt Punkte-Zusammenfassung pro Detachment + Gesamt
- Überschreitung = Warnung (kein hartes Sperren — Open-Table-Freundlichkeit)

---

## Open Play

- Keine Punktebeschränkung
- Armeewahl: beliebige Einheiten aus dem Katalog
- Start-CP: fest 3 pro Spieler
- Power Level optional als Balancing-Hilfe (kein Enforcement in der App)
- Detachment-Regeln gelten nicht (kein Battle-Forged erforderlich)

---

## Crusade

Setup-Übersicht — Details in Ziel 6.

- Jeder Spieler hat ein **Crusade Roster** mit einem Versorgungslimit (Supply Limit)
- Einheiten haben **Crusade Points** (Erfahrung, Narben, Auszeichnungen)
- Vor dem Spiel: Einheiten aus dem Crusade Roster auf die **Order of Battle** wählen
- Punktlimit der Partie bestimmt Größe der Order of Battle
- Nach dem Spiel: Crusade Points vergeben, Narben/Auszeichnungen eintragen

---

## Setup-Screen — Flow

```
1. Spielmodus wählen (Matched / Open / Crusade)
   └── Matched: Spielgröße wählen → CP-Werte setzen
   └── Open: CP = 3 (fest)
   └── Crusade: Verweis auf Ziel 6

2. Spieler 1 Fraktion + Roster wählen
   └── Roster aus data/rosters/ laden (Dropdown)
   └── ODER: Fraktion direkt + alle Katalog-Einheiten laden (kein Roster)
   └── Unmatched-Warnung anzeigen falls vorhanden

3. Spieler 2 analog

4. Startspieler festlegen (first_player)
   └── Zufalls-Button oder manuell

5. "Spiel starten" → setup_complete = True, Runde 1, Befehlsphase
```

---

## session_state Setup-Felder

```python
{
    "game_type":    Literal["matched", "open", "crusade"],
    "game_size":    Literal["patrol", "incursion", "strike_force", "onslaught"] | None,
    "setup_complete": bool,
    "first_player": Literal["p1", "p2"],
}
```

Roster-Zuordnung:

```python
{
    "armies": {
        "p1": {
            "faction":    str,         # z.B. "Necrons"
            "subfaction": str | None,
            "roster_path": str | None, # Pfad zur Roster-YAML, None = alle Katalog-Einheiten
            ...
        },
        "p2": { ... }
    }
}
```

---

## Offene Fragen (Ziel 5e)

| # | Frage | Impact |
|---|-------|--------|
| 1 | Roster-Auswahl UI: Dropdown aus `data/rosters/` oder Datei-Upload? | setup screen |
| 2 | Soll Punkte-Validierung hard blocken oder nur warnen? | setup flow |
| 3 | Welche Detachment-Typen sollen initial unterstützt werden (alle 8 oder nur Patrol/Battalion)? | detachment_types.yaml |
| 4 | Startspieler-Würfel: soll das App-intern gewürfelt oder manuell gesetzt werden? | setup screen |
