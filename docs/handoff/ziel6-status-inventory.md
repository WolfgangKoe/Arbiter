# Ziel6 — Status-Inventar (Rest-Scope), Stand 2026-06-30

Erstellt von Status-Inventar-Subagent. Faktentreue Klassifikation jeder offenen Checkbox
(`- [ ]`) in `docs/goals/ziel6.md`. Quelle: vollständige Datei (1194 Zeilen) + grep/git-Belege.

## Klassen
- **ZIEL7** — Zeile/Abschnitt explizit `→ Ziel7` markiert.
- **ERLEDIGT-UNGEHAKT** — faktisch umgesetzt, Box nur nicht abgehakt (Beleg: Datei:Symbol oder Commit).
- **OFFEN-ZIEL6** — echte verbleibende Ziel6-Arbeit.

| Abschnitt | Checkbox (Kurz) | Klasse | Beleg / Schätzung |
|---|---|---|---|
| 6a–6d Carry-over | Attacken-Auflösung Shooting/Fight/Overwatch verifizieren | OFFEN-ZIEL6 | Keine Test-/Code-Belege für expliziten 3-Kontext-Vergleich gefunden. Verifikations-/Review-Task. S, Sonnet, manuelle Prüfung + ggf. Test. |
| 6a–6d Carry-over | Tests für Damage-Block + RP-Würfellogik (6d-v2) | OFFEN-ZIEL6 | Nur 2 Treffer für `reanimat`-Tests projektweit; kein dedizierter Damage-Block/RP-Würfel-Test gefunden. S, Sonnet, Test. |
| 6e | `commandPhase.py`: Einheiten mit Befehlsphase-Fähigkeiten anzeigen (Listen-Hinweis) | OFFEN-ZIEL6 | grep bestätigt: `_render_unit_command_abilities` (commandPhase.py:319ff) rendert nur für die **selected** Unit, kein army-weiter Hinweis/Badge wie bei `has_psyker()` in psychicPhase.py. Feature fehlt wirklich. S–M, Sonnet, Code+Test. |
| 6e | `collect_modifiers_for_phase()` | ZIEL7 | Zeile 79: „→ Ziel7 (subfaction Execute-Logik)". |
| 6e | `Ability`-Schema `modifier`-Felder | ZIEL7 | Zeile 80: „→ Ziel7". |
| 6e | `unit_abilities.yaml`/`faction_abilities.yaml` Modifier-Felder | ZIEL7 | Zeile 81: „→ Ziel7". |
| 6e | Phase-Handler rufen `collect_modifiers_for_phase()` | ZIEL7 | Zeile 82: „→ Ziel7". |
| 6f (gesamter Abschnitt) | Ability-Badges + Keyword-Highlighting (3 Tasks) | ZIEL7 | Abschnitts-Header: „Ausgelagert nach Ziel7" (Zeile 89/93). |
| 6g | Prüfen: Nach Reset keine alten Einträge im Battle Log | ERLEDIGT-UNGEHAKT | `tests/gameMechanic/test_game_log.py:220` `test_log_rounds_empty_after_archive` deckt exakt diesen Fall ab (asserted `data["rounds"] == []` nach `archive_and_reset_log()`). |
| 6h Kat.1 Code | `loader.py`: CommandProtocol.secondary optional | ZIEL7 | Zeile 177: „→ Ziel7". |
| 6h Kat.1 Code | `armyCard._render_protocol_ui()` no-secondary auto-apply | ZIEL7 | Zeile 178: „→ Ziel7". |
| 6h Kat.1 Code | Tyranids Pool-Check Synapse-Unit lebt | ZIEL7 | Zeile 179: „→ Ziel7". |
| 6h Kat.1 YAML | AdMech `faction_abilities.yaml` (6 Canticles) | ZIEL7 | Zeile 183 „blocked-by-YAML… → Ziel7"; `ls data/wh40k_9e/` bestätigt: kein `adeptus_mechanicus/`-Verzeichnis. |
| 6h Kat.1 YAML | Tyranids `faction_abilities.yaml` | ZIEL7 | Zeile 184, kein `tyranids/`-Verzeichnis. |
| 6h Kat.1 Tests | `test_faction_abilities_admech.py` | ZIEL7 | Zeile 188. |
| 6h Kat.1 Tests | `test_faction_abilities_tyranids.py` | ZIEL7 | Zeile 189. |
| 6h Fix B | WAAAGH!-UI generisch (ID-String, WARBOSS-Keyword, Effekttexte) | ERLEDIGT-UNGEHAKT | `src/uiLayout/armyCard.py:370–447` `_render_once_per_battle_ability_ui` ist vollständig generisch: `once_per_battle`-Condition statt ID-String, `check_conditions()` statt WARBOSS-Hardcode, `active_text`-Feld aus YAML. `grep -rn '"waaagh"|"WARBOSS"' src/` = 0 Treffer. Commit `e031616` „Generify WAAAGH! UI". Zeilen 177/205/225–246/280 sind veraltete Beschreibung einer alten Implementierung. |
| 6h Kat.2 Code | `armyCard._render_waaagh_ui()` active_rounds (T'au) | ZIEL7 | Zeile 291: „→ Ziel7". |
| 6h Kat.2 Code | `game_state._reset_turn_state()` Runden-Fenster T'au | ZIEL7 | Zeile 292: „→ Ziel7". |
| 6h Kat.2 YAML | T'au `faction_abilities.yaml` | ZIEL7 | Zeile 295, kein `tau_empire/`-Verzeichnis. |
| 6h Kat.2 Tests | `test_faction_abilities_tau.py` | ZIEL7 | Zeile 298. |
| 6h Kat.3 (gesamt, 8 Boxen) | Auto-Progression SM/Death Guard/Chaos SM (Code+YAML+Tests) | ZIEL7 | Abschnitts-Intro Zeile 300–303 explizit „komplett… nach Ziel7 ausgelagert". |
| Daten-Review | Optional: Tests für korrekte Phase/Stage-Werte | OFFEN-ZIEL6 | Explizit als „Optional" markiert — kein Beleg für vorhandene dedizierte Phase/Stage-Wert-Tests gefunden, aber niedrige Priorität laut eigener Markierung. S, Haiku/Sonnet, Test. |
| 6l Phase 2 | Morgog's Finkin' Cap `trigger/effect: gain_cp_roll` | ERLEDIGT-UNGEHAKT | `data/wh40k_9e/orks/relics.yaml:23` Eintrag vorhanden; `commandPhase.py:72` `resolve_gain_cp_roll`, `commandPhase.py:183` `_render_gain_cp_roll`, verdrahtet über `unit.get_triggered_effect("phase_start","command","gain_cp_roll")` (commandPhase.py:353). |
| 6l Phase 2 | Da Irongob `trigger/effect: mortal_after_melee` | ERLEDIGT-UNGEHAKT | `data/wh40k_9e/orks/relics.yaml:87` Eintrag vorhanden; `fightPhase.py:123` `_render_mortal_after_melee`, aufgerufen `fightPhase.py:332`; auch in `_common.py:812` referenziert. |
| 6l Phase 2 | Veil of Darkness `trigger/effect: teleport` | ERLEDIGT-UNGEHAKT | `data/wh40k_9e/necrons/relics.yaml:67` `effect: teleport`; `movementPhase.py` implementiert `movement_locked`-Flag-Handling (Zeilen 62/132/250/263/264) — passt zu S35-Changelog „Veil of Darkness (`movement_locked`)". |
| 6l Phase 2 | UI: Button pro triggered Relic in richtiger Phase | ERLEDIGT-UNGEHAKT | Folgt aus den drei vorherigen Belegen — alle drei haben eigene Render-Funktionen mit Buttons (`_render_gain_cp_roll`, `_render_mortal_after_melee`, Movement-Lock-UI). Kein offener Rest. |
| Akzeptanzkriterien | Header VP/CP inline, Badges 2× | ERLEDIGT-UNGEHAKT | 6a Status-Tabelle (Zeile 13) = ✅; `gameHeader.py:222-223` zeigt VP/CP inline. |
| Akzeptanzkriterien | armyCard korrekte Fähigkeiten je Fraktion, kein Necron-Fallback | ERLEDIGT-UNGEHAKT | `grep -rn necron src/uiLayout/armyCard.py` = 0 Treffer; generisches System (6b ✅, S41/S51 Fraktionsbereinigung). |
| Akzeptanzkriterien | WAAAGH aktivierbar, Command Protocol wechselbar über armyCard | ERLEDIGT-UNGEHAKT | Siehe 6h Fix B Beleg + `_render_round_choice_ui` in armyCard.py; beide produktiv. |
| Akzeptanzkriterien | Ka'tah (Custodes) + Canticles (AdMech) ohne Code-Änderung | TEILWEISE ZIEL7 | Custodes-Teil ERLEDIGT (Zeile 172 ✅ YAML vorhanden, generisches `round_choice`-System trägt). AdMech-Teil ist ZIEL7 (kein YAML-Verzeichnis). Kriterium als Ganzes bleibt offen wegen AdMech-Hälfte → gehört zu Ziel7, nicht Ziel6-Restscope. |
| Akzeptanzkriterien | Auto-Progression-Badge Space Marines | ZIEL7 | Hängt direkt an Kategorie-3-Auto-Progression (s.o.), explizit Ziel7. |
| Akzeptanzkriterien | Stratagems Default-Tab in gameProtocoll | ERLEDIGT-UNGEHAKT | 6c Status-Tabelle ✅; `docs/spec/ui_layout.md:12` zeigt `[Stratagems \| Battle Log]`-Tab-Reihenfolge (Stratagems zuerst = Default). |
| Akzeptanzkriterien | Attackensequenz simultan, Modifier transparent, kein Zwischenwert-Klicken | ERLEDIGT-UNGEHAKT | 6d Status-Tabelle ✅ (Basis-Implementation); `ui_layout.md:344` „Both players may have active buttons simultaneously". 6d-v2 (volles Redesign) ist separat 🔵 offen, aber Akzeptanzkriterium bezieht sich auf 6d-Basisfunktion. |
| Akzeptanzkriterien | CP-Doppelvergabe unmöglich | ERLEDIGT-UNGEHAKT | 6e Task Zeile 77 ✅ „CP-Vergabe als einmaligen Phase-Grant" (S55 verifiziert). |
| Akzeptanzkriterien | Ability-Badges auf unitCard sichtbar + korrekt ablaufend | ZIEL7 | Direkt von 6f abhängig, das komplett nach Ziel7 ausgelagert ist. |
| Akzeptanzkriterien | Reset archiviert Log; neues Spiel startet sauber | ERLEDIGT-UNGEHAKT | 6g Tasks alle ✅ + `test_log_rounds_empty_after_archive` (s.o.). |
| Akzeptanzkriterien | Archiv-UI im Setup-Screen: Liste, Download, Löschen | ERLEDIGT-UNGEHAKT | 6g Task Zeile 154 ✅ „Archiv-Verwaltungs-Sektion (Liste, Download, Löschen mit Bestätigung)". |
| 6n Review-Runde 2 | P17 — Schadenszuweisungs-Korrekturmöglichkeit (±-Counter pro Gruppe) | OFFEN-ZIEL6 | Kein Treffer für Korrektur-Counter-UI in `_common.py`/`game_state.py`. Größere UX-Feature mit Folgefragen (Mehrwunden-Tracking). **L**, Sonnet/Opus (Design-Entscheidung nötig), Code+Test+manuelle UI-Verifikation. |
| 6n Review-Runde 2 | P18 — gegnerische Untergruppen als Ziele anzeigen, einheitlicher Deklarations-Flow auch für nicht-gruppierte Einheiten | OFFEN-ZIEL6 | `melee_with` existiert (genutzt in `_common.py`), aber keine UI, die Untergruppen-Ziele in der PlayerArea separat listet; „EIN einheitlicher Flow" ist als Ziel benannt, nicht als erledigt. **M**, Sonnet, Code+Test+manuelle UI-Verifikation. |

---

## Bottom Line

**6 Checkboxen sind echt-offen für Ziel6** (nicht Ziel7, nicht bereits erledigt):

1. Attacken-Auflösung Shooting/Fight/Overwatch verifizieren — **S (~10k)**, Sonnet, Verifikation+ggf. Test
2. Tests für Damage-Block + RP-Würfellogik (6d-v2) — **S (~10k)**, Sonnet, Test
3. `commandPhase.py`: Einheiten mit Befehlsphase-Fähigkeiten anzeigen — **S–M (~15k)**, Sonnet, Code+Test
4. Daten-Review: Optional-Tests Phase/Stage-Werte — **S (~10k)**, Haiku/Sonnet, Test (niedrige Prio, selbst als „Optional" markiert)
5. P17 — Schadenszuweisungs-Korrektur-UI (±-Counter, Mehrwunden-Tracking-Folgefrage) — **L (~50k)**, Sonnet/Opus, Code+Test+manuelle UI-Verifikation
6. P18 — Einheitlicher Deklarations-Flow für Einheiten ohne Untergruppen + Ziel-Anzeige in PlayerArea — **M (~25k)**, Sonnet, Code+Test+manuelle UI-Verifikation

**Token-Summe (grob):** ~10k + ~10k + ~15k + ~10k + ~50k + ~25k = **~120k**

Zusätzlich: 1 Akzeptanzkriterium („Ka'tah + Canticles ohne Code-Änderung") ist **gemischt** — Custodes-Hälfte erledigt, AdMech-Hälfte gehört zu Ziel7. Kein eigener Ziel6-Aufwand nötig, nur Doku-Klarstellung (Checkbox sollte als „teilw." markiert oder die Custodes-Hälfte separat abgehakt werden — keine Code-Arbeit).

### Ist die „<1 Session"-These haltbar?

**Nein, nicht uneingeschränkt — aber auch nicht weit entfernt.** Von den 6 echten Posten sind 4 klein
(S, je ~10–15k) und könnten zusammen in einer Session laufen (~45k). Die zwei größeren Posten —
**P17** (~50k, Design-Entscheidung + Mehrwunden-Tracking-Folgefrage, vom Nutzer selbst als kritischer
Fall markiert) und **P18** (~25k, UI-Flow-Vereinheitlichung mit manueller Verifikation) — sind
einzeln noch im Korridor, aber **alle 6 zusammen (~120k)** sprengen den empfohlenen
Token-Korridor (<150k bei 90%-Wind-down ab ~135k) sehr knapp bzw. lassen keinen Headroom für
Planning/Review/Retro in derselben Session.

**Realistische Einschätzung:** Die 4 kleinen Punkte (1–4) sind in **einer** Session machbar.
P17 und P18 brauchen aufgrund von Design-Tiefe (P17 explizit mit offener Folgefrage) und
Pflicht-UI-Verifikation eher **eine zweite, eigene Session** — nicht weil der Code-Umfang riesig
ist, sondern weil P17 eine echte Scope-Klärung mit dem Stakeholder braucht (wie wird das
Mehrwunden-Frontmodell-Tracking gelöst?), bevor Code geschrieben werden kann.

**Größter Brocken:** P17 (Schadenszuweisungs-Korrektur, ~50k, Opus-Tier wegen offener Design-Frage).
