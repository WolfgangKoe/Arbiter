STATUS: NEEDS-DECISION

# Retro S180 — Maßnahmen zur Entscheidung (Stakeholder wählt am nächsten Session-Start)

## Block A (S179-Abschluss, 2026-07-23)

1. **M1 — Budget-Profil für Verifikations-Integration (Korrektur):** Der A1+A2-Doku-Brief
   (Log-Einträge + Backlog-Archivierung, Haiku) verbrauchte real ~114k Token gegen ~25k Budget.
   Das S172-Budget-Profil (~100k für Backlog-Archiv-Verschiebungen) existierte, wurde beim
   Bündeln mit den Log-Einträgen aber nicht angewendet. Vorschlag: In `agent_scopes.md` das
   S172-Profil explizit auf den Brief-Typ „Verifikations-Integration (Log + Archiv)" ausweiten.
   → annehmen / ablehnen.
2. **M2 — Vollsuite-Läufer-Muster (bewährt):** Der pytest-Foreground-Hook fing den
   Koordinator-Hintergrund-pytest korrekt ab; die kombinierte Vollsuite lief stattdessen per
   `SendMessage` in einem bereits fertigen (idlen) Haiku-Executor synchron im Vordergrund —
   S173-M2-konform, ~5k Token statt Koordinator-Kontext. Vorschlag: als Standard-Muster in
   `agent_scopes.md` festhalten („Kombinierte Vollsuite: idlen Executor per SendMessage
   wiederverwenden"). → annehmen / ablehnen.
3. **M3 — Parallel-Doku-Executoren (bewährt, keine Doku-Änderung):** Zwei Haiku-Executoren
   liefen parallel auf disjunkten Handoff-Dateien; transiente Cross-Scope-Gate-Failures wurden
   regelkonform gemeldet statt gefixt (S162-Regel hielt). Kein Handlungsbedarf, nur Bestätigung.

## Block C (S180-Abschluss)

_Wird nach Block B/C ergänzt._
