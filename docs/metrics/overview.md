# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-18 20:04 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-18 12:29 cd6c  █████████░░░ 117k ↑    ████░░  72% ↓  █···········
07-18 11:00 b53c  █████████░░░ 109k ↓    █████░  85% ↑  ············
07-18 09:08 be5c  ████████████ 162k ↑    █████░  82% ↓  ············
07-17 23:54 b982  █████████░░░ 110k ↓    ██████  95% ↑  ············
07-17 22:16 d275  █████████░░░ 116k ↓    █████░  89% ↑  █···········
07-17 21:32 8096  ███████████░ 143k ↑    █████░  79% ↑  █···········
```

## Jüngste Session

**2026-07-18 12:29 · cd6ce717**

- **Aufgabe:** Task 4 fertig — B-123 Diagnose: Mischfall, Entscheidung nötig Befund: Es gibt zwei Schadens-Pfade in apply_damage() (un…
- **Modelle:** Haupt Fable · Subagent Opus, Sonnet
- **Tokens gesamt:** 13,776,834 (Haupt 3,853,978 · Subagent 9,922,856, Anteil 72 %)
- **Peak-Kontext:** █████████░░░ 117k / 150k
- **cache_read:** 11,360,384 · **Output:** 246,140

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 117k blieb im 150k-Korridor.
- ✅ 72% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 9,024,172 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: S166 DoD-Review (… █████░░░░░░░  58k    ✅
2   general-purpose: Explodes-Mockup V… ███████░░░░░  87k    ✅
3   general-purpose: B-123 Nachdiagnos… ███████░░░░░  86k    ✅
4   general-purpose: S166 Abschluss + … ███████████░ 131k    ⚠️
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  362
cache_creation ▕█████░░░░░░░░░░░░░░░░░░░▏   16%  2,169,948
cache_read     ▕████████████████████████▏   82%  11,360,384
output         ▕█░░░░░░░░░░░░░░░░░░░░░░░▏    2%  246,140
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
Warm (System/Memory/History)  ▕████████████████████▏   82%  11,360,384
Neu gecacht (Tool-Ausgaben)   ▕████░░░░░░░░░░░░░░░░▏   16%  2,169,948
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  362
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    2%  246,140
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 126 Sessions: 4,093,667,504 Token (46,972 Antworten).

