# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-16 19:39 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-16 18:03 471e  ████████████ 146k ↑    █████░  86% ↑  ············
07-16 09:35 de37  ███████████░ 139k ↑    █████░  85% ↓  ▚▚··········
07-15 21:58 ad76  ██████████░░ 127k ↑    █████░  91% ↑  ▚▚·········▒
07-15 19:12 9dd1  █████████░░░ 106k ↓    █████░  86% ↑  █··········▒
07-15 19:12 628e  ████████████ 164k ↑    ███░░░  42% ↓  ············
07-15 17:44 ac36  ████████████ 154k ↓    █████░  88% ↑  ▚█··········
```

## Jüngste Session

**2026-07-16 18:03 · 471eb78b**

- **Aufgabe:** start session
- **Modelle:** Haupt Fable · Subagent Opus, Sonnet
- **Tokens gesamt:** 70,912,565 (Haupt 9,615,131 · Subagent 61,297,434, Anteil 86 %)
- **Peak-Kontext:** ████████████ 146k / 150k
- **cache_read:** 65,640,103 · **Output:** 420,473

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ⚠️ Peak-Kontext 146k nahe am 150k-Korridor (>90 %) — geordnet beenden und frisch starten.
- ✅ 86% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 58,892,808 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: Offene UI-Verifik… ████████████ 157k    ⛔
2   general-purpose: B-099b Backlog-Fo… ████████████ 243k    ⛔
3   general-purpose: S152-Review + S15… ██████░░░░░░  69k    ✅
4   general-purpose: S152 Planning-Ent… █████████░░░ 117k    ✅
5   general-purpose: B-099a Backlog St… ██████████░░ 122k    ⚠️
6   general-purpose: markdownlint-Tria… ███░░░░░░░░░  40k    ✅
7   general-purpose: Typ-Farben-Vorsch… █████░░░░░░░  62k    ✅
8   general-purpose: S152-Abschluss + … ██████████░░ 124k    ⚠️
9   general-purpose: B-098 Boss Nob Wa… ████████░░░░  97k    ✅
10  general-purpose: Beobachtungen-Tra… ████████████ 164k    ⛔
11  general-purpose: B-002 K1-Wortlaut… ███████░░░░░  88k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  6,463
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    7%  4,845,526
cache_read     ▕████████████████████████▏   93%  65,640,103
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  420,473
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
Warm (System/Memory/History)  ▕████████████████████▏   93%  65,640,103
Neu gecacht (Tool-Ausgaben)   ▕█░░░░░░░░░░░░░░░░░░░▏    7%  4,845,526
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  6,463
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  420,473
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 116 Sessions: 3,595,295,560 Token (40,462 Antworten).

