# Next Session

## Aktueller Stand (2026-06-06)

**Aktives Ziel:** Ziel 6 — UI-Overhaul, ArmyCard, Attackensequenz, Fähigkeiten-Integration

**6d-v3 implementiert** (2026-06-06): SVG-Würfelkomponenten, englische Begriffe, Rapid Fire Badge. ✅

---

## Beobachtete Abweichungen — Testsession 2026-06-06

### Würfel-UI (6d-v3) — Verbesserungen

**HIT + WOUND (allgemein):**
- Über den Würfeln fehlt eine Zeile mit Schwellenwerten als Text (`2+  3+  4+  5+  6+`), wobei die aktive Schwelle durch einen Rahmen hervorgehoben ist
- Von der aktiven Schwelle aus: senkrechte durchgezogene Linie nach unten als Ausrichtungshilfe
- Gestrichelte senkrechte Linie zwischen Würfel 1 (immer miss) und Würfel 2

**Modifier-Paare:**
- MWBD-Farbe falsch → soll **blau** sein (wie unitCard-Badges), nicht grün
- Würfelreihenfolge falsch: linker Würfel = Ausgangsschwelle, rechter = neue Schwelle (aktuell vertauscht)

**SAVE:**
- Waagerechte Schwellenwert-Reihe fehlt komplett (wie HIT/WOUND)
- Senkrechte durchgezogene Linie bei aktiver Schwelle fehlt
- Würfel und Effekte nicht vertikal aligned — kein tabellenartiges Layout
- Effective Save: Würfelreihe mit farbigem Rahmen erwartet (kein statischer Wert)
- Invuln-Zeile: ebenfalls Schwellenwert-Reihe + senkrechte Linie nötig

**7+ Save (unmöglich):**
- Roten [×]-Würfel rechts neben dem 6er-Würfel anzeigen (erscheint in mehreren Fällen, z.B. Gretchin, Warboss)

**Effective Save bei unmöglichem Wurf:**
- 6 rote [×]-Würfel statt Zahlenwert anzeigen

### Cover (Bug + Design)

- **Phasenbindung fehlt:** Light Cover + Dense Cover → nur Shooting; Heavy Cover → nur Fight
- **Dense Cover** gehört in den HIT-Block (−1 Trefferwurf), nicht in den Save-Block
- **Heavy Cover:** Effekt wird nicht angezeigt; erscheint fälschlicherweise in der gegnerischen Phase (Entweder-Oder-Bug des Dropdowns)
- **Dropdown ist falsche Komponente:** Mehrere Cover-Typen können gleichzeitig aktiv sein → Buttons / Checkboxen statt Dropdown

### Damage-Block (Bugs)

- **Mortal Wounds immer sichtbar:** Eingabe erscheint auch wenn die Waffe keine MW-Fähigkeit hat (Staff of Light, Immortals-Waffe) — Bug
- **Einzelmodell-Einheit:** Bei Ein-Modell-Einheiten (z.B. Warboss) darf kein Modellverlust-Counter erscheinen, nur Wunden-Eingabe

### Declaration-Block

- Fightphase: Deklarations-Block entspricht noch nicht dem 6d-v3-UI-Layout
- Nach Attacke: Defender-Anzeige (inaktiver Spieler) zu prominent gegenüber aktivem Spieler; entspricht noch nicht dem Deklarations-Bereich-Konzept aus dem Entwurf

### GOs / Stratagems

- GO-Liste unten angehängt ist falsch — GOs sollen als **Buttons direkt in der gameActionArea** erscheinen, kontextuell für aktiven und inaktiven Spieler
- Overwatch (Abwehrfeuer) als reaktive GO fehlt in der Charge Phase

### Fight Phase (struktureller Fehler)

- Inaktiver Spieler kann in der Fight Phase keine Nahkämpfe durchführen — **großer Regelfehler**
- Exakte Unterscheidung nötig: `charged` / `in_melee` / `fought`
- Ablauf 9E: erst alle `CHARGED`-Einheiten → dann abwechselnd aktiver/inaktiver Spieler
- GO "Counterattack" (Unterbrechung) muss einsetzbar sein
- → Regeln Fight Phase + Charge Phase nach Sammeln genau prüfen

### Heroic Intervention

- "Intervene"-Button erscheint zu früh (schon bei Zielauswahl, nicht erst nach erfolgreichem Charge)
- Nach Intervention: `INTERVENED`-Badge fehlt; `in_melee`-System wird nicht korrekt ergänzt
- Intervention = Charge-Bewegung: Warboss muss selbst wählen, welche Einheiten er dabei in Nahkampfreichweite bringt (können mehrere sein)

### Command Phase / Necrons

- **Living Metal:** Kann mehr als einmal pro Phase angewendet werden — sollte einmalig sein
- **Protocol-Effekte auf Living Metal / RP fehlen:** Protokolle können Living Metal und RP verbessern — Interaktion fehlt
- **Fixes Protokoll (6. Protokoll):** Kann aktuell jede Befehlsphase neu gewählt werden — muss für das gesamte Spiel festgelegt sein
- **Dynastiebonus:** Wenn Direktive durch Dynastiezugehörigkeit gilt, wird das noch nicht abgebildet
- Command Phase Anzeigereihenfolge ungeordnet — Regelkasten soll immer **ganz oben** stehen (in allen Phasen prüfen)

### WAAAGH!

- Call the WAAAGH! erzeugt keine Badge auf den unitCards der betroffenen Einheiten
- → Ork-Regeln prüfen: gibt es Einheiten, die von WAAAGH! nicht betroffen sind? Falls ja → unitCard-Logik

### Resurrection Orb

- Vermutlich nur auf **KERN-Einheiten** anwendbar — Regel nachlesen, Implementierung prüfen

### Skarabäen — Waffenfähigkeit fehlt

- Unmodifizierte Trefferwürfe von 6 verwunden automatisch — erscheint nicht in der UI
- Entweder Datenlücke in YAML oder Waffenfähigkeiten werden nicht geladen/angezeigt — potenziell großer Block

### Moralphase

- Gretchin-Sonderregeln möglicherweise nicht berücksichtigt → Regeln nachlesen

---

## Regelerkenntnisse (aus core_rules.txt + units_all.txt, 2026-06-06)

### Fight Phase — exakter Ablauf (core_rules.txt Z. 1941–1973)
- **Startet mit dem inaktiven Spieler** — beide Spieler wechseln sich ab beim Auswählen eligibler Einheiten
- **Charged Units Fight First:** Einheiten die diese Runde charged haben, kämpfen VOR allen anderen. Nicht-gechargede Einheiten können erst ausgewählt werden, nachdem ALLE gechargeden Einheiten aller Spieler gekämpft haben
- Eligible = innerhalb Engagement Range ODER hat diese Runde einen Charge Move gemacht
- Wenn ein Spieler keine eligible Einheiten mehr hat, kämpft der andere mit seinen restlichen Einheiten alleine weiter
- Nach Consolidation können neue Einheiten eligible werden

### Heroic Intervention — Timing + Logik (core_rules.txt Z. 1824–1848)
- Findet in **Schritt 2 der Charge Phase** statt — erst NACHDEM alle Charges abgeschlossen sind
- Nur **CHARACTER**-Einheiten können intervenieren
- Bedingung: nicht innerhalb Engagement Range, aber innerhalb 3" horizontal + 5" vertikal von einer feindlichen Einheit
- Bewegung: bis zu 3", muss näher zum nächsten feindlichen Modell enden
- → Button darf erst nach erfolgreichem Charge erscheinen, und nur für CHARACTER-Einheiten

### Cover — Regelkonforme Funktionsweise (core_rules.txt Z. 3791–3858)
- **Dense Cover:** −1 auf Trefferwurf bei Fernkampfwaffen (nur wenn Terrain ≥ 3" hoch zwischen Schütze und Ziel). Wirkt unabhängig davon ob das Ziel Cover bekommt — ist eine Shooting-Penalty, gehört in den HIT-Block
- **Light Cover:** +1 auf Rüstungswurf gegen Fernkampfwaffen (kein Invuln). Nur Shooting Phase
- **Heavy Cover:** +1 auf Rüstungswurf gegen Nahkampfwaffen, außer wenn das angreifende Modell diese Runde charged hat (kein Invuln). Nur Fight Phase
- Alle drei können gleichzeitig aktiv sein → keine Entweder-Oder-Logik

### FNP / Wounds ignorieren (rules_appendix.txt Z. 2214–2219)
- Gilt für **alle** erlittenen Wunden — normale Wunden UND tödliche Verwundungen
- Pro Wunde kann nur **eine** Ignore-Regel verwendet werden
- → FNP-Eingabe erscheint wenn Einheit FNP hat, unabhängig von Schadenstyp

### Gretchin — Moralphase (units_all.txt Z. 417)
- **Cowardly:** Solange kein freundlicher RUNTHERD innerhalb 6", −1 auf alle Combat Attrition Tests → fliehen leichter
- **Ld 4** — sehr niedrig, Combat Attrition Tests schon bei kleinen Verlusten kritisch
- Diminutive (Cover): +1 auf Rüstungswurf zusätzlich wenn Cover-Benefits (Fernkampf)
- → Moralphase muss prüfen: ist RUNTHERD in 6"? Wenn nein, −1 auf Attrition

### Noch nachzuschlagen (vor Umsetzung)
- Resurrection Orb — Zieleinschränkung KERN?
- WAAAGH! — welche Einheiten ausgenommen?
- Command Protocols — fixes 6. Protokoll Setup-Phase, Dynastiebonus, Effekte auf Living Metal/RP
- Skarabäen Waffenfähigkeit (6=auto-wound) — Daten oder Code?

---

## Session-Start — Empfohlene Reihenfolge

1. Diese Datei + `docs/goals/ziel6.md` lesen
2. Regeln nachlesen die noch offen sind (ResOrb, WAAAGH!, Protokolle, Skarabäen)
3. Einen Block aus der Task-Liste auswählen, Plan zeigen, Freigabe einholen

**Kritischster Block:** Fight Phase (inaktiver Spieler kämpft mit) — Regeln sind bekannt, Umsetzung braucht Plan.

**Schnellster Gewinn:** 6d-v3 Würfel-UI Fixes (Schwellenwert-Zeile, Modifier-Reihenfolge, 7+-Würfel) — alle in `_common.py`, gut isoliert.

---

## Weitere offene Tasks in Ziel 6

| Task | Priorität |
|---|---|
| 6d-v3: Schwellenwert-Zeile über Würfeln (HIT/WOUND/SAVE/Invuln) | hoch |
| 6d-v3: Senkrechte Linien + Alignment im Save-Block | hoch |
| 6d-v3: 7+-Darstellung mit rotem [×]-Würfel | hoch |
| 6d-v3: Modifier-Paar Farbe (MWBD=blau) + Reihenfolge fix | hoch |
| 6d-v3: Cover auf Buttons/Checkboxen + Phasenbindung | mittel |
| Damage-Block: Mortal Wounds nur wenn Waffenfähigkeit vorhanden | hoch |
| Damage-Block: Einzelmodell-Einheit nur Wunden-Eingabe | mittel |
| Fight Phase: inaktiver Spieler kämpft mit | kritisch |
| Fight Phase: charged/in_melee/fought-Ablauf regelkonform | kritisch |
| Heroic Intervention: Timing + in_melee-Logik | hoch |
| GO-Buttons in gameActionArea (kontextuell) | mittel |
| Overwatch als reaktive GO in Charge Phase | mittel |
| WAAAGH!-Badge auf unitCards | mittel |
| Living Metal: einmalig pro Phase | mittel |
| Protokoll-Effekte auf Living Metal/RP | mittel |
| Fixes 6. Protokoll für gesamtes Spiel | mittel |
| Resurrection Orb: KERN-Einschränkung | mittel |
| Skarabäen: Waffenfähigkeit (6=auto-wound) | mittel |
| Moralphase: Gretchin-Sonderregel | niedrig |
| 6d-v2: Tests Damage-Block + RP-Würfellogik | offen |
| 6e: CP-Doppelvergabe-Fix, collect_modifiers_for_phase() | offen |
| 6f: Ability-Badges auf unitCard | offen |
| 6g: Nach Reset keine alten Einträge im Battle Log | offen |
| 6h: Hardcoded Fraktionslogik herauslösen | offen |
| Daten-Review: once_per_battle enforcement | offen |
