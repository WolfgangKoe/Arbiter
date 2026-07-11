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
TRANSPORT-Tod, Hit-/Wound-/Save-Anker × `on_target` (effect_type-gescoped), `after_roll`
via Advance-/Charge-/Psychic-/Damage-/Anzahl-Attacken-/Hit-/Wound-/Save-Anker (S136
Stufe 2)):

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
Efficient Disintegration, Shadows of Drazak (Hit-Anker, Paket 4a), Whirling Onslaught
(Wound-Anker, Paket 4a), Quantum Deflection (Save-Anker, Paket 4b).

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
  (`unit_mutations.py`, `combat.py`, Morale-Verluste), nicht nur an einen einzelnen
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
- **Aktions-Vokabular — eine Familie statt vier:** `Use` · `↺ Undo` ·
  `Confirm ⟨Aktion⟩` / `Cancel` · Toggle-Auswahl mit `✓`-Präfix (wie Heroische
  Intervention). CP-Kosten stehen bereits im Karten-Header (§6.1) — der Button
  wiederholt sie nicht (S133-D Befund 1: diese Zeile hatte zuvor `Use (N CP)` /
  `↺ Undo (+N CP)` verlangt, ein spec-interner Widerspruch zu den §6.1-Mockups,
  die durchgehend das nackte `[Use]` zeigen — Stakeholder-Entscheid löst ihn
  zugunsten §6.1). „Reset", „Undo deny", „Rückgängig" u. Ä. entfallen zugunsten
  dieser Familie.
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
