# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-23 17:51 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-23 17:16 fe07  ████████░░░░  97k ↓    █████░  81% ↑  █·····▒▒▒▒▒▒
07-23 16:34 695b  ██████████░░ 128k ↓    ████░░  63% ↑  ███▒▒▒▒▒▒▒▒▒
07-22 20:41 2123  ████████████ 224k ↑    ███░░░  56% ↓  ············
07-22 19:15 dbc6  ████████████ 166k ↑    ████░░  73% ↓  █···········
07-21 19:23 1c15  ████████████ 152k ↓    █████░  80% ↑  ██··········
07-21 17:57 4c40  ████████████ 158k ↑    ███░░░  51% ↓  █···········
```

## Jüngste Session

**2026-07-23 17:16 · fe079215**

- **Aufgabe:** &lt;task-notification&gt; &lt;task-id&gt;a31d04897596d72d7&lt;/task-id&gt; &lt;tool-use-id&gt;toolu_01SMhvXBshLnZaxM8X84PbgD&lt;/tool-use-id&gt; &lt;out…
- **Modelle:** Haupt Fable · Subagent Haiku, Opus, Sonnet
- **Tokens gesamt:** 31,792,488 (Haupt 6,086,693 · Subagent 25,705,795, Anteil 81 %)
- **Peak-Kontext:** ████████░░░░ 97k / 150k
- **cache_read:** 29,859,168 · **Output:** 177,764

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 97k blieb im 150k-Korridor.
- ✅ 81% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 24,266,658 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: B-131-Nachbesseru… ██████████░░ 121k    ⚠️
2   general-purpose: Review S180 B-131… █████░░░░░░░  60k    ✅
3   general-purpose: B-131-Verifikatio… ███████░░░░░  85k    ✅
4   general-purpose: C1: Doku-Handoff … █████████░░░ 111k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  2,824
cache_creation ▕█░░░░░░░░░░░░░░░░░░░░░░░▏    6%  1,752,732
cache_read     ▕████████████████████████▏   94%  29,859,168
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  177,764
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
Warm (System/Memory/History)  ▕████████████████████▏   94%  29,859,168
Neu gecacht (Tool-Ausgaben)   ▕█░░░░░░░░░░░░░░░░░░░▏    6%  1,752,732
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  2,824
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  177,764
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 104 Sessions: 4,239,553,831 Token (47,117 Antworten).

