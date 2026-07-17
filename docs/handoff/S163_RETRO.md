STATUS: NEEDS-DECISION

# S163 — Retro

## Maßnahmen-Liste

1. **M1:** Backlog-Item anlegen — Conditions-Auswertung in `find_unit_ability_by_effect`
   (`conditions: [has_rules: [gloom_prism]]` ist aktuell inert; optionales Wargear korrekt
   modellieren; Review-Befunde 1+2).
2. **M2:** Backlog-Schuld aufnehmen — `load_deny_wargear_names` in `loader.py` ist toter
   Produktionscode (nur Tests referenzieren); entfernen oder ersten echten Nutzer benennen
   (Review-Befund 3).
3. **M3:** Executor-Klausel in `agent_scopes.md` verankern — Selbstprüf-Suite im VORDERGRUND
   ausführen, Turn nie mit laufendem eigenem Hintergrund-Task beenden (Anlass: T1-Executor
   S163 brauchte zwei Weckrufe).
4. **M4 (bereits erledigt in S163, nur Kenntnisnahme):** Vollständige-Planung-Klausel
   verankert (agent_scopes.md + Briefing).
5. **M5:** Reviewer-Marker-Konvention klären: `STATUS: GO/NO-GO` kollidiert mit der
   Handoff-Allowlist (S163-Befund). Optionen: (a) Urteil künftig nur im Dateikörper, Datei
   nach Durchreichen löschen (S163 so praktiziert), oder (b) GO/NO-GO in Allowlist + README
   aufnehmen. Entscheid Stakeholder.

Entscheid des Stakeholders bei Session-Start S164; nur freigegebene Maßnahmen werden umgesetzt.
