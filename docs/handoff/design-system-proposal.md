STATUS: NEEDS-DECISION
Lebensdauer: dauerhaft bis Stakeholder-Entscheidung, danach in `docs/spec/design_system.md` (falls
beschlossen) überführen und diese Datei löschen.

# Design-System — Research & Vorschlag (read-only Bestandsaufnahme)

> Erstellt von Subagent "Sonnet sucht" (Design-System-Crew). Keine Code-Änderung, keine
> Farb-/Design-Entscheidung getroffen — nur Bestandsaufnahme + Optionen + Empfehlung.

## 1. Komponenten-Inventar (echte Fundstellen)

### 1.1 Badge — 4 unabhängige Implementierungen

Alle vier bauen denselben CSS-Grundtyp (`<span style="background:…;border:1px solid …;
border-radius:…;padding:…;font-size:…;color:…">`), aber **keine ruft die anderen auf** —
reine Code-Klone mit leicht abweichenden Werten:

| Funktion | Datei:Zeile | border-radius | padding | font-size | Zweck |
|---|---|---|---|---|---|
| `_badge()` | `src/uiLayout/_common.py:132` | 2px | `1px 6px` | 10px | Status-Badges im Group-Flow (MOVED, SHOT, Buff …) |
| `_badge()` | `src/uiLayout/unitCard.py:64` | 2px | `1px 6px` | 10px | Status-Badges auf der unitCard — **eigene Kopie derselben Logik**, eigene `_BADGE_COLORS`-Tabelle (Z. 44) |
| `_keyword_badge()` | `src/uiLayout/armyCard.py:52` | 2px | `2px 8px` | 10px | Faction-/Subfaction-Badge |
| `_active_ability_badge()` | `src/uiLayout/armyCard.py:60` | 2px | `2px 8px` | 10px | Army-Ability-Badge (hardcoded Buff-Grün) |
| `_keyword_chip()` | `src/uiLayout/unitCard.py:124` | 2px | `1px 5px` | 9px | Keyword-Chips (highlighted/normal) |
| `_badge_chip()` | `src/uiLayout/dice_compose.py:151` | 3px | `1px 5px` | 11px | Würfel-Modifier-Label |

**Befund:** `_common.py:_badge()` und `unitCard.py:_badge()` sind **textuell fast identisch**
(gleiche `_BADGE_COLORS`-Werte, ein Kommentar in `_common.py:106` dokumentiert sogar explizit,
dass die beiden Tabellen schon mal auseinandergedriftet sind — MOVED/Buff waren vertauscht).
Das ist exakt das Wiederholungsmuster, das ein gemeinsamer Helfer lösen würde — aktuell **zwei
Quellen der Wahrheit für dieselbe Badge-Familie**, mit Trivia-Unterschied: `unitCard.py` hat
zusätzlich `HEROIC INT.` als Key in `_BADGE_COLORS` (Z. 55), `_common.py` rendert das Badge
stattdessen über variant-Pfad — zwei Wege zum selben visuellen Ergebnis.

`armyCard.py` und `dice_compose.py` bauen das Badge-HTML nochmal komplett neu, mit jeweils
eigenen Maßen (Padding, Radius, Font-Size weichen leicht ab). Visuell minimal unterschiedlich,
aber im Code vier separate Wartungsstellen für "ein Badge rendern".

### 1.2 Invuln-SAVE-Badge-Bereich — konkret chaotisch (bestätigt Backlog-Befund S78)

`src/uiLayout/dice_html.py:188-204` (`_render_dice_save_block`): das Invuln-Label wird aus drei
separat gebauten String-Fragmenten zusammengeklebt — kein einheitlicher Badge-Baustein:

```python
active_badge = f'<span style="...">active</span>' if using_invuln else ""
note = '<span style="...">AP/Cover N/A</span>'
inv_label = f"Inv {invuln}+{active_badge}{note}"
```

Drei optisch unterschiedliche Elemente (Klartext-Label + Mini-Badge "active" + Mini-Hinweis
"AP/Cover N/A") in einer Zeile — genau der im Backlog (`docs/goals/backlog.md:129`) dokumentierte
Befund: *"Zeigt drei Teile (\"Inv 4+\", \"active\", \"AP/Cover N/A\"), die teils keinen Sinn
ergeben. Soll: eine klare Badge."*

### 1.3 Card / Panel (`st.container(border=True)`)

Verwendet in 4 Dateien (`gameHeader.py`, `unitCard.py`, `_common.py`, `armyCard.py`), aber
**ohne gemeinsamen Wrapper** — jede Stelle setzt eigene Inhalte direkt hinein. Kein Befund von
visueller Inkonsistenz hier (Streamlit liefert den Rahmen einheitlich über CSS-Selektor
`.e1rw0b1u3`, siehe `CLAUDE.md`), aber auch keine Stelle kapselt "Card mit Titel + Badges +
Inhalt" als wiederverwendbares Muster — jeder Aufrufer baut die interne Struktur (Titel,
Badge-Zeile, Caption) von Hand neu (z. B. `_common.py:341-352` vs. `unitCard.py` card-Aufbau).

### 1.4 Hinweis/Caption (`st.info`/`st.warning`/`st.success`/`st.error`)

33 Treffer über die fünf `*Phase.py`-Dateien (`grep` siehe oben), durchgehend über Streamlits
native Komponenten — **keine eigene HTML/CSS-Wartungsstelle**, also kein Inkonsistenz-Befund.
Aber: keine Konvention, wann `info` vs. `warning` vs. `success` für denselben Sachverhalt
verwendet wird (z. B. "Power failed" ist in `psychicPhase.py:304` `warning`, "Deny failed" in
`psychicPhase.py:399` ebenfalls `warning`, aber "Perils — power failed" in `psychicPhase.py:275`
ist `error`) — eher ein Stilfragen-Kandidat als ein Bug, kein dringender Fall.

### 1.5 Tabelle/Grid (Würfel-Block)

`dice_compose.py:179` `grid_row_html()` ist bereits ein etablierter, wiederverwendeter Baustein
(Label-Spalte + Inhalts-Spalte) — gutes Gegenbeispiel: hier existiert schon EIN Helfer, der
durchgängig genutzt wird (`_render_dice_save_block`, `_render_dice_wound_block` etc.). Zeigt: das
Muster "ein Helfer, mehrfach genutzt" funktioniert im Projekt bereits, wo es eingeführt wurde —
bei Badges fehlt genau dieser Schritt.

### 1.6 Button-Gruppen

Kein eigener HTML-Helfer nötig (native `st.button` + `st.columns`), aber Beschriftungs-Symbole
(`▶`/`◀`, `✓`/`✕`, `＋`) werden an vielen Stellen inline als Literal wiederholt
(`_common.py:340,404,1430` u. a.) statt aus einer kleinen Symbol-Konstante referenziert zu
werden. Geringe Priorität, aber ein Token-Kandidat (siehe unten).

## 2. Token-Kandidaten (jenseits Farbe — Vorschlag, keine Festlegung)

Aktuell ist NUR Farbe als Token verbindlich (`design_colors.md`, CSS-Variablen `--arb-*` in
`gameHeader.py:12-24`). Spacing/Radius/Font-Size sind überall Magic Numbers. Kandidaten, falls
der Nutzer ein Mini-Set will (bewusst klein gehalten — keine 20-stufige Skala):

| Token-Kategorie | Beobachtete Ist-Werte | Vorschlag (Diskussionsbasis) |
|---|---|---|
| Badge border-radius | 2px / 3px / 4px (siehe 1.1) | EIN Wert, z. B. 2px (häufigster Ist-Wert) |
| Badge padding | `1px 5px` / `1px 6px` / `2px 8px` | 2 Stufen: "klein" (Keyword-Chip) / "normal" (Status-Badge) |
| Badge font-size | 9px / 10px / 11px | an Badge-Größe koppeln (klein=9-10px, normal=10px) |
| Card/Panel border-radius | 2px (durchgängig in `gameHeader.py`) | bereits konsistent — kein Handlungsbedarf |
| Symbol-Konstanten | `▶◀✓✕＋⚔↺` als Inline-Literale | kleine `_symbols.py`-oder Konstanten-Sektion in `_common.py` |

Spacing-Skala (Margins zwischen Badges, Blockabständen) wurde NICHT systematisch als
Schmerzpunkt gefunden — `margin-right: 2px/3px/4px` variiert leicht zwischen den Badge-Familien,
aber das ist eine Konsequenz der fehlenden gemeinsamen Badge-Funktion, kein separates Problem.

## 3. UX-Mängel aus dem Backlog (reale, bereits dokumentierte Fälle)

Direktes Zitat aus `docs/goals/backlog.md`:

- **Z. 129:** *"Invuln-SAVE-Badge-Bereich chaotisch (S78): Zeigt drei Teile (\"Inv 4+\",
  \"active\", \"AP/Cover N/A\"), die teils keinen Sinn ergeben. Soll: eine klare Badge, z. B.
  \"Invuln 4+\". Überschneidet sich mit Plan 017 (SAVE-Block Fähigkeit+AP kombinierte Badge)."*
  → bestätigt in `dice_html.py:188-204` (siehe 1.2).
- **Z. 130:** *"Dice-Display Modifier-Geometrie (Befund B/C, S78): HIT/WOUND-Debuff spreizt
  nicht mit der Magnitude … SAVE-Geometrie ist korrekt."* — geometrisches Problem, kein
  Badge-/Token-Problem, aber zeigt: dieselbe Komponentenfamilie (`modifier_die_pair_html`) hat
  in HIT/WOUND vs. SAVE unterschiedliches Verhalten trotz gemeinsamer Funktion — ein Indiz, dass
  auch etablierte Helfer parametrisch auseinanderlaufen können, wenn die Variante nicht explizit
  spezifiziert ist.
- **Z. 119:** *"SAVE-Block: Fähigkeit + AP als eine Badge (\"Enslaved AP-1\") — YAML-Erweiterung
  (→ Plan 017)."* — ein weiterer Beleg für "mehrere Badges sollten zu einer kombiniert werden",
  dasselbe Muster wie der Invuln-Befund.

Diese drei Backlog-Einträge sind bereits als Plan-017-Kandidat gebündelt — ein Design-System
mit EINEM Badge-Helfer würde die Wurzelursache (vier verschiedene Badge-Bauweisen) für alle drei
gleichzeitig adressieren, statt jeden einzeln zu flicken.

## 4. Vorschlag: Struktur für `docs/spec/design_system.md`

Analog zu `design_colors.md` aufgebaut (Governance-Satz zuerst, dann Tabellen):

```
# Design-System — verbindlich

> Regel: Design-Entscheidungen trifft der Nutzer (wie Farbe, design_colors.md).

## 0. Governance
(Verweis auf design_colors.md als Vorbild; gleiche Spielregel)

## 1. Komponenten-Inventar
Je Komponente: Name, Soll-Aussehen je Zustand (Tabelle: Zustand → visuelle Eigenschaft),
kanonischer Helfer (Datei:Funktion), Verbraucher (wer ruft ihn auf).
  1.1 Badge (Status / Buff-Debuff / Keyword / Faction)
  1.2 Card/Panel
  1.3 Block-Divider / Grid-Row (bereits etabliert, nur dokumentieren)
  1.4 Hinweis (info/warning/success/error) — Konvention, wann welcher Typ

## 2. Token-Tabelle (minimal)
| Token | Wert | Verwendung |
(analog --arb-* in design_colors.md, aber für Radius/Padding/Font-Size der Badges)

## 3. Migrations-Hinweis
Welche Alt-Implementierungen (_common._badge, unitCard._badge, armyCard._keyword_badge,
dice_compose._badge_chip) auf den neuen Helfer umgestellt werden, wenn berührt — kein
Big-Bang-Rewrite, sondern "beim nächsten Anfassen konsolidieren".
```

## 5. Vorschlag: phasierter erster Schritt (klein, Clean-Code-konform)

Begründung für die Reihenfolge: Clean-Code-Regel "erst ab der dritten Wiederholung
abstrahieren" ist beim Badge **bereits klar überschritten** (4 Implementierungen) — das ist kein
Over-Engineering, sondern überfällige Konsolidierung. Bei Card/Panel und Hinweis-Typen ist die
Schwelle dagegen NICHT erreicht (keine echte Diskrepanz gefunden) — dort lohnt sich aktuell nur
Dokumentation, keine Code-Änderung.

**Schritt 1 (klein, jetzt):**
1. Komponenten-Inventar in `docs/spec/design_system.md` anlegen — nur Bestandsaufnahme + die vom
   Nutzer getroffenen Token-Entscheidungen (kein Code).
2. EINEN Badge-Helfer konsolidieren: `_common._badge()` und `unitCard._badge()` zusammenführen
   (sie sind heute schon fast identisch — geringstes Risiko, größter Nutzen, behebt direkt die im
   Code dokumentierte Drift-Gefahr aus `_common.py:106`).
3. Den Invuln-SAVE-Badge-Bereich (`dice_html.py:188-204`) auf den konsolidierten Helfer umstellen
   — löst gleichzeitig den Backlog-Befund Z. 129.

**Bewusst NICHT in Schritt 1:**
- `armyCard._keyword_badge`/`_active_ability_badge` und `dice_compose._badge_chip` anfassen —
  warten, bis Ziel7 (Gefechtsoptionen-UI) dort ohnehin Code berührt; dann im selben Zug auf den
  konsolidierten Helfer ziehen statt isoliertem Refactor-Commit.
- Card/Panel-Helfer bauen — keine echte Inkonsistenz gefunden, nur Doku nachziehen.
- Spacing-Skala / Symbol-Konstanten — Nice-to-have, kein dokumentierter Schmerzpunkt, auf später
  verschieben.

**Mit Ziel7 mitwachsend (später, iterativ):** sobald die Gefechtsoptionen-UI neue Badges/Cards
braucht, werden sie direkt gegen den (dann etablierten) Helfer gebaut statt eine fünfte Kopie zu
erzeugen — das Inventar in `design_system.md` wird bei jedem Anfassen um den neuen
Komponentenfall ergänzt (Ratchet-Prinzip, analog Rule-Catalog-Gate).

## 6. Offene Entscheidungen für den Nutzer (NICHT vom Subagenten zu treffen)

1. **Soll `docs/spec/design_system.md` überhaupt angelegt werden** — oder reicht eine kleinere
   Ergänzung in `design_colors.md` (z. B. neuer Abschnitt "§5 weitere Tokens")? Die Spec-Struktur
   oben ist ein Vorschlag, kein Muss.
2. **Token-Werte selbst** (Tabelle in Abschnitt 2): welcher Radius/welches Padding/welche
   Font-Size wird der EINE verbindliche Wert je Badge-Klasse? Aktuell drei Kandidaten je Token
   beobachtet (siehe Tabelle Abschnitt 2) — der Subagent schlägt bewusst keinen davon als
   Entscheidung vor.
3. **Reihenfolge/Umfang des ersten Schritts**: ist die vorgeschlagene Beschränkung auf
   `_common._badge` + `unitCard._badge` + Invuln-Block richtig geschnitten, oder soll z. B. auch
   `armyCard.py` schon in Schritt 1 mit rein (höheres Risiko/größerer Diff, aber alles auf einmal
   konsolidiert)?
4. **Symbol-Konstanten** (▶◀✓✕＋⚔↺): lohnt sich eine zentrale Konstantenliste, oder ist das zu
   kleinteilig für ein eigenes Token?
5. **Hinweis-Konvention** (`info`/`warning`/`success`/`error`): soll es überhaupt eine
   verbindliche Regel geben (z. B. "Fehlschlag immer `warning`, nur echte Spielregel-Verletzung
   `error`"), oder ist die aktuelle uneinheitliche Verwendung tolerierbar (kein HTML-Risiko, da
   native Streamlit-Komponente)?

---

*Hinweis: Dieser Bericht trifft keine Farb- oder Layout-Entscheidung. Alle Hex-Werte/Maße oben
sind Ist-Zustand-Zitate aus dem Code, keine Empfehlung des Subagenten.*
