# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-18 10:57 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-18 09:08 be5c  ████████████ 158k ↑    █████░  84% ↓  ············
07-17 23:54 b982  █████████░░░ 110k ↓    ██████  95% ↑  ············
07-17 22:16 d275  █████████░░░ 116k ↓    █████░  89% ↑  █···········
07-17 21:32 8096  ███████████░ 143k ↑    █████░  79% ↑  █···········
07-17 19:45 04ab  ███████████░ 140k ↓    ████░░  74% ↑  █···········
07-17 18:44 ffc7  ████████████ 159k ↓    ████░░  67% ↓  ·······▒▒▒▒▒
```

## Jüngste Session

**2026-07-18 09:08 · be5c7ef6**

- **Aufgabe:** start session
- **Modelle:** Haupt Fable · Subagent Haiku, Opus, Sonnet
- **Tokens gesamt:** 53,574,000 (Haupt 8,619,951 · Subagent 44,954,049, Anteil 84 %)
- **Peak-Kontext:** ████████████ 158k / 150k
- **cache_read:** 51,075,581 · **Output:** 299,374

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ⚠️ 7 von 89 Antworten lagen über dem 150k-Korridor — Session früher schneiden.
- ✅ 84% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 43,629,253 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: Task 1a: Vengeanc… █████████░░░ 115k    ✅
2   general-purpose: S165-Abschluss-Re… █████░░░░░░░  62k    ✅
3   general-purpose: Review-Befunde 1+… ███░░░░░░░░░  34k    ✅
4   general-purpose: Task 1b: Vengeanc… ████████████ 188k    ⛔
5   general-purpose: Task 1c: Verifika… ██░░░░░░░░░░  27k    ✅
6   general-purpose: S165-Artefakt-Übe… ██████████░░ 119k    ✅
7   general-purpose: Task 0: Retro-Maß… ████░░░░░░░░  50k    ✅
8   general-purpose: S165-Planning-Ent… ████████████ 151k    ⛔
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  6,330
cache_creation ▕█░░░░░░░░░░░░░░░░░░░░░░░▏    4%  2,192,715
cache_read     ▕████████████████████████▏   95%  51,075,581
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  299,374
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
Warm (System/Memory/History)  ▕████████████████████▏   95%  51,075,581
Neu gecacht (Tool-Ausgaben)   ▕█░░░░░░░░░░░░░░░░░░░▏    4%  2,192,715
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  6,330
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  299,374
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 127 Sessions: 4,114,251,478 Token (46,934 Antworten).

