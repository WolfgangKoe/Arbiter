# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-17 10:17 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-17 08:26 0dfe  ████████████ 150k ↑    █████░  90% ↑  ············
07-17 07:51 d5f8  ██████████░░ 128k ↑    █████░  76% ↑  ·········▒▒▒
07-16 21:15 ae52  ██████░░░░░░  77k ↓    ░░░░░░   0% ↓  ▓▓▓▓▓▓▓▓▓▓▓▓
07-16 20:22 a6af  ████████████ 173k ↑    ████░░  61% ↑  █·········▒▒
07-16 19:40 decf  ██████████░░ 129k ↓    ░░░░░░   6% ↓  ············
07-16 18:03 471e  ████████████ 149k ↑    █████░  86% ↑  ············
```

## Jüngste Session

**2026-07-17 08:26 · 0dfe44e2**

- **Aufgabe:** start session. Bitte standardvorgehensweise einhalten laut operating model. Sobald die Token-Schwellen erreicht sind gl…
- **Modelle:** Haupt Fable · Subagent Opus, Sonnet
- **Tokens gesamt:** 89,019,339 (Haupt 9,129,900 · Subagent 79,889,439, Anteil 90 %)
- **Peak-Kontext:** ████████████ 150k / 150k
- **cache_read:** 84,745,756 · **Output:** 362,850

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ⚠️ 3 von 91 Antworten lagen über dem 150k-Korridor — Session früher schneiden.
- ✅ 90% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 76,857,724 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: S156-DoD-Review (… █████░░░░░░░  66k    ✅
2   general-purpose: B-098 Kombi-Waffe… ██████████░░ 129k    ⚠️
3   general-purpose: S156-Planning-Ent… ███████████░ 135k    ⚠️
4   general-purpose: B-056 Quantum Shi… ████████████ 261k    ⛔
5   general-purpose: S156-Abschluss: A… ████████████ 222k    ⛔
6   general-purpose: S155-DoD-Review (… ████░░░░░░░░  53k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  3,398
cache_creation ▕█░░░░░░░░░░░░░░░░░░░░░░░▏    4%  3,907,335
cache_read     ▕████████████████████████▏   95%  84,745,756
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  362,850
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
Warm (System/Memory/History)  ▕████████████████████▏   95%  84,745,756
Neu gecacht (Tool-Ausgaben)   ▕█░░░░░░░░░░░░░░░░░░░▏    4%  3,907,335
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  3,398
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    0%  362,850
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 118 Sessions: 3,589,476,470 Token (41,524 Antworten).

