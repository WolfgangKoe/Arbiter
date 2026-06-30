# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-06-30 22:00 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
06-30 20:54 ac89  ████████░░░░ 104k ↓    ████░░  64% ↓  ██····▒▒▒▒▒▒
06-30 18:46 fce6  ███████████░ 133k ↓    ████░░  75% ↑  ███········▒
06-29 20:55 c673  ████████████ 162k ↑    ████░░  74% ↑  █··········▒
06-28 20:02 1b3d  ███████████░ 135k ↓    ████░░  73% ↑  ···········▒
06-28 18:27 5ed6  ████████████ 153k ↑    ████░░  64% ↓  █···········
06-27 14:42 5af7  ██████░░░░░░  80k ↓    █████░  78% ↑  ███·········
```

## Jüngste Session

**2026-06-30 20:54 · ac896ba0**

- **Aufgabe:** start Session mit dem Planner Subagenten
- **Modelle:** Haupt Opus · Subagent Haiku, Opus, Sonnet
- **Tokens gesamt:** 16,509,989 (Haupt 5,989,387 · Subagent 10,520,602, Anteil 64 %)
- **Peak-Kontext:** ████████░░░░ 104k / 150k
- **cache_read:** 15,011,603 · **Output:** 158,817

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 104k blieb im 150k-Korridor.
- ✅ 64% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 8,434,224 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   claude: Abschluss-Review S113 (DoD) █████░░░░░░░  59k    ✅
2   claude: Abschluss-Artefakte S113 s… ██████░░░░░░  74k    ✅
3   Explore: T2a: WAAAGH-Drift read-on… ███░░░░░░░░░  32k    ✅
4   claude: T1: S112-Befund schließen   ██░░░░░░░░░░  29k    ✅
5   claude: T1: S112-Befund schließen   ██░░░░░░░░░░  30k    ✅
6   claude: B1/B2 Fix Undo+Label battl… ███░░░░░░░░░  32k    ✅
7   claude: active_text Inhaltstest WA… ███░░░░░░░░░  42k    ✅
8   claude: T2b: once_per_battle battl… █████░░░░░░░  68k    ✅
9   Plan: Planning-Entwurf nächste Ses… █████░░░░░░░  66k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  35,507
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    8%  1,304,062
cache_read     ▕████████████████████████▏   91%  15,011,603
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  158,817
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
Warm (System/Memory/History)  ▕████████████████████▏   91%  15,011,603
Neu gecacht (Tool-Ausgaben)   ▕██░░░░░░░░░░░░░░░░░░▏    8%  1,304,062
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  35,507
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  158,817
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 151 Sessions: 2,960,647,861 Token (29,786 Antworten).

