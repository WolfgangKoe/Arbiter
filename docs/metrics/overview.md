# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-12 22:00 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-12 21:20 b358  ███████████░ 140k ↓    █████░  78% ↓  █·········▒▒
07-12 18:02 e7b9  ████████████ 146k ↑    █████░  83% ↑  ▚▚▚·········
07-12 18:02 8ee0  ███░░░░░░░░░  39k ↓    ░░░░░░   0% ↓  ▓▓▓▓▓▓▓▓▓▓▓▓
07-12 11:18 dedb  ████████████ 170k ↑    █████░  76% ↑  ▚▚▚▚········
07-12 02:03 76ce  █████████░░░ 119k ↓    ████░░  72% ↓  ▚▚▚█········
07-11 15:28 a4be  ████████████ 150k ↑    █████░  82% ↓  ███·········
```

## Jüngste Session

**2026-07-12 21:20 · b358187a**

- **Aufgabe:** Was auf dir liegt (manuelle UI-Verifikation): Insane Bravery ohne gewählte Einheit muss „locked" zeigen, mit Einheit lö…
- **Modelle:** Haupt Fable · Subagent Haiku, Opus, Sonnet
- **Tokens gesamt:** 35,480,741 (Haupt 7,809,191 · Subagent 27,671,550, Anteil 78 %)
- **Peak-Kontext:** ███████████░ 140k / 150k
- **cache_read:** 32,557,436 · **Output:** 433,821

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ⚠️ Peak-Kontext 140k nahe am 150k-Korridor (>90 %) — geordnet beenden und frisch starten.
- ✅ 78% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 23,893,050 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: W1-G on_target-An… █████░░░░░░░  61k    ✅
2   general-purpose: Stratagem-Existen… ██░░░░░░░░░░  26k    ✅
3   general-purpose: Planner S143 Plan… █████████░░░ 118k    ✅
4   general-purpose: DoD-Review S142 n… ███████░░░░░  84k    ✅
5   general-purpose: Fundort Eff.-Schw… ████░░░░░░░░  47k    ✅
6   general-purpose: W1-E Briefvorlage… ███░░░░░░░░░  35k    ✅
7   general-purpose: W1-F Stratagem-Ko… ██████░░░░░░  77k    ✅
8   general-purpose: W1-D Roster-Loade… ████░░░░░░░░  52k    ✅
9   Explore: Read dice_row_html render… █░░░░░░░░░░░  16k    ✅
10  general-purpose: W1-A Bugfix C Wou… ████████░░░░  98k    ✅
11  general-purpose: Regel-Lookup unmo… ██░░░░░░░░░░  31k    ✅
12  general-purpose: W1-B Bugfix A + R… ███████░░░░░  92k    ✅
13  Explore: Grep dice block callers a… ████░░░░░░░░  46k    ✅
14  general-purpose: W1-C abilityEngin… █████░░░░░░░  64k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  4,207
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    7%  2,485,277
cache_read     ▕████████████████████████▏   92%  32,557,436
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  433,821
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
Warm (System/Memory/History)  ▕████████████████████▏   92%  32,557,436
Neu gecacht (Tool-Ausgaben)   ▕██░░░░░░░░░░░░░░░░░░▏    7%  2,485,277
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  4,207
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  433,821
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 112 Sessions: 3,458,557,690 Token (37,122 Antworten).

