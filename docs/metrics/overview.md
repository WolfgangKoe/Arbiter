# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-09 20:32 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-09 17:14 bd4b  ████████████ 167k ↑    ████░░  66% ↓  ▚···········
07-08 16:31 b31b  ████████████ 167k ↑    ██████  93% ↑  ············
07-08 16:31 cf5b  ████░░░░░░░░  48k ↓    █████░  79% ↓  ············
07-07 18:58 ab9b  ███████████░ 138k ↓    █████░  79% ↓  ▚▚▚······▒▒▒
07-06 17:59 89a0  ████████████ 146k ↑    █████░  90% ↑  ▚▚▚▚▚·······
07-05 19:41 67da  ███████░░░░░  94k ↓    █████░  85% ↑  ▚▚··········
```

## Jüngste Session

**2026-07-09 17:14 · bd4b682f**

- **Aufgabe:** start session
- **Modelle:** Haupt Fable · Subagent Fable, Opus, Sonnet
- **Tokens gesamt:** 33,014,916 (Haupt 11,366,422 · Subagent 21,648,494, Anteil 66 %)
- **Peak-Kontext:** ████████████ 167k / 150k
- **cache_read:** 29,653,399 · **Output:** 337,716

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ⚠️ 18 von 115 Antworten lagen über dem 150k-Korridor — Session früher schneiden.
- ✅ 66% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 19,890,599 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: DoD-Review Sessio… ███░░░░░░░░░  41k    ✅
2   general-purpose: GO-Klassifikation… ████████░░░░ 100k    ✅
3   general-purpose: Design-Entscheide… ██████████░░ 124k    ⚠️
4   general-purpose: UI-Ist-Inventar G… ██████████░░ 123k    ⚠️
5   general-purpose: GO-UI-Konzept mit… █████░░░░░░░  69k    ✅
6   general-purpose: S131 neu planen n… ██████░░░░░░  76k    ✅
7   general-purpose: Scroll-Bug nach S… ████░░░░░░░░  56k    ✅
8   general-purpose: Planning-Entwurf … ██████░░░░░░  79k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  171,698
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    9%  2,852,103
cache_read     ▕████████████████████████▏   90%  29,653,399
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  337,716
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
Warm (System/Memory/History)  ▕████████████████████▏   90%  29,653,399
Neu gecacht (Tool-Ausgaben)   ▕██░░░░░░░░░░░░░░░░░░▏    9%  2,852,103
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    1%  171,698
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  337,716
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 116 Sessions: 3,084,045,125 Token (31,379 Antworten).

