# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-22 19:08 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-21 19:23 1c15  ███████████░ 139k ↓    █████░  82% ↑  ██··········
07-21 17:57 4c40  ████████████ 158k ↑    ███░░░  51% ↓  █···········
07-20 21:40 813e  ███████████░ 137k ↓    █████░  83% ↑  ██··········
07-20 20:48 f518  ████████████ 174k ↑    ██░░░░  40% ↓  ███·········
07-20 19:44 bc42  ████████████ 155k ↑    ████░░  67% ↓  ███·········
07-19 21:36 e1cb  ██████████░░ 129k ↑    █████░  90% ↑  ··········▒▒
```

## Jüngste Session

**2026-07-21 19:23 · 1c15771b**

- **Aufgabe:** Starte die nächste Session. Die Planung soll ein Opus übernehmen -&gt; In den Regeln des Operating_Models festhalten. -&gt; P…
- **Modelle:** Haupt Opus · Subagent Opus, Sonnet
- **Tokens gesamt:** 33,087,272 (Haupt 6,024,910 · Subagent 27,062,362, Anteil 82 %)
- **Peak-Kontext:** ███████████░ 139k / 150k
- **cache_read:** 29,614,888 · **Output:** 239,407

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ⚠️ Peak-Kontext 139k nahe am 150k-Korridor (>90 %) — geordnet beenden und frisch starten.
- ✅ 82% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 21,963,094 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: T2a Ratchet-Regel… ████████░░░░ 104k    ✅
2   general-purpose: T4-Rest C/D/E      ███░░░░░░░░░  40k    ✅
3   general-purpose: Opus-Planer Gover… ███████████░ 138k    ⚠️
4   general-purpose: T2b Backlog-Chiru… ███████░░░░░  90k    ✅
5   general-purpose: T4 S176-Zusatz Do… █████░░░░░░░  63k    ✅
6   general-purpose: T1 Koordinator-Ti… ████████████ 276k    ⛔
7   general-purpose: T5 Opus-Review Do… ███░░░░░░░░░  44k    ✅
8   general-purpose: T3 Prozess-Regel-… █████░░░░░░░  68k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  648
cache_creation ▕███░░░░░░░░░░░░░░░░░░░░░▏   10%  3,232,329
cache_read     ▕████████████████████████▏   90%  29,614,888
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  239,407
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
Warm (System/Memory/History)  ▕████████████████████▏   90%  29,614,888
Neu gecacht (Tool-Ausgaben)   ▕██░░░░░░░░░░░░░░░░░░▏   10%  3,232,329
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  648
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  239,407
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 100 Sessions: 4,094,567,582 Token (45,462 Antworten).

