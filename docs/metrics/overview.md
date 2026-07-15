# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-15 17:43 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-14 20:50 df5b  ████████████ 168k ↑    █████░  78% ↓  █···········
07-14 19:48 9c2d  ███████████░ 133k ↑    █████░  81% ↑  ▚▚▚▚▚█······
07-14 18:43 2574  ██████████░░ 126k ↑    ███░░░  57% ↓  ············
07-14 18:43 a845  █████████░░░ 107k ↓    ████░░  66% ↑  ▚▚▚▚▚▚▚▚▚▚··
07-12 22:23 0149  ████████████ 174k ↑    ████░░  61% ↑  ▚▚█·········
07-12 21:20 9271  ████████████ 154k ↑    ░░░░░░   0% ↓  ▓▓▓▓▓▓▓▓▓▓▓▓
```

## Jüngste Session

**2026-07-14 20:50 · df5b3643**

- **Aufgabe:** start next session. Folgende Punkte möchte ich im Blick auf die letzte Session ergänzen. ICh gebe die Retromaßnahmen fr…
- **Modelle:** Haupt Fable · Subagent Fable, Haiku, Opus, Sonnet
- **Tokens gesamt:** 58,374,659 (Haupt 12,730,619 · Subagent 45,644,040, Anteil 78 %)
- **Peak-Kontext:** ████████████ 168k / 150k
- **cache_read:** 53,702,691 · **Output:** 493,274

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ⚠️ 15 von 117 Antworten lagen über dem 150k-Korridor — Session früher schneiden.
- ✅ 78% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 41,397,087 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: S147-DoD-Review (… ████████░░░░ 103k    ✅
2   general-purpose: MWBD-Instanz-Fix … ███████░░░░░  86k    ✅
3   general-purpose: GO-Audit A: Strat… ██████████░░ 131k    ⚠️
4   general-purpose: Roster für B1-Ver… ███░░░░░░░░░  36k    ✅
5   general-purpose: Handoff-Bereinigu… ███████████░ 132k    ⚠️
6   general-purpose: GO-Audit B2: Ork-… ████████████ 150k    ⚠️
7   general-purpose: S147-Planning-Ent… ████████████ 168k    ⛔
8   general-purpose: GO-Audit B1: Necr… ███████████░ 143k    ⚠️
9   general-purpose: B1-Umsetzung Ziel… █████████░░░ 113k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  1,466
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    7%  4,177,228
cache_read     ▕████████████████████████▏   92%  53,702,691
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  493,274
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
Warm (System/Memory/History)  ▕████████████████████▏   92%  53,702,691
Neu gecacht (Tool-Ausgaben)   ▕██░░░░░░░░░░░░░░░░░░▏    7%  4,177,228
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  1,466
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  493,274
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 111 Sessions: 3,289,819,780 Token (37,362 Antworten).

