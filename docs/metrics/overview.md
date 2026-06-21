# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-06-21 12:33 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix: `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
06-21 10:05 de63  ███████████░ 137k ↓    █████░  81% ↑  ██··········
06-21 09:07 e19e  ███████████░ 142k ↓    ░░░░░░   0% ↓  ████████████
06-21 01:12 8fce  ████████████ 162k ↑    ░░░░░░   8% ↓  ███████████·
06-21 00:36 0702  ███████████░ 135k ↓    ███░░░  42% ↑  ███████·····
06-20 23:17 333b  ████████████ 144k ↑    ░░░░░░   0% →  ████████████
06-20 22:50 6feb  ███████░░░░░  88k ↓    ░░░░░░   0% ↓  ██████······
```

## Jüngste Session

**2026-06-21 10:05 · de63fb54**

- **Aufgabe:** Hier ist Abshcluss der letzten Session Session‑Abschluss (S78) Geliefert: Befund A (Pfeil‑Magnitude ←N/+N→) — umgesetzt…
- **Modelle:** Haupt Opus · Subagent Sonnet
- **Tokens gesamt:** 39,843,921 (Haupt 7,636,013 · Subagent 32,207,908, Anteil 81 %)
- **Peak-Kontext:** ███████████░ 137k / 150k
- **cache_read:** 37,845,220 · **Output:** 292,655

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ⚠️ Peak-Kontext 137k nahe am 150k-Korridor (>90 %) — geordnet beenden und frisch starten.
- ✅ 81% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 32,207,908 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: Reproduce Heroic … ████████████ 167k    ⛔
2   general-purpose: Phase 2 badge bug… ████░░░░░░░░  55k    ✅
3   general-purpose: Phase 3 codify in… █████░░░░░░░  60k    ✅
4   general-purpose: Phase 0 dice_html… ██████░░░░░░  71k    ✅
5   general-purpose: Phase 1 HI fix + … ██████░░░░░░  72k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  15,879
cache_creation ▕█░░░░░░░░░░░░░░░░░░░░░░░▏    4%  1,690,167
cache_read     ▕████████████████████████▏   95%  37,845,220
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  292,655
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

Σ über 165 Sessions: 2,692,897,274 Token (26,556 Antworten).

