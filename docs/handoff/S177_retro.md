STATUS: NEEDS-DECISION

# Retro S177 — Maßnahmen zur Entscheidung (Stakeholder wählt am S178-Start)

1. **R1 — Subagent-Ausfall-Wiederaufnahme (bewährt):** T4 brach am Session-Limit mitten in
   5-teiliger Doku-Korrektur ab; Koordinator verifizierte Teil-Stand per git/grep und briefte nur
   den Rest (C/D/E) neu — kein Doppel-Edit. Vorschlag: als Muster in `agent_scopes.md` festhalten
   („bei Subagent-Abbruch: Teil-Stand verifizieren, nur Rest neu briefen"). Empf. annehmen.
2. **R2 — Parallel-Split auf disjunkten Dateien (bewährt):** T2a/T2b liefen parallel konfliktfrei
   (getrennte Dateisets), Zeitgewinn. Muster beibehalten, keine Doku-Änderung nötig.
3. **R3 — „In Progress/laufend"-Wildwuchs prüfen:** B-007 („Backlog-Restrukturierung", In
   Progress) steht noch als laufendes Item — prüfen, ob abschließen/archivieren (analog
   B-024/B-124) oder zur Regel. Für S178-Planner.
