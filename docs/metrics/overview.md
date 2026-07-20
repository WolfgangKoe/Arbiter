# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-20 21:38 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-20 20:48 f518  ████████████ 168k ↑    ███░░░  44% ↓  ███·········
07-20 19:44 bc42  ████████████ 155k ↑    ████░░  67% ↓  ███·········
07-19 21:36 e1cb  ██████████░░ 129k ↑    █████░  90% ↑  ··········▒▒
07-19 16:41 4f3a  ██████████░░ 122k ↓    █████░  84% ↑  █··········▒
07-19 13:44 3636  ████████████ 182k ↑    █████░  82% ↓  ··········▒▒
07-18 22:58 067a  ███████████░ 133k ↑    ██████  94% ↑  ············
```

## Jüngste Session

**2026-07-20 20:48 · f5189ba5**

- **Aufgabe:** &lt;task-notification&gt; &lt;task-id&gt;a976eaf6222b0f3c4&lt;/task-id&gt; &lt;tool-use-id&gt;toolu_01LxQe1eW3kBEM8sE4mrSDMD&lt;/tool-use-id&gt; &lt;out…
- **Modelle:** Haupt Opus · Subagent Opus, Sonnet
- **Tokens gesamt:** 14,196,694 (Haupt 7,940,664 · Subagent 6,256,030, Anteil 44 %)
- **Peak-Kontext:** ████████████ 168k / 150k
- **cache_read:** 12,682,618 · **Output:** 226,428

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ⚠️ 19 von 66 Antworten lagen über dem 150k-Korridor — Session früher schneiden.
- ✅ 44% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 4,477,901 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: Review S174 Doku-… ████░░░░░░░░  50k    ✅
2   general-purpose: T1 Retro M1/M2/M3… ████░░░░░░░░  50k    ✅
3   Plan: B-028c2 reroll_rp Mini-Konze… █████░░░░░░░  61k    ✅
4   Plan: Planning-Entwurf S173-Retro-… ████░░░░░░░░  53k    ✅
5   general-purpose: T2 Backlog-Archiv… █████░░░░░░░  69k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  412
cache_creation ▕██░░░░░░░░░░░░░░░░░░░░░░▏    9%  1,287,236
cache_read     ▕████████████████████████▏   89%  12,682,618
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    2%  226,428
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
Warm (System/Memory/History)  ▕████████████████████▏   89%  12,682,618
Neu gecacht (Tool-Ausgaben)   ▕██░░░░░░░░░░░░░░░░░░▏    9%  1,287,236
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  412
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    2%  226,428
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 115 Sessions: 4,300,825,427 Token (48,078 Antworten).

