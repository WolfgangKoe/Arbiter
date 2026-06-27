# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-06-27 14:35 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
06-27 12:39 9ef7  ██████████░░ 130k ↑    ████░░  70% ↑  █········▒▒▒
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
- **Tokens gesamt:** 28,455,822 (Haupt 8,420,712 · Subagent 20,035,110, Anteil 70 %)
- **Peak-Kontext:** ██████████░░ 130k / 150k
- **cache_read:** 26,137,487 · **Output:** 231,300

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 130k blieb im 150k-Korridor.
- ✅ 70% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 17,628,910 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: Executor Plan 025… █████░░░░░░░  59k    ✅
2   general-purpose: Root-Cause D2 Sch… ███░░░░░░░░░  41k    ✅
3   general-purpose: Executor Plan 025… █████░░░░░░░  58k    ✅
4   general-purpose: Doku-Fix Plan 025… ████░░░░░░░░  49k    ✅
5   general-purpose: Abschluss-Artefak… ███░░░░░░░░░  36k    ✅
6   general-purpose: Executor Plan 025… ███████░░░░░  93k    ✅
7   general-purpose: Planning-Entwurf … ██████░░░░░░  73k    ✅
8   general-purpose: Fix D2 Schuss-Spe… █████░░░░░░░  64k    ✅
9   general-purpose: Review D2-Bugfix   ████░░░░░░░░  47k    ✅
10  general-purpose: Abschluss-Artefak… ███░░░░░░░░░  36k    ✅
11  general-purpose: Reviewer Plan 025… ████░░░░░░░░  51k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  38,254
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    7%  2,048,781
cache_read     ▕████████████████████████▏   92%  26,137,487
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  231,300
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
Warm (System/Memory/History)  ▕████████████████████▏   92%  26,137,487
Neu gecacht (Tool-Ausgaben)   ▕██░░░░░░░░░░░░░░░░░░▏    7%  2,048,781
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  38,254
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  231,300
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 168 Sessions: 2,968,779,305 Token (29,743 Antworten).

