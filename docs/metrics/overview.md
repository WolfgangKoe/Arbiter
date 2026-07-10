# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-10 21:00 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-10 16:04 54b0  ██████████░░ 131k ↓    ██████  92% ↑  ▚···········
07-10 13:33 b069  ████████████ 152k ↓    █████░  87% ↓  ▚▚▚▚▚·······
07-10 01:56 86c3  ████████████ 163k ↑    █████░  87% ↑  ▚▚··········
07-09 20:34 5769  ████████░░░░ 103k ↓    █████░  81% ↑  ▚··········▒
07-09 20:34 19cb  ████████████ 173k ↓    ██░░░░  38% ↓  ·······▒▒▒▒▒
07-09 17:14 bd4b  ████████████ 173k ↑    ████░░  62% ↓  ▚···········
```

## Jüngste Session

**2026-07-10 16:04 · 54b0c4dc**

- **Aufgabe:** start session
- **Modelle:** Haupt Fable · Subagent Fable, Sonnet
- **Tokens gesamt:** 103,387,995 (Haupt 7,832,446 · Subagent 95,555,549, Anteil 92 %)
- **Peak-Kontext:** ██████████░░ 131k / 150k
- **cache_read:** 98,310,289 · **Output:** 433,682

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 131k blieb im 150k-Korridor.
- ✅ 92% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 90,974,957 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: B6 Kurz-Mockup er… ██████░░░░░░  77k    ✅
2   general-purpose: Paket 4c: Attacke… ████████████ 177k    ⛔
3   general-purpose: Paket 4b: Save-/D… ████████████ 205k    ⛔
4   general-purpose: Paket 4a: Hit-/Wo… ████████████ 222k    ⛔
5   general-purpose: S135 Planning-Ent… ███████░░░░░  93k    ✅
6   general-purpose: Aufgabe 1: Entsch… ███████░░░░░  85k    ✅
7   general-purpose: B6-Fix + B1-Probe… ██████████░░ 120k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  166,692
cache_creation ▕█░░░░░░░░░░░░░░░░░░░░░░░▏    4%  4,477,332
cache_read     ▕████████████████████████▏   95%  98,310,289
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  433,682
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
Warm (System/Memory/History)  ▕████████████████████▏   95%  98,310,289
Neu gecacht (Tool-Ausgaben)   ▕█░░░░░░░░░░░░░░░░░░░▏    4%  4,477,332
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  166,692
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    0%  433,682
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 114 Sessions: 3,321,163,767 Token (33,458 Antworten).

