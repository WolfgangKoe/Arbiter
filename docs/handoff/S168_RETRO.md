STATUS: NEEDS-DECISION

# S168 — Retro (Maßnahmen zur Entscheidung im S169-Planning)

Lebensdauer: bis Stakeholder-Entscheid im S169-Planning; gewählte Maßnahmen werden dort in
die kanonischen Artefakte überführt, danach Datei löschen. Nicht genannte Maßnahmen gelten
als verworfen (operating_model.md §ev1).

## Was gut lief

- **Erster ADR-0009-Vollzug:** Planner lief auf Opus (~112k, Lesedisziplin eingehalten);
  der Plan trug die ganze Session ohne Umplanung — B-123 komplett (T1 Haiku 44k, T2 Sonnet
  177k, T3 Sonnet 160k) plus §7-Entwurf (T4 Sonnet 110k) und Opus-Review (66k).
- **Datei-Kanal beidseitig:** Stakeholder beantwortete die T3-V-Checkpunkte inline in der
  Verifikations-Datei noch während der Session — kein Chat-Roundtrip; der Opus-Reviewer
  fand die Antworten und mahnte die Überführung an (Review-Pflicht-Korrektur).
- **B-123 fachlich sauber:** Regelgrundlage als wörtlicher T1-Extrakt (Zitate mit
  Zeilennummern), Fix generisch über `has_per_group_wounds()`/`priority` — kein
  Fraktions-String; Testmatrix + S166-Regression vorhanden; Stakeholder bestätigt
  Regelkonformität.

## Was schief lief

- **UI-Qualität nur „regelkonform, aber geil ist anders":** Hinweistext zu lang/übertrieben,
  Apply-Damage-Bereich weiter uneinheitlich, §1.4-Registrierung ohne Schema wenig
  aussagekräftig — die Design-System-Schuld (B-124) bleibt spürbar; Kritik ist als
  Backlog-Substanz erfasst (siehe Abschluss-Executor-Eintrag).
- **Classifier-Blockaden bei Routine-Kommandos:** `rm` (Handoff-Lifecycle) und `curl`
  (App-Health-Check laut Briefing-Pflicht) wurden vom Permission-Classifier abgewiesen;
  der App-Check der Session ist dadurch entfallen, das `rm` gelang erst im zweiten Anlauf.
- **Token-Schätzung T3:** ~100k geschätzt, ~160k tatsächlich (Render-Test-Fixture-Aufwand
  unterschätzt); T2 lag mit 177k/190k im Rahmen.

## Maßnahmen (nummeriert, entscheidbar)

1. **Bauform-Registrierung mit Pflicht-Schema** (`docs/reference/agent_scopes.md`,
   B-124-Ratchet-Klausel schärfen): Jede §1-Registrierung enthält eine schematische
   Mini-Darstellung (ASCII/Markdown) der Bauform, nicht nur Prosa — adressiert direkt die
   Stakeholder-Kritik „§1.4 enthält keine schematische Darstellung".
   **Empfehlung: übernehmen.**
2. **Wortlaut-Budget für UI-Hinweise** (`docs/spec/design_system.md`, Wortlaut-Familien):
   Hinweis-/Warntexte max. ein kurzer Imperativ-Satz, keine Regel-Paraphrase im UI —
   Regelbegründungen gehören in die Spec, nicht in den Hinweis. Bestehende Texte als
   Ratchet bei Berührung kürzen. **Empfehlung: übernehmen.**
3. **Bash-Allowlist für Session-Routine** (`.claude/settings.json` via
   `fewer-permission-prompts`/manuell): `rm docs/handoff/*` und
   `curl http://localhost:8501` freischalten, damit Handoff-Lifecycle und App-Health-Check
   nicht am Classifier hängen. **Empfehlung: übernehmen.**

## Sessionstand-Kurzfassung (für das S169-Planning)

- Review S168: **GO** (2032 passed, Coverage 99,18 %, Arch 8/8, Doku/Akzeptanz grün) mit
  Pflicht-Korrektur backlog_details B-123 (vor Commit erledigt).
- B-123 vollständig: Core-Spillover + Menhir-Lock (T2), UI-Hinweis-Split (T3), Stakeholder
  bestätigt Regelkonformität (T3-V inline) — Item archivierbar.
- §7-Explodes-Entwurf steht; **offene Entscheidung:** `S168_SPEC7_ABNAHME.md`
  (NEEDS-DECISION) — bei Abnahme Mockups löschen, B-028c1-Code für S169 frei (L → vorher
  in ≤M-Briefs splitten: Schema+Daten / Kachel-UI / auto_explode-GO).
- Neue Backlog-Substanz aus T3-V-Kritik: Hinweistext kürzen, Apply-Damage-Bereich
  vereinheitlichen (Design-System-Arbeit, Anker B-124).
