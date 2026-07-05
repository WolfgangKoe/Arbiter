# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-05 12:59 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-05 08:37 06c9  ████████████ 204k ↑    ████░░  67% ↓  ············
07-04 20:21 4f34  ██████████░░ 124k ↓    █████░  85% ↑  ············
07-04 14:45 b13e  ████████████ 147k ↑    ████░░  67% ↓  ▚▚▚█·······▒
07-04 09:55 f800  ███████████░ 133k ↑    ████░░  67% ↓  ▚▚▚▚▚█······
07-03 22:31 622e  ██████████░░ 126k ↑    █████░  82% ↓  ▚▚▚·········
07-03 19:27 2927  ██████████░░ 124k ↓    █████░  88% ↑  ▚···········
```

## Jüngste Session

**2026-07-05 08:37 · 06c903a9**

- **Aufgabe:** &lt;task-notification&gt; &lt;task-id&gt;aa626a408ef671ba4&lt;/task-id&gt; &lt;tool-use-id&gt;toolu_01Pv5NfwenLUHp4V21hguKJ9&lt;/tool-use-id&gt; &lt;out…
- **Modelle:** Haupt Fable · Subagent Sonnet
- **Tokens gesamt:** 38,569,331 (Haupt 12,690,870 · Subagent 25,878,461, Anteil 67 %)
- **Peak-Kontext:** ████████████ 204k / 150k
- **cache_read:** 35,045,852 · **Output:** 400,082

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ⚠️ 32 von 110 Antworten lagen über dem 150k-Korridor — Session früher schneiden.
- ✅ 67% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 25,878,461 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   Explore: Audit correctness/bugs     ████████████ 188k    ⛔
2   Explore: Audit security             ████████░░░░  96k    ✅
3   Explore: Audit tests/debt/perf      ████████░░░░ 105k    ✅
4   Explore: Audit deps/DX/docs/direct… ████░░░░░░░░  52k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  33,351
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    8%  3,090,046
cache_read     ▕████████████████████████▏   91%  35,045,852
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  400,082
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
Warm (System/Memory/History)  ▕████████████████████▏   91%  35,045,852
Neu gecacht (Tool-Ausgaben)   ▕██░░░░░░░░░░░░░░░░░░▏    8%  3,090,046
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  33,351
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  400,082
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 125 Sessions: 2,829,754,567 Token (28,735 Antworten).

