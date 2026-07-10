# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-10 13:31 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-10 01:56 86c3  ████████████ 160k ↑    █████░  88% ↑  ▚▚··········
07-09 20:34 5769  ████████░░░░ 103k ↓    █████░  81% ↑  ▚··········▒
07-09 20:34 19cb  ████████████ 173k ↓    ██░░░░  38% ↓  ·······▒▒▒▒▒
07-09 17:14 bd4b  ████████████ 173k ↑    ████░░  62% ↓  ▚···········
07-08 16:31 b31b  ████████████ 167k ↑    ██████  93% ↑  ············
07-08 16:31 cf5b  ████░░░░░░░░  48k ↓    █████░  79% ↓  ············
```

## Jüngste Session

**2026-07-10 01:56 · 86c3e13b**

- **Aufgabe:** start session, bitte App starten
- **Modelle:** Haupt Fable · Subagent Fable, Haiku, Opus, Sonnet
- **Tokens gesamt:** 120,397,552 (Haupt 14,635,569 · Subagent 105,761,983, Anteil 88 %)
- **Peak-Kontext:** ████████████ 160k / 150k
- **cache_read:** 112,023,069 · **Output:** 526,791

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ⚠️ 16 von 148 Antworten lagen über dem 150k-Korridor — Session früher schneiden.
- ✅ 88% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 90,313,874 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: S133 DoD-Review (… █████░░░░░░░  60k    ✅
2   general-purpose: S133-Planungsentw… █████████░░░ 110k    ✅
3   general-purpose: T1: K1/K4-Handoff… █████░░░░░░░  57k    ✅
4   general-purpose: T5: K2 Bewegungsp… ████████████ 188k    ⛔
5   general-purpose: T3: Profilkarte S… ██████░░░░░░  72k    ✅
6   general-purpose: T6: Reaktiv-Box a… ████████████ 221k    ⛔
7   general-purpose: T4: S133-D Desper… ████████████ 218k    ⛔
8   general-purpose: T2: K3 Stratagem-… ██████░░░░░░  79k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  217,224
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    6%  7,630,468
cache_read     ▕████████████████████████▏   93%  112,023,069
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  526,791
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
Warm (System/Memory/History)  ▕████████████████████▏   93%  112,023,069
Neu gecacht (Tool-Ausgaben)   ▕█░░░░░░░░░░░░░░░░░░░▏    6%  7,630,468
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  217,224
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    0%  526,791
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 112 Sessions: 3,156,992,073 Token (31,884 Antworten).

