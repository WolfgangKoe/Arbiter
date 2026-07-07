# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-06 22:32 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-06 17:59 89a0  ██████████░░ 130k ↑    █████░  91% ↑  ▚▚▚▚▚·······
07-05 19:41 67da  ███████░░░░░  94k ↓    █████░  85% ↑  ▚▚··········
07-05 17:03 121e  ██████████░░ 130k ↓    ████░░  69% ↓  ▚▚▚▚█·······
07-05 13:00 5226  ████████████ 144k ↓    ████░░  74% ↑  ············
07-05 08:37 06c9  ████████████ 205k ↑    ████░░  66% ↓  ············
07-04 20:21 4f34  ██████████░░ 124k ↓    █████░  85% ↑  ············
```

## Jüngste Session

**2026-07-06 17:59 · 89a05bf1**

- **Aufgabe:** start session
- **Modelle:** Haupt Fable · Subagent Fable, Opus, Sonnet
- **Tokens gesamt:** 96,093,343 (Haupt 8,216,590 · Subagent 87,876,753, Anteil 91 %)
- **Peak-Kontext:** ██████████░░ 130k / 150k
- **cache_read:** 89,618,781 · **Output:** 496,465

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 130k blieb im 150k-Korridor.
- ✅ 91% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 48,570,143 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: Planning-Entwurf … ████████████ 160k    ⛔
2   general-purpose: Paket 4: Task 18.… █████████░░░ 112k    ✅
3   general-purpose: Abschluss S128: n… ██████░░░░░░  73k    ✅
4   general-purpose: Konsolidierung + … ████████████ 163k    ⛔
5   general-purpose: Paket 3: mypy gam… ███████░░░░░  91k    ✅
6   general-purpose: Executor: INV-4-L… █████████░░░ 114k    ✅
7   general-purpose: Paket 1: INV-4b-A… ████████████ 161k    ⛔
8   general-purpose: Executor: Plan 01… ██████████░░ 119k    ✅
9   general-purpose: Paket 2: mypy gam… ███████░░░░░  84k    ✅
10  general-purpose: Review S128 (DoD,… █████░░░░░░░  67k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  58,380
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    6%  5,919,717
cache_read     ▕████████████████████████▏   93%  89,618,781
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  496,465
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
Warm (System/Memory/History)  ▕████████████████████▏   93%  89,618,781
Neu gecacht (Tool-Ausgaben)   ▕█░░░░░░░░░░░░░░░░░░░▏    6%  5,919,717
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  58,380
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  496,465
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 123 Sessions: 2,936,632,397 Token (30,470 Antworten).

