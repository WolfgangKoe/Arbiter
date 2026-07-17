STATUS: NEEDS-DECISION (Stakeholder: Maßnahmen übernehmen/ergänzen/streichen — Entscheid zu Beginn S157, Vorgabe S156)

# S155-Retro (nachgeholt in S156) — Maßnahmenliste

Grundlage: Retro-Input aus `docs/handoff/S156_review.md` (Reviewer Opus, Urteil GO).
Moderation: Koordinator. Nummerierte, einzeln entscheidbare Maßnahmen:

## Maßnahmen

1. **Keine eingefrorenen Testzahlen mehr im Briefing** (aus Beobachtung 3, Drift 1880→1881):
   `.claude/tasks/briefing.md` nennt künftig nur „Gates grün (Datum)"; die exakte Zahl wird
   ausschließlich aus dem Abschluss-Vollsuite-Lauf unmittelbar vor dem Briefing-Update
   übernommen, nie aus Zwischenläufen. — *Aufwand: 0, reine Schreibregel.*

2. **Fester Lösch-Auslöser für Handoffs** (aus Beobachtung 5, `S154_planning.md` hing nach):
   Abschluss-Routine bekommt einen festen Schritt „alle Handoffs löschen, deren
   Lifecycle-Bedingung erfüllt ist" — direkt nach dem Review-GO, vor dem Commit.
   Verankerung: eine Zeile im Abschluss-Event des `operating_model.md`.
   — *Sofort-Vollzug: `S154_planning.md` wurde in S156 gelöscht (Bedingung „nach
   S155-Review" erfüllt, vorautorisiert durch die bestehende Lifecycle-Zeile).*

3. **Docstring-Länge: keine neue Regel** (aus Beobachtung 4): Empfehlung, es beim
   bestehenden Kommentar-Ratchet zu belassen (Straffung bei nächster Modulberührung).
   Alternative, falls gewünscht: Stilzeile „Docstrings ≤ ~5 Zeilen, Details in die Spec"
   in CLAUDE.md. — *Empfehlung: keine Maßnahme.*

4. **Beibehalten (keine Maßnahme):** R3-Regel (Review nachholen als Punkt 0) und das
   Muster „Fix + Zusatzbefund sofort als Backlog-Item" (B-102) haben sich bewährt
   (Beobachtungen 1+2).

Lifecycle: Stakeholder markiert je Maßnahme übernehmen/ändern/streichen → Marker auf
ANSWERED; Verankerung der übernommenen Maßnahmen als erster Schritt der Folgesession,
Datei danach löschbar (DONE).

---

## S156-Retro — Maßnahmen (Stakeholder-Input + Review)

Grundlage: Stakeholder-Kommentare aus `docs/handoff/S155_ui_verifikationen.md` (Datei nach
S156-Übernahme gelöscht, Inhalt hier + in den betroffenen Backlog-Items archiviert) und
Retro-Input aus `docs/handoff/S156_review.md`. Nummerierung setzt an Maßnahme 4 (oben) an.

5. **UI-Verifikations-Template festlegen (VOM STAKEHOLDER VORGEGEBEN):** jede Verifikation
   nennt (a) Voraussetzungen — welches Roster, wie erreiche ich den Zustand in der App;
   (b) präzise Schritte — nicht „Fight Phase erreichen", sondern der konkrete Klickpfad bis
   zum Prüfzustand; (c) präzise Erwartung inkl. Ausgangs-State der beteiligten Einheiten
   (`charged`/`in-melee`/`heroic-intervened` explizit benennen). Nur durchführbare Tests
   übergeben — ein Testfall pro Punkt, keine Sammelpunkte mit mehreren Unterfragen.
   Verankerung: `docs/governance/operating_model.md` + `docs/reference/agent_scopes.md`.
6. **Befund-Lifecycle kodifizieren (VOM STAKEHOLDER VORGEGEBEN):** Fund → Eintrag in
   `Stakeholder_Beobachtungen.md` (ggf. mit Screenshot-Referenz) → Backlog-Item mit
   Rückverweis auf die Beobachtung + Screenshots (ohne Prio-Angabe ans Listenende) → nach
   Umsetzung oder Obsoleszenz: Item ins Archiv, Beobachtungs-Eintrag + zugehörige
   Screenshots löschen.
7. **Handoff-Hygiene verschärfen (VOM STAKEHOLDER GERÜGT, 2. Vorfall):** `ANSWERED` heißt
   ab sofort sichern→löschen **im selben Abschluss**, nicht „behalten bis X" — dieses Muster
   wird abgeschafft. Ggf. den bestehenden Handoff-Hygiene-Gate-Test
   (`tests/docs/test_handoff_hygiene.py`) erweitern: ein `ANSWERED`-Marker, der älter als
   eine Session ist, wird rot statt nur informativ.
8. **(Review-Input) Mock-Fragilität erneut bestätigt** (12 rote Tests durch
   `SimpleNamespace`-Stand-ins bei S156-Mock-Angleichung) — B-078 im Backlog höher
   priorisieren?
9. **(Review-Input) INV-4b-Blast-Radius:** Ability-IDs zählen ins Fraktions-Vokabular
   (Gotcha „fail"-Suffix, dokumentiert in `docs/spec/rules_insights.md`) — keine weitere
   Maßnahme nötig, nur Kenntnisnahme.
