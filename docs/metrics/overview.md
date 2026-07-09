# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-10 01:43 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-09 20:34 5769  ████████░░░░ 103k ↓    █████░  81% ↑  ▚··········▒
07-09 20:34 19cb  ████████████ 162k ↓    ██░░░░  25% ↓  ·······▒▒▒▒▒
07-09 17:14 bd4b  ████████████ 173k ↑    ████░░  62% ↓  ▚···········
07-08 16:31 b31b  ████████████ 167k ↑    ██████  93% ↑  ············
07-08 16:31 cf5b  ████░░░░░░░░  48k ↓    █████░  79% ↓  ············
07-07 18:58 ab9b  ███████████░ 138k ↓    █████░  79% ↓  ▚▚▚······▒▒▒
```

## Jüngste Session

**2026-07-09 20:34 · 576987de**

- **Aufgabe:** start session
- **Modelle:** Haupt Fable · Subagent Fable, Haiku, Sonnet
- **Tokens gesamt:** 32,308,639 (Haupt 6,043,610 · Subagent 26,265,029, Anteil 81 %)
- **Peak-Kontext:** ████████░░░░ 103k / 150k
- **cache_read:** 29,705,599 · **Output:** 229,561

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 103k blieb im 150k-Korridor.
- ✅ 81% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 23,061,117 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: Executor 1a: GO-K… ███████████░ 131k    ⚠️
2   general-purpose: S132 Planning-Ent… ██████████░░ 127k    ⚠️
3   general-purpose: Executor 4: Doku-… █████░░░░░░░  59k    ✅
4   general-purpose: Executor 3: Start… ███░░░░░░░░░  41k    ✅
5   general-purpose: Executor 1b: Stra… █████████░░░ 115k    ✅
6   general-purpose: Executor 2: Re-Ro… █████░░░░░░░  65k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  64,592
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    7%  2,308,887
cache_read     ▕████████████████████████▏   92%  29,705,599
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  229,561
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
Warm (System/Memory/History)  ▕████████████████████▏   92%  29,705,599
Neu gecacht (Tool-Ausgaben)   ▕██░░░░░░░░░░░░░░░░░░▏    7%  2,308,887
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  64,592
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  229,561
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 111 Sessions: 3,029,766,803 Token (30,751 Antworten).

