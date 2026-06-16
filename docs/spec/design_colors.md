# Design-Farbschema — verbindlich (beschlossen + umgesetzt 2026-06-10)

> 6n E2: Bestandsaufnahme + Nutzer-Entscheidungen (Session 39, Review-Runde 2).
> **Regel: Farbentscheidungen trifft der Nutzer.**

## 0. BESCHLOSSEN (2026-06-10) — bei Umsetzung exakte Hex-Werte vorlegen

| Entscheidung | Neu |
|---|---|
| **Buff-Badges** | GRÜN `#4a9a5a` (das bisherige MOVED-Grün) — FESTGELEGT 2026-06-10 |
| **MOVED** | BLAU `#60a5fa` (das bisherige Buff/MWBD-Blau) — FESTGELEGT 2026-06-10 |
| **Cover-Würfel/-Badges (SAVE-Block)** | Cover ist ein Buff → Buff-Grün `#4a9a5a` (vormals blau) |
| **SHOT cyan, CHARGED/FOUGHT violett** | bleiben unverändert (bestätigt) |
| **Army-Ability (WAAAGH!, aktive Command Protocols …)** | = Buff-Grün; Badge in der armyCard; Label aus YAML (E1) |
| **RESERVE** | = HEROIC-INT.-Farbe `#ff9060` (warmes Lachs-Orange) — temporäre Sonderzustände |
| **Relic-Badge** | ENTFÄLLT — nur Effekt-Badges (Buff/Debuff), kein eigener Relic-Stil |
| **Wargear-Keyword-Blau** | ENTFÄLLT analog — Wargear/Weapon-Abilities = Buff/Debuff |
| **Fraktionsfarben (4c)** | NEIN — einheitliches Gold-Theme |
| **Würfel-Sequenz (4b)** | definiert durch D5-Spez + Referenz-Screenshot (ziel6.md §6n Review-Runde 2); Cover-/Buff-Würfel = Buff-Grün |

---

## 1. Basis-Theme (CSS-Variablen in `gameHeader.py` — etabliert ✓)

| Variable | Wert | Verwendung |
|---|---|---|
| `--arb-bg` | `#0f0e0c` | Hintergrund |
| `--arb-surface` | `#1c1a14` | Karten/Flächen |
| `--arb-border` | `#2e2618` | Rahmen, Trennlinien |
| `--arb-accent` | `#d4a017` | Gold-Akzent (Überschriften, Primärbuttons) |
| `--arb-accent-lt` | `#fbbf24` | helles Gold (Zahlen-Highlights: Attacken, Damage) |
| `--arb-muted` | `#6b5f44` | gedämpfter Text, Captions |
| `--arb-text` | `#e7e5e4` | Standardtext |
| `--arb-red` | `#991b1b` | destruktiv/negativ |
| `--arb-green` | `#166534` | Erfolg |
| `--arb-blue` | `#1e3a8a` | Info (Phasen-Regelkasten) |

## 2a. Faktion- & Subfaction-Badges (armyCard) — FESTGELEGT 2026-06-16

Generisch für jede Fraktion. Das Subfaction-Badge wird **immer** gerendert (nie
unsichtbar): gewählter Wert, oder sichtbarer Placeholder/Fehler.

| Badge | Zustand | Farbe (fg) | Beispieltext |
|---|---|---|---|
| Faktion | immer | `#a5b4fc` helles Blau | „Necrons", „Orks" |
| Subfaction | `set` (Wahl getroffen) | `#a5b4fc` helles Blau | „Szarekhan", „Bad Moons" |
| Subfaction | `missing` (Roster korrekt, keine Wahl) | `#9ca3af` gedämpftes Grau | „No Dynasty", „No Clan" |
| Subfaction | `error` (kein subfaction_field in Faktion) | `#ef4444` rot | „No Subfaction" |

Hintergrund/Rahmen: `bg #1a1a2e`, Rahmen = fg. Quelle: `armyCard._keyword_badge`.
Datenbindung: Faktion deklariert `subfaction_field`/`subfaction_label` in
`faction_abilities.yaml`; das Roster setzt das Feld (`dynasty`/`clan`).

## 2. Status-Badges auf unitCards (etabliert ✓ — generisch, jede Einheit)

| Badge | Farbe (fg) | Semantik |
|---|---|---|
| MOVED | `#60a5fa` blau | neutral-positiv bewegt |
| ADVANCED | `#d4a017` gold | eingeschränkt |
| STATIONARY | `#6b5f44` erdgrau | neutral |
| RETREATED / DESTROYED | `#c04040` rot | negativ |
| IN MELEE | `#e07050` orange | gebunden |
| CHARGED / FOUGHT | `#b070d8` / `#c080e8` violett | Nahkampf-Aktivierung |
| SHOT | `#40a0b8` cyan | Fernkampf-Aktivierung |
| RESERVE | `#ff9060` lachs | temporärer Sonderzustand (wie HEROIC INT.) |
| HEROIC INT. | `#ff9060` | Sonderaktion |

## 3. Effekt-Badges (etabliert ✓)

| Kategorie | Farbe | Beispiel |
|---|---|---|
| Buff | `#4a9a5a` grün | MWBD, Cover, Army-Abilities (armyCard) |
| Debuff | `#ef4444` rot | — |
| ~~Relic~~ | entfernt | Relics zeigen nur Effekt-Badges (Buff/Debuff) |
| ~~Wargear-Keyword~~ | entfernt | Wargear-Keywords = normale Chips; Effekte = Buff/Debuff |

## 4. ENTSCHIEDEN (2026-06-10) — Historie der ehemals offenen Slots

**4a Army-Ability = Buff-Grün `#4a9a5a`** — Army-Abilities (WAAAGH!, Command Protocols) GEBEN
Buffs → gleiche Kategorie, konsistent und schlank („damit die Farben nicht ausgehen").
Badge erscheint grün in der armyCard. Das hardcodierte `#b8e040` entfällt (E1).

**4b Würfel-Sequenz** = definiert durch die D5-Spezifikation + Referenz-Screenshot
(ziel6.md §6n Review-Runde 2); Cover-Würfel = Buff-Grün.

**4c Fraktionsfarben: NEIN** — einheitliches Gold-Theme.

---

### 4a. Army-Ability-Badge (6n E1) — ✅ entschieden: Buff-Grün, s. §0/§4

`WAAAGH!` ist aktuell hardcoded `#b8e040` (giftgrün) in `unitCard.py` — verstößt gegen
„Generic src/". Künftig: Label aus Army-Ability-YAML, EINE generische Farbe für alle
Fraktions-Armeefähigkeiten (WAAAGH!, Command Protocols aktiv, Ka'tah-Stance, …).

### 4b. Würfel-Sequenz (6n D5) — ✅ entschieden via D5-Spez, s. §4

Aktuell: Erfolgs-Schwellen farbig je Block (HIT grün `#22c55e`?, WOUND/SAVE orange/amber),
Fehlschläge rot/grau. Festzulegen:

| Slot | Frage | Vorschlag |
|---|---|---|
| Schwellenzahlen (2+, 3+ …) | Helligkeit wie Würfel? | `--arb-text` `#e7e5e4`, Größe = Würfelgröße |
| S-vs-T-Vergleich | Hervorhebung? | beide Werte in `--arb-accent-lt`, Vergleichszeichen groß |
| Blocktrennung | Linienfarbe | `--arb-border` |

### 4c. Fraktionsfarben — ✅ entschieden: NEIN, einheitliches Gold-Theme
