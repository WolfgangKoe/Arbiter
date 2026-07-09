# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-09 07:35 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-08 16:31 b31b  ████████████ 166k ↑    ██████  93% ↑  ············
07-08 16:31 cf5b  ████░░░░░░░░  48k ↓    █████░  79% ↓  ············
07-07 18:58 ab9b  ███████████░ 138k ↓    █████░  79% ↓  ▚▚▚······▒▒▒
07-06 17:59 89a0  ████████████ 146k ↑    █████░  90% ↑  ▚▚▚▚▚·······
07-05 19:41 67da  ███████░░░░░  94k ↓    █████░  85% ↑  ▚▚··········
07-05 17:03 121e  ██████████░░ 130k ↓    ████░░  69% ↓  ▚▚▚▚█·······
```

## Jüngste Session

**2026-07-08 16:31 · b31bd07f**

- **Aufgabe:** start session
- **Modelle:** Haupt Fable · Subagent Fable, Opus, Sonnet
- **Tokens gesamt:** 201,663,246 (Haupt 13,814,422 · Subagent 187,848,824, Anteil 93 %)
- **Peak-Kontext:** ████████████ 166k / 150k
- **cache_read:** 192,459,101 · **Output:** 509,869

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ⚠️ 19 von 128 Antworten lagen über dem 150k-Korridor — Session früher schneiden.
- ✅ 93% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 185,118,140 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: Stratagem-Integra… █████████░░░ 113k    ✅
2   general-purpose: Reviewer: DoD-Rev… —                    —
3   general-purpose: Executor: Insane … ████████████ 175k    ⛔
4   general-purpose: Reviewer: DoD-Rev… █████░░░░░░░  60k    ✅
5   general-purpose: Executor: Plan 01… ████████████ 401k    ⛔
6   general-purpose: Executor: Command… ████████████ 244k    ⛔
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  170,720
cache_creation ▕█░░░░░░░░░░░░░░░░░░░░░░░▏    4%  8,523,556
cache_read     ▕████████████████████████▏   95%  192,459,101
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  509,869
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
Warm (System/Memory/History)  ▕████████████████████▏   95%  192,459,101
Neu gecacht (Tool-Ausgaben)   ▕█░░░░░░░░░░░░░░░░░░░▏    4%  8,523,556
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  170,720
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    0%  509,869
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 116 Sessions: 3,064,393,811 Token (31,094 Antworten).

