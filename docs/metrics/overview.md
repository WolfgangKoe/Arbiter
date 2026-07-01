# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-01 20:28 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-01 18:47 b870  ███░░░░░░░░░  32k ↓    ░░░░░░   0% ↓  ▓▓▓▓▓▓▓▓▓▓▓▓
06-30 23:20 9fe6  ██████████░░ 121k ↓    ████░░  59% ↓  █·········▒▒
06-30 22:03 8996  ███████████░ 140k ↑    ████░░  72% ↑  ············
06-30 20:54 ac89  █████████░░░ 108k ↓    ████░░  62% ↓  ██····▒▒▒▒▒▒
06-30 18:46 fce6  ███████████░ 133k ↓    ████░░  75% ↑  ███········▒
06-29 20:55 c673  ████████████ 162k ↑    ████░░  74% ↑  █··········▒
```

## Jüngste Session

**2026-07-01 18:47 · b870f718**

- **Aufgabe:** Sonnet 5 ist nun verfügbar. Passe bitte die Settings an, damit Sonnet 5 statt Sonnet 4.6 genutzt wird.
- **Modelle:** Haupt Sonnet · Subagent —
- **Tokens gesamt:** 463,616 (Haupt 463,616 · Subagent 0, Anteil 0 %)
- **Peak-Kontext:** ███░░░░░░░░░ 32k / 150k
- **cache_read:** 367,473 · **Output:** 6,340

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 32k blieb im 150k-Korridor.
- ✅ 463,616 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

_keine Subagenten in der letzten Session._

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  33
cache_creation ▕██████░░░░░░░░░░░░░░░░░░▏   19%  89,770
cache_read     ▕████████████████████████▏   79%  367,473
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  6,340
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
Warm (System/Memory/History)  ▕████████████████████▏   79%  367,473
Neu gecacht (Tool-Ausgaben)   ▕█████░░░░░░░░░░░░░░░▏   19%  89,770
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  33
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  6,340
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 151 Sessions: 2,982,991,873 Token (30,123 Antworten).

