# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-22 20:28 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-22 19:15 dbc6  ████████████ 160k ↑    ████░░  75% ↓  █···········
07-21 19:23 1c15  ████████████ 152k ↓    █████░  80% ↑  ██··········
07-21 17:57 4c40  ████████████ 158k ↑    ███░░░  51% ↓  █···········
07-20 21:40 813e  ███████████░ 137k ↓    █████░  83% ↑  ██··········
07-20 20:48 f518  ████████████ 174k ↑    ██░░░░  40% ↓  ███·········
07-20 19:44 bc42  ████████████ 155k ↑    ████░░  67% ↓  ███·········
```

## Jüngste Session

**2026-07-22 19:15 · dbc68e6a**

- **Aufgabe:** start session. Was steht als nächstes im Backlog. Bereite den konkreten Plan für diese Session vor. Achte bitte darauf,…
- **Modelle:** Haupt Opus · Subagent Opus, Sonnet
- **Tokens gesamt:** 44,375,168 (Haupt 11,173,330 · Subagent 33,201,838, Anteil 75 %)
- **Peak-Kontext:** ████████████ 160k / 150k
- **cache_read:** 42,658,323 · **Output:** 273,380

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ⚠️ 11 von 106 Antworten lagen über dem 150k-Korridor — Session früher schneiden.
- ✅ 75% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 31,482,773 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: S178 Abschluss-Re… █████░░░░░░░  65k    ✅
2   general-purpose: B-113 Brief A: Re… ████████████ 147k    ⚠️
3   general-purpose: B-113 Brief B: Lo… ███████████░ 138k    ⚠️
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  881
cache_creation ▕█░░░░░░░░░░░░░░░░░░░░░░░▏    3%  1,442,584
cache_read     ▕████████████████████████▏   96%  42,658,323
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  273,380
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
Warm (System/Memory/History)  ▕████████████████████▏   96%  42,658,323
Neu gecacht (Tool-Ausgaben)   ▕█░░░░░░░░░░░░░░░░░░░▏    3%  1,442,584
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  881
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  273,380
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 101 Sessions: 4,141,234,710 Token (45,949 Antworten).

