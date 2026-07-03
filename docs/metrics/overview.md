# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-03 19:26 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-02 20:35 aa33  ██████████░░ 131k ↓    ██░░░░  38% ↓  ▚▚▚▚▚██·····
07-01 21:41 bf59  ████████████ 144k ↑    ████░░  69% ↓  ▚▚▚█········
07-01 20:29 49a0  ████████████ 144k ↑    ████░░  74% ↑  ███████··▒▒▒
07-01 18:47 b870  ███░░░░░░░░░  32k ↓    ░░░░░░   0% ↓  ▓▓▓▓▓▓▓▓▓▓▓▓
06-30 23:20 9fe6  ██████████░░ 122k ↓    ███░░░  57% ↓  █·········▒▒
06-30 22:03 8996  ███████████░ 140k ↑    ████░░  72% ↑  ············
```

## Jüngste Session

**2026-07-02 20:35 · aa337077**

- **Aufgabe:** Start session. Lass den Plan von einem Subagenten vorlegen
- **Modelle:** Haupt Fable · Subagent Fable, Haiku, Opus, Sonnet
- **Tokens gesamt:** 19,664,561 (Haupt 12,139,391 · Subagent 7,525,170, Anteil 38 %)
- **Peak-Kontext:** ██████████░░ 131k / 150k
- **cache_read:** 17,221,309 · **Output:** 244,611

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 131k blieb im 150k-Korridor.
- ✅ 38% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 3,117,942 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: DRY-Helper ±1-Cap… █████░░░░░░░  60k    ✅
2   general-purpose: Planning-Entwurf … ███████░░░░░  89k    ✅
3   general-purpose: context-audit-S91… ██████░░░░░░  73k    ✅
4   general-purpose: DoD-Review S118 d… ████░░░░░░░░  53k    ✅
5   general-purpose: Streamlit-Mock-Fi… █████░░░░░░░  61k    ✅
6   general-purpose: UI-Pass-Checklist… ███░░░░░░░░░  36k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  138,884
cache_creation ▕███░░░░░░░░░░░░░░░░░░░░░▏   10%  2,059,757
cache_read     ▕████████████████████████▏   88%  17,221,309
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  244,611
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
Warm (System/Memory/History)  ▕████████████████████▏   88%  17,221,309
Neu gecacht (Tool-Ausgaben)   ▕██░░░░░░░░░░░░░░░░░░▏   10%  2,059,757
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    1%  138,884
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  244,611
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 135 Sessions: 2,794,709,679 Token (28,181 Antworten).

