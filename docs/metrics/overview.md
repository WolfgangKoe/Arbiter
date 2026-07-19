# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-19 13:32 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-18 22:58 067a  ██████████░░ 128k ↑    ██████  95% ↑  ············
07-18 20:59 6cfc  ██████████░░ 126k ↓    █████░  83% ↑  █···········
07-18 20:08 00eb  ███████████░ 140k ↑    ████░░  64% ↓  ██··········
07-18 12:29 cd6c  ██████████░░ 122k ↑    ████░░  73% ↓  █···········
07-18 11:00 b53c  █████████░░░ 109k ↓    █████░  85% ↑  ············
07-18 09:08 be5c  ████████████ 162k ↑    █████░  82% ↓  ············
```

## Jüngste Session

**2026-07-18 22:58 · 067a868c**

- **Aufgabe:** Ich habe einige Kommentare ins Planning-Dokument geschrieben. Ich gebe den PLan soweit frei. Sorge dafür, dass die Suba…
- **Modelle:** Haupt Fable · Subagent Haiku, Opus, Sonnet
- **Tokens gesamt:** 145,483,538 (Haupt 7,537,618 · Subagent 137,945,920, Anteil 95 %)
- **Peak-Kontext:** ██████████░░ 128k / 150k
- **cache_read:** 139,424,922 · **Output:** 467,802

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 128k blieb im 150k-Korridor.
- ✅ 95% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 132,912,358 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: T2: Spec-Umbau de… ████████████ 219k    ⛔
2   general-purpose: T3: b1 Explode-Sc… ████████████ 286k    ⛔
3   general-purpose: S169-Planning-Ent… ███████████░ 139k    ⚠️
4   general-purpose: T6: Handoff-Aufrä… ██░░░░░░░░░░  29k    ✅
5   general-purpose: Review-Pflicht-Ko… ███░░░░░░░░░  36k    ✅
6   general-purpose: S169-Abschluss-Re… ██████░░░░░░  74k    ✅
7   general-purpose: T4: b2 Pflicht-Tr… ████████████ 324k    ⛔
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  2,016
cache_creation ▕█░░░░░░░░░░░░░░░░░░░░░░░▏    4%  5,588,798
cache_read     ▕████████████████████████▏   96%  139,424,922
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  467,802
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
Warm (System/Memory/History)  ▕████████████████████▏   96%  139,424,922
Neu gecacht (Tool-Ausgaben)   ▕█░░░░░░░░░░░░░░░░░░░▏    4%  5,588,798
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  2,016
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    0%  467,802
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 125 Sessions: 4,263,309,896 Token (48,130 Antworten).

