STATUS: ANSWERED

# S152 — Offene manuelle UI-Verifikationen

Sammlung aller derzeit **durchführbaren** manuellen UI-Verifikationen (App:
`streamlit run src/app.py`, Port 8501) sowie der **blockierten** Punkte, die noch nicht
prüfbar sind. Ergebnisse bitte direkt hier eintragen (OK / Befund) — je Abschnitt beim
Feld „Ergebnis:".

Quellen: `.claude/tasks/briefing.md`, `docs/goals/backlog.md` + `backlog_details.md`,
`docs/goals/ziel7.md`, `docs/audit/plans/README.md` + `015-contextual-reactive-stratagems.md`,
`docs/spec/design_system.md` §6.2/6.3.

---

## Durchführbar jetzt

### 1. on_target-Anker Option A (B-008)

**Herkunft:** `docs/goals/backlog.md` B-008 / `backlog_details.md#b-008`. Code seit S146/S147
umgesetzt und getestet (Prio-Rang 2, S145-Prioritätenliste). Nur die Stakeholder-UI-Prüfung
steht noch aus.

**Prüfschritte:**
1. Necron- oder Ork-Roster laden, in eine Phase mit Ziel-Zuweisung gehen (Shooting oder
   Fight), eine Attacke gegen ein Ziel deklarieren.
2. Auf der Ziel-Kachel (`render_group_assignment` in `src/uiLayout/_common.py`) prüfen: Ein
   `on_target`-Stratagem (z. B. Quantum Deflection, Whirling Onslaught, Shadows of Drazak
   oder Efficient Disintegration, je nach Roster) erscheint **hier** und **nur hier**.
3. Weiter in die Hit-/Wound-/Save-Auflösung (`_render_resolution_tab`) gehen und prüfen,
   dass dasselbe GO dort **nicht** noch einmal auftaucht (die früheren dedizierten Hit-/
   Wound-/Save-Anker wurden abgeschafft, s. `docs/spec/design_system.md` Zeile 261–263,
   288–289).

**Erwartetes Verhalten:** Jedes `on_target`-GO erscheint genau einmal, an der Ziel-Kachel bei
der Deklaration — keine Dopplung, kein Fehlen in Hit-/Wound-/Save-Tabs.

**Ergebnis:** Passt alles, ich meine, dass ich das teilweise schon verifiziert hätte.

---

### 2. PSI Flow/Reset — 4 manuelle UI-Checks (B-009)

**Herkunft:** `docs/goals/backlog.md` B-009 / `backlog_details.md#b-009`. Code + Tests grün
seit S65 (Commits `cc75490`/`1d8b8ba`, 8 neue Tests). Betroffene Datei:
`src/gameMechanic/psychicPhase.py`.

**Prüfschritte:** Psychic Phase, eine Psi-Power manifestieren/deny lassen, dann:
1. **Undo deny nach erfolgreichem Deny** — Power denyen, danach „Undo deny" klicken →
   prüfen, dass die Power wieder im Ausgangszustand ist und das Deny-Budget der
   verteidigenden Fraktion zurückgebucht wurde.
2. **Aktiv-Reset → nächste Power wieder denybar** — nach Abschluss einer Power zur
   nächsten wechseln → prüfen, dass „Deny the Witch" wieder anwählbar ist (nicht durch
   die vorherige Power blockiert).
3. **Skip Deny verbraucht kein Budget** — bei einer Power „Skip Deny" wählen → Budget-
   Anzeige der verteidigenden Fraktion muss unverändert bleiben.
4. **Undo nach fehlgeschlagenem Deny** — Deny-Versuch scheitert (laut Tischwurf) →
   „Undo deny" klicken → Ausgangszustand wiederhergestellt, kein Budget dauerhaft verbrannt.

**Erwartetes Verhalten:** Alle 4 Fälle verhalten sich wie oben beschrieben; kein Fall, in
dem Deny-Budget dauerhaft „hängen bleibt" oder eine Power fälschlich gesperrt bleibt.

**Ergebnis:** Dafür brauche ich zwei Roster, mit denen ich das prüfen könnte. Welche soll ich hier nehmen. Voraussetzungen für einen Test müssen klar genannt und auch tatsächlich zur Verfügung stehen. -> Neuvorlage.

---

### 3. Emergency Disembarkation am Ork-Transport-Roster (B-074)

**Herkunft:** `docs/goals/backlog.md` B-074 / `backlog_details.md#b-074`. War zuvor mangels
TRANSPORT-Roster blockiert, jetzt möglich (Roster `data/rosters/orks_transport.yaml`, Evil
Sunz, Gunwagon TRANSPORT + Warboss + 10 Boyz + 10 Gretchin, Commit `cbaeeb2`).

**Prüfschritte:**
1. Roster `orks_transport.yaml` laden (Ork-Seite).
2. Den Gunwagon (TRANSPORT) im Spielverlauf zerstören lassen (Schaden bis 0 W zuweisen).
3. Prüfen, dass die Emergency-Disembarkation-Box (`_render_pending_emergency_disembarkation`
   in `src/uiLayout/_common.py`) in der Spalte des Ork-Spielers erscheint, sobald der
   Transport zerstört wird — unabhängig davon, in welcher Phase (Movement/Charge/Shooting/
   Fight) das passiert.
4. Box anwählen/verwerfen prüfen (CP-Kosten, „used"-Markierung).

**Erwartetes Verhalten:** Box erscheint zuverlässig beim TRANSPORT-Tod, in der richtigen
Spieler-Spalte, mit korrekter CP-Buchung.

**Ergebnis:** Positiv.

---

### 4. Fire Overwatch / Counter-Offensive — Funktion + Layout-Nachprüfung

**Herkunft:** zwei zusammengehörige, noch offene Punkte am selben UI-Element:

- **Funktion (B-087):** `docs/goals/backlog.md` B-087 / `backlog_details.md#b-087` — als
  „Blocked, braucht Plan 015" geführt. **Befund:** `docs/goals/ziel7.md` Zeile 43–47 sagt
  explizit, dass seit S130 „Manuelle UI-Prüfung inkl. Punkte 3+4 jetzt OFFEN und prüfbar"
  ist (Plan 015 hat Fire Overwatch + Counter-Offensive bereits kontextuell verdrahtet,
  `docs/audit/plans/README.md` Plan-015-Zeile). **Der Blocked-Status in `backlog.md` wirkt
  daher stale — bitte beim Ausfüllen entscheiden, ob B-087 nach dieser Prüfung entblockt/
  geschlossen werden kann.**
- **Layout-Freigabe (Plan 015, README):** Der Mockup-Gate vor Step 2 wurde in S130
  planmäßig übersprungen (direkte Umsetzung beauftragt) — die Kontext-Box (Bordered
  Container, Use/Pass-Buttons, Regel-Text-Expander, in der bestehenden Spieler-Spalte statt
  `gameActionsArea`) braucht eine **nachträgliche** Layout-Freigabe.

**Prüfschritte:**
1. Charge Phase: eine Einheit gegen eine gegnerische Einheit mit Fernkampfwaffe chargen →
   prüfen, dass die verteidigende Fraktion eine „Fire Overwatch"-Box in ihrer Spalte
   angeboten bekommt (`src/gameMechanic/chargePhase.py`, `_inactive_charge`), CP-Kosten
   korrekt, „used"-Markierung nach Klick.
2. Fight Phase: eine Einheit kämpfen lassen („fought") → prüfen, dass die gegnerische
   Fraktion danach eine „Counter-Offensive"-Box angeboten bekommt
   (`src/gameMechanic/fightPhase.py`, `_apply_counter_offensive`), inkl. CP-Buchung.
3. Bei beiden Boxen das Layout bewerten: Bordered Container, Use/Pass-Buttons, Regeltext-
   Expander — passt das zum bestehenden GO-Karten-Design (`docs/spec/design_system.md`
   §6.1) oder gibt es Abweichungen, die nachgebessert werden sollen?

**Erwartetes Verhalten:** Beide GOs erscheinen kontextuell zum richtigen Zeitpunkt, in der
richtigen Spalte, mit korrekter CP-/Used-Buchung; Layout wirkt konsistent mit dem übrigen
GO-Karten-Design.

**Ergebnis:** Das Verhalten wirkt auf mich noch etwas merkwürdig. Wann können beide Spieler diese Option wählen? Geht das auch um die Reihenfolge von Einheiten zu unterbrechen, die eine Angriffsbewegung durchgüführt haben? Dann wäre es nicht korrekt. Außerdem kann ich die GO anwenden und dann verschwindet die Karte, während sie beim gegnerischen Spieler erscheint. Es sollte aber erst dann triggern, NACHDEM EINE GEGNERISCHE EINHEIT GEKÄMPFT HAT. Also nochmal prüfen, ob das Verhalten Regelkonform umgesetzt ist. Des Weiteren hätte ich gerne eine konsistente UI-ANzeige. Solche Karten sollen nicht einfach erscheinen, sondern ausgegraut sein. Dann werden sie aktiv, sobald der trigger es erlaubt. ANders wäre es bei der Auswahl von Einheitn (z.B. Zielauswahl). Dann erscheint die KArte mit der Auswahl-karte. Das passt dann aber, weil es danach ausgraut, wenn die Option genutzt wurde. Bitte prüfen, ob im Backlog ein item ist, dass dieses inkonsistente Verhalten der GO-Karten schon adressiert und hier nochmal ein Refinement durchführen.

---

## Derzeit NICHT durchführbar (blockiert)

- **Spend-Guard** (tisch-aufgelöstes Stratagem ohne Einheit) — blockiert bis Roster-Builder
  (B-067) existiert. Quelle: `.claude/tasks/briefing.md`.
- **B-017 — GO-UI „Danach": manuelle UI-Gesamt-Verifikation** — blockiert, da erst nach
  Abschluss aller GO-UI-Pakete (B-013 bis B-016, alle noch ToDo) sinnvoll durchführbar.
  Quelle: `backlog_details.md#b-017`.
- **S142-FixD Brief 2 (Resolution-Tabs strukturell in Spieler-Spalten)** — Code noch nicht
  geschrieben, wartet auf Mockup-Freigabe (Design-Entscheidung zuerst). Quelle:
  `docs/audit/plans/S142_fixD_resolution_tabs.md`, `docs/audit/plans/README.md`.
- **B-010 — Protokoll-Buff-Audit-Anzeige-Rest (Eternal Guardian S SAVE-Hinweis)** —
  blockiert, hängt an Plan 015/026 Overwatch-Hit-Block-Override, der noch nicht gebaut ist.
  Quelle: `backlog_details.md#b-010`.

**Nicht mehr aufgeführt (spec-konform, kein Bug):** B12b-Rest / B-027 (Movement-Advance-
Reroll-Randfall, `unit_key` nicht durch `spend_stratagem` durchgereicht) — laut
`.claude/tasks/briefing.md` und `backlog_details.md#b-027` ein spec-konformer Randfall,
kein offener Verifikationspunkt.
