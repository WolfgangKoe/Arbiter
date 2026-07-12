# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-12 17:45 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-12 11:18 dedb  ████████████ 151k ↑    █████░  80% ↑  ▚▚▚▚········
07-12 02:03 76ce  █████████░░░ 119k ↓    ████░░  72% ↓  ▚▚▚█········
07-11 15:28 a4be  ████████████ 150k ↑    █████░  82% ↓  ███·········
07-11 12:58 3d6e  ███████████░ 143k ↓    █████░  89% ↑  ▚▚▚█········
07-11 10:04 8553  ████████████ 178k ↑    ████░░  65% ↓  ▚▚▚▚▚▚▚▚····
07-10 21:31 e914  ███████████░ 134k ↓    █████░  89% ↑  ▚▚▚·········
```

## Jüngste Session

**2026-07-12 11:18 · dedbab76**

- **Aufgabe:** start session
- **Modelle:** Haupt Fable, Opus · Subagent Fable, Haiku, Opus, Sonnet
- **Tokens gesamt:** 74,408,205 (Haupt 14,778,491 · Subagent 59,629,714, Anteil 80 %)
- **Peak-Kontext:** ████████████ 151k / 150k
- **cache_read:** 68,368,154 · **Output:** 451,451

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ⚠️ 5 von 152 Antworten lagen über dem 150k-Korridor — Session früher schneiden.
- ✅ 80% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 41,621,586 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: Investigator 1: G… ██████████░░ 131k    ⚠️
2   Explore: Locate stratagem helper s… ███░░░░░░░░░  32k    ✅
3   general-purpose: Executor 3: B12b-… ███████████░ 133k    ⚠️
4   general-purpose: Investigator 2: E… ████████░░░░  96k    ✅
5   general-purpose: Planner: Session-… ████████░░░░ 104k    ✅
6   general-purpose: Executor 2a: mypy… ████████░░░░  96k    ✅
7   general-purpose: Fix B: Movement-T… █████░░░░░░░  67k    ✅
8   general-purpose: Executor 1: Ork-R… ██████░░░░░░  79k    ✅
9   general-purpose: Executor 2b: mypy… ███████████░ 138k    ⚠️
10  general-purpose: Executor: Artefak… █████████░░░ 108k    ✅
11  Explore: Check helper function sig… █░░░░░░░░░░░  11k    ✅
12  general-purpose: Fix A: Emergency-… ██████░░░░░░  75k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  5,107
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    8%  5,583,493
cache_read     ▕████████████████████████▏   92%  68,368,154
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  451,451
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
Warm (System/Memory/History)  ▕████████████████████▏   92%  68,368,154
Neu gecacht (Tool-Ausgaben)   ▕██░░░░░░░░░░░░░░░░░░▏    8%  5,583,493
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  5,107
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  451,451
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 110 Sessions: 3,367,908,523 Token (35,898 Antworten).

