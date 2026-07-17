# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-17 18:14 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-17 15:58 1e74  ████████████ 157k ↓    █████░  76% ↓  ··········▒▒
07-17 13:27 73bd  ████████████ 160k ↑    █████░  88% ↑  ···········▒
07-17 10:38 6342  ████████████ 160k ↑    █████░  85% ↓  ···········▒
07-17 08:26 0dfe  ████████████ 155k ↑    █████░  89% ↑  ············
07-17 07:51 d5f8  ██████████░░ 128k ↑    █████░  76% ↑  ·········▒▒▒
07-16 21:15 ae52  ██████░░░░░░  77k ↓    ░░░░░░   0% ↓  ▓▓▓▓▓▓▓▓▓▓▓▓
```

## Jüngste Session

**2026-07-17 15:58 · 1e7402bb**

- **Aufgabe:** go
- **Modelle:** Haupt Fable · Subagent Haiku, Opus, Sonnet
- **Tokens gesamt:** 48,320,236 (Haupt 11,589,528 · Subagent 36,730,708, Anteil 76 %)
- **Peak-Kontext:** ████████████ 157k / 150k
- **cache_read:** 44,134,368 · **Output:** 310,369

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ⚠️ 4 von 110 Antworten lagen über dem 150k-Korridor — Session früher schneiden.
- ✅ 76% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 35,795,564 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: Task 6: B-028b No… ████████████ 161k    ⛔
2   general-purpose: S159-Review (DoD,… █████░░░░░░░  60k    ✅
3   general-purpose: Task 1: Würfelsym… ███████████░ 143k    ⚠️
4   general-purpose: Task 5: mypy-Base… ████░░░░░░░░  51k    ✅
5   general-purpose: S159-Abschluss: A… ███████████░ 135k    ⚠️
6   general-purpose: S159-Planungsentw… ███████████░ 142k    ⚠️
7   general-purpose: Haiku-Scan: fehle… █████░░░░░░░  59k    ✅
8   general-purpose: Katalog-Tabellen … ██████░░░░░░  71k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  2,945
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    8%  3,872,554
cache_read     ▕████████████████████████▏   91%  44,134,368
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  310,369
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
Warm (System/Memory/History)  ▕████████████████████▏   91%  44,134,368
Neu gecacht (Tool-Ausgaben)   ▕██░░░░░░░░░░░░░░░░░░▏    8%  3,872,554
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  2,945
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  310,369
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 121 Sessions: 3,792,107,213 Token (43,548 Antworten).

