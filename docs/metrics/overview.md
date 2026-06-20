# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-06-20 11:03 UTC

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Fokus: letzte Session

**2026-06-20 09:41 · 593cf2bf**

- **Aufgabe:** start session + freigabe
- **Modelle:** Haupt <synthetic>, Opus · Subagent Sonnet
- **Tokens gesamt:** 28,890,772 (Haupt 19,893,071 · Subagent 8,997,701, Anteil 31 %)
- **Peak-Kontext:** ████████████ 162k / 150k
- **cache_read:** 27,306,771 · **Output:** 235,119

Zusammensetzung aller Antworten (input / cache_creation / cache_read / output):

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  32,539
cache_creation ▕█░░░░░░░░░░░░░░░░░░░░░░░▏    5%  1,316,343
cache_read     ▕████████████████████████▏   95%  27,306,771
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    1%  235,119
```

**Legende & Zielwerte:**

- **input** — neue, ungecachte Tokens → niedrig halten.
- **cache_creation** — erstmals gecacht (einmalig teurer) → moderat, unvermeidbar bei neuem Kontext.
- **cache_read** — aus warmem Cache gelesen (günstig) → **hoher Anteil = gut** (Kontext bleibt warm, Cache-TTL ~5 Min).
- **output** — generierte Tokens; **kein Selbstzweck — Qualität vor Menge.** Ein höherer Output-Anteil *relativ zu* cache_read kann Ziele schneller erreichen, *sofern das Ergebnis trägt*; viel cache_read bei wenig substanziellem Output = Reibung, „Mist“-Output ist schädlich, nicht gut.

**Zielbild:** hoher cache_read-Anteil + niedriger input-Anteil = effizientes Arbeiten; Output bewusst gegen Qualität gewichtet (nicht maximieren). Viele Cache-Misses (hoher input nach Pausen > 5 Min) sind ein Warnsignal.

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix: `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
06-20 09:41 593c  ████████████ 162k ↑    ██░░░░  31% ↑  ████████····
06-20 08:44 f4c2  ███████████░ 144k ↓    ██░░░░  28% ↑  █████████···
06-20 07:29 7048  ████████████ 304k ↑    ░░░░░░   0% ↓  ████████████
06-19 20:08 f76d  ████████████ 152k ↑    ░░░░░░   6% ↑  ███████████·
06-19 19:31 1273  █████████░░░ 110k ↑    ░░░░░░   0% ↓  ████████████
06-19 18:53 7f15  █████████░░░ 107k ↓    █░░░░░  12% ↑  ███████████·
```

## Hinweise

_Auto-generiert zur jüngsten Session._

- ⚠️ 27 von 217 Antworten lagen über dem 150k-Korridor — Session früher schneiden.
- ✅ 31% der Token liefen über Subagenten — das Hauptfenster blieb schlank.
- ✅ 8,997,701 Token auf günstigeren Tiers (Sonnet/Haiku) — gutes Tiering.

## Subagenten im 150k-Korridor

_Peak-Kontext je Subagent der letzten Session (selbe Metrik wie Haupt-Peak)._

```text
#   Agent / Aufgabe                     Peak-Kontext / 150k  Status
--- ----------------------------------- -------------------- ------
1   general-purpose: Add subagent peak… ████░░░░░░░░  52k    ✅
2   general-purpose: Extract render-le… ████████░░░░ 104k    ✅
```

## Subagenten — wer wurde wofür gestartet

| Session | Modell | Agent | Aufgabe | Peak |
|---|---|---|---|---|
| 2026-06-20 09:41 · 593cf2bf | Sonnet | general-purpose | Add subagent peak-context to overview | 52k ✅ |
| 2026-06-20 09:41 · 593cf2bf | Sonnet | general-purpose | Extract render-ledger logic + tests | 104k ✅ |
| 2026-06-20 08:44 · f4c215ad | Sonnet | general-purpose | Klasse-1 Ledger-Tests + R-CMD-03 Befund | 96k ✅ |
| 2026-06-19 20:08 · f76dbdd8 | Sonnet | general-purpose | Battle-Round rules catalog | 47k ✅ |
| 2026-06-19 18:53 · 7f1575c3 | Sonnet | general-purpose | Prepare next session docs | 65k ✅ |
| 2026-06-19 15:34 · 2672bd18 | Sonnet | general-purpose | Draft Psychic Phase rule catalog | 29k ✅ |
| 2026-06-19 14:28 · 42c5e10a | Sonnet | general-purpose | Draft Charge/Morale rule entries | 47k ✅ |
| 2026-06-18 20:32 · 9f42d3f0 | Sonnet | general-purpose | Draft R-MOVE rule catalog entries | 34k ✅ |
| 2026-06-18 17:54 · 31e0b9d7 | Sonnet | general-purpose | Draft governance operating-model docs | 28k ✅ |
| 2026-06-17 18:07 · be0fc36f | Sonnet | general-purpose | Draft Command Phase rule catalog | 65k ✅ |
| 2026-06-17 16:45 · 86550f2b | Sonnet | general-purpose | Combat rule catalog draft | 78k ✅ |
| 2026-06-11 20:14 · 754eff0d | Haiku | Explore | Audit model-groups code correctness | 75k ✅ |
| 2026-06-11 16:49 · a176c827 | Haiku | Explore | Audit test coverage and docs | 49k ✅ |
| 2026-06-11 16:49 · a176c827 | Haiku | Explore | Audit security and input handling | 45k ✅ |
| 2026-06-11 16:49 · a176c827 | Haiku | Explore | Audit correctness and bugs | 71k ✅ |
| 2026-06-11 16:49 · a176c827 | Haiku | Explore | Audit tech debt and architecture | 40k ✅ |
| 2026-06-07 17:39 · 147f87c8 | Haiku | Explore | Audit all YAML data files across all factions for structural redundancy | 49k ✅ |
| 2026-06-05 18:15 · 32f76ee9 | Haiku | Explore | Ork unit abilities gap analysis | 76k ✅ |
| 2026-06-04 19:40 · bc940273 | Haiku | Explore | Scan for faction-specific hardcoding in gameMechanics | 56k ✅ |
| 2026-06-04 17:42 · ead78f19 | Sonnet | general-purpose | Wahapedia data fetch + YAML comparison for Necrons and Orks | 57k ✅ |
| 2026-06-04 12:18 · bdc63d07 | Sonnet | general-purpose | Wahapedia 9E rules research | 31k ✅ |
| 2026-06-04 07:32 · 15dddda1 | Sonnet | general-purpose | Subfaction affinity verification Necrons + Custodes | 20k ✅ |
| 2026-06-04 07:32 · 15dddda1 | Sonnet | general-purpose | WH40K 9E core rules research for shared_abilities | 53k ✅ |
| 2026-06-03 21:37 · 3019eacd | Haiku | Explore | Explore data layer: YAML files, loader, schemas | 31k ✅ |
| 2026-06-03 21:37 · 3019eacd | Haiku | Explore | Explore code callers and test patterns | 49k ✅ |
| 2026-06-03 21:37 · 3019eacd | Haiku | Explore | Explore Ork data files and full arkana.yaml for cleanup audit | 46k ✅ |
| 2026-06-03 20:39 · e259fb10 | Haiku | Explore | Research faction abilities across all factions | 27k ✅ |
| 2026-06-03 20:39 · e259fb10 | Sonnet | general-purpose | Research faction command-phase mechanics on Wahapedia | 21k ✅ |
| 2026-06-03 18:08 · 51558266 | Haiku | Explore | Vollständige Ability-Analyse aller Fraktionen | 81k ✅ |
| 2026-06-03 14:06 · 63304cc4 | Haiku | Explore | Read key UI files for Ziel 6 analysis | 43k ✅ |
| 2026-06-02 18:50 · 4e6f19df | Sonnet | general-purpose | Wahapedia game setup rules research | 36k ✅ |
| 2026-06-01 20:22 · d46eacfb | Haiku | Explore | Test file analysis for session state keys | 39k ✅ |
| 2026-05-31 17:28 · 33526f8d | Sonnet | general-purpose | Wahapedia: PL, Punkte, Brackets für Necrons fetchen | 75k ✅ |
| 2026-05-31 14:05 · 0041c5ee | Haiku | Explore | Explore data directory structure and spec | 48k ✅ |
| 2026-05-31 14:05 · 0041c5ee | Haiku | Explore | Explore wahapedia scraper capabilities | 35k ✅ |
| 2026-05-31 12:32 · dc2b02fb | Sonnet | general-purpose | Wahapedia relic + weapon ability texts | 64k ✅ |
| 2026-05-31 05:07 · 804d9ccd | Sonnet | general-purpose | Fetch Wahapedia Necrons stratagems page | 39k ✅ |
| 2026-05-30 03:54 · 366a7c8e | Sonnet | general-purpose | Documentation consistency audit | 74k ✅ |
| 2026-05-30 03:54 · 366a7c8e | Sonnet | general-purpose | Wahapedia setup rules research | 13k ✅ |
| 2026-05-30 03:54 · 366a7c8e | Sonnet | general-purpose | BattleScribe XML format research | 87k ✅ |
| 2026-05-28 07:37 · e114e70f | Sonnet | general-purpose | A1+A2 architecture research for Arbiter review doc | 73k ✅ |
| 2026-05-26 18:34 · db34412f | Sonnet | general-purpose | Ziel 1A — uiLayout Struktursplit | 56k ✅ |
| 2026-05-26 18:34 · db34412f | Sonnet | general-purpose | Ziel 1B — gameObjects Foundation | 39k ✅ |
| 2026-05-24 22:10 · 05f4c40e | Haiku | Explore | Explore web frontend files | 35k ✅ |

---

Σ über 153 Sessions: 2,509,671,811 Token (24,050 Antworten).

