STATUS: ANSWERED

# S141 — Ganzheitlicher DoD-Review (Reviewer-Subagent, Opus, read-only)

Geprüft: Commits `42af867`, `292b3ad`, `cdb55e2`, `f36f1e7`, `7fc8b16`, `cbaeeb2`
gegen die DoD (CLAUDE.md „Definition of Done"). Basis: Diffs (`git show`),
Regeltexte, Specs, Artefakte. Keine Testausführung (Stand: 1783 passed / 99,15 % /
mypy-Baseline 28 grün laut Sessionstand).

## Gesamt-Verdikt: **GO-mit-Auflagen**

Die drei Verhaltensänderungen (FixA Emergency Disembark, FixB Movement-Timing, B12b-Suffix)
sind regelkonform, generisch, jeweils mit einem ohne-Fix-roten Regressionstest belegt und
sauber geschnitten. Blocker: keine. Zwei echte Doku-Drift-Befunde + eine Handoff-Lifecycle-
Spannung sind vor dem Abschluss-Commit zu bereinigen.

## DoD-Punkte

1. **Regelkonform — GO.** Emergency Disembarkation greift laut `core_rules.txt` „when a
   TRANSPORT model is destroyed"; FixA (`f36f1e7`) reicht `unit_for_conditions=unit` durch,
   damit das TRANSPORT-Keyword-Gate auflöst statt die Box zu verstecken — regelkonform.
   FixB (`7fc8b16`) und B12b sind reine GO-Zustands-/Anzeige-Logik (used_elsewhere unabhängig
   vom eigenen Advance-Choice) — konsistent mit „Stratagem einmal pro Phase".
2. **Generisch — GO.** Kein neuer Fraktions-String/-Check in `src/` über alle Commits
   (grep auf hinzugefügte `src/`-Zeilen leer). Fraktionsdaten (Evil Sunz, Gunwagon) liegen
   korrekt in `data/rosters/orks_transport.yaml`. mypy-Commits sind reine Typ-Annotationen
   (`dict`→`MutableMapping`, `# type: ignore[type-arg]`-Abbau).
3. **Tests — GO.** Jeder Fix hat einen verhaltensbeschreibenden Regressionstest, der ohne
   Fix rot wäre: FixA `test_pending_transport_destroyed_box_visible_through_real_conditions_gate`
   (fährt den ungemockten conditions-Gate-Pfad); FixB
   `test_advance_reroll_state_used_elsewhere_before_advance_chosen` (pinnt die korrigierte
   Prioritätsreihenfolge); B12b deckt alle drei Mapper + `go_card_html` + Randfälle
   (kein unit_key, unauflösbarer key) ab.
4. **Architektur-Gate — GO (lesend).** Keine Änderung an `tests/architecture/`; die drei
   Zustands-Mapper bleiben laut Docstring/Diff pure, Streamlit-freie Entscheidungsfunktionen,
   die Wortlaut-Formatierung sitzt in `go_card.py` (Format-Trennung gewahrt). Kein neuer
   Layer-Verstoß in den Diffs. Nicht ausgeführt (Stand grün) — als n/a-Rest vermerkt.
5. **Clean Code — GO.** Sprechende Namen (`stratagem_used_elsewhere_unit_name`); Docstrings
   mit Spec-Verweis (§6.1) + Warum, keine neuen Erklär-Kommentare im Code. Docstrings sind
   sehr ausführlich, aber zulässig (öffentliche API / Warum). Kosmetik, keine Auflage.
6. **Artefakte — GO-mit-Auflagen.** backlog: B12b als ✅ verdrahtet markiert, Restpunkte
   offen — gut. `next_session.md` ist aktualisiert, aber **uncommittet** (erwartbar, gehört
   in den Abschluss-Commit). Spannung: `group_a`/`group_b`-Handoffs sind `ANSWERED` und laut
   Kopfzeile „am Session-Ende löschen", tragen aber noch die FixC/FixD/Insassen-Fix-Orte,
   auf die `next_session.md` (S142) verweist → Auflage 3.
7. **Doku-Drift — NO-GO (2 Befunde, behebbar).**
   - `design_system.md` §6.1 Zeile 184 behauptet weiterhin, der B12b-Suffix sei „noch nicht
     verdrahtet (Ratchet-Schuld S139 B12b)" — S141 (`cdb55e2`) hat ihn verdrahtet. Spec
     widerspricht Code.
   - `backlog.md` Zeile 252 verweist auf `docs/handoff/S141_planning.md` „Aufgabe 4" — diese
     Datei existiert nicht mehr (nie committet, in `61a4e19` verworfen). Toter Verweis.

## Auflagen (nummeriert, vor Abschluss-Commit)

1. `design_system.md` §6.1 Zeile 184: „Ratchet-Schuld … noch nicht verdrahtet"-Passage
   entfernen/umschreiben — Suffix ist seit `cdb55e2` verdrahtet (die drei Mapper geben jetzt
   den Einheitennamen als Grund zurück).
2. `backlog.md` Zeile 252: toten Verweis auf `S141_planning.md` auflösen — den B13-Detailinhalt
   (Schema+Loader+Daten in einem Aufwasch) inline in den Backlog ziehen statt auf eine
   gelöschte Datei zu zeigen.
3. Handoff-Lifecycle: bevor `group_a`/`group_b` am Session-Ende gelöscht werden, die
   FixC/FixD- bzw. Insassen-Fix-Orte in `backlog.md` überführen, damit der `next_session.md`-
   Verweis nicht ins Leere zeigt (DoD Punkt 7: Erkenntnisse überführen, dann löschen).
4. (Hygiene) `next_session.md` mit in den Abschluss-Commit nehmen — aktuell einziger
   uncommitteter Baum-Rest.

## Nicht geprüft (n/a)
- Testsuite/Architektur-Wächter nicht ausgeführt (Sessionstand grün; Diffs zeigen keine
  Wächter-berührenden Änderungen).
- UI-Render manuell: FixA/FixB laut Auftrag stakeholder-verifiziert (positiv); B12b-Suffix
  und Klan-Affinität am Ork-Transport-Roster bleiben offene manuelle Verifikation (backlog §3),
  korrekt als offen geführt.
