# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-11 09:59 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-10 21:31 e914  ██████████░░ 127k ↓    █████░  89% ↑  ▚▚▚·········
07-10 16:04 54b0  ████████████ 197k ↑    █████░  83% ↓  ▚···········
07-10 13:33 b069  ████████████ 152k ↓    █████░  87% ↓  ▚▚▚▚▚·······
07-10 01:56 86c3  ████████████ 163k ↑    █████░  87% ↑  ▚▚··········
07-09 20:34 5769  ████████░░░░ 103k ↓    █████░  81% ↑  ▚··········▒
07-09 20:34 19cb  ████████████ 173k ↓    ██░░░░  38% ↓  ·······▒▒▒▒▒
```

## Jüngste Session

**2026-07-10 21:31 · e914c95e**

- **Aufgabe:** start session
- **Modelle:** Haupt Fable · Subagent Fable, Opus, Sonnet
- **Tokens gesamt:** 76,165,549 (Haupt 8,089,567 · Subagent 68,075,982, Anteil 89 %)
- **Peak-Kontext:** ██████████░░ 127k / 150k
- **cache_read:** 70,190,385 · **Output:** 422,297

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 127k blieb im 150k-Korridor.
- ✅ 89% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 52,492,925 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: Planning-Entwurf … █████████░░░ 113k    ✅
2   general-purpose: S136-Abschluss: A… ████████████ 159k    ⛔
3   general-purpose: Retro-Maßnahmen H… █████░░░░░░░  61k    ✅
4   general-purpose: B1-Probe per Play… █████████░░░ 115k    ✅
5   general-purpose: 4c a+b Re-Roll-UI… ██████████░░ 130k    ⚠️
6   general-purpose: 4c(c) Command-Re-… ████████░░░░ 105k    ✅
7   general-purpose: Handoff bereinige… ██████░░░░░░  70k    ✅
8   general-purpose: 4c(c) Stufe 2: Hi… ████████████ 170k    ⛔
9   general-purpose: S136 DoD-Review d… ████░░░░░░░░  50k    ✅
10  general-purpose: B1 Scroll-Sprung … ██████░░░░░░  75k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  141,120
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    7%  5,411,747
cache_read     ▕████████████████████████▏   92%  70,190,385
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  422,297
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
Warm (System/Memory/History)  ▕████████████████████▏   92%  70,190,385
Neu gecacht (Tool-Ausgaben)   ▕██░░░░░░░░░░░░░░░░░░▏    7%  5,411,747
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  141,120
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  422,297
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 110 Sessions: 3,152,540,879 Token (33,463 Antworten).

