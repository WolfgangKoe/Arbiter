STATUS: AWAITING-VERIFICATION (S171 — a/b/c/e verifiziert; letzter offener Punkt d ist umgesetzt (Code), Verifikation → `S171_d_ui_verifikation.md`; Datei löschen, sobald d grün)

# S169 b2 — Explodes Pflicht-Trigger-Kachel — manuelle UI-Verifikation

Auftrag: B-028c1 Teil b2 (Pflicht-Trigger-Kachel-UI für Explodes). Spec:
`docs/spec/processes.md` P-16, `docs/spec/design_system.md` §1.5–§1.9/§3.1.
Render-Code (`_common.py`, `*Phase.py`) ist von der Coverage-Messung
ausgeschlossen — diese manuelle Prüfung ist der einzige Nachweis, dass die
Kachel im echten UI so erscheint wie spezifiziert.

## Voraussetzungen

1. App auf :8501 (bereits gestartet, nicht neu starten).
2. Neues Spiel starten, Necrons-Roster `data/rosters/necrons_1500pts_silent_king.yaml`
   laden (enthält The Silent King — trägt die reale Vengeance-of-the-Enchained-
   Ability, `effect.type: explode`, Schwelle 4+, Radius 2D6", Schaden D6).
   Gegner-Roster beliebig (z. B. ein Orks-Roster).
3. Silent King zerstören — am einfachsten: in der Shooting- oder Fight-Phase
   dem Silent King per Schaden-Buttons genug Wunden zuweisen, bis
   `unit_state.destroyed` greift (Szarekh + Triarchal Menhirs beide auf 0 LP).

## Klickpfad + erwartetes Verhalten

1. **Silent King wird zerstört** (beliebige Phase/Spielerseite — `trigger.phase:
   any`, `trigger.player: either`) → in der **center-Spalte** (`gameActionsArea`,
   nicht in einer der beiden Seitenleisten, §1.9) erscheint eine neue
   umrandete Kachel, Gold-Rahmen (aktiv bedienbar, §7.2/§6.5):
   - Titel **„The Silent King"**, Caption **„Explodes on 4+"** (§1.6, P-16
     Schritt 3) — kein CP-Suffix, kein `[Use]`-Button (§1.5: Pflicht-Trigger,
     keine GO).
   - Zwei Buttons **„Explodes!"** / **„Does not explode"** (exakter Wortlaut,
     P-16).
2. **Klick „Does not explode":**
   - Die Kachel bleibt sichtbar (verschwindet **nicht** kommentarlos, P-16
     Schritt 4/Regressionstest), zeigt jetzt einen blauen Info-Hinweiskasten
     (`st.info`, §1.8): **„The Silent King does not explode."** — genau ein
     Satz, keine Regel-Paraphrase (§3.1).
   - Kein Multi-Unit-Panel darunter.
   - Rahmen ist nicht mehr golden hervorgehoben (kein aktiver Baustein mehr).
3. **Klick „Explodes!" (Alternativlauf, neues Spiel/neuer Test):**
   - Info-Hinweiskasten: **„The Silent King explodes. Every unit within 2D6"
     suffers D6 mortal wounds."**
   - Darunter erscheint das **Multi-Unit-Ziel-Auswahl-Panel** (§1.7): beide
     Armeen nebeneinander (Necrons- und Gegner-Einheiten), je Einheit ein
     Toggle-Button; Silent King selbst taucht nicht als Ziel auf (ist bereits
     zerstört); zerstörte/in Reserve befindliche Einheiten fehlen ebenfalls.
   - Spaltenkopf über dem Zahlenfeld: **„D6 Mortal Wounds"**.
   - Eine Einheit antippen → Button zeigt **„✓ ⟨Name⟩"**, daneben erscheint
     ein Zahlenfeld (Default 0).
   - Wert eintragen (den am Tisch gewürfelten D6-Betrag), **„Confirm all"**
     klicken → LP-Balken der gewählten Einheit(en) sinkt live in der
     jeweiligen armyList-Sidebar (Bestandskomponente unitCard, §1.7); Panel
     verschwindet, Info-Kasten bleibt stehen.
   - **„Reset"** (statt Confirm) verwirft nur die Auswahl — keine
     Schadensanwendung, Panel bleibt offen für eine neue Auswahl.

## Bekannte Lücken (nicht Teil dieses Scopes)

- Der `auto_explode`-CP-Automatismus (Curse of the Phaeron, Baustein ② der
  Kachel-Gruppe) hat laut `design_system.md` §6.2-Schulden-Tabelle noch
  keinen Anker (Paket 5, generischer `on_destroy`-Hook) — in dieser Session
  bewusst nicht gebaut, Kachel zeigt daher nur Baustein ①③④.

## Pflicht-Checkpunkte (bitte einzeln freigeben/ablehnen)

1. **Interaktion regelkonform?** Zwei physische Tischwürfe (Explodes-Gate +
   Schaden), App würfelt selbst nichts, Reichweite wird nicht nachgezählt
   (P-16 Fachliche Einordnung, Wahapedia-Zitat).
   Antwort: Die grundsätzliche Mechanik funktioniert, sowohl mit "explodes" und "does not explode".
2. **Komponente + Anker gemäß §-Verweis?** §1.5 (Kachel-Shell)/§1.6
   (Binär-Wurf)/§1.7 (Multi-Unit-Panel)/§1.8 (Info-Kasten)/§1.9
   (center-Spalte, Sidebars unangetastet) — kein Vollbreite-Layout, keine
   GO-Karte für den Pflicht-Trigger selbst.
   Antwort: Die Anker sind an der richtigen Stelle. Allerdings erstreckt sich die Binärwurf-Kachel und der Hinweis des Infokastens über die gesamte gameActionArea, obwohl sich das nur in der playerArea des Spielers erstrecken sollte, dessen Einheit explodiert. Die GO-Karte wurde nicht angezeigt. Das Multi-Unit-Panel war korrekt.
3. **Wortlaut-Familie eingehalten?** „Explodes!"/„Does not explode",
   „Confirm all"/„Reset", genau ein Satz je Info-Ausgang (§3.1).
   Antwort: Ja auch hier wurde alles eingehalten und die Buttons funktionieren wie erwartet.


Ergänzungen:
- Den Hinweis-Block  mit "► Triarchal Menhirs zuerst vollständig zerstören." bitte entfernen. Den braucht es nicht!
- Es fehlen mehrere Reset-Buttons. Bei der Karte mit dem Wurf der Explosion selbst (sowohll bei Erfolg als auch Misserfolg) und auch nachdem man den verteilten Schaden mit Confirm bestätigt hat.
- Ein Verhalten ist ebenfalls noch nicht wie erwartet. Wird im Multi-Unit-Panel eine Einheit gewählt, wird nicht die entsprechende unitCard der betroffenen Einheit in der linken bzw. rechten Armylist ganz nach oben sortiert. Die Schadenspunkte auf die gewählte Einheit wird es durch "confirm" und dann für alle Einheiten gleichzeitig durchgeführt. Die Anforderungen war, dass dies beim zuweisen des Schadens direkt geschieht (selbst wenn die Einheit dadurch zerstört wird). Durch "Reset" sollte das entsprechend Rrückgängig gemacht werden können. Nach erfolgter Bestätigung durch "Confirm" sollte man einfach wieder in diesen Bildschirm mit demselben state zurückkehren können, bevor direktbevor bestätigt wurde. Es soll möglich sein, Zuweisungen korrigieren zu können, falls etwas falsch gelaufen ist. 