# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-12 19:16 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-12 18:02 e7b9  ███████████░ 138k ↑    █████░  86% ↑  ▚▚▚·········
07-12 18:02 8ee0  ███░░░░░░░░░  39k ↓    ░░░░░░   0% ↓  ▓▓▓▓▓▓▓▓▓▓▓▓
07-12 11:18 dedb  ████████████ 170k ↑    █████░  76% ↑  ▚▚▚▚········
07-12 02:03 76ce  █████████░░░ 119k ↓    ████░░  72% ↓  ▚▚▚█········
07-11 15:28 a4be  ████████████ 150k ↑    █████░  82% ↓  ███·········
07-11 12:58 3d6e  ███████████░ 143k ↓    █████░  89% ↑  ▚▚▚█········
```

## Jüngste Session

**2026-07-12 18:02 · e7b945c1**

- **Aufgabe:** start session
- **Modelle:** Haupt Fable · Subagent Fable, Haiku, Sonnet
- **Tokens gesamt:** 60,609,440 (Haupt 8,784,769 · Subagent 51,824,671, Anteil 86 %)
- **Peak-Kontext:** ███████████░ 138k / 150k
- **cache_read:** 56,021,581 · **Output:** 372,287

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ⚠️ Peak-Kontext 138k nahe am 150k-Korridor (>90 %) — geordnet beenden und frisch starten.
- ✅ 86% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 39,430,851 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: 5 rote Tests anpa… █████░░░░░░░  64k    ✅
2   general-purpose: FixD-Detail-Plan … ███████░░░░░  92k    ✅
3   general-purpose: Rename snake_case… ████████░░░░ 100k    ✅
4   general-purpose: FixD-Sofortlinder… ████████░░░░ 101k    ✅
5   general-purpose: Stratagem-Dispatc… ████████████ 171k    ⛔
6   Explore: Locate render_attack_reso… ███░░░░░░░░░  37k    ✅
7   general-purpose: Planning-Entwurf … ████████████ 150k    ⛔
8   general-purpose: Backlog-Überführu… █████░░░░░░░  66k    ✅
9   general-purpose: FixC Insane Brave… ███████░░░░░  89k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  7,120
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    7%  4,208,452
cache_read     ▕████████████████████████▏   92%  56,021,581
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  372,287
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
Warm (System/Memory/History)  ▕████████████████████▏   92%  56,021,581
Neu gecacht (Tool-Ausgaben)   ▕██░░░░░░░░░░░░░░░░░░▏    7%  4,208,452
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  7,120
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  372,287
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 112 Sessions: 3,434,612,688 Token (36,685 Antworten).

