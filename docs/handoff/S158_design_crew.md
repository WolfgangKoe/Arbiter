STATUS: NEEDS-DECISION

# S158 — Design-Crew-Konzept: B-104 / B-105 / B-111 (Würfelblock-Optik)

Reiner Konzept-Vorschlag, keine Code-/Spec-Änderung. Grundlage: `docs/goals/backlog_details.md`
(B-104/B-105/B-111), `docs/spec/design_system.md`, `docs/spec/design_colors.md`, Ist-Code
`src/uiLayout/diceHtml.py` + `src/uiLayout/diceCompose.py`.

## Grundannahmen (PFLICHT — bitte zuerst bestätigen)

Diese drei Punkte sind das Weltbild, auf dem alle Varianten unten aufbauen. Wenn eines davon
nicht stimmt, sind die Detail-Varianten hinfällig und müssen neu gedacht werden.

1. **B-104 — wo sitzt das ✕:** Es geht NUR um die zusätzliche Marker-Zeile unter dem
   Würfel-Grid (`diceCompose._marker_row_html`, aufgerufen von `always_fail_marker_row_html`),
   die aktuell pro Auto-fail-Spalte ein nacktes `<span>✕</span>` zeigt. Die eigentlichen
   Würfel-SVGs im Grid selbst (`dice_row_html`, Erfolg/Miss) bleiben unverändert — dort ist das
   Miss-✕ bereits ein echtes Würfelsymbol (`dice_face_svg(1, miss=True)`/`miss_die_html`). Das
   Backlog-Item will die Marker-Zeile an dieses bereits etablierte Muster angleichen, nicht die
   Würfel-SVGs selbst ändern.
2. **B-105 — was „GO-Referenz" fachlich bedeutet:** ein sichtbarer **Namens-Bezug** (Chip/Badge
   mit dem GO-Namen, z. B. „Quantum Deflection") direkt neben/an dem Würfelwert, der aus dieser
   GO stammt — keine Tooltip-Lösung, kein Klick-Aufklappen, kein Regeltext (der bleibt Sache der
   GO-Karte selbst, `design_system.md` §6.1). Reine Kennzeichnung „dieser Wert kommt von X". Der
   Mechanismus existiert bereits zweimal unabhängig im Code (`_strength_source_badge_html` für
   Strength-Buffs, `label`-Parameter in `always_fail_marker_row_html` für Auto-fail) — beide
   sind schon exakt „GO-Referenz an Würfelblock", nur nicht als ein Baustein benannt. Betroffen
   ist zusätzlich der **Invuln-Save-Row** (`_render_dice_save_block`), der aktuell `Inv N+` ohne
   jeden Namensbezug zeigt (das S155-Beispiel „Quantum Deflection" spielt genau dort).
3. **B-111 — welcher Badge-Kontext:** das bestehende `diceCompose._badge_chip`-Element (linke
   Spalte im Grid-Row), NICHT der gemeinsame `badges.py`-Builder aus `design_system.md` §1.1.
   `_badge_chip` ist dort bereits explizit als eigenständige, bewusst getrennte Geometrie
   dokumentiert („feste Spaltenbreite + Ellipsis-Truncation, kein Status-Badge"). Die
   Truncation, die den Bug erzeugt, sitzt in genau diesem Baustein (`max-width: 88px`,
   `white-space:nowrap`, `text-overflow:ellipsis` — Zeile 159–168 `diceCompose.py`). Die Lösung
   ändert diesen Baustein selbst (oder eine benannte Variante davon), nicht das globale
   `badges.py`.

Alle drei Items betreffen denselben Rendering-Bereich (`diceHtml.py`/`diceCompose.py`,
Attackenauflösung) — Backlog nennt bereits die Möglichkeit, sie gemeinsam umzusetzen.

---

## B-104 — Würfelsymbol statt nacktem ✕

**Ist:** `_marker_row_html` (diceCompose.py:377–397) rendert je Slot
`<span style="color:{color};font-weight:bold;">✕</span>` — reiner Text-Glyph, kein
Würfelsymbol. `_AUTO_FAIL_GLYPH = SYM_CROSS` (design_system.md §4).

### Variante A — bestehenden Trigger-Die-Chip wiederverwenden (empfohlen)

`diceCompose._triggered_die_chip_html(content, color)` existiert bereits (Zeile 430–437): ein
30×30px umrandetes Kästchen, exakt für kurze Inhalte in einem Würfel-Slot gebaut (aktuell für
„AP-1" bei `value_triggered_die_row_html` genutzt). `_marker_row_html` übergibt statt des
bloßen Glyphen `_triggered_die_chip_html(SYM_CROSS, color)`:

```html
<span style="display:inline-block;width:30px;height:30px;line-height:30px;
  border:1.5px solid {color};border-radius:4px;background:#1e293b;
  font-size:14px;font-weight:700;color:{color};text-align:center;">✕</span>
```

Farbe kommt unverändert aus `_modifier_color`/`color_hint` (Buff-Grün/Debuff-Rot aus
`design_colors.md`). Nur EIN Call-Site-Wechsel in `_marker_row_html`, keine neue Geometrie.

### Variante B — echtes Würfel-SVG (dice_face_svg-Familie erweitern)

`dice_face_svg(1, miss=True)`/`miss_die_html()` zeichnen bereits ein echtes SVG-Würfelgesicht
mit ✕ (grauer Rahmen, rotes Kreuz, fix). Für B-104 müsste die Rahmen-/Kreuzfarbe parametrisierbar
werden (aktuell hart `#374151`/`#c0392b`), damit Buff-Grün vs. Debuff-Rot (Perspektive) möglich
bleibt. Optisch am nächsten am „echten" Würfel-Look, aber Eingriff in eine Funktion, die auch an
anderen Stellen (impossible-threshold-Miss, Wert-1-Miss) mit fixen Farben verwendet wird —
größeres Risiko, dort versehentlich etwas zu verschieben.

### Variante C — nur optisches Polster um den bestehenden Glyph (Budget-Variante)

Glyph bleibt Text, bekommt aber einen kreisförmigen/quadratischen Rahmen-Hintergrund
(`border-radius:50%` o. ä.) statt reinem `<span>`. Günstigster Eingriff, trifft aber die
Formulierung „Würfelsymbol mit ✕ darin" nur näherungsweise — kein echtes Würfel-Quadrat wie bei
den Dice-Grids darüber.

**Empfehlung:** Variante A — nutzt einen bereits im Code vorhandenen, für genau diesen Zweck
gebauten Baustein (`_triggered_die_chip_html`), ein Call-Site-Wechsel, keine neue Farb-/Geometrie-
Entscheidung nötig.

**Vorschlag Spec-Abschnitt:** neuer `design_system.md` §1.4 „Würfel-Slot-Marker-Chip" —
dokumentiert `_triggered_die_chip_html` als kanonischen Baustein für JEDE kurze Inhalts-Anzeige
in einem Würfel-Slot (AP-Wert, Auto-fail-✕, künftig ggf. Reroll-↺) statt bloßer Text-Glyphen.

---

## B-105 — GO-Referenz an Würfelblöcken (generisch)

**Ist:** Zwei unabhängige Ad-hoc-Umsetzungen desselben Bedürfnisses existieren bereits:
`_strength_source_badge_html` (diceHtml.py:83–95, grüner Chip neben S-vs-T bei Strength-Buffs)
und der `label`-Parameter von `always_fail_marker_row_html` (Auto-fail-Zeile, B-103/B-109). Der
Invuln-Save-Row (`_render_dice_save_block`, diceHtml.py:250–260) hat dagegen **keinen**
Namens-Bezug — nur `Inv N+` in Buff-Grün, ohne zu sagen welche GO das war (S155-Befund-Beispiel
Quantum Deflection).

### Variante A — einen generischen „GO-Quellen-Chip" extrahieren (empfohlen)

`_strength_source_badge_html` wird zu einem allgemeinen `go_source_chip(label, color)` in
`diceCompose.py` verallgemeinert (gleiche Optik: Buff-Grün-Rahmen-Chip, aber Farbe über
`_modifier_color`/`color_hint` statt hart `_BUFF_COLOR_HEX`, damit auch Debuff-GOs wie Quantum
Shielding denselben Chip nutzen können). Aufrufstellen: (a) Strength-Buff (bestehend), (b)
Invuln-Row (neu — GO-Name neben `Inv 4+`), (c) jeder künftige Würfelwert mit GO-Ursprung.

```html
Inv 4+  [Quantum Deflection]
```

(Chip-Optik identisch zum bestehenden Strength-Buff-Chip, nur Farbe je nach `color_hint`.)

### Variante B — GO-Name in die linke Grid-Label-Spalte statt als Inline-Chip

Statt eines Inline-Chips NACH dem Wert wandert der GO-Name in die linke `grid_row_html`-Spalte
(wie es `always_fail_marker_row_html` bereits für die Auto-fail-Zeile tut — der Name ERSETZT
dort „Auto-fail" als Zeilen-Label). Für den Invuln-Row hieße das: linke Spalte zeigt
„Quantum Deflection" statt leer, rechte Spalte den Würfel-Wert. Konsistent mit der Auto-fail-
Zeile, aber stilistisch anders als der bestehende Strength-Buff-Chip (der bleibt inline).
Zwei visuelle Muster im selben Würfelblock (Label-Spalte vs. Inline-Chip) wären die Folge, wenn
nicht beide bestehenden Stellen mit-vereinheitlicht werden.

### Variante C — reiner Text-Suffix, kein Chip (Budget-Variante)

`Inv 4+ (Quantum Deflection)` in gedämpftem Grau, ohne Chip-Rahmen. Günstigster Eingriff, aber
bricht mit der Chip-Sprache, die an den zwei bestehenden Stellen (Strength-Buff, Auto-fail-Label)
bereits etabliert ist — Inkonsistenz innerhalb desselben Würfelblocks.

**Empfehlung:** Variante A — führt die zwei bereits bestehenden, unabhängig gewachsenen
Ad-hoc-Lösungen zu EINEM Baustein zusammen (DRY) und deckt den fehlenden Invuln-Fall in
derselben Bewegung ab, ohne ein neues visuelles Muster einzuführen.

**Vorschlag Spec-Abschnitt:** neuer `design_system.md` §1.5 „GO-Quellen-Chip an Würfelwerten" —
dokumentiert `go_source_chip()` als kanonischen Baustein für jeden Würfelwert, der aus einer
aktiven GO/Ability stammt; Farbe folgt `_modifier_color`/`color_hint` (Buff-Grün/Debuff-Rot,
`design_colors.md` §0), kein neues Token.

---

## B-111 — Quantum-Shielding-Badge-Truncation

**Ist:** `_badge_chip` (diceCompose.py:159–168) begrenzt jedes Label auf
`max-width: {_BADGE_COL_W - 8}px` = 88px mit `white-space:nowrap` + `text-overflow:ellipsis`.
„Quantum Shielding" (17 Zeichen bei 11px) wird zu „Quantum Sh…" abgeschnitten — der B-103-Fix
(korrektes Label statt „Auto-fail") wird dadurch in der Wirkung wieder unlesbar.

### Variante A — Zeilenumbruch statt Truncation, nur für diesen Badge-Typ (empfohlen)

`_badge_chip` bekommt einen optionalen `wrap: bool`-Parameter (Default `False`, bestehendes
Verhalten unverändert für alle anderen Aufrufer wie AP-/Cover-Modifier-Badges, die kurz genug
sind). Bei `wrap=True` (genutzt von `always_fail_marker_row_html`) entfällt `white-space:nowrap`
und `text-overflow:ellipsis`, `max-width` bleibt als Breiten-Obergrenze der Spalte erhalten —
das Label bricht auf eine zweite Zeile um, die Zeile wächst nur vertikal (kein Spaltenumbau,
keine Kollision mit den Würfel-Slots rechts):

```
[Quantum
 Shielding]
```

### Variante B — Spaltenbreite `_BADGE_COL_W` global erhöhen

`_BADGE_COL_W` (aktuell 96px) wird erhöht, bis „Quantum Shielding" einzeilig passt (~130–140px
geschätzt). Erfüllt „volle Label-Breite" wörtlich, aber `_BADGE_COL_W` ist die gemeinsame linke
Spalte JEDES Grid-Rows im gesamten Würfelblock (HIT/WOUND/SAVE-Modifier, Eff.-Zeile, Auto-fail,
Reroll) — eine globale Erhöhung verschiebt die Würfel-Slots aller Zeilen nach rechts und ändert
die Optik überall, nicht nur an der einen betroffenen Stelle. Größerer Blast-Radius als nötig.

### Variante C — Truncation behalten, volles Label per `title`-Attribut (Hover)

`_badge_chip` bekommt zusätzlich `title="{label}"` am `<span>` — das volle Label erscheint als
Tooltip bei Hover, sichtbarer Text bleibt abgeschnitten. Günstigster Eingriff (eine Zeile), löst
das Problem aber nur für Maus-Nutzer und weicht von der Backlog-Formulierung „volle Breite ODER
Zeilenumbruch" ab (keine der beiden genannten Optionen).

**Empfehlung:** Variante A — trifft exakt eine der zwei vom Stakeholder selbst im Backlog-Item
genannten Optionen (Zeilenumbruch), betrifft nur den einen Aufrufer mit langen Labels (Auto-fail/
GO-Referenz-Chips aus B-105), lässt die Spaltenbreite für alle anderen, bereits kurzen Badges
(AP-2, MWBD, Reroll) unangetastet.

**Vorschlag Spec-Abschnitt:** Ergänzung in `design_system.md` §1.1 an der bestehenden Stelle zu
`diceCompose._badge_chip` („eigene Sonder-Geometrie… bleibt eigenständig") — ein Satz, dass lange
GO-/Keyword-Labels (Auto-fail-Label, GO-Quellen-Chip aus B-105) die `wrap=True`-Variante nutzen,
statt eine zweite Truncation-Konvention einzuführen.

---

## Interaktion der drei Items

B-105 (GO-Quellen-Chip) und B-111 (Wrap-fähiger `_badge_chip`) hängen zusammen: Wenn B-105
Variante A den GO-Namen zusätzlich in der Auto-fail-/Invuln-Zeile als Chip zeigt, braucht dieser
Chip denselben Wrap-Schutz aus B-111 Variante A — sonst reproduziert B-105 den B-111-Bug an
einer weiteren Stelle. Empfehlung: B-111 (Wrap-Fähigkeit in `_badge_chip`) zuerst oder im selben
Schritt wie B-105 umsetzen.

## Offene Fragen an den Stakeholder

1. Grundannahmen (oben) bestätigt? - Ja, dürfte passen.
2. B-104: Variante A (Trigger-Die-Chip wiederverwenden) oder B (echtes SVG, mehr Eingriff)? - A
3. B-105: Variante A (ein generischer `go_source_chip`, Inline neben dem Wert) oder B
   (GO-Name wandert in die linke Label-Spalte, wie bei Auto-fail bereits)? - A
4. B-111: Variante A (Zeilenumbruch, nur für lange Labels) bestätigt, oder soll stattdessen die
   Spaltenbreite global wachsen (Variante B)? - C
5. Sollen B-104/B-105/B-111 als EIN gemeinsamer Executor-Auftrag eingeplant werden (Backlog
   erwähnt das als Option), oder getrennt? Das kommt auf die Größe der Tasks an. Ich würde hier für jede Task einen Subagenten starten und diese nach Möglichkeit parallel laufen lassen.
