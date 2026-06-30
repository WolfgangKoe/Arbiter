NEEDS-DECISION

# Planning — S113 (2026-06-30)

> Mailbox-Entwurf (ADR-0007). Branch: `feature/016-protocol-rp-effects`.
> Stand-Quelle: `.claude/tasks/next_session.md` (nach S112). Aktive Zieldatei: `docs/goals/ziel6.md` (Reste) + neu `ziel7.md`.

## Regelklärung vorab — Priorität 1 ist GEKLÄRT (kein Fix nötig)

**Stakeholder-Vermutung (S112-Befund):** Die Direktive des permanent aktiven (Extra-)Protokolls
werde EINMAL zu Spielbeginn gewählt und bleibe dann FIX; nur eine Silent-King-Fähigkeit könne das ändern.

**Regel-Befund (selbst nachgeschlagen, nicht geraten):**
`docs/work/wahapedia_necrons/faction_overview.txt`
- **Z. 568** (runden-zugewiesenes Protokoll): „When a command protocol becomes active … select one of its directives."
- **Z. 579** (Extra-/permanentes Protokoll bei Dynastie-Affinität): „… select which directive your units
  will benefit from **at the start of each battle round**."

Beide Direktiv-Wahlen (runden-zugewiesen UND Extra) werden also **jede Runde neu** getroffen.
Die Vermutung „einmal fix" ist damit **regeltechnisch widerlegt**.

**Code-Abgleich:** Das aktuelle Verhalten ist bereits korrekt UND dokumentiert:
`src/gameMechanic/game_state.py:583` `_reset_round_choice_state()` zitiert im Docstring (Z. 593–597)
exakt Z. 568 + Z. 579 und öffnet das Direktiv-Fenster (Haupt + Extra) bewusst pro Runde neu.

**Die einzige Regel, die Protokolle im Spiel umschichtet** = Voice of the Triarch (Silent King):
`data/wh40k_9e/necrons/unit_abilities.yaml:272–288`, `rule_text` Z. 278: „Once per battle, at the start
of any battle round … One command protocol that was not assigned … becomes active for that battle round
instead of the one assigned to it." → Das ändert **welches Protokoll aktiv ist**, NICHT die Permanenz
der Direktiv-Wahl. Handler `voiceOfTheTriarch` (Z. 288) ist YAML-deklariert, aber in `src/` **nicht
verdrahtet** (Backlog §2 „Voice of the Triarch", `grep voiceOfTheTriarch src/` = leer).

> **Folge:** Prio 1 braucht **keinen** Code-Fix an der Direktiv-Permanenz. Sie reduziert sich auf
> (a) Befund schließen + Regel als rules_insight festhalten, und (b) optional die Silent-King-Lücke
> (Voice of the Triarch) als eigenständigen Task einplanen.

---

## Drift-Befund (konstruktiv-kritisch) — next_session.md Prio 2a ist überholt

`next_session.md` Z. 54 sagt: „Fix B WAAAGH! generisch — `active_text`-Feld im YAML fehlt noch."
**Stimmt nicht mehr:** `data/wh40k_9e/orks/faction_abilities.yaml` hat `active_text` bereits
(Z. 35: „+1 Strength · +1 Attacks · 5+ invuln · Advance & Charge"; Z. 72 analog für Stage 2).
→ Vor dem Einplanen klären, was an „Fix B WAAAGH! generisch" real noch offen ist (vermutlich der
**Konsum** des Feldes im Render-Code, nicht das Feld selbst). Als Frage an den Stakeholder geführt.

---

## Session-Ziel (1–2 Sätze)

Den S112-Befund zur Extra-Direktiven-Permanenz **regelkonform schließen** (kein Fix — die App ist
bereits korrekt), die Erkenntnis als `rules_insight` sichern, und einen kleinen, in sich grünen
Folge-Schritt aus den Ziel6-Resten erledigen. Am Ende: Vollsuite ≥ 99 %, Architektur 8/8, Doku-Tests grün.

## Priorisierung

Prio 1 (Befund) ist die offene Frage aus S112 und blockiert das saubere Schließen der Protokoll-Arbeit
auf `feature/016`. Da die Regelklärung ergibt „kein Fix nötig", ist der teuerste Teil bereits erledigt —
es bleibt dünne Doku-Arbeit. Der freiwerdende Kontext-Korridor wird für **einen** kleinen Ziel6-Rest
genutzt (kleine Schritte, < 150k). Voice of the Triarch ist die natürlich nächste Protokoll-Lücke,
aber größer (eigener Plan) → als Option, nicht als Default.

---

## Aufgaben-Schnitt

| # | Aufgabe | Effort | Token | Modus | Subagent + Tier | Dateien (Scope) |
|---|---------|--------|-------|-------|-----------------|-----------------|
| T1 | Befund schließen + rules_insight | XS | ~6k | Gate | Executor + Haiku | s.u. |
| T2a | WAAAGH-Drift klären (read-only) | XS | ~5k | Gate | Planner/Executor + Haiku | s.u. |
| T2b | Ziel6-Rest: `once_per_battle` battle-scope | S–M | ~20k | Gate | Executor + Sonnet | s.u. |
| T3 (opt) | Voice of the Triarch Handler | M | ~30k | Gate | Executor + Sonnet | eigener Plan |

### T1 — S112-Befund regelkonform schließen (Default, Haiku)
**Was:** Festhalten, dass Extra- und Haupt-Direktive lt. Z. 568/579 **jede Runde** wählbar sind
(App korrekt), und die Silent-King-Ausnahme (Voice of the Triarch, Handler fehlt) notieren. Befund
in `next_session.md` von „P-hoch, regel-prüfen DANN fixen" auf „geklärt, kein Fix" umschreiben.
Neuer kurzer Eintrag in `docs/spec/rules_insights.md` (Direktiv-Wahl ist runden-scoped; nur Voice
of the Triarch schichtet Protokolle um).
**Betroffene Dateien (vollständig):**
- `.claude/tasks/next_session.md`
- `docs/spec/rules_insights.md`
**Tier:** Haiku (format-fixe Doku-Arbeit gegen expliziten Regeltext). **DoD:** keine Code-Änderung →
keine neuen Tests; Doku-Tests (`tests/docs/`) müssen grün bleiben (Zeilen-Limit next_session ≤ 120).

### T2a — WAAAGH-Drift klären (read-only Vorklärung, Haiku)
**Was:** Per `grep` belegen, ob `active_text` im Ork-Render-Code konsumiert wird; entscheiden, ob
„Fix B WAAAGH!" erledigt oder nur Anzeige offen ist. **Nur Befund**, keine Änderung ohne Freigabe.
**Betroffene Dateien (lesen):**
- `data/wh40k_9e/orks/faction_abilities.yaml`
- `src/uiLayout/armyCard.py`, `src/uiLayout/_common.py`
- `src/gameMechanic/ability_engine.py`
**Tier:** Haiku (reiner Lookup). **DoD:** n/a (read-only), Ergebnis als Mailbox-Notiz.

### T2b — Ziel6-Rest: `once_per_battle`-Enforcement battle-scope (Sonnet)
**Was:** `Stratagem.once_per_battle` (stratagem.py:59 „enforcement pending session-state tracking")
echt durchsetzen. Aktuell ist `used_stratagem_ids` phase-scoped → ein `once_per_battle`-Stratagem
ist faktisch nur once-per-phase gesperrt. Battle-scoped Set einführen (Session-State), Enforcement
in der Stratagem-Verfügbarkeitsprüfung, Reset bei Spielreset. **Regel:** Core Rules „once per battle".
**Betroffene Dateien (vollständig):**
- `src/gameObjects/stratagem.py`
- `src/gameMechanic/ability_engine.py` (Verfügbarkeits-/Dispatch-Pfad)
- `src/gameMechanic/game_state.py` (battle-scoped used-set + Reset)
- `tests/gameMechanic/test_ability_engine.py` (+ Regressionstest)
- ggf. `tests/gameMechanic/test_game_state.py`
**Tier:** Sonnet (Logik + Session-State-Verdrahtung, kein reiner Lookup). **DoD:** Regressionstest
„once_per_battle bleibt über Phasen-/Spielerwechsel gesperrt"; Vollsuite ≥ 99 %; Architektur-Gate 8/8;
Generic-src (keine Fraktions-Strings). **Hinweis:** Test-Mock-Fragilität (Backlog §4) beachten —
Importreihenfolge der `st`-Mocks.

### T3 (optional, eigener Plan) — Voice of the Triarch Handler (Sonnet)
**Was:** `voiceOfTheTriarch`-Handler verdrahten: einmal pro Spiel, am Rundenanfang (Szarekh auf dem
Feld) ein nicht-zugewiesenes Protokoll **statt** des zugewiesenen aktivieren. Greift in den Round-
Choice-Aktivierungspfad. **Größer** (UI-Aktivator + Engine + once-per-battle-Kopplung) → erst nach T2b
oder als separater Plan. **Betroffene Dateien (voraussichtlich):**
- `data/wh40k_9e/necrons/unit_abilities.yaml` (vorhanden)
- `src/gameMechanic/ability_engine.py`, `src/gameMechanic/game_state.py`
- `src/uiLayout/armyCard.py` / commandPhase-Aktivator
- Tests `tests/test_faction_abilities_necrons.py`, `tests/gameMechanic/test_ability_engine.py`
**Tier:** Sonnet. Hängt an der generischen Aktivator-Lücke (Backlog §0 „Failsafe/Arkana-Aktivator-UI fehlt").

---

## Offene Fragen / Entscheidungsbedarf (NEEDS-DECISION)

1. **Befund Prio 1:** Bestätigst du, dass Extra- + Haupt-Direktive lt. Regel (Z. 568/579) korrekt
   **jede Runde** wählbar sind und damit **kein Code-Fix** nötig ist? (Mein Befund: ja.) Dann schließt
   T1 den Befund nur dokumentarisch.
2. **WAAAGH-Drift:** Was ist an „Fix B WAAAGH! generisch" real noch offen, nachdem `active_text` im
   YAML bereits existiert? (T2a klärt read-only; bitte trotzdem die intendierte Stoßrichtung bestätigen.)
3. **Folge-Schritt nach T1:** Lieber **T2b** (`once_per_battle` battle-scope, klein, in sich grün)
   oder direkt **T3 Voice of the Triarch** (größer, schließt die Silent-King-Ausnahme aus dem Befund)?
   Default-Vorschlag: T1 + T2b in S113; T3 als eigener Plan in S114.

---

## Risiken / blinde Flecken

- **Test-Mock-Fragilität (Backlog §4):** T2b berührt `game_state` + `ability_engine`, beide mit
  globalem `session_state`-Zugriff und reihenfolge-abhängigen `st`-Mocks → neue Tests können bestehende
  brechen. Bei rot: STOP + fragen (Sicherheitsnetz-Regel).
- **Branch-Hygiene:** `feature/016-protocol-rp-effects` heißt nach Protokoll-RP-Effekten — T2b
  (Stratagem-Scope) ist thematisch off-branch. Vor Commit klären, ob T2b hierher gehört oder einen
  eigenen Branch braucht.
- **Doku-Zeilen-Limit:** `next_session.md` Gate ist 120 Zeilen (Test rot darüber). T1 muss beim
  Umschreiben des Befunds ggf. Erledigtes nach `backlog.md`/`session_archive.md` auslagern.
- **Voice of the Triarch (T3)** hängt an der generischen Aktivator-Lücke (Backlog §0) — nicht isoliert
  lösbar, daher bewusst als eigener Plan und nicht als S113-Default.

---

## Nächster Schritt
T1 (Befund schließen) → `.claude/tasks/next_session.md` Prio-1-Block + `docs/spec/rules_insights.md`.
