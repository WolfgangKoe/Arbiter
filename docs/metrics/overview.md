# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-06-21 10:02 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix: `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
06-21 09:07 e19e  ███████████░ 138k ↓    ░░░░░░   0% ↓  ████████████
06-21 01:12 8fce  ████████████ 162k ↑    ░░░░░░   8% ↓  ███████████·
06-21 00:36 0702  ███████████░ 135k ↓    ███░░░  42% ↑  ███████·····
06-20 23:17 333b  ████████████ 144k ↑    ░░░░░░   0% →  ████████████
06-20 22:50 6feb  ███████░░░░░  88k ↓    ░░░░░░   0% ↓  ██████······
06-20 22:11 58e9  ███████░░░░░  93k ↓    ████░░  59% ↑  ············
```

## Jüngste Session

**2026-06-21 09:07 · e19e2fe0**

- **Aufgabe:** start next session + freigabe. Bitte starte die APP für UI Überprüfung und der zu prüfenden Fälle. Schau, ob für alles…
- **Modelle:** Haupt Opus · Subagent —
- **Tokens gesamt:** 13,544,008 (Haupt 13,544,008 · Subagent 0, Anteil 0 %)
- **Peak-Kontext:** ███████████░ 138k / 150k
- **cache_read:** 12,527,584 · **Output:** 212,482

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ⚠️ Peak-Kontext 138k nahe am 150k-Korridor (>90 %) — geordnet beenden und frisch starten.
- 💡 Große Session ohne Subagent — mechanische Fleißarbeit ließe sich an Sonnet/Haiku auslagern (CLAUDE.md, Tiering).

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

_keine Subagenten in der letzten Session._

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  17,244
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    6%  786,698
cache_read     ▕████████████████████████▏   92%  12,527,584
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    2%  212,482
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

Σ über 164 Sessions: 2,651,785,383 Token (25,996 Antworten).

