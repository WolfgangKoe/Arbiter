# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-06-26 00:23 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix: `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
06-26 00:01 bfe5  ██████░░░░░░  69k ↓    ████░░  65% ↑  ████········
06-25 23:18 c50f  ████████████ 145k ↓    ██░░░░  36% ↑  ████████····
06-25 22:39 6357  ████████████ 188k ↑    ░░░░░░   0% ↓  ████████████
06-25 20:53 bb3d  ██████████░░ 124k ↑    █░░░░░  24% ↑  █████████▒▒▒
06-25 20:23 2f61  █████████░░░ 117k ↓    ░░░░░░   0% →  ████████████
06-25 19:52 2d95  ██████████░░ 123k ↓    ░░░░░░   0% ↓  ████████████
```

## Jüngste Session

**2026-06-26 00:01 · bfe55b74**

- **Aufgabe:** Freigabe. Bitte nutze Haiku oder Sonnet Agenten so viel wie öglich.
- **Modelle:** Haupt Opus · Subagent Sonnet
- **Tokens gesamt:** 6,845,065 (Haupt 2,379,321 · Subagent 4,465,744, Anteil 65 %)
- **Peak-Kontext:** ██████░░░░░░ 69k / 150k
- **cache_read:** 6,418,787 · **Output:** 51,139

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 69k blieb im 150k-Korridor.
- ✅ 65% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 4,465,744 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: Badge-Label-Bug f… █████░░░░░░░  66k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  13,717
cache_creation ▕█░░░░░░░░░░░░░░░░░░░░░░░▏    5%  361,422
cache_read     ▕████████████████████████▏   94%  6,418,787
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  51,139
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

Σ über 175 Sessions: 2,937,299,934 Token (29,152 Antworten).

