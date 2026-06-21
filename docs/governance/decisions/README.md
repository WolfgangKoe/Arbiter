# Entscheidungslog (ADR)

Konsens-Entscheidungen werden hier amnesie-fest dokumentiert — damit die Organisation in ihren Artefakten erinnert, nicht im Bewusstsein einzelner Agenten. Festgehalten wird das **Warum**, nicht nur das Was.

**Dateiname-Konvention:** `NNNN-kebab-titel.md`

---

## ADR-Vorlage

```markdown
# NNNN — Titel der Entscheidung

**Datum:** YYYY-MM-DD
**Status:** vorgeschlagen | angenommen | abgelöst

## Kontext

Welche Situation, welches Problem, welche Spannung hat diese Entscheidung ausgelöst?
Welche Optionen standen zur Wahl?

## Entscheidung

Was wurde entschieden? Kurz und präzise.

## Konsequenzen

- Was wird dadurch einfacher / sicherer?
- Was wird dadurch schwieriger / teurer?
- Welche Folgefragen entstehen?

## Review-Termin

Nächste Retrospektive — oder konkretes Datum, wenn absehbar.
```

---

## Einträge

| Nr | Titel | Status | Datum |
|---|---|---|---|
| [0001](0001-explizite-freigabe-beibehalten.md) | Explizite Freigabe für Probe-Session beibehalten | angenommen | 2026-06-18 |
| [0002](0002-stakeholder-artefakte-und-retro.md) | Stakeholder-Artefakte sind für den Leser; Retro fester Teil von Event 5 | angenommen | 2026-06-18 |
| [0003](0003-events-als-hooks-vollzogen.md) | Operating-Model-Events werden von der Harness vollzogen, nicht erinnert | angenommen | 2026-06-19 |
| [0004](0004-skill-fetch-nur-per-subagent.md) | Skill-/Claude-Inhalte über die API nur per Subagent ziehen | angenommen | 2026-06-20 |
| [0005](0005-stehende-subagent-freigabe.md) | Stehende Freigabe für Subagenten-Einsatz (verengt 0001) | angenommen | 2026-06-21 |
| [0006](0006-subagent-grossausgaben-als-datei.md) | Subagenten geben Großausgaben als Datei zurück (Permanent/Temporär-Konvention) | angenommen | 2026-06-22 |
