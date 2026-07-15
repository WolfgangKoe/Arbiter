# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-15 19:08 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-15 17:44 ac36  ████████████ 153k ↓    █████░  89% ↑  ▚█··········
07-14 20:50 df5b  ████████████ 169k ↑    █████░  78% ↓  █···········
07-14 19:48 9c2d  ███████████░ 133k ↑    █████░  81% ↑  ▚▚▚▚▚█······
07-14 18:43 2574  ██████████░░ 126k ↑    ███░░░  57% ↓  ············
07-14 18:43 a845  █████████░░░ 107k ↓    ████░░  66% ↑  ▚▚▚▚▚▚▚▚▚▚··
07-12 22:23 0149  ████████████ 174k ↑    ████░░  61% ↑  ▚▚█·········
```

## Jüngste Session

**2026-07-15 17:44 · ac36a79b**

- **Aufgabe:** start session, die UI-Verifikation bitte als Datei in Handoff ablegen und parallel die App starten.
- **Modelle:** Haupt Fable · Subagent Fable, Opus, Sonnet
- **Tokens gesamt:** 81,726,637 (Haupt 9,008,918 · Subagent 72,717,719, Anteil 89 %)
- **Peak-Kontext:** ████████████ 153k / 150k
- **cache_read:** 76,722,690 · **Output:** 467,180

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ⚠️ 3 von 92 Antworten lagen über dem 150k-Korridor — Session früher schneiden.
- ✅ 89% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 62,653,964 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: Brief 7: camelCas… ███████████░ 138k    ⚠️
2   general-purpose: Brief 1: Apply-Bu… █████████░░░ 115k    ✅
3   Explore: Find Unit dataclass and k… ███░░░░░░░░░  36k    ✅
4   general-purpose: UI-Verifikations-… ████████████ 145k    ⚠️
5   general-purpose: Brief 3: Fire-Ove… ███████████░ 139k    ⚠️
6   general-purpose: S148 Planning-Ent… ████████████ 181k    ⛔
7   general-purpose: S148 Abschluss-Pa… ████████████ 163k    ⛔
8   general-purpose: Brief 2: CP-Fress… ███████░░░░░  91k    ✅
9   Explore: Poll research subagent fo… █░░░░░░░░░░░  12k    ✅
10  general-purpose: Brief 4: grantsKe… ████████████ 160k    ⛔
11  general-purpose: S148 Review (DoD)  █████░░░░░░░  67k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  24,591
cache_creation ▕█░░░░░░░░░░░░░░░░░░░░░░░▏    6%  4,512,176
cache_read     ▕████████████████████████▏   94%  76,722,690
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  467,180
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
Warm (System/Memory/History)  ▕████████████████████▏   94%  76,722,690
Neu gecacht (Tool-Ausgaben)   ▕█░░░░░░░░░░░░░░░░░░░▏    6%  4,512,176
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  24,591
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  467,180
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 112 Sessions: 3,371,886,965 Token (38,195 Antworten).

