NEEDS-DECISION

# Planning — Ziel6-Abschluss + Design-System-Priorisierung (S114)

**Stand:** Nach S113 (commit 4330bdc). Vollsuite 1311 passed, 99,10 % Coverage, Architektur 8/8.
Branch `feature/016-protocol-rp-effects`.

Kurzlage: Ziel6 ist inhaltlich praktisch fertig — die einzigen "echten" Restpunkte sind nach
Ziel7 ausgelagert (per Beschluss S112) oder sind reine Doku-/Verifikationsarbeit. Die Audit-Plan-
Queue hat noch offene Pläne, von denen aber keiner ein Ziel6-Abschluss-Blocker ist (alle sind
Backlog-Feinschliff, nicht Ziel6-Kernscope). Handoff-Verzeichnis hat 9 Dateien, 5 sind bereits
abgeschlossen/verarbeitet und können bereinigt werden. Design-System existiert heute nur als
Farbschema (`design_colors.md`) — kein Komponenten-Inventar, keine Tokens jenseits Farbe.

---

## A. Ziel6-Abschluss — was ist exakt noch offen?

`docs/goals/ziel6.md` Übersichtstabelle zeigt 6a–6e, 6g, 6h als ✅ (teilweise), 6f → Ziel7
ausgelagert. Die verbleibenden offenen Checkboxen in der aktiven Datei sind:

| # | Punkt | Datei | Token | Subagent/Tier | Bemerkung |
|---|---|---|---|---|---|
| 1 | "Attacken-Auflösung in allen drei Kontexten verifizieren" (Shooting/Fight/Overwatch) | manuell, kein Code-File | ~10k | Opus (manuelle Prüfung, kein Lookup) | Generischer Kontext-Check, Overwatch-Teil ist bereits Plan 015 zugeordnet |
| 2 | "Tests für Damage-Block + RP-Würfellogik" (aus 6d-v2) | `tests/uiLayout/` bzw. `tests/gameMechanic/` | ~15k | Sonnet (Fleißarbeit, Testfälle nach Vorgabe) | Kein eigener Plan vorhanden — müsste vor Abschluss entweder erledigt oder explizit nach Backlog verschoben werden |
| 3 | 6g: "Prüfen: Nach Reset keine alten Einträge im Battle Log sichtbar" | manuell (Render, `gameLog`) | ~5k | Opus (manuell) | Bereits auch in Backlog §3 als offene UI-Verifikation gelistet — Dopplung, ein Ort reicht |
| 4 | S113 DoD-Punkt 6: manuelle UI-Prüfung once_per_battle Undo/Label | `gameProtocoll.py` (Code bereits da, nur Prüfung fehlt) | ~5k | Opus (manuelle Prüfung) | **Code-Fix ist bereits committet** (`used_battle_ids` in gameProtocoll.py verifiziert) — nur die manuelle Prüfliste aus `review-S113.md` muss noch durchlaufen werden |
| 5 | Daten-Review: "Optional: Tests für korrekte Phase/Stage-Werte" | YAML + Tests | ~10k | Haiku (Lookup gegen Wahapedia) | Als "Optional" markiert — kann explizit als nicht-blockierend für den Abschluss erklärt werden |

**Alles, was tatsächlich Code/Logik betrifft (6e Execute-Logik, 6f Badges, 6h Kat1–3), ist
bereits nach `ziel7.md` ausgelagert** — dort steht es korrekt, nicht hier doppelt einplanen.

**Einschätzung:** Punkt 2 (Damage-Block/RP-Tests) ist der einzige Punkt mit echtem Code-Impact
und keinem Zuhause — sollte vor dem "Ziel6 ✅"-Haken entweder als Mini-Subagent-Auftrag erledigt
oder bewusst nach `backlog.md` verschoben werden (Stakeholder-Entscheidung, da reine Test-Nacharbeit
ohne aktuellen Bug-Treiber). Punkte 1, 3, 4 sind reine manuelle Verifikationen — kein Subagent-
Fleißarbeit-Kandidat, da Streamlit-UI-Interaktion nötig ist (Stakeholder selbst oder `/run`+`/verify`-
Skill-Unterstützung).

**Empfehlung für den Ziel6-Abschluss-Schnitt:** Punkt 4 zuerst (Code ist fertig, nur Haken
nachziehen — günstigster Punkt), dann 1+3 gebündelt als eine manuelle Verifikationsrunde,
Punkt 2 und 5 explizit als bewusste Backlog-Verschiebung dokumentieren statt offen in ziel6.md
liegen zu lassen.

---

## B. Auditpläne — sind alle durch?

**Nein.** Aus `docs/audit/plans/README.md` (Stand selbst geprüft, nicht geraten):

| Plan | Status | Blockiert Ziel6? |
|---|---|---|
| 031 | TODO | Nein — Protokoll-Meta-Timing-Bugs, Ziel7/Backlog-Scope |
| 030 | TODO | Nein — Conquering Tyrant UI-Bugfixes, Backlog-Feinschliff |
| 025 | ✅ DONE | — |
| 016 | TODO | Nein — RP/Living-Metal-Anzeige, eigenständiger Backlog-Punkt |
| 018 | TODO | Nein — Kleinkram-Sammelplan (CP-Doppelvergabe etc.) |
| 015 | TODO | Nein — Reaktive Stratagems/Overwatch, eigener Plan |
| 026 | TODO | Nein — abhängig von 015 |
| 017 | TODO | Nein — SAVE-Block-Badge-Kombination |
| 029 | TODO, **Divergenz** | Nein — Plandatei fehlt im Verzeichnis, README markiert das bereits als zu klärende Divergenz vor Beauftragung |

**Fazit: Keiner der offenen Audit-Pläne blockiert den Ziel6-Abschluss.** Alle offenen
Pläne adressieren Backlog-Feinschliff (UI-Bugfixes, Anzeige-Verbesserungen, Kleinkram), die
bereits korrekt im Backlog/Ziel7-Bereich verortet sind, nicht im Ziel6-Kernscope. Ziel6 kann
unabhängig von der Audit-Queue abgeschlossen werden.

---

## C. Handoff-Bereinigung

`ls docs/handoff/` (9 Dateien, tatsächlich geprüft):

| Datei | Marker | Vorschlag |
|---|---|---|
| `context-audit-S91.md` | kein Marker (Findings-Liste) | next_session.md führt diesen Punkt seit S91 als offenen Carry-over ("ADR-0007-Reste (c)"). Entweder jetzt verarbeiten (Findings durchgehen, in backlog.md übernehmen) oder als bewusste Alt-Schuld markieren. **Nicht** kommentarlos löschen — Inhalt ist nicht dupliziert. |
| `plan-025-step4.md` | Teil A: ANSWERED | Datei selbst sagt "Teil A löschen nach Umsetzung von Step 4; Teil B in eigenen Plan überführen." Plan 025 ist komplett DONE → **kann gelöscht werden**, sofern Teil B (Hold Steady/Set to Defend) bereits als Plan 026 existiert (ist er — README listet 026 mit Verweis auf den 025-Step-4-Übergang). |
| `planning-next-session.md` (S108) | offene Fragen-Block, kein klarer DONE | Inhalt (Conquering-Tyrant-Bugs) ist laut `planning_next_session.md` (S110) "vollständig abgeschlossen und committet". **Kann archiviert/gelöscht werden.** |
| `planning_next_session.md` (S110) | NEEDS-DECISION | S110 ist laut next_session.md / backlog.md längst abgeschlossen (S110-Retro-Maßnahmen M1–M4 sind im Backlog als Punkte geführt, M3 erledigt). **Kann gelöscht werden** — Inhalt ist in Retro-Maßnahmen im Backlog überführt. |
| `planning-S112.md` | NEEDS-DECISION (Ziel7-Frage) | next_session.md bestätigt: "S112 — Coverage-Schuld M3 erledigt, §5 Ziel7 neu definiert". next_session.md selbst sagt "ist verarbeitet (committet) — kann bei Bedarf archiviert werden". **Kann gelöscht werden.** |
| `planning-S113.md` | NEEDS-DECISION | S113 ist laut next_session.md vollständig abgeschlossen (vier Tasks erledigt, T1–T2b committet). **Kann gelöscht werden.** |
| `README.md` | — (Erklärung der Marker-Konvention) | **Bleibt** — ist die Mailbox-Spielregel-Datei selbst. |
| `review_s110.md` | DONE | Marker sagt selbst DONE. **Kann gelöscht/archiviert werden.** |
| `review-S113.md` | NEEDS-DECISION | **Faktisch bereits erledigt** — eigene Recherche bestätigt: der B1/B2-Fix (`used_battle_ids` battle-scope für Undo/Label) ist bereits in `gameProtocoll.py` committet (S113-Commit 4330bdc, Titel "fix stratagem undo/label"). Nur die **manuelle UI-Prüfliste** (7 Schritte, s. Datei) wurde noch nicht durchlaufen — das ist exakt Punkt A.4 oben. **Nicht löschen, bevor die manuelle Prüfung erfolgt ist** — danach Marker auf DONE setzen oder löschen. |

**Konkreter Bereinigungsvorschlag:** 5 Dateien sind toter Ballast und können gelöscht werden
(`plan-025-step4.md`, `planning-next-session.md`, `planning_next_session.md`, `planning-S112.md`,
`planning-S113.md`). `review_s110.md` (Marker DONE) ebenfalls löschbar. `context-audit-S91.md`
bleibt bis zur bewussten Verarbeitung (ADR-0007-Rest, schon als Carry-over geführt).
`review-S113.md` bleibt bis die manuelle UI-Prüfung (Punkt A.4) erledigt ist — danach ebenfalls
löschbar. `README.md` bleibt immer. Macht aus 9 Dateien voraussichtlich 2–3 verbleibende.

---

## D. Verschobener Punkt (Stakeholder-Hinweis, nicht einplanen)

Die UI-Verifikation aus `review-S113.md` wird **nicht** jetzt gemacht, sondern erst im Zuge
von Ziel7 (Gefechtsoptionen) — so der Stakeholder-Hinweis. Notiert, keine Arbeit dafür in diesem
Plan vorgesehen. (Das steht im Spannungsfeld zu Punkt A.4 oben, der die Prüfung dem Ziel6-Abschluss
zuordnet — das ist genau die Stelle, an der dieser Plan eine Stakeholder-Entscheidung braucht,
s. Optionsliste unten.)

---

## E. Strategische Priorisierungsfrage — Design-System vorziehen vor Ziel7?

### Was existiert heute schon?

**Substanz vorhanden:**
- `docs/spec/design_colors.md` (107 Zeilen) — vollständiges, **verbindliches** Farbschema:
  CSS-Variablen (`--arb-*`) in `gameHeader.py`, Status-Badge-Farben (MOVED/ADVANCED/CHARGED/...),
  Effekt-Badge-Kategorien (Buff/Debuff), Subfaction-Badge-Zustände.
- `src/uiLayout/_common.py:_badge()` — ein generischer Badge-HTML-Helper, von
  `state_badges_html()` u. a. genutzt.
- `src/uiLayout/dice_html.py` + `dice_compose.py` — eigene kleine "Komponenten" für die
  Würfelanzeige (mit eigener Spec `docs/spec/dice_display.md`).
- Mehrere "Render-Patterns" über die Dateien verteilt (`_render_*`-Funktionen), aber **nicht**
  als wiederverwendbare, dokumentierte Komponentenbibliothek — jede Datei (`armyCard.py`,
  `unitCard.py`, `gameProtocoll.py`, `_common.py`) baut Badges/Cards/Blöcke mit eigenem
  Streamlit-Markup, nicht über eine gemeinsame Komponentenschicht.

**Kein Treffer** für "Design-System"/"Designsystem" als eigenständiges Artefakt in
`docs/goals/`, `docs/spec/`, `docs/inbox/` oder `backlog.md` — das Thema existiert bisher nur
implizit über `design_colors.md` (Farbe) und vereinzelte Backlog-Einträge zu UI-Unschönheiten.

### Was fehlt für ein echtes Design-System?

1. **Komponenten-Inventar:** Keine Liste "diese UI-Bausteine existieren" (Badge, Card, Block,
   Button-Gruppe, Tab) mit Soll-Aussehen je Zustand.
2. **Tokens jenseits Farbe:** Kein Spacing-/Typografie-/Border-Radius-System.
3. **Einheitliche Patterns:** `_badge()` existiert, wird aber nicht überall genutzt.
4. **Governance:** Farb-Governance müsste auf Komponenten-Ebene erweitert werden.

### Empfehlung

**Mittelweg statt Entweder-Oder:** Ziel6 jetzt sauber abschließen (klein, schnell), danach
**kein großes vorgezogenes Design-System-Großprojekt**, sondern ein **kleiner, scharf
geschnittener erster Schritt**: ein Komponenten-Inventar + minimale Tokens (Spacing, Card-Pattern,
Badge-Pattern) als eigenes kleines Dokument (`docs/spec/design_system.md`, analog zu
`design_colors.md`), gespeist aus den **bereits bekannten** Backlog-Befunden (Invuln-Badge-Chaos,
SAVE-Block-Kombination, Dice-Geometrie). Billig (Befunde liegen vor), und die neuen Ziel7-UI-Stellen
(Kat1–3-Badges) können sich direkt daran halten. Ein **vollumfängliches** Design-System jetzt
vorzuziehen wäre Over-Engineering ohne ausreichend bekannte Anwendungsfälle (verstößt gegen
"DRY: erst ab der dritten Wiederholung").

---

## Optionsliste für den Stakeholder

1. **Ziel6 minimal abschließen** (nur Punkt A.4 — Haken nachziehen, Code ist fertig) **+
   Handoff bereinigen** (5–6 Dateien löschen) **+ Punkte A.1–A.3 und Review-S113-Prüfung explizit
   nach Ziel7 verschieben** (konsistent mit Stakeholder-Hinweis D) **+ kleinen Design-System-
   Inventar-Schritt vorziehen**, dann Ziel7 starten.  ≈ **45k**

2. **Ziel6 vollständig abschließen** (alle Punkte A.1–A.5 inkl. manueller Prüfungen jetzt
   durchführen — widerspricht teils Stakeholder-Hinweis D) **+ Handoff bereinigen +
   Design-System-Inventar vorziehen**, dann Ziel7.  ≈ **75k**

3. **Ziel6 minimal abschließen + Handoff bereinigen, direkt Ziel7 starten — kein Design-System-
   Vorzieh-Schritt** (Design-System ad hoc während Ziel7).  ≈ **25k**

4. **Nur Handoff bereinigen jetzt, Ziel6-Reste + Design-System-Frage auf nächste Session
   vertagen** (falls Kontext-Korridor knapp).  ≈ **10k**

**Empfehlung des Planners: Option 1.**
