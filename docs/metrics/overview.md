# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-12 23:28 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-12 22:23 0149  ████████████ 170k ↑    ████░░  63% ↑  ▚▚█·········
07-12 21:20 9271  ████████████ 154k ↑    ░░░░░░   0% ↓  ▓▓▓▓▓▓▓▓▓▓▓▓
07-12 21:20 b358  ████████████ 152k ↑    ████░░  71% ↓  █·········▒▒
07-12 18:02 e7b9  ████████████ 146k ↑    █████░  83% ↑  ▚▚▚·········
07-12 18:02 8ee0  ███░░░░░░░░░  39k ↓    ░░░░░░   0% ↓  ▓▓▓▓▓▓▓▓▓▓▓▓
07-12 11:18 dedb  ████████████ 170k ↑    █████░  76% ↑  ▚▚▚▚········
```

## Jüngste Session

**2026-07-12 22:23 · 01498047**

- **Aufgabe:** starte nächste Session
- **Modelle:** Haupt Fable · Subagent Fable, Opus, Sonnet
- **Tokens gesamt:** 49,763,218 (Haupt 18,477,869 · Subagent 31,285,349, Anteil 63 %)
- **Peak-Kontext:** ████████████ 170k / 150k
- **cache_read:** 46,530,482 · **Output:** 368,545

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ⚠️ 32 von 165 Antworten lagen über dem 150k-Korridor — Session früher schneiden.
- ✅ 63% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 22,476,024 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: Planner: Session-… ███████████░ 142k    ⚠️
2   general-purpose: Executor: Doku-Ma… ██████░░░░░░  70k    ✅
3   general-purpose: Executor: mypy-Ra… █████████░░░ 110k    ✅
4   general-purpose: Reviewer: DoD-Rev… ██████░░░░░░  75k    ✅
5   general-purpose: Recherche: Klan-/… █████████░░░ 114k    ✅
6   general-purpose: Executor: Stratag… █████████░░░ 106k    ✅
7   general-purpose: Reviewer: DoD-Rev… █████░░░░░░░  62k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  35,246
cache_creation ▕█░░░░░░░░░░░░░░░░░░░░░░░▏    6%  2,828,945
cache_read     ▕████████████████████████▏   94%  46,530,482
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  368,545
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
Warm (System/Memory/History)  ▕████████████████████▏   94%  46,530,482
Neu gecacht (Tool-Ausgaben)   ▕█░░░░░░░░░░░░░░░░░░░▏    6%  2,828,945
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  35,246
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  368,545
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 113 Sessions: 3,493,910,054 Token (37,519 Antworten).

