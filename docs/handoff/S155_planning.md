STATUS: ANSWERED (S155: Freigabe erteilt inkl. Empfehlungen — E1-Hinweis bei Hypothese A ja,
B-028 → S156; Zusatz-Aufträge Stakeholder: Backlog-Bereinigung, Planner-Prio-Regel,
UI-Verifikationen immer als Handoff-Datei → Regeln in agent_scopes.md/operating_model.md verankert)

# S155 — Planning-Entwurf (freigegeben)

Datum: 2026-07-17

---

## Punkt 0 — Pflicht laut Briefing (vor allem anderen)

### 0.1 — E1: Counter-Offensive „gar nicht sichtbar" reproduzieren

Aus `docs/handoff/S154_offene_entscheide.md` (Koordinator-Vermerk, S154-Ende), wörtlich zitiert:

> **Hypothese A:** Der Stakeholder testete mit dem neuen Code (die laufende App nutzt den
> Arbeitsbaum), und die Box erscheint regelkonform erst, nachdem eine GEGNERISCHE Einheit
> gefochten hat — vorher erschien sie (fälschlich) sofort; „nicht sichtbar" könnte das
> korrekte neue Verhalten in einer Situation ohne gegnerischen Fight sein.
> **Hypothese B:** echter Bug im Fix (z. B. Flag-Reset pro Runde, Fraktionszuordnung).

**Vorgehen:**
1. `git stash apply` (stash@{0}: „B-087 Counter-Offensive fix – E1", bestätigt vorhanden,
   siehe Befunde unten) in einer Testumgebung/Zweig — App neu starten.
2. Manuell (oder Playwright) beide Seiten fechten lassen: (a) eigene Einheit fight zuerst,
   kein gegnerischer Fight → Box darf laut neuem Code NICHT erscheinen (Hypothese A prüft
   sich hier); (b) gegnerische Einheit fight → Box MUSS erscheinen.
3. Bestätigt sich (a)+(b) wie erwartet → Hypothese A: Fix ist korrekt, Stakeholder testete
   vermutlich Szenario ohne gegnerischen Fight. Weiter mit Stash anwenden + committen
   (Commit ④ aus E1 nachholen) + kurzer UI-Erklärtext/Tooltip erwägen (siehe offene Frage).
4. Erscheint die Box auch bei (b) nicht → Hypothese B: echter Bug in
   `_enemy_has_fought(faction, first, second)` (`src/gameMechanic/fightPhase.py`) — Flag-
   Reset pro Runde oder Fraktionszuordnung debuggen, Fix nachbessern, Tests anpassen.
5. Ergebnis in jedem Fall: Stash entweder anwenden+committen oder bewusst verwerfen
   (`git stash drop`) mit Befund zurück in den Backlog (B-087 neu aufmachen).

**Dateien:** `src/gameMechanic/fightPhase.py`, `tests/gameMechanic/test_fight_turn_advance.py`.
**Tier:** Sonnet (Debugging/Playwright-Verifikation, kein reiner Lookup).
**Modus:** Konsens (Verhaltensbruch-Bestätigung war laut E1 bereits „ja", aber Ausgang der
Reproduktion entscheidet über Commit vs. Revert — neuer Fakt, daher hier erneut geführt).

### 0.2 — B-036-Archivierung nachholen

Stakeholder-Entscheid „archivieren" liegt seit S154 vor (Duplikat des S129-Fixes), Umsetzung
scheiterte 2× an API 529 (reine Ausführungspanne, keine inhaltliche Frage). Nachholen:
Zeile aus `docs/goals/backlog.md` entfernen, Detail-Abschnitt „B-036 — Battle Log nach Reset
alte Einträge" (`docs/goals/backlog_details.md:764`) samt Fakten/Links nach
`docs/goals/backlog_archive.md` verschieben.
**Dateien:** `docs/goals/backlog.md`, `docs/goals/backlog_details.md`, `docs/goals/backlog_archive.md`.
**Tier:** Haiku (reine Lookup+Verschiebe-Aufgabe, Format bereits vorgegeben).
**Token:** ~5k.

### 0.3 — E3: `gretchin_mob` löschen (freigegeben)

Eintrag `gretchin_mob` in `data/wh40k_9e/orks/unit_abilities.yaml:260–275` löschen (8E-Relikt,
0 Referenzen außerhalb der Definition, Vollsuite-Beleg danach Pflicht).
**Dateien:** `data/wh40k_9e/orks/unit_abilities.yaml`; danach `docs/goals/backlog.md` (B-053-Zeile)
+ `docs/goals/backlog_details.md` (Detail-Abschnitt) nach `backlog_archive.md` verschieben.
**Tier:** Haiku (Lösch-Aufgabe + Vollsuite-Beleg, kein Ermessen).
**Token:** ~5k.

### 0.4 — E4: B-025 umformulieren

Backlog-Eintrag B-025 von „B11-Rest-Wahrnehmung nach B1-Fix" zu „strukturelle Verbesserung:
Skeleton-Platzhalter mit fixer Höhe oder Streamlit-Fragment-Isolierung" umformulieren,
Priorität niedrig (rein kosmetisch), Befund CLS≈0.29 aus der S154-Playwright-Probe referenzieren.
**Dateien:** `docs/goals/backlog.md` (B-025-Zeile), `docs/goals/backlog_details.md` (Detail-Abschnitt).
**Tier:** Haiku (Textänderung nach vorgegebener Formulierung).
**Token:** ~5k.

### 0.5 — Kurzes S154-Review

S154 war eine parallelisierte Session mit viel Fertiggestelltem (B-019/B-072, B-068,
B-039/061/082 archiviert, B-009-Testpaar benannt, B-087-Fix identifiziert). Gates laut
Briefing: Vollsuite 1878 passed / 99,14 % Coverage; Architektur+Doku+Acceptance 31 passed.
Kein Formal-Review mit eigenem Maßnahmenkatalog (R3 wurde vom Stakeholder verworfen — „keine
Token um der Regel willen verschwenden, wenn nichts fertig wurde"; hier ist aber vieles fertig
geworden, daher genügt diese Kurzfassung als Kenntnisnahme statt eines vollen Retro-Events).
**Kein separater Auftrag nötig** — wird vom Koordinator direkt als Teil von Punkt 0 vermerkt,
sobald 0.1–0.4 abgeschlossen sind.

---

## Priorisierte Aufgabenliste (nach Punkt 0)

### (a) S154-Restpaket (klein, sequenziell nach Punkt 0)

| Aufgabe | Ziel | Dateien | Token | Tier | Parallel? |
|---|---|---|---|---|---|
| M1+M2 (agent_scopes.md) | Werkzeug-Klausel + Retro-Formalisierung in EINEM Brief | `docs/reference/agent_scopes.md`, `docs/governance/operating_model.md` | ~15k | Sonnet (Doku-Integration mit Ermessen, kein reiner Lookup) | ja, disjunkt zu (b) |
| B-060 | CLAUDE.md-Token-Details nach `operating_model.md` Event 6 verlagern (Stakeholder-freigegeben S154) | `CLAUDE.md`, `docs/governance/operating_model.md` | ~5k | Sonnet (Text integrieren ohne Struktur zu brechen) | ja |
| B-027 | `unit_key`/uid durch `spend_stratagem` durchreichen (Advance-Reroll/Overwatch-Randfall) | `src/gameMechanic/*Phase.py`, `src/gameObjects/stratagem.py`, zugehörige Tests | ~5k | Sonnet (Code-Change) | ja |
| B-079 | DRY ±1-Cap-Helper in `diceHtml.py` | `src/uiLayout/diceHtml.py`, Tests | ~5k | Sonnet (Code-Change) | ja |

Diese vier sind untereinander unabhängig (verschiedene Dateien) → parallelisierbar in einer
Welle, sofern Kontext-Budget das zulässt (siehe Session-Budget unten).

### (b) Engine-Aufgaben (je ~35k, einzeln an der M-Obergrenze — nicht weiter splitten)

| Aufgabe | Ziel | Dateien | Token | Tier | Parallel? |
|---|---|---|---|---|---|
| B-056 | Quantum Shielding — fester Invuln 4+ statt additivem Modifier + S148-Anzeige-Bug | `src/uiLayout/_common.py`, `src/gameMechanic/combat.py`, `data/wh40k_9e/necrons/faction_abilities.yaml`, Tests | ~35k | Sonnet | ∥ mit B-098 (disjunkt) |
| B-098 Teil 2 | Kombi-Waffenprofile — `weapon_swap` + Kombi-Mechanik (Engine-Erweiterung, Teil 1 in `orks/weapons.yaml` bereits erledigt S152) | `src/gameObjects/weapon.py`, `src/gameMechanic/shootingPhase.py`, `data/wh40k_9e/orks/weapons.yaml`, Tests | ~35k | Sonnet | ∥ mit B-056 (disjunkt) |
| B-028 | „used on ⟨Einheit⟩"-Suffix auf alle reaktiven GOs ausweiten — **erster Teilschritt: reaktive Non-Stratagem-GOs zählen/auflisten**, erst danach Umsetzung | `src/uiLayout/_common.py`, `src/gameMechanic/abilityEngine.py`, `docs/handoff/S150_usedon_renderpaths.md` | ~35k | Sonnet | **NICHT** parallel zu B-056 (beide `_common.py`) |

**Reihenfolge-Konsequenz:** B-056 ∥ B-098 als gemeinsame Welle möglich. B-028 läuft danach
(oder in einer eigenen Session), sequenziell nach B-056 wegen der gemeinsamen Datei
`_common.py`.

---

## Session-Budget

Korridor: <150k, Wind-down ab ~120k, spätestens ~135k geordnet beenden; ab ~100k keine neue
Aufgabe mehr, solange Review/Retro noch aussteht; Review/Retro-Budget ~45k einplanen.

Realistische Einschätzung für S155:

1. **Punkt 0** (Reproduktion E1 inkl. Playwright/manuell, drei kleine Doku-Fixes 0.2–0.4,
   Kurz-Review 0.5): grob ~25–35k (E1-Reproduktion ist die einzige Aufgabe mit echter
   Ungewissheit — bei Hypothese B kann sie länger dauern).
2. **Restpaket (a)**, vier disjunkte Kleinaufgaben, parallelisierbar: grob ~30k gesamt
   (Koordination + Review der vier Diffs).
3. Nach Punkt 0 + (a): ca. 55–65k verbraucht → Headroom bis Wind-down (~120k) reicht für
   **eine** Welle aus (b): **B-056 ∥ B-098** (~35k je Subagent, parallel gestartet, Review
   danach).
4. **B-028 realistisch NICHT mehr in dieser Session** — nach (b)-Welle liegt der Verbrauch
   bereits im Bereich ~90–110k; ein weiterer ~35k-Task plus Review/Retro-Reserve (~45k)
   würde den Korridor sprengen. Empfehlung: B-028 auf S156 verschieben, es sei denn Punkt 0
   und (a) laufen deutlich günstiger als geschätzt und es bleibt sauberer Headroom
   **unter** 100k inklusive Review-Reserve.
5. Session-Ende regulär: `python tools/token_report.py --write` +
   `python tools/rotate_history.py --session 155 --summary "…"`, `briefing.md` aktualisieren,
   Commit.

---

## Offene Fragen an den Stakeholder

1. **E1-Ausgang bei Hypothese A:** Falls die Reproduktion bestätigt, dass die Box korrekt
   erst nach gegnerischem Fight erscheint (regelkonform, vorher war das Verhalten falsch) —
   reicht das als Erklärung für „komplett kaputt", oder soll zusätzlich ein kurzer
   UI-Hinweis/Tooltip ergänzt werden, der erklärt, warum die Box (noch) nicht erscheint?
2. **B-028-Verschiebung:** Passt die Verschiebung von B-028 auf S156 (Budget-Grund, siehe
   Session-Budget Punkt 4), oder soll B-028 unbedingt in S155 versucht werden auch auf
   Kosten eines knapperen Review/Retro-Puffers?

---

## Befunde

- **B-036 stale:** `docs/goals/backlog.md` führt B-036 weiterhin als aktive `ToDo`-Zeile
  (Zeile 65), obwohl der Stakeholder die Archivierung bereits in S154 freigegeben hat
  (Duplikat des S129-Fixes, siehe `S154_offene_entscheide.md` „Kontext: bereits entschieden").
  Grund laut Briefing: zweimaliges API-529-Scheitern bei der Umsetzung — reine
  Ausführungspanne, keine neue inhaltliche Frage. Wird in Punkt 0.2 nachgeholt.
- **Screenshot 2026-07-16 18:44 bereits erklärt:** `docs/handoff/Bildschirmfoto vom
  2026-07-16 18-44-05.png` ist referenziert in `docs/goals/backlog_details.md:1966+1970`
  als Beleg für B-101 (Tesla-Waffen-Badge zeigt „Extra Hits" statt „TESLA", Design-System-
  Abweichung). Kein verwaistes Foto, keine neue Beobachtung nötig — B-101 ist bereits im
  Backlog als eigenes Item geführt.
- **`Stakeholder_Beobachtungen.md` aktuell leer** („keine offenen Beobachtungen"; letzter
  Übertrag S152) — nichts Neues zu überführen.
- **Checkbox-Sync `docs/goals/ziel7.md`:** alle gesetzten Häkchen tragen einen
  Commit-/Session-Beleg inline (z. B. „S113, e031616", „S130: … (b5c774b, 2e3aa98)"); keine
  neue Stale-Checkbox gefunden. Offene Punkte (§6e `collect_modifiers_for_phase`, §6f
  Ability-Badges, §6h Kat1–3 neue Fraktionen) sind konsistent unmarkiert und decken sich mit
  dem aktiven Ziel-7-Scope aus dem Backlog-Kopf.
- **Keine Widersprüche Briefing↔Backlog** bei den geprüften IDs B-060, B-027, B-079, B-056,
  B-028, B-098, B-053, B-025 — alle als `ToDo` mit passendem Kontext in `backlog.md`
  vorhanden; nur B-036 ist der oben genannte Sonderfall.
- **git stash bestätigt:** `stash@{0}: On dev: B-087 Counter-Offensive fix - E1: Stakeholder
  meldet Box unsichtbar, S155 untersuchen` — genau der im Briefing benannte Stash, einzig
  vorhandener Eintrag (`git stash list` liefert nur diese eine Zeile).

---

## Selbstprüf-Checkliste

- [x] Gelesen: `.claude/tasks/briefing.md` (Abschnitt „Aktueller Stand" + „Nächster Schritt (S155)")
- [x] Gelesen: `docs/handoff/S154_offene_entscheide.md` (vollständig, Marker ANSWERED)
- [x] Gelesen: `docs/goals/backlog.md` (vollständige Tabelle, IDs B-036/B-060/B-027/B-079/
      B-056/B-028/B-098/B-053/B-025 einzeln abgeglichen)
- [x] Gelesen: `docs/reference/agent_scopes.md` (vollständig, Scope-Tabelle + Brief-Pflichten
      + Auftragsgrößen-Gate)
- [x] Gelesen: `docs/handoff/Stakeholder_Beobachtungen.md` (leer, nichts zu überführen)
- [x] Geprüft: `ls -la docs/handoff/` — Screenshot 2026-07-16 18-44-05 identifiziert und
      Referenz in `docs/goals/backlog_details.md` (B-101) per `grep` bestätigt; Foto selbst
      nicht geöffnet
- [x] Checkbox-Sync: `git log --oneline -15` gegen `docs/goals/ziel7.md`-Checkboxen abgeglichen
      (per `grep` auf `- [x]`/`- [ ]`) — keine neuen Stale-Checks gefunden
- [x] Geprüft: `git stash list` — bestätigt genau ein Eintrag, „B-087 Counter-Offensive fix – E1"
- [x] Zusätzlich gelesen (zur Verifikation, nicht in der Pflichtliste): `docs/goals/backlog_details.md`
      (B-036- und B-101-Abschnitte, `grep`-Treffer)
- [x] Bestätigt: **keine andere Datei als `docs/handoff/S155_planning.md` wurde geschrieben
      oder verändert** — kein Code, kein Memory, keine Backlog-Datei in diesem Schritt selbst
      angefasst (die in Punkt 0/(a)/(b) beschriebenen Änderungen sind Vorschläge für die
      Executor-Phase nach Freigabe, nicht bereits ausgeführt)
