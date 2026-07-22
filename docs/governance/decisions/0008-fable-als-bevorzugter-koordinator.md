# 0008 — Fable als bevorzugter Koordinator

**Datum:** 2026-07-02
**Status:** angenommen — **Teilweise abgelöst durch [ADR-0010](0010-koordinator-tier-opus-fable-nicht-verfuegbar.md)
(Koordinator-Tier, Fable derzeit nicht verfügbar).** Der Rest dieser ADR (Reviewer-,
Planner-, Executor-Tiering, Konsens-Punkt 2) bleibt gültig.

## Kontext

Mit der Verfügbarkeit von **Claude Fable 5** (Mythos-Klasse, kapazitiv **über** Opus)
stellt sich die Prämisse-3-Frage, wo das neue Top-Tier im Rollenmodell sitzt. Der
Stakeholder hat entschieden, dass Fable integriert werden soll (S117), und Fable
selbst um die Rollen-Einschätzung gebeten.

Das bestehende Tiering-Prinzip gibt die Richtung vor: *„Je offener das Zweckprogramm /
je mehr Sinn, Generic-src-Urteil, Stakeholder-Abgleich → desto höher das Tier."*
Optionen waren: (a) Fable überall zulassen, (b) Fable nur als Koordinator-Option
(„gleichwertig zu Opus"), (c) Fable gezielt dort **präferieren**, wo das offenste
Urteil sitzt, und sonst die Kosten-Disziplin (O2) unverändert lassen.

## Entscheidung

Option (c) — Fable wird gezielt an der Urteilsspitze präferiert:

1. **Koordinator-Sitz: Fable präferiert, sofern verfügbar; Opus als Fallback.**
   Begründung: Der Koordinator ist per ADR-0007 *dünn* (kleines Token-Volumen →
   Premium-Tier konzentriert sich dort, wo pro Token am meisten Urteilsqualität
   anfällt), *nicht delegierbar* (Qualität ist nicht durch Subagenten-Fan-out
   ersetzbar) und trägt die offensten Programme (Gates, Entscheidungsmodi,
   Eskalation, Retro, Maßnahmen-Entscheid).
2. **Prämissen-/Verfassungsänderungen und Konsens-Entscheidungen** wandern in der
   Tiering-Tabelle von Opus zu **Fable** (sie laufen ohnehin im Koordinator-Sitz).
3. **Reviewer: Opus bleibt Default.** Der DoD-Review ist ein halb-geschlossenes
   Programm (7 messbare Punkte); jeder Befund wird ohnehin vom Koordinator
   durchgereicht und vom Stakeholder gegengeprüft. **Ausnahme:** Reviews mit
   Prämissen-/Architektur-Urteil (Invarianten-Änderung, ADR-relevante Befunde)
   dürfen auf Fable gehen — mit expliziter Begründung im Auftrag (O2-Mechanik).
4. **Planner: Opus bleibt.** Das Prioritäten-Urteil ist durch Backlog/Zieldatei
   stark gebunden; die eigentliche Entscheidung fällt am Freigabe-Gate.
5. **Executor / Recherche / Beobachter / Artefaktpflege: unverändert**
   (Sonnet/Haiku) — geschlossene Konditionalprogramme, O2-Kostenprinzip.

**Reporting:** Fable wird in den Metrik-Artefakten als eigenes Tier ausgewiesen
(Symbol `▚` im Modell-Mix von `tools/token_report.py`), nicht als „sonstige".

## Konsequenzen

- **Mehr Urteilsqualität am Engpass:** Die nicht delegierbare Rolle bekommt das
  stärkste Modell; der Kosteneffekt ist nahe null, weil die Token-Masse
  (Subagenten) auf Haiku/Sonnet/Opus bleibt.
- **Tiering-Leiter bleibt konsistent:** Haiku → Sonnet → Opus → Fable folgt
  unverändert dem Offenheits-Prinzip; O2-Default (Haiku) und Begründungspflicht
  nach oben gelten weiter.
- **Verfügbarkeits-Abhängigkeit:** Ist Fable nicht verfügbar, arbeitet Opus als
  Koordinator ohne Prozessänderung weiter.
- **Folgefrage:** Ob Fable-Reviews bei Prämissen-Themen messbar bessere Befunde
  liefern als Opus, ist unbelegt — beobachten, nicht vorab ausweiten.

## Review-Termin

Nächste Retrospektive nach dem ersten Fable-Review-Einsatz (Ausnahme-Fall Punkt 3).
