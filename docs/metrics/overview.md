# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-18 22:15 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-18 20:59 6cfc  ████████░░░░  97k ↓    █████░  90% ↑  █···········
07-18 20:08 00eb  ███████████░ 140k ↑    ████░░  64% ↓  ██··········
07-18 12:29 cd6c  ██████████░░ 122k ↑    ████░░  73% ↓  █···········
07-18 11:00 b53c  █████████░░░ 109k ↓    █████░  85% ↑  ············
07-18 09:08 be5c  ████████████ 162k ↑    █████░  82% ↓  ············
07-17 23:54 b982  █████████░░░ 110k ↓    ██████  95% ↑  ············
```

## Jüngste Session

**2026-07-18 20:59 · 6cfc9b70**

- **Aufgabe:** start Session. Wir übernehmen keine der Retromaßnahmen aus der letzten Session. Opus soll den Plan für diese Session du…
- **Modelle:** Haupt Fable · Subagent Haiku, Opus, Sonnet
- **Tokens gesamt:** 41,091,403 (Haupt 3,955,585 · Subagent 37,135,818, Anteil 90 %)
- **Peak-Kontext:** ████████░░░░ 97k / 150k
- **cache_read:** 37,957,975 · **Output:** 300,895

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 97k blieb im 150k-Korridor.
- ✅ 90% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 33,887,720 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: T4: §7-Spec-Überf… █████████░░░ 108k    ✅
2   general-purpose: T3: B-123 UI + Re… ████████████ 159k    ⛔
3   general-purpose: S168-Planning-Ent… █████████░░░ 111k    ✅
4   general-purpose: T5: S168 DoD-Revi… █████░░░░░░░  65k    ✅
5   general-purpose: T2: B-123 Core-Fi… ████████████ 175k    ⛔
6   general-purpose: T1: B-123 Regel-L… ████░░░░░░░░  44k    ✅
7   general-purpose: T5b: S168 Abschlu… ████████░░░░ 104k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  15,185
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    7%  2,817,348
cache_read     ▕████████████████████████▏   92%  37,957,975
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  300,895
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
Warm (System/Memory/History)  ▕████████████████████▏   92%  37,957,975
Neu gecacht (Tool-Ausgaben)   ▕█░░░░░░░░░░░░░░░░░░░▏    7%  2,817,348
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  15,185
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  300,895
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 128 Sessions: 4,158,804,316 Token (47,717 Antworten).

