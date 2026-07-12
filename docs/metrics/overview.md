# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-12 11:15 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-12 02:03 76ce  █████████░░░ 117k ↓    ████░░  75% ↓  ▚▚▚█········
07-11 15:28 a4be  ████████████ 150k ↑    █████░  82% ↓  ███·········
07-11 12:58 3d6e  ███████████░ 143k ↓    █████░  89% ↑  ▚▚▚█········
07-11 10:04 8553  ████████████ 178k ↑    ████░░  65% ↓  ▚▚▚▚▚▚▚▚····
07-10 21:31 e914  ███████████░ 134k ↓    █████░  89% ↑  ▚▚▚·········
07-10 16:04 54b0  ████████████ 197k ↑    █████░  83% ↓  ▚···········
```

## Jüngste Session

**2026-07-12 02:03 · 76ce5f18**

- **Aufgabe:** start sessino
- **Modelle:** Haupt Fable, Opus · Subagent Fable, Opus, Sonnet
- **Tokens gesamt:** 23,545,016 (Haupt 5,867,007 · Subagent 17,678,009, Anteil 75 %)
- **Peak-Kontext:** █████████░░░ 117k / 150k
- **cache_read:** 21,562,650 · **Output:** 192,058

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 117k blieb im 150k-Korridor.
- ✅ 75% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 12,009,165 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: S140 Welle 1 Engi… ██████░░░░░░  81k    ✅
2   Plan: S140 Planning-Entwurf erstel… ████████░░░░ 102k    ✅
3   general-purpose: S140 Welle 3 mypy… ██████░░░░░░  70k    ✅
4   general-purpose: S140 Welle 2 UI+D… ███████░░░░░  88k    ✅
5   general-purpose: S140 DoD-Review (… ██████░░░░░░  75k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  705
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    8%  1,789,603
cache_read     ▕████████████████████████▏   92%  21,562,650
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  192,058
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
Warm (System/Memory/History)  ▕████████████████████▏   92%  21,562,650
Neu gecacht (Tool-Ausgaben)   ▕██░░░░░░░░░░░░░░░░░░▏    8%  1,789,603
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  705
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  192,058
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 109 Sessions: 3,292,553,346 Token (34,968 Antworten).

