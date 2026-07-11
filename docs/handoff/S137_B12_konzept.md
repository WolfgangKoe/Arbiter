STATUS: NEEDS-DECISION

# S137/B12 — Konzept: GO-Zustand „used" mit Auslöser-Tracking

Lifecycle: Konzept-Handoff für S138. Nach Stakeholder-Entscheid (Fragen unten beantworten,
Marker auf ANSWERED) wird hieraus der Umsetzungsplan; nach Umsetzung Marker DONE und Datei
löschen. KEIN Code in dieser Session geändert.

---

## Grundannahmen (bitte bestätigen)

Diese Annahmen liegen dem ganzen Konzept zugrunde. Wenn eine nicht stimmt, bitte
widersprechen — dann ändert sich das Design.

1. **Die App würfelt nicht.** Alle Würfe passieren am Tisch. Die App erfasst manche
   Wurfwerte (Damage, Manifest, Deny), andere nie (Advance, Charge, Hit, Wound, Save).
2. **Einsatz pro Phase einmal.** Jede Gefechtsoption (GO) darf pro Spieler und Phase
   höchstens einmal eingesetzt werden; die CP-Abbuchung ist global pro Spieler.
   Once-per-battle-GOs sind zusätzlich fürs ganze Spiel gesperrt.
3. **Stakeholder-Entscheid S137:** Der Undo-Button erscheint NUR an der Stelle
   (Einheit/Anker), wo die GO tatsächlich angewendet wurde. Überall sonst, wo dieselbe
   GO in der Phase angeboten würde, ist der Einsatz unterbunden und der Button zeigt
   „Used" (deaktiviert).
4. **Scope-Erweiterung S137 (verbindlich):**
   a) Beim **Inline-Angebot** des Command-Re-Rolls (Attacken-Sequenz, Charge-Roll) gibt
      es **gar kein Undo** — ein Re-Roll ist nicht ungeschehen zu machen (so vereinbart).
   b) Once-per-Phase wird **erzwungen und sichtbar gemacht**: Command-Re-Roll beim
      Hit-Roll genutzt ⇒ Wound- und Save-Roll-Bereich zeigen „Used" (kein erneutes
      Angebot). Entsprechend in allen anderen Phasen.
5. **Undo auf Karten bleibt** (nur am Auslöser-Anker): Undo ist dort die Korrektur einer
   Fehlbuchung (falsche Karte gedrückt), kein „Wurf zurücknehmen". CP zurück, Effekt
   zurück — solange das Phasenfenster offen ist.
6. Command-Re-Roll ist heute die **einzige** GO, die an mehreren Stellen gleichzeitig
   angeboten wird. Das Design wird aber **generisch** gebaut (gilt für jede
   once-per-phase-GO mit mehreren Render-Stellen), keine GO-Namens-Checks in `src/`.

---

## 1 Ist-Zustand: Inventar aller Render-Stellen

Es gibt **drei gemeinsame Bausteine** und **18 Aufrufstellen**, die den Zustand einer
once-per-phase-GO anzeigen.

### 1.1 GO-Karten, direkt gerendert (Baustein: render_go_card in uiLayout/_common.py)

| # | Stelle | Datei:Funktion | Undo heute |
|---|---|---|---|
| 1 | Zentrale Stratagems-Liste (proaktive GOs, pro Spieler) | `src/uiLayout/gameProtocoll.py:_render_stratagem_column` | Ja — Karte zeigt „used" mit Undo, unabhängig davon, auf welche Einheit die GO wirkte |
| 2 | Advance-Re-Roll-Karte (pro selektierter Einheit, Bewegungsphase) | `src/gameMechanic/movementPhase.py:_render_advance_reroll_card` (Zustand: `_advance_reroll_state`) | Ja — **das gemeldete Problem**: nach Einsatz bei Einheit A zeigt die Karte auch bei Einheit B „used" mit Undo |
| 3 | Desperate-Breakout-Auflösungskarte | `src/gameMechanic/movementPhase.py:_render_desperate_breakout` | Ja — erscheint konstruktionsbedingt nur an der auslösenden Einheit (Flag an der Einheit), also faktisch schon „Undo nur am Auslöser" |

### 1.2 Reaktive GO-Boxen (Baustein: render_reactive_stratagem_box, rendert intern dieselbe GO-Karte kompakt)

Zustands-Logik: `_reactive_go_state` in `src/uiLayout/_common.py` — „verbraucht + Fenster
noch offen" wird pauschal zu „used" mit Undo, ohne zu wissen, WO der Einsatz stattfand.

| # | Anker | Datei:Funktion | Mehrfach-Anzeige möglich? |
|---|---|---|---|
| 4 | Fire Overwatch (Charge-Ziel deklariert) | `src/gameMechanic/chargephase.py:_inactive_charge` | Ja — pro deklariertem Ziel eine Karte |
| 5 | Cut Them Down (Fall Back) | `src/gameMechanic/movementPhase.py:_render_pending_cut_them_down` | Nein — Fenster-Marker wird bei Use gelöscht, Karte verschwindet |
| 6 | Counter-Offensive (Fight-Aktivierung) | `src/gameMechanic/fightPhase.py` (inactive-Zweig) | Nein (ein Fenster pro Aktivierungswechsel) |
| 7 | Manifest-Re-Roll (Psychic) | `src/gameMechanic/psychicPhase.py:_render_manifest_reroll` | Ja — drei Zweige, plus Deny-Anker (#8) in derselben Phase |
| 8 | Deny-Re-Roll (Psychic) | `src/gameMechanic/psychicPhase.py:_render_undo_deny_button` | Ja — teilt sich die Phase mit #7 |
| 9 | Emergency Disembarkation (TRANSPORT zerstört) | `src/uiLayout/_common.py:_render_pending_emergency_disembarkation` | Nein — Marker wird bei Use gelöscht |
| 10 | Damage-Roll-Re-Roll (Attacken-Sequenz) | `src/uiLayout/_common.py` (Damage-Block, Z. ~1405) | Ja — teilt sich die Phase mit den Inline-Angeboten #14–#18 |
| 11 | Hit-Anker (Verteidiger-Debuff-GOs) | `src/uiLayout/_common.py` (Hit-Block, Z. ~1844) | Ja — pro Waffen-Tab/Angriff |
| 12 | Wound-Anker (Verteidiger-Debuff-GOs) | `src/uiLayout/_common.py` (Wound-Block, Z. ~1883) | Ja — pro Waffen-Tab/Angriff |
| 13 | Save-Anker (Invuln-GOs, z. B. Quantum Deflection) | `src/uiLayout/_common.py` (Save-Block, Z. ~1917) | Ja — pro Waffen-Tab/Angriff |

### 1.3 Inline-Command-Re-Roll-Angebote (Baustein: render_inline_command_reroll in uiLayout/_common.py)

Kleiner Button neben einem Wurf-Ergebnis („Pull, not Push"). Heute: nach Einsatz oder bei
CP-Mangel ist der Button **komplett weg** — kein „Used"-Hinweis, kein Undo (gab es dort
nie).

| # | Anker | Datei (Aufrufstelle) |
|---|---|---|
| 14 | Charge-Roll | `src/gameMechanic/chargephase.py` (Z. ~114) |
| 15 | Hit-Roll (Angreifer zahlt) | `src/uiLayout/_common.py` (Z. ~1831) |
| 16 | Wound-Roll (Angreifer zahlt) | `src/uiLayout/_common.py` (Z. ~1873) |
| 17 | Saving Throw (Verteidiger zahlt) | `src/uiLayout/_common.py` (Z. ~1902) |
| 18 | Anzahl-Attacken-Wurf (Fight, pro Waffe) | `src/uiLayout/_common.py` (Z. ~2580) |

### 1.4 Wie Undo heute funktioniert (Buchhaltung)

- **Eine** kanonische Buchungs-Pipeline: `spend_stratagem` (CP abbuchen, Phasen- und
  Battle-Nutzungs-Sets füllen, Modifier registrieren, Effekt anwenden) und
  `undo_stratagem` (exakter Voll-Rollback) — beide in `src/uiLayout/_common.py`.
- Das Undo-Fenster ist phasengebunden: `stratagem_undo_visible` in
  `src/gameObjects/stratagem.py` — offen, solange die GO im Phasen-Nutzungs-Set steht;
  der Phasenwechsel (`_reset_phase_state` in `src/gameMechanic/game_state.py`) leert das Set.
- **Die Lücke:** Die Buchhaltung speichert nur DASS eine GO benutzt wurde (Set von IDs),
  nicht WO (welche Einheit, welcher Wurf). Deshalb kann kein Render-Ort unterscheiden,
  ob ER der Auslöser war — jede Stelle, die „used" erkennt, bietet Undo an.

---

## 2 Soll-Design

### 2.1 Auslöser-Tracking im Session-State

Neuer Session-State-Eintrag (Arbeitstitel): **`stratagem_use_anchor`** — pro Spieler und
GO-ID genau ein Datensatz mit:

- **anchor_id** — eindeutiger String des Anker-Orts. Jede Render-Stelle hat heute schon
  einen eindeutigen Schlüssel (z. B. `decline_key` der reaktiven Box, `reopen_key` des
  Inline-Angebots, Einheiten-uid der Advance-Karte) — genau dieser wird gespeichert,
  keine neue Schlüssel-Erfindung.
- **unit_key** (optional) — die Einheit, auf die die GO wirkte, für die Anzeige
  („used on ⟨Einheit⟩").

Geschrieben in `spend_stratagem` (neuer optionaler Parameter), gelöscht in
`undo_stratagem`, geleert beim Phasenwechsel zusammen mit dem Phasen-Nutzungs-Set
(zwei Stellen in `game_state.py`). Damit ist das Tracking automatisch genauso
phasengebunden wie das Undo-Fenster selbst.

Wichtig: `render_reactive_stratagem_box` kann die anchor_id **intern** aus seinen
vorhandenen Parametern (event + decline_key) bilden — die 10 Aufrufstellen aus §1.2
müssen dafür **nicht** angefasst werden.

### 2.2 Zustandsmodell-Erweiterung für design_system.md §6.1

Der bisherige Zustand „verwendet" spaltet sich in zwei. Neue Tabelle (5 Zustände):

| Zustand | Wann | Darstellung |
|---|---|---|
| ruhend | Trigger (noch) nicht erfüllt | gedimmt, `[Use]` disabled |
| bereit | Trigger erfüllt, CP reichen | Gold-Primary, `[Use]` aktiv |
| **verwendet-hier** | Use HIER gedrückt, Fenster offen | `[↺ Undo]` statt `[Use]` |
| **verwendet-anderswo** | GO diese Phase an ANDERER Stelle benutzt | gedimmt, Button zeigt **`Used`**, disabled; Header-Suffix „used on ⟨Einheit⟩" |
| gesperrt | CP fehlen / Voraussetzung weg | gedimmt, Grund als Suffix |

Technisch: `GoCardState` in `src/uiLayout/go_card.py` bekommt den fünften Wert;
`action_slot_text` liefert dafür „Used"; Farb-/Dimm-Zuordnung wie „gesperrt" (keine
neuen Farb-Token, §6.5 bleibt). Der Button in `render_go_card` wird für diesen Zustand
deaktiviert gerendert (nicht weggelassen — der Stakeholder-Entscheid verlangt den
sichtbaren „Used"-Text).

Die Zustands-Entscheidung treffen die drei bestehenden Mapper — sie bekommen den
Anker-Vergleich als zusätzliche Eingabe:

- `_go_state_and_reason` (zentrale Liste, `gameProtocoll.py`)
- `_reactive_go_state` (reaktive Boxen, `_common.py`)
- `_advance_reroll_state` (Advance-Karte, `movementPhase.py`)

Regel überall gleich: „verbraucht + Fenster offen" ⇒ **verwendet-hier**, wenn die
gespeicherte anchor_id zu dieser Render-Stelle gehört, sonst **verwendet-anderswo**.

### 2.3 Inline-Anker: „Used" statt verschwinden — und NIE Undo

Scope-Erweiterung (Grundannahme 4) umgesetzt in `render_inline_command_reroll`:

- **Kein Undo, nirgends** — auch nicht am Auslöser-Anker. Ein Re-Roll ist am Tisch
  passiert und nicht rückholbar. Der Auslöser-Anker zeigt nach dem Einsatz denselben
  Zustand wie alle anderen: „Used", deaktiviert.
- **Once-per-Phase sichtbar erzwungen:** Ist die GO diese Phase verbraucht, rendert
  jedes Inline-Angebot derselben Phase einen **deaktivierten Button mit Text „Used"**
  (statt wie heute komplett zu verschwinden). Beispiel: Command-Re-Roll beim Hit-Roll
  genutzt ⇒ Wound-, Save- und Anzahl-Attacken-Angebote zeigen „Used".
- Bei **CP-Mangel** bleibt das Angebot wie heute komplett unsichtbar (Pull-not-Push:
  nichts anbieten, was nie gedrückt werden konnte). Nur der Verbrauchs-Fall wird
  sichtbar — er trägt die Information „schon eingesetzt".
- Die Erzwingung selbst ist heute schon dicht (`stratagem_visibility` blendet
  Verbrauchtes aus) — neu ist die **Sichtbarkeit** der Sperre.

Damit gilt: Karten-Anker (§1.1, §1.2) = Undo nur am Auslöser; Inline-Anker (§1.3) =
gar kein Undo, nur „Used".

### 2.4 Undo-Semantik (Karten, unverändert im Kern)

Undo bleibt der bestehende Voll-Rollback (`undo_stratagem`): CP zurück, beide
Nutzungs-Sets bereinigt, registrierte Modifier entfernt, Effekt zurückgenommen —
**plus neu**: der Auslöser-Datensatz wird gelöscht, alle „verwendet-anderswo"-Stellen
kehren automatisch zu „bereit" zurück. Undo erscheint ausschließlich am
Auslöser-Anker; das Fenster schließt wie bisher mit dem Phasenwechsel.

Sonderfall unverändert: Anker, deren Fenster-Marker bei Use konsumiert wird (Cut Them
Down, Emergency Disembarkation), verschwinden nach Use ganz — dort gibt es weiterhin
keinen Undo-Ort (bestehendes, dokumentiertes Verhalten; siehe Entscheidungsfrage F3).

### 2.5 Phasen-Reset

Der Auslöser-Datensatz wird an denselben zwei Stellen geleert wie das
Phasen-Nutzungs-Set (`game_state.py`, Spielstart + Phasenwechsel). Kein neuer
Reset-Pfad, keine Leckage über Phasengrenzen.

---

## 3 Umsetzungsplan — drei Teil-Briefs (je ≤ Effort M)

Jeder Brief enthält seine Spec-Nachzüge und die manuelle UI-Prüfliste im selben Schritt
(DoD Punkt 7) sowie die Selbstprüf-Checkliste (Verdrahtung per grep belegen).

### Brief B12a — Fundament: 5. Zustand + Auslöser-Buchhaltung

- Dateien: `src/uiLayout/go_card.py` (GoCardState + action_slot_text + Styles),
  `src/uiLayout/_common.py` (render_go_card: disabled-Button; spend_stratagem/
  undo_stratagem: Anker-Datensatz + Abfrage-Helfer), `src/gameMechanic/game_state.py`
  (2 Reset-Stellen), `docs/spec/design_system.md` §6.1 (neue 5-Zeilen-Tabelle).
- Tests: HTML-Output-Tests für den neuen Zustand (Button-Text „Used",
  Dimmung/Border via go_card_container_style), Buchhaltungs-Tests
  (spend setzt Anker, undo löscht ihn, Phasen-Reset leert ihn).
- Noch keine sichtbare Verhaltensänderung an den Ankern (Mapper folgen in B12b) —
  gefahrlos einzeln committbar.
- Token-Schätzung: ~25k.

### Brief B12b — Karten-Anker: verwendet-hier vs. verwendet-anderswo

- Dateien: `src/uiLayout/gameProtocoll.py` (`_go_state_and_reason` + Aufruf),
  `src/uiLayout/_common.py` (`_reactive_go_state` + render_reactive_stratagem_box:
  anchor_id intern bilden und bei Use mitgeben), `src/gameMechanic/movementPhase.py`
  (`_advance_reroll_state` + Advance-Karte + Desperate-Breakout-Karte anchor_id).
  Die 10 Box-Aufrufstellen bleiben unberührt (anchor_id wird intern gebildet, §2.1).
- Tests: Mapper-Tests für alle drei Mapper (hier/anderswo/Fenster zu); Regressionstest
  für das Stakeholder-Szenario: Advance-Re-Roll bei Einheit A eingesetzt ⇒ Karte bei
  Einheit B ist „verwendet-anderswo" (kein Undo), Karte bei A zeigt Undo; nach Undo
  beide wieder „bereit".
- Manuelle UI-Prüfung: Bewegungsphase mit zwei advancenden Einheiten; Psychic-Phase
  Manifest- vs. Deny-Anker; Attacken-Sequenz Hit-Debuff-Anker über zwei Waffen-Tabs.
- Token-Schätzung: ~35k.

### Brief B12c — Inline-Angebote: „Used" sichtbar, kein Undo

- Dateien: `src/uiLayout/_common.py` (render_inline_command_reroll: Zustands-Logik als
  reine, testbare Funktion herausziehen [angeboten/used/versteckt]; „Used"-Button
  disabled rendern; anchor_id = reopen_key bei Use mitgeben),
  `docs/spec/design_system.md` §6.3 (Inline-Angebot: Used-Zustand, explizit KEIN Undo)
  und §6.4 (Wortlaut „Used" in die Use/Undo-Familie aufnehmen).
  Die 5 Aufrufstellen (§1.3) bleiben unberührt (reopen_key existiert schon).
- Tests: Tests der herausgezogenen Zustands-Funktion (verbraucht ⇒ used an ALLEN
  Inline-Ankern der Phase inkl. Auslöser; CP-Mangel ⇒ versteckt; sonst angeboten);
  Regressionstest „Hit-Roll genutzt ⇒ Wound-/Save-Angebot used".
- Manuelle UI-Prüfung: Shooting-/Fight-Attacke: Re-Roll beim Hit nutzen, dann Wound-,
  Save-, Anzahl-Attacken- und Damage-Bereich kontrollieren; Charge-Roll-Angebot.
- Token-Schätzung: ~25k.

Reihenfolge zwingend a → b → c (b und c bauen auf a auf; b und c untereinander
unabhängig). Gesamt ~85k zzgl. Review.

---

## 4 Offene Entscheidungsfragen

**F1 — Anker-Granularität: Einheit oder exakter Wurf-Ort?**
Der Entscheid sagt „bei der Einheit". Bei den Attacken-Ankern gehören aber mehrere
Wurf-Orte zur selben Einheit (Hit/Wound/Save im selben Waffen-Tab). Für Inline-Angebote
ist die Frage durch die Scope-Erweiterung erledigt (nirgends Undo). Für KARTEN-Anker
(z. B. Damage-Re-Roll-Karte, Hit-Debuff-Karte) schlage ich vor: Undo am **exakten
Anker** (Einheit + Wurf-Ort), nicht an allen Ankern derselben Einheit — das ist die
strengere, verwechslungsfreie Lesart.
**Default: exakter Anker.**

Antwort: Es soll auf jeden Fall an jedem Wurfort gezeigt werden, unabhängig von der Einheit. Aber an dem Ort, wo es eingesetzt wurde, soll eben "Undo" stehen und überall sonst "used". Wichtig wäre nur (und da kommt die Einheitvielleicht zum tragen), dass der Gegner die Option auch in der Phase einsetzen können soll. Es wäre fatal, wenn ich den Command-Reroll einsetze und dann ist es für den Gegner blockiert. Das darf nicht geschehen, aber sobald der Gegner diese Option eingesetzt hat, ist es bei ihm dasselbe Verhalten. Gibt es hier noch fachliche Klärungsfragen? Bitte vor der Umsetzung stellen.

**F2 — „used on ⟨Einheit⟩" als Header-Suffix bei „verwendet-anderswo"?**
Kleiner Zusatznutzen: Der Spieler sieht sofort, WO die GO hinging (und wo das Undo zu
finden ist). Kostet eine Zusatzangabe im Anker-Datensatz (unit_key), die B12a ohnehin
vorsieht.
**Default: ja, Suffix anzeigen (wenn eine Einheit bekannt ist).**

Antwort: Ja, fände ich sinnvoll. Hatte ichbei F1 schon gedacht.

**F3 — Fenster-konsumierende GOs (Cut Them Down, Emergency Disembarkation): unverändert lassen?**
Deren Karte verschwindet bei Use mitsamt Fenster — es gibt danach keinen Ort mehr für
Undo. Das ist heute so dokumentiert und kein Teil des gemeldeten Problems.
**Default: unverändert lassen (out of scope für B12).**

Antwort: Hmm, diese GOS kommen nicht so häufig zur Anwendung, weshalb eine unsaubere Logik nicht auffallen dürfte. Das fände ich aber nicht schön. Die Anwendung von GOs ist an sich für alle gleich! Ich kann jede GO nur einmal pro Phase pro Spieler anwenden. Und theoretisch gibt es pro Phase mehrere Möglichkeiten, an denen die GO eingesetzt werden kann. Dann braucht es da ein Anker mit demselben Verhalten wir unter F1 entschieden.

**F4 — Re-Roll-KARTEN (Damage/Manifest/Deny): Undo behalten?**
Die Scope-Erweiterung streicht Undo nur bei den INLINE-Angeboten. Die drei
Re-Roll-Karten-Anker behalten laut Koordinator-Vorgabe ihr Undo am Auslöser-Anker
(Lesart: Undo = Fehlbuchungs-Korrektur, nicht „Wurf zurücknehmen"). Falls der
Grundsatz „ein Re-Roll ist nicht ungeschehen zu machen" auch dort gelten soll, bitte
sagen — die Änderung wäre klein (Mapper liefert dann „verwendet-anderswo"-Darstellung
auch am Auslöser).
**Default: Undo auf Karten behalten, nur am Auslöser-Anker (wie entschieden).**

Antwort: An sich soll das Verhalten nicht nur auf INLINE-ANgebote beschränkt sein. Ist es nun so, dass der Anker in einer Karte unten in der Tab-Schalter-Liste ist,
 dann kommt es auch da nicht unbedingt vor. Wichtig wäre mir, dass wir Darstellung von Funktionalität unterscheiden. Jede GO sollte sich einem generischen Verhalten unterwerfen.
 Und zwar unabhängig davon, wie sie konkret angezeigt wird. Verstehst du, was ich meine?
