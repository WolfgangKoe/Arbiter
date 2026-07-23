# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-23 22:29 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-23 21:51 6eae  ██████████░░ 124k ↓    █████░  80% ↑  ██··········
07-23 17:56 33e4  ████████████ 153k ↑    ████░░  65% ↓  ██········▒▒
07-23 17:16 fe07  ████████░░░░ 100k ↓    █████░  79% ↑  █·····▒▒▒▒▒▒
07-23 16:34 695b  ██████████░░ 128k ↓    ████░░  63% ↑  ███▒▒▒▒▒▒▒▒▒
07-22 20:41 2123  ████████████ 224k ↑    ███░░░  56% ↓  ············
07-22 19:15 dbc6  ████████████ 166k ↑    ████░░  73% ↓  █···········
```

## Jüngste Session

**2026-07-23 21:51 · 6eae1d4b**

- **Aufgabe:** Start Session
- **Modelle:** Haupt Opus · Subagent Opus, Sonnet
- **Tokens gesamt:** 17,914,651 (Haupt 3,498,926 · Subagent 14,415,725, Anteil 80 %)
- **Peak-Kontext:** ██████████░░ 124k / 150k
- **cache_read:** 16,025,209 · **Output:** 144,416

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 124k blieb im 150k-Korridor.
- ✅ 80% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 12,041,236 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   Plan: Session-Plan B-128 erstellen  █████░░░░░░░  62k    ✅
2   general-purpose: T2+T3 Verif-Hando… ███████████░ 134k    ⚠️
3   general-purpose: T1 B-128(b) DAMAG… ███████░░░░░  93k    ✅
4   general-purpose: Review S182 B-128… █████░░░░░░░  58k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  483
cache_creation ▕███░░░░░░░░░░░░░░░░░░░░░▏   10%  1,744,543
cache_read     ▕████████████████████████▏   89%  16,025,209
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  144,416
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
Warm (System/Memory/History)  ▕████████████████████▏   89%  16,025,209
Neu gecacht (Tool-Ausgaben)   ▕██░░░░░░░░░░░░░░░░░░▏   10%  1,744,543
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  483
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  144,416
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 105 Sessions: 4,265,706,965 Token (47,555 Antworten).

