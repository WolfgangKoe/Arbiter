STATUS: AWAITING-VERIFICATION

# S163 — B-028b-Rest UI-Verifikation: Gloom Prism Deny-Karte

**Lebensdauer:** temporär — löschen nach Stakeholder-Sichtprüfung (Marker → `ANSWERED`/`DONE`,
Ergebnis im selben Abschluss in `docs/goals/backlog.md`/`backlog_details.md` überführen, dann
diese Datei löschen).

**Kontext:** `gloom_prism` (Canoptek Spyder) wurde von der alten Wargear-Namens-Gate
(`load_deny_wargear_names`) auf die B-028a-Ability-Infrastruktur migriert — exakt dasselbe Muster
wie Szarekhs Noctilith Beacons (B-028b, S160 bereits verifiziert). Neuer Datenpfad:
`data/wh40k_9e/necrons/unit_abilities.yaml` (`wh40k_9e.necrons.unit.canoptek_spyder.gloom_prism`,
`effect.type: deny_psychic`) → `find_unit_ability_by_effect` → `_render_deny_ability_cards`
(`src/gameMechanic/psychicPhase.py`) rendert additiv eine reaktive GO-Karte. Render-Code ist von
der Coverage-Messung ausgenommen (CLAUDE.md) → manuelle Prüfung nötig.

## Voraussetzungen

- Roster `data/rosters/necrons_beta.yaml` geladen (enthält `gloom_prism` als Wargear-Zeile 18) —
  Canoptek Spyder ist in der Necron-Armeeliste vorhanden.
- Gegner-Fraktion mit einem PSYKER (z. B. Orks Weirdboy) für einen Manifest-Versuch.

## Klickpfad

1. App starten (`streamlit run src/app.py`), beide Rosters laden, in die Psychic Phase wechseln.
2. Auf der aktiven Seite (Orks) den Weirdboy selektieren, Smite versuchen (2D6-Eingabe ≥ 5,
   z. B. 8), „Attempt Manifest" klicken.
3. Auf der Necron-Seite (inaktiv, Deny-Spalte) beobachten: die Deny-Spalte soll jetzt eine
   zusätzliche GO-Karte zeigen, **bevor** das Deny-Roll-UI erscheint.

## Erwartung

- Eine reaktive GO-Karte mit dem Titel „Gloom Prism" erscheint additiv in der Deny-Spalte, Ziel
  „Canoptek Spyder", Rule-Text „…may attempt to deny as if it were a PSYKER." (identisches
  Karten-Layout wie Szarekhs Noctilith-Beacons-Karte, S160 bereits abgenommen).
- Das bestehende Deny-Roll-Eingabefeld darunter bleibt **unverändert** funktionsfähig — die Karte
  ist additiv (Use/Undo), blockiert den Roll-UI-Pfad nicht (identisch zum Noctilith-Verhalten).
- Kein doppeltes Rendering: nur eine Gloom-Prism-Karte, kein zusätzlicher Chip/Hinweistext (D-1
  Entscheidung Variante A — die Karte selbst löst B-119 Fall b, kein separater Quellen-Chip nötig).

## Ergebnis (Stakeholder trägt hier ein)

— positiv
