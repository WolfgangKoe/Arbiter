# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-04 09:48 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-03 22:31 622e  █████████░░░ 119k ↓    █████░  83% ↓  ▚▚▚·········
07-03 19:27 2927  ██████████░░ 124k ↓    █████░  88% ↑  ▚···········
07-02 20:35 aa33  ███████████░ 133k ↓    ██░░░░  37% ↓  ▚▚▚▚▚██·····
07-01 21:41 bf59  ████████████ 144k ↑    ████░░  69% ↓  ▚▚▚█········
07-01 20:29 49a0  ████████████ 144k ↑    ████░░  74% ↑  ███████··▒▒▒
07-01 18:47 b870  ███░░░░░░░░░  32k ↓    ░░░░░░   0% ↓  ▓▓▓▓▓▓▓▓▓▓▓▓
```

## Jüngste Session

**2026-07-03 22:31 · 622e1eb5**

- **Aufgabe:** &lt;task-notification&gt; &lt;task-id&gt;aa547245ccf957e39&lt;/task-id&gt; &lt;tool-use-id&gt;toolu_017ra8SugfobQvLCE1P3LSfw&lt;/tool-use-id&gt; &lt;out…
- **Modelle:** Haupt Fable · Subagent Fable, Opus, Sonnet
- **Tokens gesamt:** 35,734,806 (Haupt 6,013,905 · Subagent 29,720,901, Anteil 83 %)
- **Peak-Kontext:** █████████░░░ 119k / 150k
- **cache_read:** 32,818,901 · **Output:** 259,430

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 119k blieb im 150k-Korridor.
- ✅ 83% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 21,723,524 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: Review S120 nach … ████░░░░░░░░  51k    ✅
2   general-purpose: Phase-2-Plan Desi… █████████░░░ 108k    ✅
3   general-purpose: Konsens in design… ████████░░░░ 102k    ✅
4   general-purpose: S120-Abschluss: z… ████████████ 150k    ⛔
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  116,302
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    7%  2,540,173
cache_read     ▕████████████████████████▏   92%  32,818,901
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  259,430
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
Warm (System/Memory/History)  ▕████████████████████▏   92%  32,818,901
Neu gecacht (Tool-Ausgaben)   ▕██░░░░░░░░░░░░░░░░░░▏    7%  2,540,173
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  116,302
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  259,430
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 133 Sessions: 2,800,519,763 Token (28,370 Antworten).

