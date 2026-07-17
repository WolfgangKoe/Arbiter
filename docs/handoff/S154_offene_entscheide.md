STATUS: ANSWERED (S154-Ende: E1 = neuer Befund → S155-Untersuchung; E2: R1+R2 ja, R3
verworfen — Regel gilt, wird aber nicht verregelt, kein Formal-Review wenn nichts fertig;
E3: Löschen freigegeben; E4: Vorschlag übernommen)

# S154 — Offene Entscheide (Stakeholder-Mailbox)

Lifecycle: Nach Beantwortung Marker auf ANSWERED; Datei behalten, bis alle Punkte in
S155 umgesetzt bzw. archiviert sind, dann löschen.

---

## E1 — B-087: Verhaltensbruch Counter-Offensive bestätigen (blockiert Commit ④)

**Was wurde geändert:** Das Counter-Offensive-Stratagem wurde bisher angeboten, sobald
*irgendeine* Einheit in der Fight Phase gekämpft hatte. Durch den Seitenwechsel nach jedem
Kampf erschien die Box damit faktisch immer direkt, nachdem die **eigene** Einheit des
reagierenden Spielers gefochten hatte (die Caption sagte wörtlich „You just fought").

**Regel (9E, wörtlich):** „Use this Stratagem **after an enemy unit has fought** in this
turn. Select one of your own eligible units and fight with it next."
(`docs/work/wahapedia_core_rules/core_rules.txt:3256–3259`, gleichlautend
`rules_appendix.txt:2570–2573`)

**Fix:** `src/gameMechanic/fightPhase.py` — Gate `_any_unit_fought(first, second)` ersetzt
durch `_enemy_has_fought(faction, first, second)`: geprüft werden nur noch die Kampf-Flags
der Gegnerseite. Fire Overwatch wurde ebenfalls verifiziert und ist **konform**
(Trigger nach Charge-Deklaration, vor dem Charge-Roll; `core_rules.txt:3243–3255`) — dort
kein Edit.

**Warum das eine Entscheidung braucht (Sicherheitsnetz-Regel):** Zwei vorher grüne Tests
in `tests/gameMechanic/test_fight_turn_advance.py` kodierten das alte — regelwidrige —
Verhalten und wurden durch drei neue ersetzt (darunter
`test_enemy_has_fought_false_when_only_own_side_fought`, der genau den Bug abdeckt).
Ersetzte Alt-Tests sind eine Nachricht aus einer früheren Session; deshalb keine stille
Anpassung, sondern diese Vorlage.

**Manuelle UI-Prüfung:** Fight Phase spielen — die Counter-Offensive-Box darf erst
erscheinen, nachdem eine *gegnerische* Einheit gefochten hat, nicht mehr direkt nach dem
eigenen Kampf.

**Optionen:** (a) Verhaltensbruch bestätigen → Commit ④ geht mit raus. (b) Ablehnen →
Revert von `fightPhase.py` + Testdatei, B-087 zurück in den Backlog mit Befund.
**Empfehlung: (a)** — Regelbeleg ist eindeutig, Ist-Verhalten war spielentscheidend falsch
(bot das Stratagem dem falschen Spieler zum falschen Zeitpunkt an).

Antwort: Aktuell kann ich die Counter-Offensive gar nicht sehen. Es ist komplett kaputt.

**Koordinator-Vermerk (S154-Ende):** Kein Commit. Fix konserviert in
`git stash` („B-087 Counter-Offensive fix – E1"); Arbeitsbaum zurück auf altem Verhalten.
S155-Auftrag: Befund untersuchen — Hypothese A: Der Stakeholder testete mit dem neuen Code
(die laufende App nutzt den Arbeitsbaum), und die Box erscheint regelkonform erst, nachdem
eine GEGNERISCHE Einheit gefochten hat — vorher erschien sie (fälschlich) sofort; „nicht
sichtbar" könnte das korrekte neue Verhalten in einer Situation ohne gegnerischen Fight
sein. Hypothese B: echter Bug im Fix (z. B. Flag-Reset pro Runde, Fraktionszuordnung).
Erst reproduzieren (Playwright/manuell mit beiden Seiten fechten lassen), dann entscheiden:
Stash anwenden + nachbessern oder verwerfen.

---

## E2 — Retro S153: Maßnahmen R1–R3

Kernbefund der Retro: In S153 blockierte das API-Session-Limit (Reset 20 Uhr) sowohl
Executor- als auch Reviewer-Starts; die Session wich auf einen offengelegten
script-gestützten Edit aus und ließ Review/Retro nach S154 nachholen.

- **R1 — kein zusätzlicher Prozess fürs API-Limit.** Der S153-Ausweg (offengelegter
  Skript-Edit + grüner Gate-Beleg) wird durch die bereits freigegebene Maßnahme **M2**
  (Werkzeug-Klausel in `agent_scopes.md`, Umsetzung S155) formalisiert; ein weiterer
  Prozess (z. B. Tageszeit-Planung um den Limit-Reset) wäre Overhead ohne belastbaren
  Nutzen. **Optionen:** zustimmen / andere Maßnahme benennen.
- **R2 — „91"-Kosmetik im Briefing.** Der S153-Review fand einen INFO-Befund: In
  `briefing.md` ist die Zahl „91" sprachlich der falschen Datei zugeordnet (91 =
  Detailabschnitte in `backlog_details.md`; `backlog.md` selbst hatte 91, nach
  Archivierung 87 Tabellenzeilen). Wird beim regulären Briefing-Update am S154-Abschluss
  mitkorrigiert. **Optionen:** so machen / lassen.
- **R3 — Grundsatz verankern:** „Ausstehendes Review/Retro = Punkt 0 der Folgesession"
  als ein Satz in `docs/governance/operating_model.md` (wurde S144 beschlossen, S154
  praktiziert, steht aber nirgends als Regel). Umsetzung S155 (Wind-down).
  **Optionen:** ja / nein.

R1 und R2 fein. Keine Regel ohne Ausnahme. D.h. nicht, dass wir die Ausnahme verregeln müssen. Wir halten uns an die Regel. Ich möchte aber keine Token um der Regel willen verschwenden, wenn in der Session nichts fertig geworden ist.

---

## E3 — B-053: `gretchin_mob` komplett löschen (Umsetzung S155)

**Befund (Haiku-Executor, S154):** Die Fähigkeit `gretchin_mob`
(`data/wh40k_9e/orks/unit_abilities.yaml:260–275`, Text „must take a Morale test if it
suffers any casualties") ist ein **8E-Relikt**. Das 9E-Gretchin-Datenblatt
(`docs/work/wahapedia_orks/units_all.txt:410–418`) kennt nur „Waaagh! Cowardly"
(Combat-Attrition −1, bereits korrekt als `cowardly` in der YAML) und „Diminutive".
Der generische Morale-Test gilt in 9E für alle Einheiten (`core_rules.txt:2089–2128`);
auch die Aussage zu Objective Secured im Eintrag ist falsch.

**Referenz-Check (Koordinator):** `grep -rn gretchin_mob data/ src/ tests/` → außerhalb
der Definitionsdatei **0 Treffer** — toter Dateneintrag, Löschung bricht nichts.

**Optionen:** (a) Löschen (Empfehlung; Umsetzung S155 inkl. Vollsuite-Beleg).
(b) Behalten und nur Text anpassen — nicht empfohlen, da die Fähigkeit in 9E schlicht
nicht existiert.

Dann löschen

---

## E4 — B-025: Umformulierung statt Schließen (Kenntnisnahme)

Playwright-Probe (S154): Zucken beim Slot-Wechsel reproduziert (7 Layout-Shift-Events,
CLS ≈ 0.29); der B1-Scroll-Fix wirkt weiter, es scrollt nichts. Ursache ist strukturell —
Streamlit rendert den Einheiten-Datenblock inkrementell, jedes Element löst einen Reflow
aus; eine feste `min-height` wäre je Einheit falsch dimensioniert. **Vorschlag:** B-025 im
Backlog umformulieren zu „strukturelle Verbesserung: Skeleton-Platzhalter mit fixer Höhe
oder Streamlit-Fragment-Isolierung", Priorität niedrig (rein kosmetisch). Umsetzung der
Umformulierung S155. **Optionen:** so übernehmen / Item schließen / Priorität anders.

---

## Kontext: bereits entschieden und erledigt (keine Aktion nötig)

- Review S153: **GO** (Gates grün, M2-Offenlegung korrekt; Datei lifecycle-gemäß nach
  Kenntnisnahme gelöscht, Kernaussagen hier konserviert).
- B-036: als Duplikat des S129-Fixes archiviert (Stakeholder-Entscheid S154).
- B-009-Neuvorlage: PSI-Flow-Testpaar = `orks.yaml` (Weirdboy castet) vs.
  `necrons_test.yaml` (Canoptek Spyder mit Gloom Prism denyt über den Wargear-Pfad).
  Anleitung: Weirdboy selektieren → Manifest-Roll (z. B. 8) → Deny-Karte erscheint in der
  Necron-Spalte → Deny-Roll → bei Durchkommen Smite-Schaden + Log prüfen; Perils separat
  mit Roll 2/12.
- B-068: Backlog-Zahlen waren vertauscht — regelkonform laut YAML + Wahapedia
  (`units_all.txt:236–237`): Staff of Stars max **3**, Scythe of Dust max **4**.
  UI-Prüfung: Silent King in der Kampfphase → Eingaben mit 3/4 vorbelegt.
