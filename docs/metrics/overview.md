# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-06-27 07:21 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
06-26 22:48 72c5  ██████░░░░░░  78k ↓    █████░  85% ↑  ············
06-26 22:24 654b  ███████████░ 141k ↓    █░░░░░  24% ↑  ············
06-26 18:17 3d7c  ████████████ 168k ↑    ░░░░░░   0% ↓  ▓▓▓▓▓▓▓▓▓▓▓▓
06-26 18:17 0c87  ███████████░ 142k ↑    ████░░  68% ↑  ············
06-26 17:27 23e6  ██████████░░ 128k ↓    ██░░░░  37% ↑  ████········
06-26 16:32 cf15  ███████████░ 136k ↑    █░░░░░  14% ↓  █···········
```

## Jüngste Session

**2026-06-26 22:48 · 72c53db3**

- **Aufgabe:** Start session
- **Modelle:** Haupt Opus · Subagent Sonnet
- **Tokens gesamt:** 12,790,097 (Haupt 1,861,123 · Subagent 10,928,974, Anteil 85 %)
- **Peak-Kontext:** ██████░░░░░░ 78k / 150k
- **cache_read:** 11,956,245 · **Output:** 78,261

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 78k blieb im 150k-Korridor.
- ✅ 85% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 10,928,974 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: Execute Plan 027 … █████░░░░░░░  67k    ✅
2   general-purpose: Review Plan 028 D… ███░░░░░░░░░  40k    ✅
3   general-purpose: Execute Plan 028 … ███████░░░░░  93k    ✅
4   general-purpose: Review Plan 027 d… ███░░░░░░░░░  34k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  31,181
cache_creation ▕█░░░░░░░░░░░░░░░░░░░░░░░▏    6%  724,410
cache_read     ▕████████████████████████▏   93%  11,956,245
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  78,261
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
Warm (System/Memory/History)  ▕████████████████████▏   93%  11,956,245
Neu gecacht (Tool-Ausgaben)   ▕█░░░░░░░░░░░░░░░░░░░▏    6%  724,410
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  31,181
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  78,261
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 175 Sessions: 2,978,619,641 Token (29,795 Antworten).

