# Design-System — verbindlich (beschlossen S115, 2026-07-01; bestätigt S120, 2026-07-03)

> **Regel: Design-Entscheidungen trifft der Nutzer** (wie beim Farbschema).
> Diese Spec deckt Geometrie (Badge/Chip-Maße), die Hinweis-Konvention und die
> Symbol-Konstanten ab. **Farben** stehen weiterhin verbindlich in
> [`design_colors.md`](design_colors.md) — hier NICHT dupliziert, nur referenziert.
>
> **S120-Nachtrag:** Der Konsens-Vorschlag aus `docs/handoff/design-system-consensus.md`
> (Task 0, Phase 1) wurde am 2026-07-03 vom Stakeholder mit der Default-Empfehlung in
> allen fünf Entscheidungsfragen bestätigt — die Werte in §2–§4 waren bereits identisch
> umgesetzt (S115), keine inhaltliche Änderung nötig. Die Handoff-Datei wurde danach
> gelöscht (Lebensdauer laut Datei-Kopf: bis Stakeholder-Entscheidung).
>
> **S131-Nachtrag (entschieden 2026-07-09):** §6 ergänzt — die GO-Karte (Gefechtsoptionen-
> UI), der Tisch-Wurf-Eingabe-Baustein und die Wortlaut-Konventionen sind jetzt
> verbindlicher Standard für jeden weiteren UI-Auftrag an Gefechtsoptionen. Quelle:
> `docs/handoff/design_system_konzept_s131.md` (Stakeholder hat alle 4 Entscheidungsfragen
> mit der Empfehlung beantwortet). Orte-Zuordnung stützt sich auf
> [`../reference/go_klassifikation.md`](../reference/go_klassifikation.md) (95-GO-Katalog,
> 3 Achsen). Umsetzung läuft als Roadmap über S132–S134+ (Pakete in
> [`../goals/backlog.md`](../goals/backlog.md) §2) — jedes Paket geht einzeln durchs
> Freigabe-Gate, diese Spec ist der Maßstab dafür.

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
`armyCard._keyword_badge`/`_active_ability_badge`, Invuln-Fragmente in `diceHtml`)
denselben `<span>` mit leicht abweichenden Maßen von Hand nach — sie waren bereits
gedriftet. Jetzt liefert `badges.py` die Geometrie zentral; **Farben bleiben am
Call-Site** (sie stammen aus den semantischen Tabellen in `design_colors.md`).

| Builder | Zweck | Konsumenten |
|---|---|---|
| `badge(text, fg, bg, *, margin_right)` | Status / Buff / Debuff / Faction / Army-Ability | `_common._badge`, `unitCard._badge`, `armyCard._keyword_badge` + `_active_ability_badge` |
| `chip(text, fg, bg, border, *, margin_right)` | Keyword-Chip / sekundärer Hinweis | `unitCard._keyword_chip`, `gameActionsArea._display_unit_datasheet` (seit S117/S118) |

Der Invuln-Block (`diceHtml.py`, `_render_dice_save_block`) wurde in S116 bewusst
**gestrichen**, nicht auf die Bausteine umgestellt (Commit `143d848`: „Invuln cleanup:
drop active badge + AP/Cover N/A chip from SAVE block"): „active"-Badge und
„AP/Cover N/A"-Hinweis entfielen ersatzlos; übrig bleibt nur die `Inv N+`-Zeile als
eingefärbter `<span>` (Buff-Grün bei ability-basiertem Invuln) — kein
`badge()`/`chip()`-Aufruf. Der Backlog-Befund S78 (drei lose HTML-Fragmente, Z. 129)
ist damit durch Streichung erledigt. *(Korrigiert S120, 2026-07-03 — die frühere
Formulierung „baut das Label aus diesen Bausteinen" beschrieb einen nie gebauten Stand.)*

**Nicht Teil des gemeinsamen Builders (bewusst):** `diceCompose._badge_chip` — das
Dice-Modifier-Label hat eine eigene Sonder-Geometrie (feste Spaltenbreite +
Ellipsis-Truncation), es ist kein Status-Badge. Bleibt eigenständig.

**Tooltip-Konvention für lange Labels (S158/B-111, Variante C):** Die
Ellipsis-Truncation bleibt für alle Aufrufer bestehen (kein Wrap-Modus, keine
Verbreiterung der Spalte). `_badge_chip` trägt zusätzlich das volle,
ungekürzte Label im `title`-Attribut des `<span>` — bei Hover zeigt der Browser
den vollständigen Text (z.B. „Quantum Shielding" statt „Quantum Sh…"). Gilt für
jeden Aufrufer von `_badge_chip` einheitlich, keine Sonderfälle je Label-Länge.

### 1.2 Card / Panel

`st.container(border=True)` — Streamlit liefert den Rahmen einheitlich über den
Emotion-Selektor (siehe `CLAUDE.md`). Kein eigener Wrapper, keine Divergenz gefunden →
kein Handlungsbedarf, nur hier dokumentiert.

### 1.3 Dice-Grid / Block-Divider

`diceCompose.py` (`grid_row_html`, `block_divider_html`, …) ist der bereits etablierte,
Streamlit-freie, Coverage-gemessene Kompositions-Layer (INV-6). `badges.py` folgt exakt
demselben Seam: pure HTML-Builder, kein Streamlit, Coverage-gemessen.

### 1.4 Subgruppen-Selector / Damage-Block (Loss-Allocation, S168/B-124)

`_render_subgroup_selector` + `_render_damage_block` (`src/uiLayout/_common.py`) — der
Verteidiger-Baustein im DAMAGE-Block einer Resolution-Tab für Einheiten mit mehreren
Modell-Gruppen (`unit.model_groups`, z. B. Ork Nobz, Silent King). Drei Zustände, EIN
Radio + EIN `dmg_col.warning(...)`, keine Sonderform je Zustand:

- **A — frei wählbar:** kein Modell angeschlagen, keine Zuteilungspflicht
  (`get_locked_group()` → `None`) → Radio über alle aktiven Gruppen, Default = niedrigste
  Priorität.
- **B/gesperrt — Warnhinweis statt Radio:** `get_locked_group()` liefert eine Gruppe →
  Radio entfällt vollständig, die Gruppe wird direkt übernommen. Der Warnhinweis-Text hat
  zwei Zweige für zwei Sperrgründe (beide `► …`-Präfix, gleiche Warning-Familie):
  „Angeschlagenes Modell … muss zuerst abgehandelt werden" (Front-Modell bereits verwundet)
  vs. „… muss laut Regel zuerst vollständig zerstört werden, bevor andere Gruppen Schaden
  nehmen" (Zwangs-Zuteilungs-Einheit, `unit.has_per_group_wounds()`, ab vollem HP gesperrt —
  z. B. Silent King: Triarchal Menhirs vor Szarekh, Codex „Triarchal Menhir").
- **C — nur eine Gruppe übrig:** Selector entfällt ersatzlos (nichts zum Wählen), Schaden
  trifft die verbleibende Gruppe direkt.

Die Sperrentscheidung selbst lebt ausschließlich in `get_locked_group()`
(`gameMechanic/unitMutations.py`) — die UI liest nur das Ergebnis, keine Dopplung der
Regel-Logik. Registriert als B-124-Ratchet-Eintrag (berührte Bauform bei jeder Modul-Berührung
hier nachziehen, kein Big-Bang).

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

## 4. Symbol- & Würfel-Design-System (§4.1 S115, §4.2/§4.3 neu S159/B-104)

Ein kanonischer Ort je Glyph/Würfelfläche — projektweit konsistent tauschbar, keine
Fraktionslogik. Drei Unterabschnitte, auf Augenhöhe mit §6 (Gefechtsoptionen-UI):
§4.1 Glyph-Konstanten (Einzelzeichen, kein Würfel-Slot-Kontext), §4.2 Würfelflächen-
Katalog (echte Würfel-SVGs), §4.3 Effekt-Symbol-Katalog (Symbole, die in einem
Würfel-Slot erscheinen — teils SVG-Würfel, teils bewusst Text-Chip).

### 4.1 Glyph-Konstanten (`src/constants/symbols.py`, S115)

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

### 4.2 Würfelflächen-Katalog (`diceCompose.dice_face_svg`-Familie, S159/B-104)

Kanonische Zeichenroutine für „das ist eine echte Würfelfläche": `dice_face_svg(value,
color, miss, size)` — 32×32 SVG (`viewBox="0 0 32 32"`), abgerundetes Rechteck
(`rx=4 ry=4`), Rahmen 1.5px. Jede Zeile unten ist eine Variante **derselben** Funktion —
kein zweiter Bau-Ort für „sieht aus wie ein Würfel".

| Würfelfläche | Geometrie | Farblogik | Konsument |
|---|---|---|---|
| Erfolgs-Würfel (Pip-Muster 1–6) | 32×32 SVG, `rx=4`, Rahmen 1.5px = `color`-Parameter, Pips als `<circle r="2">` an festen Positionen (`_PIP_POSITIONS`) | Rahmen-/Pip-Farbe = Schwellen-Skala (`_THRESHOLD_COLOR`: grün 2+/3+, amber 4+, orange 5+/6+) oder Modifier-Perspektivfarbe (Buff-Grün/Debuff-Rot), s. `design_colors.md` §0/§4b — kein neues Token | `dice_row_html` (Erfolgsrahmen), `_aligned_modifier_row_html` (linker/rechter Vergleichswürfel) |
| Miss-Würfel (echter Fehlschlag, Wert 1) | gleiche 32×32-Box, Kreuz = zwei diagonale `<line>` volle Fläche statt Pips | Heute hart `#374151` (Rahmen) / `#c0392b` (Kreuz). **Task-2-Entscheid:** optionaler Farbparameter, Default = exakt dieser Ist-Wert — kein bestehender Aufrufer ändert sich optisch | `dice_row_html` (Wert 1, immer Miss), `miss_die_html()` |
| Off-Scale-Miss-Marker (Schwelle > 6, z. B. Sv 6+ mit AP-4) | identisch Miss-Würfel — reine Zweitverwendung, kein eigener Stil | identisch Miss-Würfel | `dice_row_html` (threshold>6-Zweig), `_aligned_modifier_row_html` (`right_off_scale=True`) |
| Modifier-Paar-Miss (linker Würfel = natürliche 1, S122/F3) | identisch Miss-Würfel, in der linken statt rechten Spalte | identisch Miss-Würfel | `_aligned_modifier_row_html(left_miss=True)`, `save_modifier_die_pair_html` |

### 4.3 Effekt-Symbol-Katalog (Würfel-Slot-Marker, S159/B-104, ersetzt bisheriges §4.1)

Symbole in einem Würfel-Slot (die Spalte unter/neben der Würfelreihe, die einen bestimmten Wert markiert) folgen zwei verschiedenen Familien: zwei erscheinen als echte Würfelflächen-SVGs (§4.2-Familie, gleiche 32×32-Box-Geometrie), eine ist bewusst ein Text-Chip (weil das Dargestellte keine reale Würfelfläche im Spiel ist). Die folgenden Vorgriff-Zeilen dokumentieren Effekt-Typen, die heute noch nicht oder nur unvollständig gerendert werden — jede Zeile entscheidet explizit Familie und Rendering-Stand, damit „noch kein Producer" nicht mit „kein Katalog-Eintrag" verwechselt wird (Ratchet: Zeile existiert, Code folgt erst mit dem Producer).

| Effekt | Symbol | Familie | Geometrie | Farblogik | Konsument / Status |
|---|---|---|---|---|---|
| Auto-fail/miss | ✕ | SVG-Würfelfläche | dieselbe Miss-Würfel-SVG wie §4.2 Zeile 2 (Kreuz statt Pips) — einziger Unterschied: Rahmen-/Kreuzfarbe parametrisiert statt hart | `_modifier_color({"color_hint": ...})` → Buff-Grün (Verteidiger-Perspektive) oder Debuff-Rot (Angreifer-Perspektive), `design_colors.md` §0/§4b — kein neues Token | `always_fail_marker_row_html` → `_marker_row_html` (produktiv verdrahtet, Quantum Shielding) |
| Reroll | ↺ | SVG-Würfelfläche | gleiche 32×32-Box (Rahmen 1.5px, `rx=4`), Inhalt statt Kreuz/Pip = zentriertes ↺-Glyph (`SYM_RESET`) | fix Reroll-Orange `#f59e0b` (bereits etablierte Reroll-Farbe, kein neues Token) | `reroll_marker_row_html` → `_marker_row_html` (Stand S158/S159: noch nicht produktiv verdrahtet — wartet auf Skorpekh/Destroyer-Lord-Producer, B-113) |
| AP-Modifier-Trigger | z. B. `AP-1` | Text-Chip | 30×30px Box, `border-radius:4px`, `border` = Farbparameter, `bg:#1e293b`, Text 9px/700 zentriert (`_triggered_die_chip_html`) | Aufrufer-Parameter (aktuell immer Buff-Grün, Baustein selbst ist farbneutral) | `value_triggered_die_row_html` (Direktiv-Effekt bei unmodifiziertem Wurfergebnis, z. B. Hungry Void D1 bei einer 6) |
| Tesla-Extra-Hits (`extra_hits_on_unmodified_6`, generisch +N Treffer) | +N | Text-Chip | identisch AP-Trigger-Chip (30×30, `border-radius:4px`, Text zentriert), Inhalt `+N` statt `AP-N`, in der auslösenden Spalte (meist 6) | Buff-Grün (Angreifer-Vorteil), analog `value_triggered_die_row_html` | **TEILWEISE** — heute nur externer Badge außerhalb des Grids (`special_die_html`, diceHtml.py:70, „Extra Hits: unmod. 6 = +2 Hits"), kein In-Slot-Chip. Vorgriff empfiehlt Migration auf `value_triggered_die_row_html("Extra Hits", 6, "+2", buff-grün)` — vereinheitlicht mit dem AP-Trigger-Muster (s. §4.4-Lücke) |
| Extra-Wound-on-6 (Custodes) | +1 | Text-Chip | wie Tesla-Zeile — nur im WOUND- statt HIT-Block, Inhalt `+1` | wie Tesla-Zeile | **KEIN Rendering heute** — reiner Vorgriff, kein Producer verdrahtet |
| Auto-Hit (Flamer u. ä.) | — | Text-Chip | wie `special_die_html` (bestehender Waffenregel-Badge: `border:1px solid`, `border-radius:4px`, `padding:2px 6px`, 11px Text); **kein Slot-Marker** innerhalb der Würfelreihe — der gesamte HIT-Grid entfällt (kein Wurf, keine Schwelle) | Buff-Grün (kein Fehlschlag mehr möglich — reiner Vorteil), NICHT das fixe Reroll-Orange von `special_die_html` heute — bewusster Farb-Unterschied, weil dies kein Waffenregel-Hinweis, sondern ein Wurf-Ersatz ist | **KEIN Rendering heute** — Vorgriff; künftiger Konsument ersetzt `threshold_header_html`+`dice_row_html` komplett in `_render_dice_roll_block`, wenn `auto_hit` gesetzt ist |
| Auto-Wound (Necron-Stratagems) | — | Text-Chip | wie Auto-Hit-Zeile — WOUND-Block statt HIT-Block | wie Auto-Hit-Zeile | **KEIN Rendering heute** — Vorgriff |
| Zusätzlicher Trefferwurf (ein Erfolg löst einen echten Zusatzwurf aus, keine feste Zahl) | ＋ | SVG-Würfelfläche | neue Anker-Position rechts von Spalte 6 (gleiche Position wie der Off-Scale-Miss-Marker, §4.2 Zeile 3), gleiche 32×32-Box, Inhalt = `SYM_ADD` („＋") zentriert statt Pips/Kreuz — signalisiert „hier wird ein Würfel angehängt" | Buff-Grün (Angreifer-Vorteil) | **KEIN Rendering heute, kein Producer bekannt** — reiner Vorgriff für einen künftigen Effekt-Typ; falls ein solcher Effekt datengetrieben auftaucht, referenziert er diese Zeile statt eine neue zu erfinden |
| Plasma-Overcharge / Selbstverwundung (`mortal_wounds_self`) | — | Text-Chip | bis der DAMAGE-Block entworfen ist: Debuff-Rot Text-Chip analog `_strength_source_badge_html`, Inhalt z. B. „Overcharge: D3 MW self" | Debuff-Rot (Nachteil für den Träger selbst, unabhängig vom Ziel) | **KEIN Rendering heute** — Vorgriff, **blockiert durch die DAMAGE-Block-Entscheidung** (§4.4); kein eigenständiger Bau vor diesem Entscheid |

**Abgrenzung — keine Würfel trotz Namens/Kontext (dokumentarisch, kein Rename in diesem
Task):**

- `special_die_html` (diceCompose.py) — trotz Namen **kein** Würfel: reiner Label-Chip
  für Waffenregeln (Tesla, Alt. Fire, Extra Hits), fix Reroll-Orange umrandet, aber ohne
  Würfelfläche. Nicht Teil dieser Kataloge.
- `_strength_source_badge_html` (diceHtml.py) — trotz Nähe zum S-vs-T-Vergleich **kein**
  Würfel: Inline-Chip, der die GO-Quelle eines Strength-Buffs benennt (S146 Fix 1).
  B-105-Kandidat für Generalisierung zu `go_source_chip`, bleibt aber immer Text-Chip.

**Ratchet-Prinzip (gilt für §4.2 und §4.3 gemeinsam):** Neuer Fall künftig — erst die
passende Zeile hier ergänzen (§4.2 für eine echte neue Würfelfläche, §4.3 für ein neues
Slot-Symbol inkl. Entscheidung SVG- vs. Text-Chip-Familie), dann Code anpassen. Kein
Symbol ohne Tabellen-Eintrag. Vorgriff-Zeilen (Effekt-Typ ohne Producer) bleiben stehen,
bis ein Producer sie befüllt — sie werden nicht gelöscht, nur weil noch kein Code sie
konsumiert.

### 4.4 Wurf-Block-Pattern (S159 Fassung 2)

Nicht nur die Symbole *in* einem Würfel-Slot sind katalogisiert (§4.2/§4.3) — auch der
Aufbau des Wurf-Blocks selbst (HIT/WOUND/SAVE/DAMAGE) folgt einem kanonischen Muster,
damit ein Spieler jeden Block gleich liest, unabhängig davon, wofür gewürfelt wird.

**Kanonischer Aufbau (Soll, einheitlich für HIT/WOUND/SAVE/DAMAGE):**

```
├─ Titel + Vergleichswert (WS/BS N+, S vs T, Sv N+, …)
├─ Threshold-Header + Dice-Row (Basis-Schwelle)
├─ Marker-Zeilen (optional): Auto-fail (✕) / Reroll (↺) / Value-Trigger (+N) — alle
│  über denselben Slot-Mechanismus wie §4.3
├─ Modifier-Zeilen (je Modifier: Vergleichs-Würfelpaar + eigene Eff.-Zeile, verschachtelt)
├─ Eff.-Zeile (finale Schwelle nach allen Modifiers)
└─ Quellen-Chips (optional): GO-/Ability-Herkunft eines Buffs/Debuffs (Text-Chip-Familie)
```

HIT und WOUND folgen diesem Muster weitgehend (WOUND vollständiger: Marker-Zeilen sind
dort bereits verdrahtet, s. §4.3). SAVE und DAMAGE weichen ab — die Abweichungen sind
**Vereinheitlichungs-Lücken**, hier benannt, aber **nicht in S159 umgesetzt**:
Backlog-Kandidaten für einen eigenen Folge-Task (Muster wie die Pakete 4c/5/6 in §6.2).

| Lücke | Ist-Zustand | Soll-Zustand | Status |
|---|---|---|---|
| SAVE-Modifier flach statt verschachtelt | AP + Cover je eine flache Zeile, nur eine finale Eff.-Zeile am Ende (`_render_dice_save_block`, diceHtml.py:225–246) | Jeder SAVE-Modifier bekommt wie bei HIT/WOUND seine eigene Eff.-Zeile (verschachtelt), damit AP+Cover-Kombinationen den Zwischenschritt zeigen statt eines Sprungs | Backlog-Kandidat |
| Invuln als Separat-Sektion | Invuln rendert außerhalb des Save-Block-Patterns, ohne Marker-Zeilen-Hooks (diceHtml.py:250–260) | Invuln folgt demselben Wurf-Block-Pattern (Threshold-Header/Dice-Row/Marker-Zeilen), bleibt aber als eigene Sektion sichtbar — Invuln ist regelkonform ein anderer Save-Typ, keine Verschmelzung mit dem Armour-Path | Backlog-Kandidat |
| Keine Marker-Zeilen im SAVE-Block | SAVE hat keine Auto-fail-/Reroll-Anker, obwohl Save-Rerolls regelseitig existieren (z. B. Invuln-Reroll) | SAVE-Block bekommt dieselben Marker-Zeilen-Hooks wie WOUND — Struktur vorbereiten, nicht erst beim ersten Anwendungsfall improvisieren | Backlog-Kandidat |
| HIT-Block ohne Marker-Zeilen | `_render_dice_roll_block` ruft `always_fail_marker_row_html`/`reroll_marker_row_html` nicht auf, obwohl HIT-Rerolls existieren (Skorpekh, B-113) | HIT-Block bekommt dieselben Marker-Zeilen-Hooks wie WOUND, sobald ein HIT-seitiger Producer (B-113) sie befüllt | Backlog-Kandidat, an B-113 gekoppelt |
| Fehlender DAMAGE-Block | Kein `_render_dice_damage_block()`; Mortal Wounds/Overcharge sind reine Text-Labels ohne Würfel-Grid | Neuer DAMAGE-Block folgt demselben Pattern (Titel/Dice-Row bei echtem Schadenswurf, Marker-/Quellen-Chip-Zeilen immer) — offene Entwurfsfrage: zeigt er ein Grid, wenn nur D3/D6 ohne Erfolgsschwelle gewürfelt wird? | Backlog-Kandidat, eigener Entwurfsschritt nötig (kein Trivial-Fix) |
| Tesla-Extra-Hits als externer Badge statt In-Slot-Chip | `special_die_html`-Badge außerhalb des Grids statt `value_triggered_die_row_html` in Spalte 6 (s. §4.3-Vorgriff-Zeile) | Migration auf das AP-Trigger-Muster, damit „Erfolg bei 6 löst Zusatzwert aus" gleich aussieht, egal ob AP-Bonus oder Zusatz-Treffer | Backlog-Kandidat |

## 5. Migrations-Hinweis (Ratchet, kein Big-Bang)

S115 hat die vier Badge-Stencils + den Invuln-Block + die Reroll/Fail-Glyphen umgestellt.
Weitere Glyph-Literale (`✓`/`✕`/`＋`/`⚔` in Phase-Modulen) werden auf die Konstanten
gezogen, **wenn die Stelle ohnehin angefasst wird** — nicht als isolierter Refactor-Commit.
Neue Badges/Chips werden direkt gegen `badges.py` gebaut, statt eine fünfte Kopie zu
erzeugen (Ratchet-Prinzip, analog Rule-Catalog-Gate).

**Schritt 2 (S117/S118) abgeschlossen:** Rollout auf die restlichen 10 Produktivdateien
(`_common.py`, `chargePhase.py`, `moralePhase.py`, `shootingPhase.py`, `fightPhase.py`,
`commandPhase.py`, `psychicPhase.py`, `gameActionsArea.py`, `gameHeader.py`,
`setupScreen.py`) — alle `▶ ◀ ▷ ✓ ✕ ＋ ⚔ ↺`-Literale in Code-Ausdrücken auf die
`symbols.py`-Konstanten gezogen, dazu die Keyword-Chip-Stelle in
`gameActionsArea._display_unit_datasheet` auf `chip()` migriert. Bewusste Ausnahmen bleiben
Literal, kein Ratchet-Anspruch: `gameHeader._phase_badges_html` (eigene dritte
Geometrie-Klasse, kein Badge im Sinne von §1.1), `diceCompose._badge_chip` (S115 bereits
eigenständig), der `←`-Pfeil (keine Konstante in §4 vorgesehen) sowie das `⬇`-Download-Icon
in `setupScreen.py` (kein Semantik-Match in §4). Der Ratchet-Rest ist damit auf Null —
neue Literale, die künftig hinzukommen, werden wieder gegen diesen Stand geprüft.

## 6. Gefechtsoptionen-UI — GO-Karte, Tisch-Wurf-Baustein, Wortlaut (entschieden S131, 2026-07-09)

Zweck: verbindlicher UI-Standard für jede Gefechtsoption (GO — Stratagems + vergleichbare
optionale Regeln), damit künftige Aufträge nicht wieder eigene Bauformen erfinden (Anlass:
S130-Befund — GOs existierten bereits in drei divergenten Formen: reaktive Box, Inline-Offer,
Tab-Schalter). Grundlage: `docs/handoff/design_system_konzept_s131.md` (vom Stakeholder mit
der Empfehlung in allen 4 Fragen bestätigt) und die GO-Klassifikation in
[`../reference/go_klassifikation.md`](../reference/go_klassifikation.md).

### 6.1 Die GO-Karte — eine Komponente, drei Orte, vier Zustände

Statt drei Bauformen gibt es genau **eine** Komponente, überall gleich aufgebaut, nur in
Voll- oder Kompaktform gerendert:

```
▸ Fire Overwatch · 1 CP                    [Use]
[CORE] [CHARGE] [reaktiv]
   (▸ klappt den Regeltext aus — nur dafür)
```

- Header-Zeile: Name · CP-Kosten · genau **ein** Aktions-Slot rechts (`[Use]` oder `[↺]`).
- Keyword-Chips wie in der UnitCard (bestehender `chip()`-Baustein aus §1.1).
- Regeltext nur ausklappbar (Akkordeon-Fix: klappt nie von selbst zu — S130-Beschwerde).
- Kein Pass-Button (passen = `[Use]` nicht drücken), keine CP-Gesamtanzeige auf der Karte
  (die steht nur im GameHeader, s. §6.4).

Fünf Zustände ersetzen das bisherige plötzliche Auftauchen der reaktiven Box
(5. Zustand „verwendet-anderswo" ergänzt S139 B12a — Auslöser-Tracking, s.
`docs/handoff/S137_B12_konzept.md` §2.1/§2.2, Stakeholder-Entscheid F-A in
`docs/handoff/S139_planning.md`):

| Zustand | Wann | Darstellung |
|---|---|---|
| ruhend | Trigger (noch) nicht erfüllt | sichtbar, gedimmt, `[Use]` disabled |
| bereit | Trigger erfüllt, CP reichen | hervorgehoben (Gold-Primary, s. §6.5), `[Use]` aktiv |
| verwendet-hier | Use HIER (an diesem Anker) gedrückt, Fenster noch offen | `[↺ Undo]` statt `[Use]` |
| verwendet-anderswo | dieselbe GO (Spieler + GO-ID) diese Phase an EINEM ANDEREN Anker benutzt | gedimmt wie „gesperrt", Button zeigt deaktiviertes **„Used"** (kein Undo dort); Header-Suffix „used on ⟨Einheit⟩", falls eine Einheit bekannt (**verdrahtet S141, Commit `cdb55e2`;** Randfall Advance-Reroll/Inline-Spends ohne `unit_key` zeigen spec-konform keinen Suffix) |
| gesperrt | CP fehlen / Voraussetzung weg | gedimmt, Grund als Suffix im Header |

Gilt **einheitlich für jeden Anker** — Karte oder Inline, gleich an welcher Render-Stelle,
inklusive fenster-konsumierender GOs (Cut Them Down, Emergency Disembarkation): „Undo"
erscheint ausschließlich dort, wo tatsächlich eingesetzt wurde, überall sonst „Used".
Granularität pro Spieler UND GO-ID (nicht pro Einheit) — ein Spieler, der eine GO einsetzt,
blockiert damit nicht den Gegner; der Gegner sieht dieselbe GO unabhängig weiter als
„bereit", bis ER sie einsetzt.

**Anker-Schema (S139 B12b/c, konkrete `anchor_id`-Werte je Baustein):** zentrale
Stratagems-Liste (`gameProtocoll.py`) verwendet die Konstante `"central_list"` (ein
Spieler+GO hat dort genau EINE Render-Stelle, unabhängig von der gerade selektierten
Einheit); reaktive GO-Boxen (`_common.py:render_reactive_stratagem_box`) bilden
`f"reactive:{event}:{decline_key}"` intern aus ihren vorhandenen Parametern (keine
Aufrufer-Änderung nötig, s. Konzept §2.1); die Advance-Reroll-Karte
(`movementPhase.py:_render_advance_reroll_card`) verwendet `f"movement_reroll:{uid}"`
(ein Anker pro Einheit); das Inline-Command-Re-Roll-Angebot
(`_common.py:render_inline_command_reroll`) bildet `f"inline:{phase}:{reopen_key}"`
intern aus seinen vorhandenen Parametern (`reopen_key` existierte schon an allen 5
Aufrufstellen — keine Aufrufer-Änderung nötig, s. Konzept §2.1/B12c). Die vier
Zustands-Mapper (`_go_state_and_reason`, `_reactive_go_state`,
`_advance_reroll_state`, `_inline_reroll_state`) bleiben Streamlit-frei, pure Funktionen:
sie nehmen ein vom Aufrufer bereits berechnetes `used_here: bool`
(`stratagem_used_here(faction, id, anchor_id)`) entgegen, statt selbst auf
`st.session_state` zuzugreifen — gleiches Muster wie die bestehenden `used_ids`/
`used_battle_ids`-Sets. Desperate Breakout ist von diesem Mapper ausgenommen (bleibt
hart „used" — s. `movementPhase.py:_render_desperate_breakout` Docstring): die
Auflösungskarte rendert konstruktionsbedingt nur an der einen Einheit, deren
Pending-Flag gesetzt ist, das Flag wird nur durch genau den einen Einsatz über die
zentrale Liste gesetzt — „verwendet-anderswo" kann dort nicht auftreten.

Undo ist am Auslöser-Anker **Vollrückgängig** (CP zurück, Effekt/Wert zurück), solange das
Aktivierungsfenster offen ist — der Schiedsrichter-Moment kommt erst am Phasen-/Zug-/
Rundenende, nicht bei jedem Klick (App ist Erinnerer/Entscheidungshelfer, würfelt selbst
nicht — Regel bleibt unverändert gegenüber dem Bestand).

### 6.2 Orte-Zuordnung — statisches Modell (Stakeholder-Entscheid S134)

**Sichtbarkeits-Invariante (statisch, ersetzt die dynamische S133-Formulierung):**
GOs sind **statisch** in reaktiv und proaktiv unterteilt — die Zuordnung ist eine
Eigenschaft der GO-Klasse aus dem YAML, kein situatives Ein-/Ausblenden:

- `timing: phase_reactive` = **reaktiv**: die GO wird **on-trigger aktiv** — ein
  Spielereignis öffnet ihr Fenster (z. B. die Auswahl einer Einheit, die „in melee"
  ist ⇒ Desperate Breakout; eine gegnerische Charge-Deklaration; ein gefallener
  Wurf). Der Render-Ort folgt dem Trigger: Karte erscheint **NUR** inline am
  Trigger-Ort (Kompaktform), niemals in der zentralen Stratagems-Liste
  (Stakeholder-Definition, S134-Review Befund 2).
- sonst = **proaktiv**: der Spieler initiiert die GO selbst, ohne auslösendes
  Spielereignis ⇒ Karte erscheint **NUR** in der zentralen Stratagems-Liste
  (Vollform), niemals inline.

Nie beides, kein dynamischer Wechsel zwischen den Orten. Durchgesetzt an zwei Stellen:
`stratagem_visibility()` (versteckt `phase_reactive` ohne `reactive_trigger_active`)
und explizit in `_render_stratagem_column()` (`gameProtocoll.py`), damit der
Listen-Kontrakt nicht am Default-Argument hängt.

| Klassifikation (Achse b) | Ort | Form |
|---|---|---|
| spielweit (12 GOs, `before_battle`) | Liste im ArmySetup, vor „Start Game" | Vollform |
| phasenweit/proaktiv | zentrale Stratagems-Liste (Spielerseite) | Vollform |
| reaktiv (`timing: phase_reactive`, bei_ereignis) | **nur** Inline-Anker am Trigger-Ort | Kompakt |
| vor_wurf / nach_wurf (reaktiv) | Inline-Anker direkt an der Wurf-Eingabe | Kompakt |

Die zentrale Liste ist der **Planungs-Überblick** über die proaktiven Optionen, der
Inline-Anker die **Erinnerung am Ort des Geschehens** für die reaktiven — beide rendern
dieselbe Karte aus derselben Buchhaltung (`spend_stratagem`-Pipeline), nichts wird
doppelt gebucht. Der `before_battle`-Sichtbarkeitsfix bleibt konzeptionell gelöst:
eigener Ort statt Sonderphase. Achse (b) und die vollständige GO-Tabelle:
[`../reference/go_klassifikation.md`](../reference/go_klassifikation.md).

**Paket-4-Schuld (Anker folgen S134/S135, Ist-Stand nach 4a/4b/4c):** Der Stakeholder hat
die Übergangs-Ausnahme abgelehnt — reaktive GOs sind ab S134 komplett aus der zentralen
Liste, auch wenn ihr Inline-Anker noch fehlt. Nach Paket 4a–4c sind folgende
`phase_reactive`-GOs weiterhin nirgends aktivierbar (grep-Stand S135 Paket 4c; vorhandene
Anker-Fenster: movement/charge/fight × `on_declaration`, `on_destroy` nur bei
TRANSPORT-Tod, Deklarations-Anker (Ziel-Kachel) × `on_target` — seit S146 Fix 2 (Wound)
und S147/B1 (Hit, Save) der EINZIGE Ort für alle on_target-GOs, die dedizierten Hit-/
Wound-/Save-Anker in `_render_resolution_tab` wurden abgeschafft —, `after_roll`
via Advance-/Charge-/Psychic-/Damage-/Anzahl-Attacken-/Hit-/Wound-/Save-Anker (S136
Stufe 2, unverändert — das sind die Command-Re-Roll-Fenster, nicht die on_target-GO-Karten)):

| GO | (phase, event) | fehlender Anker |
|---|---|---|
| Desperate Breakout (Shared) | movement, — | Use-Anker an der in-melee-Unit (nur die Auflösungskarte nach Use existiert, `movementPhase.py`) |
| Aetheric Interception (Necrons) | movement, on_set_up | kein `on_set_up`-Fenster (neues Ereignis, kein bestehender Anker erweiterbar) |
| Reanimation Prioritisation (Necrons) | shooting, on_target | `effect.type: reanimate` gehört zur Attackenfolge/Reanimation-Priorisierung, nicht zum Hit-/Wound-/Save-Komplex — bewertet in Paket 4c (s. u.), nicht gebaut |
| Tough as Squig-Hide (Orks) | any, on_target | `effect.type: restriction` (unmodifizierter Wundwurf 1–3 scheitert, kein additiver Modifier) — passt in keinen der drei Hit-/Wound-/Save-Anker-Filter, eigener Mechanik-Ausbau nötig — bewertet in Paket 4c (s. u.), nicht gebaut |
| Resurrection Protocols (Necrons) | any, on_destroy | `on_destroy`-Fenster öffnet nur bei TRANSPORT-Tod, nicht beim eigentlichen Trigger |
| Curse of the Phaeron (Necrons) | any, on_destroy | dito |
| Revenge of the Doomstalker (Necrons) | any, on_destroy | dito |
| Canoptek Overdrive (Necrons) | fight, on_destroy | dito |
| Murderous Demise (Necrons) | fight, on_destroy | dito |
| Careen! (Orks) | any, on_destroy | dito |
| Orks is Never Beaten (Orks) | fight, on_destroy | dito |

Mit Anker erreichbar (kein Handlungsbedarf): Command Re-Roll (inkl. Anzahl-Attacken-Fenster,
Paket 4c, sowie Hit-/Wound-/Save-Fenster, S136 Stufe 2 — alle 9 regelerlaubten Wurf-Arten
von R-CMD-12 jetzt erreichbar, keine offene GO-Fensterfrage mehr für Command Re-Roll
insgesamt), Cut Them Down, Emergency Disembarkation, Fire Overwatch, Counter-Offensive,
Efficient Disintegration, Shadows of Drazak, Whirling Onslaught, Quantum Deflection
(alle drei: Deklarations-Anker an der Ziel-Kachel in `render_group_assignment`, S146
Fix 2 + S147/B1 — die früheren dedizierten Wound- (S146), Hit- und Save-Anker (S147)
in `_render_resolution_tab` wurden abgeschafft, alle on_target-GOs erscheinen nur noch
einmal, bei der Ziel-Zuweisung).

**Bewertung fehlender Ereignis-Fenster (Paket 4c, nur Doku — kein Bau):** drei
Fenster fehlen komplett bzw. sind zu eng gescopt, betreffen zusammen 10 der 11 oben
gelisteten GOs (alle außer Desperate Breakout, dessen fehlender Use-Anker ein
separates Problem ist — kein Ereignis-Fenster fehlt dort, nur die Verdrahtung):

- **`on_set_up`** (Aetheric Interception, 1 GO) — existiert im Code gar nicht; der
  Trigger liegt im gegnerischen Reinforcements-Schritt (`movementPhase.py`), einer
  bisher UI-technisch nicht behandelten Stelle.
- **`on_target` außerhalb des Hit-/Wound-/Save-Modifier-Stacks** (Reanimation
  Prioritisation, Tough as Squig-Hide, 2 GOs) — beide sind kein additiver
  Wurf-Modifier: Reanimation Prioritisation ist eine Zusatz-Aktion (Reanimate direkt
  bei Ziel-Auswahl), Tough as Squig-Hide ist ein Auto-Fail-Schwellenwert
  (unmodifizierter Wundwurf 1–3 scheitert) — beides bräuchte eigene Auswertungslogik
  statt eines Modifier-Eintrags in `resolve_attack_modifiers`/`resolve_save`.
- **generisches `on_destroy`** (Resurrection Protocols, Curse of the Phaeron,
  Revenge of the Doomstalker, Canoptek Overdrive, Murderous Demise, Careen!, Orks is
  Never Beaten — 7 GOs, größter Cluster; Resurrection Protocols zählt hier als eine
  Zeile der Debt-Tabelle, obwohl es als Infantry-/Character-Variante zwei separate
  Stratagems in `go_klassifikation.md` §2 sind) — der bestehende `on_destroy`-Hook feuert nur
  beim TRANSPORT-Tod (Emergency Disembarkation); eine generische Version muss an jede
  Stelle, an der ein Modell/eine Einheit über alle Phasen hinweg als zerstört gilt
  (`unitMutations.py`, `combat.py`, Morale-Verluste), nicht nur an einen einzelnen
  Aufruf.

**Empfehlung: eigener Folge-Split, in zwei Pakete statt einem.** Begründung: die drei
Fenster sind architektonisch verschieden (neues Setup-Phase-Ereignis / Mechanik-Ausbau am
Modifier-Stack / Querschnitts-Hook über alle Phasen) und der `on_destroy`-Cluster allein
ist mit 7 GOs so groß, dass er zusammen mit den zwei `on_target`-Sonderfällen ein
S-Aufwand-Paket sprengen würde (Analogie: Paket 4a/4b/4c waren je S–M für 1–3 GOs).
Vorschlag: **Paket 5** = generisches `on_destroy` (größter Hebel, 7 GOs, ein
Querschnitts-Hook statt sieben Einzellösungen); **Paket 6** = `on_set_up` +
die zwei `on_target`-Sonderfälle (kleiner, aber je eigene Mechanik, kein gemeinsamer
Hook — daher eigenes Paket statt Anhängsel an 5).

### 6.3 Tisch-Wurf-Eingabe-Baustein

Die App würfelt nicht. Jede Stelle „Spieler trägt Tischwurf ein" wird **ein** Baustein:
Label-Schema `⟨Wurf⟩ (D6/2D6)`, Zahlenfeld, darunter ein Anker-Slot für wurf-bezogene
GO-Karten (Kompaktform). Gilt für: Morale-Test, Manifest/Deny, Damage-Block — die
Attackenabfolge bekommt so je einen Anker bei Treffer / Verwundung / Rüstung / Rettung /
Schadenszuweisung.

**Gegenbeispiel — Advance/Charge (und jeder andere reine Button-Anker ohne Wertfeld,
z. B. Hit-/Wound-/Save-/Anzahl-Attacken-Re-Roll in der Attackenabfolge):** Diese
Wurf-Arten haben KEINE Werterfassung; statt Tisch-Wurf-Baustein bietet die App nur
(a) den Zustand (Advanced/Charged oder nicht) und (b) ein Inline-Command-Re-Roll-
Angebot (Button, 1 CP, ohne Wertfeld). Dieser Button folgt seit S139 B12c derselben
Fünf-Zustands-Logik wie jede GO-Karte (§6.1): CP-Mangel bleibt weiterhin komplett
unsichtbar (Pull-not-Push — nichts anbieten, das nie klickbar war), aber sobald das
Angebot diese Phase (an IRGENDEINEM seiner Anker, z. B. Hit- **oder** Wound-Reroll)
eingesetzt wurde, bleibt der Button sichtbar: am Anker, der tatsächlich gedrückt
wurde, zeigt er `[↺ Undo]`, an jedem anderen Anker derselben GO/Phase ein
deaktiviertes `Used` — vorher verschwand er dort ersatzlos, ohne Hinweis, dass die GO
schon verbraucht war.

Beispiel — Command Re-Roll beim Deny (aktiver Spieler, Psychic Phase):

```
Deny roll (D6): [ 4 ]
▸ Command Re-Roll · 1 CP                   [Use]     ← bereit, wenn Wert da
```

Ablauf: Wert eintragen → Karte wird „bereit" → `[Use]` bucht 1 CP, Feld öffnet sich für
den neuen Tischwurf → Karte „verwendet" mit `[↺ Undo (+1 CP)]` = Vollrückgängig (alter Wert
+ CP zurück). Gleiches Muster gilt für alle Wurf-GOs außer Advance/Charge (Umsetzung als
Roadmap-Pakete, s. `../goals/backlog.md` §2).

### 6.4 Wortlaut-Konventionen

- **Sprache:** durchgehend Englisch (Ist-Befund: `moralePhase.py` komplett Deutsch,
  Subgruppen-Selector gemischt → Bereinigung als Roadmap-Paket, s. §6.6).
- **Aktions-Vokabular — eine Familie statt vier:** `Use` · `↺ Undo` · deaktiviertes
  `Used` (verwendet-anderswo, s. §6.1 — kein Undo dort) ·
  `Confirm ⟨Aktion⟩` / `Cancel` · Toggle-Auswahl mit `✓`-Präfix (wie Heroische
  Intervention). CP-Kosten stehen bereits im Karten-Header (§6.1) — der Button
  wiederholt sie nicht (S133-D Befund 1: diese Zeile hatte zuvor `Use (N CP)` /
  `↺ Undo (+N CP)` verlangt, ein spec-interner Widerspruch zu den §6.1-Mockups,
  die durchgehend das nackte `[Use]` zeigen — Stakeholder-Entscheid löst ihn
  zugunsten §6.1). „Reset", „Undo deny", „Rückgängig" u. Ä. entfallen zugunsten
  dieser Familie — gilt identisch für Karten- und Inline-Anker (S139 B12c: der
  Inline-Button trägt Name/CP zusätzlich im Label, da er keinen separaten
  Karten-Header hat, s. §6.3).
- **Eine** CP-Anzeige (GameHeader) — keine zweite Doppel-Caption auf der GO-Karte oder im
  Tab.
- **Ein** Stepper-Baustein (`wound_adjustment_buttons` bleibt kanonisch; der Zweitbau in
  `fightPhase.py` wird auf ihn migriert).

### 6.5 Farben

Keine neuen Farb-Token für die GO-Karte — Zuordnung innerhalb des bestehenden Schemas
([`design_colors.md`](design_colors.md)): Zustand „bereit" = **Gold-Primary**-Rahmen
(`--arb-accent`, wie ein ausgewählter Zustands-Button), „ruhend"/„gesperrt" = Secondary
gedimmt (`--arb-muted`). Kein `--arb-go-ready`- o. ä. Sondertoken.

### 6.6 Umsetzung

Die Migration von Bestand (reaktive Box, Inline-Offer, Tab-Schalter) auf die GO-Karte läuft
als Mehr-Session-Roadmap (6 Pakete, S132–S134+) — Details, Reihenfolge und Freigabe-Stand:
[`../goals/backlog.md`](../goals/backlog.md) §2. Jedes Paket geht einzeln durchs
Freigabe-Gate; diese Spec (§6.1–§6.5) ist dabei der Maßstab, gegen den jeder Auftrag
geprüft wird.

## 7. Pflicht-Trigger-Kachel — Explodes-Familie (Entwurf S168, B-028c1)

> **ENTWURF — wartet auf Stakeholder-Abnahme.** Dieser Abschnitt überführt Mockup V3
> (`docs/handoff/S167_MOCKUP_EXPLODES_V3.html`) inkl. der drei S167-Auflagen aus der
> §h-Antwort in `docs/handoff/S166_MOCKUP_EXPLODES.md`. Abnahme-Entscheidung:
> `docs/handoff/S168_SPEC7_ABNAHME.md`. Bei Ablehnung/Korrektur wird dieser Abschnitt
> erneut überarbeitet, bevor B-028c1 in Code geht (Spec-first-Gate, `agent_scopes.md`
> Punkt c).

Fachliche Einordnung (S165-Re-Scope, unverändert): Explodes ist ein **Pflicht-Ereignis**
beim Tod des Modells — kein Verwenden/Nicht-Verwenden-Entscheid, kein `[Use]`, keine CP.
Die GO-Karte (§6.1) ist deshalb die falsche Komponente für den Trigger selbst; §7 baut
aber **ausschließlich aus Bestandskomponenten** — keine neue Bauform, kein neues
Farb-Token. Betroffene Bausteine: GO-Karten-Bauform ohne Aktions-Slot (§6.1), der
Tisch-Wurf-Baustein (§6.3, hier bewusst abgewandelt — s. 7.4), die Hinweis-Konvention
(§3), der Heroic-Intervention-Toggle-Stil (bestehender Code, `chargePhase.py`) und die
unitCard (`src/uiLayout/unitCard.py`).

### 7.1 Aufbau der Kachel-Gruppe

Am Eintrag der zerstörten Einheit erscheint eine Folge von Bausteinen (kein neuer
Container-Typ, jeder Baustein für sich bereits Bestand):

1. **Wurf-Baustein** (§7.4-Abwandlung von §6.3): Titel/Regelname der Fähigkeit +
   Schwellen-Caption, darunter zwei Buttons „Explodes!" (filled) / „Does not explode"
   (outline) statt Zahlenfeld.
2. **`auto_explode`-GO-Karte**, falls das Ziel eine passende Stratagem-Fähigkeit hat:
   Standard-GO-Karte §6.1 direkt neben/unter dem Wurf-Baustein, gleicher Anker. `[Use]`
   ersetzt den Wurf automatisch (Erfolg ohne Würfeln, regelkonform zum Stratagem-Text).
   Titel = `name_en` aus der YAML (z. B. „Curse of the Phaeron",
   `necrons/stratagems.yaml`), **nicht** der technische `effect.type: auto_explode`.
3. **Ziel-Auswahl-Panel** bei Erfolg (Wurf oder Stratagem) — s. 7.2.
4. **EIN Hinweiskasten unter der GO-Karte** (Auflage 1, s. 7.3) mit dem Klartext-Ergebnis.

Anker-Regel: genauso wie jede reaktive Karte (§6.2) — inline am Trigger-Ort, NICHT
Vollbreite, NICHT in der zentralen Stratagems-Liste (die `auto_explode`-GO ist zwar eine
echte GO, ihr Fenster öffnet aber nur reaktiv beim `on_destroy`-Trigger, s. §6.2-Debt-
Tabelle „generisches `on_destroy`").

### 7.2 Ziel-Auswahl-Panel

Reiner Toggle-Zeilen-Stil wie die bestehende Heroic-Intervention-Auswahl
(`chargePhase.py:_render_heroic_intervention`) — **keine Card-Ansicht** für die
Auswahlliste selbst: Gruppenüberschrift je Fraktion, darunter Toggle-Buttons
(`✓`-Präfix bei Auswahl, §6.4-Wortlaut), je ausgewählter Einheit ein Zahlenfeld für den
zugewiesenen Schaden.

**Auflage 3 (wörtlich):** „D6 Mortal Wounds" (bzw. der jeweilige Schadensausdruck aus der
YAML, z. B. `D3`) steht als **eine** Spaltenüberschrift **direkt über der Zahlenfeld-
Spalte** — nicht über der gesamten Liste (V3-Fehler: Header stand über dem ganzen Panel,
aber die Zahlenfelder erscheinen nur inline neben ausgewählten Zeilen und richten sich
dadurch nicht darunter aus). Damit die Überschrift tatsächlich über den Feldern steht,
braucht die Zeile ein festes Zwei-Spalten-Layout (Label-Spalte + fest breite
Zahlenfeld-Spalte), keine variable Flex-Breite wie im Mockup.

Ausgewählte Einheit springt in der zugehörigen armyList-Sidebar (first_player/second_player,
s. 7.5) an die erste Position und zeigt den sinkenden LP-Balken direkt in der unitCard
(Bestandskomponente) — keine zusätzliche Vorschau-/Mini-Karte im Panel. Footer:
„Confirm all" / „Reset" (§6.4-Wortlaut, analog Abschluss der Attackensequenz).

### 7.3 EIN Hinweiskasten (Auflage 1)

Genau **ein** Hinweiskasten, **unter** der GO-Karte (nicht innerhalb des Ziel-Auswahl-
Panels) — er deckt beide Ausgänge ab: Erfolg („⟨Einheit⟩ explodes. Every unit within
⟨Reichweite⟩ suffers ⟨Schadensausdruck⟩ mortal wounds.") und Fehlschlag
(„⟨Einheit⟩ does not explode."). Farbe **Blau**, aber als das, was er ist: ein
**Hinweis** (`info`-Typ, Hinweis-Konvention §3), derselbe `--arb-blue`-Token wie der
bestehende Phasen-Regelkasten (`design_colors.md` Zeile 40) — **kein eigener
„Resolved"-Zustand** und kein neues Token. Der Kasten erscheint, sobald der Wurf/die GO
aufgelöst ist, und bleibt stehen (kein stilles Verschwinden, Grundannahme S166 §a.4) —
er ist aber semantisch ein Hinweistext zum Ausgang, keine dritte Zustandsklasse neben
`info`/`warning`/`success`/`error`.

### 7.4 Bewusste Abweichung von §6.3 — Zwei-Button-Wurf statt Zahlenfeld

§6.3 sieht für jeden Tischwurf ein Zahlenfeld vor. Für das Explodes-Gate weicht §7 davon
ab: zwei Buttons „Explodes!" / „Does not explode" statt Werterfassung. Begründung: der
Explodes-Wurf hat für die App keinen eigenständigen Zahlenwert-Zweck — es zählt nur, ob
die (aus der YAML bekannte) Schwelle erreicht wurde, nicht der genaue Würfelwert selbst
(anders als z. B. beim Deny-Wurf, dessen Wert weiterverrechnet wird). Ein Zahlenfeld plus
Schwellenvergleich wäre hier Mehraufwand ohne Informationsgewinn; der binäre Ausgang ist
die einzige regelrelevante Information. Explizit auf Stakeholder-Wunsch entschieden
(`S166_MOCKUP_EXPLODES.md` §g Korrektur 4, Wortlaut „Does not explode" bestätigt) und hier
dokumentiert statt stillschweigend eingeführt — **kein Präzedenzfall** für andere
Tischwürfe mit tatsächlichem Zahlenwert; §6.3 bleibt dort unverändert Standard.

### 7.5 Layout-Invariante — armyList getrennt von Auswahl/Effekt-Ausführung (Auflage 2)

`src/app.py` teilt die Ansicht in drei Spalten: `left` = `render_army_list(first_player)`,
`center` = `render_game_actions_area()` (+ `render_game_protocoll()`), `right` =
`render_army_list(second_player)`. Die Seitenleisten sind fest an `first_player`/
`second_player` gebunden, nie an `active` (Domänen-Constraint, `CLAUDE.md`) — diese
Bindung bleibt durch §7 **unangetastet**.

Die Pflicht-Trigger-Kachel-Gruppe (7.1) inklusive Ziel-Auswahl-Panel (7.2) und
Hinweiskasten (7.3) rendert **ausschließlich in der `center`-Spalte**, genau wie jede
andere reaktive Karte (§6.2) — nie innerhalb einer der beiden armyList-Sidebars. Das
Mockup V3 stellte Necrons/Orks-Inhalte optisch in zwei nebeneinanderliegenden Spalten
dar, die wie „armyList + Ausführung in derselben Spalte" wirkten; das bildet die reale
App-Struktur nicht ab. In der App gibt es für diesen Ablauf keine „Necron-Spalte" und
keine „Ork-Spalte" — das Ziel-Auswahl-Panel (7.2) zeigt beide Fraktionsgruppen
nebeneinander **innerhalb derselben `center`-Kachel** (Gruppenüberschrift je Fraktion,
s. 7.2), während die beiden armyList-Sidebars unverändert links/rechts weiterlaufen und
nur reaktiv auf Auswahl/Schaden reagieren (LP-Balken, Sortierung an die Spitze).

### 7.6 Wortlaut & Farbe — keine neuen Tokens

- „Explodes!" / „Does not explode" (7.4), „Confirm all" / „Reset" (§6.4) — sonst gilt
  §6.4 unverändert (Englisch, `Use`/`↺ Undo`/`Used`-Familie für die `auto_explode`-GO).
- `DESTROYED` bleibt in der bestehenden unitCard-Farbe (`#c04040`,
  `src/uiLayout/unitCard.py:61`) — keine Änderung, kein neues Token.
- Blau = `--arb-blue`/`--arb-blue-text` (Hinweis-Konvention §3, `design_colors.md`
  Zeile 40) — wiederverwendet, nicht neu vergeben (s. 7.3).

### 7.7 Umsetzung

Nach Abnahme dieses Abschnitts (s. `docs/handoff/S168_SPEC7_ABNAHME.md`): Rückbau des
Engine-Selbstwurfs in `abilityEngine.resolve_mortal_wounds_effect` (Verstoß gegen „Die
App würfelt nicht"), Schema-Erweiterung `effect.type: explode` + `mandatory`-Achse,
`auto_explode`-GO-Anbindung, Wahapedia-Nacherfassung aller Explodes-Träger — Details und
Reihenfolge: `docs/goals/backlog_details.md` B-028c1.
