STATUS: ANSWERED

# S146 — Planungsentwurf

**Stakeholder-Entscheide (2026-07-14, Chat):**

1. Welle 1 (1a ∥ 1b): **freigegeben**.
2. Welle 2 mit Headroom-Gate: **freigegeben**.
3. Nihilakh: **vorab klären** — Lookup-Ergebnis (S146, Haiku-Subagent): **GEKLÄRT**,
   K1 schließt Nihilakh EIN. Primärquelle `faction_overview.txt:908–936` (drei Klauseln:
   Objective Secured, AP-1→0 wholly within eigener Aufstellungszone, beide Direktiven
   bei reiner Dynastie-Armee); der aktuelle YAML-Eintrag
   `subfaction_abilities.yaml:41–59` („Acquisitive Grasp", Fall-Back-Verbot) ist ein
   Datenqualitäts-Bug aus einer 8E-Zweitquelle und wird in K1 gegen den 9E-Wortlaut
   ersetzt.
4. Stufe-B-Verifikation läuft parallel rein stakeholderseitig; Befunde folgen nach
   Abschluss, keine Plan-Einarbeitung jetzt.

Auftrag: Planner-Subagent (general-purpose, Tier Sonnet), S146. Gelesen:
`CLAUDE.md`, `.claude/tasks/next_session.md`, `docs/goals/backlog.md` §Prioritätenliste,
`docs/goals/ziel7.md`, `docs/reference/agent_scopes.md`, `docs/handoff/S143_on_target_anker_konzept.md`,
`docs/handoff/S145_planning.md`, `docs/handoff/S144_klan_dynastie_konzept.md`,
`docs/audit/plans/S142_fixD_resolution_tabs.md`, plus gezielte `grep`/`Read` gegen
`data/wh40k_9e/orks/warlord_traits.yaml`, `src/`, `tests/`.

---

## 0. Checkbox-Sync (PFLICHT vor Planaufbau)

Alle in `docs/goals/ziel7.md` gesetzten Haken gegen `git log --oneline -30` geprüft:

- Stufe A Task 0/1/2 + manuelle Verifikation S121 + S130-7-Stratagems: Commits
  (`f9279fe`, `8c124c3`, `396fdec`, `b5c774b`, `2e3aa98`) liegen **vor** dem
  30-Commit-Fenster (ältere Sessions S120/S121/S130) — kein Widerspruch im Fenster.
- Stufe B „Vollständigkeitsabgleich" + „once_per_battle/conditions" (beide S123):
  ebenfalls vor dem Fenster, keine gegenteilige Spur im aktuellen Log.
- 6h Fix B WAAAGH generisch (×3, S113/`e031616`): vor dem Fenster.

**Befund: keine stale Checks im Log-Fenster der letzten 30 Commits.** Die einzige noch
offene Checkbox in `ziel7.md` ist bereits korrekt als offen markiert (Stufe B, Zeile 76:
„Manuelle UI-Verifikation mit echtem Necron-Roster" — läuft stakeholderseitig parallel,
Anleitung `docs/handoff/S145_stufeB_verifikation.md`, s. u. §4).

**Zusatzbefund (kein Stale-Check, aber Klärung wert):** `S143_on_target_anker_konzept.md`
trägt `STATUS: ANSWERED` und einen Stakeholder-Entscheid „Option A … freigegeben —
Umsetzung S144" (Zeile 177). Die Umsetzung ist **nicht** in den letzten 30 Commits
sichtbar (kein `_common.py`-Diff zu `render_group_assignment` mit `on_target`-Anker) —
sie wurde in S144 zurückgestellt und lebt seither als Rang 2 der Prioritätenliste weiter.
Kein Fehler, nur Doku-Erwartung („Umsetzung S144") vs. Ist („Umsetzung noch offen")
präzisiert.

---

## 1. Bestandsaufnahme Vigilus-Warlord-Traits (Rang 3, vor Vergabe verifiziert)

`data/wh40k_9e/orks/warlord_traits.yaml` (151 Zeilen) enthält unter der Überschrift
„Specialist Detachment Warlord Traits" (Zeile 106-151) genau **5 Einträge**, alle an
Vigilus-Defiant-Spezialdetachments gebunden (nicht Codex: Orks):

| Zeile | id | category |
|---|---|---|
| 108-116 | `blitz_brigade.back_seat_driver` | `blitz_brigade` |
| 118-125 | `dread_waaagh.dread_mek` | `dread_waaagh` |
| 127-134 | `kult_of_speed.quick_ladz` | `kult_of_speed` |
| 136-143 | `stompa_mob.gorks_one` | `stompa_mob` |
| 145-151 | `stompa_mob.morks_one` | `stompa_mob` |

Präzedenzfall (bereits umgesetzt, Commit `942e1ba`, S144): `data/wh40k_9e/orks/stratagems.yaml`
wurde exakt für dieselben vier Spezialdetachments (Blitz Brigade, Dread Waaagh!, Kult of
Speed, Stompa Mob) um 11 Stratagems gekürzt, Begründung im Datei-Header dokumentiert
(„Quelle ist das Kampagnenbuch Imperium Nihilus: Vigilus Defiant, nicht Codex: Orks").
Dieselbe Begründung gilt für die Warlord-Traits — Datenqualitäts-Nachzug, kein neuer Fall.

**Risiko-Verifikation (per grep):** `grep -rniE "warlord.?trait" src/` findet **keinen**
Loader/Engine-Konsumenten von `warlord_traits.yaml` — nur einen Kommentar in
`stratagemEngine.py:92`. `tests/` hat keine Datei, die `warlord_traits`/`load_warlord`
referenziert. Die Datei wird aktuell von keinem Code-Pfad geladen (Diskrepanz zu
`docs/spec/loader_contract.md:266`, das einen Ladepfad „nur der referenzierte Trait"
beschreibt, der nicht implementiert ist — **nicht** Teil dieses Tasks, nur zur Kenntnis).
Damit ist die Einschätzung „XS-Restrisiko" aus S145 bestätigt: reine Daten-Löschung ohne
Engine-/Test-Angriffsfläche.

---

## 2. Wellenplan

**Wellen-Kriterium wie S145: Datei-Disjunktheit.** `_common.py` ist der einzige
Kollisionspunkt (on_target-Anker UND FixD Brief 1 schreiben dort) — deshalb strikt
sequenziell 2a → 2b.

### Welle 1 (parallel, dateidisjunkt) — MUSS diese Session

| Aufgabe | Effort | Token-Schätzung | Dateien |
|---|---|---|---|
| 1a. on_target-Anker Option A | M | ~30k | `src/uiLayout/_common.py`, `tests/uiLayout/` |
| 1b. Vigilus-Warlord-Traits entfernen | S | ~12k | `data/wh40k_9e/orks/warlord_traits.yaml`, ggf. neuer Daten-Wächter-Test |

### Welle 2 (parallel untereinander, NACH Welle 1) — nur wenn Kontext-Korridor es erlaubt

Review-Budget-Regel beachten: ab ~100k Kontext keine neue Aufgabe mehr beginnen, solange
Review/Retro der Session noch aussteht. Welle 2 startet nur, wenn nach Welle 1 +
Zwischen-Commit realistisch noch Headroom für Review/Retro bleibt (Richtwert: Start von
Welle 2 nur unter ~70k Ist-Kontext).

| Aufgabe | Effort | Token-Schätzung | Dateien |
|---|---|---|---|
| 2a. Klan/Dynastie Brief K1 (Wortlaut-Fixes) | S | ~15k | `data/wh40k_9e/necrons/subfaction_abilities.yaml`, `data/wh40k_9e/orks/subfaction_abilities.yaml`, `tests/gameObjects/` |
| 2b. FixD Brief 1 (Compute/Render-Trennung) | M | ~38k | `src/uiLayout/_common.py`, `tests/uiLayout/test_common.py` |

2a und 2b sind dateidisjunkt (parallelisierbar); 2b darf erst nach 1a laufen (beide
schreiben `_common.py`).

**Stufe-B-Verifikation (Rang 8):** kein Executor-Brief — läuft stakeholderseitig parallel
zu jeder Welle, Anleitung `docs/handoff/S145_stufeB_verifikation.md`. Keine Koordinator-
Aktion nötig außer ggf. Rückfragen entgegennehmen.

---

## 3. Aufgabe 1a — on_target-Anker Option A

**Ziel:** Zusätzlicher `render_reactive_stratagem_box(def_faction, phase, event="on_target", …)`-Aufruf
in `render_group_assignment` (`src/uiLayout/_common.py`, Schleife über zugewiesene Ziele
~Zeile 2506), analog Konzept `S143_on_target_anker_konzept.md` Option A. Karte muss
verschwinden, sobald das Ziel per `toggle_group_target` wieder entfernt wird (Pflichtteil,
nicht optional — Konzept-Risikohinweis).

**Scope / erlaubte Quellen:** `src/uiLayout/_common.py`, `tests/uiLayout/` (Scope-Tabelle
Zeile „Phase-UI anpassen" + „Stratagem-Effekt umsetzen").

**Test-Budget:** gezielte Tests während der Arbeit (`pytest tests/uiLayout/ -q --no-cov`),
**eine** Vollsuite am Ende (`pytest --tb=short`, `timeout: 600000`, NICHT im Hintergrund).
Erwartete Neuzugänge: Anzeige-Test (Karte erscheint bei Zielzuweisung), Verschwinden-Test
(Karte weg nach Toggle-Rückgängig), Kein-Doppel-Verbrauch-Test (bereits genutzte GO bleibt
an beiden Ankern gesperrt).

**Selbst-Stopp:** Budget ~30k, harte Schwelle 45k — bei Überschreitung sofort abbrechen,
Zwischenstand (geänderte Dateien + offene Schritte) zurückgeben statt weiterzuarbeiten.

**DoD:**
1. Regelkonform — Whirling-Onslaught-Wortlaut bereits per Konzept belegt (`stratagems.yaml:400`), kein neuer Regel-Check nötig.
2. Generisch — `render_reactive_stratagem_box` ist bereits fraktionsneutral; keine neuen Fraktions-Strings.
3. Tests grün, Coverage ≥ 99 %.
4. Architektur-Gate grün (`pytest tests/architecture/ --no-cov -q`).
5. Clean Code — `black`/`isort`/`ruff` + `pre-commit run --files <geänderte Dateien>`.
6. UI manuell verifizieren: (a) Whirling Onslaught erscheint bei Zielzuweisung in der Verteidiger-Spalte; (b) verschwindet bei Toggle-Rückgängig; (c) bleibt am Wound-Anker weiterhin sichtbar (Option A ist additiv, kein Entfernen); (d) kein Doppel-CP-Verbrauch bei zwei sichtbaren Ankern.
7. Artefakte im selben Schritt: `S143_on_target_anker_konzept.md` STATUS `ANSWERED` → `DONE` + löschen (Erkenntnisse sind bereits vollständig in diesem Planning-Dokument + der Konzeptdatei selbst dokumentiert, nichts geht verloren); `docs/goals/backlog.md` Prioritätenliste Rang 2 auf erledigt markieren.

**Selbstprüf-Checkliste (zusätzlich zum Standardsatz `agent_scopes.md`):**
- [ ] Verdrahtung: neuer `render_reactive_stratagem_box`-Aufruf per grep in `render_group_assignment` belegt
- [ ] Toggle-Verschwinden-Test deckt tatsächlich `group_targets`-Rerun ab, nicht nur Erstanzeige
- [ ] `python tools/mypy_gate.py` — Baseline nicht erhöht
- [ ] INV-4b-Vokabular geprüft (`tests/architecture/test_generic_src_vocab.py`) vor neuen Namen

---

## 4. Aufgabe 1b — Vigilus-Warlord-Traits entfernen

**Ziel:** `data/wh40k_9e/orks/warlord_traits.yaml` Zeilen 106-151 (Abschnitt „Specialist
Detachment Warlord Traits", 5 Einträge: `blitz_brigade.back_seat_driver`,
`dread_waaagh.dread_mek`, `kult_of_speed.quick_ladz`, `stompa_mob.gorks_one`,
`stompa_mob.morks_one`) entfernen — analog Commit `942e1ba` (Stratagems-Pruning
derselben 4 Spezialdetachments). Datei-Header-Kommentar um denselben Ausschlusshinweis
ergänzen wie in `stratagems.yaml` (Quelle Vigilus Defiant, nicht Codex: Orks).

**Scope / erlaubte Quellen:** `data/wh40k_9e/orks/warlord_traits.yaml`,
`data/wh40k_9e/orks/stratagems.yaml` (nur lesend, als Formatvorbild für den
Header-Kommentar), `tests/gameObjects/test_data_quality.py` (falls ein Daten-Wächter
sinnvoll ist — s. u.).

**Vorab-Befund (bereits durch den Planner verifiziert, Executor muss nicht erneut suchen):**
Kein `src/`-Loader liest diese Datei (`grep -rniE "warlord.?trait" src/` trifft nur einen
Kommentar in `stratagemEngine.py:92`), kein Test referenziert sie. Reine Datei-Löschung
ohne Code-Konsumenten — **kein** Verdrahtungs-Risiko, aber auch **kein** grep-Beleg für
„Nicht-Test-Code ruft es auf" möglich (Datei ist grundsätzlich unverdrahtet, nicht nur der
gelöschte Teil). Selbstprüf-Punkt „Verdrahtung" entfällt dadurch begründet — im Endbericht
explizit vermerken, nicht stillschweigend auslassen.

**Test-Budget:** kein gezielter Testlauf nötig außer YAML-Parse-Check
(`python -c "import yaml; yaml.safe_load(open('data/wh40k_9e/orks/warlord_traits.yaml'))"`
oder bestehender Loader-Smoke-Test,
falls vorhanden), **eine** Vollsuite am Ende zur Absicherung, dass nichts unerwartet auf
die 5 IDs verweist (`grep -rn "blitz_brigade.back_seat_driver\|dread_waaagh.dread_mek\|kult_of_speed.quick_ladz\|stompa_mob.gorks_one\|stompa_mob.morks_one" data/ src/ tests/` vor dem Löschen, um verwaiste Referenzen auszuschließen).

**Selbst-Stopp:** Budget ~12k, harte Schwelle 18k.

**DoD:**
1. Regelkonform — Quelle bereits durch S144-Präzedenzfall (Stratagems) belegt; kein neuer Wahapedia-Check nötig, nur Konsistenz zur bereits getroffenen Stakeholder-Entscheidung.
2. Generisch — reine Datenänderung, keine `src/`-Berührung.
3. Tests grün (Vollsuite als Nachweis „nichts referenziert die 5 IDs mehr").
4. Architektur-Gate grün (unverändert, keine Architektur-Berührung erwartet).
5. Clean Code — YAML-Formatierung konsistent zum Rest der Datei, Header-Kommentar analog `stratagems.yaml`.
6. UI manuell — **entfällt**, da die Datei nicht gerendert wird (kein UI-Konsument, s. Vorab-Befund); explizit als n/a vermerken, nicht stillschweigend weglassen.
7. Artefakte im selben Schritt: `docs/goals/backlog.md` Prioritätenliste Rang 3 auf erledigt markieren.

**Selbstprüf-Checkliste:**
- [ ] grep-Beleg VOR dem Löschen: keine der 5 IDs wird sonstwo referenziert (Roster-YAMLs eingeschlossen: `data/rosters/*.yaml`)
- [ ] Datei bleibt valides YAML nach dem Schnitt (Parse-Test)
- [ ] `python tools/mypy_gate.py` — unverändert (keine `src/`-Datei berührt)
- [ ] Header-Kommentar-Ergänzung vorhanden und wortgleich zum Begründungsmuster aus `stratagems.yaml`

---

## 5. Aufgabe 2a — Klan/Dynastie Brief K1 (nur bei Headroom)

**Ziel:** 5 Wortlaut-Fixes an bestehenden `subfaction_abilities.yaml`-Einträgen gegen
`docs/work/wahapedia_orks/faction_overview.txt` bzw. `docs/work/wahapedia_necrons/faction_overview.txt`
Zeilen 847-1035 (Necron-Dynastien) + Snakebites-Ausnahmeklausel (Orks) — s.
`S144_klan_dynastie_konzept.md` §2 für die vollständige Soll/Ist-Tabelle:

| Fraktion | Eintrag | Fehler |
|---|---|---|
| Orks | Snakebites „Da Old Ways" | S8+-Ausnahmeklausel fehlt |
| Necrons | Novokh „Awakened by Murder" | falscher Effekt-Typ (Hit statt AP) |
| Necrons | Nephrekh „Translocation Beams" | Kernmechanik fehlt (nur Teilzitat) |
| Necrons | Sautekh „Relentless Advance" | komplett andere Fähigkeit/anderer Name |
| Necrons | Mephrit „Solar Fury" | falscher Name + Range-Bonus fehlt |

**Wichtig — Scope-Begrenzung (explizit, nicht selbst erweitern):** Dieser Brief korrigiert
NUR `rule_text`/`name_en` (Wortlaut). Er führt **nicht** den neuen `ability_type:
subfaction_passive` ein (Stakeholder-Entscheid S145: Option B, aber das ist K2-Scope,
Rang 7, noch nicht eingeplant) und schließt **nicht** die Engine-/Trigger-Lücke (§3 im
Konzept). Nihilakh bleibt unangetastet (Sekundärklausel ungeklärt, S144 Entscheidungsfrage 1
noch offen — kein Freigabe-Text dazu in den S145-Stakeholder-Entscheiden gefunden, im
Endbericht als weiterhin offene Frage markieren, nicht selbst entscheiden).

**Scope / erlaubte Quellen:** `data/wh40k_9e/necrons/subfaction_abilities.yaml`,
`data/wh40k_9e/orks/subfaction_abilities.yaml`, `docs/work/wahapedia_necrons/faction_overview.txt`,
`docs/work/wahapedia_orks/faction_overview.txt`, `tests/gameObjects/` (Loader-/Daten-Tests).

**Test-Budget:** gezielte Loader-Tests während der Arbeit, **eine** Vollsuite am Ende.
Erwartete Neuzugänge: je korrigiertem Eintrag ein Regressionstest, der den neuen
`rule_text` gegen das Wahapedia-Zitat prüft (String-Contains oder exakter Match, analog
bestehendem Muster in `test_data_quality.py`).

**Selbst-Stopp:** Budget ~15k, harte Schwelle 22k.

**DoD:**
1. Regelkonform — jeder neue Wortlaut mit Datei+Zeile aus `docs/work/wahapedia_*` belegt (nicht aus dem Gedächtnis, Konzept liefert die Fundstellen bereits vor).
2. Generisch — reine Datenänderung.
3. Tests grün, Coverage ≥ 99 %.
4. Architektur-Gate grün.
5. Clean Code — YAML-Konsistenz.
6. UI manuell — entfällt (Engine-Lücke bleibt bestehen, diese Einträge sind weiterhin nicht sichtbar/wirksam bis K2; explizit vermerken, kein Verifikations-Anspruch für diesen Brief).
7. Artefakte im selben Schritt: `docs/goals/backlog.md` Prioritätenliste Rang 6 auf erledigt markieren; `S144_klan_dynastie_konzept.md` bleibt bestehen (K2 braucht sie noch — NICHT löschen, erst wenn K2 abgeschlossen ist).

**Selbstprüf-Checkliste:**
- [ ] Jeder korrigierte `rule_text` mit `docs/work/wahapedia_*`-Fundstelle (Datei:Zeile) im Endbericht belegt
- [ ] Nihilakh unverändert (bewusst ausgeklammert, nicht versehentlich mitkorrigiert)
- [ ] `python tools/mypy_gate.py` — unverändert
- [ ] Kein `ability_type`-Feldwechsel (bleibt `triggered` — das ist K2-Scope)

---

## 6. Aufgabe 2b — FixD Brief 1 (nur bei Headroom)

Vollständig spezifiziert in `docs/audit/plans/S142_fixD_resolution_tabs.md` §4 „Brief 1 —
Compute/Render-Trennung ohne Layout-Änderung" (Effort M, nur `src/uiLayout/_common.py`,
kein Verhaltens-/Layout-Change, ~6-8 neue Tests für die extrahierte
`compute_resolution_context`-Funktion). Dieser Planungsentwurf übernimmt den Plan
unverändert als Brief — keine Abweichung nötig, Plan-Autor hat DoD/Selbst-Stopp bereits
in Abschnitt „Jeder Brief" adressiert (Vollsuite, Architektur-Gate, `black`/`isort`/`ruff`,
Verdrahtungs-grep, max. Effort M).

**Zusatz-Auflage für diesen Slot:** darf NICHT parallel zu Aufgabe 1a laufen (beide
schreiben `_common.py`) — erst nach Abschluss + Commit von 1a starten. Darf parallel zu
2a laufen (disjunkte Dateien).

**DoD-Ergänzung (Plan deckt 1-5 + 7 ab, hier nur Punkt 6 präzisiert):**
6. UI manuell verifizieren: Shooting- und Fight-Auflösung sehen pixelidentisch aus wie
   vorher (kein sichtbarer Unterschied — reiner Struktur-Refactor); ein voller Durchstich
   Deklaration→Apply→All done je Phase (wie im Plan gefordert).

**Artefakte im selben Schritt:** `docs/goals/backlog.md` Prioritätenliste Rang 4 auf
„Brief 1 erledigt, Brief 2+3 offen" präzisieren (kein Vollhaken, Rang 4 deckt nur Brief 1);
`docs/audit/plans/README.md` Status-Zeile für `S142_fixD_resolution_tabs.md` aktualisieren.

---

## 7. Freigabe-Fragen an den Stakeholder

1. **Welle 1 wie geplant freigeben?** (1a on_target-Anker Option A ∥ 1b Vigilus-Warlord-Traits
   entfernen, beide Effort ≤ M, dateidisjunkt.)
2. **Welle 2 (K1 ∥ FixD Brief 1) als bedingte Folge-Welle freigeben**, gestartet nur wenn nach
   Welle 1 + Zwischen-Commit realistisch Headroom für Review/Retro bleibt (Richtwert <70k
   Ist-Kontext vor Wellenstart) — oder soll Welle 2 grundsätzlich auf S147 verschoben werden,
   unabhängig vom Kontextstand dieser Session?
3. **Nihilakh-Sekundärklausel (K1-Ausklammerung bestätigen):** Bleibt Nihilakh in diesem
   Brief bewusst unangetastet (ungeklärte Quellenlage, S144 Entscheidungsfrage 1 weiterhin
   offen), oder soll die Klärung einer Primärquelle vorgezogen werden, damit K1 alle 6
   Necron-Dynastien in einem Rutsch abdeckt statt 5?
4. **Stufe-B-Verifikation (Rang 8):** weiterhin rein stakeholderseitig parallel laufen
   lassen (keine Koordinator-/Executor-Aktion), oder gibt es Rückmeldungen aus der
   laufenden manuellen Prüfung, die als neue Befunde in diese Session einfließen sollen?
