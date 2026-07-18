STATUS: NEEDS-DECISION

# S165 — Retro: Maßnahmen-Liste (Stakeholder wählt/gibt frei)

**Lebensdauer:** temporär — nach Stakeholder-Entscheid gewählte Maßnahmen in
Backlog/Specs überführen, Marker → `DONE`, Datei löschen (Sichtung Start S166).

## Was lief

- Alle 4 S164-Retro-Maßnahmen umgesetzt und verankert; Sichtbarkeits-Fix (Variante B,
  selektionsunabhängiger Scan, 5 Phasen) mit Erreichbarkeits-Tests und
  Vorher/Nachher-Stash-Beweis; alle Gates grün (2018 passed, 99,14 %, Arch 8/8, mypy 0).
- Diagnose-vor-Fix-Schnitt (1a/1b getrennt) und der Verifikations-Deckel haben
  funktioniert: keine dritte Nachbesserungsrunde, stattdessen nach Runde 1 die
  Fable-Direktanalyse mit fachlicher Neueinordnung (Explodes = Pflicht-Trigger).
- Review-Urteil **GO** — der fachlich falsche Zwischenstand ist ehrlich als
  Blocked/re-scoped dokumentiert, Infrastruktur bleibt verwertbar.

## Maßnahmen (nummeriert, entscheidbar)

1. **Definition of Ready + Refinement-Schritt (Stakeholder-Input S165, wörtlich
   aufgenommen):** Das Feld „Benötigte Regeln/Scopes" in `backlog_details.md` steht
   für gewöhnlich auf „-" — die ursprüngliche Absicht, schon bei der Item-Erstellung
   auf konkrete Regeln (Design-System-§, operating_model, Wahapedia) zu verweisen,
   wird ignoriert. Vorschlag: DoR als hartes Gate vor jeder Umsetzungs-Freigabe —
   (a) „Benötigte Regeln/Scopes" PFLICHT konkret befüllt (kein „-" bei Items mit
   Regel-/UI-Bezug); (b) Akzeptanzkriterien werden von einem Subagenten aus den
   lokalen Regelquellen erstellt und dem Item beigelegt; (c) Refinement-Fragen
   dokumentiert: Anforderung richtig verstanden? AK korrekt + vollständig?
   Stakeholder-Entscheid nötig? Ganzheitlich betrachtet (Code ↔ App ↔ Regeln ↔
   Architektur)? Verankerung: Feldschema in `backlog_details.md`, Planner-Pflicht in
   `agent_scopes.md`, DoR-Definition in `operating_model.md`. Bestehende aktive Items
   werden beim nächsten Anfassen nachgezogen (Ratchet, kein Big-Bang).
2. **Budget-Skala kalibrieren:** Schätzungen vs. tatsächliche Subagent-Tokens klafften
   um Faktor 5–10 (Task 0: XS ~5k geschätzt → ~50k tatsächlich; Task 1b: M ~20–25k →
   ~190k). Vorschlag: Schätzskala in `agent_scopes.md` explizit auf
   „Subagent-Gesamt-Tokens" umstellen und die S165-Ist-Werte als Referenzpunkte
   dokumentieren (XS≈50k, S≈100–120k, M≈190k+), damit Planner-Budgets real sind.
3. **Verifikations-Handoff-Vorlage erweitern:** Die Prüffragen fragten bisher nur
   Sichtbarkeit ab („erscheint die Karte?"), nie Interaktion und Design-Konformität.
   Vorschlag: Pflicht-Checkpunkte in jede Verifikations-Vorlage — „Ist die Interaktion
   regelkonform (optional vs. Pflicht)?", „Komponente + Anker laut design_system.md-§?",
   „Wortlaut-Familie korrekt?" (ergänzt den Reviewer-Ratchet aus S165 um die
   Stakeholder-Perspektive).
4. **Memory-Ergänzung `feedback_test_mandate` (offen aus S165, 2× unbeantwortet):**
   Ergänzung um den Erreichbarkeits-Beweis (Render-Einstiegspfad-Test mit realem
   `session_state`, S164-Lehre). Bitte hier explizit Ja/Nein entscheiden.

## Ergebnis (Stakeholder trägt hier ein)

