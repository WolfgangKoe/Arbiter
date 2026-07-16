# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-16 09:31 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-15 21:58 ad76  ██████████░░ 122k ↑    ██████  92% ↑  ▚▚·········▒
07-15 19:12 9dd1  █████████░░░ 106k ↓    █████░  86% ↑  █··········▒
07-15 19:12 628e  ████████████ 164k ↑    ███░░░  42% ↓  ············
07-15 17:44 ac36  ████████████ 154k ↓    █████░  88% ↑  ▚█··········
07-14 20:50 df5b  ████████████ 169k ↑    █████░  78% ↓  █···········
07-14 19:48 9c2d  ███████████░ 133k ↑    █████░  81% ↑  ▚▚▚▚▚█······
```

## Jüngste Session

**2026-07-15 21:58 · ad76aa89**

- **Aufgabe:** start session
- **Modelle:** Haupt Fable · Subagent Fable, Haiku, Opus, Sonnet
- **Tokens gesamt:** 78,937,718 (Haupt 6,330,961 · Subagent 72,606,757, Anteil 92 %)
- **Peak-Kontext:** ██████████░░ 122k / 150k
- **cache_read:** 74,663,458 · **Output:** 409,773

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 122k blieb im 150k-Korridor.
- ✅ 92% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 62,130,437 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: FixD Brief 1 Comp… ████████████ 215k    ⛔
2   general-purpose: S150 DoD-Review    ████████░░░░  94k    ✅
3   general-purpose: Restrukturierungs… ███░░░░░░░░░  35k    ✅
4   general-purpose: S150 Abschluss du… ████████████ 170k    ⛔
5   general-purpose: S150-Planungsentw… █████████░░░ 110k    ✅
6   general-purpose: used-on Render-Pf… ██████░░░░░░  73k    ✅
7   general-purpose: K1 Klan/Dynastie … ███████████░ 138k    ⚠️
8   general-purpose: M8 Backlog-Archiv… ████████████ 172k    ⛔
9   general-purpose: used-on-Fix Insan… █████████░░░ 113k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  2,252
cache_creation ▕█░░░░░░░░░░░░░░░░░░░░░░░▏    5%  3,862,235
cache_read     ▕████████████████████████▏   95%  74,663,458
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  409,773
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
Warm (System/Memory/History)  ▕████████████████████▏   95%  74,663,458
Neu gecacht (Tool-Ausgaben)   ▕█░░░░░░░░░░░░░░░░░░░▏    5%  3,862,235
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  2,252
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  409,773
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 114 Sessions: 3,473,322,947 Token (39,362 Antworten).

