# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-18 01:46 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-17 23:54 b982  ████████░░░░ 105k ↓    ██████  96% ↑  ············
07-17 22:16 d275  █████████░░░ 116k ↓    █████░  89% ↑  █···········
07-17 21:32 8096  ███████████░ 143k ↑    █████░  79% ↑  █···········
07-17 19:45 04ab  ███████████░ 140k ↓    ████░░  74% ↑  █···········
07-17 18:44 ffc7  ████████████ 159k ↓    ████░░  67% ↓  ·······▒▒▒▒▒
07-17 15:58 1e74  ████████████ 160k ↓    ████░░  74% ↓  ··········▒▒
```

## Jüngste Session

**2026-07-17 23:54 · b9822b92**

- **Aufgabe:** Freigabe, AUfgaben Parallelisieren.
- **Modelle:** Haupt Fable · Subagent Opus, Sonnet
- **Tokens gesamt:** 103,025,990 (Haupt 4,452,333 · Subagent 98,573,657, Anteil 96 %)
- **Peak-Kontext:** ████████░░░░ 105k / 150k
- **cache_read:** 99,529,806 · **Output:** 330,331

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 105k blieb im 150k-Korridor.
- ✅ 96% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 95,109,074 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: S164 Abschluss: L… ████████░░░░  96k    ✅
2   general-purpose: T2+T3 Vengeance C… ████████████ 308k    ⛔
3   general-purpose: T1 mortal_wounds-… ████████████ 151k    ⛔
4   general-purpose: S164 DoD-Review (… ████████░░░░  95k    ✅
5   general-purpose: Mailbox-Lifecycle… ████░░░░░░░░  47k    ✅
6   general-purpose: T0 Housekeeping B… ██████░░░░░░  71k    ✅
7   general-purpose: S164-Planungsentw… █████████░░░ 113k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  11,593
cache_creation ▕█░░░░░░░░░░░░░░░░░░░░░░░▏    3%  3,154,260
cache_read     ▕████████████████████████▏   97%  99,529,806
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  330,331
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
Warm (System/Memory/History)  ▕████████████████████▏   97%  99,529,806
Neu gecacht (Tool-Ausgaben)   ▕█░░░░░░░░░░░░░░░░░░░▏    3%  3,154,260
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  11,593
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    0%  330,331
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 126 Sessions: 4,059,589,077 Token (46,343 Antworten).

