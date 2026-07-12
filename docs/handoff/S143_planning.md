STATUS: ANSWERED

# S143 Planning-Entwurf

## Stakeholder-Entscheid (2026-07-12, im Chat)

1. **Plan S143: freigegeben wie vorgelegt** (Review+Retro S142 → Welle 1 → mypy-Wellen → FixD).
2. **Frage 1 (FixD): (b)** — FixD-Plan freigegeben UND Folge-Task „on_target-Anker vor
   Hit/Wound/Save" (read-only Recherche/Konzept) einplanen.
3. **Frage 2 (Stratagems): (b)** — auf Kern-Kodex filtern. Vorgehen: Recherche-Task erstellt
   zuerst die Abgleichliste (Kodex vs. Supplement) als NEEDS-DECISION-Handoff; Löschung in
   den YAML-Daten erst nach Stakeholder-Bestätigung der Liste.

Quelle: `.claude/tasks/next_session.md` (Stand S142), `docs/goals/ziel7.md`,
`docs/goals/backlog.md`, `docs/reference/agent_scopes.md`, `docs/handoff/S141_ui_befunde_group_a.md`,
`docs/audit/plans/S142_fixD_resolution_tabs.md` + heutiger Stakeholder-Input (5 UI-Befunde A–E,
2026-07-12). Mypy-Baseline verifiziert: `python tools/mypy_gate.py` → 28 == Baseline (OK), Punkte
E (Stratagem-Zeilen 748/762 in `necrons/stratagems.yaml`) gegen Datei belegt.

## Kontext / Priorisierungs-Begründung

Queue-Punkt 1 (Review+Retro S142) ist überfällig und günstig — steht zuerst. Die zwei
Entscheidungsfragen (FixD-Scope, Stratagem-Umfang) müssen laut `agent_scopes.md`
("Entscheidungs-Timing") früh im Plan stehen, damit der Stakeholder bei vollem
Kontext-Headroom entscheidet — sie stehen daher als eigener Schritt 2, VOR der
Detailarbeit. Danach werden die beiden frisch verifizierten Bugs (C: Wound-Panel-
Fehlberechnung, A: Insane-Bravery-Zielauswahl) VOR die bestehende Queue (mypy/abilityEngine/
Roster-Test) gezogen: beide sind konkrete, stakeholder-bestätigte Funktions-Bugs mit
Spielauswirkung (C verfälscht eine Würfelauswertung, A blockiert dem zweiten Spieler die
Aktion), während mypy-Ratchet/abilityEngine-Recherche reine Technik-Schuld ohne akuten
Funktionsbruch sind. FixD-Ausführung bleibt hinter der Stakeholder-Antwort auf Frage 1 und
läuft daher am Ende (Brief 1 könnte parallel laufen, kollidiert aber mit den mypy-Waves in
denselben Dateien — siehe Wellenplan).

---

## Priorisierte Aufgabenliste

| # | Aufgabe | Ziel | Dateien | Effort | Token-Schätzung | Tier + Begründung |
|---|---|---|---|---|---|---|
| 1 | Review + Retro S142 nachholen | Fiel S142 dem Kontext-Korridor zum Opfer (Queue-Punkt 1); DoD-Review + Retro-Maßnahmenliste für S142 nachholen, bevor neue Arbeit beginnt | — (Review-Subagent liest Diff/Tests, keine Quelldateien fest) | S | ~20k | Reviewer-Subagent **Opus** (DoD-Review braucht Ganzheits-Urteil, kein Lookup) |
| 2 | Entscheidungsfragen an Stakeholder vorlegen | Frage 1 (FixD-Scope) + Frage 2 (Stratagem-Umfang) früh entscheidbar machen, bevor Kontext-Headroom sinkt | `docs/handoff/S143_planning.md` (dieses Dokument) | XS | ~0 (kein Subagent, nur Vorlage) | — (Koordinator direkt) |
| 3 | **Bugfix C — Wound/Hit-Threshold-Cap fehlt** | `resolve_attack_modifiers()` deckelt den Modifikator korrekt auf ±1, aber NICHT den resultierenden Zielwert auf `[2,6]` → S2 vs T5 mit −1 Wound-Debuff zeigt „Eff. 7+" statt „Eff. 6+", natürliche 6 wird als Fehlschlag markiert. Fix: `min(6, …)`-Cap in Hit- UND Wound-Zweig von `combat.py`; Anzeige-Notfall-Patch `min(modified, 7)` in `diceHtml.py` durch echten Cap ersetzen; unmodifizierte-6-Erfolgsregel für Hit/Wound ergänzen (fehlt aktuell komplett — kein `natural_six`-Pfad in `combat.py`/`attackMath.py`); Saves unverändert (dort gilt nur „unmodifizierte 1 = Fehlschlag", **kein** 6-Autoerfolg — `combat.py:252`/`diceHtml.py:186-192` bereits korrekt). | `src/gameMechanic/combat.py:197-212` (`resolve_attack_modifiers`), `src/uiLayout/diceHtml.py:23-30,60-61,147-148` (`_capped_modifier_threshold`, `_render_dice_roll_block`, `_render_dice_wound_block`) | M | ~30k | Sonnet (Regelumsetzung + Anzeige-Pfad, kein reiner Lookup; Regeltext bereits Haiku-verifiziert im Auftrag) |
| 4 | **Bugfix A — Insane Bravery: zweiter/inaktiver Spieler kann keine Einheit wählen** | Necrons α (inactive) bleibt auf „select an eligible unit" obwohl eine Einheit selektiert ist. Vermutlich verwandt mit Befund 5 (`_effect_gate_met` in `stratagemEngine.py` kennt nur die Desperate-Breakout-Gate-Form, Insane Bravery fällt durch → State wird fälschlich "ready" ohne Einheit), ABER das heute gemeldete Symptom ist umgekehrt (Karte bleibt "locked" TROTZ Auswahl, speziell beim inaktiven Spieler) — **erst Root-Cause verifizieren, ob dieselbe oder eine andere Ursache** (z. B. `_selected_state_key_for(player)`-Scoping für den inaktiven Spieler), dann fixen. Nicht ungeprüft „ist Befund 5" annehmen (CLAUDE.md Scope-Regel). | `src/gameMechanic/stratagemEngine.py` (`_effect_gate_met`), `src/uiLayout/gameProtocoll.py` (`_use_callback`, `_selected_state_key_for`) | S | ~25k (inkl. Root-Cause-Verifikation) | Sonnet (Root-Cause-Abgleich + Fix, kein reiner Lookup) |
| 5 | mypy-Ratchet `gameMechanic`-Rest | Baseline 28 → senken (11 Fehler in `gameMechanic/`) | `src/gameMechanic/*.py` (laut mypy-Report) | S–M | ~25k | Sonnet (Typing-Fixes brauchen Kontext-Urteil, kein reiner Lookup — Präzedenz S138–S141) |
| 6 | abilityEngine-Refactor-Recherche | Read-only Design-Vorschlag: Konsolidierungsmöglichkeiten jetzt, wo `stratagemEngine.py` existiert (S142 Option B) | `src/gameMechanic/abilityEngine.py` (nur lesen) | S | ~15k | Sonnet (Architektur-Bewertung, kein reiner Lookup) |
| 7 | mypy-Ratchet `uiLayout` | 17 Fehler senken | `src/uiLayout/*.py` (laut mypy-Report) | M | ~30k | Sonnet; **Selbst-Stopp bei ~20k prüfen** — falls > M abzeichnet, in diesem Schritt abbrechen und Rest als Folge-Brief zurückmelden |
| 8 | Roster-Loader-Test auf Glob umstellen | `backlog.md` §4d — Loader-Test soll neue Roster-Dateien automatisch erfassen statt Einzel-Pfade | `tests/gameObjects/test_loader.py` (oder Roster-Test-Äquivalent, Executor verifiziert genauen Dateinamen zuerst) | XS–S | ~10k | Haiku (mechanischer Test-Umbau, format-fix) |
| 9 | FixD-Ausführung (nur wenn Frage 1 beantwortet + Freigabe vorliegt) | Brief 1 (Compute/Render-Split, kein Layout-Change) starten; Brief 2 hinter Mockup-Gate; Brief 3 Spec-Nachzug — Details bereits in `docs/audit/plans/S142_fixD_resolution_tabs.md`, ggf. um Timing-Scope aus Frage 1 erweitert | `src/uiLayout/_common.py`, `src/gameMechanic/fightPhase.py`, `src/gameMechanic/shootingPhase.py`, `src/gameMechanic/gameState.py` | L (3 Teil-Briefs M+M+S, wie im Plan) | ~30k / ~30k / ~10k | Sonnet je Brief (bereits im Plan festgelegt) |

**Wellenplan (Parallelisierung / Konflikte):**
- **Welle 1 (parallel-sicher, unabhängige Dateien):** Aufgabe 3 (Bugfix C:
  `combat.py`/`diceHtml.py`), Aufgabe 4 (Bugfix A: `stratagemEngine.py`/`gameProtocoll.py`),
  Aufgabe 6 (abilityEngine-Recherche, read-only), Aufgabe 8 (Roster-Loader-Test).
  EINE Vollsuite zentral am Ende dieser Welle.
- **Welle 2:** Aufgabe 5 (mypy `gameMechanic`) — NACH Welle 1, weil Bugfix C `combat.py`
  ändert (Typing-Pass auf denselben Dateien vermeidet Merge-Reibung).
- **Welle 3:** Aufgabe 7 (mypy `uiLayout`) — NACH Welle 1, weil Bugfix C `diceHtml.py`
  ändert.
- **Aufgabe 9 (FixD):** NICHT parallel zu Welle 2/3 (`gameState.py`/`fightPhase.py`/
  `shootingPhase.py` überschneiden sich) — läuft sequenziell danach, zusätzlich hinter
  dem Mockup-Gate für Brief 2 (unverändert aus dem bestehenden Plan).

**Test-Budget-Hinweis:** EINE Vollsuite (`pytest --tb=short`, `timeout: 600000`, niemals
`run_in_background`) zentral am Ende jeder Welle — nicht pro Einzelaufgabe. Architektur-Gate
(`pytest tests/architecture/ --no-cov -q`) im selben Aufwasch.

---

## Entscheidungsfragen an den Stakeholder (NEEDS-DECISION)

**Frage 1 — FixD-Plan: Freigabe und Scope-Prüfung (Befund D von heute).**
Der bestehende Plan `docs/audit/plans/S142_fixD_resolution_tabs.md` löst NUR die
Breiten-Beschwerde (Box „geht über die kompletten Spielerbereiche" → wird durch die
Spalten-Aufteilung behoben). Die zweite Beschwerde von heute — die Box soll „einen
Screen FRÜHER" erscheinen, nämlich beim Deklarieren des Ziels einer Attacke, statt erst
im Hit-/Wound-/Save-Auflösungstab — deckt der Plan **nicht** ab. Gegenrecherche in
`docs/spec/design_system.md` §6.2 (Zeilen 279-284): Whirling Onslaught ist bewusst auf
den **Wound-Anker** gemappt („Mit Anker erreichbar, kein Handlungsbedarf") — das ist
aktueller Architektur-Stand, kein Bug. Eine frühere Anzeige (bei Ziel-Deklaration statt
beim Wound-Wurf) wäre eine **Architektur-Änderung des Anker-Schemas**, keine Layout-
Korrektur — verwandt mit dem bereits zurückgestellten „on_target außerhalb des Hit-/
Wound-/Save-Stacks"-Sonderfall (Paket 6, `design_system.md` Zeile 294-299, dort für
andere GOs benannt).
→ Bitte entscheiden: (a) FixD-Plan wie vorliegend freigeben (nur Breite/Spalten,
Timing bleibt wie heute — am Wound-Anker), (b) FixD-Plan freigeben UND einen Folge-Task
für „on_target-Anker vor Hit/Wound/Save" einplanen (Aufwand vorab unklar, eigene
Recherche nötig), oder (c) FixD-Plan zurückstellen, bis das Timing-Konzept mit
geklärt ist (dann läuft Aufgabe 9 diese Session nicht).

**Frage 2 — Stratagem-Umfang: Kodex vs. volle Wahapedia-9E-Quelle (Befund E von heute).**
„Swift Dismemberment" und „Weaponised Bodies" stehen belegt in
`docs/work/wahapedia_necrons/stratagems.txt:150,168` und
`data/wh40k_9e/necrons/stratagems.yaml:748,762` — die Wahapedia-9E-Quelle enthält auch
Supplement-/Army-of-Renown-Material (z. B. Annihilation Legion, War Zone Charadon), das
nicht im Kern-Kodex steht. Der Stakeholder findet sie im Kodex nicht.
→ Bitte entscheiden: (a) alle 9E-Wahapedia-Stratagems behalten (App bildet die volle
Turnier-/Erweiterungs-Bandbreite ab), (b) auf Kern-Kodex-Inhalte filtern (Datenpflege:
welche Einträge raus, nach welcher Quelle?), oder (c) behalten, aber mit Quell-Tag
kennzeichnen (z. B. `source: army_of_renown`), damit die UI optional filtern/ausblenden
kann. Keine Umsetzung ohne diese Entscheidung.

---

## Offene manuelle Verifikationen (weiterführen, nicht neu)

- B12b (3 Punkte): zentrale Liste zeigt „Used"+Suffix an anderen Angebotsstellen;
  Charge-Phase Fire Overwatch zeigt Suffix; Movement Advance-Reroll zeigt **keinen**
  Suffix (spec-konformer Randfall).
- Klan-Affinität + Emergency Disembarkation am Ork-Transport-Roster
  (`data/rosters/orks_transport.yaml`) — Emergency Disembark heute vom Stakeholder als
  „funktioniert" bestätigt; Klan-Affinität wurde nicht erwähnt → bleibt offen.
- Nach Aufgabe 3 (Bugfix C): manuelle Nachprüfung mit echtem S2-vs-T5-Whirling-Onslaught-
  Szenario, dass „Eff. 6+" korrekt erscheint und die natürliche 6 als Erfolg zählt.
- Nach Aufgabe 4 (Bugfix A): manuelle Nachprüfung, dass der inaktive/zweite Spieler eine
  Einheit für Insane Bravery auswählen kann und der Morale-Test korrekt automatisch
  besteht.

---

## Selbstprüf-Checkliste (Planner)

- [x] Befund A (Insane Bravery zweiter Spieler) im Plan verortet → Aufgabe 4
- [x] Befund B (Emergency Disembark) im Plan verortet → „Offene manuelle
      Verifikationen" (bestätigt funktionierend, Klan-Affinität bleibt offen)
- [x] Befund C (Wound-Panel Eff. 7+) im Plan verortet → Aufgabe 3 (Fundorte
      recherchiert und belegt: `combat.py:197-212`, `diceHtml.py:23-30,60-61,147-148`)
- [x] Befund D (Whirling-Onslaught-Box Timing/Breite) im Plan verortet → Aufgabe 9 +
      Entscheidungsfrage 1 (Scope-Lücke gegen `design_system.md` §6.2 belegt)
- [x] Befund E (Stratagem-Umfang) im Plan verortet → Entscheidungsfrage 2 (Zeilen
      748/762 in `necrons/stratagems.yaml` gegen Datei verifiziert)
- [x] Queue-Punkt 1 (Review + Retro S142) enthalten → Aufgabe 1, an erster Stelle
- [x] Kein Brief > Effort M (Aufgabe 9/FixD bleibt L, ist aber bereits im Vorplan in
      3 Teil-Briefs ≤ M gesplittet — unverändert übernommen, nicht neu als ein Brief
      vergeben)
- [x] Token-Schätzungen je Aufgabe vorhanden
- [x] STATUS-Marker Zeile 1 exakt `STATUS: NEEDS-DECISION`, keine Kommentar-Syntax
