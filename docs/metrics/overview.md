# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-17 15:45 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-17 13:27 73bd  ████████████ 157k ↓    █████░  88% ↑  ···········▒
07-17 10:38 6342  ████████████ 160k ↑    █████░  85% ↓  ···········▒
07-17 08:26 0dfe  ████████████ 155k ↑    █████░  89% ↑  ············
07-17 07:51 d5f8  ██████████░░ 128k ↑    █████░  76% ↑  ·········▒▒▒
07-16 21:15 ae52  ██████░░░░░░  77k ↓    ░░░░░░   0% ↓  ▓▓▓▓▓▓▓▓▓▓▓▓
07-16 20:22 a6af  ████████████ 173k ↑    ████░░  61% ↑  █·········▒▒
```

## Jüngste Session

**2026-07-17 13:27 · 73bdc555**

- **Aufgabe:** start session
- **Modelle:** Haupt Fable · Subagent Haiku, Opus, Sonnet
- **Tokens gesamt:** 79,662,475 (Haupt 9,319,799 · Subagent 70,342,676, Anteil 88 %)
- **Peak-Kontext:** ████████████ 157k / 150k
- **cache_read:** 74,764,958 · **Output:** 409,440

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ⚠️ 4 von 92 Antworten lagen über dem 150k-Korridor — Session früher schneiden.
- ✅ 88% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 69,406,745 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: S158-Abschluss-Re… ████░░░░░░░░  48k    ✅
2   general-purpose: S158-Abschluss-Ar… ███████████░ 143k    ⚠️
3   general-purpose: Backlog-Umbau B-0… █████████░░░ 115k    ✅
4   general-purpose: S158 Planning-Ent… ████████░░░░ 101k    ✅
5   general-purpose: Design-Crew B-104… ██████████░░ 119k    ✅
6   general-purpose: B-028a Reactive-A… ████████████ 271k    ⛔
7   general-purpose: B-111 Badge-Toolt… ███████░░░░░  89k    ✅
8   general-purpose: B-104 Würfelsymbo… ████████░░░░  98k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  1,968
cache_creation ▕█░░░░░░░░░░░░░░░░░░░░░░░▏    6%  4,486,109
cache_read     ▕████████████████████████▏   94%  74,764,958
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  409,440
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
Warm (System/Memory/History)  ▕████████████████████▏   94%  74,764,958
Neu gecacht (Tool-Ausgaben)   ▕█░░░░░░░░░░░░░░░░░░░▏    6%  4,486,109
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  1,968
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  409,440
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 120 Sessions: 3,742,402,108 Token (42,999 Antworten).

