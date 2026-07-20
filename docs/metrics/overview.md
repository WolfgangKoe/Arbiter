# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-20 22:47 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-20 21:40 813e  ███████████░ 136k ↓    █████░  83% ↑  ██··········
07-20 20:48 f518  ████████████ 174k ↑    ██░░░░  40% ↓  ███·········
07-20 19:44 bc42  ████████████ 155k ↑    ████░░  67% ↓  ███·········
07-19 21:36 e1cb  ██████████░░ 129k ↑    █████░  90% ↑  ··········▒▒
07-19 16:41 4f3a  ██████████░░ 122k ↓    █████░  84% ↑  █··········▒
07-19 13:44 3636  ████████████ 182k ↑    █████░  82% ↓  ··········▒▒
```

## Jüngste Session

**2026-07-20 21:40 · 813e8468**

- **Aufgabe:** start Session. Achte darauf, die Umsetzung der items im Backlog einzuplanen-
- **Modelle:** Haupt Opus · Subagent Opus, Sonnet
- **Tokens gesamt:** 36,420,108 (Haupt 6,147,014 · Subagent 30,273,094, Anteil 83 %)
- **Peak-Kontext:** ███████████░ 136k / 150k
- **cache_read:** 32,880,324 · **Output:** 215,987

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ⚠️ Peak-Kontext 136k nahe am 150k-Korridor (>90 %) — geordnet beenden und frisch starten.
- ✅ 83% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 25,247,316 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: S175 Abschluss: A… ████████████ 176k    ⛔
2   general-purpose: B-028c2 reroll_rp… ███████████░ 136k    ⚠️
3   general-purpose: S175 Review gegen… █████░░░░░░░  63k    ✅
4   Plan: S175 Planning-Entwurf erstel… ████████░░░░ 104k    ✅
5   general-purpose: B-121 + B-110 XS-… █████░░░░░░░  67k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  39,345
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    9%  3,284,452
cache_read     ▕████████████████████████▏   90%  32,880,324
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  215,987
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
Warm (System/Memory/History)  ▕████████████████████▏   90%  32,880,324
Neu gecacht (Tool-Ausgaben)   ▕██░░░░░░░░░░░░░░░░░░▏    9%  3,284,452
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  39,345
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  215,987
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 116 Sessions: 4,338,808,121 Token (48,497 Antworten).

