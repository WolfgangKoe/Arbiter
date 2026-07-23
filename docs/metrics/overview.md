# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-23 17:03 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-23 16:34 695b  ██████████░░ 124k ↓    ████░░  66% ↑  ████▒▒▒▒▒▒▒▒
07-22 20:41 2123  ████████████ 224k ↑    ███░░░  56% ↓  ············
07-22 19:15 dbc6  ████████████ 166k ↑    ████░░  73% ↓  █···········
07-21 19:23 1c15  ████████████ 152k ↓    █████░  80% ↑  ██··········
07-21 17:57 4c40  ████████████ 158k ↑    ███░░░  51% ↓  █···········
07-20 21:40 813e  ███████████░ 137k ↓    █████░  83% ↑  ██··········
```

## Jüngste Session

**2026-07-23 16:34 · 695b8861**

- **Aufgabe:** &lt;task-notification&gt; &lt;task-id&gt;a6a0a25186de68f40&lt;/task-id&gt; &lt;tool-use-id&gt;toolu_01CcxJv56v6KoSWDL1vGAGgv&lt;/tool-use-id&gt; &lt;out…
- **Modelle:** Haupt Fable · Subagent Haiku, Opus
- **Tokens gesamt:** 19,001,161 (Haupt 6,439,907 · Subagent 12,561,254, Anteil 66 %)
- **Peak-Kontext:** ██████████░░ 124k / 150k
- **cache_read:** 17,130,785 · **Output:** 186,154

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 124k blieb im 150k-Korridor.
- ✅ 66% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 8,893,802 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: A5 Review S179 (D… █████░░░░░░░  65k    ✅
2   general-purpose: A3 Handoff-Hygiene ████░░░░░░░░  51k    ✅
3   general-purpose: S180-Planning-Ent… █████░░░░░░░  68k    ✅
4   general-purpose: A1+A2 Verifikatio… █████████░░░ 114k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  1,357
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    9%  1,682,865
cache_read     ▕████████████████████████▏   90%  17,130,785
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  186,154
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
Warm (System/Memory/History)  ▕████████████████████▏   90%  17,130,785
Neu gecacht (Tool-Ausgaben)   ▕██░░░░░░░░░░░░░░░░░░▏    9%  1,682,865
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  1,357
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  186,154
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 103 Sessions: 4,206,757,584 Token (46,668 Antworten).

