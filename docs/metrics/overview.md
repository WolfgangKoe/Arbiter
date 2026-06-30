# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-06-30 22:44 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
06-30 22:03 8996  █████████░░░ 111k ↑    █████░  82% ↑  ············
06-30 20:54 ac89  █████████░░░ 108k ↓    ████░░  62% ↓  ██····▒▒▒▒▒▒
06-30 18:46 fce6  ███████████░ 133k ↓    ████░░  75% ↑  ███········▒
06-29 20:55 c673  ████████████ 162k ↑    ████░░  74% ↑  █··········▒
06-28 20:02 1b3d  ███████████░ 135k ↓    ████░░  73% ↑  ···········▒
06-28 18:27 5ed6  ████████████ 153k ↑    ████░░  64% ↓  █···········
```

## Jüngste Session

**2026-06-30 22:03 · 8996deff**

- **Aufgabe:** Beginne die nächste Session und starte den Plan-subagenten. Mich interessiert vor allem, was noch zur Erfüllung von zie…
- **Modelle:** Haupt Opus · Subagent Opus, Sonnet
- **Tokens gesamt:** 20,844,777 (Haupt 3,783,108 · Subagent 17,061,669, Anteil 82 %)
- **Peak-Kontext:** █████████░░░ 111k / 150k
- **cache_read:** 18,990,792 · **Output:** 210,092

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 111k blieb im 150k-Korridor.
- ✅ 82% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 16,396,342 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: Design-System Res… █████████░░░ 109k    ✅
2   Plan: Session-Planung Ziel6-Abschl… ████████░░░░  97k    ✅
3   general-purpose: Ziel6 Status-Inve… ████████░░░░  98k    ✅
4   general-purpose: Executor Test-Pak… ███████░░░░░  92k    ✅
5   general-purpose: DoD-Review Sessio… █████░░░░░░░  61k    ✅
6   general-purpose: Executor commandP… █████░░░░░░░  68k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  19,163
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    8%  1,624,730
cache_read     ▕████████████████████████▏   91%  18,990,792
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  210,092
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
Warm (System/Memory/History)  ▕████████████████████▏   91%  18,990,792
Neu gecacht (Tool-Ausgaben)   ▕██░░░░░░░░░░░░░░░░░░▏    8%  1,624,730
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  19,163
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  210,092
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 152 Sessions: 2,982,032,210 Token (30,111 Antworten).

