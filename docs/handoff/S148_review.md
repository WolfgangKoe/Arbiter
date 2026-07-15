STATUS: ANSWERED — Befund wird vom Koordinator wortgleich durchgereicht

# S148 Abschluss-Review (Reviewer-Subagent, Opus)

## Verdikt: GO mit Auflagen

Welle 1 ist funktional und regelkonform umgesetzt, Messstand bestätigt (Vollsuite
**1851 passed / 99,14 % Coverage** nachgelaufen, Architektur-Gate läuft mit und ist grün,
`black`/`isort`/`ruff` sauber über `src/`). Keine blockierenden Befunde. Zwei Auflagen (B)
betreffen Doku-Drift, die die genannte Abschluss-Liste des parallel laufenden Executors
noch **nicht** abdeckt.

## Prüftiefe (Stichproben, verifiziert)

- **Regelkonformität Overwatch/weapon_conditions** — belegt gegen rules_appendix.txt Z. 2319-2323
  („A unit cannot fire Overwatch if there are any enemy units within Engagement Range of it";
  „resolved like a normal shooting attack"). `in_melee`-Gate + `weapon_conditions: [RANGED]`
  sind eine korrekte, konservative Umsetzung. Tests wired (test_no_go_box_when_already_in_
  engagement_range, test_go_box_offered_when_not_in_melee, test_go_box_passes_reacting_unit_
  for_weapon_conditions).
- **Generic-src** — keine Fraktions-Strings in den `src/`-Diffs. `GAUSS`/`TESLA` nur in YAML;
  `RANGED`/`MELEE` in stratagem.py sind generisches Waffen-Shape-Vokabular (aus `is_melee`
  abgeleitet), keine Fraktionsnamen. INV-Wächter grün.
- **is_effect_executable = Single Source of Truth** — bestätigt: `_EFFECT_HANDLERS`-Dict wird
  von `is_effect_executable()` UND `execute_effect()` gelesen; armyCard konsumiert nur
  `is_effect_executable`, hält keine zweite Liste. test_is_effect_executable_matches_execute_
  effect_dispatch sichert die Kopplung.
- **grantsKeyword-Architektur** — YAML-Werte fließen ausschließlich über den Loader
  (`_weapon_profile_from_dict`, `_relic_weapon_from_entry`); Merge in `keywords`/`derived_keywords`
  via `_apply_weapon_granted_keywords` an allen 3 Waffen-Änderungsstellen (Basis, Wargear, Relic).
  Invariante „YAML nur über Loader" respektiert.
- **modifier-Blöcke** — Judgement of the Triarch / Showin' Off / Unbridled Carnage folgen exakt
  dem bestehenden Muster (roll_type/value/target/expires_at/source_label; vgl. Disruption Fields,
  Whirling Onslaught, Shadows of Drazak).

## Befunde

- **B1 — Doku-Drift Caption:** processes.md (Overwatch-Absatz) zitiert weiter *„Overwatch: only
  unmodified 6s hit." als „angezeigt"* und R-CHARGE-07 sagt „Die App zeigt bisher nur einen
  Hinweis" — die Caption ist im Code aber entfernt. Abschluss-Executor-Liste nennt nur
  next_session/backlog/operating_model → processes.md + acceptance/rules.md R-CHARGE-07 fallen
  durch. Auflage: mit der Caption-Entfernung mitziehen.
- **B2 — Untracked-Handoffs:** S148_planning.md + S148_ui_verifikation.md sind noch untracked;
  Löschung ist in der Abschluss-Liste vorgesehen — nur als Verifikationspunkt vor Commit vermerkt.
- **C1 — MWBD/Barge ist KEIN Bug (Stakeholder-Befund c relativiert):** Code gated MWBD korrekt
  auf CORE (unit_abilities.yaml `conditions: has_keywords: [CORE]`, geprüft via check_conditions).
  Die Annihilation Barge trägt CORE **regelkonform** — Wahapedia units_all.txt:505 listet
  „VEHICLE, CORE, QUANTUM SHIELDING, FLY". Also Datenlage == Quelle, kein fehlender Eligibility-
  Check. Der S149-„CORE-Datenprüfung"-Punkt wird das bestätigen, nicht korrigieren. (Quantum-
  Shielding-Anzeige, Befund b, ist ein separates fehlendes Feature, nicht Teil dieser Welle.)
- **C2 — camelCase-Interim:** grantsKeyword ist das erste camelCase-YAML-Feld neben 107
  snake_case-Feldern. Bewusst + in loader_contract.md §8 dokumentiert; akzeptabel, sollte aber
  vor dem Migrations-Ticket (S149+) nicht weiter proliferieren.
