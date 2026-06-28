# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-06-28 19:59 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
06-28 18:27 5ed6  ████████████ 149k ↑    ████░░  68% ↓  █···········
06-27 14:42 5af7  ██████░░░░░░  80k ↓    █████░  78% ↑  ███·········
06-27 12:39 9ef7  ███████████░ 137k ↑    ████░░  68% ↑  ██·······▒▒▒
06-27 10:21 02e7  ██░░░░░░░░░░  26k ↓    ███░░░  42% ↓  ············
06-27 07:30 8203  ██████████░░ 131k ↑    █████░  82% ↓  ████········
06-26 22:48 72c5  ██████░░░░░░  78k ↓    █████░  85% ↑  ············
```

## Jüngste Session

**2026-06-28 18:27 · 5ed6267d**

- **Aufgabe:** Start Session. Folgende Ergänzungen für Planungs-Agent. 2 Bugs zum Concering Tyrant Protokoll: 1. D2: Retreat & Shoot f…
- **Modelle:** Haupt Opus · Subagent Opus, Sonnet
- **Tokens gesamt:** 30,867,679 (Haupt 9,804,830 · Subagent 21,062,849, Anteil 68 %)
- **Peak-Kontext:** ████████████ 149k / 150k
- **cache_read:** 28,883,180 · **Output:** 262,462

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ⚠️ Peak-Kontext 149k nahe am 150k-Korridor (>90 %) — geordnet beenden und frisch starten.
- ✅ 68% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 19,153,988 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: Planner: Conqueri… ████████████ 155k    ⛔
2   general-purpose: Executor: Conquer… ████████░░░░  97k    ✅
3   general-purpose: Executor: Dense-C… ████░░░░░░░░  52k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  19,240
cache_creation ▕█░░░░░░░░░░░░░░░░░░░░░░░▏    6%  1,702,797
cache_read     ▕████████████████████████▏   94%  28,883,180
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  262,462
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
Warm (System/Memory/History)  ▕████████████████████▏   94%  28,883,180
Neu gecacht (Tool-Ausgaben)   ▕█░░░░░░░░░░░░░░░░░░░▏    6%  1,702,797
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  19,240
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  262,462
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 157 Sessions: 2,927,674,491 Token (29,171 Antworten).

