STATUS: NEEDS-DECISION (Block A entschieden; Block C folgt beim S180-Abschluss)

# Retro S180 — Maßnahmen zur Entscheidung (Stakeholder wählt am nächsten Session-Start)

**Stakeholder-Entscheid Block A (2026-07-23, Session-Start Block B/C):**
M1 abgelehnt · M2 abgelehnt · M3 bestätigt — keine Änderung an `agent_scopes.md`.

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

## Block C (S180-Abschluss, 2026-07-23)

4. **M4 — Testroster-Lücke Mehr-Spender-Aura (Stakeholder-Anmerkung aus der B-131b-Verifikation):**
   `necrons_test.yaml` enthält nur einen Aura-Spender-Lord — der Mehr-Spender-Hinweistext
   („…of Lokhust Lord or Skorpekh Lord.") ist im Browser nicht verifizierbar, nur unit-getestet.
   Vorschlag: zweiten Spender (z. B. Lokhust Lord) in `necrons_test.yaml` oder ein eigenes
   Verifikations-Roster aufnehmen (reine Daten-Änderung, ~5k). → annehmen / ablehnen.
5. **M5 — Loader-Caching-Fundstelle (Review-Finding 2, Minor):** `get_wound_reroll_aura_donor_names`
   ruft ungecachtes `load_army` im Render-Hot-Path — konsistent mit bestehendem Muster
   (`get_unit_rp_reroll_ability`), kein Regress. Vorschlag: als Backlog-Item „Loader-Caching
   der Ability-Accessoren prüfen" aufnehmen (sonst bleibt es unadressiert notiert).
   → annehmen / ablehnen.
6. **M6 — Verifikation-im-Fluss (bewährt, keine Doku-Änderung):** Stakeholder füllte den
   AWAITING-VERIFICATION-Handoff noch während der laufenden Session; der Koordinator hat vor
   der Verwertung die Herkunft der Haken belegt (Executor legte Checkboxen leer an, [x] kam
   per IDE-Edit 17:36) und die Verifikation noch in S180 integriert. Nur Bestätigung.

   Entscheidung: Wir übernehmen Maßnahme M4.

   Ergänzung: Bitte prüfen, welche Screenshots im Handoff noch relevant sind. Meines Erachtens möchte ich nur noch folgende Screenshots behalten:
   ![alt text](<Bildschirmfoto vom 2026-07-09 21-29-43.png>)
   ![alt text](<Bildschirmfoto vom 2026-07-09 20-58-07.png>)

   Die übrigen scheinen aus meiner Sicht erstmal gelöst oder aktuell nicht relevant zu sein. 
