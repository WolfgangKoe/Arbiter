# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-12 01:58 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-11 15:28 a4be  ███████████░ 136k ↓    █████░  86% ↓  ███·········
07-11 12:58 3d6e  ███████████░ 143k ↓    █████░  89% ↑  ▚▚▚█········
07-11 10:04 8553  ████████████ 178k ↑    ████░░  65% ↓  ▚▚▚▚▚▚▚▚····
07-10 21:31 e914  ███████████░ 134k ↓    █████░  89% ↑  ▚▚▚·········
07-10 16:04 54b0  ████████████ 197k ↑    █████░  83% ↓  ▚···········
07-10 13:33 b069  ████████████ 152k ↓    █████░  87% ↓  ▚▚▚▚▚·······
```

## Jüngste Session

**2026-07-11 15:28 · a4bed672**

- **Aufgabe:** start session
- **Modelle:** Haupt Fable, Opus · Subagent Fable, Haiku, Opus, Sonnet
- **Tokens gesamt:** 74,275,833 (Haupt 10,458,355 · Subagent 63,817,478, Anteil 86 %)
- **Peak-Kontext:** ███████████░ 136k / 150k
- **cache_read:** 68,221,366 · **Output:** 413,692

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ⚠️ Peak-Kontext 136k nahe am 150k-Korridor (>90 %) — geordnet beenden und frisch starten.
- ✅ 86% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 49,817,359 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: S139 Planning-Ent… █████████░░░ 106k    ✅
2   general-purpose: B12a: 5. Zustand … ███████████░ 135k    ⚠️
3   general-purpose: Cut-Them-Down-Lay… ██████░░░░░░  73k    ✅
4   general-purpose: INV-4b: 'never' i… ███░░░░░░░░░  33k    ✅
5   general-purpose: mypy-Ratchet game… ████░░░░░░░░  56k    ✅
6   general-purpose: Toten Code build_… ████░░░░░░░░  49k    ✅
7   general-purpose: B12c: Inline-Undo… ███████████░ 137k    ⚠️
8   general-purpose: Konzept Dynastie↔… ██████░░░░░░  81k    ✅
9   general-purpose: DoD-Review S139-A… ██████░░░░░░  70k    ✅
10  general-purpose: B12b: Karten-Anke… ████████████ 202k    ⛔
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  1,631
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    8%  5,639,144
cache_read     ▕████████████████████████▏   92%  68,221,366
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  413,692
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
Warm (System/Memory/History)  ▕████████████████████▏   92%  68,221,366
Neu gecacht (Tool-Ausgaben)   ▕██░░░░░░░░░░░░░░░░░░▏    8%  5,639,144
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  1,631
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  413,692
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 113 Sessions: 3,362,902,062 Token (35,863 Antworten).

