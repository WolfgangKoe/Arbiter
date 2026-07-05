# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-07-05 19:55 CEST

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix (Subagenten): `▚` Fable · `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
07-05 19:41 67da  █████░░░░░░░  61k ↓    █████░  83% ↑  ···········▒
07-05 17:03 121e  ██████████░░ 130k ↓    ████░░  69% ↓  ▚▚▚▚█·······
07-05 13:00 5226  ████████████ 144k ↓    ████░░  74% ↑  ············
07-05 08:37 06c9  ████████████ 205k ↑    ████░░  66% ↓  ············
07-04 20:21 4f34  ██████████░░ 124k ↓    █████░  85% ↑  ············
07-04 14:45 b13e  ████████████ 147k ↑    ████░░  67% ↓  ▚▚▚█·······▒
```

## Jüngste Session

**2026-07-05 19:41 · 67da766e**

- **Aufgabe:** Du hast die Freigabe für den Plan. Sobald die Subagenten dafür laufen, beauftrage einen weiteren, der prüft, was mit /h…
- **Modelle:** Haupt Fable · Subagent Haiku, Sonnet
- **Tokens gesamt:** 7,881,723 (Haupt 1,302,660 · Subagent 6,579,063, Anteil 83 %)
- **Peak-Kontext:** █████░░░░░░░ 61k / 150k
- **cache_read:** 6,760,121 · **Output:** 80,169

## (Retro-)Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 61k blieb im 150k-Korridor.
- ✅ 83% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 6,579,063 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## 150k-Korridor für Subagenten

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   Explore: r-proto-02 Löschbarkeit p… ██░░░░░░░░░░  26k    ✅
2   general-purpose: Planning-Entwurf … ███████░░░░░  90k    ✅
3   general-purpose: Plan 038+039 ausf… ██████░░░░░░  76k    ✅
4   Explore: Ratchet/Ledger-Trend anal… ████░░░░░░░░  53k    ✅
```

## Zusammensetzung der Antworten

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  16,616
cache_creation ▕████░░░░░░░░░░░░░░░░░░░░▏   13%  1,024,817
cache_read     ▕████████████████████████▏   86%  6,760,121
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  80,169
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
Warm (System/Memory/History)  ▕████████████████████▏   86%  6,760,121
Neu gecacht (Tool-Ausgaben)   ▕███░░░░░░░░░░░░░░░░░▏   13%  1,024,817
Ungecacht (neue Inhalte)      ▕░░░░░░░░░░░░░░░░░░░░▏    0%  16,616
Generiert (Output)            ▕░░░░░░░░░░░░░░░░░░░░▏    1%  80,169
```

**Legende (Slide-Kategorien):**

- **Warm** (`cache_read`) — System-Prompt, CLAUDE.md, Memory, stabiler Verlauf (bereits im Cache; günstig). Hoher Anteil = warmer Kontext = effizient.
- **Neu gecacht** (`cache_creation`) — neue Datei-Inhalte, Tool-Ausgaben, die erstmals gecacht werden (einmalig teurer, danach warm).
- **Ungecacht** (`input`) — frische Konversations-Token, die noch nicht im Cache sind. Niedriger Anteil anstreben.
- **Generiert** (`output`) — Antwort-Token. Kein Selbstzweck; Qualität vor Menge.

## Vergangene Sessions

→ vollständige Historie: [session_archive.md](session_archive.md)

---

Σ über 128 Sessions: 2,924,834,443 Token (30,157 Antworten).

