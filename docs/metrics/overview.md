# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-16 21:04 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-16 20:22 a6af  ████████████ 153k ↑    ████░░  69% ↑  █·········▒▒
07-16 19:40 decf  ██████████░░ 129k ↓    ░░░░░░   6% ↓  ············
07-16 18:03 471e  ████████████ 149k ↑    █████░  86% ↑  ············
07-16 09:35 de37  ███████████░ 139k ↑    █████░  85% ↓  ▚▚··········
07-15 21:58 ad76  ██████████░░ 127k ↑    █████░  91% ↑  ▚▚·········▒
07-15 19:12 9dd1  █████████░░░ 106k ↓    █████░  86% ↑  █··········▒
```

## Jüngste Session

**2026-07-16 20:22 · a6af1597**

- **Aufgabe:** start session
- **Modelle:** Haupt Fable · Subagent Haiku, Opus, Sonnet
- **Tokens gesamt:** 34,050,681 (Haupt 10,689,234 · Subagent 23,361,447, Anteil 69 %)
- **Peak-Kontext:** ████████████ 153k / 150k
- **cache_read:** 31,368,663 · **Output:** 357,893

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ⚠️ 5 von 105 Antworten lagen über dem 150k-Korridor — Session früher schneiden.
- ✅ 69% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 21,779,301 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: Executor: Backlog… █████░░░░░░░  57k    ✅
2   general-purpose: Executor B-019: A… █████░░░░░░░  57k    ✅
3   general-purpose: Executor B-025: S… ████░░░░░░░░  56k    ✅
4   general-purpose: Executor B-009: P… ████░░░░░░░░  52k    ✅
5   general-purpose: Planner: S154-Ent… █████████░░░ 116k    ✅
6   general-purpose: Executor B-087: O… ██████░░░░░░  72k    ✅
7   general-purpose: Executor B-072: K… ███░░░░░░░░░  37k    ✅
8   general-purpose: Executor B-053: G… ███░░░░░░░░░  39k    ✅
9   general-purpose: Executor B-068: S… ██████░░░░░░  70k    ✅
10  general-purpose: Reviewer: DoD-Rev… ████░░░░░░░░  51k    ✅
11  general-purpose: Executor B-036: B… ██████░░░░░░  74k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  1,977
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    7%  2,322,148
cache_read     ▕████████████████████████▏   92%  31,368,663
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  357,893
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
Warm (System/Memory/History)  ▕████████████████████▏   92%  31,368,663
Neu gecacht (Tool-Ausgaben)   ▕█░░░░░░░░░░░░░░░░░░░▏    7%  2,322,148
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  1,977
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  357,893
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 118 Sessions: 3,639,004,345 Token (41,143 Antworten).

