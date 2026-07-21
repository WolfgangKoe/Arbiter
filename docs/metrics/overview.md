# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-21 19:09 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-21 17:57 4c40  ████████████ 150k ↑    ███░░░  56% ↓  █···········
07-20 21:40 813e  ███████████░ 137k ↓    █████░  83% ↑  ██··········
07-20 20:48 f518  ████████████ 174k ↑    ██░░░░  40% ↓  ███·········
07-20 19:44 bc42  ████████████ 155k ↑    ████░░  67% ↓  ███·········
07-19 21:36 e1cb  ██████████░░ 129k ↑    █████░  90% ↑  ··········▒▒
07-19 16:41 4f3a  ██████████░░ 122k ↓    █████░  84% ↑  █··········▒
```

## Jüngste Session

**2026-07-21 17:57 · 4c4003c9**

- **Aufgabe:** start session
- **Modelle:** Haupt Opus · Subagent Opus, Sonnet
- **Tokens gesamt:** 20,254,534 (Haupt 8,922,482 · Subagent 11,332,052, Anteil 56 %)
- **Peak-Kontext:** ████████████ 150k / 150k
- **cache_read:** 18,099,851 · **Output:** 261,571

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ⚠️ 2 von 90 Antworten lagen über dem 150k-Korridor — Session früher schneiden.
- ✅ 56% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 10,640,300 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   Plan: S176 Planning-Entwurf erstel… ███████████░ 132k    ⚠️
2   Explore: B-113 Scope-Discovery Rec… █████░░░░░░░  58k    ✅
3   claude: Executor B-127 RP-Hinweis … █████░░░░░░░  67k    ✅
4   claude: Review S176 B-127 gegen DoD ████░░░░░░░░  47k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  5,940
cache_creation ▕███░░░░░░░░░░░░░░░░░░░░░▏    9%  1,887,172
cache_read     ▕████████████████████████▏   89%  18,099,851
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  261,571
```

**Legende & Zielwerte:**

- **input** — neue, ungecachte Tokens → niedrig halten.
- **cache_creation** — erstmals gecacht (einmalig teurer) → moderat, unvermeidbar bei neuem Kontext.
- **cache_read** — aus warmem Cache gelesen (günstig) → **hoher Anteil = gut** (Kontext bleibt warm, Cache-TTL ~5 Min).
- **output** — generierte Tokens; **kein Selbstzweck — Qualität vor Menge.** Ein höherer Output-Anteil *relativ zu* cache_read kann Ziele schneller erreichen, *sofern das Ergebnis trägt*; viel cache_read bei wenig substanziellem Output = Reibung, "Mist"-Output ist schädlich, nicht gut.

**Zielbild:** hoher cache_read-Anteil + niedriger input-Anteil = effizientes Arbeiten; Output bewusst gegen Qualität gewichtet (nicht maximieren). Viele Cache-Misses (hoher input nach Pausen > 5 Min) sind ein Warnsignal.

## Kontext-Zusammensetzung (nach Quelle, approximiert)

_Approximation: exakte Per-Quelle-Aufschlüsselung ist im Transcript nicht verfügbar. Orientiert an Wegner 2026 / context-engineering-slides.md._

```text
Warm (System/Memory/History)  ▕████████████████████▏   89%  18,099,851
Neu gecacht (Tool-Ausgaben)   ▕██░░░░░░░░░░░░░░░░░░▏    9%  1,887,172
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  5,940
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  261,571
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 106 Sessions: 4,191,265,904 Token (46,570 Antworten).

