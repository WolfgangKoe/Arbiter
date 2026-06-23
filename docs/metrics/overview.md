# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-06-23 21:17 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix: `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
06-22 13:28 2813  ████████████ 156k ↑    ░░░░░░   4% ↑  ████████████
06-22 12:58 2627  ███████████░ 142k ↓    ░░░░░░   0% ↓  ████████████
06-22 00:21 6b94  ████████████ 145k ↓    █░░░░░  19% ↑  ██████████··
06-21 23:51 08bb  ████████████ 172k ↓    █░░░░░  17% ↑  ██████████··
06-21 22:47 73d2  ████████████ 185k ↑    █░░░░░  10% ↑  ███████████·
06-21 20:33 92d9  ████████████ 162k ↓    ░░░░░░   4% ↑  ████████████
```

## Jüngste Session

**2026-06-22 13:28 · 2813de22**

- **Aufgabe:** start session
- **Modelle:** Haupt Opus · Subagent Sonnet
- **Tokens gesamt:** 19,280,730 (Haupt 18,488,254 · Subagent 792,476, Anteil 4 %)
- **Peak-Kontext:** ████████████ 156k / 150k
- **cache_read:** 18,030,336 · **Output:** 192,087

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ⚠️ 8 von 180 Antworten lagen über dem 150k-Korridor — Session früher schneiden.
- ✅ 792,476 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: Verify Undying Le… ██░░░░░░░░░░  27k    ✅
2   general-purpose: Investigate overv… ███░░░░░░░░░  44k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  29,738
cache_creation ▕█░░░░░░░░░░░░░░░░░░░░░░░▏    5%  1,028,569
cache_read     ▕████████████████████████▏   94%  18,030,336
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  192,087
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

Σ über 174 Sessions: 2,866,567,678 Token (28,387 Antworten).

