STATUS: AWAITING-VERIFICATION

# S173 — UI-Verifikation Explodes-Panel (B-125 + B-126)

Render-Code (`_render_explode_target_panel` in `src/uiLayout/_common.py`) ist nicht
test-gedeckt → manuelle Prüfung durch den Stakeholder. Beide Fixes liegen an derselben
`st.number_input`-Zelle. Lebensdauer: bis Stakeholder-Verifikation; Ergebnis je Testfall
direkt hier kommentieren, dann räumt der Koordinator den Marker ab.

## Voraussetzung (beide Testfälle)

- Roster mit explode-Träger laden. Verifiziert vorhanden: **Ork Gunwagon** in
  `data/rosters/orks_transport.yaml` (`damage: "D6"`). Alternativ Necron Monolith/Doomsday Ark.
- Gegnerische Einheit(en) in Reichweite, damit Mortal Wounds zuweisbar sind.

## Testfall 1 — B-125: Wunden bleiben nach Reopen erhalten

**Klickpfad:**
1. Explode-Träger zerstören → Explodes-Kachel erscheint → „Explodes!".
2. Im Panel ein gegnerisches Ziel anhaken, **3** Mortal Wounds eingeben — der LP-Balken des
   Ziels sinkt live.
3. „Confirm all" → Panel schließt, Info-Kasten bleibt.
4. „↺ Reset" (Reopen) unterhalb des Info-Kastens.

**Erwartung:** Das Panel kehrt mit **angehaktem Ziel** und **Wert 3** zurück; die LP des Ziels
bleiben **reduziert** (nicht auf Voll/0 zurückgesetzt). Vor dem Fix wurden die zugewiesenen
Wunden beim Reopen auf 0 genullt (Lesart-A-Verstoß, §1.7).

## Testfall 2 — B-126: Mortal-Wounds-Cap pro Einheit

**Klickpfad:**
1. Bei einem **„D6"-Träger** (Gunwagon) im Panel versuchen, einen Wert **> 6** einzugeben.
2. Zum Vergleich (falls verfügbar) „D3"-Träger (Triarch Stalker/Night Scythe) und Festwert-Träger
   („1", Doomsday Ark) prüfen.

**Erwartung:** Das Eingabefeld begrenzt auf **6** (D6), **3** (D3) bzw. exakt **N** bei Festwert
(z. B. 1). Die Obergrenze kommt datengetrieben aus `ability.effect.damage` — kein Fraktions-String.

## Stakeholder-Rückmeldung

- Testfall 1: positiv.
- Testfall 2: positiv.
