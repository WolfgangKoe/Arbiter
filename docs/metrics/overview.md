# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-06-30 20:51 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
06-30 18:46 fce6  ██████████░░ 126k ↓    █████░  79% ↑  ███········▒
06-29 20:55 c673  ████████████ 162k ↑    ████░░  74% ↑  █··········▒
06-28 20:02 1b3d  ███████████░ 135k ↓    ████░░  73% ↑  ···········▒
06-28 18:27 5ed6  ████████████ 153k ↑    ████░░  64% ↓  █···········
06-27 14:42 5af7  ██████░░░░░░  80k ↓    █████░  78% ↑  ███·········
06-27 12:39 9ef7  ███████████░ 137k ↑    ████░░  68% ↑  ██·······▒▒▒
```

## Jüngste Session

**2026-06-30 18:46 · fce6bdee**

- **Aufgabe:** start session. Prüfe nextsession und starte einen Planungs-Subagenten
- **Modelle:** Haupt Opus · Subagent Haiku, Opus, Sonnet
- **Tokens gesamt:** 31,686,348 (Haupt 6,785,526 · Subagent 24,900,822, Anteil 79 %)
- **Peak-Kontext:** ██████████░░ 126k / 150k
- **cache_read:** 29,715,760 · **Output:** 201,795

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 126k blieb im 150k-Korridor.
- ✅ 79% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 18,759,134 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   Plan: Planungs-Entwurf S112         █████░░░░░░░  60k    ✅
2   general-purpose: Ziel-Renumbering … ████░░░░░░░░  49k    ✅
3   general-purpose: Doku-Drift 92 auf… ███░░░░░░░░░  40k    ✅
4   general-purpose: Plan 031 Executor  ██████████░░ 119k    ✅
5   general-purpose: Ziel6 konsolidier… ██████████░░ 119k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  17,481
cache_creation ▕█░░░░░░░░░░░░░░░░░░░░░░░▏    6%  1,751,312
cache_read     ▕████████████████████████▏   94%  29,715,760
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  201,795
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
Warm (System/Memory/History)  ▕████████████████████▏   94%  29,715,760
Neu gecacht (Tool-Ausgaben)   ▕█░░░░░░░░░░░░░░░░░░░▏    6%  1,751,312
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  17,481
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  201,795
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 150 Sessions: 2,942,559,916 Token (29,447 Antworten).

