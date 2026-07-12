# Dice Display Spec

> Kanonisches Dokument für die Würfelanzeige in `src/uiLayout/diceHtml.py`.
> Änderungen an `diceHtml.py` müssen hier reflektiert und durch Tests in
> `tests/uiLayout/test_dice_html.py` abgedeckt sein.
> Letzte Aktualisierung: 2026-06-20 (Refinement-Session)

---

## 1. Zeilenstruktur

Jede Modifier-Zeile besteht aus:

```
[BADGE] [  1 ][  2 ][ | ][  3 ][  4 ][  5 ][  6 ]
```

| Element | Breite | Beschreibung |
|---|---|---|
| `[BADGE]` | 96 px | Label + Wert (z. B. `"AP −2"`); CSS `overflow:hidden; text-overflow:ellipsis` |
| `[Slot N]` | 34 px | je 32 px SVG + 2 px Margin |
| `[ \| ]` | variabel | Erfolgsschwelle (Trennzeichen Fail-Zone / Success-Zone) |

**Invariante (unveränderlich):** Slot 1 zeigt **immer** `[✕]`. Ein
unmodifiziertes Würfelergebnis von 1 misslingt immer — kein Buff kann das
aufheben.

**Randfall Schwelle ≤ 1 (S122/F3):** Drücken Modifikatoren den effektiven
Zielwert auf 1+ oder besser, beginnt `dice_row_html` den Erfolgsrahmen bei
Wert 1 — der Wert-1-Würfel wird dann **innerhalb** des Rahmens trotzdem als
✕-Miss-Würfel gezeichnet (nie als normaler Erfolgspip). Rechenseitig floort
`resolve_save()` (`combat.py`) den effektiven Save analog zu Hit/Wound auf
minimal 2 (`max(2, …)`), sodass „Eff. 1+" weder angezeigt noch gewertet wird
(Regel: „An unmodified roll of 1 always fails", core_rules.txt Hit/Wound/Save).

Konkretes Soll-Bild im SAVE-Block (Stakeholder-Entscheid S122, Variante A):

- **Eff.-Zeile floort auch in der Anzeige bei 2+** (`diceHtml.py`,
  `_render_dice_save_block`): Label nie „Eff. 1+", Rahmen 2–6; die Farbe folgt
  der normalen Schwellen-Konvention (§7 / `_THRESHOLD_COLOR`) und ist bei der
  gefloorten 2 damit **grün** — orange kodiert Schwellen-Schwere, nie
  „modifiziert".
- **Modifier-Mini-Zeile:** Drückt ein Buff den Zielwert unter 2+
  (`armour − value ≤ 1`), steht der Quell-Würfel für eine natürliche 1 und wird
  als ×-Miss-Face gezeichnet: `[✕] +1→ [2]` statt `[1] +1→ [2]`
  (`save_modifier_die_pair_html`, Parameter `left_miss`).
- **Inv-Zeile bleibt konventionsgemäß** in ihrer Schwellenfarbe (z. B. Inv 4+
  → amber) — „alles grün" bezieht sich nur auf die gefloorte Eff.-Zeile.

### 1.1 Schwellen-Position

| Profil-Wert | `[ | ]` sitzt zwischen |
|---|---|
| 2+ | Slot 1 und Slot 2 |
| 3+ | Slot 2 und Slot 3 |
| 4+ | Slot 3 und Slot 4 |
| 5+ | Slot 4 und Slot 5 |
| 6+ | Slot 5 und Slot 6 |

---

## 2. Richtungskonvention

> **Korrektur zum früheren Code:** `diceHtml.py:200` hatte `rightward = value < 0`
> — Richtung war invertiert. Korrekt: `rightward = value > 0`.
> Gefixt in Plan 022 (2026-06-20). Bei Regressionen: `test_buff_arrow_points_right`
> und `test_debuff_arrow_points_left` schlagen fehl.

| Modifier-Typ | Pfeil-Richtung | Farbe | Bedeutung |
|---|---|---|---|
| **Buff (+)** | RECHTS `[→]` | Grün `#4a9a5a` | Effektiver Würfelwert steigt — niedrigere Ergebnisse genügen |
| **Debuff (−)** | LINKS `[←]` | Rot `#ef4444` | Effektiver Würfelwert sinkt — höhere Ergebnisse nötig |

### 2.1 Pfeil-Label-Format

| Modifier | Label |
|---|---|
| Debuff −N | `[←N]` (z. B. `[←1]`, `[←2]`) |
| Buff +N | `[+N→]` (z. B. `[+1→]`, `[+2→]`) |

---

## 3. Modifier-Fälle

### 3.1 Standardfall — Basis 3+

```
         [✕ ][  2 ][ | ][  3 ][  4 ][  5 ][  6 ]
Debuff-1: [✕ ][  2 ][←1 ][  3 ]
Buff +1:  [✕ ][  2 ][+1→][  3 ]
Debuff-2: [✕ ][  2 ][←2 ][  ─ ][  4 ]
Buff +2:  [✕ ][  2 ][+2→][  3 ]           ← Slot 1 bleibt ✕ (Invariante)
Debuff-3: [✕ ][  2 ][←3 ][  ─ ][  ─ ][  5 ]
Buff +3:  [✕ ][  2 ][+3→][  3 ]           ← Slot 1 bleibt ✕ (Invariante)
```

### 3.2 Grenzfall — Basis 6+

```
         [✕ ][  2 ][  3 ][  4 ][  5 ][ | ][  6 ]
Debuff-1:                        [  5 ][←1 ][  6 ]
Debuff-2:                        [  5 ][←2 ][  ─ ][✕ ]   ← über 6 = immer miss
Debuff-3:                        [  5 ][←3 ][  ─ ][  ─ ][✕ ]
Buff +1:                         [  5 ][+1→][  6 ]
Buff +2:                    [  4 ][  ─ ][+2→][  6 ]
Buff +3:               [  3 ][  ─ ][  ─ ][+3→][  6 ]
```

### 3.3 Grenzfall — Buff gegen die 1 (Basis 3+)

```
         [✕ ][  2 ][ | ][  3 ]
Buff +2:  [✕ ][  2 ][+2→][  3 ]   ← Slot 1 = ✕, Buff ändert nichts
Buff +3:  [✕ ][  2 ][+3→][  3 ]   ← identisch (Invariante gilt absolut)
```

---

## 4. Reroll-Marker

Reroll-Würfe zeigen das `↺`-Symbol **unterhalb** des betroffenen Slots.

```
         [✕ ][  2 ][ | ][  3 ][  4 ][  5 ][  6 ]
Reroll 1:  ↺
Reroll 1-2: ↺    ↺
```

---

## 5. Always-Fail-Marker

Fähigkeiten, die bestimmte Würfelergebnisse immer scheitern lassen, zeigen
`✕` **unterhalb** der betroffenen Slots (zusätzlich zum regulären Slot-Inhalt).

```
         [✕ ][  2 ][ | ][  3 ][  4 ][  5 ][  6 ]
QShield:   ✕    ✕           ✕         ← 1, 2 und 3 scheitern immer (Angreifer-Perspektive)
```

### 5.1 Perspektivabhängige Farbe (Quantum Shield)

Quantum Shield ist kontextabhängig:

| Perspektive | Bedeutung | `color_hint` | Farbe |
|---|---|---|---|
| Verteidiger | Angreifer-Würfe 1–3 scheitern → Vorteil | `"buff"` | Grün `#4a9a5a` |
| Angreifer | Eigene Würfe 1–3 scheitern → Nachteil | `"debuff"` | Rot `#ef4444` |

Steuerung: optionales `color_hint: "buff" | "debuff"` im Modifier-Dict
(aus `abilityEngine.py`). Wenn nicht gesetzt: wertbasierte Farbe (Vorzeichen).

---

## 6. `color_hint`-Feld

Optionales Feld im Modifier-Dict (rückwärtskompatibel):

```python
{
    "value": -3,           # Würfelmodifikator
    "color_hint": "buff",  # optional; überschreibt Vorzeichen-basierte Farbe
}
```

| `color_hint` | Farbe |
|---|---|
| `"buff"` | Grün `#4a9a5a` |
| `"debuff"` | Rot `#ef4444` |
| nicht gesetzt | wertbasiert (`value > 0` → grün, `value < 0` → rot) |

---

## 7. Farbschema

| Wert / Hinweis | Farbe | Hex |
|---|---|---|
| Buff / `color_hint: "buff"` | Grün | `#4a9a5a` |
| Debuff / `color_hint: "debuff"` | Rot | `#ef4444` |

Beide Werte sind in `docs/spec/design_colors.md §3` (Effekt-Badges) verankert.

---

## 8. Test-Anforderungen (PFLICHT)

Jede Änderung an `diceHtml.py` braucht einen entsprechenden Test in
`tests/uiLayout/test_dice_html.py`. Neue Fälle erweitern die Tabelle.

| Test | Was wird geprüft | Plan |
|------|-----------------|------|
| `test_buff_arrow_points_right` | Buff → Pfeil rechts (Regression) | 022 |
| `test_debuff_arrow_points_left` | Debuff → Pfeil links (Regression) | 022 |
| `test_slot_1_always_shows_x` | Slot 1 = ✕, unabhängig von Modifier | 022 |
| `test_long_badge_does_not_overflow` | Badge truncated bei > 96 px | 022 |
| `test_color_hint_overrides_value_sign` | `color_hint` > Vorzeichen | 022 |
| `test_debuff_beyond_6_shows_x_slot` | Debuff über 6 → ✕ rechts | 022 |
| `test_buff_cannot_make_1_succeed` | Buff macht 1 nie zu Erfolg | 022 |
| `test_reroll_marker_correct_slot` | ↺ unter korrektem Slot | 022 |
| `test_always_fail_marks_correct_slots` | ✕ unter allen auto-fail-Slots | 022 |
| `test_multi_step_debuff_arrow_carries_magnitude` | Debuff ≥2 → `←N` am Pfeilkopf (§2.1) | 022/S78 |
| `test_multi_step_buff_arrow_carries_magnitude` | Buff ≥2 → `+N→` am Pfeilkopf (§2.1) | 022/S78 |
| `test_single_step_debuff_magnitude_rides_in_boundary_gap` | Shift 1 → `←1` im Boundary-Gap (§3.1) | 022/S78 |
| `test_single_step_buff_magnitude_rides_in_boundary_gap` | Shift 1 → `+1→` im Boundary-Gap (§3.1) | 022/S78 |
| `test_off_scale_debuff_arrow_carries_magnitude` | Off-Scale → `←N` mit echter Magnitude | 022/S78 |
| `test_hit_debuff_arrow_carries_magnitude` | HIT-Zeile trägt `←N` (Geometrie = B, separat) | 022/S78 |
| `test_buff_magnitude_uses_buff_colour_not_context_grey` | Pfeil-Label in Modifier-Farbe, nicht Grau | 022/S78 |
| `test_dice_row_natural_one_always_shows_miss_marker_even_in_success_frame` | Schwelle ≤ 1 → Wert 1 als ✕ im Erfolgsrahmen (§1 Randfall) | S122/F3 |
| `test_save_floored_at_2_armour_path` / `test_save_floored_at_2_invuln_path` | `resolve_save()` floort effektiven Save auf 2 (`test_combat_6d.py`) | S122/F3 |
| `test_effective_save_row_floors_display_at_2_and_renders_green` | Eff.-Zeile zeigt nie „1+", gefloorte 2 → grüner Rahmen (§1 Soll-Bild) | S122/F3 |
| `test_save_modifier_row_natural_one_source_die_shows_miss_cross` | Mini-Zeile: Buff-Ziel ≤ 1 → Quell-Würfel als ×-Miss-Face (Variante A) | S122/F3 |

---

## 9. Bekannte offene Punkte

Alle D1–D5 in Plan 022 erledigt (2026-06-21). Tabelle als Historie.

| ID | Beschreibung | Plan | Status |
|---|---|---|---|
| D1 | Arrow-Direction-Bug (`rightward = value < 0` invertiert) | Plan 022 Step 1 | ✅ GEFIXT (`rightward = value > 0`) |
| D2 | Badge-Breite / Overflow bei langen Labels | Plan 022 Step 2 | ✅ GEFIXT (Ellipsis-Truncate) |
| D3 | Edge Cases 6+ / gegen-1 fehlen | Plan 022 Step 4 | ✅ Marker-Bausteine + Guard-Tests |
| D4 | `color_hint`-Feld nicht vorhanden | Plan 022 Step 3 | ✅ `_modifier_color()` |
| D5 | `dakka`/`klaw`/`tesla`-Literals (INV-4b) | Plan 022 Step 5 | ✅ datengetrieben via `effect.type` |

**Verdrahtungs-Hinweis (D3):** `reroll_marker_row_html` / `always_fail_marker_row_html`
sind getestete Anzeige-Bausteine, aber noch **nicht** in einen Roll-Block verdrahtet —
sie werden konsumiert, sobald ein Produzent Reroll-/Auto-fail-Slots liefert
(z. B. Quantum Shield, `reroll_hit_1`).

| D6 | Pfeil-Magnitude `←N`/`+N→` fehlte (Befund A) | S78 | ✅ GEFIXT (`_arrow_span` + Boundary-Gap-Label) |
| D7 | HIT/WOUND-Debuff-Geometrie spreizt nicht mit Magnitude (Befund B); Slot-1-Invariante bei HIT-Buff verletzt (Befund C) | — | ⏳ OFFEN → eigener Plan (`modifier_die_pair_html`-Rework, getestet → Regressionsfläche) |

---

## 10. Detaillierte Beispielgeometrie (Stakeholder-Mockups, Refinement 2026-06-21)

> Verbindliche Slot-Geometrie für den Executor. `[ | ]` = Erfolgsschwelle aus dem
> Profil. `[leer]` = Slot ohne Inhalt. `[✕]` = Miss-Symbol. `[↺]` = Reroll-Symbol
> (= App-weites Reset-Glyph). Trailing `[✕]` ganz rechts = Off-Scale-Miss (> 6).
> Buff = grün `[+N→]`, Debuff = rot `[←N]`. Jeder Block braucht einen HTML-Test.

### 10.1 Reroll-Wurf (z. B. „wiederhole Trefferwurf von 1")

`[↺]` steht **unterhalb** des betroffenen Slots; rechts die Off-Scale-Spalte.

```
        [leer][Slot1][Slot2][ | ][Slot3][Slot4][Slot5][Slot6][✕]
[Badge] [↺]
```

### 10.2 Always-Fail (z. B. Quantum Shield: Wundwürfe 1–3 scheitern)

`[✕]` unterhalb jedes betroffenen Slots. **Perspektiv-Farbe** (§5.1): für den
Verteidiger Buff (grün), für den würfelnden Angreifer Debuff (rot) — über
`color_hint` gesteuert, NICHT über das Vorzeichen.

```
        [leer][Slot1][Slot2][ | ]   [Slot3][Slot4][Slot5][Slot6][✕]
[Badge] [✕]   [✕]          [leer][✕]
```

### 10.3 Standardfall — Buff +1 und Debuff −2 bei Schwelle 3+

```
         [leer][Slot1][Slot2][ | ]   [Slot3][Slot4][Slot5][Slot6][✕]
[Debuff] [leer]      [2]      [←2]   [─]    [5]
[Buff]   [leer]      [2]      [+1→]  [3]
```

### 10.4 Grenzfall gegen die 6 — Rüstung 6+, diverse Modifier

Debuffs über 6 erzeugen einen Off-Scale-Miss `[✕]` rechts; Buffs ziehen die
effektive Schwelle nach links.

```
           [leer][Slot1][Slot2][Slot3][Slot4][Slot5][ | ][Slot6][✕]
[Debuff-1] [leer]                            [5]    [←1] [6]
[Debuff-2] [leer]                            [5]    [←2] [─]   [✕]
[Debuff-3] [leer]                            [5]    [←3] [─]   [✕]
[Buff+1]   [leer]                            [5]    [+1→][6]
[Buff+2]   [leer]                     [4]    [─]    [+2→][6]
[Buff+3]   [leer]              [3]    [─]    [─]    [+3→][6]
```

### 10.5 Grenzfall gegen die 1 — Rüstung 2+, diverse Modifier

Spiegelbildlich zu 10.4. Slot 1 bleibt **immer** `[✕]` (Invariante §1): ein
unmodifiziertes 1 misslingt; ein Debuff, der unter 1 drückt, erzeugt Off-Scale-Miss.

```
           [leer][Slot1][ | ][Slot2][Slot3][Slot4][Slot5][Slot6][✕]
[Debuff-1] [✕]   [←1] [2]
[Debuff-2] [✕]   [←2] [─]   [3]
[Buff+1]   [✕]   [+1→][2]
[Buff+2]   [✕]   [+2→][2]   (Slot 1 bleibt ✕ — Invariante absolut)
```
