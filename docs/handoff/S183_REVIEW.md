STATUS: NEEDS-APPROVAL

# S183 — DoD-Review B-134-Fix + Retro-M2/M3 + Artefakt-Nachzug

## Urteil: GO — mit einer Commit-Auflage (A1) + zwei Follow-up-Minors (S184)

Der Callback-Umbau ist fachlich korrekt und vollständig: die drei Inline-Schaden-Mutationen
sind semantik-treu in `on_click`/`on_change` verlagert, Berechnung/Reihenfolge/group_wounds-
Zwangszuteilung unverändert, kein stiller Verhaltensbruch. Tests treiben den Render-Einstiegspfad
(S164-Lehre erfüllt), M3-Assert vorhanden, Doku widerspruchsfrei. Keine Major-Befunde.

---

## Befunde

### A1 (Auflage, Commit-Zeit) — Referenzierter Screenshot ist untracked
`docs/handoff/Bildschirmfoto vom 2026-07-23 23-44-40.png` ist als **Beleg** referenziert in
`docs/goals/backlog_details.md` (B-134 „Belege") **und** im Test-Docstring
`tests/uiLayout/test_group_flow.py:...test_damage_block_apply_mutates_before_render_returns_b134`,
liegt aber als *unversionierte* Datei vor (git status). Wird er nicht mitcommittet, dangeln beide
Beleg-Referenzen. → Beim Abschluss-`git add` einschließen (der Koordinator macht ohnehin `add -A`,
daher leichtgewichtig — hier nur als bewusste Kontrolle).

### Minor 1 — Dritte konvertierte Mutation (`_wound_adjustment_click`) ohne eigenen Regressionstest
`src/uiLayout/_common.py:317` (`_wound_adjustment_click`). Die beiden im Plan §0 benannten Stellen
(DAMAGE-Apply, Multi-Unit-Panel) haben je einen neuen Timing-/Verhaltens-Assert
(`test_group_flow.py` B-134-Test, `test_common.py` on_change/on_click-Asserts). Die *dritte*
mitkonvertierte Mutation (±Wunden-Buttons) hat **keinen** Test, der den Callback auslöst — `grep`
nach w-Button-Presses in `tests/uiLayout/` liefert 0 Treffer. Risiko niedrig (schlichte
`apply_damage`/`heal_unit`-Mutation, identische Wurzel), aber unter dem Test-Mandat eine kleine
Lücke. Empfehlung: 1-Zeilen-Assert in S184 nachziehen (nicht commit-blockierend).

### Minor 2 — number_input→Apply „tippen-ohne-Enter-dann-klicken"-Race (bewusster Streamlit-Tradeoff)
`src/uiLayout/_common.py:2978` (Apply-Button `args=(…, total, …)`). Mit `on_click` trägt der Button
`total`/`models_lost`/`mortal_wounds` aus dem **Render-Lauf**, in dem er erzeugt wurde. Tippt der
Nutzer einen neuen Wert ins Damage-`number_input` und klickt Apply, **ohne** vorher Enter/Blur
auszulösen, wendet der Callback für eine Interaktion den *Vor-Editier*-`total` an (die alte
Inline-Variante recomputete `total` im Klick-Lauf frisch). Für Stepper (Pfeiltasten — B-135-Thema)
und Enter-Commit greift der Fall nicht: dort committet jeder Wert per eigenem Rerun, der Button
trägt dann den frischen `total`, und Button-Label == angewandter Wert bleibt stets konsistent. Das
ist der kanonische Streamlit-Callback-Tradeoff und strikt harmloser als der behobene Stale-Bug.
Kein Blocker; nur Awareness — falls je gewünscht, ließen sich auch die Damage-`number_input`s auf
`on_change`-Seeding ziehen (Scope S184+, nicht jetzt).

---

## DoD-Punkte

1. **Regelkonform** ✔ — Mutation identisch; group_wounds-Zwangszuteilung weiter über
   `select_damage_target_group`/Priority-Spill (`_common.py:2748-2755`), Prioritäts-basierte
   Verlustzuteilung unverändert; `wounds_on_front`-Res-Feld war und bleibt hart 0 (nur in `total`
   gefaltet).
2. **Generisch** ✔ — keine neuen Fraktions-Strings in `src/`; die 4 neuen Callbacks enthalten
   keine; INV-4b unverändert 6/16/3 (bestehende Treffer nur in Kommentar-Beispielen).
3. **Tests grün** ✔ — `pytest tests/uiLayout/ -q --no-cov` = 531 passed; Regressionstests treiben
   `_render_damage_block`/`_render_explode_target_panel` (Render-Einstieg, nicht die isolierten
   Helfer) und lesen `front_group_hp` — die exakte UnitCard-Quelle; M3-Assert
   (`"Enter damage taken" in col.caption_calls`) vorhanden.
4. **Architektur-Gate** ✔ — Scoreboard grün, INV-4b/INV-4/INV-5 unverändert; keine bewusste
   Invarianten-Änderung nötig (reiner Callback-Umbau).
5. **Clean Code** ✔ — sprechende Callback-Namen, Docstrings erklären das *Warum* (Callback-Timing)
   mit Quellenverweis; keine Magie; pre-commit lt. Executor sauber.
6. **UI manuell verifiziert** ✔ — Executor-Playwright-E2E UnitCard 3/3 → 1/3 im selben Frame
   (Render-Code, per DoD-6 nicht test-gedeckt); Bauform §1.4.1 unverändert (keine sichtbare
   Layout-Änderung, nur Timing).
7. **Artefakte aktuell** ✔ — Backlog (B-134 Done S183 / B-135 ToDo + B-132-Kopplungsnotiz),
   `backlog_details.md`, `briefing.md`, `design_system.md` (M2) nachgezogen; 2 S182-Handoffs
   gelöscht; `grep "^STATUS:"` nur STANDING (Stakeholder_Beobachtungen) + NEEDS-APPROVAL
   (S183_PLANNING = aktueller Plan) — keine verwaisten DONE-Marker. Einschränkung: A1 (Beleg-
   Screenshot untracked).

## Design-System-Konformität
✔ §1.4.1-Schema (Header → Dmg/HP → Subgruppen-Selector → „Enter damage taken" → Zahlenfelder →
Mortal Wounds → Apply → Post-Apply) unverändert; Sub-Header in *beiden* Eingabepfaden gerendert
(`_common.py:2913` group_wounds, `:2937` non-group).
