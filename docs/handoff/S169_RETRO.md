STATUS: NEEDS-DECISION

# S169 — Retro (Maßnahmen zur Entscheidung im S170-Planning)

Lebensdauer: bis Stakeholder-Entscheid im S170-Planning; gewählte Maßnahmen werden dort in
die kanonischen Artefakte überführt, danach Datei löschen. Nicht genannte Maßnahmen gelten
als verworfen (operating_model.md §ev1).

## Was gut lief

- **Erste echte Parallel-Welle:** T2 (Spec-Umbau), T3 (b1) und T6 (Aufräumen) liefen
  gleichzeitig auf disjunkten Dateien — kein Konflikt, Koordinator-Kontext blieb im
  Korridor, Session schaffte Spec-Umbau + b1 + b2 + Aufräumen + Dreiklang.
- **Manuelle Referenz-Vorprüfung zahlte sich aus:** T6 behielt `21-29-43.png`, weil der
  Datei-Grep eine Referenz fand, die der Planner-Sammel-Grep übersehen hatte (Kurzform-
  Gotcha, exakt wie im Planning §E.3 gewarnt).
- **Agent-Resume nach Hard-Abort:** T4 wurde vom Account-Session-Limit mitten im Auftrag
  abgebrochen und nach Reset mit intaktem Kontext fortgesetzt („erst Working-Tree prüfen,
  nichts doppelt") — kein Arbeitsverlust, kein Doppel-Edit.
- **b1 fachlich sauber:** 5 Explodes-Träger wortgetreu belegt, Spyder-Auslassung begründet
  + regressionsgetestet; Reviewer bestätigt Regelkonformität ohne Beanstandung.

## Was schief lief

- **Review-NO-GO durch Lösch-Reihenfolge:** T6 löschte Mockups/Marker, während aktive
  Artefakte (processes.md, abilityEngine.py-Docstring, backlog_details.md) noch auf sie
  verwiesen — die Whitelist-Vorprüfung prüfte nur Screenshots, nicht die Marker/Mockups.
  Korrektur kostete eine Extra-Runde (Haiku, 3 Stellen).
- **Token-Schätzungen erneut deutlich zu niedrig:** T3 ~288k bei ~180k Budget, T4 ~325k
  bei ~190k (T4 lief dadurch ins Account-Limit und musste tags darauf fortgesetzt werden).
  Muster aus S168 (T3 160k/100k) wiederholt sich mit Faktor ~1,5–1,7.
- **Retro-M3 nicht durch Claude umsetzbar:** Permission-Classifier blockiert jede Änderung
  an der eigenen Permission-Konfiguration (Subagent UND update-config-Skill) —
  `S169_M3_ALLOWLIST.md` wartet auf den Stakeholder; `rm`/`curl` liefen in dieser Session
  trotzdem durch (Classifier-Verhalten inkonsistent zu S168).

## Maßnahmen (nummeriert, entscheidbar)

1. **Lösch-Whitelist-Standardsatz schärfen** (`docs/reference/agent_scopes.md`): Vor JEDER
   Whitelist-Löschung Pflicht-Grep je Datei (Voll- UND Kurzname) über `docs/` + `src/`;
   Treffer in aktiven Artefakten ⇒ erst umbiegen, dann löschen — gilt für alle Dateitypen,
   nicht nur Screenshots. **Empfehlung: übernehmen.**
2. **Token-Schätzfaktor 1,5 für M-Briefs** (`agent_scopes.md` Auftragsgrößen-Gate):
   Executor-Schätzungen ab sofort ×1,5 als Budget ansetzen, Selbst-Stopp bei 2× Schätzung;
   bei prognostiziertem Realverbrauch > 250k den Brief vor Vergabe splitten.
   **Empfehlung: übernehmen.**
3. **M3-Allowlist durch Stakeholder eintragen** (`S169_M3_ALLOWLIST.md`): zwei Regeln in
   `.claude/settings.json`, danach Datei löschen. **Empfehlung: Stakeholder-Aktion, kein
   Claude-Task.**

## Offen für den Stakeholder (kein Maßnahmen-Entscheid)

- **UI-Verifikation b2** (`S169_b2_ui_verifikation.md`, AWAITING-VERIFICATION) — App läuft
  auf :8501; B-028c1 bleibt bis dahin unabgehakt „In Progress".
- **§6-Interpretation bestätigen:** T2 hat statt des wörtlich genannten „§6" den
  Würfel-Abschnitt §4.4 gesplittet (nach P-08 migriert), da §6 (GO-Karten) keine
  Würfeldarstellungs-Inhalte hat — bitte bestätigen oder korrigieren.

## Sessionstand-Kurzfassung (für das S170-Planning)

- Review S169: **NO-GO → GO nach Pflicht-Korrektur** (3 verwaiste Referenzen umgebogen);
  Gates: 2066 passed, Coverage 99,18 %, Arch 8/8, Doku/Akzeptanz 25 passed, Nenner 159,
  Ledger 0.
- Geliefert: Spec-Umbau (design_system generisch §1.5–1.9/§7/§3.1; processes P-08/P-16),
  Retro-M1, b1 (explode-Schema, Engine ohne Selbstwurf, 5 Träger), b2 (Pflicht-Trigger-
  Kachel in allen 5 Phasen, B-124(a)-Kürzung), Handoff-Aufräumen (12 Dateien).
- Nächstes: b3 (`auto_explode`-GO, ~M), b2-Verifikation einlösen, B-124(b) Apply-Damage-
  Vereinheitlichung, Spyder-Explodes (braucht Per-Modell-Konzept).
