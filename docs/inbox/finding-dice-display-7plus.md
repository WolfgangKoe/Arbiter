# Finding: Dice-Display 7+/Off-Scale-Saves + Magnitude-Position (Gap-Analyse)

> Analysiert: 2026-06-21. Kein Code geändert. Entscheidungen bleiben bei Opus + Stakeholder.

---

## Ist-Zustand (Code)

### Rendering-Pfad für SAVE-Block

`dice_html.py:_render_dice_save_block` erstellt den SAVE-Block:

1. **Armour-Basis-Zeile**: `threshold_header_html(min(armour, 7)) + dice_row_html(min(armour, 7))`
2. **Modifier-Zeilen**: `save_ap_modifier_row_html(armour, ap)` → ruft `save_modifier_die_pair_html`
3. **Effektiv-Zeile**: `threshold_header_html(eff_clamped) + dice_row_html(eff_clamped)` mit `eff_clamped = min(armour_modified, 7)`

`dice_compose.py` stellt folgende Bausteine bereit:

- `threshold_header_html(threshold)`: Header-Labels 1+..6+; boundary-gap nur wenn `2 <= threshold <= 6`. Für threshold=7 iteriert die Schleife nur bis v=6 und die Bedingung `v==threshold` ist nie wahr → kein Separator, kein hervorgehobenes Label.
- `dice_row_html(threshold)`: Für threshold>6 → alle 6 Miss-Würfel + ein Miss-Würfel rechts (existierende Off-Scale-Darstellung).
- `save_modifier_die_pair_html(armour, value, label, color)`: Debuff-Pfad berechnet `left_val = max(1, armour-1)` (grau), `right_raw = armour + abs(value) - 1`. `off_scale = right_raw > 6`.
- `_aligned_modifier_row_html(...)`: Generische Modifier-Zeile. Setzt boundary_gap bei `v == base_threshold`. Magnitude-Label (`←N` / `+N→`) wird platziert bei `v == lo+1` (Debuff) bzw. `v == hi-1` (Buff) — also als eigenständiger Slot **nach** dem boundary-gap-Slot.

### Magnitude-Position — Ist-Zustand

Für shift==1 (Sonderfall): Magnitude **ersetzt** den boundary-gap-Slot (`_modifier_slot_html(glyph_span(head_glyph, ...))` statt `_boundary_gap_html`). Das ist korrekt laut Spec §3.1.

Für shift>1: Der boundary-gap-Slot ist leer (`_boundary_gap_html(with_line=False)`), und `←N` erscheint im **nächsten** Slot (v=lo+1 für Debuff, v=hi-1 für Buff). Zwei Slots: erst leer, dann Magnitude.

Für SAVE-Modifier (Debuff, armour≤6): `lo = armour-1`, `base_threshold = armour`. Daher `lo+1 = armour = base_threshold`. Der leere boundary-gap-Slot und der `←N`-Slot liegen am **selben** v-Index — d.h. `←N` erscheint eine Stelle rechts des leeren Gaps. Beide Slots zusammen entsprechen visuell zwei Spaltenbreiten an der Grenzposition.

---

## Lücke 1 — 7+/Off-Scale-Saves (native Sv 7+, z.B. Gretchin)

### Was fehlt

**In `threshold_header_html`**: Die Bedingung `2 <= threshold <= 6` schließt threshold=7 aus. Für eine native 7+-Rüstung (armour=7) produziert `threshold_header_html(7)` sechs gleichförmige, nicht hervorgehobene Labels (1+..6+), keinen Separator, kein `7+`-Label und kein visuelles Off-Scale-Signal. Der Nutzer sieht eine leere, unmarkierte Kopfzeile.

**Stakeholder-Soll**: `[6] | [✕]` — die Spalte 6+ wird hervorgehoben, danach ein Separator, dann ein Miss-Würfel als Off-Scale-Marker.

**In `dice_html.py:_render_dice_save_block`**: `sv_text = f"Sv {armour}+" if armour <= 6 else "Sv —"` blendet das 7+ komplett aus. Titel zeigt `Sv —` statt z.B. `Sv 7+`.

**In `save_modifier_die_pair_html`** bei armour=7 + Debuff: `left_val = 6` (grey), `right_raw = 7 + n - 1 ≥ 7 → off_scale=True`, `right_col = 6`. Da `left_col == right_col == 6` und `shift = 0`, wird kein Pfeil und keine Magnitude erzeugt. Die Modifier-Zeile zeigt nur einen grauen Würfel bei Spalte 6 und danach den Miss-Würfel — ohne Richtungspfeil.

**Cover-Randfall (Stakeholder: `[6] 1→[7]`)**: Sv 7+, Cover +1 → effektiv immer noch unmöglich. Was zu zeigen ist, wenn ein Buff auf eine 7+ Rüstung angewendet wird, ist in der Spec noch nicht definiert.

### Betroffene Funktionen

- `dice_compose.py:threshold_header_html` — keine 7+-Darstellung
- `dice_compose.py:save_modifier_die_pair_html` — shift=0 bei armour=7 unterdrückt Pfeil
- `dice_html.py:_render_dice_save_block` — `sv_text` blendet 7+ aus; Basis-Zeile fehlt visuell

---

## Lücke 2 — Magnitude-Position

### Was fehlt

Für shift>1 erzeugt `_aligned_modifier_row_html` an der Grenzposition **zwei** Slots in Folge:
1. `_boundary_gap_html(with_line=False)` — leer, keine Linie
2. `_modifier_slot_html(←N)` — Magnitude

Visuell: Magnitude steht eine Spaltenbreite **rechts** der Grenzposition. Der Nutzer sieht `…[Grey-Die][leer][←N][Red-Die]…` statt `…[Grey-Die][←N][Red-Die]…` (wobei `←N` die Grenzmarkierung ist).

Der Stakeholder-Befund (Screenshot AP-2): „-2 unter die Grenze" bedeutet: `←N` soll **an der Stelle des `|`** stehen, nicht dahinter. Der boundary-gap-Slot soll `←N` direkt tragen, nicht leer sein.

Für shift==1 ist dies bereits korrekt gelöst (Magnitude ersetzt den Gap-Slot). Der Befund trifft nur shift>1.

**HIT/WOUND-Buff mit shift>1** (via `modifier_die_pair_html`): `+N→` sitzt bei `v == hi-1` — das ist die Stelle **links** der boundary-gap (v=base_threshold=from_thresh). Für Buff erscheint die Magnitude links vor dem Separator, nicht im Separator-Slot.

**SAVE-Debuff shift>1** (via `save_modifier_die_pair_html`): Wie beschrieben, `lo+1 == base_threshold` → Magnitude ist im Slot direkt nach dem leeren Gap (gleicher v-Index). Die Magnitude erscheint also eine extra Spaltenbreite zu weit rechts.

---

## Betroffene Funktionen/Spec (Datei:Funktion)

| Datei | Funktion | Befund |
|---|---|---|
| `src/uiLayout/dice_compose.py` | `threshold_header_html` | Lücke 1: kein 7+-Label, kein Separator bei threshold=7 |
| `src/uiLayout/dice_compose.py` | `dice_row_html` | Lücke 1: bereits korrekt (miss dice + miss die bei >6) |
| `src/uiLayout/dice_compose.py` | `save_modifier_die_pair_html` | Lücke 1: shift=0 bei armour=7 unterdrückt Pfeil |
| `src/uiLayout/dice_compose.py` | `_aligned_modifier_row_html` | Lücke 2: für shift>1, boundary-gap-Slot ist leer, Magnitude in separatem Slot danach |
| `src/uiLayout/dice_compose.py` | `modifier_die_pair_html` | Lücke 2: Buff shift>1 setzt Magnitude links des Separators (Debuff-Shift ist immer 1 → kein Problem) |
| `src/uiLayout/dice_html.py` | `_render_dice_save_block` | Lücke 1: `sv_text` = "Sv —" für armour>6; Basis-Zeile ruft `threshold_header_html(7)` ohne 7+-Unterstützung |
| `docs/spec/dice_display.md` | §1.1, §10 | Lücke 1: 7+-Schwelle nicht spezifiziert (nur 2+..6+); Cover-Randfall bei 7+ offen |

---

## Optionen je Befund (Trade-offs)

### Lücke 1 — 7+/Off-Scale-Saves: drei Optionen

**Option A: Minimal — nur `threshold_header_html` erweitern**

`threshold_header_html` erhält einen 7+-Spezialfall: Bei threshold=7 hängt die Funktion nach dem Label 6+ einen Separator-Slot und danach ein hervorgehobenes `✕`-Label (als Off-Scale-Marker) an. `dice_row_html(7)` bleibt unverändert (zeigt bereits miss dice + miss die). In `_render_dice_save_block`: `sv_text` zeigt für armour=7 `Sv 7+` statt `Sv —`.

Für Modifier-Zeilen mit armour=7: `save_modifier_die_pair_html` erzeugt derzeit shift=0 → kein Pfeil. Dieses Problem bleibt ungelöst.

*Trade-offs*: Geringer Aufwand, header-Anzeige wird korrekt. Modifier-Pfeil bei nativer 7+-Rüstung fehlt weiter (AP-N auf Sv 7+ zeigt keine Richtung). Kein Spec-Text für 7+-Modifier nötig. Minimale Testfläche.

**Option B: Vollständig — alle 7+-Fälle adressieren**

Zusätzlich zu Option A: `save_modifier_die_pair_html` erhält Logik für armour>6. Der linke Ankerpunkt bleibt Spalte 6 (grey), der Pfeil zeigt trotzdem ←N (Debuff), rechts folgt ein Miss-Würfel. Dafür muss `_aligned_modifier_row_html` den Fall `left_col==right_col` mit off_scale anders behandeln (Pfeil von Spalte 6 nach rechts-outside).

Spec §10 muss um 7+-Abschnitt ergänzt werden (native 7+, Cover-Randfall, AP-N auf 7+). Neue Testfälle für alle Varianten.

*Trade-offs*: Korrekte Darstellung aller 7+-Modifier. Erfordert Spec-Erweiterung (Design-Entscheidung: wie sieht AP-N auf Sv 7+ aus?). Mehr Testfläche. Mittlerer Aufwand. Cover-Randfall (`[6] 1→[7]`) bleibt designoffen.

**Option C: Visuell vereinfacht — 7+ als reines "Unmöglich"-Signal**

Für alle 7+-Saves (native oder durch AP) wird in Header + Modifier keine echte Geometrie gezeigt, sondern nur ein "Sv 7+ (unmöglich)"-Badge ohne Pfeildarstellung. `dice_row_html(7)` bleibt die Basis.

*Trade-offs*: Kein Geometrie-Umbau nötig. Verliert die Informations-Granularität (kein Pfeil für "wie weit über 6 wurde die Rüstung gedrückt"). Spec-mäßig am wenigsten ambitioniert. Leicht implementierbar, leicht testbar.

---

### Lücke 2 — Magnitude-Position: zwei Optionen

**Option A: Magnitude in den boundary-gap-Slot legen (für shift>1)**

In `_aligned_modifier_row_html`: Wenn `v == base_threshold` und shift>1 (und Debuff: `v == lo+1`, oder Buff: `v == hi-1` entspricht base_threshold), dann `←N` / `+N→` in den boundary-gap-Slot legen statt leerer Gap. Den v-Slot (v=lo+1 bzw v=hi-1) dann zum leeren Connector oder ─ degradieren.

Konkret: Die Bedingung `if shift == 1` auf `if v == hi and lo == hi - 1` ausweiten zu `if v == base_threshold and (lo+1 == base_threshold or hi-1 == base_threshold)` — also immer wenn der boundary-gap mit dem arrowhead-Slot zusammenfällt.

Effekt: Boundary-gap-Slot trägt `←N`, kein leerer Zwischenraum.

*Trade-offs*: Entspricht Stakeholder-Soll. Betrifft SAVE-Debuff (shift>1), SAVE-Buff (shift>1), HIT/WOUND-Buff (shift>1). Keine bestehenden Tests prüfen die Position des leeren boundary-gaps → Regressionslücke ist klein. Visuell: ←N sitzt direkt neben dem linken Würfel ohne Extra-Lücke davor. Erfordert manuelle Verifikation.

**Option B: Separate visuelle Linie + Magnitude nebeneinander**

Statt den boundary-gap-Slot zu belegen: `_boundary_gap_html(with_line=True)` für shift>1 verwenden (zeigt die vertikale Linie) und die Magnitude separat daneben als eigenen Slot belassen. So bleiben beide Elemente sichtbar: `|` und `←N`.

*Trade-offs*: `|` und `←N` erscheinen als zwei Slots, was mehr Breite verbraucht. Entspricht nicht exakt dem Stakeholder-Screenshot ("←N unter |"), da beide nebeneinander stehen. Keine Code-Logik-Änderung in der Slot-Reihenfolge nötig. Visuell weniger sauber.

---

## Regressionsfläche (bestehende Tests)

### Tests, die bei Lücke-1-Änderungen brechen könnten

| Test | Funktion | Risiko |
|---|---|---|
| `test_impossible_threshold_uses_miss_die_not_text_cross` | `dice_row_html(7)` | Prüft SVG-Count=7; safe solange dice_row_html(7) unverändert |
| `test_threshold_header_all_thresholds_render` | `threshold_header_html` (loop 2..6) | Safe; testet nur 2-6 |
| `test_threshold_header_boundary_gap_inserted` | `threshold_header_html(4)` | Safe; testet Threshold 4 |
| `test_threshold_header_no_gap_below_two` | `threshold_header_html(1)` | Safe |

Kein Test prüft `threshold_header_html(7)` — Neuland, keine Regression durch Neuimplementierung.

### Tests, die bei Lücke-2-Änderungen brechen könnten

| Test | Was er prüft | Risiko |
|---|---|---|
| `test_multi_step_debuff_arrow_carries_magnitude` | `←2` present in HTML | Kein Positionscheck → safe |
| `test_multi_step_buff_arrow_carries_magnitude` | `+2→` present | Kein Positionscheck → safe |
| `test_single_step_debuff_magnitude_rides_in_boundary_gap` | `←1` present | Shift-1-Pfad unverändert → safe |
| `test_single_step_buff_magnitude_rides_in_boundary_gap` | `+1→` present | Shift-1-Pfad unverändert → safe |
| `test_off_scale_debuff_arrow_carries_magnitude` | `←4` present | Kein Positionscheck → safe |
| `test_hit_debuff_arrow_carries_magnitude` | `←2` present | HIT-Debuff immer shift-1 → unberührt |
| `test_buff_magnitude_uses_buff_colour_not_context_grey` | Farbcheck `+2→` | Kein Positionscheck → safe |
| `test_reroll_marker_with_base_threshold_boundary_gap` | `width:34px` in html | Prüft Gap-Slot-Breite, nicht Inhalt → safe |

**Kein bestehender Test pinnt, dass der boundary-gap-Slot leer sein muss.** Magnitude-Position-Änderungen erzeugen daher keine direkten Test-Regressionen. Visuelles Risiko besteht (manuelle Verifikation Pflicht).

Einziges mittelbares Risiko: Wenn die Slot-Schleife umgebaut wird, könnten indirekte Struktur-Tests (`test_modifier_columns_*`, `test_aligned_modifier_row_off_scale_appends_miss_die`) scheitern, falls die Off-Scale-Logik mit angefasst wird.

---

## Offene Design-Fragen für Opus + Stakeholder

1. **Lücke 1, Cover-Randfall**: Was soll `[6] 1→[7]` exakt bedeuten? Wenn Sv 7+ mit Cover+1 → Sv 6+, soll das als "Cover verbessert die unmögliche Rüstung auf 6+" mit einem Buff-Pfeil von 7→6 dargestellt werden? Das erfordert einen rechtswärtigen Pfeil von außerhalb-der-Skala — spezielle Geometry-Logik.

2. **Lücke 1, AP auf Sv 7+**: Stakeholder-Soll `[6] ←4 [✕]` legt nahe, dass auch AP auf eine 7+-Rüstung einen Pfeil zeigen soll (von 6 nach rechts/off-scale). Derzeit erzeugt shift=0 keinen Pfeil. Soll dafür eine neue Geometrie-Variante in `_aligned_modifier_row_html` entstehen, oder reicht ein Sonderfall in `save_modifier_die_pair_html`?

3. **Lücke 1, `sv_text`**: Soll der Titel `Sv 7+` oder `Sv —` zeigen? Wenn Sv 7+ gezeigt wird: ist das spielregelkonform (in WH40k 9E gibt es keine nativen Sv 7+ Profile außer No Save)?

4. **Lücke 2, Buff vs Debuff Symmetrie**: Der Stakeholder-Screenshot zeigt AP-Debuff. Soll die Magnitude-in-Boundary-Logik auch für Buff gelten (Magnitude in boundary-gap-Slot, nicht im hi-1-Slot)? Oder nur für Debuff?

5. **Lücke 2, HIT/WOUND-Buff shift>1**: Der Befund D7 (backlog.md) beschreibt, dass `modifier_die_pair_html` für Buff die Slot-1-Invariante verletzt und für Debuff die Geometrie nicht spreizt. Die Magnitude-Position ist ein Teilaspekt dieses größeren D7-Problems. Sollen beide in einem Plan gelöst werden, oder Magnitude-Position zuerst?

6. **Spec-Erweiterung**: Welcher der §10-Abschnitte soll um 7+-Geometrie erweitert werden, und welche Fälle (native 7+, Buff auf 7+, AP auf 7+, Cover auf 7+) müssen mit Beispiel-Slots spezifiziert werden, bevor Implementierung startet?
