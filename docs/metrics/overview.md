# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-06-25 18:42 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix: `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
06-24 22:27 e86c  ██████████░░ 130k ↓    ░░░░░░   0% ↓  ████████████
06-24 21:32 9726  ████████████ 162k ↓    █░░░░░  18% ↑  ██████████··
06-24 20:32 fb5f  ████████████ 177k ↑    ░░░░░░   4% ↓  ████████████
06-23 21:27 0ab4  ████████████ 166k ↓    ██░░░░  27% ↑  ███████████·
06-22 13:28 2813  ████████████ 171k ↑    ░░░░░░   3% ↑  ████████████
06-22 12:58 2627  ███████████░ 142k ↓    ░░░░░░   0% ↓  ████████████
```

## Jüngste Session

**2026-06-24 22:27 · e86cda96**

- **Aufgabe:** start session
- **Modelle:** Haupt Opus · Subagent —
- **Tokens gesamt:** 11,191,824 (Haupt 11,191,824 · Subagent 0, Anteil 0 %)
- **Peak-Kontext:** ██████████░░ 130k / 150k
- **cache_read:** 10,374,762 · **Output:** 92,433

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 130k blieb im 150k-Korridor.
- 💡 Große Session ohne Subagent — mechanische Fleißarbeit ließe sich an Sonnet/Haiku auslagern (CLAUDE.md, Tiering).

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

_keine Subagenten in der letzten Session._

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  23,248
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    6%  701,381
cache_read     ▕████████████████████████▏   93%  10,374,762
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  92,433
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

Σ über 170 Sessions: 2,857,107,107 Token (28,162 Antworten).

