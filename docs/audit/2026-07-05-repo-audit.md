# Repo-Audit 2026-07-05 — Vollaudit (Standard-Tiefe)

Durchgeführt mit dem `improve`-Skill gegen Commit `f6c464a`
(Branch `feature/016-protocol-rp-effects`, Arbeitsbaum sauber).
Methode: Recon durch den Koordinator, danach 4 parallele read-only
Audit-Subagenten (Sonnet, isolierte Kontexte) für (1) Correctness, (2) Security
+ Dependencies, (3) Tests/Tech-Debt/Performance, (4) DX/Docs/Direction.
**Jeder übernommene Befund wurde vom Koordinator selbst am Code verifiziert**
(Datei + Zeile gelesen); Subagent-Zahlen ohne eigene Verifikation sind als
solche markiert. Bereits geplante bzw. am 2026-06-11 verworfene Befunde wurden
per Sperrliste ausgeschlossen (Reconcile gegen `plans/README.md`).

Abgeleitete Pläne: **033–041** in [`plans/`](plans/README.md).

## Befunde (verifiziert)

| # | Befund | Kategorie | Impact | Effort | Plan |
|---|---|---|---|---|---|
| 1 | `next_phase()` inkrementiert `phase_idx` vor `_reset_phase_state()` → `expires_at_phase`-Modifier (6 Stratagems) laufen erst beim nächsten *Beginn* derselben Phase ab statt an ihrem Ende (`game_state.py:636-638`; Kontrast: korrekter Rundenwechsel-Zweig `:632-635`) | Correctness | HOCH | S | 033 |
| 2 | Duplikat-Trupps (`#N`-State-Keys) werden in `moralePhase.py:80-83` in einer Bare-ID-Map nachgeschlagen → Moraltest still übersprungen; Roster `necrons_1500pts_silent_king.yaml` mit 4 Duplikaten ist live betroffen | Correctness | HOCH | S | 034 |
| 3 | Gleicher Key-Mismatch: Deployment-Snapshot (`gameProtocoll.py:104-110`), Melee-Liste (`fightPhase.py:485-486`), Revive-Wargear-Ziel (`commandPhase.py:317`, Schreiber `unitCard.py:269`) | Correctness | MITTEL | S | 034 |
| 4 | Stored XSS: Roster-`name`-Attribut → unescaped `display_name` (`rosz_importer.py:168/235`) → Spielername → f-String in `unsafe_allow_html` (`gameHeader.py:267-271`); Roster serverseitig persistiert → trifft spätere Besucher. Einzige Freitext-Quelle der App | Security | HOCH | S | 036 |
| 5 | Zip-Bomb: 5-MB-Check nur auf komprimierte Größe, `zf.read()` ohne Dekompressions-Limit (`rosz_importer.py:157-164`) | Security | MITTEL | S | 036 |
| 6 | `_reset_turn_state()` leert `active_buffs` beider Spieler bei jedem Zugwechsel (`game_state.py:568`) — „until your next Command Phase"-Buffs (MWBD) wirken de facto nur im eigenen Zug; UI zeigt weiter „Active", Budget verbraucht. Intendierte Semantik existiert in `commandPhase.py:161-173` | Correctness | HOCH | M | 035 |
| 7 | mypy strict konfiguriert, aber CI-Step `continue-on-error: true`; Fehlerbestand wächst (127 → ~136 seit 06-11; Zahl vom Subagenten gemessen) | DX | MITTEL | M | 038 |
| 8 | Totes Phasen-Lifecycle: `advance_stage()` ohne Aufrufer (Docstring behauptet fälschlich Button-Anbindung), 14 unerreichbare `render_start/end`, `phase_stage` nach Init konstant, `psychicPhase.render_end` = inertes Duplikat eines Live-Resets | Tech-Debt | MITTEL | S–M | 040 |
| 9 | Requirements ungepinnt (`>=`, kein Lockfile), kein `pip-audit` im CI; Dockerfile ohne `USER` (root) | Security/Deps | MITTEL | S | 037 |
| 10 | README reicht nicht für frischen Clone (kein venv/install/pre-commit/Port); `.env.example`-`DATA_DIR` tot (0 Referenzen); kein pytest-xdist (~64 s Suite × viele Läufe/Session; Zeit vom Subagenten gemessen) | DX | NIEDRIG–MITTEL | S | 039 |
| 11 | Regel-Sequenzierung (Mortal-Wounds, Smite/Perils/Deny, Teleport-Gate u. a., ~15–20 Funktionen) lebt in coverage-ausgenommenen `_render_*`-Funktionen mit 0 Testaufrufen — die Primitiven sind getestet, die Orchestrierung nicht; Befunde 1/2/3 saßen genau dort | Tests | HOCH | L | 041 (Stufe 1: 3 Cluster) |

## Direction-Optionen (Entscheid des Stakeholders, keine Pläne angelegt)

1. **ziel9 Faction Fetcher** — `tools/fetch_faction.py` fehlt, aber
   `wahapedia_scraper.py` (555 Z.) liefert die teure Grundlage; billigster Hebel
   gegen die 3-Fraktionen-Decke. Bestätigt bestehende Backlog-Priorität.
2. **Deployment-Phase** — mit 11 % niedrigster Regelbereich, kein Handler.
   Alternative zur Implementierung: explizite ADR „Deployment bleibt am Tisch",
   damit die Lücke eine Entscheidung wird.
3. **Mission-Scoring** — 23 %, nur manueller VP-Zähler
   (`gameActionsArea.py:270-325`); wenn angehen, dann eine Mission end-to-end,
   keine generische Engine im ersten Schritt.

## Geprüft und bewusst NICHT geplant

- **Setup-Screen lädt Punkte-/Roster-YAML pro Rerun neu**
  (`setupScreen.py:221-222` → `load_yaml` uncached): bestätigt, aber
  Kleinstdateien nur auf dem Setup-Screen — Nutzen unter Planschwelle.
- **6 ungenutzte Loader-Funktionen** (`load_weapon_abilities`,
  `wargear_ids_with_handler`, `load_wargear_abilities`, `load_detachment_types`,
  `load_points`, `scaled_pl` — je 0 Aufrufer in src/tools, nur eigene Tests):
  teils mutmaßlich Scaffolding für ziel9/Zukunft → **Merkposten: Intent mit
  Stakeholder klären**, dann löschen oder behalten. Kein blinder Löschplan.
- **3 handgerollte Undo-Muster** (`_undo_teleport`, `pending_mortal_undo`,
  `refund_deny`): echte Duplikation, aber genau an der „dritte
  Wiederholung"-Schwelle; Konsolidierung erst, wenn ein 4. Undo-Fall kommt
  (dann als Investigate-Plan).
- **`weapon = next(..., weapons[0])`-Fallback** (`_common.py:918`): defensiv,
  kein konstruierbarer Live-Pfad — nur bei Refactorings an `in_melee`-Timing
  erneut ansehen.

## Von den Subagenten als sauber gemeldet (Stichproben durch Koordinator)

`attack_math.py`/`combat.py` (Modifier-Caps, AP/Invuln), `unit_mutations.py`,
`ability_engine.py`, Psychic-State-Machine-Primitiven, `dice_compose.py`/
`dice_html.py`-Konsistenz, YAML-Load-Pfad (durchgängig `safe_load`), CI-Secret-
Handling, Log-Datei-Pfade (kein Traversal), `.streamlit/config.toml`-Defaults,
Doku-System (LEITSTAND/CLAUDE.md/backlog konsistent — ausdrückliche Stärke).

## Nicht auditiert

- Inhaltliche Korrektheit der YAML-Kataloge gegen Wahapedia (nur Stichproben,
  wo Code eine Datenform annimmt) — dafür läuft der separate Abgleich (Plan 032).
- `docs/work/`-Regeltexte selbst; `tools/`-Scraper in der Tiefe (Dev-only).
- Live-CVE-Scan der Dependencies (`pip-audit` nicht installiert — wird durch
  Plan 037 dauerhaft nachgerüstet); Versionseinschätzung des Subagenten beruht
  auf Modellwissen.
