STATUS: NEEDS-DECISION

# S168 — Finaler DoD-Review (Reviewer, Opus, eigenes Fenster)

Lebensdauer: bis Sichtung im S169-Planning, dann löschen.
Review-Gegenstand: gesamter uncommitted Working-Tree-Diff (`git status` + `git diff`),
Stand vor Abschluss-Commit. Regelgrundlage T2: `scratchpad/S168_T1_B123_regeln.md` (K1–K6,
Zitate aus `core_rules.txt` mit Zeilennummern).

## Gesamturteil: GO mit einer Pflicht-Korrektur vor Commit

Der B-123-Core-Fix (T2) und der UI-Nachzug (T3) sind regelkonform, generisch und vollständig
getestet; §7-Entwurf (T4) liegt entscheidungsreif vor. **Ein Artefakt-Drift (DoD-7) muss vor
dem Commit korrigiert werden:** die B-123-Statuszeile im Backlog behauptet T3 sei noch offen,
obwohl T3 diese Session umgesetzt wurde. Kein Code- oder Regel-Blocker.

## Messzahlen (alle selbst gemessen)

- Vollsuite `pytest --tb=short`: **2032 passed** in 291.90s, **Coverage 99.18 %** (Gate 99 %, erreicht).
- Architektur-Gate `pytest tests/architecture/ --no-cov -q`: **8 passed**.
- Doku-Gate `pytest tests/docs/ tests/acceptance/ --no-cov -q`: **25 passed** (acceptance) + **8 passed** (docs).
- INV-4b Ratchet: 6 Tokens / 16 Fundstellen / 3 Dateien — nicht verschlechtert (Gate grün).
- Regel-Ledger (impl. ohne Test): 0 (leer).

## Urteil je DoD-Punkt

### 1. Regelkonform — GO
- K1 (Intra-Attacken-Überschuss verfällt): `unitMutations.py:220-222` cappt Non-resolved-Treffer
  über `_group_front_hp` (`:163-173`) auf die Frontmodell-HP; da diese ≤ Gruppen-Pool ist, ist
  `overflow` in `_apply_directed_group_damage` (`:191-197`) für Einzelattacken immer 0. Spillover
  greift nur bei `resolved=True` (6d-v2-Volley-Total) → korrekt „cross-attack, never intra-attack".
  Belegt durch `test_apply_damage_directed_not_resolved_overflow_still_lost_within_one_attack`.
- K2/K3 (Zwangsbindung vs. Freiwahl): `get_locked_group` (`:129-160`) — heterogene Gruppen-Wundwerte
  (`unit.has_per_group_wounds()`, `unit.py:139-141`) locken ab dem 1. Schaden die Gruppe mit
  niedrigster `priority` (= stirbt zuerst, Konvention konsistent mit `_heal_group_wounds`/
  `_restore_group_models`); homogene Einheiten behalten Freiwahl. Belegt durch
  `test_get_locked_group_forces_front_group_before_any_wound_on_hetero_unit` und
  `test_get_locked_group_free_choice_of_any_homogeneous_group_at_full_health`.
- K4/K5 (Mortal-Wounds-Spillover/Reihenfolge): `apply_damage` (`:223-228`, `mortal=True` ignoriert
  Lock und spillt über Gruppengrenzen), belegt durch `test_directed_mortal_resolved_ignores_active_and_lock`.
- S166-Regression (26 Schaden auf vollen Silent King erreicht Szarekh): belegt durch
  `test_apply_damage_directed_resolved_regression_s166_26_damage`.
- Menhir-Sonderregel generisch abgeleitet + kanonisch dokumentiert: `rules_insights.md:80-95`.
  Kein Urteil aus dem Gedächtnis — gegen T1-Extrakt-Zitate geprüft.

### 2. Generisch — GO
- Entscheidungslogik nutzt ausschließlich `unit.has_per_group_wounds()` und `g.priority` — keine
  Fraktions-/Einheiten-Strings in der Logik (`unitMutations.py:156-159`, `_common.py:1955-1971`).
  Fraktionsnamen (Szarekh, Menhirs, Boyz, Silent King) erscheinen nur in Docstrings/Kommentaren
  als Beispiele. INV-4b-Gate grün, nicht verschlechtert; Architektur-Gate 8/8.

### 3. Tests grün — GO
- 2032 passed, 0 failed, Coverage 99.18 % (siehe Messzahlen). Der zuvor rote
  `test_no_done_or_answered_handoff_lingers` ist grün, da `S167_RETRO.md` im Working Tree gelöscht ist.
- Neue Tests: 11 in `test_unit_mutations.py` (Matrix directed×resolved×locked×mortal + K1/K3-
  Gegenbeispiele + Grenzfall-Vollzerstörung) und 3 Render-Einstiegspfad-Tests in `test_group_flow.py`.
  Testnamen verhaltensbeschreibend.

### 4. Architektur-Gate — GO
- `tests/architecture/`: 8 passed. Keine Invariante berührt/aufgeweicht.

### 5. Clean Code — GO (mit minorem Hinweis)
- Namen sprechend, Early Returns vorhanden (`get_locked_group`, `_apply_directed_group_damage`).
- Hinweis (kein Blocker): Die erweiterten Docstrings in `unitMutations.py:129-160` und `:179-190`
  erzählen Regelinhalte mit Zitaten recht ausführlich nach. Die Konvention erlaubt Gotcha-Kommentare
  mit Quelle; die kanonische Erzählung liegt bereits in `rules_insights.md`. Empfehlung: bei nächster
  Modulberührung die Docstrings auf einen Spec-Verweis + kurzes Warum kürzen (Ratchet, kein Big-Bang).

### 6. UI manuell verifiziert — GO (Reconciliation nötig)
- `S168_B123_ui_verifikation.md` ist vollständig: (a) Voraussetzungen inkl. konkretem Roster, (b)
  Klickpfad, (c) Erwartung für beide Zustände, plus die 3 Pflicht-Checkpunkte.
- **Beobachtung:** Der Stakeholder hat die 3 Checkpunkte bereits inline beantwortet
  (`:56`, `:60`, `:65`): Verhalten „nun regelkonform" (Checkpunkt 1 ✓), aber Kritik an
  Hinweis-Wortlaut („wahnsinnig übertrieben"), an Uneinheitlichkeit des Apply-Damage-Bereichs und
  an ungenügendem Design-System/Spec-Detailgrad (§1.4 ohne schematische Darstellung).
- Damit ist die manuelle Verifikation funktional erfolgt (regelkonform), der STATUS-Marker
  `AWAITING-VERIFICATION` widerspricht aber den bereits eingetragenen Antworten. **Zu klären im
  Abschluss/S169-Planning:** Status auf „verifiziert mit Folgekritik" reconcilen UND die Stakeholder-
  Kritik (Hinweis-Ton, Apply-Damage-Einheitlichkeit, Spec-Detailgrad) als Backlog-Item(s) erfassen —
  sonst geht die Beobachtung verloren (CLAUDE.md: Beobachtungen gehören in ein kanonisches Artefakt).

### 7. Artefakte aktuell — NO-GO (eine Pflicht-Korrektur vor Commit)
- **Stale-Drift:** `backlog_details.md:2382` „**Status:** ToDo — Core-Fix (T2) umgesetzt,
  UI-Nachzug (T3) offen" und der Block `:2442-2448` („aktuell zeigt Zustand A weiterhin einen freien
  Radio-Button …") beschreiben T3 als offen bzw. das alte UI-Verhalten als aktuell — T3 wurde diese
  Session umgesetzt (`_common.py:1955-1971` Zwei-Zweig-Warnung, `test_group_flow.py` 3 Tests).
  → Vor Commit korrigieren: Statuszeile auf „T3 umgesetzt, UI-Verifikation gemäß
  `S168_B123_ui_verifikation.md`" und den „Offen für T3"-Block als erledigt/umgeschrieben.
- Nebenbefund (kein Blocker): der T2-Block `:2431` nennt „2028 passed, 1 vorbestehender Fail
  (S167_RETRO.md)" — Momentaufnahme aus der T2-Mitte; Endstand ist 2032 passed / 0 fail. Bei der
  Statuskorrektur mitziehen.
- Korrekt/konsistent: `design_system.md` §1.4 (`:9`) und §7 (`:42 ff.`) vorhanden und in sich
  stimmig; §7.4 dokumentiert die §6.3-Abweichung sauber. `S168_SPEC7_ABNAHME.md` (NEEDS-DECISION)
  und `S168_B123_ui_verifikation.md` liegen als Mailbox-Dateien vor. Doku-/Acceptance-Gates grün.

## Offene Abschluss-Schritte (nach Review, vor/als Commit)
1. **Pflicht:** `backlog_details.md` B-123-Statuszeile (`:2382`) + „Offen für T3"-Block (`:2442`)
   auf T3-erledigt korrigieren (DoD-7-Blocker).
2. `S168_B123_ui_verifikation.md` STATUS mit den vorhandenen Stakeholder-Antworten reconcilen;
   Stakeholder-Kritik (Hinweis-Ton/Einheitlichkeit/Spec-Detailgrad) als Backlog-Item erfassen.
3. `.claude/tasks/briefing.md` aktualisieren (Stand/nächster Schritt/Erkenntnisse) — war zum
   Review-Zeitpunkt bewusst noch nicht aktualisiert, kein Mangel.
4. `S168_SPEC7_ABNAHME.md` bleibt bis Stakeholder-Entscheid im S169-Planning stehen.

## Ziel-Fortschritt
Ziel-Fortschritt: **ja** — sichtbar daran, dass B-123 vollständig (Core-Fix T2 + UI-Nachzug T3,
S166-Regression grün, Menhir-Zwangslock generisch) gefixt ist und der §7-Explodes-Entwurf
abnahmereif vorliegt. Einziger Rest ist die Artefakt-Statuskorrektur (DoD-7), kein Fachbruch.

## Selbstprüf-Checkliste
- [x] Jedes DoD-Urteil mit datei:zeile-Beleg
- [x] Vollsuite + Architektur + Doku-Gate selbst gemessen (Zahlen oben)
- [x] Keine Datei außer dieser Review-Datei geschrieben, kein Commit
