# 0007 — Dünner persistenter Koordinator: Planung und Review ausgelagert, Stakeholder-Kanal über Datei

**Datum:** 2026-06-26
**Status:** angenommen

## Kontext

Der Orchestrator vereint heute Scrum-Master + Tech-Lead + Kontext-Hüter in **einem**
Opus-Fenster ([operating_model.md](../operating_model.md)). Die zwei tokenschwersten
Tätigkeiten — die Detail-**Planung** (Dateien lesen, Tasks schneiden) und das **Review**
(Diffs lesen) — leben genau dort und füllen das Fenster schnell. Verschärfend: der
ewige Zyklus Session öffnen/schließen/öffnen/schließen zwingt den Koordinator jedes Mal
zur **Neu-Orientierung**, bevor überhaupt Arbeit beginnen kann — reiner Overhead.

Die Recherche dieser Session (zwei read-only Subagenten) klärte die Harness-Grenzen:
**kein Subagent-Nesting**; **kein direkter Subagent↔User-Kanal**; die zurückgegebene
Subagent-Nachricht kostet den Koordinator **immer** Tokens; **aber** Subagenten können ihr
Ergebnis in eine Datei schreiben und nur den **Pfad** zurückgeben (verlängert
[ADR-0006](0006-subagent-grossausgaben-als-datei.md)), und ein Agent kann über viele
Delegationen **fortbestehen** (`SendMessage`, intakter Kontext). Betroffene Prämissen: 2
(Kommunikationswege) und 3 (Personal/Tier) — und die Grundprämisse „der Agent hört zwischen
Sessions auf zu existieren".

## Entscheidung

Vier gekoppelte Züge:

1. **Dünner, persistenter Koordinator.** Der Opus-Hauptthread wird ein dünner, langlebiger
   Koordinator: er routet Subagenten, hält die menschzugewandten Gates (Plan-Freigabe,
   Maßnahmen-Entscheid) und eskaliert. Er liest **bewusst keine** Quelldateien und **keine
   vollen** Subagent-Ergebnisse — nur Pfade + Status-Marker. So bleibt sein Fenster klein und
   überlebt über das hinweg, was bisher getrennte Sessions waren; die Neu-Orientierung entfällt.

2. **Kognition ausgelagert.** Detail-Planung → **Planner-Subagent**; finales Review →
   **Reviewer-Subagent** (Opus-Tier wegen Urteil). Executor (Sonnet) setzt um. Der Koordinator
   startet sie **flach und sequenziell** (Nesting unmöglich) und weckt sie per `SendMessage`
   mit intaktem Kontext wieder.

3. **Kanal-Regel gelockert — durchreichen statt urteilen.** Da es keinen direkten
   Subagent↔User-Kanal gibt, bleibt der Koordinator der einzige Transportweg — aber er reicht
   Befunde/Fragen **wortgleich, ohne zu urteilen** durch und nennt die **Herkunft** („Befund des
   Reviewer-Subagenten, von mir nicht nachgerechnet"). Das lockert die alte Regel (Koordinator
   mediiert + reviewt) zu (Koordinator transportiert + gated). Das Urteil lebt in den
   Opus-Subagenten, nicht im Router.

4. **Stakeholder-Kanal über Mailbox-Datei (asynchron).** Ein Subagent kann mitten im Lauf nicht
   blockierend auf den Stakeholder warten. Er schreibt seine Entscheidungsfrage in eine
   **Mailbox-Datei** (`docs/handoff/…`, Marker `STATUS: NEEDS-DECISION`) und **beendet seinen
   Lauf**. Der Koordinator legt sie dem Stakeholder vor; dieser antwortet (in der Datei oder über
   den Koordinator); der Koordinator weckt **denselben** Subagenten per `SendMessage`, der die
   Antwort liest und weitermacht. Ergebnis-Übergabe und Frage-Mailbox teilen die
   `docs/handoff/`-Konvention (README) — das erweitert ADR-0006 von „Ausgabe" auf
   **bidirektionale Übergabe**.

**Weiches Scoping:** Der Koordinator begrenzt das Lesen jedes Subagenten auf das Minimum — über
den **Vertrag** (erlaubte Pfade im Brief) plus den **Index** (`agent_scopes.md`). Eine harte
per-Subagent-Pfad-ACL zur Laufzeit gibt es nicht; Scoping ist Vertrags-Disziplin, kein Zaun.

## Konsequenzen

- **Schlanker, langlebiger Koordinator** → keine Neu-Orientierungs-Steuer; die 150k-Wand ist nicht
  mehr der Session-Taktgeber.
- **Höhere Gesamt-Token** (Multi-Agent grob 15×) — bewusster Tausch: Ziel ist ein Koordinator, der
  **nie an die Wand läuft**, nicht Token-Minimierung (`CLAUDE.md`: „nicht Token-Nullsumme"). Sehr
  kleine Tasks laufen bei einem bestehenden Agentenpaar mit, statt das volle Gespann zu zünden.
- **Stärkere Artefakt-Abhängigkeit:** Index (`agent_scopes.md`), Handoff/Mailbox-Konvention und
  saubere Briefs sind jetzt tragend, nicht Komfort.
- **Urteils-Herkunft wird explizit:** der Stakeholder weiß immer, ob ein Urteil vom Koordinator
  oder von einem Subagenten stammt.
- **Rollen werden komponierbar:** Prozess-Optimierer-/Beobachter-Subagenten lassen sich nach Bedarf
  ergänzen/entfernen, je mit eigenem Handoff-Ordner.
- Neues Roster + Kanal + Events stehen in `operating_model.md` (Delta dieser Session); Index =
  `agent_scopes.md`; Handoff-Lebenszyklus = `docs/handoff/README.md`.

## Bekannte Lücke / Review-Termin

- Die Harness-Fakten stammen aus der Agent-SDK-„Managed Agents"-Doku, **nicht 1:1 gegen unsere
  Claude-Code-CLI verifiziert**. **Pilot vor Verbindlichkeit:** einen echten Mailbox-Round-Trip
  (Subagent schreibt → Koordinator weckt per `SendMessage` → Subagent liest) durchspielen; erst wenn
  er trägt, gilt die Mailbox im Operating Model als verbindlich.
- Offen: ob das „wortgleiche Durchreichen" des Koordinators unter Druck ehrlich bleibt — Review
  nächste Retro.
