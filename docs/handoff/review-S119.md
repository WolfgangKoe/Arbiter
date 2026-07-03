# Review S119 — Abschluss-DoD (Reviewer-Subagent, Opus)

**Gesamturteil: GO** (uneingeschränkt — keine Auflagen, keine Blocker/Major-Befunde)

Umfang: 4 Commits vom 2026-07-03 — `dde16f3` (P21), `1f9d82b` (P19), `dfebd27` (P20),
`b3ebfd5` (ziel6-Abschluss/Doku). Freigegebener Plan: `docs/handoff/plan-S119.md`.

## Messwerte (selbst gelaufen)

| Messung | Ergebnis |
|---|---|
| Vollsuite `pytest --tb=short` | **1405 passed** in 224,67 s, **99,11 %** Coverage (Gate 99 % ✅) |
| Architektur-Gate `pytest tests/architecture/` | **8 passed** — INV-4b 11 Tokens (ratchet, unverändert), Ledger 0, alle AC gepinnt |
| `ruff check src tests` | **All checks passed** |

Kein neuer Coverage-Verlust durch S119: die drei geänderten Logikmodule (`stratagem.py`
100 %, `attack_math.py` 99 %, `game_state.py` 100 %) sind voll gedeckt; jeder Fix bringt
seinen Regressionstest mit.

## DoD-Tabelle (7 Punkte je Commit)

| # | DoD-Punkt | dde16f3 (P21) | 1f9d82b (P19) | dfebd27 (P20) | b3ebfd5 (Doku) |
|---|---|---|---|---|---|
| 1 | Regelkonform | ✅ Undo-Fenster ≠ once_per_battle-Sperre; kein Regelbezug verletzt | ✅ 9E: Einschränkung gilt je Spieler (core Stratagem-Regeln) | ✅ core_rules.txt:1578-1586 (Rapid Fire verdoppelt Attacken bei halber Reichweite) | n/a (Doku) |
| 2 | Generisch (keine Fraktions-Strings in src/) | ✅ | ✅ Key = Faktions-Anzeigename aus State, kein hardcodierter Check | ✅ Prüfung auf `weapon_type`-Präfix, aus YAML | n/a |
| 3 | Tests grün + Regressionstest | ✅ `TestUndoHiddenAfterPhaseResetButBattleGreyedPersists` (4 Fälle) | ✅ `TestBattleScopedStratagemUsedByOnePlayerDoesNotBlockOther` + angepasster `test_does_not_reset_used_stratagem_battle_ids` | ✅ `TestRapidFireInputCap` (7 Fälle) | n/a |
| 4 | Architektur-Gate | ✅ | ✅ | ✅ | ✅ unverändert |
| 5 | Clean Code (Type Hints/Namen/black/ruff) | ✅ reine Helferfunktion, dokumentiertes Warum | ✅ | ✅ `_rapid_fire_input_cap` sprechend, base_cap/cap sauber getrennt | n/a |
| 6 | UI manuell | ✅ Stakeholder bestätigt (P21 + S113-Carry-over) | ✅ Stakeholder bestätigt | ✅ Stakeholder bestätigt | n/a |
| 7 | Artefakte aktuell | s. Befund 3 | s. Befund 3 | s. Befund 3 | ✅ backlog §5 / ziel6 / index / ziel7-Drift konsistent |

## Befunde (nummeriert)

**1 — [Minor, kein S119-Mangel] P19-Restlücke bei Spiegel-Fraktionen.**
Der Fix keyt `used_stratagem_battle_ids` auf `spending_faction` (den Faktions-Anzeigenamen,
`gameProtocoll.py:169/183`). Das trennt beide Spieler korrekt, **solange sie unterschiedliche
Fraktionen spielen**. In einem Mirror-Match (z. B. Necrons vs. Necrons) kollidieren beide auf
demselben Dict-Key und die Sperre würde wieder geteilt — also der ursprüngliche Bug im
Sonderfall. Bewertung: **für S119-Zwecke korrekt genug** und **konsistent mit dem bereits
bestehenden Muster** (`cp` ist ebenfalls faktions-gekeyt, gleiche latente Grenze — keine neue
Schuld). Die Restlücke ist durch den geplanten S120-Umbau **gedeckt**: `plan-ziel7-restruktur.md`
migriert alle drei State-Sets auf **Player-Slot-Keys** (Task 1/2), womit der Mirror-Fall
auflöst. Empfehlung: die Mirror-Match-Grenze in S120 explizit als Abnahmekriterium mitführen.

**2 — [kein Mangel] P20 sauber abgegrenzt.** `_rapid_fire_input_cap` greift ausschließlich bei
`weapon_type.startswith("Rapid Fire")`; alle anderen Typen (Assault, Pistol, Grenade, Melee)
geben `base_cap` unverändert zurück (7 Testfälle belegen das). Der **Default** bleibt bei
`base_cap` (`_common.py`: `st.session_state[models_key] = base_cap if (i==0 and base_cap>1) else 0`)
— nur das Feld-**Maximum** wird verdoppelt. Multi-Target ist konsistent: `weapon_max = max(0, cap - others)`
nutzt den (ggf. verdoppelten) `cap`, sodass die Summe über alle Ziele bis 2×`alive` reichen darf.
Regelkonform (Verdopplung nur als optionaler Hebel, ohne Reichweiten-Input in der App).

**3 — [erwartet, kein Mangel] `next_session.md` noch auf S118-Stand.** Das Update folgt
planmäßig im Abschluss nach der Retro (laut Auftrag). **Ausstehend im Abschluss**, nicht als
Mangel gewertet. Übrige Artefakte sind konsistent: backlog §5 listet die drei bewusst offenen
Folge-Befunde (Doppelanzeige, Attributions-Bug, globales phase-Set) sauber mit Code-Verweisen
und Zeiger auf `plan-ziel7-restruktur.md`; ziel6 ist ehrlich archiviert (ausgelagerte Checkboxen
bleiben bewusst `[ ]`, „kein Fake-Abhaken"); index auf „✅ erreicht (S119)"; ziel7 Fix-B-Drift
(WAAAGH! generisch, S113/e031616) korrekt nachgezogen.

**4 — [Positiv] Kein Widerspruch zum S120-Plan.** Alle drei S119-Fixes bewegen sich in die
Richtung des Player-Slot-Splits: `used_stratagem_battle_ids` ist bereits ein Dict (P19 hat es
von `set` auf `dict[str, set]` gehoben) — der S120-Plan baut ausdrücklich darauf auf
(`plan-ziel7-restruktur.md:161`). Nichts in S119 muss für S120 zurückgebaut werden.

## Empfehlungen

- **GO für Commit/Abschluss** — keine Nacharbeit vor dem Merge nötig.
- S120: Mirror-Match (gleiche Fraktion beidseitig) als explizites Abnahmekriterium des
  Player-Slot-Umbaus aufnehmen (schließt Befund 1 endgültig).
- Im Abschluss: `next_session.md` auf S119-Stand ziehen (Befund 3).

DONE
