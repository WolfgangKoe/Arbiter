STATUS: AWAITING-VERIFICATION (S171 — Testfälle 1–7 positiv ausgewertet; Rest-Punkt „Reset nach Confirm" = Nacharbeit d → `S171_d_ui_verifikation.md`; Datei löschen, sobald d grün)

# S170 T4-bc — Explodes: Menhir-Hinweis entfernt + Wurf-Karten-Reset — manuelle UI-Verifikation

Der Render-Code in `src/uiLayout/_common.py` ist aus der Coverage-Messung ausgeschlossen — diese manuelle Prüfung ist der Nachweis für die korrekte Funktion im echten UI. In S170 umgesetzt: Nacharbeit **(b)** Menhir-Hinweis entfernt, **(c)** Reset-Buttons auf der Explosionswurf-Karte. Später in S170 ebenfalls umgesetzt (nach Spec-Abnahme, in Specs überführt): **(a)** playerArea-Layout, **(e)** Phasenwechsel-Lifecycle, **(f)** Reset-Position — Prüfpunkte im Nachtrag unten. Folgesession: **(d)** Direkt-Apply + Reset-nach-Confirm.

---

## Testfall 1 — (b) Menhir-Hinweis weg

**Voraussetzungen:**
- App läuft auf :8501 (nicht neu starten).
- Neues Spiel, Necrons-Roster `data/rosters/necrons_1500pts_silent_king.yaml` laden, Gegner beliebig.

**Klickpfad:**
1. The Silent King auswählen.
2. Schaden-Zuweisung öffnen.
3. Solange Szarekh noch volle LP hat und die Triarchal Menhirs noch leben.

**Erwartung:**
- Es erscheint KEIN Hinweis „► Triarchal Menhirs zuerst vollständig zerstören." mehr.
- Die Lock-Logik selbst bleibt: Szarekh ist weiterhin erst wählbar, wenn die Menhirs zerstört sind.
- Der Teilschaden-Hinweis („… zuerst erledigen (N LP)") bei angebrochener Menhir-Gruppe bleibt unverändert sichtbar.

Antwort: Befund positiv.

---

## Testfall 2 — (c) Reset bei „Does not explode"

**Voraussetzungen:**
- wie Testfall 1.
- The Silent King vollständig zerstören (Menhirs + Szarekh auf 0 LP).
- Explodes-Kachel erscheint in der center-Spalte.

**Klickpfad:**
1. „Does not explode" klicken.

**Erwartung:**
- Info-Kasten „The Silent King does not explode." + darunter neuer Button **„Reset"**.
- Klick auf Reset → Kachel zeigt wieder die Binär-Wurf-Ansicht („Explodes!" / „Does not explode").

Befund: positiv. Die Position des Reset-Buttons in der Multi-Unit-Auswahl ist aber an keiner guten Stelle. Er sollte direkt unterhalb des blauen Hinweis-Kastens erscheinen.

---

## Testfall 3 — (c) Reset bei „Explodes!" (unbestätigte Auswahl wird verworfen)

**Voraussetzungen:**
- wie Testfall 2 (neuer Durchlauf).

**Klickpfad:**
1. „Explodes!" klicken.
2. Im Multi-Unit-Panel 1–2 Einheiten antippen und Schadenswerte eintragen.
3. NICHT „Confirm all" klicken.
4. „Reset" klicken.

**Erwartung:**
- Zurück zur Binär-Wurf-Ansicht.
- Die begonnene Ziel-Auswahl + eingetragene Werte sind verworfen.
- KEINE LP-Änderung an irgendeiner Einheit.
- Hinweis: Nach „Confirm all" (Schaden angewendet) erscheint dieser Reset dagegen NICHT (Korrektur nach Confirm = Folgesession-Arbeit d).

Befund positiv. Es gibt aber noch ein Problem. NACHDEM der confirm-Button gedrückt wurde VERSCHWINDET die ganze Auswahlliste. Danach muss ein Reset-Button erscheinen, der mich wieder in die Liste zurückbringt. Der kann unter dem Hinweis in der Kachel erscheinen, die nach Explosion kommt. Es fehlt noch die Anordnung der UnitCards.

---

## Pflicht-Checkpunkte

1. **Interaktion regelkonform?** — App würfelt selbst nichts; Reset ändert keine bereits angewendeten Schäden.

positiv.

2. **Komponente + Anker gemäß design_system.md-§?** — Kachel-Shell §1.5, Binär-Wurf §1.6 mit neuem Reset-Zustand, center-Spalte §1.9. (Layout-Breite wird erst mit Nacharbeit a korrigiert, hier NICHT bewerten.)

positiv, aber der Reset bei Erfolg bringt mich nicht zum Multi-UNit-Panel.

3. **Wortlaut-Familie?** — Button heißt exakt „Reset", §3.1.

positiv.

---

## Nachtrag T4-aef (S170) — vier weitere Prüfpunkte

Umgesetzt nach deiner Spec-Abnahme: (a) playerArea-Layout, (e) Phasenwechsel-Lifecycle,
(f) Reset-Position. Voraussetzung je Testfall wie oben (Silent King zerstören).

positiv.

### Testfall 4 — (a) Kachel nur in der Spieler-Hälfte
**Klickpfad:** Silent King zerstören, Kachel beobachten.
**Erwartung:** Binär-Wurf-Baustein + (nach Klick) blauer Info-Kasten erscheinen nur in der
linken Hälfte der gameActionsArea (first_player kontrolliert den Silent King) — nicht volle
Breite. Explodiert eine Einheit des zweiten Spielers: rechte Hälfte.

positiv.

### Testfall 5 — (a) Multi-Unit-Panel bleibt voll breit
**Klickpfad:** „Explodes!" klicken.
**Erwartung:** Multi-Unit-Panel weiterhin volle Breite, beide Armeen nebeneinander,
unterhalb der halbbreiten Kachel.

positiv.

### Testfall 6 — (e) Kachel verschwindet beim Phasenwechsel
**Klickpfad:** Kachel in beliebigem Zustand (offen/entschieden/bestätigt) → nächste Phase.
**Erwartung:** Kachel-Gruppe komplett weg und kommt in Folgephasen nicht wieder; Ereignis
steht im Protokoll („… explodes" / „… does not explode" / „explode damage confirmed — …").

positiv. Mich hat nur gewundert, dass der Royal Warden mit 4 LP durch die Explosion zerstört wurde. Ist das ein Bug? 

### Testfall 7 — (f) Reset-Position
**Klickpfad:** „Explodes!" klicken, Panel offen lassen.
**Erwartung:** Reset-Button direkt unter dem blauen Info-Kasten (nicht unter dem Panel).

positiv. Die Reset-Position ist nun korrekt. Nur der Reset-Buttton nach Confirm all ist noch nicht da, mit dem ich in den Multi-unit-panel zurück komme.
