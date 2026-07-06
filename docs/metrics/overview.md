# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-06 17:58 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-05 19:41 67da  ███████░░░░░  92k ↓    █████░  86% ↑  ▚▚··········
07-05 17:03 121e  ██████████░░ 130k ↓    ████░░  69% ↓  ▚▚▚▚█·······
07-05 13:00 5226  ████████████ 144k ↓    ████░░  74% ↑  ············
07-05 08:37 06c9  ████████████ 205k ↑    ████░░  66% ↓  ············
07-04 20:21 4f34  ██████████░░ 124k ↓    █████░  85% ↑  ············
07-04 14:45 b13e  ████████████ 147k ↑    ████░░  67% ↓  ▚▚▚█·······▒
```

## Jüngste Session

**2026-07-05 19:41 · 67da766e**

- **Aufgabe:** Du hast die Freigabe für den Plan. Sobald die Subagenten dafür laufen, beauftrage einen weiteren, der prüft, was mit /h…
- **Modelle:** Haupt Fable · Subagent Fable, Haiku, Opus, Sonnet
- **Tokens gesamt:** 24,154,546 (Haupt 3,416,907 · Subagent 20,737,639, Anteil 86 %)
- **Peak-Kontext:** ███████░░░░░ 92k / 150k
- **cache_read:** 21,926,041 · **Output:** 169,036

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 92k blieb im 150k-Korridor.
- ✅ 86% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 16,852,223 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   Explore: r-proto-02 Löschbarkeit p… ██░░░░░░░░░░  26k    ✅
2   general-purpose: Planning-Entwurf … ███████░░░░░  90k    ✅
3   general-purpose: Session-Abschluss… ████░░░░░░░░  53k    ✅
4   general-purpose: S127 DoD-Review d… ███░░░░░░░░░  36k    ✅
5   general-purpose: Plan 038+039 ausf… ████████░░░░  95k    ✅
6   general-purpose: Doku-Paket S127 u… █████░░░░░░░  68k    ✅
7   Explore: Ratchet/Ledger-Trend anal… ████░░░░░░░░  53k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  42,698
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    8%  2,016,771
cache_read     ▕████████████████████████▏   91%  21,926,041
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  169,036
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
Warm (System/Memory/History)  ▕████████████████████▏   91%  21,926,041
Neu gecacht (Tool-Ausgaben)   ▕██░░░░░░░░░░░░░░░░░░▏    8%  2,016,771
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  42,698
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  169,036
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 122 Sessions: 2,839,879,250 Token (29,375 Antworten).

