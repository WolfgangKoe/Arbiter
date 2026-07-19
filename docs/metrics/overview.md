# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-19 18:50 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-19 16:41 4f3a  ██████████░░ 120k ↓    █████░  84% ↑  █··········▒
07-19 13:44 3636  ████████████ 182k ↑    █████░  82% ↓  ··········▒▒
07-18 22:58 067a  ███████████░ 133k ↑    ██████  94% ↑  ············
07-18 20:59 6cfc  ██████████░░ 126k ↓    █████░  83% ↑  █···········
07-18 20:08 00eb  ███████████░ 140k ↑    ████░░  64% ↓  ██··········
07-18 12:29 cd6c  ██████████░░ 122k ↑    ████░░  73% ↓  █···········
```

## Jüngste Session

**2026-07-19 16:41 · 4f3aa7b3**

- **Aufgabe:** start session, wir übernehmen alle drei Retromaßnahmen.
- **Modelle:** Haupt Fable · Subagent Haiku, Opus, Sonnet
- **Tokens gesamt:** 43,442,124 (Haupt 6,769,582 · Subagent 36,672,542, Anteil 84 %)
- **Peak-Kontext:** ██████████░░ 120k / 150k
- **cache_read:** 40,145,734 · **Output:** 247,644

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 120k blieb im 150k-Korridor.
- ✅ 84% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 33,587,337 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: S171-Review (DoD … ██████░░░░░░  70k    ✅
2   general-purpose: S171-Planning-Ent… ██████░░░░░░  74k    ✅
3   general-purpose: T4: Verifikations… ███░░░░░░░░░  34k    ✅
4   general-purpose: T3-d1: Direkt-App… ████████████ 156k    ⛔
5   general-purpose: T2: Teilhaken + H… ███░░░░░░░░░  39k    ✅
6   general-purpose: T3-d2: Render-Tei… ████████████ 163k    ⛔
7   general-purpose: T1: Retro-M1/M2 v… ███░░░░░░░░░  37k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  1,366
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    7%  3,047,380
cache_read     ▕████████████████████████▏   92%  40,145,734
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  247,644
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
Warm (System/Memory/History)  ▕████████████████████▏   92%  40,145,734
Neu gecacht (Tool-Ausgaben)   ▕██░░░░░░░░░░░░░░░░░░▏    7%  3,047,380
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  1,366
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  247,644
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 127 Sessions: 4,382,094,708 Token (49,318 Antworten).

