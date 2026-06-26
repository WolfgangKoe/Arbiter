# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-06-26 22:36 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix: `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
06-26 22:24 654b  ██████████░░ 121k ↓    ██░░░░  32% ↑  ████████····
06-26 18:17 3d7c  ████████████ 168k ↑    ░░░░░░   0% ↓  ████████████
06-26 18:17 0c87  ██████████░░ 128k ↑    ████░░  71% ↑  ████········
06-26 17:27 23e6  ██████████░░ 128k ↓    ██░░░░  37% ↑  █████████···
06-26 16:32 cf15  ███████████░ 136k ↑    █░░░░░  14% ↓  ██████████··
06-26 00:01 bfe5  ███████░░░░░  89k ↓    ███░░░  43% ↑  ███████·····
```

## Jüngste Session

**2026-06-26 22:24 · 654bda63**

- **Aufgabe:** start session
- **Modelle:** Haupt Opus · Subagent Sonnet
- **Tokens gesamt:** 5,297,956 (Haupt 3,578,080 · Subagent 1,719,876, Anteil 32 %)
- **Peak-Kontext:** ██████████░░ 121k / 150k
- **cache_read:** 4,724,547 · **Output:** 76,865

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 121k blieb im 150k-Korridor.
- ✅ 32% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 1,719,876 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   Plan: Draft Doku-Org + Reporting p… ██████░░░░░░  78k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  13,933
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    9%  482,611
cache_read     ▕████████████████████████▏   89%  4,724,547
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  76,865
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

Σ über 174 Sessions: 2,963,198,104 Token (29,533 Antworten).

