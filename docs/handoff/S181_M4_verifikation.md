STATUS: AWAITING-VERIFICATION

# S181 M4 Verifikation: Necron Aura-Spender (Lokhust Lord hinzugefügt)

Änderung: Necron Test-Roster (`data/rosters/necrons_test.yaml`) erhielt einen zweiten Aura-Spender (**Lokhust Lord**) zusätzlich zum existierenden Skorpekh Lord. Beide tragen die Aura **United in Destruction** (reroll_wound_1 für DESTROYER CULT).

---

## Verifikations-Felder

### Voraussetzung
Lade das Necron-Test-Roster in die App (`Testspiel` mit Fraktion `Necrons`).  
Verifiziere, dass die Einheitenliste beide anzeigt:
- Skorpekh Lord (1 Modell)
- Lokhust Lord (1 Modell)

### Klickpfad
1. Wähle im **Feld** die Skorpekh Destroyers (6 Modelle mit Reap-Blades, im Roster enthalten).
2. Gehe in die **Kampfphase**.
3. Initiiere einen **Wundwurf** für eine Skorpekh Destroyer (Button: z.B. „Roll 1d6 wound roll").
4. Beobachte die **Hinweiskachel** (rp_col-Muster, halbe Breite), die neben dem Wurfergebnis oder in der Aktion-Info angezeigt wird.

### Erwartung
Die Hinweiskachel zeigt den Text: **„…of Lokhust Lord or Skorpekh Lord."** (exakt diese Wortfolge und Reihenfolge, wie sie der Code erzeugt).  
Die Kachel bleibt **halbbreit** (rp_col-Layout, design_system §1.9.1 — nicht vollbreit, nicht schmaler).

---

## Checkpunkte (vor Abschluss prüfen)

- [x] **Kachel erscheint:** Hinweiskachel ist in der Kampfphase beim Wundwurf sichtbar
- [x] **Beide Spender genannt:** Der Hinweistext nennt beide Lords in der Reihenfolge „Lokhust Lord or Skorpekh Lord" (exaktes Wortlaut-Match)
- [x] **Halbbreit (rp_col):** Kachel ist nicht vollbreit und nicht schmäler als rp_col-Standard
