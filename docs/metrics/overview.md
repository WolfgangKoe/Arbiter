# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-05 18:34 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-05 17:03 121e  ██████░░░░░░  81k ↓    █████░  88% ↑  ▚▚▚▚▚·······
07-05 13:00 5226  ████████████ 144k ↓    ████░░  74% ↑  ············
07-05 08:37 06c9  ████████████ 205k ↑    ████░░  66% ↓  ············
07-04 20:21 4f34  ██████████░░ 124k ↓    █████░  85% ↑  ············
07-04 14:45 b13e  ████████████ 147k ↑    ████░░  67% ↓  ▚▚▚█·······▒
07-04 09:55 f800  ███████████░ 133k ↑    ████░░  67% ↓  ▚▚▚▚▚█······
```

## Jüngste Session

**2026-07-05 17:03 · 121e0a1c**

- **Aufgabe:** start session, bitte Plan vorlegen
- **Modelle:** Haupt Fable, Opus · Subagent Fable, Sonnet
- **Tokens gesamt:** 27,295,706 (Haupt 3,388,884 · Subagent 23,906,822, Anteil 88 %)
- **Peak-Kontext:** ██████░░░░░░ 81k / 150k
- **cache_read:** 25,298,940 · **Output:** 235,191

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 81k blieb im 150k-Korridor.
- ✅ 88% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 13,331,663 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   Plan: Planungsentwurf Session 126   ██████░░░░░░  74k    ✅
2   Explore: UI-Verifikationsanleitung… ██████████░░ 126k    ⚠️
3   general-purpose: Executor Plan 040… ██████████░░ 125k    ⚠️
4   Plan: Mitfix-Design Stratagem-Stage ██████░░░░░░  74k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  70,531
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    6%  1,691,044
cache_read     ▕████████████████████████▏   93%  25,298,940
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  235,191
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
Warm (System/Memory/History)  ▕████████████████████▏   93%  25,298,940
Neu gecacht (Tool-Ausgaben)   ▕█░░░░░░░░░░░░░░░░░░░▏    6%  1,691,044
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  70,531
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  235,191
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 127 Sessions: 2,900,048,787 Token (29,760 Antworten).

