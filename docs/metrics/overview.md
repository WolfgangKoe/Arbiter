# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-17 13:24 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-17 10:38 6342  ████████████ 156k ↑    █████░  87% ↓  ···········▒
07-17 08:26 0dfe  ████████████ 155k ↑    █████░  89% ↑  ············
07-17 07:51 d5f8  ██████████░░ 128k ↑    █████░  76% ↑  ·········▒▒▒
07-16 21:15 ae52  ██████░░░░░░  77k ↓    ░░░░░░   0% ↓  ▓▓▓▓▓▓▓▓▓▓▓▓
07-16 20:22 a6af  ████████████ 173k ↑    ████░░  61% ↑  █·········▒▒
07-16 19:40 decf  ██████████░░ 129k ↓    ░░░░░░   6% ↓  ············
```

## Jüngste Session

**2026-07-17 10:38 · 63426237**

- **Aufgabe:** Plan ist kommentiert und freigegeben.
- **Modelle:** Haupt Fable · Subagent Haiku, Opus, Sonnet
- **Tokens gesamt:** 70,906,509 (Haupt 9,417,051 · Subagent 61,489,458, Anteil 87 %)
- **Peak-Kontext:** ████████████ 156k / 150k
- **cache_read:** 66,238,279 · **Output:** 389,830

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ⚠️ 4 von 91 Antworten lagen über dem 150k-Korridor — Session früher schneiden.
- ✅ 87% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 60,240,154 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: B-028-Entscheid v… ████░░░░░░░░  53k    ✅
2   general-purpose: Executor 0a: Proz… █████░░░░░░░  65k    ✅
3   general-purpose: S157-Abschluss-Ar… ████████████ 169k    ⛔
4   general-purpose: S157-Planning-Ent… ████████████ 147k    ⚠️
5   general-purpose: Executor B-098-Re… ████████████ 175k    ⛔
6   general-purpose: Executor B-028 Sc… █████████░░░ 115k    ✅
7   general-purpose: Marker-Fix NEEDS-… ██░░░░░░░░░░  29k    ✅
8   general-purpose: Executor 0b: Back… ████████████ 163k    ⛔
9   general-purpose: Executor B-103 La… ████████░░░░ 100k    ✅
10  general-purpose: Backlog-Items B-1… ██████░░░░░░  81k    ✅
11  general-purpose: S157-Abschluss-Re… ██████░░░░░░  69k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  16,427
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    6%  4,261,973
cache_read     ▕████████████████████████▏   93%  66,238,279
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  389,830
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
Warm (System/Memory/History)  ▕████████████████████▏   93%  66,238,279
Neu gecacht (Tool-Ausgaben)   ▕█░░░░░░░░░░░░░░░░░░░▏    6%  4,261,973
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  16,427
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  389,830
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 119 Sessions: 3,661,308,602 Token (42,290 Antworten).

