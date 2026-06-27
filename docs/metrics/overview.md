# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-06-27 13:44 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
06-27 12:39 9ef7  █████░░░░░░░  66k ↑    █████░  84% ↑  █········▒▒▒
06-27 10:21 02e7  ██░░░░░░░░░░  26k ↓    ███░░░  42% ↓  ············
06-27 07:30 8203  ██████████░░ 131k ↑    █████░  82% ↓  ████········
06-26 22:48 72c5  ██████░░░░░░  78k ↓    █████░  85% ↑  ············
06-26 22:24 654b  ███████████░ 141k ↓    █░░░░░  24% ↑  ············
06-26 18:17 3d7c  ████████████ 168k ↓    ░░░░░░   0% ↓  ▓▓▓▓▓▓▓▓▓▓▓▓
```

## Jüngste Session

**2026-06-27 12:39 · 9ef7a257**

- **Aufgabe:** start session
- **Modelle:** Haupt Opus · Subagent Haiku, Opus, Sonnet
- **Tokens gesamt:** 15,651,785 (Haupt 2,572,637 · Subagent 13,079,148, Anteil 84 %)
- **Peak-Kontext:** █████░░░░░░░ 66k / 150k
- **cache_read:** 14,337,970 · **Output:** 91,675

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 66k blieb im 150k-Korridor.
- ✅ 84% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 12,337,390 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: Executor Plan 025… █████░░░░░░░  59k    ✅
2   general-purpose: Executor Plan 025… █████░░░░░░░  58k    ✅
3   general-purpose: Executor Plan 025… ███████░░░░░  93k    ✅
4   general-purpose: Planning-Entwurf … ██████░░░░░░  73k    ✅
5   general-purpose: Reviewer Plan 025… ███░░░░░░░░░  43k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  22,972
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    8%  1,199,168
cache_read     ▕████████████████████████▏   92%  14,337,970
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  91,675
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
Warm (System/Memory/History)  ▕████████████████████▏   92%  14,337,970
Neu gecacht (Tool-Ausgaben)   ▕██░░░░░░░░░░░░░░░░░░▏    8%  1,199,168
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  22,972
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  91,675
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 168 Sessions: 2,955,975,268 Token (29,500 Antworten).

