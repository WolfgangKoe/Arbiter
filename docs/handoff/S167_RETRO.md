STATUS: NEEDS-DECISION

# S167 — Retro (Maßnahmen zur Entscheidung im S168-Planning)

Lebensdauer: bis Stakeholder-Entscheid im S168-Planning; gewählte Maßnahmen werden dort in
die kanonischen Artefakte überführt, danach Datei löschen. Nicht genannte Maßnahmen gelten
als verworfen (operating_model.md §ev1).

## Was gut lief

- Governance-Auftrag in einem Zug: Spec-first-Gate, Screenshot-Konvention, Diagnose-Ratchet
  und B-124-Ratchet sitzen alle am selben kanonischen Ort (`agent_scopes.md`) — der Planner
  fand den bestehenden Anker Punkt (c), statt einen zweiten Regelort zu eröffnen.
- Mockup V3 wurde in einer Iteration arbeitsfähig („damit sollten wir arbeiten können") —
  die Screenshot-/Bestandskomponenten-Konvention wirkt messbar (V1 abgelehnt → V2 positiv →
  V3 abgenommen mit Rest-Auflagen).
- Parallele Sonnet-Subagenten (Governance + Mockup) + Koordinator-Eigenanalyse
  (Planner-Tier) liefen ohne Kollision; Stakeholder-Feedback über Datei-Kommentare
  (Mockup-§h-Antwort, Vormerkung-Entscheid) hat den Chat-Roundtrip gespart.

## Was schief lief

- **Planner-Tier-Drift (Koordinator-Fehler):** ADR-0008 verlangte bereits Opus für den
  Planner — der S167-Planning-Entwurf lief trotzdem auf Sonnet (~140k). Der
  Stakeholder-Eindruck „Sonnet übersieht Zusammenhänge" hatte also einen Regelverstoß als
  Hintergrund, keine Regelungslücke. Jetzt zusätzlich per ADR-0009 geschärft (Opus
  durchgängig + Lesedisziplin; Sonnet-Ausarbeitung nur bei Schreib-Artefakten >~300 Zeilen).
- **Handoff-Marker-Lücke am Abschluss:** `S166_REVIEW.md` trug seit S166 einen ungültigen
  Status-Marker (`REVIEW`), weil die Datei beim S166-Abschluss erst NACH dem letzten
  Doku-Gate-Lauf entstand; der Koordinator hat den gleichen Fehler in S167 wiederholt
  (Vormerkung-Datei mit erfundenem Marker `RETRO-VORMERKUNG`). Beides erst durch den
  Gate-Lauf des Governance-Executors aufgefallen.

## Maßnahmen (nummeriert, entscheidbar)

1. **Tier-Abgleich beim Subagent-Start** (`docs/governance/operating_model.md`, Event 3):
   Der Koordinator gleicht das Tier jedes Subagent-Starts gegen die Rollen-Tier-Tabelle ab,
   bevor er startet; Abweichung nur mit expliziter Begründung im Chat. Verhindert die
   ADR-0008-Drift strukturell statt per Erinnerung. **Empfehlung: übernehmen.**
2. **Abschluss-Reihenfolge-Klausel** (`operating_model.md` Event 5): Der letzte
   `pytest tests/docs/ --no-cov -q`-Lauf erfolgt NACH Anlage aller Abschluss-Handoffs
   (Review-/Retro-Datei), unmittelbar vor dem Commit — Handoff-Dateien, die nach dem
   letzten Gate-Lauf entstehen, umgehen sonst das Hygiene-Gate (S166_REVIEW-Fall).
   In S167 bereits so praktiziert; Klausel macht es dauerhaft. **Empfehlung: übernehmen.**

## Sessionstand-Kurzfassung (für das S168-Planning)

- Review S167: **GO** (2018 passed, Coverage 99,14 %, Arch 8/8, Doku/Akzeptanz 25/25);
  K1 (V3-Auflagen kanonisch verankert) + K2 (Planning-Datei gelöscht) im Abschluss erledigt.
- Governance komplett: Spec-first-Gate (neue ODER geänderte UI-Bauform → erst Spec, dann
  Code), Screenshot-Konvention, Diagnose-Ratchet, B-124-Ratchet, ADR-0009 Planner=Opus.
- Explodes V3 abgenommen mit 3 Auflagen (kanonisch in B-028c1 + `S166_MOCKUP_EXPLODES.md`
  §h-Antwort); nächster Schritt §7-Spec-Überführung, dann B-028c1-Code.
- B-123 unangetastet (Budget-Check laut Plan) → erster Task S168, Grenzfall-Testmatrix-
  Auflage steht im Item.
