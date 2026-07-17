# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-17 19:42 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-17 18:44 ffc7  ████████████ 155k ↓    ████░░  69% ↓  ·······▒▒▒▒▒
07-17 15:58 1e74  ████████████ 160k ↓    ████░░  74% ↓  ··········▒▒
07-17 13:27 73bd  ████████████ 160k ↑    █████░  88% ↑  ···········▒
07-17 10:38 6342  ████████████ 160k ↑    █████░  85% ↓  ···········▒
07-17 08:26 0dfe  ████████████ 155k ↑    █████░  89% ↑  ············
07-17 07:51 d5f8  ██████████░░ 128k ↑    █████░  76% ↑  ·········▒▒▒
```

## Jüngste Session

**2026-07-17 18:44 · ffc7c981**

- **Aufgabe:** start session
- **Modelle:** Haupt Fable · Subagent Haiku, Opus, Sonnet
- **Tokens gesamt:** 30,596,206 (Haupt 9,356,778 · Subagent 21,239,428, Anteil 69 %)
- **Peak-Kontext:** ████████████ 155k / 150k
- **cache_read:** 27,853,357 · **Output:** 240,758

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ⚠️ 1 von 90 Antworten lagen über dem 150k-Korridor — Session früher schneiden.
- ✅ 69% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 20,240,208 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: S160 Backlog-Absc… █████████░░░ 113k    ✅
2   general-purpose: S160 Planning-Ent… ████████░░░░  99k    ✅
3   general-purpose: B-104 Würfel-SVG … ███████████░ 142k    ⚠️
4   general-purpose: S160 DoD-Review (… ████░░░░░░░░  56k    ✅
5   general-purpose: M1/M2-Klauseln + … █████░░░░░░░  68k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  1,270
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    8%  2,500,821
cache_read     ▕████████████████████████▏   91%  27,853,357
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  240,758
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
Warm (System/Memory/History)  ▕████████████████████▏   91%  27,853,357
Neu gecacht (Tool-Ausgaben)   ▕██░░░░░░░░░░░░░░░░░░▏    8%  2,500,821
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  1,270
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  240,758
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 122 Sessions: 3,824,524,529 Token (43,888 Antworten).

