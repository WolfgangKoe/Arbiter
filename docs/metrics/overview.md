# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-06-26 17:22 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix: `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
06-26 16:32 cf15  ██████████░░ 120k ↑    █░░░░░  18% ↓  ██████████··
06-26 00:01 bfe5  ███████░░░░░  89k ↓    ███░░░  43% ↑  ███████·····
06-25 23:18 c50f  ████████████ 145k ↓    ██░░░░  36% ↑  ████████····
06-25 22:39 6357  ████████████ 188k ↑    ░░░░░░   0% ↓  ████████████
06-25 20:53 bb3d  ██████████░░ 124k ↑    █░░░░░  24% ↑  █████████▒▒▒
06-25 20:23 2f61  █████████░░░ 117k ↓    ░░░░░░   0% →  ████████████
```

## Jüngste Session

**2026-06-26 16:32 · cf1566cc**

- **Aufgabe:** Beginnen wir die nächste Session, allerdings unterbrechen wir den aktuellen Plan und ziehen den Carry-over vor. Ich möc…
- **Modelle:** Haupt Opus · Subagent Opus, Sonnet
- **Tokens gesamt:** 8,192,329 (Haupt 6,701,371 · Subagent 1,490,958, Anteil 18 %)
- **Peak-Kontext:** ██████████░░ 120k / 150k
- **cache_read:** 6,782,166 · **Output:** 193,766

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 120k blieb im 150k-Korridor.
- ✅ 1,403,967 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: Draft agent_scope… ███░░░░░░░░░  39k    ✅
2   general-purpose: Mailbox round-tri… ██░░░░░░░░░░  22k    ✅
3   claude-code-guide: Claude Code sub… █████░░░░░░░  58k    ✅
4   general-purpose: Repo index / code… ███░░░░░░░░░  40k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  23,583
cache_creation ▕████░░░░░░░░░░░░░░░░░░░░▏   15%  1,192,814
cache_read     ▕████████████████████████▏   83%  6,782,166
output         ▕█░░░░░░░░░░░░░░░░░░░░░░░▏    2%  193,766
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

Σ über 171 Sessions: 2,914,274,133 Token (28,869 Antworten).

