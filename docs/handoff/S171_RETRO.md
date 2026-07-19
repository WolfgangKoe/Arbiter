STATUS: NEEDS-DECISION

# S171 — Retro (Maßnahmen zur Entscheidung im S172-Planning)

Lebensdauer: bis Stakeholder-Entscheid im S172-Planning; gewählte Maßnahmen werden dort in
die kanonischen Artefakte überführt, danach Datei löschen. Nicht genannte Maßnahmen gelten
als verworfen (operating_model.md §ev1).

## Was gut lief

- **×2,5-Faktor (Retro-M1 S170) hat kalibriert:** d1 ~148k und d2 ~166k bei je 180k-Budget —
  erstmals seit S168 kein Budget-Riss bei test-/mock-lastigen UI-Briefs; der alte ×1,5-Faktor
  (~108k) wäre erneut gerissen. Faktor beibehalten.
- **d-Split (d1 State / d2 Render) trug:** klare State-API-Übergabe (Snapshot-Keys,
  Funktionsnamen) im d1-Bericht machte d2 reibungslos; kein Doppel-Edit am selben File.
- **Session-Limit-Abbruch verlustfrei:** T4 wurde vom Session-Limit gekappt und per
  SendMessage mit intaktem Kontext fortgesetzt (S137-Regel), Working-Tree-Prüfung zuerst.
- **Royal-Warden-Frage im Planning selbst geklärt** (kein eigener Recherche-Brief):
  kein Bug — D6 Mortal Wounds pro Einheit, Beleg `unit_abilities.yaml:392`.
- **T4-Downgrade Sonnet→Haiku** (format-fixe Handoff-Datei): ~34k statt geplanter ~90k —
  Haiku-Default-Regel griff auch gegen die Plan-Vorgabe.

## Was schief lief

- **Review-NO-GO durch falsche M2-Anwendung des Koordinators:** Die frisch verankerte
  Maßnahme „Marker-Wechsel sofort" wurde auf `ANSWERED` ausgelegt, obwohl der letzte Punkt
  (d) erst umgesetzt, nicht verifiziert war — der Hygiene-Wächter verbietet liegende
  ANSWERED-Dateien → Vollsuite rot. In-Session korrigiert (→ AWAITING-VERIFICATION),
  aber die M2-Formulierung lässt den Zielmarker bei Teil-Auswertung offen.

## Maßnahmen (nummeriert, entscheidbar)

1. **M2-Schärfung** (`agent_scopes.md` Handoff-Lifecycle): Beim Sofort-Marker-Wechsel gilt —
   `ANSWERED`/`DONE` nur, wenn die Datei im selben Abschluss gelöscht wird; bleibt ein
   Teilpunkt offen, Marker `AWAITING-VERIFICATION` mit Auswertungsnotiz in Zeile 1.
   **Empfehlung: übernehmen (XS, Doku-Einzeiler).**
2. **PLANNING-Datei-Lifecycle kodifizieren** (`agent_scopes.md` Handoff-Lifecycle):
   `S<N>_PLANNING.md` wird nach Umsetzung + Review im **selben Abschluss** gelöscht
   (Entscheide leben in briefing/backlog) — nicht mehr bis zur Folgesession liegen lassen.
   S171 so praktiziert. **Empfehlung: übernehmen (XS).**

## Offen für den Stakeholder (kein Maßnahmen-Entscheid)

- **UI-Verifikation Nacharbeit d** (`S171_d_ui_verifikation.md`, 6 Testfälle): Direkt-Apply,
  Undo, Nach-Confirm-Reset (dein Testfall-7-Punkt), Sort-to-top, ↺-Glyph, Phasenwechsel —
  App läuft auf :8501. Bei Grün: alle drei Verifikationsdateien (S169/S170/S171) löschen
  + B-028c1-Teilhaken d.

## Sessionstand-Kurzfassung (für das S172-Planning)

- Review S171: **NO-GO → GO nach Marker-Korrektur** (2 STATUS-Zeilen); Gates: 2101 passed,
  Coverage 99,19 %, Arch 8/8, Doku/Akzeptanz 25, mypy 0, black/isort/ruff sauber.
- Geliefert: Retro-M1/M2 (S170) verankert; B-028c1-Nacharbeit **d komplett umgesetzt**
  (Direkt-Apply + Undo-Snapshots, Nach-Confirm-Reset Lesart A, Sort-to-top, ↺-Glyph auf
  allen 4 Reset-Buttons; 22 neue Tests, 2 Alt-Tests begründet an Spec angepasst);
  Royal-Warden-Antwort; Handoff-Cleanup (S170_PLANNING/S170_RETRO/S171_PLANNING weg).
- Nächstes (S172): d-Verifikation auswerten → ggf. Teilhaken; **T6/b3 `auto_explode`-GO**
  (~M, vertagt aus S171); **B-122 „Careen!"** (XS–S); Spyder-Konzept; Retro-Maßnahmen 1–2.
