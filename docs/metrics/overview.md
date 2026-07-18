# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-18 20:57 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-18 20:08 00eb  ███████████░ 138k ↑    ████░░  67% ↓  ██··········
07-18 12:29 cd6c  ██████████░░ 122k ↑    ████░░  73% ↓  █···········
07-18 11:00 b53c  █████████░░░ 109k ↓    █████░  85% ↑  ············
07-18 09:08 be5c  ████████████ 162k ↑    █████░  82% ↓  ············
07-17 23:54 b982  █████████░░░ 110k ↓    ██████  95% ↑  ············
07-17 22:16 d275  █████████░░░ 116k ↓    █████░  89% ↑  █···········
```

## Jüngste Session

**2026-07-18 20:08 · 00ebf28c**

- **Aufgabe:** start session. Wir übernehmen Maßnahme 3 aus der Retro. So langsam müssen wir dahin kommen, dass wir UI-Komponenten ver…
- **Modelle:** Haupt Fable · Subagent Opus, Sonnet
- **Tokens gesamt:** 20,951,494 (Haupt 6,982,791 · Subagent 13,968,703, Anteil 67 %)
- **Peak-Kontext:** ███████████░ 138k / 150k
- **cache_read:** 19,065,738 · **Output:** 226,572

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ⚠️ Peak-Kontext 138k nahe am 150k-Korridor (>90 %) — geordnet beenden und frisch starten.
- ✅ 67% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 11,744,192 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: Planner-Tier Opus… ██████░░░░░░  69k    ✅
2   general-purpose: S167 DoD-Review d… ██████░░░░░░  81k    ✅
3   general-purpose: Governance-Edits … ███████░░░░░  92k    ✅
4   general-purpose: Explodes-Mockup V… ████████░░░░  99k    ✅
5   general-purpose: S167-Planning-Ent… ███████████░ 139k    ⚠️
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  534
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    8%  1,658,650
cache_read     ▕████████████████████████▏   91%  19,065,738
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  226,572
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
Warm (System/Memory/History)  ▕████████████████████▏   91%  19,065,738
Neu gecacht (Tool-Ausgaben)   ▕██░░░░░░░░░░░░░░░░░░▏    8%  1,658,650
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  534
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  226,572
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 127 Sessions: 4,116,731,488 Token (47,263 Antworten).

