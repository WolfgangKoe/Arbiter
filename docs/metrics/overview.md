# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-24 13:11 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-24 08:26 0b11  ████████████ 148k ↑    ██████  92% ↑  █···········
07-23 21:51 6eae  ███████████░ 131k ↓    ████░░  75% ↑  ██··········
07-23 17:56 33e4  ████████████ 153k ↑    ████░░  65% ↓  ██········▒▒
07-23 17:16 fe07  ████████░░░░ 100k ↓    █████░  79% ↑  █·····▒▒▒▒▒▒
07-23 16:34 695b  ██████████░░ 128k ↓    ████░░  63% ↑  ███▒▒▒▒▒▒▒▒▒
07-22 20:41 2123  ████████████ 224k ↑    ███░░░  56% ↓  ············
```

## Jüngste Session

**2026-07-24 08:26 · 0b113c5c**

- **Aufgabe:** start session S183
- **Modelle:** Haupt Fable · Subagent Haiku, Opus, Sonnet
- **Tokens gesamt:** 130,630,950 (Haupt 10,487,179 · Subagent 120,143,771, Anteil 92 %)
- **Peak-Kontext:** ████████████ 148k / 150k
- **cache_read:** 126,764,463 · **Output:** 405,225

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ⚠️ Peak-Kontext 148k nahe am 150k-Korridor (>90 %) — geordnet beenden und frisch starten.
- ✅ 92% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 115,273,181 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: T1 Backlog-Überfü… ██████░░░░░░  76k    ✅
2   general-purpose: Playwright UI-Ver… ████████████ 190k    ⛔
3   general-purpose: T2 B-134-Fix + M2… ████████████ 337k    ⛔
4   general-purpose: T2-Finisher: Gate… ████████████ 225k    ⛔
5   general-purpose: S183 Review (DoD,… █████░░░░░░░  66k    ✅
6   general-purpose: S183 Planning-Ent… █████████░░░ 114k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  1,951
cache_creation ▕█░░░░░░░░░░░░░░░░░░░░░░░▏    3%  3,459,311
cache_read     ▕████████████████████████▏   97%  126,764,463
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  405,225
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
Warm (System/Memory/History)  ▕████████████████████▏   97%  126,764,463
Neu gecacht (Tool-Ausgaben)   ▕█░░░░░░░░░░░░░░░░░░░▏    3%  3,459,311
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  1,951
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    0%  405,225
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 106 Sessions: 4,397,642,249 Token (48,455 Antworten).

