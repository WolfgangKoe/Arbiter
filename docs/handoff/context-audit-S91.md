# Kontext-Audit S91 (read-only, Auditor)
Stand: 2026-06-24  ·  Geprüft: 8 Dateien

## Findings (priorisiert, höchster Hebel zuerst)

| # | Datei | Prinzip | Problem (1 Zeile) | Vorschlag (1 Zeile) | Aufwand |
|---|-------|---------|-------------------|---------------------|---------|
| 1 | `docs/goals/ziel6.md` | Compress | 1 744 Zeilen — erledigte Specs (6a–6d-v3 Tasks, Backend-Erkenntnisse, Mockup-Layouts) stehen inline statt archiviert | Erledigte Abschnitte (✅ Tasks, veraltete Layouts) ins Git-Archiv bzw. History-Eintrag auslagern; nur Offene + Spec-Invarianten behalten | L |
| 2 | `docs/spec/architecture.md` | Compress + Write | Refactoring Plan (Phasen 0–4) + Backend-Erkenntnisse (2026-05-26) + Open Design Questions sind historisch erledigt; bekannte Doku-Drifts (session_state-Schema, Colour, Layer) unbehoben | Als „Historie" markieren oder in `decisions/`-ADR auslagern; Drifts aus backlog §4b abarbeiten (kleine Doku-Session) | M |
| 3 | `CLAUDE.md` | Isolate | Token-Disziplin-Abschnitt (~40 Zeilen) trägt technische Implementierungsdetails von `session_context.py` (Regex-Fallstrick, Transcript-Pfad) — das ist operating_model-Territorium | Impl.-Detail-Absatz → `operating_model.md` Event 6 auslagern; in `CLAUDE.md` nur 2-Zeilen-Verweis lassen | S |
| 4 | `docs/goals/backlog.md` | Compress | §0 „Aktuelle Findings (S51)" — Überschrift veraltet (Stand jetzt S90), und ✅-Einträge (#1, R-COMBAT-32, Dice-Arrow, …) bleiben inline statt archiviert; Letzter Abgleich: 2026-06-22 | ✅-Einträge nach Eintrag in `ziel6.md`/Session-Historie entfernen; §0-Überschrift datieren; Abgleich-Datum aktualisieren | S |
| 5 | `next_session.md` | Write | Carry-over §3 „Plan 016 Anzeige-Rest" + §4 „Reihenfolge" + Retro-Vormerke sind detaillierter als hier-sein-sollte (Ziel: Stand + nächster Schritt); Doku-Sync-Schuld explizit vermerkt aber nicht abgearbeitet | Detail-Slicing (Group A/C) → `docs/audit/plans/016` schreiben; hier nur Zeiger; Doku-Sync direkt als §0-Task | S |
| 6 | `docs/spec/architecture.md` | Select | Colour-Abschnitt beschreibt `COLOR_*`/Tailwind — kanonisch ist `design_colors.md`; kein Link dorthin | Einzeiler-Verweis auf `design_colors.md` + Hinweis „live theme = `--arb-*` in gameHeader.py" | XS |
| 7 | `docs/goals/backlog.md` | Isolate | §2 „Offene Tasks" verweist für Details auf `next_session.md`, aber hält selbst die vollständigen Task-Texte (Token-Report v2/v3 Spec, ~80 Zeilen) doppelt | Token-Report-Spec aus §2 kürzen auf „Done, Details → ziel6.md"; §2 nur aktiv-offene Tasks | S |

## Regel-Index-Befund (Select)

`core_rules.txt` 5 503 Z., `rules_appendix.txt` 2 837 Z., `faction_overview.txt` 14 642 Z. — zusammen ~23 k Zeilen ohne Überschriften-TOC oder Stichwort-Index. Mechaniken (z. B. „Lethal Hits", „RP", „Cover") finden sich nur per `grep`. Empfehlung: **additiver Stichwort→Datei:Zeilenbereich-Index** als separates `docs/work/rule_index.md` (Format: `Lethal Hits → core_rules.txt:1420-1435`) — kein Wortlaut berührt, nur Lookup beschleunigt.

## Nicht-Befunde / schon gut

- `LEITSTAND.md` und `operating_model.md` sind schlank, verlinken statt zu duplizieren — nicht anfassen.
- `docs/spec/rules_insights.md` ist kurz und präzise (nur Gotchas, kein Duplikat) — bleibt so.
- `next_session.md`-Gate (120 Zeilen, aktuell 78 Z.) funktioniert — Ratchet hält.
