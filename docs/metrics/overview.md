# Token-Report — Effizienz statt Menge

<!-- Generiert von tools/token_report.py — nicht von Hand pflegen. -->
Stand: 2026-06-19 18:24 UTC

Beantwortet: *wurden die Token gut ausgegeben, werden wir besser oder schlechter?*
Korridor: **150k** Kontext-Token je Antwort (CLAUDE.md). Token-Maß = input + cache_creation + cache_read + output.

## Fokus: letzte Session

**2026-06-19 17:59 · ac794a89**

- **Aufgabe:** start session + freigabe
- **Modelle:** Haupt Opus · Subagent —
- **Tokens gesamt:** 8,292,634 (Haupt 8,292,634 · Subagent 0, Anteil 0 %)
- **Peak-Kontext:** █████████░░░ 111k / 150k
- **cache_read:** 7,854,058 · **Output:** 127,765

Zusammensetzung aller Antworten (input / cache_creation / cache_read / output):

```text
input          ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    0%  8,674
cache_creation ▕█░░░░░░░░░░░░░░░░░░░░░░░▏    4%  302,137
cache_read     ▕████████████████████████▏   95%  7,854,058
output         ▕░░░░░░░░░░░░░░░░░░░░░░░░▏    2%  127,765
```

## Verlauf (letzte 6 Sessions)

Jüngste zuerst. Balken theme-sicher (Unicode); Trend ↑/↓ ggü. der älteren Session.
Modell-Mix: `█` Opus · `▓` Sonnet · `▒` Haiku · `·` sonstige.

```text
Session           Peak-Kontext           Subagent       Modell-Mix  
----------------- ---------------------- -------------- ------------
06-19 17:59 ac79  █████████░░░ 111k ↑    ░░░░░░   0% →  ████████████
06-19 16:17 5a54  ████░░░░░░░░  54k ↓    ░░░░░░   0% ↓  ████████████
06-19 15:34 2672  ████████████ 155k ↑    ░░░░░░   1% ↑  ████████████
06-19 15:00 bfc7  ███████████░ 135k ↓    ░░░░░░   0% ↓  ████████████
06-19 14:28 42c5  ████████████ 171k ↑    ░░░░░░   7% ↑  ███████████▓
06-18 20:32 e634  ██████░░░░░░  81k ↓    ░░░░░░   0% ↓  ████████████
```

## Hinweise

_Auto-generiert zur jüngsten Session._

- ✅ Peak-Kontext 111k blieb im 150k-Korridor.
- 💡 Große Session ohne Subagent — mechanische Fleißarbeit ließe sich an Sonnet/Haiku auslagern (CLAUDE.md, Tiering).

## Subagenten — wer wurde wofür gestartet

| Session | Modell | Agent | Aufgabe |
|---|---|---|---|
| 2026-06-19 15:34 · 2672bd18 | Sonnet | general-purpose | Draft Psychic Phase rule catalog |
| 2026-06-19 14:28 · 42c5e10a | Sonnet | general-purpose | Draft Charge/Morale rule entries |
| 2026-06-18 20:32 · 9f42d3f0 | Sonnet | general-purpose | Draft R-MOVE rule catalog entries |
| 2026-06-18 17:54 · 31e0b9d7 | Sonnet | general-purpose | Draft governance operating-model docs |
| 2026-06-17 18:07 · be0fc36f | Sonnet | general-purpose | Draft Command Phase rule catalog |
| 2026-06-17 16:45 · 86550f2b | Sonnet | general-purpose | Combat rule catalog draft |
| 2026-06-11 20:14 · 754eff0d | Haiku | Explore | Audit model-groups code correctness |
| 2026-06-11 16:49 · a176c827 | Haiku | Explore | Audit test coverage and docs |
| 2026-06-11 16:49 · a176c827 | Haiku | Explore | Audit security and input handling |
| 2026-06-11 16:49 · a176c827 | Haiku | Explore | Audit correctness and bugs |
| 2026-06-11 16:49 · a176c827 | Haiku | Explore | Audit tech debt and architecture |
| 2026-06-07 17:39 · 147f87c8 | Haiku | Explore | Audit all YAML data files across all factions for structural redundancy |
| 2026-06-05 18:15 · 32f76ee9 | Haiku | Explore | Ork unit abilities gap analysis |
| 2026-06-04 19:40 · bc940273 | Haiku | Explore | Scan for faction-specific hardcoding in gameMechanics |
| 2026-06-04 17:42 · ead78f19 | Sonnet | general-purpose | Wahapedia data fetch + YAML comparison for Necrons and Orks |
| 2026-06-04 12:18 · bdc63d07 | Sonnet | general-purpose | Wahapedia 9E rules research |
| 2026-06-04 07:32 · 15dddda1 | Sonnet | general-purpose | Subfaction affinity verification Necrons + Custodes |
| 2026-06-04 07:32 · 15dddda1 | Sonnet | general-purpose | WH40K 9E core rules research for shared_abilities |
| 2026-06-03 21:37 · 3019eacd | Haiku | Explore | Explore data layer: YAML files, loader, schemas |
| 2026-06-03 21:37 · 3019eacd | Haiku | Explore | Explore code callers and test patterns |
| 2026-06-03 21:37 · 3019eacd | Haiku | Explore | Explore Ork data files and full arkana.yaml for cleanup audit |
| 2026-06-03 20:39 · e259fb10 | Haiku | Explore | Research faction abilities across all factions |
| 2026-06-03 20:39 · e259fb10 | Sonnet | general-purpose | Research faction command-phase mechanics on Wahapedia |
| 2026-06-03 18:08 · 51558266 | Haiku | Explore | Vollständige Ability-Analyse aller Fraktionen |
| 2026-06-03 14:06 · 63304cc4 | Haiku | Explore | Read key UI files for Ziel 6 analysis |
| 2026-06-02 18:50 · 4e6f19df | Sonnet | general-purpose | Wahapedia game setup rules research |
| 2026-06-01 20:22 · d46eacfb | Haiku | Explore | Test file analysis for session state keys |
| 2026-05-31 17:28 · 33526f8d | Sonnet | general-purpose | Wahapedia: PL, Punkte, Brackets für Necrons fetchen |
| 2026-05-31 14:05 · 0041c5ee | Haiku | Explore | Explore data directory structure and spec |
| 2026-05-31 14:05 · 0041c5ee | Haiku | Explore | Explore wahapedia scraper capabilities |
| 2026-05-31 12:32 · dc2b02fb | Sonnet | general-purpose | Wahapedia relic + weapon ability texts |
| 2026-05-31 05:07 · 804d9ccd | Sonnet | general-purpose | Fetch Wahapedia Necrons stratagems page |
| 2026-05-30 03:54 · 366a7c8e | Sonnet | general-purpose | Documentation consistency audit |
| 2026-05-30 03:54 · 366a7c8e | Sonnet | general-purpose | Wahapedia setup rules research |
| 2026-05-30 03:54 · 366a7c8e | Sonnet | general-purpose | BattleScribe XML format research |
| 2026-05-28 07:37 · e114e70f | Sonnet | general-purpose | A1+A2 architecture research for Arbiter review doc |
| 2026-05-26 18:34 · db34412f | Sonnet | general-purpose | Ziel 1A — uiLayout Struktursplit |
| 2026-05-26 18:34 · db34412f | Sonnet | general-purpose | Ziel 1B — gameObjects Foundation |
| 2026-05-24 22:10 · 05f4c40e | Haiku | Explore | Explore web frontend files |

---

Σ über 147 Sessions: 2,396,792,503 Token (22,773 Antworten).

