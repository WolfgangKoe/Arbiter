# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-19 16:33 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-19 13:44 3636  ████████████ 177k ↑    █████░  84% ↓  ··········▒▒
07-18 22:58 067a  ███████████░ 133k ↑    ██████  94% ↑  ············
07-18 20:59 6cfc  ██████████░░ 126k ↓    █████░  83% ↑  █···········
07-18 20:08 00eb  ███████████░ 140k ↑    ████░░  64% ↓  ██··········
07-18 12:29 cd6c  ██████████░░ 122k ↑    ████░░  73% ↓  █···········
07-18 11:00 b53c  █████████░░░ 109k ↓    █████░  85% ↑  ············
```

## Jüngste Session

**2026-07-19 13:44 · 363638c4**

- **Aufgabe:** start session. Ich habe alle Artefakte im Handoff kommentiert.
- **Modelle:** Haupt Fable · Subagent Haiku, Opus, Sonnet
- **Tokens gesamt:** 73,328,951 (Haupt 12,064,324 · Subagent 61,264,627, Anteil 84 %)
- **Peak-Kontext:** ████████████ 177k / 150k
- **cache_read:** 69,062,924 · **Output:** 407,831

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ⚠️ 24 von 104 Antworten lagen über dem 150k-Korridor — Session früher schneiden.
- ✅ 84% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 58,211,948 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: T8 Review S170 (O… ████░░░░░░░░  55k    ✅
2   general-purpose: S170-Planning ers… ████████░░░░  99k    ✅
3   general-purpose: T4-bc Menhir-Hinw… ██████████░░ 119k    ✅
4   general-purpose: T3 Screenshot-Dia… ██████░░░░░░  78k    ✅
5   general-purpose: T6 Verifikations-… ██░░░░░░░░░░  28k    ✅
6   general-purpose: T4-aef Layout+Lif… ████████████ 243k    ⛔
7   general-purpose: T2 Spec-first-Vor… ██████████░░ 121k    ⚠️
8   general-purpose: T1 Retro-Doku age… ███░░░░░░░░░  41k    ✅
9   general-purpose: T7 Artefakt-Nachz… ███████░░░░░  90k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  10,410
cache_creation ▕█░░░░░░░░░░░░░░░░░░░░░░░▏    5%  3,847,786
cache_read     ▕████████████████████████▏   94%  69,062,924
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  407,831
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
Warm (System/Memory/History)  ▕████████████████████▏   94%  69,062,924
Neu gecacht (Tool-Ausgaben)   ▕█░░░░░░░░░░░░░░░░░░░▏    5%  3,847,786
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  10,410
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  407,831
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 126 Sessions: 4,337,565,199 Token (48,831 Antworten).

