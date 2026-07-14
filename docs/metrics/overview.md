# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-14 20:48 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-14 19:48 9c2d  ██████████░░ 131k ↑    █████░  82% ↑  ▚▚▚▚▚█······
07-14 18:43 2574  ██████████░░ 126k ↑    ███░░░  57% ↓  ············
07-14 18:43 a845  █████████░░░ 107k ↓    ████░░  66% ↑  ▚▚▚▚▚▚▚▚▚▚··
07-12 22:23 0149  ████████████ 174k ↑    ████░░  61% ↑  ▚▚█·········
07-12 21:20 9271  ████████████ 154k ↑    ░░░░░░   0% ↓  ▓▓▓▓▓▓▓▓▓▓▓▓
07-12 21:20 b358  ████████████ 152k ↑    ████░░  71% ↓  █·········▒▒
```

## Jüngste Session

**2026-07-14 19:48 · 9c2d7f6b**

- **Aufgabe:** start session und start App, damit ich die UI Verifikation der letzten Session durchführen kann.
- **Modelle:** Haupt Fable · Subagent Fable, Haiku, Opus, Sonnet
- **Tokens gesamt:** 40,266,697 (Haupt 7,143,423 · Subagent 33,123,274, Anteil 82 %)
- **Peak-Kontext:** ██████████░░ 131k / 150k
- **cache_read:** 37,058,054 · **Output:** 270,080

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 131k blieb im 150k-Korridor.
- ✅ 82% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 18,407,765 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: Nihilakh-Klärung … ████░░░░░░░░  50k    ✅
2   general-purpose: S146-Planungsentw… ████████████ 153k    ⛔
3   general-purpose: Executor 1a: on_t… ████████████ 176k    ⛔
4   general-purpose: S146-Review (DoD)… █████░░░░░░░  66k    ✅
5   general-purpose: MWBD-Verknüpfung … ████░░░░░░░░  53k    ✅
6   general-purpose: Executor 1b: Vigi… █████░░░░░░░  62k    ✅
7   general-purpose: Stufe-B-Lifecycle… ██████░░░░░░  73k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  964
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    7%  2,937,599
cache_read     ▕████████████████████████▏   92%  37,058,054
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  270,080
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
Warm (System/Memory/History)  ▕████████████████████▏   92%  37,058,054
Neu gecacht (Tool-Ausgaben)   ▕██░░░░░░░░░░░░░░░░░░▏    7%  2,937,599
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  964
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  270,080
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 110 Sessions: 3,230,780,755 Token (36,703 Antworten).

