# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-17 08:22 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-17 07:51 d5f8  █████████░░░ 116k ↑    █████░  80% ↑  ·········▒▒▒
07-16 21:15 ae52  ██████░░░░░░  77k ↓    ░░░░░░   0% ↓  ▓▓▓▓▓▓▓▓▓▓▓▓
07-16 20:22 a6af  ████████████ 173k ↑    ████░░  61% ↑  █·········▒▒
07-16 19:40 decf  ██████████░░ 129k ↓    ░░░░░░   6% ↓  ············
07-16 18:03 471e  ████████████ 149k ↑    █████░  86% ↑  ············
07-16 09:35 de37  ███████████░ 139k ↑    █████░  85% ↓  ▚▚··········
```

## Jüngste Session

**2026-07-17 07:51 · d5f8d64e**

- **Aufgabe:** start session
- **Modelle:** Haupt Fable · Subagent Haiku, Sonnet
- **Tokens gesamt:** 33,089,933 (Haupt 6,648,649 · Subagent 26,441,284, Anteil 80 %)
- **Peak-Kontext:** █████████░░░ 116k / 150k
- **cache_read:** 31,043,805 · **Output:** 271,565

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 116k blieb im 150k-Korridor.
- ✅ 80% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 26,441,284 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: S155 Planning-Ent… ███████░░░░░  86k    ✅
2   general-purpose: Governance-Doku M… ███████████░ 136k    ⚠️
3   general-purpose: Backlog-Pflege un… █████████░░░ 106k    ✅
4   general-purpose: Backlog-Nachzug n… ████████░░░░ 105k    ✅
5   general-purpose: B-027 unit_key du… ██████░░░░░░  76k    ✅
6   general-purpose: B-079 DRY-Helper … ████░░░░░░░░  45k    ✅
7   general-purpose: E1 Counter-Offens… ███████░░░░░  92k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  46,857
cache_creation ▕█░░░░░░░░░░░░░░░░░░░░░░░▏    5%  1,727,706
cache_read     ▕████████████████████████▏   94%  31,043,805
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  271,565
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
Warm (System/Memory/History)  ▕████████████████████▏   94%  31,043,805
Neu gecacht (Tool-Ausgaben)   ▕█░░░░░░░░░░░░░░░░░░░▏    5%  1,727,706
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  46,857
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  271,565
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 117 Sessions: 3,497,851,502 Token (40,785 Antworten).

