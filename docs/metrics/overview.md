# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-06-26 18:14 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix: `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
06-26 17:27 23e6  █████████░░░ 116k ↓    ██░░░░  39% ↑  █████████···
06-26 16:32 cf15  ███████████░ 136k ↑    █░░░░░  14% ↓  ██████████··
06-26 00:01 bfe5  ███████░░░░░  89k ↓    ███░░░  43% ↑  ███████·····
06-25 23:18 c50f  ████████████ 145k ↓    ██░░░░  36% ↑  ████████····
06-25 22:39 6357  ████████████ 188k ↑    ░░░░░░   0% ↓  ████████████
06-25 20:53 bb3d  ██████████░░ 124k ↑    █░░░░░  24% ↑  █████████▒▒▒
```

## Jüngste Session

**2026-06-26 17:27 · 23e6416b**

- **Aufgabe:** start session
- **Modelle:** Haupt Opus · Subagent Opus, Sonnet
- **Tokens gesamt:** 10,241,422 (Haupt 6,262,136 · Subagent 3,979,286, Anteil 39 %)
- **Peak-Kontext:** █████████░░░ 116k / 150k
- **cache_read:** 8,741,610 · **Output:** 176,816

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 116k blieb im 150k-Korridor.
- ✅ 39% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 2,718,983 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: Detail-plan Plan … ████████░░░░  99k    ✅
2   general-purpose: Session-Abschluss… ████░░░░░░░░  55k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  25,697
cache_creation ▕████░░░░░░░░░░░░░░░░░░░░▏   13%  1,297,299
cache_read     ▕████████████████████████▏   85%  8,741,610
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    2%  176,816
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

Σ über 172 Sessions: 2,927,190,700 Token (29,042 Antworten).

