# Startprompt — Nächste Session
<!-- Kanonische Planung. Nicht durch separate Plan-Dateien ersetzen — immer hier ergänzen. -->

## Was ist Arbiter?

**Arbiter** ist ein digitaler Spielbegleiter für Warhammer 40.000 9. Edition, gebaut in Streamlit (Python).
Starten: `streamlit run src/app.py` (Port fest: 8501)
Branch: `dev` (Entwicklung), `main` (stabiler Stand, nur per PR)

---

## Was in dieser Session passiert ist

**Ziel 5c war abgeschlossen — in dieser Session: Bugfixes aus erstem Testlauf**

### Bugfixes (2026-06-01)

1. **`Weapon`-Properties fehlten** — `Weapon`-Dataclass hatte keine `is_melee`, `attacks`, `ap`, `strength`, `damage`, `abilities`, `range_inches`. Code griff überall direkt auf `Weapon`-Objekte zu → `AttributeError` im Column-Kontext → Shooting-/Fight-Phase-Columns verschwanden still.
   - Fix: Convenience-Properties auf `Weapon` ergänzt, delegieren auf `profiles[0]`.

2. **Dual-Profil-Waffen** (Staff of Light: Shooting + Melee-Profil) — `Weapon.is_melee` gab immer `profiles[0].is_melee` (= Shooting) zurück → Overlord in Nahkampfphase: "No melee weapons".
   - Fix: `Weapon.for_phase(use_melee: bool) → WeaponProfile` ergänzt. Filter in Fight-/Shooting-Phase und `render_attack_form` nutzen jetzt Profil-Ebene.
   - **Achtung für zukünftige Arbeit:** Weapon-Zugriffe nie per `w.is_melee` filtern, wenn Dual-Profile möglich sind — immer `any(p.is_melee for p in w.profiles)` und dann `w.for_phase(use_melee)` nutzen.

3. **`models_initial` fehlte** — `unitCard.py` nutzte `unit.models_max` als Nenner → Immortals mit Roster-Anzahl 5 zeigten `5/10` statt `5/5`.
   - Fix: `models_initial` in `_unit_state()` gespeichert.

4. **MWBD Keyword-Case** — Check war `"Core" in unit.keywords`, Keywords in units.yaml sind `UPPERCASE`.
   - Fix: `"Core"` → `"CORE"`.
   - **Achtung:** Alle zukünftigen Keyword-Checks müssen `UPPERCASE` nutzen.

5. **MWBD/ResOrb gegenseitiger Ausschluss** — Beide Awaiting-States konnten gleichzeitig aktiv sein → `elif res_orb_awaiting:` im unitCard wurde von `if mwbd_awaiting:` blockiert, ResOrb-Zielauswahl war nie erreichbar.
   - Fix: Aktivieren des einen States löscht den anderen in `commandPhase.py`.

### Stand nach Session
- 323 Tests grün
- App läuft mit zwei Necron-Armeen (α + β)
- Shooting-Phase, Fight-Phase, Command-Phase (inkl. MWBD + ResOrb) funktionieren grundsätzlich

---

## Aktueller Status

| Ziel | Status |
|------|--------|
| 5a — Spec | ✅ |
| 5b — Necron-Katalog | ✅ |
| 5b.2 — Datensäuberung | ✅ |
| 5c — Loader-Refactoring | ✅ |
| 5c — Bugfixes (Weapon, MWBD, ResOrb) | ✅ |
| 5d — BattleScribe Importer | ⬜ |
| 5e — Setup-Screen Redesign | ⬜ |
| 5f — Stratagems PoC | ⬜ |

---

## Nächste Schritte

### Priorät 1 — Ziel 5e: Setup-Screen Redesign

Das ist der sinnvollste nächste Schritt, weil er:
- Die hartcodierten Roster-Dateien in `game_state.py` auflöst (blockiert alles andere)
- Einen Roster-Dropdown einführt — Basis für echtes Spielen mit verschiedenen Armeen
- Die Unmatched-Warnungen sichtbar macht

**Kritische Architektur-Änderung (muss zuerst gelöst werden):**
`game_state.py` lädt Roster auf Modul-Ebene (beim Import) — `_P1_MATCHED`, `_P2_MATCHED` etc. sind globale Variablen. Das muss in `init_state()` verschoben werden, damit Roster-Pfade dynamisch übergeben werden können.

Plan:
1. Roster-Globals aus Modul-Ebene entfernen
2. `init_state(roster_p1, roster_p2, game_mode, game_size)` — Roster-Pfade als Parameter
3. Setup-Screen-UI: Dropdown für P1 + P2 aus `data/rosters/`, Spielmodus, Spielgröße, CP-Initialisierung
4. Start-Button erst aktiv wenn P1 ≠ P2 und beide Rosters gewählt

### Priorität 2 — Ziel 5d: BattleScribe Importer

Erst nach 5e sinnvoll, weil 5e die Roster-Auswahl erst ermöglicht.

Erweiterung Roster-Format um Wargear (Entwurf):
```yaml
- id: wh40k_9e.necrons.unit.overlord
  models: 1
  wargear:
    - wh40k_9e.necrons.weapon.voidscythe
    - wh40k_9e.necrons.wargear.resurrection_orb
```

### Priorität 3 — Orks-Fraktion

Orks haben nur eine Legacy `army.yaml` — kein `units.yaml`. Für echtes Zwei-Fraktionen-Spiel wird eine zweite vollständige Fraktion gebraucht. Kann parallel zu 5d/5e laufen.

---

## Bekannte offene Lücken (nicht vergessen)

| Lücke | Beschreibung |
|-------|-------------|
| `resolve_bracket_stats` unverdrahtet | Implementiert, aber kein UI-Aufruf — Vehicles zeigen immer Basis-Stats unabhängig vom aktuellen Wundstand |
| Orks-Fraktion fehlt | Nur Legacy `army.yaml`, kein `units.yaml` — Ziel 5c.6 war geplant, nicht umgesetzt |
| Wargear im Roster-Format | Aktuell nur `id` + `models` — keine Wargear-Auswahl speicherbar |
| Punkte-Validierung | `load_points()` implementiert, aber Roster-Gesamtpunkte werden nicht geprüft |
| Unmatched-UI | `roster_warnings` in session_state, aber kein UI-Feedback |
| Dual-Profil Datasheet | Setup-Phase zeigt nur `profiles[0]` einer Waffe im Datasheet-View |

---

## Wichtige Constraints

- Freigabe vor Umsetzung — Plan zeigen, auf „ja" warten
- Seitenleisten IMMER fest: first_player links, second_player rechts (unveränderlich während Spiel)
- dev-Branch — kein direktes Committen auf main
- Keywords immer `UPPERCASE` in units.yaml — Checks entsprechend schreiben
- Weapon-Zugriff: Nie `w.is_melee` für Filter nutzen wenn Dual-Profile möglich — `w.for_phase(use_melee)` verwenden
