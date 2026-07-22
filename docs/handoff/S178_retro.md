STATUS: NEEDS-DECISION

# S178 — Retro-Maßnahmen (zur Sichtung/Entscheid, nächster Session-Start)

Interaktive Retro in S178 aus Kontext-Gründen (Hard-Wind-down ~140k) in diese Datei verlagert.
B-113 A+B ist committet, verifiziert (Suite grün, UI positiv). Bitte auswählen/freigeben.

## A — Folge-Items aus der UI-Verifikation (Details: `S178_B113_ui_verifikation.md`)
Vorschlag: als neue Backlog-Items aufnehmen (IDs B-129/130/131 frei). Alle Fachlichkeit Ziel 7.
1. **B-129 (Vorschlag): Destroyer-Lord Hit-Reroll-von-1 verdrahten.** Lord besitzt (Stakeholder)
   auch einen Treffer-Reroll-1 — fehlt. Regelrecherche `docs/work/wahapedia_necrons/` + Verdrahtung
   (self-Muster analog Brief A). Benötigte Regeln-Scopes: `docs/work/wahapedia_necrons/` + core_rules „Re-rolls".
2. **B-130 (Vorschlag): Reroll-Marker-Farbe Buff→Grün.** `_REROLL_COLOR` (fix Orange) → buff-grün
   je Farb-Konvention; ggf. perspektiv-abhängig (color_hint) wie `always_fail_marker_row_html`.
   Betrifft `design_system.md` §4.3 Z.455 (Spec-Farbe mit ändern). Scopes: `design_colors.md` + `design_system.md` §4.3/§4.4.
3. **B-131 (Vorschlag): Aura-Reichweiten-Hinweis (Klasse B).** Bei Destroyer-Cult-Einheiten
   st.info-Hinweis, dass Wound-Reroll-1 nur in 6″-Aura eines Destroyer Lords gilt (App misst nicht,
   informiert). Muster wie B-127 RP-Hinweise. Scopes: `docs/work/wahapedia_necrons/` + `design_system.md`.

## B — Prozessmaßnahmen
4. **„start session" = stehende Regel** (Stakeholder-Wunsch S178): Beim Befehl „start session" ohne
   weitere Worte immer denselben Plan-Typ erzeugen wie in S178 (Backlog-Rang-1 wählen, Kernbefund selbst
   verifizieren, Regel-Scopes je Brief setzen/nachtragen, Teil-Briefs + DoD + UI-Verifikations-Roster
   + Token-Budget + Abschluss-Dreiklang, dann Freigabe abwarten). Verankern in `CLAUDE.md` §Standard-Prompts
   + `operating_model.md` (Session-Start). Ggf. Memory-Feedback-Eintrag.
5. **S177-Hygiene-Miss:** S177 hat einen roten Test mitcommittet (`S177_review.md` mit `STATUS: DONE`
   nicht gelöscht → `test_no_done_or_answered_handoff_lingers` rot, in S178 bereinigt). Ursache:
   Vollsuite lief vor dem Schreiben der Review-Datei / DoD-7-Löschung übersprungen. Maßnahme: Abschluss-Schritt
   „DONE/ANSWERED-Handoffs löschen" + „Vollsuite als LETZTER Pre-Commit-Schritt" schärfen.
6. **UI-Verifikations-Persistenz (Stakeholder-Wunsch):** UI-Verifikationen sollen als Datei im Handoff
   liegen. Kollision mit transitory-Hygiene (DoD-7 + `test_handoff_hygiene`). Entscheid nötig: (a) eigene
   persistente Konvention/Verzeichnis für UI-Verifikations-Belege, oder (b) Erkenntnisse ins Backlog
   archivieren + löschen wie bisher.

## C — Offene Backlog-Admin (S178 nicht mehr geschafft, Wind-down)
7. **B-113 formal schließen:** Detail-Abschnitt `backlog_details.md` → `backlog_archive.md`, Zeile in
   `backlog.md` löschen (Pflege-Regel). Am S179-Start miterledigen.
8. **Akzeptanz-Katalog:** je 1 Zeile in `docs/spec/acceptance/rules.md` für „Hardwired for Destruction"
   (Hit-Reroll-1) + „United in Destruction" (Wound-Reroll-1-Aura), `status: implementiert / getestet: ja`
   (Reviewer-Empfehlung, kein Gate-Blocker).
