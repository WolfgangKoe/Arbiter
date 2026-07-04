# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-04 10:07 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-04 09:55 f800  ████░░░░░░░░  52k ↓    █████░  77% ↓  ▚▚··········
07-03 22:31 622e  ██████████░░ 126k ↑    █████░  82% ↓  ▚▚▚·········
07-03 19:27 2927  ██████████░░ 124k ↓    █████░  88% ↑  ▚···········
07-02 20:35 aa33  ███████████░ 133k ↓    ██░░░░  37% ↓  ▚▚▚▚▚██·····
07-01 21:41 bf59  ████████████ 144k ↑    ████░░  69% ↓  ▚▚▚█········
07-01 20:29 49a0  ████████████ 144k ↑    ████░░  74% ↑  ███████··▒▒▒
```

## Jüngste Session

**2026-07-04 09:55 · f800d10f**

- **Aufgabe:** start session - Plan durch Subagenten vorlegen
- **Modelle:** Haupt Fable · Subagent Fable, Sonnet
- **Tokens gesamt:** 5,486,529 (Haupt 1,241,296 · Subagent 4,245,233, Anteil 77 %)
- **Peak-Kontext:** ████░░░░░░░░ 52k / 150k
- **cache_read:** 4,692,063 · **Output:** 47,247

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 52k blieb im 150k-Korridor.
- ✅ 77% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 3,593,338 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: Executor: Task 0 … █████░░░░░░░  59k    ✅
2   general-purpose: Planner: Planning… ███████░░░░░  84k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  48,413
cache_creation ▕████░░░░░░░░░░░░░░░░░░░░▏   13%  698,806
cache_read     ▕████████████████████████▏   86%  4,692,063
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  47,247
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
Warm (System/Memory/History)  ▕████████████████████▏   86%  4,692,063
Neu gecacht (Tool-Ausgaben)   ▕███░░░░░░░░░░░░░░░░░▏   13%  698,806
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    1%  48,413
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  47,247
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 134 Sessions: 2,809,333,192 Token (28,496 Antworten).

