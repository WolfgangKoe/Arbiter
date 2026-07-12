STATUS: ANSWERED

Auflage erfüllt (Lifecycle-Löschung der zwei markierten Handoffs, EXCLUDED-Header
präzisiert), Vollsuite danach erneut grün (1816 passed, 99,12 %);
Warlord-Traits-Folgebefund → S145.

# S144 — Ganzheitlicher DoD-Review (Reviewer-Subagent, Opus)

Prüfgegenstand: kompletter uncommitteter Arbeitsstand (`git status` + `git diff`,
inkl. gelöschter/neuer Dateien — kein S144-Commit vorhanden). Branch
`feature/016-protocol-rp-effects`. READ-ONLY; einzige geschriebene Datei ist dieser Befund.

## Gesamturteil: NO-GO (Rote Tests blockieren Commit) — nach trivialer Auflage GO

Der Arbeitsstand ist inhaltlich sauber: Datenpflege regelkonform, Refactor
verhaltensgleich, `src/` generisch, Formatter/Architektur/mypy grün, Artefakte gut
nachgezogen. **Ein einziger, aber harter Blocker:** der Hygiene-Test
`test_no_done_handoff_lingers` ist rot, weil zwei auf `DONE` gesetzte Handoffs nicht
gelöscht wurden. Regel „Kein Commit mit roten Tests" ⇒ NO-GO. Die Behebung ist trivial
(zwei Dateien löschen, Erkenntnisse sind bereits überführt) — danach GO.

## DoD-Punkte

**1. Regelkonform — GRÜN.**
- Orks: die 11 entfernten Vigilus-Defiant-Einträge (BLITZ BRIGADE, DREAD WAAAGH!,
  KULT OF SPEED, STOMPA MOB, OPENING SALVO, KRUSH 'EM, HOLD ON BOYZ!, KUSTOM AMMO,
  TURBO-BOOSTAS, STOMP STOMP STOMP!, STOMPA-PORTA) kommen in
  `docs/work/wahapedia_orks/stratagems.txt` **nicht** vor (grep leer) → korrekt als
  Nicht-Kodex entfernt. Stichprobe der verbliebenen (Showin' Off, Ded Sneaky, Wreckaz,
  Get Da Loot, Unbridled Carnage, Mystic Chanting …) ist in der Wahapedia-Liste
  vorhanden. Entryzahl real = 17 (Header: „2 Requisitions + 8 Core + 7 Klan"), stimmt.
- Necrons: real = 40 (Header „34 Core + 6 Dynastic"), stimmt; der alte Header war
  intern widersprüchlich (35+6+8+8=57≠56) und wurde beim Kürzen auf konsistente 34+6=40
  korrigiert — positiv. Siehe Befund 2 zur Wortlaut-Nuance.

**2. Generisch — GRÜN.** `git diff src/` fügt keine neuen Fraktions-Strings/-Checks ein;
die Änderungen sind reine Typannotationen + Extraktion des generischen Helfers
`_sum_effect_value`. INV-4b-Ledger unverändert (6 Tokens, 16 Fundstellen — bestehende Schuld).

**3. Tests — ROT (1 Fehlschlag), Coverage GRÜN.** `pytest --tb=short`: 1 failed,
1815 passed. Coverage TOTAL 99.12 % ≥ 99 % (abilityEngine 100 %, stratagemEngine 98 %
— Gesamtgate erfüllt). Einziger Fehler: `test_no_done_handoff_lingers` (Befund 1).
`python tools/mypy_gate.py`: `24 errors == baseline 24 — OK` (Baseline 28→24 korrekt
mitgezogen).

**4. Architektur-Gate — GRÜN.** Alle Wächter (INV-1..5) im Vollsuite-Lauf grün; keine
Invarianten-Verletzung.

**5. Clean Code — GRÜN.** `black --check .` (140 Dateien unverändert), `isort --check-only .`
(sauber), `ruff check` (All checks passed). Helfer-Docstring benennt die 6 Call-Sites und
den `combine=min`-Sonderfall — nachvollziehbar.

**6. UI manuell verifiziert — n/a (bestätigt).** `git diff --stat` berührt kein
`uiLayout/` und keine `*Phase.py`; Render-Code unverändert. Refactor ist verhaltensgleich
(Helfer-Logik 1:1 mit den Ursprungsschleifen abgeglichen, inkl. `missing_value=None`-
Skip bei `ability_invuln_save`). Keine manuelle UI-Prüfung nötig.

**7. Artefakte — überwiegend GRÜN, ein Blocker (Befund 1).**
- ziel7.md/backlog.md: Klan-Affinität-Drift geschlossen, neuer Scope Klan-/Dynastie-
  Fähigkeiten sauber verlinkt; Cap-DRY-Schuld + Directive-DRY-Schuld als Backlog-§4-
  Einträge ergänzt. Konsistent.
- Keine Referenz auf entfernte Stratagems in `docs/spec/` oder `docs/goals/`
  (grep leer) → keine verwaisten Verweise.
- Bekannter Folgebefund korrekt eingeordnet: 5 Vigilus-Warlord-Traits in
  `data/wh40k_9e/orks/warlord_traits.yaml:108ff` (blitz_brigade/dread_waaagh/
  kult_of_speed/stompa_mob) warten auf Stakeholder-Entscheid — **nicht** als neuer
  Befund gewertet.
- Handoff-Marker sonst konsistent: S144_planning=ANSWERED, S144_review_s143 und
  S144_klan_dynastie_konzept=NEEDS-DECISION.

## Befundliste

**1. [BLOCKER] Zwei DONE-Handoffs nicht gelöscht → Hygiene-Test rot.**
Beleg: `tests/docs/test_handoff_hygiene.py:56` (AssertionError listet
`S143_abilityengine_refactor.md`, `S143_stratagem_kodex_abgleich.md`);
`docs/handoff/S143_abilityengine_refactor.md:1` und
`docs/handoff/S143_stratagem_kodex_abgleich.md:1` tragen `STATUS: DONE`. Beide Dateien
sagen im Text selbst „Datei kann gemäß Lifecycle gelöscht werden". Regel „Kein Commit
mit roten Tests" ⇒ blockiert den Abschluss.
Lösung: Die Erkenntnisse sind bereits überführt (Refactor-Punkt-4 → backlog §4;
Stratagem-Abgleich → Header/EXCLUDED-Blöcke + ziel7/backlog). Daher **beide Dateien
löschen** (`git rm docs/handoff/S143_abilityengine_refactor.md
docs/handoff/S143_stratagem_kodex_abgleich.md`), dann Vollsuite grün. Falls doch etwas
bewahrt werden soll: vorher in Backlog/Spec ziehen, nicht als DONE liegen lassen.

**2. [NIEDRIG / Wortlaut] Necron-Header-Formulierung leicht ungenau.**
Beleg: `data/wh40k_9e/necrons/stratagems.yaml` EXCLUDED-Block („laut wahapedia 9ed …
are not Codex: Necrons content"); die entfernten Einträge existieren aber sehr wohl in
`docs/work/wahapedia_necrons/stratagems.txt` (z. B. EXALTED CRYPTEK :138, OVERKILL
PROTOCOLS :126, MURDEROUS DEMISE :162, WEAPONISED BODIES :168). Wahapedia aggregiert
Codex **und** White-Dwarf-Supplement-Detachments; die Entfernung ist inhaltlich korrekt
(Cult of the Cryptek = WD 08/22, Annihilation Legion = WD 10/22 sind echte White-Dwarf-
Detachments), aber die Wortwahl suggeriert „steht nicht in wahapedia". Anders als bei
Orks (dort fehlen die Einträge in der Quelle tatsächlich) ist es hier eine
Kodex-vs-Supplement-Kuration.
Lösung: optional präzisieren, z. B. „Quelle: White Dwarf, nicht Codex: Necrons —
wahapedia listet sie unter Supplement-Detachments". Kein Blocker.

## Selbstprüfung
Stichproben mit Fundstelle belegt (Wahapedia-Zeilen zitiert). pytest/mypy/black/isort/ruff
tatsächlich ausgeführt und Ergebnisse zitiert. Jeder Befund mit Beleg + Lösungsvorschlag.
Außer dieser Datei nichts geändert.
