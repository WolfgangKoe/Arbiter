STATUS: ANSWERED

# S137 — DoD-Review (Reviewer-Subagent, vor Close-Commit)

Lifecycle: Review-Handoff. Nach Kenntnisnahme im Abschluss → Marker DONE, Datei löschen.

Geprüft: uncommitteter Stand gegen HEAD (14 geänderte + 11 neue Dateien). Reine
Diff-/Doku-Prüfung; Gates liefen zentral (1708 passed, 99,12 %, mypy 62 = Baseline,
Doku-/Architektur-/Akzeptanz-Gates grün). Die 8 neuen Beobachtungen im Eingang sind
S138-Input und wurden vereinbarungsgemäß nicht bewertet.

## Ergebnis: GO

Der Stand ist commit-fähig. Alle DoD-Punkte erfüllt; drei Befunde unten, keiner
blockiert den Commit (Befund 1 sollte in S138 als Einzeiler nachgezogen werden).

## Befunde (schwer → leicht)

1. **Pistolen-im-Nahkampf: Re-Roll-Angebot auf falsche Phase geschlüsselt (mittel,
   Regelkonformität — heute ohne Auswirkung).**
   `_common.py` (render_group_assignment): `reroll_phase = "fight" if (use_melee or
   in_melee) else "shooting"`. Der `in_melee`-Fall ist der Pistolen-Beschuss aus der
   Engagement Range — der findet laut Grundregeln (core_rules.txt, Abschnitt PISTOL)
   in der **Shooting-Phase** statt, nicht in der Fight-Phase; gerendert wird er auch
   nur aus `shootingPhase.py`. Der Test
   `test_render_group_assignment_ranged_in_melee_offer_uses_fight_phase` zementiert
   die falsche Regelaussage („Pistols fired while in melee happen in the Fight
   phase") sogar im Docstring.
   **Heute kein Verhaltensfehler:** Command Re-Roll deckt in der YAML beide Phasen ab,
   und `used_stratagem_ids` wird bei jedem echten Phasenwechsel geleert
   (game_state.py) — Once-per-Phase bleibt korrekt erzwungen. Latentes Risiko: eine
   künftige Fight-only-after_roll-GO würde am Pistolen-Anker in der Shooting-Phase
   fälschlich angeboten.
   **Empfehlung S138:** `reroll_phase = "fight" if use_melee else "shooting"` +
   Test/Docstring korrigieren (Einzeiler, keine Verhaltensänderung heute).

2. **Doppelter STATUS-Marker in `S137_yaml_trunkierung_scan.md` (leicht).**
   Zeile 1 `STATUS: ANSWERED`, Zeile 5 zusätzlich `STATUS: DONE`. Verwirrt den
   Handoff-Lifecycle — den inneren Marker beim Abschluss entfernen.

3. **Asymmetrie Melee-/Fernkampf-Gating (leicht, vorbestehend).** Der neue
   Fernkampf-Zweig bietet den Re-Roll korrekt nur bei `eff_models > 0` an; der
   Melee-Zweig kennt kein analoges Gating (Angebot auch bei 0 zugewiesenen Attacken).
   Nicht durch diesen Diff eingeführt — nur Notiz, ggf. mit B12 zusammen anfassen.

## Geprüfte DoD-Punkte

- **Regelkonform:** Command Re-Roll gegen core_rules.txt geprüft — Once-per-Phase
  („The same Stratagem cannot be used more than once during the same phase") und
  Anwendbarkeit auf den Attackenzahl-Wurf („…rolled the dice to determine the number
  of attacks…") sind korrekt umgesetzt; Anker-only ohne Wert-Eingabe passt zum
  Nicht-Erfassen des Wurfs. Einzige Abweichung: Befund 1 (Phasen-Schlüssel Pistolen).
  CAST-Badge korrekt an `turn_flags["cast"]` (psychicPhase) gebunden.
- **Generic src:** keine Fraktions-Strings im src-Diff („Stikkbombz"/„Orks" nur in
  Tests als Fixture-Daten; CAST/Badge-Logik generisch).
- **Architektur-Invarianten:** kein direkter YAML-Zugriff, Layer-Richtung intakt
  (uiLayout → gameMechanic), kein Streamlit in gameObjects; markdownlint-Trial
  (package.json, .markdownlint.jsonc) berührt src nicht, node_modules ignoriert.
- **Artefakt-Sync:** Backlog B12/B13/B14 + Scraper-Trunkierung eingetragen;
  design_colors.md um CAST-Zeile ergänzt (deckungsgleich mit `unitCard.py`);
  Beobachtungs-Eingang nach „Zuletzt überführt" verschoben; Handoff-Marker konsistent
  (B12-Konzept bewusst NEEDS-DECISION für S138, Befund-Dateien ANSWERED) — bis auf
  Befund 2.
- **Auffälligkeiten:** keine Debug-Reste, keine toten Pfade; neue Kommentare folgen
  der Konvention (Spec-Verweis + Warum, z. B. design_system.md §6.2/§6.3 — Abschnitte
  existieren). Regressionstests decken beide Bugfixes präzise (genau EIN
  Wound/Save-Trenner; „−1 to Hit" genau einmal).

## Empfehlungen S138

1. Befund 1 als Einzeiler-Fix zu Beginn von S138 (vor B12-Umsetzung, gleiche Stelle).
2. Befund 2 beim Abschluss S137 gleich mit bereinigen (Marker-Zeile löschen).
3. B12-Konzept (NEEDS-DECISION) wie geplant zuerst entscheiden — die
   Inventar-Grundlage im Konzept passt zum jetzt committeten Stand.
