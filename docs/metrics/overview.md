# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-06-21 15:24 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix: `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
06-21 13:14 a977  ████████████ 153k ↓    █░░░░░  19% ↓  ██████████··
06-21 10:05 de63  ████████████ 177k ↑    ████░░  72% ↑  ███·········
06-21 09:07 e19e  ███████████░ 142k ↓    ░░░░░░   0% ↓  ████████████
06-21 01:12 8fce  ████████████ 162k ↑    ░░░░░░   8% ↓  ███████████·
06-21 00:36 0702  ███████████░ 135k ↓    ███░░░  42% ↑  ███████·····
06-20 23:17 333b  ████████████ 144k ↑    ░░░░░░   0% →  ████████████
```

## Jüngste Session

**2026-06-21 13:14 · a977e6b5**

- **Aufgabe:** Start session. Was steht als nächstes im Backlog auf "zu tun"? bitte Auflisten und Tokenschätzung bitte.
- **Modelle:** Haupt Opus · Subagent Sonnet
- **Tokens gesamt:** 15,969,259 (Haupt 12,971,467 · Subagent 2,997,792, Anteil 19 %)
- **Peak-Kontext:** ████████████ 153k / 150k
- **cache_read:** 15,057,968 · **Output:** 190,328

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ⚠️ 9 von 118 Antworten lagen über dem 150k-Korridor — Session früher schneiden.
- ✅ 2,997,792 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: Silent-King targe… ███░░░░░░░░░  33k    ✅
2   general-purpose: Dice display 7+ g… ██████░░░░░░  80k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  37,529
cache_creation ▕█░░░░░░░░░░░░░░░░░░░░░░░▏    4%  683,434
cache_read     ▕████████████████████████▏   94%  15,057,968
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  190,328
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

Σ über 166 Sessions: 2,714,055,879 Token (26,770 Antworten).

