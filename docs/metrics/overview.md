# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-15 21:56 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-15 19:12 9dd1  █████████░░░ 106k ↓    █████░  86% ↑  █··········▒
07-15 19:12 628e  ████████████ 156k ↑    ███░░░  44% ↓  ············
07-15 17:44 ac36  ████████████ 154k ↓    █████░  88% ↑  ▚█··········
07-14 20:50 df5b  ████████████ 169k ↑    █████░  78% ↓  █···········
07-14 19:48 9c2d  ███████████░ 133k ↑    █████░  81% ↑  ▚▚▚▚▚█······
07-14 18:43 2574  ██████████░░ 126k ↑    ███░░░  57% ↓  ············
```

## Jüngste Session

**2026-07-15 19:12 · 9dd15bf3**

- **Aufgabe:** start session
- **Modelle:** Haupt Fable · Subagent Fable, Haiku, Opus, Sonnet
- **Tokens gesamt:** 40,101,044 (Haupt 5,511,255 · Subagent 34,589,789, Anteil 86 %)
- **Peak-Kontext:** █████████░░░ 106k / 150k
- **cache_read:** 37,688,331 · **Output:** 246,671

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 106k blieb im 150k-Korridor.
- ✅ 86% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 31,424,819 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: Reviewer S149 (Do… ██████░░░░░░  72k    ✅
2   general-purpose: Executor Welle 1+… ███████████░ 137k    ⚠️
3   general-purpose: Roster-Recherche … ██████░░░░░░  79k    ✅
4   general-purpose: Planner: Session-… ████████████ 144k    ⚠️
5   general-purpose: Handoff-Triage (A… ██████░░░░░░  78k    ✅
6   general-purpose: Executor B7+B8 Ph… █████████░░░ 116k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  1,482
cache_creation ▕█░░░░░░░░░░░░░░░░░░░░░░░▏    5%  2,164,560
cache_read     ▕████████████████████████▏   94%  37,688,331
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  246,671
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
Warm (System/Memory/History)  ▕████████████████████▏   94%  37,688,331
Neu gecacht (Tool-Ausgaben)   ▕█░░░░░░░░░░░░░░░░░░░▏    5%  2,164,560
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  1,482
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  246,671
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 114 Sessions: 3,429,199,841 Token (38,843 Antworten).

