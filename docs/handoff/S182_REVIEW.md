STATUS: NEEDS-APPROVAL

# S182 Review — B-128(b) DAMAGE-Block-Vereinheitlichung

## Gesamturteil: GO

Alle DoD-Dimensionen (Code ↔ App ↔ Regeln ↔ Architektur ↔ Doku) erfüllt. D1–D3 sind
regelkonform, generisch und getestet; §1.4.1 sauber mit ASCII-Schema registriert; B-128
vollständig ohne Info-Verlust archiviert. Nur Minor/Nit-Befunde, keine Blocker. Der vom
Koordinator gemeldete Doku-Drift (Punkt 5) ist ein Nit, kein NO-GO.

## Befunde

### Blocker
Keine.

### Minor
- **M1 — Doku-Drift, Punkt-5-Einordnung (`docs/spec/design_system.md:154`):** Toter Verweis
  auf die gelöschte Datei `S181_B128b_mockup.md` („Begründung §2 in …, D4 unten"), OHNE
  Löschhinweis. Anders als Z. 192, die korrekt „— Datei danach gelöscht" annotiert. Da die
  D4-Begründung im Abschnitt selbst vollständig inline steht, ist der §2-Zeiger redundant +
  tot → **kein Info-Verlust**, aber inkonsistente Provenienz-Notation. Empfehlung (Follow-up,
  nicht abschlussblockierend): Z. 154 an Z. 192 angleichen („Datei gelöscht") oder den
  §2-Zeiger streichen, da D4 inline ist. **Einordnung: Nit/Minor, GO — kein NO-GO.**

### Nit
- **N1 — D3-Obergrenze konzeptionell lockerer als group_wounds-Pfad
  (`src/uiLayout/_common.py:2815`):** `max_value=def_unit.models_max` ist ein **statischer**
  Anfangswert, nicht die aktuell lebenden Modelle — eine bereits dezimierte Einheit könnte mehr
  „Models lost" eintragen als noch am Leben. Regelkonform als sichere Obergrenze (eine Einheit
  kann nie mehr Modelle verlieren als sie je hatte) und strikt besser als der vorherige
  unbegrenzte Zustand; konsistent mit dem statischen „Wounds on front (0–{wounds-1})"-Muster.
  Der group_wounds-Pfad kappt dagegen dynamisch bei `gw_total`. Vom Stakeholder so abgenommen.
  Keine Aktion nötig — nur als bewusste Divergenz vermerkt.
- **N2 — Test-Abdeckung group_wounds-Pfad (`tests/uiLayout/test_group_flow.py:709`):** Der
  neue Render-Pfad-Test deckt nur Pfad (ii) (Multi-/Einzel-Modell). Für Pfad (i) prüft der
  `_DmgColStub` das D1-Label indirekt (`label.startswith("Damage dealt")`), aber der
  D2-Sub-Header „Enter damage taken" im group_wounds-Pfad wird nicht explizit assertiert (die
  `caption`-Methode des Stubs verwirft ihr Argument). Beide sind Ein-Zeilen-Additionen; kein
  Regress-Risiko. Optionaler Follow-up.
- **N3 — briefing.md Screenshot-Zählung (`.claude/tasks/briefing.md`):** „2 behaltene
  Screenshots" genannt, `docs/handoff/` enthält aber 4 PNGs (`20-58-07`, `21-29-43`
  unerwähnt). Vorbestehend, nicht durch S182 eingeführt. Bei nächster Gelegenheit angleichen.

## Detailprüfung je DoD-Punkt

1. **Regelkonform (D3/D4):** D3 sichere Obergrenze — OK (s. N1). D4-Begründung sachlich korrekt
   gegen `core_rules.txt` (Z. ~1700 „5. Inflict Damage": „If a model … is destroyed, any excess
   damage inflicted by that attack is lost" + per-Modell-sequenzielle Zuteilung). Nicht-
   Invertierbarkeit für gemischte Untergruppen ist damit belegt. ✓
2. **Generisch (INV-4b):** Geänderte src-Zeilen enthalten keine Fraktions-Strings. INV-4b-Gate
   unverändert (6 Tokens/16 Fundstellen — vorbestehend, nicht durch S182 erhöht). ✓
3. **Design-System-Konformität:** §1.4.1 mit ASCII-Mini-Schema + D1–D4-Begründung registriert;
   D2 nutzt `caption` (gedämpft, nicht fett) konsistent in beiden Pfaden. ✓
4. **Test-Qualität:** `test_damage_block_multi_model_shows_subheader_and_caps_models_lost`
   treibt den echten Render-Einstiegspfad `_render_damage_block` durch (nicht isolierten
   Helfer), mit realistischem session_state, der das `applied`-Gate passiert; assertiert auf die
   tatsächlichen `number_input`-kwargs (`max_value == models_max`) und die Caption-Liste — keine
   Tautologie (S164-Lehre erfüllt). ✓ (Lücke: Pfad-i-Sub-Header, s. N2.)
5. **Doku-Drift:** s. M1 — Nit, GO.
6. **Artefakt-Hygiene:** B-128 vollständig nach `backlog_archive.md` migriert (D1–D4,
   Provenienz, Verifikations-Zeiger — kein Info-Verlust); Detailblock aus `backlog_details.md`
   entfernt; backlog.md neu sortiert + „Letzter Abgleich" gesetzt; briefing konsistent;
   S181-Handoffs gelöscht, `S182_B128b_verifikation.md` (AWAITING-VERIFICATION) sauber. ✓

## Gate-Stichprobe (verifiziert)
- `test_common.py`-Neutest + `test_group_flow.py`: 38 passed (`--no-cov`).
- Ledger (impl. ohne Test): 0. INV-Konsistenz: alle Testnamen existieren.
