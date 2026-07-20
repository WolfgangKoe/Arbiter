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
> **S169-Nachtrag (Struktur-Umbau, entschieden 2026-07-18):** §7 (S168-Entwurf) vermischte
> generische UI-Bausteine mit dem Explodes-Feature-Ablauf (Schwelle, Radius, Schadenswürfel,
> betroffene Einheiten) — Stakeholder-Befund. Die generischen Bausteine sind jetzt einzeln in
> §1.5–1.9 registriert, §7 beschreibt nur noch die abstrakte Zusammensetzung; der Explodes-
> Ablauf steht in [`processes.md` P-16](processes.md#p-16--explodes--pflicht-trigger-bei-zerstörung).
> Gleiche Trennung angewendet auf §4.4: das generische Wurf-Block-Muster bleibt hier, die
> konkrete Anwendung auf HIT/WOUND/SAVE/DAMAGE (Vereinheitlichungs-Lücken) steht jetzt in
> [`processes.md` P-08](processes.md#p-08--attacksequence--auflösungsreihenfolge-shooting--fight).
> Zusätzlich §3.1 (Wortlaut-Budget) neu — Retro-Maßnahme M2/B-124(a).
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

```
┌──────────────────────────────────────────────┐
│ DAMAGE                                        │
│ Nobz — model_groups: [Boss Nob, Nobz]         │
│ ──────────────────────────────────────────── │
│  A — frei wählbar (kein Modell angeschlagen): │
│   ○ Boss Nob         ○ Nobz     ← EIN Radio   │
│                                                │
│  B — gesperrt (Warnhinweis statt Radio):      │
│   ⚠ ► Angeschlagenes Modell … muss zuerst      │
│       abgehandelt werden.        ← warning    │
│                                                │
│  C — nur eine Gruppe übrig:                   │
│   (Selector entfällt — Schaden trifft die      │
│    verbleibende Gruppe direkt)                │
└──────────────────────────────────────────────┘
```

Genau ein Zustand ist zu jedem Zeitpunkt aktiv (nie Radio + Warnhinweis gleichzeitig,
nie beide Warnhinweis-Zweige zugleich); welcher Zustand aktiv ist, entscheidet
ausschließlich `get_locked_group()` (s. u.), die UI liest nur das Ergebnis.

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

### 1.5 Pflicht-Trigger-Kachel (generische Bauform, S169)

Gleiche Bauform wie die GO-Karte (§6.1: `st.container(border=True)`, Header-Zeile +
Rule-Text-Akkordeon) — aber **ohne** Aktions-Slot: kein `[Use]`, keine CP-Anzeige. Für
Pflicht-Ereignisse, die beim Eintreten eines Spielzustands automatisch fällig werden (kein
Verwenden/Nicht-Verwenden-Entscheid).

```
┌──────────────────────────────────────────────┐
│ [Titel aus YAML]                              │  ← KEIN CP-Suffix, KEIN [Use]
│ [Kontext-/Schwellen-Caption]                  │
│ ──────────────────────────────────────────── │
│  (nachfolgender Baustein, kontextabhängig:    │
│   §1.6 Binär-Wurf / §1.7 Ziel-Auswahl / …)    │
└──────────────────────────────────────────────┘
```

Anker-Regel identisch zu jeder reaktiven GO-Karte (§6.2): inline am Trigger-Ort, NICHT
Vollbreite, NICHT in der zentralen Stratagems-Liste. Konkrete Anwendung: Explodes-Familie,
[`processes.md` P-16](processes.md#p-16--explodes--pflicht-trigger-bei-zerstörung).

**Lebensdauer (S170, Stakeholder-Befund):** Die Kachel-Gruppe (①–④, §7.1) ist an die Phase
gebunden, in der der Pflicht-Trigger ausgelöst wurde — sie verschwindet **vollständig beim
Phasenwechsel** (`gameState.next_phase()`), unabhängig vom Ausgang (Erfolg/Misserfolg/kein
CP-Automatismus genutzt). Kein Dauerzustand über Phasen-/Rundengrenzen hinweg. Danach ist das
Ereignis nur noch im Spiel-Protokoll (`gameProtocoll`/gameLog) nachvollziehbar. Konkrete
Anwendung: `processes.md` P-16.

### 1.6 Binär-Wurf-Baustein — zwei Buttons statt Zahlenfeld (generische Bauform, S169)

Bewusste Alternative zum Tisch-Wurf-Eingabe-Baustein (§6.3, Zahlenfeld): für Tischwürfe, bei
denen für die App nur das Erreichen/Verfehlen einer YAML-Schwelle zählt, nicht der genaue
Würfelwert (anders als z. B. beim Deny-Wurf, dessen Wert weiterverrechnet wird).

```
┌──────────────────────────────────────────────┐
│ [Titel]                                       │  ← KEIN CP-Suffix, KEIN [Use]
│ [Schwellen-Caption, z. B. "… on N+"]          │
│ ──────────────────────────────────────────── │
│  [ Erfolgs-Label ]      [ Fehlschlags-Label ] │
└──────────────────────────────────────────────┘
```

Kein Präzedenzfall für andere Tischwürfe mit echtem Zahlenwert — §6.3 bleibt dort Standard
(S166-Entscheid). Konkreter Wortlaut + Anwendung: `processes.md` P-16.

**Reset-Zustand (S170, Stakeholder-Befund):** Zwei Zustände statt einem — „offen" (beide
Buttons aktiv, noch keine Entscheidung) und „entschieden" (nach Klick auf **eines** der
beiden Labels, Erfolg ODER Fehlschlag gleichermaßen). Im Zustand „entschieden" ersetzt ein
`↺ Reset`-Button (§4.1 `SYM_RESET`) die beiden Erfolgs-/Fehlschlags-Buttons; Klick darauf
kehrt zum Zustand „offen" zurück (Entscheidung verworfen). Gilt identisch für beide Ausgänge
— kein Sonderfall je Richtung. **Präzisierung (S170-Stakeholder-Entscheid, Lesart A):**
VOR „Confirm all" verwirft der Reset auch eine begonnene, unbestätigte Ziel-Auswahl im
Multi-Unit-Panel (④). NACH „Confirm all" führt ein Reset unterhalb des Info-Kastens (③)
zurück ins Multi-Unit-Panel — mit allen bisherigen Zuweisungen sichtbar und nachbearbeitbar
(Teil der Nacharbeit d „Korrektur nach Confirm", §1.7 — Umsetzung Folgesession).

```
┌──────────────────────────────────────────────┐
│ [Titel]                                       │  ← Zustand „offen"
│ [Schwellen-Caption]                           │
│ ──────────────────────────────────────────── │
│  [ Erfolgs-Label ]      [ Fehlschlags-Label ] │
└──────────────────────────────────────────────┘
                    │  Klick auf EINES der beiden Labels
                    ▼
┌──────────────────────────────────────────────┐
│ [Titel]                                       │  ← Zustand „entschieden"
│ [Schwellen-Caption]                           │
│ ──────────────────────────────────────────── │
│                 ↺ Reset                       │
└──────────────────────────────────────────────┘
                    │  Klick auf Reset
                    ▼
              zurück zu Zustand „offen"
```

Konkrete Anwendung inkl. Wechselwirkung mit dem Multi-Unit-Panel (§1.7, falls bereits aktiv):
`processes.md` P-16.

### 1.7 Multi-Unit-Ziel-Auswahl-Panel — beide Armeen (generische Bauform, S169)

Reiner Toggle-Zeilen-Stil wie die bestehende Heroic-Intervention-Auswahl
(`chargePhase.py:_render_heroic_intervention`) — **keine Card-Ansicht**. Zeigt Einheiten
beider Armeen gruppiert nebeneinander, mit festem Zwei-Spalten-Layout je Gruppe (Label-Spalte
+ fest breite Zahlenfeld-Spalte), damit ein Spaltenkopf zuverlässig über der Zahlenfeld-
Spalte steht, auch wenn nur einzelne Zeilen ein Feld zeigen (Zahlenfeld erscheint nur bei
ausgewählten Einheiten, `✓`-Präfix §6.4-Wortlaut).

```
┌────────────────────────────────────────────────────────────────────────────┐
│ [Titel] ℹ [Kontext-Hinweis]                                                 │
├────────────────────────┬──────────────────────┬────────────────────┬──────┤
│ Gruppe A (var. Breite) │ [Feld-Spaltenkopf]   │ Gruppe B (var.)     │[Kopf]│
├────────────────────────┼──────────────────────┼────────────────────┼──────┤
│  [✓ Einheit 1]         │ [ n ] [−] [+]        │  [  Einheit 3]      │      │
│  [  Einheit 2]         │                      │  [✓ Einheit 4]      │[n][−][+]│
├────────────────────────┴──────────────────────┴────────────────────┴──────┤
│  [Confirm all]     [Reset]                                                 │
└────────────────────────────────────────────────────────────────────────────┘
```

Die **zuletzt bearbeitete** Einheit (zuletzt angehakt ODER zuletzt geänderter Mortal-Wounds-Wert)
springt in ihrer armyList-Sidebar (§1.9) an die erste Position. Eine zuvor bearbeitete Einheit
kehrt an ihre Standardposition zurück, sobald eine andere Einheit bearbeitet wird — auch wenn
sie weiterhin angehakt bleibt. Bei mehreren gleichzeitig offenen Explodes-Kacheln gilt das pro
Kachel unabhängig (je Kachel eine gepinnte Einheit möglich). Der sinkende LP-Balken zeigt direkt
in der unitCard (Bestandskomponente) — keine zusätzliche Vorschau-/Mini-Karte im Panel. Footer:
„Confirm all" / „Reset" (§6.4-Wortlaut-Familie, analog Abschluss der Attackensequenz). Konkrete
Anwendung: `processes.md` P-16.

**Direkt-Apply statt Sammel-Buchung (S170-Präzisierung, Umsetzung Folgesession — S169-Befund:
Schaden wurde bisher gesammelt und erst bei „Confirm all" für alle Einheiten gleichzeitig
gebucht, spec-widrig):** Der Schaden wird **je Einheit sofort bei Werteingabe** angewendet
(`apply_damage`, mortal) — nicht gesammelt und erst am Ende gebucht. Der LP-Balken sinkt live,
auch bis zur Zerstörung der Einheit (`unit_state.destroyed` greift wie bei jeder anderen
Schadensquelle); der Sidebar-Sprung an die erste Position (s. o.) passiert im selben Moment.
„Confirm all" bucht dadurch **nichts mehr selbst** — es schließt das Panel ab (Panel
verschwindet, Info-Kasten §1.8 bleibt stehen). „Reset" macht alle bereits direkt angewendeten
Zuweisungen der aktuellen Auswahl-Runde rückgängig (LP zurück auf den Stand vor dem Panel) und
hält das Panel für eine neue Auswahl offen.

```
Zuweisung je Einheit (SOFORT, nicht erst bei Confirm all):
  [✓ Einheit X]   [ n ]  ──►  apply_damage(X, n) sofort
                               LP-Balken live + Sidebar-Sprung an Position 1

Footer:
  [Confirm all]  ──►  schließt Panel ab (keine erneute Schadensbuchung —
                       die Zuweisungen sind bereits angewendet)
  [Reset]        ──►  macht ALLE bisherigen Zuweisungen der Runde rückgängig,
                       Panel bleibt offen für neue Auswahl
```

**Korrektur nach Confirm (Umsetzung Folgesession, hier nur Zielverhalten spezifiziert):** nach
„Confirm all" kann der Spieler in denselben Panel-Zustand direkt VOR der Bestätigung
zurückkehren, um Fehlzuweisungen zu korrigieren (z. B. falscher Würfelwert eingetragen) — ohne
das gesamte Explodes-Ereignis neu durchlaufen zu müssen. Der konkrete Anker/Button dafür wird
in der Folgesession festgelegt; diese Spec bindet nur das Verhalten: gleicher Panel-Zustand,
gleiche Auswahl, wie unmittelbar vor „Confirm all".

### 1.8 Info-Hinweiskasten — Wiederverwendung für Ergebnis-Ausgänge (generische Bauform, S169)

Kein neuer Zustand neben `info`/`warning`/`success`/`error` (§3): ein Ergebnis-Hinweis
(„X trifft ein" / „X tritt nicht ein") ist semantisch weiterhin ein neutraler Hinweis-/
Regel-Text → Typ `info`, derselbe `--arb-blue`-Token wie der bestehende Phasen-Regelkasten
(`design_colors.md` Zeile 40) — kein neues Token. Genau **ein** Kasten deckt beide möglichen
Ausgänge ab (nie beide gleichzeitig sichtbar); Wortlaut-Budget gilt (§3.1).

```
┌──────────────────────────────────────────────┐
│ ℹ info                                        │
│ [Ein-Satz-Ergebnistext, austauschbar je       │
│  Ausgang — Wortlaut-Budget §3.1]              │
└──────────────────────────────────────────────┘
```

**Lebensdauer (S170):** identisch zur Kachel-Gruppe, an die dieser Kasten gehört (§1.5) —
verschwindet beim Phasenwechsel zusammen mit der Kachel, kein Dauerzustand über die Runde
hinaus. Kein stilles Verschwinden VOR dem Phasenwechsel (§1.5 bleibt maßgeblich: „does not
explode" ist ein expliziter, sichtbar markierter Endzustand, keine kommentarlose Löschung).

### 1.9 Layout-Invariante — Effekt-Ausführung in `center`, Sidebars unveränderlich (S169)

`src/app.py` teilt die Ansicht in drei Spalten: `left` = `render_army_list(first_player)`,
`center` = `render_game_actions_area()` (+ `render_game_protocoll()`), `right` =
`render_army_list(second_player)`. Jede Pflicht-Trigger-/Effekt-Ausführungs-Bauform
(§1.5–1.8) rendert **ausschließlich in der `center`-Spalte**, nie innerhalb einer der beiden
armyList-Sidebars — die Sidebars sind fest an `first_player`/`second_player` gebunden, nie an
`active` (Domänen-Constraint, `CLAUDE.md`), und bleiben unangetastet: sie reagieren nur
reaktiv auf Auswahl/Schaden (LP-Balken, Sortierung an die Spitze, §1.7).

```
┌───────────────────────────────────────────────────────────────────────────┐
│                              gameHeader                                   │
├───────────────────────┬───────────────────────────────────┬───────────────┤
│  left                 │  center                           │  right        │
│  armyList             │  gameActionsArea                  │  armyList     │
│  (first_player)       │  (Effekt-Ausführung rendert HIER) │ (second_player)│
│  unangetastet         │                                   │  unangetastet │
└───────────────────────┴───────────────────────────────────┴───────────────┘
```

Mehrere Gruppen (z. B. beide Fraktionen im Multi-Unit-Panel, §1.7) erscheinen nebeneinander
**innerhalb derselben `center`-Kachel**, nie in eigenen Seiten-Spalten — es gibt keine
armee-eigene Spalte auf App-Ebene (Mockup-V3-Fehler, korrigiert S168/S169).

#### 1.9.1 playerArea-Beschränkung für Bausteine ①③ (S170, Stakeholder-Befund S169)

`gameActionsArea` (die `center`-Spalte) gliedert sich intern kanonisch weiter in
`gameActionDisplayArea` (oben, volle `center`-Breite) und darunter `firstPlayerArea` /
`secondPlayerArea` (50/50-Split, [`ui_layout.md` §7](ui_layout.md#7-gameactionsarea) —
hier nicht dupliziert, nur referenziert). Binär-Wurf-Baustein (§1.6) und Info-Hinweiskasten
(§1.8) einer Pflicht-Trigger-Kachel-Gruppe (Baustein ① und ③, §7.1) rendern **ausschließlich
in der `playerArea` des Spielers, dessen Einheit den Pflicht-Trigger auslöst** (`first_player`
oder `second_player`, nie an `active` gebunden — Domänen-Constraint `CLAUDE.md`) — **nicht**
über die volle `gameActionsArea`-Breite (S169-Ist-Befund: Kachel + Info-Kasten erstreckten
sich über die gesamte `gameActionsArea`, war als Regression gemeldet).

Ausnahme, unverändert: das Multi-Unit-Ziel-Auswahl-Panel (§1.7, Baustein ④) zeigt bewusst
beide Armeen nebeneinander und spannt deshalb weiterhin die volle `gameActionsArea`-Breite
(vom Stakeholder als korrekt abgenommen, S169).

```
┌───────────────────────────────────────────────────────────────────────────┐
│                gameActionDisplayArea (volle center-Breite)                │
├──────────────────────────────────┬──────────────────────────────────────┤
│  firstPlayerArea                  │  secondPlayerArea                     │
│  ┌──────────────────────────────┐ │                                      │
│  │ ① Binär-Wurf-Baustein (§1.6) │ │  ← nur hier, wenn first_player die   │
│  │ ③ Info-Hinweiskasten (§1.8)  │ │    explodierende Einheit kontrolliert│
│  └──────────────────────────────┘ │                                      │
├──────────────────────────────────┴──────────────────────────────────────┤
│  ④ Multi-Unit-Ziel-Auswahl-Panel — volle Breite, beide Armeen (Ausnahme, │
│    unverändert — s. o.)                                                   │
└───────────────────────────────────────────────────────────────────────────┘
```

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

### 3.1 Wortlaut-Budget (Ratchet, S169 — Retro-Maßnahme M2, erledigt zugleich B-124(a))

Hinweis-/Warntexte im UI: **maximal ein kurzer Imperativ- oder Aussagesatz.** Keine
Regel-Paraphrase im UI — die Regelbegründung („warum gilt das") gehört in die zuständige
Spec (`docs/spec/rules_insights.md` für Implementierungs-Gotchas, `docs/spec/acceptance/rules.md`
für den Akzeptanz-Katalog), nicht in den Hinweis-/Warntext selbst. Der UI-Text sagt nur, WAS
der Spieler jetzt tun muss oder was gerade gilt — nicht WARUM. Gilt für alle vier Typen aus
der Tabelle oben, nicht nur `warning`.

Bestehende Texte, die das Budget überschreiten, werden **nicht** in einem Big-Bang-Durchgang
gekürzt, sondern als Ratchet bei der nächsten Modul-Berührung (analog §1.1/§4.3-Ratchet-
Prinzip). Bekannter Kandidat: der Sperr-Warnhinweis im Subgruppen-Selektor (§1.4 Zustand B,
`_common.py`) — zwei mehrsatzige Zweige mit eingebauter Regelbegründung; Kürzung bei
nächster Berührung des Bausteins (B-124(a), Code-Kürzung selbst ist ein separater Auftrag).

## 4. Symbol- & Würfel-Design-System (§4.1 S115, §4.2/§4.3 neu S159/B-104)

Ein kanonischer Ort je Glyph/Würfelfläche — projektweit konsistent tauschbar, keine
Fraktionslogik. Vier Unterabschnitte, auf Augenhöhe mit §6 (Gefechtsoptionen-UI):
§4.1 Glyph-Konstanten (Einzelzeichen, kein Würfel-Slot-Kontext), §4.2 Würfelflächen-
Katalog (echte Würfel-SVGs), §4.3 Effekt-Symbol-Katalog (Symbole, die in einem
Würfel-Slot erscheinen — teils SVG-Würfel, teils bewusst Text-Chip), §4.4 Wurf-Block-
Pattern (kanonischer Aufbau eines ganzen Wurf-Blocks, generisch — die konkrete
Anwendung auf HIT/WOUND/SAVE/DAMAGE steht seit S169 in `processes.md` P-08).

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

### 4.4 Wurf-Block-Pattern — kanonischer Aufbau (S159 Fassung 2, Split S169)

Nicht nur die Symbole *in* einem Würfel-Slot sind katalogisiert (§4.2/§4.3) — auch der
Aufbau eines Wurf-Blocks selbst folgt einem kanonischen Muster, damit ein Spieler jeden
Block gleich liest, unabhängig davon, wofür gewürfelt wird. Das Muster selbst ist
generisch (jeder künftige Wurf-Block-Konsument richtet sich danach, nicht nur die
Attackenabfolge):

```
├─ Titel + Vergleichswert (WS/BS N+, S vs T, Sv N+, …)
├─ Threshold-Header + Dice-Row (Basis-Schwelle)
├─ Marker-Zeilen (optional): Auto-fail (✕) / Reroll (↺) / Value-Trigger (+N) — alle
│  über denselben Slot-Mechanismus wie §4.3
├─ Modifier-Zeilen (je Modifier: Vergleichs-Würfelpaar + eigene Eff.-Zeile, verschachtelt)
├─ Eff.-Zeile (finale Schwelle nach allen Modifiers)
└─ Quellen-Chips (optional): GO-/Ability-Herkunft eines Buffs/Debuffs (Text-Chip-Familie)
```

**S169-Struktur-Umbau:** die konkrete Anwendung dieses Musters auf HIT/WOUND/SAVE/DAMAGE
(Ist-Zustand, Vereinheitlichungs-Lücken-Tabelle mit Code-Zeilen) ist Feature-/Prozess-
spezifisch für die Attackenabfolge und steht jetzt in
[`processes.md` P-08, Abschnitt „Wurf-Block-Rendering"](processes.md#p-08--attacksequence--auflösungsreihenfolge-shooting--fight)
— hier verblieb nur das abstrakte Muster.

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

## 7. Pflicht-Trigger-Kachel-Familie — generische Bauform (S169, ersetzt Explodes-Entwurf S168)

> **Struktur-Korrektur S169 (Stakeholder-Befund):** der S168-Entwurf dieses Abschnitts
> vermischte generische UI-Bausteine mit dem Explodes-Feature-Ablauf (Schwelle, Radius,
> Schadenswürfel, betroffene Einheiten, konkreter Wortlaut). Das widerspricht der
> Artefakt-Landkarte: „UI-Design-System" definiert *welche Kachel, welcher Button in
> welcher Farbe* — generisch; Feature-/Prozess-Spezifisches gehört in die Prozess-Spec.
> Die generischen Bausteine sind jetzt einzeln in §1.5–1.9 registriert (mit ASCII-Schema,
> M1-Pflicht); dieser Abschnitt beschreibt nur noch, wie sie sich zu **einer**
> Kachel-Gruppe zusammensetzen — abstrakt, ohne einen einzigen Explodes-Zahlenwert. Der
> konkrete Feature-Ablauf (Explodes: Schwelle, Radius, Mortal-Wounds-Würfel, betroffene
> Einheiten, Screenshot-Referenzen, Wortlaut) steht in
> [`processes.md` P-16](processes.md#p-16--explodes--pflicht-trigger-bei-zerstörung).
> Inhaltlich **nichts verworfen** — nur verschoben/generalisiert (S168-Fassung war bereits
> vom Stakeholder korrigiert und damit maßgeblich für beide Zielorte).

Fachliche Einordnung (abstrakt): ein Pflicht-Trigger ist ein **Pflicht-Ereignis** bei
einem Spielzustands-Wechsel (z. B. Modell-Tod) — kein Verwenden/Nicht-Verwenden-Entscheid,
kein `[Use]`, keine CP. Die GO-Karte (§6.1) ist deshalb die falsche Komponente für den
Trigger selbst — diese Familie baut **ausschließlich aus Bestandskomponenten**: keine neue
Bauform, kein neues Farb-Token.

### 7.1 Aufbau der Kachel-Gruppe (abstrakt)

Am Eintrag der betroffenen Einheit erscheint eine Folge von Bausteinen (kein neuer
Container-Typ, jeder Baustein für sich bereits Bestand):

```
┌──────────────────────────────────────────────┐
│ ① Binär-Wurf-Baustein (§1.6)                  │
├──────────────────────────────────────────────┤
│ ② optionale GO-Karte(n) (§6.1, falls die Regel│
│    einen CP-Automatismus ODER ein "vor-Wurf-  │
│    GO" anbietet)                              │
├──────────────────────────────────────────────┤
│ ③ EIN Info-Hinweiskasten (§1.8)               │
├──────────────────────────────────────────────┤
│ ④ Multi-Unit-Ziel-Auswahl-Panel (§1.7, nur    │
│    bei Erfolg)                                │
└──────────────────────────────────────────────┘
     ↑ Anker: INLINE am Trigger-Ort (center-Spalte, §1.9)
```

**Anker-Regel:** genauso wie jede reaktive GO-Karte (§6.2) — inline am Trigger-Ort, NICHT
Vollbreite, NICHT in der zentralen Stratagems-Liste. Bausteine ①–④ sind alle Bestand
(§1.5–1.8 + §6.1) — kein neuer Container-Typ, ③ entfällt bei Fehlschlag (dann folgt ④
direkt auf ① oder ②). Reihenfolge und konkrete Belegung (welcher Baustein bei welchem
Ereignis, welche Zahlenwerte) bestimmt die jeweilige Prozess-Spec — für Explodes:
`processes.md` P-16.

**Breiten-Regel (S170, §1.9.1):** Bausteine ①③ (Binär-Wurf + Info-Hinweiskasten) rendern nur
innerhalb der `playerArea` des kontrollierenden Spielers, nicht über die volle
`gameActionsArea`-Breite; Baustein ④ (Multi-Unit-Panel) ist die einzige Ausnahme und spannt
bewusst die volle Breite (beide Armeen nebeneinander). Details + ASCII-Schema: §1.9.1.

**Lebensdauer (S170, §1.5/§1.8):** die gesamte Kachel-Gruppe verschwindet beim
Phasenwechsel, unabhängig vom Ausgang — kein Dauerzustand über die Runde hinaus, Ereignis
danach nur noch im gameLog.

**Baustein ② — zwei Spielarten (S173, B-122):** Baustein ② deckt zwei fachlich
unterschiedliche GO-Karten ab, beide über CP-Automatismen der jeweiligen Fraktion
angeboten, keine neue Bauform:
- **CP-Automatismus** ersetzt den Wurf selbst (z. B. „Curse of the Phaeron": „Do not roll
  … it does so automatically" → Baustein ① wird übersprungen, `exploded` wird direkt
  gesetzt).
- **„Vor-Wurf-GO"** spendet CP + loggt, bevor der Wurf stattfindet, lässt Baustein ① aber
  unangetastet und weiterhin manuell bedienbar (z. B. „Careen!": „…before rolling to see
  if it explodes" — Orks-Regelwortlaut). Beide Spielarten teilen sich denselben Anker
  (inline neben Baustein ①) und dieselbe Use/Undo-Wortlautfamilie (§6.4); der Unterschied
  liegt allein darin, ob der Effekt den Wurf ersetzt oder ihm nur vorausgeht.

### 7.2 Wortlaut & Farbe (abstrakt)

Keine neuen Farb-Token für diese Familie — Zuordnung innerhalb des bestehenden Schemas
(`design_colors.md`), identisch zur GO-Karte (§6.5): Gold-Primary für aktiv bedienbare
Bausteine, `--arb-blue` für den Info-Hinweiskasten (§1.8, Hinweis-Konvention §3),
Standard-Wortlaut-Familie (§6.4: `Use`/`↺ Undo`/`Used`, `Confirm ⟨Aktion⟩`/`Cancel`,
`✓`-Präfix-Toggle). Wortlaut-Budget gilt (§3.1: maximal ein kurzer Satz je Hinweis, keine
Regel-Paraphrase im UI). Feature-spezifische Button-Beschriftungen (z. B. „Explodes!"/
„Does not explode") stehen in der jeweiligen Prozess-Spec, nicht hier.
