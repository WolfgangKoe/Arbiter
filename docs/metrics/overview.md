# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-04 14:01 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-04 09:55 f800  ████████░░░░  97k ↓    ████░░  70% ↓  ▚▚▚▚▚▚▚▚····
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
- **Tokens gesamt:** 19,785,964 (Haupt 5,937,588 · Subagent 13,848,376, Anteil 70 %)
- **Peak-Kontext:** ████████░░░░ 97k / 150k
- **cache_read:** 17,329,445 · **Output:** 128,001

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 97k blieb im 150k-Korridor.
- ✅ 70% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 5,014,623 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: Executor: Task 0 … █████████░░░ 111k    ✅
2   general-purpose: Planner: Planning… ███████░░░░░  84k    ✅
3   general-purpose: Root-Cause: Crash… █████░░░░░░░  62k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  78,213
cache_creation ▕███░░░░░░░░░░░░░░░░░░░░░▏   11%  2,250,305
cache_read     ▕████████████████████████▏   88%  17,329,445
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  128,001
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
Warm (System/Memory/History)  ▕████████████████████▏   88%  17,329,445
Neu gecacht (Tool-Ausgaben)   ▕███░░░░░░░░░░░░░░░░░▏   11%  2,250,305
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  78,213
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  128,001
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 134 Sessions: 2,823,632,627 Token (28,683 Antworten).

