# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-03 22:16 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-03 19:27 2927  ████████░░░░ 104k ↓    █████░  91% ↑  ▚···········
07-02 20:35 aa33  ███████████░ 133k ↓    ██░░░░  37% ↓  ▚▚▚▚▚██·····
07-01 21:41 bf59  ████████████ 144k ↑    ████░░  69% ↓  ▚▚▚█········
07-01 20:29 49a0  ████████████ 144k ↑    ████░░  74% ↑  ███████··▒▒▒
07-01 18:47 b870  ███░░░░░░░░░  32k ↓    ░░░░░░   0% ↓  ▓▓▓▓▓▓▓▓▓▓▓▓
06-30 23:20 9fe6  ██████████░░ 122k ↓    ███░░░  57% ↓  █·········▒▒
```

## Jüngste Session

**2026-07-03 19:27 · 2927d113**

- **Aufgabe:** start session
- **Modelle:** Haupt Fable · Subagent Fable, Opus, Sonnet
- **Tokens gesamt:** 37,312,392 (Haupt 3,529,477 · Subagent 33,782,915, Anteil 91 %)
- **Peak-Kontext:** ████████░░░░ 104k / 150k
- **cache_read:** 33,643,725 · **Output:** 308,246

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 104k blieb im 150k-Korridor.
- ✅ 91% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 29,832,956 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: Stratagem-Anzeige… █████░░░░░░░  65k    ✅
2   general-purpose: Doku: Ziel6 schli… █████████░░░ 114k    ✅
3   general-purpose: Executor Task 3 P… ████████░░░░ 102k    ✅
4   general-purpose: Reviewer DoD-Revi… ████░░░░░░░░  52k    ✅
5   general-purpose: Planner-Entwurf f… ████████████ 146k    ⚠️
6   general-purpose: Executor Task 2 P… ██████░░░░░░  78k    ✅
7   general-purpose: Abschluss S119 au… ███████░░░░░  92k    ✅
8   general-purpose: Executor Task 1 P… █████░░░░░░░  65k    ✅
9   general-purpose: Planner Ziel7-Neu… ███████████░ 132k    ⚠️
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  209,329
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    8%  3,151,092
cache_read     ▕████████████████████████▏   90%  33,643,725
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  308,246
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
Warm (System/Memory/History)  ▕████████████████████▏   90%  33,643,725
Neu gecacht (Tool-Ausgaben)   ▕██░░░░░░░░░░░░░░░░░░▏    8%  3,151,092
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    1%  209,329
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  308,246
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 136 Sessions: 2,832,953,016 Token (28,717 Antworten).

