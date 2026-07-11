# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-11 12:55 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-11 10:04 8553  ████████████ 173k ↑    ████░░  67% ↓  ▚▚▚▚▚▚▚▚····
07-10 21:31 e914  ███████████░ 134k ↓    █████░  89% ↑  ▚▚▚·········
07-10 16:04 54b0  ████████████ 197k ↑    █████░  83% ↓  ▚···········
07-10 13:33 b069  ████████████ 152k ↓    █████░  87% ↓  ▚▚▚▚▚·······
07-10 01:56 86c3  ████████████ 163k ↑    █████░  87% ↑  ▚▚··········
07-09 20:34 5769  ████████░░░░ 103k ↓    █████░  81% ↑  ▚··········▒
```

## Jüngste Session

**2026-07-11 10:04 · 855349e1**

- **Aufgabe:** Ich habe in S137_plan ein paar Antworten eingefügt. Ansonsten kannst du das die CLI von Markdown ins Projekt ziehen und…
- **Modelle:** Haupt Fable · Subagent Fable, Haiku, Opus, Sonnet
- **Tokens gesamt:** 45,924,502 (Haupt 15,291,073 · Subagent 30,633,429, Anteil 67 %)
- **Peak-Kontext:** ████████████ 173k / 150k
- **cache_read:** 39,614,146 · **Output:** 472,015

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ⚠️ 16 von 141 Antworten lagen über dem 150k-Korridor — Session früher schneiden.
- ✅ 67% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 11,429,734 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: P2-2 chargephase … ███████░░░░░  83k    ✅
2   general-purpose: Stikkbomb Inline-… ███████░░░░░  87k    ✅
3   general-purpose: Attack-UI-Bugs un… █████████░░░ 108k    ✅
4   general-purpose: P2-1 unitCard Bad… ██████░░░░░░  75k    ✅
5   general-purpose: YAML abilities Tr… ████░░░░░░░░  47k    ✅
6   general-purpose: B12 Konzept GO-us… ███████░░░░░  91k    ✅
7   general-purpose: S137 DoD-Review (… ██████░░░░░░  74k    ✅
8   general-purpose: S137 Planning-Ent… █████████░░░ 115k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  1,371
cache_creation ▕████░░░░░░░░░░░░░░░░░░░░▏   13%  5,836,970
cache_read     ▕████████████████████████▏   86%  39,614,146
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  472,015
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
Warm (System/Memory/History)  ▕████████████████████▏   86%  39,614,146
Neu gecacht (Tool-Ausgaben)   ▕███░░░░░░░░░░░░░░░░░▏   13%  5,836,970
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  1,371
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  472,015
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 111 Sessions: 3,201,353,605 Token (34,120 Antworten).

