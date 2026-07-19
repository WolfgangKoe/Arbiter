STATUS: NEEDS-DECISION

# S169 Review — Reviewer (Opus)

**Gesamturteil: NO-GO** — funktionale Substanz vollständig grün und regelkonform,
aber die Handoff-Aufräum-Aktion (Task 5) hat verwaiste Referenzen auf soeben
gelöschte Dateien in einer **aktiven Spec**, in **Quellcode** und im **aktiven
Backlog-Detail** hinterlassen. Das ist genau der DoD-Punkt 7 (keine Doku-Drift) und
der explizit geforderte Prüfpunkt „keine verwaisten Referenzen auf gelöschte
Handoff-Dateien". Die Korrekturen sind klein und mechanisch — nach ihnen GO.

---

## Gemessene Gates

| Gate | Ergebnis |
|---|---|
| `pytest --tb=short` (Vollsuite) | **2066 passed** in 325.91s |
| Coverage | **99.18 %** (Gate 99 %, `Required test coverage of 99.0% reached`) |
| `pytest tests/architecture/ --no-cov -q` | **8 passed** |
| `pytest tests/docs/ tests/acceptance/ --no-cov -q` | **25 passed** |
| Regel-Nenner | **159** (rules.md: A 69/99, B 0/41, C 18/19); Ledger (impl. ohne Test) = **0 (leer)**; getestet-Refs konsistent |

Alle Suiten grün, keine roten Tests, Coverage über Gate.

---

## Was einwandfrei ist (GO-Teile)

1. **b1 Datenmodell + Engine + Loader** — `effect.type: explode`
   (`roll_threshold`/`radius`/`damage`) und die `mandatory`-Achse sauber in
   `ability.py`/`loader.py`; `resolve_explode_effect` würfelt bewusst NICHT selbst
   (nur `exploded`-Durchreichung, ValueError-Guard bei Fehlverdrahtung);
   `_require_explode_effect_shape` erzwingt Vollständigkeit beim Laden (Spiegel zu
   `_require_wound_auto_fail_label`).

2. **b1 Regelkonformität — alle 5 Träger stichprobenübergreifend gegen Wahapedia belegt:**
   - Silent King / Vengeance of the Enchained: 4+ / 2D6" / D6 ✓ (Vorgabe erfüllt)
   - Triarch Stalker: 6 / 6" / D3 ✓ (Vorgabe erfüllt)
   - Annihilation Barge: 6 / 3" / 1 ✓
   - Night Scythe: 6 / 6" / D3 ✓
   - Gunwagon (Orks): 6 / 6" / D6 ✓ (Transport-Wortlaut „before any embarked models disembark" korrekt übernommen)
   - Vengeance-`rule_text` auf „On a 4+ **it explodes**" korrigiert — deckt sich mit Wahapedia.
   - **Canoptek Spyder bewusst ausgelassen** — Begründung im YAML sauber dokumentiert
     (1-3-Modell-Einheit, Trigger pro sterbendem Modell, kein Per-Modell-Casualty-State),
     mit Verweis auf denselben Grund wie `canoptek_plasmacyte`.

3. **Generic src/** — der `src/`-Diff enthält **keinen** Fraktions-String
   (grep necron/ork/silent king/triarch/spyder/… im `+`-Diff = leer). ✓

4. **b2 Call-Sites** — `render_explode_tiles_for_destroyed(first, second)` in allen 5
   `*Phase.py` verdrahtet und über `first`/`second` (nicht `active`) parametrisiert —
   respektiert die Seitenleisten-Invariante. ✓

5. **Spec-Konsistenz (Teil):** `design_system.md` §7 ist generisch umgebaut
   („Pflicht-Trigger-Kachel-Familie", §7.1/§7.2 abstrakt) und enthält **keine**
   Explodes-Zahlen (die „(D6/2D6)"-Stelle ist das generische Label-Schema, die
   „Silent King"-Nennungen betreffen §1.5/§1.7 model_groups, nicht Explode-Werte).
   Der einzige §7.x-Querverweis (`processes.md:738` → §7.1) ist **valide** (§7.1
   existiert). ✓

6. **agent_scopes.md M1** — Schema-Pflicht in der Selbstprüf-Checkliste ergänzt
   („PFLICHT ein schematisches Mini-Schema … nicht nur Prosa", Retromaßnahme S168-M1). ✓

7. **Handoff-Marker (Zeile-1-Konvention):** S169_M3_ALLOWLIST.md `NEEDS-DECISION`,
   S169_b2_ui_verifikation.md `AWAITING-VERIFICATION`, S169_PLANNING.md `NEEDS-DECISION`. ✓

8. **Backlog:** B-028c1 auf `In Progress` entstalet, **nicht** abgehakt — korrekt, da
   b3 (`auto_explode`-GO) offen und UI unverifiziert. ✓

---

## Pflicht-Korrekturen (Blocker — vor Commit beheben)

Task 5 hat 6 Handoff-Dateien gelöscht (S166_MOCKUP_EXPLODES.md/_V2.html,
S167_MOCKUP_EXPLODES_V3.html, S168_RETRO/REVIEW/SPEC7_ABNAHME.md), aber die folgenden
lebenden Artefakte zeigen weiter auf sie — Leser landen auf 404, das ist Doku-Drift:

1. **`docs/spec/processes.md:787`** (aktive Spec, P-16 Screenshot-Referenzblock):
   Prosa zitiert `docs/handoff/S166_MOCKUP_EXPLODES.md` als Bauform-Quelle. Die 5
   verlinkten Screenshots selbst sind vorhanden — nur die Herkunfts-Zitierung auf die
   gelöschte .md muss raus/umformuliert werden (Inhalt lebt jetzt in P-16 selbst).

2. **`src/gameMechanic/abilityEngine.py:673`** (Quellcode-Kommentar in
   `resolve_explode_effect`): zitiert `docs/handoff/S168_SPEC7_ABNAHME.md` als Beleg für
   die Zwei-Button-Form. Auf die kanonische Quelle umbiegen (`design_system.md` §7 /
   `processes.md` P-16), da die Handoff-Datei entfernt ist.

3. **`docs/goals/backlog_details.md:696/700/720`** (aktiver Backlog-Detail zu B-028c1,
   nicht Archiv): zitiert S166_MOCKUP_EXPLODES_V2.html, S166_MOCKUP_EXPLODES.md §g,
   S167_MOCKUP_EXPLODES_V3.html §h. B-028c1 ist ein **offenes** Item (In Progress), also
   kein archivierte-Historie-Freibrief — die Zitate auf die neuen kanonischen Orte
   (design_system §7 / processes P-16) umbiegen oder als „(Mockup S166/S167, in Spec
   überführt)" ohne Dateilink umformulieren.

Einordnung Konventionsfrage (aus dem Auftrag): Archivierte Historie
(`backlog_archive.md`, `docs/goals/archive/`) darf alte Dateien nennen — aber diese
Treffer stehen in **aktiven** Artefakten (Spec, Quellcode, aktives Backlog-Detail),
daher fallen sie unter das Drift-Verbot.

---

## Bewertung: Commit vor UI-Verifikation vertretbar?

**Ja, vertretbar** — nach Behebung der Pflicht-Korrekturen. Die b2-UI
(`render_explode_tiles_for_destroyed`, Render-Code) ist per Projektregel von der
Coverage ausgenommen und wird manuell verifiziert; der Verifikations-Handoff
`S169_b2_ui_verifikation.md` steht auf `AWAITING-VERIFICATION`, und B-028c1 ist NICHT
abgehakt. Damit ist der offene Zustand korrekt markiert und geht nicht verloren
(Präzedenz: Handoff-Marker bleibt offen, Checkbox ungesetzt). Der Commit dokumentiert
also einen ehrlichen Zwischenstand — kein „fertig"-Anspruch auf ungeprüfter UI.

**Manuell zu prüfen (Stakeholder, laut Handoff):** Pflicht-Trigger-Kachel erscheint
inline am Eintrag der zerstörten Einheit in allen 5 Phasen; Binär-Wurf-Baustein
(„Explodes!"/„Does not explode") ohne Engine-Selbstwurf; Multi-Unit-Ziel-Auswahl +
Schadens-Zahlenfeld je Ziel; Confirm-all senkt LP-Balken live; Reset verwirft.

---

## Nebenbefund (kein Blocker)

- Der `resolve_explode_effect`-Docstring ist sehr lang (Warum-Begründung + Verweise) —
  vertretbar (nicht-offensichtliche „App würfelt nicht"-Entscheidung), aber grenzt an die
  Kommentar-Konvention (Spec statt Kommentar). Bei nächster Modul-Berührung Richtung
  Spec-Verweis straffen (Ratchet), nicht jetzt.

---

## Token-/Kontext-Report (Review-Lauf)

Reine Review-Arbeit (read-only außer dieser Datei). Kein präzises Selbst-Maß im
Subagenten verfügbar; geschätzt deutlich innerhalb des Korridors (< 150k, grober
Bereich ~45–55k durch die große YAML-/Wahapedia-Ausgabe). Kein Wind-down nötig.
Sessionstand: b1+b2 inhaltlich fertig; verbleibend vor Commit = die 3 Ref-Korrekturen
(Minuten); b3 (`auto_explode`-GO) und UI-Verifikation planmäßig → S170.
