# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-16 18:02 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-16 09:35 de37  ███████████░ 138k ↑    █████░  86% ↓  ▚▚··········
07-15 21:58 ad76  ██████████░░ 127k ↑    █████░  91% ↑  ▚▚·········▒
07-15 19:12 9dd1  █████████░░░ 106k ↓    █████░  86% ↑  █··········▒
07-15 19:12 628e  ████████████ 164k ↑    ███░░░  42% ↓  ············
07-15 17:44 ac36  ████████████ 154k ↓    █████░  88% ↑  ▚█··········
07-14 20:50 df5b  ████████████ 169k ↑    █████░  78% ↓  █···········
```

## Jüngste Session

**2026-07-16 09:35 · de3709f9**

- **Aufgabe:** start Session Hier meine Gedanken zur Backlog-Restrukturierung und next Session Backlog-Restrukturierung: - Einleitungs…
- **Modelle:** Haupt Fable · Subagent Fable, Sonnet
- **Tokens gesamt:** 47,977,068 (Haupt 6,700,232 · Subagent 41,276,836, Anteil 86 %)
- **Peak-Kontext:** ███████████░ 138k / 150k
- **cache_read:** 44,096,503 · **Output:** 257,279

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ⚠️ Peak-Kontext 138k nahe am 150k-Korridor (>90 %) — geordnet beenden und frisch starten.
- ✅ 86% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 34,958,054 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: S151-Abschluss: B… ███████░░░░░  86k    ✅
2   general-purpose: S151-A Backlog-In… ████████████ 148k    ⚠️
3   general-purpose: S151-C briefing.m… ████████████ 219k    ⛔
4   general-purpose: S151-D Wächter-Te… █████░░░░░░░  64k    ✅
5   general-purpose: S151-B Backlog-Re… ████████████ 228k    ⛔
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  6,125
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    8%  3,617,161
cache_read     ▕████████████████████████▏   92%  44,096,503
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  257,279
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
Warm (System/Memory/History)  ▕████████████████████▏   92%  44,096,503
Neu gecacht (Tool-Ausgaben)   ▕██░░░░░░░░░░░░░░░░░░▏    8%  3,617,161
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  6,125
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  257,279
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 115 Sessions: 3,523,687,018 Token (39,726 Antworten).

