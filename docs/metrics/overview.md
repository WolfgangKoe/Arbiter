# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-16 20:17 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-16 19:40 decf  ██████████░░ 123k ↓    ░░░░░░   7% ↓  ············
07-16 18:03 471e  ████████████ 149k ↑    █████░  86% ↑  ············
07-16 09:35 de37  ███████████░ 139k ↑    █████░  85% ↓  ▚▚··········
07-15 21:58 ad76  ██████████░░ 127k ↑    █████░  91% ↑  ▚▚·········▒
07-15 19:12 9dd1  █████████░░░ 106k ↓    █████░  86% ↑  █··········▒
07-15 19:12 628e  ████████████ 164k ↑    ███░░░  42% ↓  ············
```

## Jüngste Session

**2026-07-16 19:40 · decf492d**

- **Aufgabe:** start session. Ein paar kleine Nachträge zum Backlog-Feinschliff. Die ID Spalte ist immer noch zu klein. Dagegen ist di…
- **Modelle:** Haupt Fable · Subagent Sonnet
- **Tokens gesamt:** 6,542,579 (Haupt 6,067,419 · Subagent 475,160, Anteil 7 %)
- **Peak-Kontext:** ██████████░░ 123k / 150k
- **cache_read:** 5,664,267 · **Output:** 137,363

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 123k blieb im 150k-Korridor.
- ✅ 475,160 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: Planner: S153-Pla… ██████░░░░░░  78k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  141
cache_creation ▕███░░░░░░░░░░░░░░░░░░░░░▏   11%  740,808
cache_read     ▕████████████████████████▏   87%  5,664,267
output         ▕█░░░░░░░░░░░░░░░░░░░░░░░▏    2%  137,363
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
Warm (System/Memory/History)  ▕████████████████████▏   87%  5,664,267
Neu gecacht (Tool-Ausgaben)   ▕███░░░░░░░░░░░░░░░░░▏   11%  740,808
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  141
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    2%  137,363
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 117 Sessions: 3,603,673,074 Token (40,551 Antworten).

