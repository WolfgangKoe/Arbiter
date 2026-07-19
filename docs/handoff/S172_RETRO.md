STATUS: NEEDS-DECISION

# S172 — Retro (Maßnahmen zur Entscheidung im S173-Planning)

Lebensdauer: bis Stakeholder-Entscheid im S173-Planning; gewählte Maßnahmen werden dort in
die kanonischen Artefakte überführt, danach Datei löschen. Nicht genannte Maßnahmen gelten
als verworfen (operating_model.md §ev1).

## Was gut lief

- **Live-Verifikation im Sessionfluss:** Der Stakeholder testete parallel zu laufenden
  Executors und kommentierte direkt in der Verifikationsdatei — alle 3 Testfälle noch in
  derselben Session grün, d + b3 abgeschlossen, **B-028c1 nach 4 Sessions archiviert**.
- **Sequenzielles Same-File-Briefing trug:** Bug-1- und Bug-2-Executor nacheinander auf
  `_common.py`, mit explizitem Hinweis auf den frischen `st.rerun()`-Fix im Folge-Brief —
  kein Edit-Konflikt, Vorgänger-Fix blieb erhalten.
- **Code-verifizierte Planner-Hypothesen hielten:** beide Root Causes (fehlendes `st.rerun()`,
  `selected`-Scan statt Einzel-Pin) exakt wie im Planning analysiert — Fixes ohne Umwege.
- **Review GO im ersten Anlauf** (S170/S171 jeweils NO-GO im ersten Durchgang) — die frisch
  verankerte M2-Schärfung (Marker nur bei Löschung im selben Abschluss) wurde korrekt angewandt.

## Was schief lief

- **Zwei Budget-Risse:** Task 5 (`auto_explode`-GO) ~292k Ist vs. ~190k Plan (+54 %) — der
  M-Brief bündelte Wahapedia-Recherche + neues Schema + UI + 15 Tests, war real eine
  L-Aufgabe (Auflage „max. M" verfehlt, hätte gesplittet werden müssen). Artefakt-Pflege
  (Haiku) ~138k Ist vs. ~40k Budget — Archiv-Verschiebung (133 Zeilen) + 2 neue Items +
  Cleanup war kein XS-Brief.
- **2× Executor-Hänger an Hintergrund-pytest:** Vollsuite via `run_in_background` ging beim
  Shell-Reset zwischen Bash-Aufrufen verloren; Executors warteten auf eine Notification, die
  nie kam → je ein SendMessage-Nudge des Koordinators nötig.
- **Haiku-Doku-Edit brauchte Nachschliff:** sprachliche/faktische Schnitzer in der
  Retro-Verankerung (falsche Maßnahmen-Nummer, „DONE" statt „ANSWERED" als S171-Grund) —
  vom Koordinator korrigiert; billig, aber Muster (Haiku-Prosa gegenlesen).

## Maßnahmen (nummeriert, entscheidbar)

1. **Brief-Baustein „Vollsuite synchron"** (`agent_scopes.md`, Executor-Brief-Pflichten):
   Testläufe in Executor-Briefs ausdrücklich SYNCHRON ausführen lassen (kein
   `run_in_background` für pytest) — beseitigt die Hänger + Nudge-Kosten.
   **Empfehlung: übernehmen (XS, Doku-Einzeiler).**
2. **Recherche-Aufschlag in der Budget-Regel** (`agent_scopes.md`): Briefs mit
   Regelrecherche-Anteil (Wahapedia-Suche + wortgetreue Erfassung) bekommen +50 % aufs
   ×2,5-Budget ODER die Recherche wird als eigener Vorab-Brief abgespalten (dann bleibt der
   Umsetzungs-Brief bei M). **Empfehlung: übernehmen (XS).**
3. **Backlog-Archivierung als eigener Brief-Typ** (`agent_scopes.md`, Zeile
   „Doku/Backlog pflegen"): Archiv-Verschiebungen (Item + Details-Block) realistisch mit
   ~100k budgetieren und von übriger Artefakt-Pflege trennen — oder explizit dem Koordinator
   zuordnen. **Empfehlung: übernehmen (XS).**

## Sessionstand-Kurzfassung (für das S173-Planning)

- Review S172: **GO im ersten Anlauf**; Gates: 2123 passed, Coverage 99,20 %, Arch 8/8,
  Doku/Akzeptanz 25, black/isort/ruff sauber.
- Geliefert: S171-Retro-M1/M2 verankert; d-Repair (Direkt-Apply-`st.rerun()`,
  `last_touched`-Pin + §1.7-Neufassung); b3 `auto_explode`-GO „Curse of the Phaeron"
  (generisches `cp_overrides`-Schema, 15 Tests, R-COMBAT-45); Stakeholder-Live-Verifikation
  Testfälle 1–3 positiv → **B-028c1 Done + archiviert**; B-125/B-126 neu erfasst;
  R-COMBAT-41–44-Drift gefixt; 6 Handoff-Dateien abgeräumt.
- Nächstes (S173): Retro-Maßnahmen 1–3 entscheiden; **B-122 „Careen!"** (GO-Karte an
  Baustein ②, wie Curse of the Phaeron); **B-125** (Nach-Confirm-Reset-Wunden) +
  **B-126** (MW-Cap je Würfeltyp); danach B-028c2 (`reroll_rp`) / Spyder-Konzept laut Backlog.
