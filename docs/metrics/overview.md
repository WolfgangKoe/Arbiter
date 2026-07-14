# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-14 19:42 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-14 18:43 2574  ██████████░░ 119k ↑    ███░░░  55% ↓  ············
07-14 18:43 a845  █████████░░░ 107k ↓    ████░░  66% ↑  ▚▚▚▚▚▚▚▚▚▚··
07-12 22:23 0149  ████████████ 174k ↑    ████░░  61% ↑  ▚▚█·········
07-12 21:20 9271  ████████████ 154k ↑    ░░░░░░   0% ↓  ▓▓▓▓▓▓▓▓▓▓▓▓
07-12 21:20 b358  ████████████ 152k ↑    ████░░  71% ↓  █·········▒▒
07-12 18:02 e7b9  ████████████ 146k ↑    █████░  83% ↑  ▚▚▚·········
```

## Jüngste Session

**2026-07-14 18:43 · 257436e2**

- **Aufgabe:** Bevor wir weiter machen, müssen wir die branches gegeneinander auflösen. Neben dev und main haben wir noch einen dritte…
- **Modelle:** Haupt Fable · Subagent Sonnet
- **Tokens gesamt:** 10,557,030 (Haupt 4,726,051 · Subagent 5,830,979, Anteil 55 %)
- **Peak-Kontext:** ██████████░░ 119k / 150k
- **cache_read:** 9,311,921 · **Output:** 115,783

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 119k blieb im 150k-Korridor.
- ✅ 55% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 5,830,979 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: Prioritäten-Konso… ████████░░░░  94k    ✅
2   general-purpose: Stufe-B-Verifikat… ██████░░░░░░  73k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  301
cache_creation ▕███░░░░░░░░░░░░░░░░░░░░░▏   11%  1,129,025
cache_read     ▕████████████████████████▏   88%  9,311,921
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  115,783
```

**Legende & Zielwerte:**

- **input** — neue, ungecachte Tokens → niedrig halten.
- **cache_creation** — erstmals gecacht (einmalig teurer) → moderat, unvermeidbar bei neuem Kontext.
- **cache_read** — aus warmem Cache gelesen (günstig) → **hoher Anteil = gut** (Kontext bleibt warm, Cache-TTL ~5 Min).
- **output** — generierte Tokens; **kein Selbstzweck — Qualität vor Menge.** Ein höherer Output-Anteil *relativ zu* cache_read kann Ziele schneller erreichen, *sofern das Ergebnis trägt*; viel cache_read bei wenig substanziellem Output = Reibung, "Mist"-Output ist schädlich, nicht gut.

**Zielbild:** hoher cache_read-Anteil + niedriger input-Anteil = effizientes Arbeiten; Output bewusst gegen Qualität gewichtet (nicht maximieren). Viele Cache-Misses (hoher input nach Pausen > 5 Min) sind ein Warnsignal.

## Kontext-Zusammensetzung (nach Quelle, approximiert)

_Approximation: exakte Per-Quelle-Aufschlüsselung ist im Transcript nicht verfügbar. Orientiert an Wegner 2026 / context-engineering-slides.md._

```text
Warm (System/Memory/History)  ▕████████████████████▏   88%  9,311,921
Neu gecacht (Tool-Ausgaben)   ▕██░░░░░░░░░░░░░░░░░░▏   11%  1,129,025
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  301
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  115,783
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 109 Sessions: 3,186,146,425 Token (36,200 Antworten).

