# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-06-24 21:28 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix: `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
06-24 20:32 fb5f  ████████████ 159k ↓    ░░░░░░   5% ↓  ███████████·
06-23 21:27 0ab4  ████████████ 166k ↓    ██░░░░  27% ↑  ███████████·
06-22 13:28 2813  ████████████ 171k ↑    ░░░░░░   3% ↑  ████████████
06-22 12:58 2627  ███████████░ 142k ↓    ░░░░░░   0% ↓  ████████████
06-22 00:21 6b94  ████████████ 145k ↓    █░░░░░  19% ↑  ██████████··
06-21 23:51 08bb  ████████████ 172k ↓    █░░░░░  17% ↑  ██████████··
```

## Jüngste Session

**2026-06-24 20:32 · fb5f6a02**

- **Aufgabe:** Ich bin ein wenig lost. Wo stehen wir jetzt?
- **Modelle:** Haupt Opus · Subagent Sonnet
- **Tokens gesamt:** 21,714,259 (Haupt 20,678,425 · Subagent 1,035,834, Anteil 5 %)
- **Peak-Kontext:** ████████████ 159k / 150k
- **cache_read:** 20,628,825 · **Output:** 269,354

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ⚠️ 12 von 204 Antworten lagen über dem 150k-Korridor — Session früher schneiden.
- ✅ 1,035,834 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: Context-engineeri… ██████░░░░░░  79k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  38,925
cache_creation ▕█░░░░░░░░░░░░░░░░░░░░░░░▏    4%  777,155
cache_read     ▕████████████████████████▏   95%  20,628,825
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  269,354
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

Σ über 168 Sessions: 2,825,445,516 Token (27,801 Antworten).

