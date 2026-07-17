# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-17 21:29 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-17 19:45 04ab  ███████████░ 137k ↓    █████░  76% ↑  █···········
07-17 18:44 ffc7  ████████████ 159k ↓    ████░░  67% ↓  ·······▒▒▒▒▒
07-17 15:58 1e74  ████████████ 160k ↓    ████░░  74% ↓  ··········▒▒
07-17 13:27 73bd  ████████████ 160k ↑    █████░  88% ↑  ···········▒
07-17 10:38 6342  ████████████ 160k ↑    █████░  85% ↓  ···········▒
07-17 08:26 0dfe  ████████████ 155k ↑    █████░  89% ↑  ············
```

## Jüngste Session

**2026-07-17 19:45 · 04abb172**

- **Aufgabe:** start session wir übernehmen M1 aus der Retro.
- **Modelle:** Haupt Fable, Opus · Subagent Haiku, Opus, Sonnet
- **Tokens gesamt:** 38,201,515 (Haupt 9,226,010 · Subagent 28,975,505, Anteil 76 %)
- **Peak-Kontext:** ███████████░ 137k / 150k
- **cache_read:** 34,707,521 · **Output:** 345,847

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ⚠️ Peak-Kontext 137k nahe am 150k-Korridor (>90 %) — geordnet beenden und frisch starten.
- ✅ 76% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 27,306,192 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: Abschluss-Dreikla… ████░░░░░░░░  50k    ✅
2   general-purpose: Wiring: Invuln-Qu… ███████░░░░░  84k    ✅
3   general-purpose: Review S161 gegen… █████░░░░░░░  69k    ✅
4   general-purpose: Task 1: AWAITING-… ████░░░░░░░░  52k    ✅
5   general-purpose: Backlog-Status B-… ████░░░░░░░░  44k    ✅
6   general-purpose: Task 3: B-105 go_… ██████████░░ 120k    ⚠️
7   general-purpose: Task 4: B-119 pri… ████░░░░░░░░  48k    ✅
8   general-purpose: Task 5: Retro-Ent… ████░░░░░░░░  51k    ✅
9   general-purpose: Task 2: B-109 Aut… ████████░░░░ 101k    ✅
10  general-purpose: Planning-Entwurf … ███████████░ 140k    ⚠️
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  1,129
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    8%  3,147,018
cache_read     ▕████████████████████████▏   91%  34,707,521
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  345,847
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
Warm (System/Memory/History)  ▕████████████████████▏   91%  34,707,521
Neu gecacht (Tool-Ausgaben)   ▕██░░░░░░░░░░░░░░░░░░▏    8%  3,147,018
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  1,129
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  345,847
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 123 Sessions: 3,863,839,304 Token (44,426 Antworten).

