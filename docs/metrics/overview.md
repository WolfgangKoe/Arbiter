# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-06-29 20:37 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
06-28 20:02 1b3d  █████████░░░ 110k ↓    █████░  79% ↑  ···········▒
06-28 18:27 5ed6  ████████████ 153k ↑    ████░░  64% ↓  █···········
06-27 14:42 5af7  ██████░░░░░░  80k ↓    █████░  78% ↑  ███·········
06-27 12:39 9ef7  ███████████░ 137k ↑    ████░░  68% ↑  ██·······▒▒▒
06-27 10:21 02e7  ██░░░░░░░░░░  26k ↓    ███░░░  42% ↓  ············
06-27 07:30 8203  ██████████░░ 131k ↑    █████░  82% ↓  ████········
```

## Jüngste Session

**2026-06-28 20:02 · 1b3d129b**

- **Aufgabe:** start next session
- **Modelle:** Haupt Opus · Subagent Haiku, Opus, Sonnet
- **Tokens gesamt:** 38,773,413 (Haupt 8,263,880 · Subagent 30,509,533, Anteil 79 %)
- **Peak-Kontext:** █████████░░░ 110k / 150k
- **cache_read:** 36,336,822 · **Output:** 233,592

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 110k blieb im 150k-Korridor.
- ✅ 79% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 29,966,274 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: Schritt A Wound-B… ███░░░░░░░░░  39k    ✅
2   general-purpose: Schritt B Lauf 2b  ████████████ 159k    ⛔
3   general-purpose: Schritt B Coverag… ██████████░░ 125k    ⚠️
4   general-purpose: Schritt B Coverag… █████░░░░░░░  67k    ✅
5   general-purpose: Schritt 0 Nebenpu… ███░░░░░░░░░  43k    ✅
6   general-purpose: Marker-Fix korrig… ██░░░░░░░░░░  27k    ✅
7   general-purpose: Ruff-Lint-Fehler … ██░░░░░░░░░░  29k    ✅
8   Plan: Planning-Entwurf nächste Ses… ████░░░░░░░░  45k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  23,368
cache_creation ▕█░░░░░░░░░░░░░░░░░░░░░░░▏    6%  2,179,631
cache_read     ▕████████████████████████▏   94%  36,336,822
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  233,592
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
Warm (System/Memory/History)  ▕████████████████████▏   94%  36,336,822
Neu gecacht (Tool-Ausgaben)   ▕█░░░░░░░░░░░░░░░░░░░▏    6%  2,179,631
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  23,368
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  233,592
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 153 Sessions: 2,913,717,947 Token (28,907 Antworten).

