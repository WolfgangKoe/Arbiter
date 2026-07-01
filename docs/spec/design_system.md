# Design-System — verbindlich (beschlossen S115, 2026-07-01)

> **Regel: Design-Entscheidungen trifft der Nutzer** (wie beim Farbschema).
> Diese Spec deckt Geometrie (Badge/Chip-Maße), die Hinweis-Konvention und die
> Symbol-Konstanten ab. **Farben** stehen weiterhin verbindlich in
> [`design_colors.md`](design_colors.md) — hier NICHT dupliziert, nur referenziert.

## 0. Governance & Artefakt-Zuschnitt

| Aspekt | Kanonischer Ort |
|---|---|
| Farbwerte (Hex, CSS-Variablen, Badge-Farbsemantik) | [`design_colors.md`](design_colors.md) |
| Geometrie-Tokens (Radius/Padding/Font-Size/Weight) | **diese Datei, §2** |
| Hinweis-Konvention (info/warning/success/error) | **diese Datei, §3** |
| Symbol-Konstanten (Glyphen) | **diese Datei, §4** → Code: `src/constants/symbols.py` |
| Kanonische Badge-/Chip-Builder (Code) | `src/uiLayout/badges.py` |

Warum getrennt: `design_colors.md` ist bereits etabliert und wird an vielen Stellen
referenziert. Diese Spec ergänzt die *nicht-farblichen* Design-Entscheidungen, statt
sie zu duplizieren (Artefakt-Landkarte: genau ein kanonischer Ort je Frage).

## 1. Komponenten-Inventar

### 1.1 Badge / Chip — EIN Builder (`src/uiLayout/badges.py`)

Vor S115 bauten vier Call-Sites (`_common._badge`, `unitCard._badge`,
`armyCard._keyword_badge`/`_active_ability_badge`, Invuln-Fragmente in `dice_html`)
denselben `<span>` mit leicht abweichenden Maßen von Hand nach — sie waren bereits
gedriftet. Jetzt liefert `badges.py` die Geometrie zentral; **Farben bleiben am
Call-Site** (sie stammen aus den semantischen Tabellen in `design_colors.md`).

| Builder | Zweck | Konsumenten |
|---|---|---|
| `badge(text, fg, bg, *, margin_right)` | Status / Buff / Debuff / Faction / Army-Ability | `_common._badge`, `unitCard._badge`, `armyCard._keyword_badge` + `_active_ability_badge`, `dice_html` Invuln-„active" |
| `chip(text, fg, bg, border, *, margin_right)` | Keyword-Chip / sekundärer Hinweis | `unitCard._keyword_chip`, `dice_html` Invuln-„AP/Cover N/A" |

Der Invuln-Block (`dice_html.py`, `_render_dice_save_block`) baut das Label jetzt aus
diesen Bausteinen statt aus drei losen HTML-Fragmenten (Backlog-Befund S78, Z. 129):
„active" = `badge(...)`, „AP/Cover N/A" = `chip(...)` mit gedämpfter Farbe.

**Nicht Teil des gemeinsamen Builders (bewusst):** `dice_compose._badge_chip` — das
Dice-Modifier-Label hat eine eigene Sonder-Geometrie (feste Spaltenbreite +
Ellipsis-Truncation), es ist kein Status-Badge. Bleibt eigenständig.

### 1.2 Card / Panel

`st.container(border=True)` — Streamlit liefert den Rahmen einheitlich über den
Emotion-Selektor (siehe `CLAUDE.md`). Kein eigener Wrapper, keine Divergenz gefunden →
kein Handlungsbedarf, nur hier dokumentiert.

### 1.3 Dice-Grid / Block-Divider

`dice_compose.py` (`grid_row_html`, `block_divider_html`, …) ist der bereits etablierte,
Streamlit-freie, Coverage-gemessene Kompositions-Layer (INV-6). `badges.py` folgt exakt
demselben Seam: pure HTML-Builder, kein Streamlit, Coverage-gemessen.

## 2. Geometrie-Tokens (verbindlich, S115)

Zwei Größenklassen. Werte aus dem jeweils häufigsten IST-Wert abgeleitet
(minimal-invasiv). Quelle im Code: `src/uiLayout/badges.py` (dort EINMAL definiert).

| Token | `badge` | `chip` |
|---|---|---|
| border-radius | 2px | 2px |
| padding | `1px 6px` | `1px 5px` |
| font-size | 10px | 9px |
| font-weight | 600 | 400 |
| letter-spacing | 0.06em | 0.05em |

`badge` verwendet `fg` zugleich als Rahmenfarbe (Outline-Pille). `chip` erlaubt einen
vom `fg` abweichenden `border` (z. B. gedämpfter Keyword-Chip).

## 3. Hinweis-Konvention (info/warning/success/error, S115)

Regel in einem Satz: *Fehlschlag, der Teil des normalen Spielablaufs ist (Würfel
verloren, Test nicht bestanden) → `warning`; Fehlschlag mit Zusatzkonsequenz oder
echtem Fehlerzustand (Perils, Daten-/Konfigurationsfehler) → `error`; reine Bestätigung
→ `success`; neutrale Regel-Erinnerung ohne Erfolg/Misserfolg → `info`.*

| Typ | Wann | Beispiel |
|---|---|---|
| `success` | Aktion erfolgreich / Regelwirkung wie erwartet | „✓ N models · MW · damage applied" |
| `info` | Neutraler Hinweis, keine Wertung (Regel-Erinnerung, Tisch-Hinweis Klasse B/C) | Aura-Range-Hinweis |
| `warning` | Erwarteter, regelkonformer Fehlschlag | „Power failed", „Deny failed", Subgruppe verloren |
| `error` | Regelverletzung / Datenfehler / Fehlschlag mit Zusatzkonsequenz | „Perils — power failed", fehlendes `subfaction_field` |

**Farbe:** `success` = `--arb-green`, `info` = `--arb-blue`, `error` = `--arb-red`
(s. `design_colors.md` §1). `warning` bleibt bewusst bei Streamlits nativem Amber —
es wird nur über `st.warning()` gerendert, nie als eigenes HTML-Badge; **kein
`--arb-warning`-Token** (S115-Entscheidung).

## 4. Symbol-Konstanten (`src/constants/symbols.py`, S115)

Ein kanonischer Ort je Glyph — projektweit konsistent tauschbar, keine Fraktionslogik.

| Konstante | Glyph | Bedeutung |
|---|---|---|
| `SYM_EXPAND` | ▶ | nicht selektiert → aufklappen/ansehen |
| `SYM_COLLAPSE` | ◀ | selektiert/aktiv → einklappen |
| `SYM_EXPAND_ALT` | ▷ | Aufklapp-Variante für Zeile **ohne** wählbares Ziel (eigener Zustand, NICHT auf ▶ vereinheitlichen) |
| `SYM_CHECK` | ✓ | bestanden / erledigt / zugewiesen |
| `SYM_CROSS` | ✕ | fehlgeschlagen / entfernen / abbrechen |
| `SYM_ADD` | ＋ | hinzufügen / zuweisen |
| `SYM_SWORDS` | ⚔ | Kampf / Kampfhandlung (ohne Variation-Selector — `⚔️` VS16 wurde S115 angeglichen) |
| `SYM_RESET` | ↺ | Reset / Rückgängig / Reroll |

## 5. Migrations-Hinweis (Ratchet, kein Big-Bang)

S115 hat die vier Badge-Stencils + den Invuln-Block + die Reroll/Fail-Glyphen umgestellt.
Weitere Glyph-Literale (`✓`/`✕`/`＋`/`⚔` in Phase-Modulen) werden auf die Konstanten
gezogen, **wenn die Stelle ohnehin angefasst wird** — nicht als isolierter Refactor-Commit.
Neue Badges/Chips werden direkt gegen `badges.py` gebaut, statt eine fünfte Kopie zu
erzeugen (Ratchet-Prinzip, analog Rule-Catalog-Gate).
