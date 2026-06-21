# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-06-21 06:59 UTC

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix: `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
06-20 23:12 8fce  ███████████░ 143k ↑    █░░░░░  11% ↓  ███████████·
06-20 22:36 0702  ███████████░ 135k ↓    ███░░░  42% ↑  ███████·····
06-20 21:17 333b  ████████████ 144k ↑    ░░░░░░   0% →  ████████████
06-20 20:50 6feb  ███████░░░░░  88k ↓    ░░░░░░   0% ↓  ██████······
06-20 20:11 58e9  ███████░░░░░  93k ↓    ████░░  59% ↑  ············
06-20 19:54 78e2  █████████░░░ 107k ↓    ░░░░░░   0% ↓  ············
```

## Jüngste Session

**2026-06-20 23:12 · 8fce93a2**

- **Aufgabe:** Start session. Was sind die nächsten Schritte mit Tokenschätzung.
- **Modelle:** Haupt <synthetic>, Opus · Subagent Sonnet
- **Tokens gesamt:** 18,783,285 (Haupt 16,792,918 · Subagent 1,990,367, Anteil 11 %)
- **Peak-Kontext:** ███████████░ 143k / 150k
- **cache_read:** 17,733,516 · **Output:** 184,297

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ⚠️ Peak-Kontext 143k nahe am 150k-Korridor (>90 %) — geordnet beenden und frisch starten.
- ✅ 1,990,367 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: Investigate Step … ████░░░░░░░░  48k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  45,340
cache_creation ▕█░░░░░░░░░░░░░░░░░░░░░░░▏    4%  820,132
cache_read     ▕████████████████████████▏   94%  17,733,516
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  184,297
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

Σ über 163 Sessions: 2,632,587,109 Token (25,798 Antworten).

