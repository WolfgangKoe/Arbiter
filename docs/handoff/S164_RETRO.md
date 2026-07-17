STATUS: NEEDS-DECISION

# S164 — Retro: Maßnahmen-Liste (Stakeholder wählt/gibt frei)

**Lebensdauer:** temporär — nach Stakeholder-Entscheid gewählte Maßnahmen in Backlog/Specs
überführen, Marker → `DONE`, Datei löschen (Sichtung typischerweise am Start von S165).

## Was lief

- T0 (Archivierung B-028b/B-119) und T1 (generischer mortal_wounds-Handler, 11 Tests) sauber;
  Review bestätigt Regelkonformität inkl. der infused_madness-Datenkorrektur.
- Parallelisierung (T0 ∥ T1) funktionierte konfliktfrei; NEEDS-DECISION-Mailbox-Zyklus
  (Datenlage-Befund → Entscheid → reduzierter Scope) lief innerhalb einer Session.
- Review-Urteil **NO-GO**, minimal-GO-Auflagen (Lint-Fix + ehrliches Re-Scoping von B-028c1)
  wurden vor dem Commit umgesetzt; der GO-kritische UI-Befund ist als offener Bug dokumentiert,
  NICHT als verifiziertes Feature eingecheckt.

## Maßnahmen (nummeriert, entscheidbar)

1. **S165-Top-Priorität: Vengeance-Sichtbarkeits-Bug** (Review-Befund 1). Untersuchungs-Lead
   liegt vor: beide Call-Sites hängen an Selektion/Zielung, zerstörte Einheiten sind aber nicht
   (neu) selektierbar (`unitCard.py:232`) → Sichtbarkeits-Anker von der Selektion entkoppeln
   (z. B. Karte an den zerstörten-Einheiten-Eintrag hängen). Handoff
   `S164_B028c1_ui_verifikation.md` (NEEDS-REWORK) enthält den Verlauf der 3 Runden.
2. **Budget-Profil für UI-Verdrahtungs-Tasks:** T2-Executor verbrauchte ~311k gegen ~20k Budget
   (Live-Verifikations-Schleife mit 3 Runden + Session-Limit-Abbruch/Resume). Vorschlag:
   UI-Verdrahtung und Live-Verifikation als getrennte Aufträge briefen, Verifikations-Runden
   deckeln (max. 2, dann zurück an Koordinator).
3. **Formatter-Pflichtschritt im Executor-Brief:** DoD 5 stand im Brief, wurde aber nicht
   ausgeführt (5× E501 + black-Diff). Vorschlag: „`black`+`ruff check` laufen lassen und
   Ergebnis im Bericht nennen" als expliziten letzten Schritt in jede Code-Brief-Vorlage in
   `agent_scopes.md` aufnehmen (analog Vollsuite-Klausel).
4. **Test-Mandat schärfen — Erreichbarkeits-Beweis:** Der isolierte Funktions-Test bewies nur
   „rendert bei destroyed=True", nicht dass die App den Zustand je erreicht (exakt so vom
   Review seziert). Vorschlag: für Render-Verdrahtungen zusätzlich einen Test verlangen, der
   den Render-Einstiegspfad (Spaltenfunktion → Gate-Bedingung) mit realem Session-State
   durchläuft; Formulierung in `feedback_test_mandate`/`agent_scopes.md` ergänzen.

## Ergebnis (Stakeholder trägt hier ein)

—
