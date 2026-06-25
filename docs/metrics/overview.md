# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-06-25 22:37 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix: `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
06-25 20:53 bb3d  █████████░░░ 118k ↑    ██░░░░  27% ↑  █████████▒▒▒
06-25 20:23 2f61  █████████░░░ 117k ↓    ░░░░░░   0% →  ████████████
06-25 19:52 2d95  ██████████░░ 123k ↓    ░░░░░░   0% ↓  ████████████
06-25 19:02 0aa5  ████████████ 149k ↓    ██░░░░  27% ↑  █████████···
06-24 22:27 e86c  ████████████ 152k ↓    ░░░░░░   0% ↓  ████████████
06-24 21:32 9726  ████████████ 162k ↓    █░░░░░  18% ↑  ██████████··
```

## Jüngste Session

**2026-06-25 20:53 · bb3dbf84**

- **Aufgabe:** ÜBerlege, wofür du Subagenten einsetzen kannst. Wichtig!
- **Modelle:** Haupt Opus · Subagent Haiku
- **Tokens gesamt:** 9,639,971 (Haupt 7,056,444 · Subagent 2,583,527, Anteil 27 %)
- **Peak-Kontext:** █████████░░░ 118k / 150k
- **cache_read:** 8,836,409 · **Output:** 165,035

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 118k blieb im 150k-Korridor.
- ✅ 2,583,527 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   Explore: Recherche combat/engine V… ████░░░░░░░░  56k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  15,318
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    6%  623,209
cache_read     ▕████████████████████████▏   92%  8,836,409
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    2%  165,035
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

Σ über 172 Sessions: 2,884,163,995 Token (28,551 Antworten).

