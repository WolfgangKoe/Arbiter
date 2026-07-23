# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-23 21:45 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-23 17:56 33e4  ████████████ 149k ↑    ████░░  68% ↓  ██········▒▒
07-23 17:16 fe07  ████████░░░░ 100k ↓    █████░  79% ↑  █·····▒▒▒▒▒▒
07-23 16:34 695b  ██████████░░ 128k ↓    ████░░  63% ↑  ███▒▒▒▒▒▒▒▒▒
07-22 20:41 2123  ████████████ 224k ↑    ███░░░  56% ↓  ············
07-22 19:15 dbc6  ████████████ 166k ↑    ████░░  73% ↓  █···········
07-21 19:23 1c15  ████████████ 152k ↓    █████░  80% ↑  ██··········
```

## Jüngste Session

**2026-07-23 17:56 · 33e40467**

- **Aufgabe:** start next session
- **Modelle:** Haupt Fable, Opus · Subagent Haiku, Opus, Sonnet
- **Tokens gesamt:** 29,413,798 (Haupt 9,550,999 · Subagent 19,862,799, Anteil 68 %)
- **Peak-Kontext:** ████████████ 149k / 150k
- **cache_read:** 26,516,107 · **Output:** 293,725

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ⚠️ Peak-Kontext 149k nahe am 150k-Korridor (>90 %) — geordnet beenden und frisch starten.
- ✅ 68% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 16,228,699 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: T2 B-128b DAMAGE-… ██████░░░░░░  79k    ✅
2   general-purpose: S181-Planning-Ent… █████████░░░ 107k    ✅
3   general-purpose: T4 Screenshot-Ber… █████░░░░░░░  68k    ✅
4   general-purpose: S181 Review DoD    ████░░░░░░░░  48k    ✅
5   general-purpose: T1 B-128a Doku + … ██████░░░░░░  79k    ✅
6   general-purpose: S181 Abschluss-Ar… █████████░░░ 106k    ✅
7   general-purpose: T3 M4 zweiter Aur… ███░░░░░░░░░  32k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  8,412
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    9%  2,595,554
cache_read     ▕████████████████████████▏   90%  26,516,107
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  293,725
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
Warm (System/Memory/History)  ▕████████████████████▏   90%  26,516,107
Neu gecacht (Tool-Ausgaben)   ▕██░░░░░░░░░░░░░░░░░░▏    9%  2,595,554
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  8,412
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  293,725
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 105 Sessions: 4,269,664,929 Token (47,531 Antworten).

