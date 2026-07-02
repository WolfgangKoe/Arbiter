# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-02 20:34 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-01 21:41 bf59  ███████████░ 143k ↓    ████░░  70% ↓  ▚▚▚█········
07-01 20:29 49a0  ████████████ 144k ↑    ████░░  74% ↑  ███████··▒▒▒
07-01 18:47 b870  ███░░░░░░░░░  32k ↓    ░░░░░░   0% ↓  ▓▓▓▓▓▓▓▓▓▓▓▓
06-30 23:20 9fe6  ██████████░░ 122k ↓    ███░░░  57% ↓  █·········▒▒
06-30 22:03 8996  ███████████░ 140k ↑    ████░░  72% ↑  ············
06-30 20:54 ac89  █████████░░░ 108k ↓    ████░░  62% ↓  ██····▒▒▒▒▒▒
```

## Jüngste Session

**2026-07-01 21:41 · bf595349**

- **Aufgabe:** Bereite die nächste Session vor. Committen.
- **Modelle:** Haupt Fable, Opus · Subagent Fable, Opus, Sonnet
- **Tokens gesamt:** 45,022,300 (Haupt 13,416,453 · Subagent 31,605,847, Anteil 70 %)
- **Peak-Kontext:** ███████████░ 143k / 150k
- **cache_read:** 41,070,655 · **Output:** 259,371

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ⚠️ Peak-Kontext 143k nahe am 150k-Korridor (>90 %) — geordnet beenden und frisch starten.
- ✅ 70% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 22,283,044 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: Plan design-syste… █████░░░░░░░  60k    ✅
2   general-purpose: Fable ins Token-R… ████████████ 280k    ⛔
3   general-purpose: DoD-Review S116 u… ████░░░░░░░░  53k    ✅
4   general-purpose: Execute DS-2 glyp… ████████░░░░  96k    ✅
5   general-purpose: DoD-Review S117 v… ███░░░░░░░░░  41k    ✅
6   general-purpose: Plan P18 declarat… ████░░░░░░░░  55k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  131,178
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    8%  3,561,096
cache_read     ▕████████████████████████▏   91%  41,070,655
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  259,371
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
Warm (System/Memory/History)  ▕████████████████████▏   91%  41,070,655
Neu gecacht (Tool-Ausgaben)   ▕██░░░░░░░░░░░░░░░░░░▏    8%  3,561,096
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  131,178
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  259,371
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 148 Sessions: 2,978,295,874 Token (30,256 Antworten).

