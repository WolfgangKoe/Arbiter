# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-08 07:51 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-07 18:58 ab9b  ███████████░ 135k ↓    █████░  80% ↓  ▚▚▚······▒▒▒
07-06 17:59 89a0  ████████████ 146k ↑    █████░  90% ↑  ▚▚▚▚▚·······
07-05 19:41 67da  ███████░░░░░  94k ↓    █████░  85% ↑  ▚▚··········
07-05 17:03 121e  ██████████░░ 130k ↓    ████░░  69% ↓  ▚▚▚▚█·······
07-05 13:00 5226  ████████████ 144k ↓    ████░░  74% ↑  ············
07-05 08:37 06c9  ████████████ 205k ↑    ████░░  66% ↓  ············
```

## Jüngste Session

**2026-07-07 18:58 · ab9b709c**

- **Aufgabe:** start next session
- **Modelle:** Haupt Fable · Subagent Fable, Haiku, Sonnet
- **Tokens gesamt:** 52,924,821 (Haupt 10,396,161 · Subagent 42,528,660, Anteil 80 %)
- **Peak-Kontext:** ███████████░ 135k / 150k
- **cache_read:** 48,229,205 · **Output:** 309,178

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ⚠️ Peak-Kontext 135k nahe am 150k-Korridor (>90 %) — geordnet beenden und frisch starten.
- ✅ 80% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 32,442,980 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: Task 6: Rename mo… █████░░░░░░░  66k    ✅
2   general-purpose: rp-Fälle + revive… —                    —
3   general-purpose: Gate-Fixes + S130… █████████░░░ 116k    ✅
4   general-purpose: Task 1: Deny-Bloc… ████████░░░░  94k    ✅
5   general-purpose: Ledger-Check abil… ████░░░░░░░░  50k    ✅
6   general-purpose: Planning-Entwurf … ████████░░░░  96k    ✅
7   general-purpose: Task 4: Battle-Lo… ██████░░░░░░  81k    ✅
8   general-purpose: Task 7+8: Katalog… █████░░░░░░░  63k    ✅
9   general-purpose: rp-Fälle + revive… █████░░░░░░░  66k    ✅
10  general-purpose: Suche opponent-Fa… ███░░░░░░░░░  34k    ✅
11  general-purpose: Task 3: mypy phas… █████░░░░░░░  66k    ✅
12  general-purpose: Task 5: type-stub… ███░░░░░░░░░  34k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  55,510
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    8%  4,330,928
cache_read     ▕████████████████████████▏   91%  48,229,205
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  309,178
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
Warm (System/Memory/History)  ▕████████████████████▏   91%  48,229,205
Neu gecacht (Tool-Ausgaben)   ▕██░░░░░░░░░░░░░░░░░░▏    8%  4,330,928
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  55,510
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  309,178
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 119 Sessions: 2,935,498,733 Token (30,740 Antworten).

