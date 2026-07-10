# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-10 16:22 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-10 16:04 54b0  █████░░░░░░░  62k ↓    █████░  82% ↓  ············
07-10 13:33 b069  ████████████ 152k ↓    █████░  87% ↓  ▚▚▚▚▚·······
07-10 01:56 86c3  ████████████ 163k ↑    █████░  87% ↑  ▚▚··········
07-09 20:34 5769  ████████░░░░ 103k ↓    █████░  81% ↑  ▚··········▒
07-09 20:34 19cb  ████████████ 173k ↓    ██░░░░  38% ↓  ·······▒▒▒▒▒
07-09 17:14 bd4b  ████████████ 173k ↑    ████░░  62% ↓  ▚···········
```

## Jüngste Session

**2026-07-10 16:04 · 54b0c4dc**

- **Aufgabe:** start session
- **Modelle:** Haupt Fable · Subagent Sonnet
- **Tokens gesamt:** 6,668,341 (Haupt 1,201,433 · Subagent 5,466,908, Anteil 82 %)
- **Peak-Kontext:** █████░░░░░░░ 62k / 150k
- **cache_read:** 5,741,382 · **Output:** 61,679

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 62k blieb im 150k-Korridor.
- ✅ 82% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 5,466,908 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: S135 Planning-Ent… ███████░░░░░  93k    ✅
2   general-purpose: Aufgabe 1: Entsch… ███████░░░░░  85k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  91,579
cache_creation ▕███░░░░░░░░░░░░░░░░░░░░░▏   12%  773,701
cache_read     ▕████████████████████████▏   86%  5,741,382
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  61,679
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
Warm (System/Memory/History)  ▕████████████████████▏   86%  5,741,382
Neu gecacht (Tool-Ausgaben)   ▕███░░░░░░░░░░░░░░░░░▏   12%  773,701
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    1%  91,579
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  61,679
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 114 Sessions: 3,224,444,113 Token (32,675 Antworten).

