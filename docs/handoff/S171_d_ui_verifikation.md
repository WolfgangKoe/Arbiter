STATUS: AWAITING-VERIFICATION

# S171 — UI-Verifikation Nacharbeit d (Direkt-Apply, Nach-Confirm-Reset, Sort-to-top, ↺-Glyph)

**Lebensdauer:** bis Stakeholder-Verifikation; bei Grün darf diese Datei UND `S169_b2_ui_verifikation.md` + `S170_b2bc_ui_verifikation.md` gelöscht werden (d war deren letzter offener Punkt).

Der Render-Code in `src/uiLayout/_common.py` ist aus der Coverage-Messung ausgeschlossen — diese manuelle Prüfung ist der Nachweis für die korrekte Funktion im echten UI.

---

## Kontextnotiz

Deine Testfälle 4–7 aus S170 waren alle positiv — danke. 

Deine Royal-Warden-Frage ist beantwortet: **kein Bug**. Die Explode-Fähigkeit des Silent King verursacht D6 Mortal Wounds **pro Einheit** im Radius (Wahapedia „Vengeance of the Enchained"). Der Royal Warden hat 4 LP; ein Wurf von 4–6 zerstört ihn regelkonform.

Dein Punkt „Reset nach Confirm all fehlt" ist genau die hier umgesetzte **Nacharbeit d**. Folgende Testfälle prüfen die vier neuen Features (Direkt-Apply, Nach-Confirm-Reset mit Panel-Rückkehr, Sort-to-top, einheitliche ↺-Glyph).

---

## Testfall 1 — Direkt-Apply (LP-Balken reagiert sofort)

**Voraussetzungen:**
- App läuft auf :8501.
- Neues Spiel, Necrons-Roster `data/rosters/necrons_1500pts_silent_king.yaml` laden.
- The Silent King zerstören → Explodes-Kachel öffnen → „Explodes!" klicken → Multi-Unit-Panel öffnet sich.

**Klickpfad:**
1. Eine beliebige Zieleinheit (z. B. Immortals) im Panel abhaken.
2. Im Feld neben der Einheit einen Mortal-Wound-Wert eintragen (z. B. 2).
3. Panel offen lassen (NICHT „Confirm all" klicken).
4. Beobachte die armyList-Sidebar auf der rechten Seite.

**Erwartung:**
- Der LP-Balken der ausgewählten Einheit sinkt SOFORT (nicht erst nach „Confirm all").
- Die LP-Zahl unter dem Balken wird aktualisiert.
- Wenn der Schaden die LP übersteigt, wird die Einheit grau/durchgestrichen angezeigt (visueller Indikator für Zerstörung), bleibt aber im Panel korrigierbar.

Befund: ____________________

---

## Testfall 2 — Undo vor Confirm (Panel-Footer-Reset)

**Voraussetzungen:**
- wie Testfall 1, Panel noch offen.

**Klickpfad:**
1. Eine oder mehrere Einheiten anhaken und Schadenswerte eintragen.
2. Den **„↺ Reset"-Button im Panel-Footer** klicken.

**Erwartung:**
- Alle Häkchen verschwinden.
- Alle eingetragenen Werte werden gelöscht.
- Die LP-Balken in der armyList kehren zu ihren ursprünglichen Werten zurück.
- Zerstörte Einheiten (grau angezeigt) werden wieder sichtbar.
- Das Panel bleibt offen und zeigt eine leere Auswahlliste.

**Zusatz — Teilweises Reset:**
3. Wieder mehrere Einheiten anhaken und Werte eintragen.
4. Häkchen EINER Einheit entfernen (ohne Reset-Button zu drücken).

**Erwartung:**
- Nur der Schaden dieser Einheit wird rückgängig gemacht.
- Die anderen angehakten Einheiten behalten ihre Häkchen und Werte.
- Ihre LP sinken weiterhin entsprechend.

Befund: ____________________

---

## Testfall 3 — Nach-Confirm-Reset (Panel-Rückkehr)

**Voraussetzungen:**
- Neuer Durchlauf (Reset alle Zustände oder neue Session).
- The Silent King zerstören, Explodes-Kachel öffnen, „Explodes!" klicken.

**Klickpfad:**
1. Im Multi-Unit-Panel 1–2 Einheiten abhaken und Schadenswerte eintragen.
2. **„Confirm all"-Button klicken** (Schaden wird angewendet).
3. Panel schließt sich.
4. In der center-Spalte erscheint ein blauer Info-Kasten (z. B. „X Mortal Wounds confirmed").
5. Direkt darunter oder seitlich neben dem Info-Kasten: **„↺ Reset"-Button** sichtbar.
6. Klick auf **„↺ Reset"**.

**Erwartung:**
- Panel öffnet sich wieder.
- Die zuvor angehakten Einheiten sind NOCH IMMER angehakt (mit ihren Werten).
- Die armyList-LP sind WEITERHIN reduziert (Schaden nicht automatisch rückgängig, nur die Anwendung wird rückgängig).
- Der Spieler kann die Werte korrigieren (editieren oder einzelne Häkchen entfernen) und erneut „Confirm all" klicken — oder mit Panel-Footer-Reset alles verwerfen.

Befund: ____________________

---

## Testfall 4 — Sort-to-top (Angehakte Einheit an Position 1)

**Voraussetzungen:**
- Explodes-Kachel offen, Multi-Unit-Panel sichtbar.
- armyList-Sidebar beobachten.

**Klickpfad:**
1. Eine Einheit im Panel abhaken (z. B. die 3. oder 4. in der Liste).
2. Beobachte die Reihenfolge in der armyList-Sidebar.
3. Die abhaken (Häkchen entfernen).

**Erwartung:**
- Solange die Einheit angehakt ist, steht ihre unitCard in ihrer Armee-Sidebar an **Position 1** (oben).
- Wenn das Häkchen entfernt wird, kehrt die Einheit zu ihrer ursprünglichen Position zurück (basierend auf Roster-Reihenfolge oder Destruktionsindex).
- Mehrfach anhaken/abhaken zeigt konsistentes Verhalten.

Befund: ____________________

---

## Testfall 5 — ↺-Glyph einheitlich

**Voraussetzungen:**
- Explodes-Kachel in verschiedenen Zuständen durchlaufen.

**Klickpfad:**
1. Alle Reset-Buttons im Kontext beobachten:
   - Wurf-Reset auf der Binär-Karte (vor Auswahl: „Does not explode" → Reset)
   - Wurf-Reset auf der Binär-Karte (nach Auswahl: „Explodes!" → Reset)
   - Panel-Footer-Reset (während Multi-Unit-Auswahl offen)
   - Nach-Confirm-Reset (nach „Confirm all" → Reset)

**Erwartung:**
- Alle vier Reset-Buttons tragen einheitlich das Glyph-Symbol **„↺"** (Rotation/Undo-Symbol).
- Alle heißen exakt **„↺ Reset"** (oder nur „↺", je nach Design — aber konsistent).
- Wortlaut folgt §3.1 der design_system.md.

Befund: ____________________

---

## Testfall 6 — Phasenwechsel (Regression)

**Voraussetzungen:**
- Explodes-Kachel in beliebigem Zustand (offen, mit Panel, nach Confirm, etc.).

**Klickpfad:**
1. Die Kachel verlassen.
2. Nächste Phase starten (z. B. via Button im Protokoll oder Sidebar-Navigation).

**Erwartung:**
- Die Explodes-Kachel ist NICHT mehr sichtbar.
- Das Ereignis steht im Protokoll („… explodes" / „… does not explode" / „damage confirmed — …" je nach Endstand).
- Wenn man zu einer früheren Phase zurückgeht: die Kachel erscheint NICHT wieder.
- **Regression-Check:** Verhalten wie in S170 Testfall 6 — kein neuer Bug bei Nach-Confirm-Reset.

Befund: ____________________

---

## Schluss

Diese Datei und ihre beiden Vorgänger (`S169_b2_ui_verifikation.md`, `S170_b2bc_ui_verifikation.md`) bilden ein zusammenhängendes Verifikations-Set für das Explodes-Feature. Sobald alle Testfälle hier grün sind, wird die Nacharbeit d abgeschlossen und kann zusammen mit den vorherigen Dateien gelöscht werden (Lebensdauer-Zeile oben).

Bei roten Befunden bitte im Slack oder per Mail Bescheid geben — dann wird eine Repair-Session eingeplant.
