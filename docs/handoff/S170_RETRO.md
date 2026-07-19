STATUS: NEEDS-DECISION

# S170 — Retro (Maßnahmen zur Entscheidung im S171-Planning)

Lebensdauer: bis Stakeholder-Entscheid im S171-Planning; gewählte Maßnahmen werden dort in
die kanonischen Artefakte überführt, danach Datei löschen. Nicht genannte Maßnahmen gelten
als verworfen (operating_model.md §ev1).

## Was gut lief

- **Spec-first-Zyklus in einer Session komplett:** Vorlage (T2) → Stakeholder-Abnahme →
  Umsetzung (T4-aef) → Review-GO auf die Spec-Konformität — der S165–S169 eingeführte
  Prozess trug erstmals durch, ohne Ping-Pong.
- **Retro-M1 (Lösch-Grep) griff sofort:** T3 löschte 5 Screenshots mit dokumentiertem
  Voll-+Kurzname-Grep je Datei; kein verwaister Verweis (S169-Fehlerbild nicht wiederholt).
- **Session-Limit-Resume verlustfrei:** T7 wurde hart abgebrochen und per SendMessage mit
  intaktem Kontext fortgesetzt — Working-Tree-Prüfung zuerst, kein Doppel-Edit.
- **Mehrdeutigkeit über Mailbox geklärt:** Die Reset-Semantik-Frage ging als
  NEEDS-DECISION-Datei mit zwei Lesarten + Empfehlung an den Stakeholder — eine Runde,
  klare Entscheidung (Lesart A), sofort in §1.6 überführt.

## Was schief lief

- **Token-Schätzungen erneut ~2× über dem bereits ×1,5-korrigierten Budget:** T2 ~121k bei
  60k-Budget, T4-aef ~244k bei 120k-Budget. Das Muster S168/S169 besteht fort — der
  ×1,5-Faktor (Retro-M2 S169) reicht für test-/mock-lastige UI-Briefs nicht.
- **Koordinator-Korridor gerissen:** Session-Peak ~153k (> 150k), Kontext-Summarization
  nötig; Ursache: 7 Subagent-Endberichte + 3 Stakeholder-Kommentar-Runden in einer Session.
- **Review-NO-GO wegen stale Marker:** `S170_SPEC_ABNAHME.md` trug nach der Abnahme weiter
  `NEEDS-DECISION` — in-Session korrigiert (→ ANSWERED), aber vermeidbar.
- **Stakeholder-Kommentare über zwei Dateien verteilt** (Abnahme-Doc + Verifikationsdatei)
  erzeugten die Reset-Mehrdeutigkeit überhaupt erst — kostete eine Klärungsrunde.

## Maßnahmen (nummeriert, entscheidbar)

1. **Schätz-Kategorie „test-/mock-lastiger UI-Brief"** (`agent_scopes.md`
   Auftragsgrößen-Gate): Briefs, die Render-Code + Test-Mocks gemeinsam anfassen, erhalten
   Faktor **×2,5** (statt ×1,5) oder werden vor Vergabe gesplittet. **Empfehlung: übernehmen.**
2. **Marker-Wechsel bei Auswertung sofort** (`agent_scopes.md` Handoff-Lifecycle): Wertet
   der Koordinator eine kommentierte NEEDS-DECISION-Datei aus, setzt er im selben Zug den
   Marker (→ ANSWERED bzw. löschen) — nie erst am Session-Ende. **Empfehlung: übernehmen.**
3. **↺-Glyph nachziehen** (Review-Befund 2, minor): `st.button("Reset")` in
   `_common.py:674/687` ohne `↺` (§4.1 `SYM_RESET`); Mini-Fix in S171 zusammen mit der
   d-Umsetzung. **Empfehlung: übernehmen (S171, kein eigener Brief).**

## Offen für den Stakeholder (kein Maßnahmen-Entscheid)

- **UI-Verifikation Testfälle 4–7** (`S170_b2bc_ui_verifikation.md`, Nachtrag): playerArea-
  Layout, Panel-Breite, Phasenwechsel-Lifecycle, Reset-Position — App läuft auf :8501.
- Dein Checkpunkt-2-Kommentar („Reset bei Erfolg bringt mich nicht zum Multi-Unit-Panel")
  ist durch deine spätere Lesart-A-Entscheidung abgedeckt: diese Rückkehr ist der
  Nach-Confirm-Reset und kommt mit (d) in S171. Falls du es anders meintest, bitte melden.

## Sessionstand-Kurzfassung (für das S171-Planning)

- Review S170: **NO-GO → GO nach Marker-Korrektur** (1 Zeile); Gates: 2080 passed,
  Coverage 99,18 %, Arch 8/8, Doku/Akzeptanz 25, mypy 0.
- Geliefert: Retro-M1/M2 verankert, M3-Allowlist (Stakeholder), Spec-first a/d/e abgenommen,
  P-16-Screenshots → In-Spec-Diagramme (5 PNGs weg), Nacharbeiten b/c/a/e/f umgesetzt,
  Careen!-Backlog-Item, Handoff-Lifecycle (4 S169-Dateien weg).
- Nächstes (S171): Testfälle 4–7 verifizieren → B-028c1-Teilhaken; **d-Umsetzung**
  (Direkt-Apply + Nach-Confirm-Reset ins Panel, Lesart A, ~M) + ↺-Glyph; **T5/b3
  `auto_explode`-GO** (~M, Annihilation Barge im Roster vorhanden); Careen!; Spyder-Konzept.
