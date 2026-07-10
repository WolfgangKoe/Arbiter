# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-10 16:02 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-10 13:33 b069  ████████████ 149k ↓    █████░  87% ↑  ▚▚▚▚▚·······
07-10 01:56 86c3  ████████████ 163k ↑    █████░  87% ↑  ▚▚··········
07-09 20:34 5769  ████████░░░░ 103k ↓    █████░  81% ↑  ▚··········▒
07-09 20:34 19cb  ████████████ 173k ↓    ██░░░░  38% ↓  ·······▒▒▒▒▒
07-09 17:14 bd4b  ████████████ 173k ↑    ████░░  62% ↓  ▚···········
07-08 16:31 b31b  ████████████ 167k ↑    ██████  93% ↑  ············
```

## Jüngste Session

**2026-07-10 13:33 · b0698466**

- **Aufgabe:** start session
- **Modelle:** Haupt Fable · Subagent Fable, Haiku, Opus, Sonnet
- **Tokens gesamt:** 57,929,252 (Haupt 7,362,726 · Subagent 50,566,526, Anteil 87 %)
- **Peak-Kontext:** ████████████ 149k / 150k
- **cache_read:** 52,033,526 · **Output:** 493,283

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ⚠️ Peak-Kontext 149k nahe am 150k-Korridor (>90 %) — geordnet beenden und frisch starten.
- ✅ 87% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 27,564,248 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: DoD-Review Sessio… █████░░░░░░░  59k    ✅
2   general-purpose: STANDING-Marker i… ████░░░░░░░░  45k    ✅
3   general-purpose: BA-Stratagems aus… ██████░░░░░░  69k    ✅
4   general-purpose: Wahapedia-Lookup … ███░░░░░░░░░  39k    ✅
5   general-purpose: Wahapedia-Live-Ab… █████████░░░ 108k    ✅
6   general-purpose: §6.2 statisches M… ████████████ 149k    ⚠️
7   general-purpose: Planning-Entwurf … ████████████ 206k    ⛔
8   Explore: Verify S134 UI-Befunde ge… █████░░░░░░░  63k    ✅
9   general-purpose: B5-Fix, B1-Recher… █████████░░░ 116k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  208,261
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    9%  5,194,182
cache_read     ▕████████████████████████▏   90%  52,033,526
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  493,283
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
Warm (System/Memory/History)  ▕████████████████████▏   90%  52,033,526
Neu gecacht (Tool-Ausgaben)   ▕██░░░░░░░░░░░░░░░░░░▏    9%  5,194,182
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  208,261
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  493,283
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 113 Sessions: 3,216,547,086 Token (32,568 Antworten).

