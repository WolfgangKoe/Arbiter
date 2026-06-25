# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-06-25 23:48 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix: `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
06-25 23:18 c50f  ██████████░░ 121k ↓    ███░░░  44% ↑  ████████····
06-25 22:39 6357  ████████████ 188k ↑    ░░░░░░   0% ↓  ████████████
06-25 20:53 bb3d  ██████████░░ 124k ↑    █░░░░░  24% ↑  █████████▒▒▒
06-25 20:23 2f61  █████████░░░ 117k ↓    ░░░░░░   0% →  ████████████
06-25 19:52 2d95  ██████████░░ 123k ↓    ░░░░░░   0% ↓  ████████████
06-25 19:02 0aa5  ████████████ 149k ↓    ██░░░░  27% ↑  █████████···
```

## Jüngste Session

**2026-06-25 23:18 · c50fcaa1**

- **Aufgabe:** Danke für die Design-Frage, So muss es sein. Für D2 ist hier ein Hinweis sinnvoll, weil wir hier eine Hybrid Ability ha…
- **Modelle:** Haupt Opus · Subagent Opus, Sonnet
- **Tokens gesamt:** 12,723,148 (Haupt 7,142,024 · Subagent 5,581,124, Anteil 44 %)
- **Peak-Kontext:** ██████████░░ 121k / 150k
- **cache_read:** 11,976,589 · **Output:** 93,617

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 121k blieb im 150k-Korridor.
- ✅ 44% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 4,576,385 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: Implement Plan 02… ██████░░░░░░  78k    ✅
2   general-purpose: Continue Step 3 i… ███░░░░░░░░░  39k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  22,916
cache_creation ▕█░░░░░░░░░░░░░░░░░░░░░░░▏    5%  630,026
cache_read     ▕████████████████████████▏   94%  11,976,589
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  93,617
```

**Legende & Zielwerte:**

- **input** — neue, ungecachte Tokens → niedrig halten.
- **cache_creation** — erstmals gecacht (einmalig teurer) → moderat, unvermeidbar bei neuem Kontext.
- **cache_read** — aus warmem Cache gelesen (günstig) → **hoher Anteil = gut** (Kontext bleibt warm, Cache-TTL ~5 Min).
- **output** — generierte Tokens; **kein Selbstzweck — Qualität vor Menge.** Ein höherer Output-Anteil *relativ zu* cache_read kann Ziele schneller erreichen, *sofern das Ergebnis trägt*; viel cache_read bei wenig substanziellem Output = Reibung, "Mist"-Output ist schädlich, nicht gut.

**Zielbild:** hoher cache_read-Anteil + niedriger input-Anteil = effizientes Arbeiten; Output bewusst gegen Qualität gewichtet (nicht maximieren). Viele Cache-Misses (hoher input nach Pausen > 5 Min) sind ein Warnsignal.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 174 Sessions: 2,926,103,784 Token (28,960 Antworten).

