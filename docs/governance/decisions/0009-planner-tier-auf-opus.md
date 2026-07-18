# 0009 — Planner-Tier auf Opus (Lesedisziplin + Sonnet nur bei großen Schreib-Artefakten)

**Datum:** 2026-07-18
**Status:** angenommen

## Kontext

ADR-0008 hatte den Planner bereits nominell auf Opus belassen (Punkt 4: „Planner: Opus
bleibt."). In der Praxis driftete der Einsatz dennoch — S167 verbrauchte für die
Planner-Arbeit ~140k Sonnet-Tokens, nicht Opus. Der Stakeholder-Eindruck (S167): Sonnet
übersieht als Planner wichtige Dinge bzw. sieht sie nicht im größeren Zusammenhang —
Konzeption braucht ein stärkeres Modell.

**Befundlage (S166):** (a) Die B-123-Erstdiagnose folgerte „kein Bug" aus einem
UI-unerreichbaren Testpfad — fehlender Blick auf den Gesamtzusammenhang, wie die echte UI
den State aufbaut (Ratchet-Maßnahme M1). (b) Mockup V1 wurde abgelehnt, weil frei an der
Bestands-UI vorbei entworfen. Beides Muster „fleißig, aber nicht ganzheitlich" — deckt sich
mit dem Stakeholder-Eindruck. Gegenbeispiel S167: derselbe Sonnet-Planner fand einen
bestehenden Anker statt einen neuen zu eröffnen und empfahl Ratchet statt Big-Bang — die
Qualität streut, das Risiko liegt in den Sessions, in denen es schiefgeht.

**Kostenstruktur:** Der Tokenverbrauch der Planner-Arbeit entsteht überwiegend beim
**Lesen** des Kontexts (Briefing, Retro, Backlog, Specs, Checkbox-Sync), nicht beim
Schreiben (~200-Zeilen-Planning-Datei). Das ist der entscheidende Punkt für den
Team-Zuschnitt: ein Team aus Opus (konzipiert) + Sonnet (arbeitet aus) müsste die gleiche
Lektüre zweimal bezahlen — Sonnet braucht zum Ausarbeiten (Dateilisten, Token-Schätzungen,
Anker prüfen) dieselben Quellen erneut, dazu kommt Übergabeverlust Konzept→Plan. Bei einem
~200-Zeilen-Artefakt ist der eingesparte Opus-Schreibanteil klein gegen die doppelten
Lesekosten.

Geprüfte Optionen: (1) Team Opus (Konzept) + Sonnet (Ausarbeitung) als Default — verworfen,
s. o. (2) Planner komplett auf Opus, ein Lesedurchgang — gewählt. (3) Status quo + Opus-Review
vor Vorlage — verworfen, ein Review sieht nur, was im Plan *steht*; fehlende Zusammenhänge
(das eigentliche Problem) sind post-hoc am schwersten zu erkennen, gleiches Blindfeld wie bei
der B-123-Erstdiagnose.

## Entscheidung

**Planner-Tier = Opus als Default, durchgängig** (ein Lesedurchgang, Konzept und Plan aus
einer Hand). Zwei Auflagen dazu:

1. **Gezielt lesen, keine Volltext-Lektüre** — briefing.md, aktive Zieldatei, `backlog.md`
   und Index werden nach Scope-Zeile gezielt gelesen, nicht komplett am Stück.
2. **Sonnet-Ausarbeitung nur bei großen Schreib-Artefakten** (> ~300 Zeilen, z. B.
   Migrations-/Split-Dokumente): dort darf nach fertigem Opus-Konzept die Ausarbeitung an
   Sonnet delegiert werden — dort überwiegt der Schreibanteil, die Team-Trennung lohnt sich.

Umsetzungsort: `docs/governance/operating_model.md` (Abschnitt „Rollen & Model-Tier", MUST-
Klausel „Planner-Tier, S167") und `docs/reference/agent_scopes.md` (Pflichtschritte Planner).
Diagnose-Briefs mit „kein Bug"-Risiko (verwandt mit Ratchet M1/S166) bleiben eine offene
Folgefrage, nicht Teil dieser Entscheidung.

## Konsequenzen

- **Weniger Ganzheitlichkeits-Lücken erwartet:** Konzept und Plan aus einer Hand, kein
  Übergabeverlust zwischen Konzept- und Ausarbeitungs-Modell.
- **Höhere Token-Kosten pro Planning-Session:** Opus-Preisaufschlag auf die ohnehin nötige
  Lektüre. Gegengerechnet: die Folgekosten schlechter Pläne/Diagnosen (S130-403k-Vorfall;
  S166-Fehldiagnose inkl. Nachdiagnose-Session) fallen bei besserer Planqualität weg.
  Ist-Messung erst nach mehreren Opus-Planning-Sessions möglich.
- **Kein Team-Split als Default:** Der Doppel-Lektüre-Einwand gilt so lange, wie das
  Schreib-Artefakt klein bleibt (~200 Zeilen) — nur bei großen Schreib-Artefakten kippt die
  Rechnung zugunsten Sonnet-Ausarbeitung.
- **Folgefrage:** Ob die Lesedisziplin-Auflage („gezielt, kein Volltext") in der Praxis
  eingehalten wird oder der Opus-Lesedurchgang trotzdem in Breite ausufert, ist zu
  beobachten.

## Review-Termin

Nächste Retrospektive nach den ersten Opus-Planning-Sessions (Vergleich Tokenverbrauch +
Plan-Qualität gegen den S166/S167-Befund).
