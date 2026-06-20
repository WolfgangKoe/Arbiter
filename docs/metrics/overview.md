# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-06-20 23:08 UTC

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix: `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
06-20 22:36 0702  █████████░░░ 119k ↓    ███░░░  51% ↑  ██████······
06-20 21:17 333b  ████████████ 144k ↑    ░░░░░░   0% →  ████████████
06-20 20:50 6feb  ███████░░░░░  88k ↓    ░░░░░░   0% ↓  ██████······
06-20 20:11 58e9  ███████░░░░░  93k ↓    ████░░  59% ↑  ············
06-20 19:54 78e2  █████████░░░ 107k ↓    ░░░░░░   0% ↓  ············
06-20 17:19 63cc  ████████████ 156k ↑    ███░░░  48% ↓  ············
```

## Jüngste Session

**2026-06-20 22:36 · 07026b3b**

- **Aufgabe:** start Session, was sind dienächsten Schritte, bitte vorlegen und eine Tolen Schätzung dran.
- **Modelle:** Haupt Opus · Subagent Sonnet
- **Tokens gesamt:** 14,792,525 (Haupt 7,250,197 · Subagent 7,542,328, Anteil 51 %)
- **Peak-Kontext:** █████████░░░ 119k / 150k
- **cache_read:** 14,094,226 · **Output:** 170,979

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 119k blieb im 150k-Korridor.
- ✅ 51% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 7,542,328 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: Implement Plan 02… ███████░░░░░  93k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  27,432
cache_creation ▕█░░░░░░░░░░░░░░░░░░░░░░░▏    3%  499,888
cache_read     ▕████████████████████████▏   95%  14,094,226
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  170,979
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

Σ über 162 Sessions: 2,610,456,580 Token (25,542 Antworten).

