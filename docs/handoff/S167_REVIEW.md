STATUS: NEEDS-DECISION

# S167 — DoD-Review vor Abschluss-Commit

**Votum: GO** (Doku-/Governance-/Mockup-Session, kein `src/`-Code) — mit **zwei
Pflicht-Handlungen im Abschluss** (unten K1/K2), ohne die S168 die V3-Auflagen verliert.

## Gate-Zahlen (echte Läufe)
- **Vollsuite:** `2018 passed in 279s`, Coverage **99.14 %** ≥ 99 % Floor. ✅
- **Architektur-Gate:** `8 passed`. ✅ INV-4b unverändert 16 Fundstellen (Ratchet, kein
  `src/`-Touch in S167 → keine neue Schuld); Ledger 0. `briefing.md` 74/120 Zeilen
  (Kürzungs-Ziel ≤70, informativ, kein Fail).

## DoD-Punkte (CLAUDE.md)
1. **Regelkonform** — n/a (keine Regel-Logik; Mockup-Inhalt = Bestandskomponenten).
2. **Generisch** — n/a (kein `src/`); keine Fraktions-Strings eingeführt.
3. **Tests grün** — ✅ (s. o.), keine vorher-grünen Tests rot.
4. **Architektur-Gate** — ✅.
5. **Clean Code** — n/a (Markdown/HTML). ADR-0009 sauber, ADR-Index nachgezogen.
6. **UI-Verifikation** — Mockup ist HTML-Vorlage; Stakeholder hat V3 gesichtet und im
   §h-Rückkanal geantwortet → erfüllt für den Zweck einer Vorlage.
7. **Artefakte aktuell** — Planning-Entscheidungen vollständig überführt (Abgleich unten);
   **offen: briefing.md + §h-Auflagen** → K1/K2.

## Planning→Artefakt-Abgleich (S167_PLANNING.md, alle 6 Entscheide)
- (e) Screenshot-Konvention → `agent_scopes.md` Pkt (e) ✅
- (c) Spec-first-Gate „**neue oder geänderte**" → `agent_scopes.md` Z.168–171 ✅
- B-124 Ratchet → `backlog.md` + `backlog_details.md` §B-124, bidirektional verlinkt ✅
- Diagnose-Ratchet M1 → `agent_scopes.md` Executor-Pflichten Z.239–246 ✅
- Planner-Tier → `operating_model.md` MUST-Klausel + ADR-0009 + Index ✅
- V3-Wortlaut „Does not explode" → in V3 umgesetzt ✅

## Konsistenz-Stichproben
- (a) Spec-first deckt „neue ODER geänderte" Bauformen — ✅ wörtlich.
- (b) B-124-Zeile + Detail-Abschnitt formal korrekt gegenseitig verlinkt — ✅.
- (c) ADR-0009 vs. ADR-0008 — **ergänzt, kein Widerspruch**: 0008 Pkt 4 „Planner: Opus
  bleibt", 0009 schärft zu „durchgängig Opus + Lesedisziplin, Sonnet nur >~300-Zeilen-
  Artefakte". ✅
- (d) §h-Auflagen — **nur in der Mockup-Datei**, nicht in Briefing/B-028c1 → K1.

## Kritische Befunde (vor Commit)
- **K1 — §h-Auflagen nirgends außer im Mockup.** Der Stakeholder gibt V3 **bedingte**
  Abnahme („Ansonsten sollten wir mit diesem Mockup arbeiten können") mit **3 Auflagen**:
  (1) nur **ein** Hinweiskasten, unter der GO-Karte — Blau = Hinweis, nicht „Resolved";
  (2) armylist darf in der App **nicht** in derselben Spalte wie Auswahlliste/Effekt-
  Ausführung stehen; (3) „D6 Mortal Wounds"-Text gehört **nicht** über die Schadens-Zahlen-
  felder. `briefing.md` spiegelt noch den Session-START (V2 + 7 Wünsche). **Pflicht im
  Abschluss:** diese 3 Auflagen in `briefing.md` (und B-028c1-Notiz) festhalten + auf §h
  verweisen, sonst gehen sie für S168 verloren. Hinweis: Stakeholder merkt an „das hatte ich
  schon beim letzten Mal gesagt" — V3 hat Vorfeedback teils nicht getroffen, B-028c1 bleibt
  zu Recht `Blocked`.
- **K2 — S167_PLANNING.md Lifecycle.** Marker noch `NEEDS-DECISION`, alle Entscheide sind
  überführt → laut eigener Kopfzeile (Z.5–7) im Abschluss-Commit **löschen**.
  `S166_MOCKUP_EXPLODES.md` bleibt `NEEDS-DECISION` (V3 noch nicht final) — korrekt behalten.

## Nice-to-have
- N1 — `S166_REVIEW.md` steht auf `NEEDS-DECISION`; ein abgeschlossener Alt-Review wäre als
  `DONE` sauberer. Nicht blockierend.

**Abschluss-Empfehlung:** Commit freigegeben, **sofern K1 (Auflagen in briefing/B-028c1) und
K2 (Planning löschen) im selben Abschluss erledigt** werden.
