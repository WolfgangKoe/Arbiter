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
`armyCard._keyword_badge`/`_active_ability_badge`, Invuln-Fragmente in `dice_html`)
denselben `<span>` mit leicht abweichenden Maßen von Hand nach — sie waren bereits
gedriftet. Jetzt liefert `badges.py` die Geometrie zentral; **Farben bleiben am
Call-Site** (sie stammen aus den semantischen Tabellen in `design_colors.md`).

| Builder | Zweck | Konsumenten |
|---|---|---|
| `badge(text, fg, bg, *, margin_right)` | Status / Buff / Debuff / Faction / Army-Ability | `_common._badge`, `unitCard._badge`, `armyCard._keyword_badge` + `_active_ability_badge` |
| `chip(text, fg, bg, border, *, margin_right)` | Keyword-Chip / sekundärer Hinweis | `unitCard._keyword_chip`, `gameActionsArea._display_unit_datasheet` (seit S117/S118) |

Der Invuln-Block (`dice_html.py`, `_render_dice_save_block`) wurde in S116 bewusst
**gestrichen**, nicht auf die Bausteine umgestellt (Commit `143d848`: „Invuln cleanup:
drop active badge + AP/Cover N/A chip from SAVE block"): „active"-Badge und
„AP/Cover N/A"-Hinweis entfielen ersatzlos; übrig bleibt nur die `Inv N+`-Zeile als
eingefärbter `<span>` (Buff-Grün bei ability-basiertem Invuln) — kein
`badge()`/`chip()`-Aufruf. Der Backlog-Befund S78 (drei lose HTML-Fragmente, Z. 129)
ist damit durch Streichung erledigt. *(Korrigiert S120, 2026-07-03 — die frühere
Formulierung „baut das Label aus diesen Bausteinen" beschrieb einen nie gebauten Stand.)*

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

**Schritt 2 (S117/S118) abgeschlossen:** Rollout auf die restlichen 10 Produktivdateien
(`_common.py`, `chargephase.py`, `moralePhase.py`, `shootingPhase.py`, `fightPhase.py`,
`commandPhase.py`, `psychicPhase.py`, `gameActionsArea.py`, `gameHeader.py`,
`setupScreen.py`) — alle `▶ ◀ ▷ ✓ ✕ ＋ ⚔ ↺`-Literale in Code-Ausdrücken auf die
`symbols.py`-Konstanten gezogen, dazu die Keyword-Chip-Stelle in
`gameActionsArea._display_unit_datasheet` auf `chip()` migriert. Bewusste Ausnahmen bleiben
Literal, kein Ratchet-Anspruch: `gameHeader._phase_badges_html` (eigene dritte
Geometrie-Klasse, kein Badge im Sinne von §1.1), `dice_compose._badge_chip` (S115 bereits
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

Vier Zustände ersetzen das bisherige plötzliche Auftauchen der reaktiven Box:

| Zustand | Wann | Darstellung |
|---|---|---|
| ruhend | Trigger (noch) nicht erfüllt | sichtbar, gedimmt, `[Use]` disabled |
| bereit | Trigger erfüllt, CP reichen | hervorgehoben (Gold-Primary, s. §6.5), `[Use]` aktiv |
| verwendet | Use gedrückt, Fenster noch offen | `[↺ Undo (+N CP)]` statt `[Use]` |
| gesperrt | CP fehlen / Voraussetzung weg | gedimmt, Grund als Suffix im Header |

Undo ist überall **Vollrückgängig** (CP zurück, Effekt/Wert zurück), solange das
Aktivierungsfenster offen ist — der Schiedsrichter-Moment kommt erst am Phasen-/Zug-/
Rundenende, nicht bei jedem Klick (App ist Erinnerer/Entscheidungshelfer, würfelt selbst
nicht — Regel bleibt unverändert gegenüber dem Bestand).

### 6.2 Orte-Zuordnung (aus der GO-Klassifikation, Achse b)

| Klassifikation (Achse b) | Ort | Form |
|---|---|---|
| spielweit (12 GOs, `before_battle`) | Liste im ArmySetup, vor „Start Game" | Vollform |
| phasenweit/proaktiv (~22) | zentrale Stratagems-Liste (Spielerseite) | Vollform |
| bei_ereignis (~45) | zentrale Liste (ruhend) **+** Inline-Anker am auslösenden Schritt | Voll + Kompakt |
| vor_wurf / nach_wurf (11) | Inline-Anker direkt an der Wurf-Eingabe | Kompakt |

Die zentrale Liste ist der **Planungs-Überblick** („was habe ich diese Phase?"), der
Inline-Anker die **Erinnerung am Ort des Geschehens** — beide rendern dieselbe Karte aus
derselben Buchhaltung (`spend_stratagem`-Pipeline), nichts wird doppelt gebucht. Damit ist
auch der `before_battle`-Sichtbarkeitsfix (13 GOs matchen `PHASES` heute nie) konzeptionell
gelöst: eigener Ort statt Sonderphase. Achse (b) und die vollständige 95-GO-Tabelle:
[`../reference/go_klassifikation.md`](../reference/go_klassifikation.md).

### 6.3 Tisch-Wurf-Eingabe-Baustein

Die App würfelt nicht. Jede Stelle „Spieler trägt Tischwurf ein" wird **ein** Baustein:
Label-Schema `⟨Wurf⟩ (D6/2D6)`, Zahlenfeld, darunter ein Anker-Slot für wurf-bezogene
GO-Karten (Kompaktform). Gilt für: Morale-Test, Manifest/Deny, Damage-Block — die
Attackenabfolge bekommt so je einen Anker bei Treffer / Verwundung / Rüstung / Rettung /
Schadenszuweisung.

**Gegenbeispiel — Advance/Charge:** Diese Wurf-Arten haben KEINE Werterfassung; statt
Tisch-Wurf-Baustein bietet die App nur (a) den Zustand (Advanced/Charged oder nicht) und
(b) ein Inline-Command-Re-Roll-Angebot (Button, 1 CP, ohne Wertfeld).

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
- **Aktions-Vokabular — eine Familie statt vier:** `Use (N CP)` · `↺ Undo (+N CP)` ·
  `Confirm ⟨Aktion⟩` / `Cancel` · Toggle-Auswahl mit `✓`-Präfix (wie Heroische
  Intervention). „Reset", „Undo deny", „Rückgängig" u. Ä. entfallen zugunsten dieser
  Familie.
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
