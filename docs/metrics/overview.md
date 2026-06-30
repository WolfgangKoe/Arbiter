# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-06-30 18:37 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
06-29 20:55 c673  ██████████░░ 122k ↓    █████░  79% ↑  █··········▒
06-28 20:02 1b3d  ███████████░ 135k ↓    ████░░  73% ↑  ···········▒
06-28 18:27 5ed6  ████████████ 153k ↑    ████░░  64% ↓  █···········
06-27 14:42 5af7  ██████░░░░░░  80k ↓    █████░  78% ↑  ███·········
06-27 12:39 9ef7  ███████████░ 137k ↑    ████░░  68% ↑  ██·······▒▒▒
06-27 10:21 02e7  ██░░░░░░░░░░  26k ↓    ███░░░  42% ↓  ············
```

## Jüngste Session

**2026-06-29 20:55 · c67384fd**

- **Aufgabe:** start session. Ich habe noch folgendes offen, dafür bitte die App starten oD-6 UI-Check: Im laufenden Streamlit bei 2 g…
- **Modelle:** Haupt Opus · Subagent Haiku, Opus, Sonnet
- **Tokens gesamt:** 28,201,836 (Haupt 6,040,916 · Subagent 22,160,920, Anteil 79 %)
- **Peak-Kontext:** ██████████░░ 122k / 150k
- **cache_read:** 25,400,627 · **Output:** 256,771

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 122k blieb im 150k-Korridor.
- ✅ 79% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 21,386,428 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   Explore: Toten Reroll-Loop analysi… ██░░░░░░░░░░  30k    ✅
2   Explore: Recherche 2 Protokoll-Met… ████░░░░░░░░  49k    ✅
3   Explore: Recherche 2 Protokoll-Met… ███░░░░░░░░░  39k    ✅
4   Plan: Planning-Entwurf nächste Ses… ██████░░░░░░  78k    ✅
5   claude: Coverage-Gate auf 99 setzen ███░░░░░░░░░  39k    ✅
6   claude: Executor B: ability_engine… █████░░░░░░░  64k    ✅
7   claude: Executor A: game_state Cov… ███████░░░░░  85k    ✅
8   Explore: Bestandsaufnahme Ziel6/Au… █████░░░░░░░  66k    ✅
9   claude: Executor C: Plan 016 RP-Hi… ███████░░░░░  81k    ✅
10  claude: Coverage-Gate auf 99 setzen ██░░░░░░░░░░  25k    ✅
11  Explore: Bestandsaufnahme Ziel6/Au… ███░░░░░░░░░  36k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  17,531
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    9%  2,526,907
cache_read     ▕████████████████████████▏   90%  25,400,627
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  256,771
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
Warm (System/Memory/History)  ▕████████████████████▏   90%  25,400,627
Neu gecacht (Tool-Ausgaben)   ▕██░░░░░░░░░░░░░░░░░░▏    9%  2,526,907
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  17,531
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  256,771
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 154 Sessions: 2,946,840,868 Token (29,545 Antworten).

