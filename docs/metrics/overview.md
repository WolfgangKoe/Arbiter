# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-06-27 08:15 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
06-27 07:30 8203  █████████░░░ 108k ↑    █████░  89% ↑  ████········
06-26 22:48 72c5  ██████░░░░░░  78k ↓    █████░  85% ↑  ············
06-26 22:24 654b  ███████████░ 141k ↓    █░░░░░  24% ↑  ············
06-26 18:17 3d7c  ████████████ 168k ↓    ░░░░░░   0% ↓  ▓▓▓▓▓▓▓▓▓▓▓▓
06-26 18:17 0c87  ████████████ 172k ↑    ███░░░  56% ↑  ············
06-26 17:27 23e6  ██████████░░ 128k ↓    ██░░░░  37% ↑  ████········
```

## Jüngste Session

**2026-06-27 07:30 · 8203a146**

- **Aufgabe:** &lt;task-notification&gt; &lt;task-id&gt;a951ea494cc8979f5&lt;/task-id&gt; &lt;tool-use-id&gt;toolu_01MLzqhpAjhsjhZXenwccMV2&lt;/tool-use-id&gt; &lt;out…
- **Modelle:** Haupt Opus · Subagent Opus, Sonnet
- **Tokens gesamt:** 27,798,782 (Haupt 3,065,350 · Subagent 24,733,432, Anteil 89 %)
- **Peak-Kontext:** █████████░░░ 108k / 150k
- **cache_read:** 24,707,960 · **Output:** 248,652

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 108k blieb im 150k-Korridor.
- ✅ 89% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 16,620,124 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: Executor Paket A+… ██████░░░░░░  79k    ✅
2   general-purpose: Finales Doku-Kons… █████░░░░░░░  58k    ✅
3   general-purpose: Executor Paket B … ████████████ 207k    ⛔
4   general-purpose: Governance-Konsis… ████░░░░░░░░  55k    ✅
5   general-purpose: Planungsartefakt-… ██████░░░░░░  73k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  35,316
cache_creation ▕███░░░░░░░░░░░░░░░░░░░░░▏   10%  2,806,854
cache_read     ▕████████████████████████▏   89%  24,707,960
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  248,652
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
Warm (System/Memory/History)  ▕████████████████████▏   89%  24,707,960
Neu gecacht (Tool-Ausgaben)   ▕██░░░░░░░░░░░░░░░░░░▏   10%  2,806,854
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  35,316
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  248,652
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 170 Sessions: 2,956,315,865 Token (29,479 Antworten).

