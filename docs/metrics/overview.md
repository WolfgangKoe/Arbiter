# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-20 20:46 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-20 19:44 bc42  ████████████ 149k ↑    ████░░  70% ↓  ███·········
07-19 21:36 e1cb  ██████████░░ 129k ↑    █████░  90% ↑  ··········▒▒
07-19 16:41 4f3a  ██████████░░ 122k ↓    █████░  84% ↑  █··········▒
07-19 13:44 3636  ████████████ 182k ↑    █████░  82% ↓  ··········▒▒
07-18 22:58 067a  ███████████░ 133k ↑    ██████  94% ↑  ············
07-18 20:59 6cfc  ██████████░░ 126k ↓    █████░  83% ↑  █···········
```

## Jüngste Session

**2026-07-20 19:44 · bc427e5a**

- **Aufgabe:** Fable ist vermutlich nicht mehr erreichbar. Starte Session wir übernehmen Retromaßnahme 3
- **Modelle:** Haupt Opus, Sonnet · Subagent Opus, Sonnet
- **Tokens gesamt:** 35,735,835 (Haupt 10,841,437 · Subagent 24,894,398, Anteil 70 %)
- **Peak-Kontext:** ████████████ 149k / 150k
- **cache_read:** 32,834,354 · **Output:** 287,742

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ⚠️ Peak-Kontext 149k nahe am 150k-Korridor (>90 %) — geordnet beenden und frisch starten.
- ✅ 70% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 19,345,161 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: Brief 2: Careen! … ████████████ 166k    ⛔
2   general-purpose: S173 Planning-Ent… ████████████ 145k    ⚠️
3   general-purpose: Brief 1: B-125 + … ████████░░░░  94k    ✅
4   general-purpose: S173 Abschluss-Re… █████░░░░░░░  66k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  774
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    7%  2,612,965
cache_read     ▕████████████████████████▏   92%  32,834,354
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  287,742
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
Warm (System/Memory/History)  ▕████████████████████▏   92%  32,834,354
Neu gecacht (Tool-Ausgaben)   ▕██░░░░░░░░░░░░░░░░░░▏    7%  2,612,965
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  774
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  287,742
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 114 Sessions: 4,285,386,834 Token (47,861 Antworten).

