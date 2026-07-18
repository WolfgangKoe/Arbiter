STATUS: NEEDS-DECISION

# S166 — Retro (Maßnahmen zur Entscheidung im S167-Planning)

Lebensdauer: bis Stakeholder-Entscheid im S167-Planning; gewählte Maßnahmen werden dort
in die kanonischen Artefakte überführt, danach Datei löschen. Nicht genannte Maßnahmen
gelten als verworfen (operating_model.md §ev1).

## Was gut lief

- Mockup-Iteration über Stakeholder-Screenshots: V1 (frei entworfene Komponenten) wurde
  abgelehnt, V2 (streng an Screenshot-Bestandskomponenten) „passt deutlich besser" —
  Screenshots als verbindliche Referenz sind wirksamer als Spec-§-Verweise allein.
- Die manuelle UI-Verifikation (B-122) hat einen echten, durch Tests verdeckten Bug
  aufgedeckt (B-123-Kern) — der DoD-Punkt 6 zahlt sich messbar aus.
- Nachdiagnose mit Scratchpad-Repro gegen die echten Funktionen (statt nur Testzitate)
  hat den Widerspruch in einem Durchgang aufgelöst und die Erstdiagnose korrigiert.

## Was schief lief

- **Erstdiagnose B-123 zog „kein Bug" aus einem UI-unerreichbaren Testpfad:** Die als
  Beweis zitierten Tests (`_sk_session()` ohne `damage_active_group_id`) simulieren einen
  Zustand, den die echte UI für Mehrgruppen-Einheiten praktisch nie erzeugt. Die
  Empfehlung (nur UI-Hinweis) wäre am echten Bug vorbeigegangen — erst der
  Stakeholder-Praxistest hat das aufgedeckt.
- Session musste wegen vollem Koordinator-Kontext hart geteilt werden (Decision-Handoff
  über Dateien hat aber funktioniert).

## Maßnahmen (nummeriert, entscheidbar)

1. **Diagnose-Ratchet „UI-Erreichbarkeit des Beweispfads"** (`docs/reference/agent_scopes.md`,
   Diagnose-/Verifikations-Brief-Pflichten): Eine „kein Bug / bereits regelkonform"-
   Schlussfolgerung ist nur zulässig, wenn die Repro den echten Klickpfad nachstellt —
   d. h. den Session-State so aufbaut, wie die UI ihn erzeugt (inkl. Selector-Defaults),
   nicht nur bestehende Unit-Tests zitiert.
2. **Grenzfall-Test-Auflage für Flag-Zweige in den B-123-Brief (S167):** Der Fix-Auftrag
   muss die Testmatrix directed×resolved×locked×mortal mit dem Grenzfall
   „Schaden > Gruppen-Restpool" abdecken (die Lücke, die den Bug verdeckt hat:
   `test_directed_damage_reduces_only_chosen_group` schöpft die Gruppe nie aus).
   Kein separater Big-Bang-Testdurchgang — nur als Auflage im Umsetzungs-Brief.
3. **Screenshot-Konvention für UI-Mockup-Briefs** (`agent_scopes.md`, Mockup-Gate-Zeile):
   UI-Mockup-Briefs referenzieren konkrete App-Screenshots (Stakeholder-Vorlage oder
   selbst erstellte) als verbindliche Bauform-Referenz, zusätzlich zu den
   design_system-§-Zitaten.

## Sessionstand-Kurzfassung (für das S167-Planning)

- Review S166: **GO** (2018 passed, Coverage 99,14 %, Arch 8/8, Doku/Akzeptanz 25/25).
- B-122 erledigt (Menhir-Wounds 5, UI bestätigt). B-123: Root Cause verifiziert
  (`_apply_directed_group_damage` verwirft Überschuss an Subgruppengrenzen; UI erzwingt
  diesen Zweig), Stakeholder-Richtung liegt vor (Subgruppen-Logik vereinheitlichen,
  Menhirs initial gelockt — kein pauschaler Spillover), Umsetzung S167.
- Explodes-Mockup V2 „passt deutlich besser"; 7 Korrekturwünsche für V3 in
  `S166_MOCKUP_EXPLODES.md` §g; B-028c1 bleibt Blocked bis V3-Abnahme.
