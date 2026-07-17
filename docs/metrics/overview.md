# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-17 23:41 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-17 22:16 d275  ████████░░░░ 106k ↓    █████░  90% ↑  █···········
07-17 21:32 8096  ███████████░ 143k ↑    █████░  79% ↑  █···········
07-17 19:45 04ab  ███████████░ 140k ↓    ████░░  74% ↑  █···········
07-17 18:44 ffc7  ████████████ 159k ↓    ████░░  67% ↓  ·······▒▒▒▒▒
07-17 15:58 1e74  ████████████ 160k ↓    ████░░  74% ↓  ··········▒▒
07-17 13:27 73bd  ████████████ 160k ↑    █████░  88% ↑  ···········▒
```

## Jüngste Session

**2026-07-17 22:16 · d27554b4**

- **Aufgabe:** start session
- **Modelle:** Haupt Fable · Subagent Opus, Sonnet
- **Tokens gesamt:** 47,492,678 (Haupt 4,896,639 · Subagent 42,596,039, Anteil 90 %)
- **Peak-Kontext:** ████████░░░░ 106k / 150k
- **cache_read:** 44,825,937 · **Output:** 270,933

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 106k blieb im 150k-Korridor.
- ✅ 90% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 38,188,374 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: DoD-Review S163 (… ██████░░░░░░  79k    ✅
2   general-purpose: T1: mypy-Drift re… █████████░░░ 118k    ✅
3   general-purpose: Abschluss S163: A… ██████░░░░░░  71k    ✅
4   general-purpose: Planning-Entwurf … ███████░░░░░  89k    ✅
5   general-purpose: Feedback vollstän… ████░░░░░░░░  49k    ✅
6   general-purpose: T2: gloom_prism-M… ████████████ 175k    ⛔
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  1,136
cache_creation ▕█░░░░░░░░░░░░░░░░░░░░░░░▏    5%  2,394,672
cache_read     ▕████████████████████████▏   94%  44,825,937
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  270,933
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
Warm (System/Memory/History)  ▕████████████████████▏   94%  44,825,937
Neu gecacht (Tool-Ausgaben)   ▕█░░░░░░░░░░░░░░░░░░░▏    5%  2,394,672
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  1,136
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  270,933
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 125 Sessions: 3,948,071,919 Token (45,407 Antworten).

