# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-05 08:36 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-04 20:21 4f34  ██████████░░ 122k ↓    █████░  86% ↑  ············
07-04 14:45 b13e  ████████████ 147k ↑    ████░░  67% ↓  ▚▚▚█·······▒
07-04 09:55 f800  ███████████░ 133k ↑    ████░░  67% ↓  ▚▚▚▚▚█······
07-03 22:31 622e  ██████████░░ 126k ↑    █████░  82% ↓  ▚▚▚·········
07-03 19:27 2927  ██████████░░ 124k ↓    █████░  88% ↑  ▚···········
07-02 20:35 aa33  ███████████░ 133k ↓    ██░░░░  37% ↓  ▚▚▚▚▚██·····
```

## Jüngste Session

**2026-07-04 20:21 · 4f34b17d**

- **Aufgabe:** start session
- **Modelle:** Haupt Fable · Subagent Opus, Sonnet
- **Tokens gesamt:** 46,672,361 (Haupt 6,652,616 · Subagent 40,019,745, Anteil 86 %)
- **Peak-Kontext:** ██████████░░ 122k / 150k
- **cache_read:** 42,857,495 · **Output:** 357,324

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 122k blieb im 150k-Korridor.
- ✅ 86% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 38,876,780 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: HOCH-Datenfixes +… ███████████░ 133k    ⚠️
2   general-purpose: Auditpläne ins Ar… —                    —
3   general-purpose: Planning-Entwurf … ██████░░░░░░  76k    ✅
4   general-purpose: DoD-Review S123    █████░░░░░░░  58k    ✅
5   general-purpose: Abschluss-Doku S1… ███░░░░░░░░░  43k    ✅
6   general-purpose: Engine-Fix unit_k… ████████░░░░ 101k    ✅
7   general-purpose: Auditpläne und Ar… ████████████ 150k    ⚠️
8   general-purpose: Stratagem-Abgleic… ████████░░░░  94k    ✅
9   general-purpose: Stratagem-Abgleic… ███████░░░░░  88k    ✅
10  general-purpose: Auditpläne ins Ar… ███████░░░░░  92k    ✅
11  general-purpose: Stratagem-Abgleic… ███████░░░░░  91k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  35,497
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    7%  3,422,045
cache_read     ▕████████████████████████▏   92%  42,857,495
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  357,324
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
Warm (System/Memory/History)  ▕████████████████████▏   92%  42,857,495
Neu gecacht (Tool-Ausgaben)   ▕██░░░░░░░░░░░░░░░░░░▏    7%  3,422,045
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  35,497
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  357,324
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 124 Sessions: 2,790,565,933 Token (28,281 Antworten).

