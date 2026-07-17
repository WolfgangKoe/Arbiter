STATUS: NEEDS-DECISION (Stakeholder: bitte prüfen und Ergebnis je Punkt vermerken — OK / Befund)

# S155 — Offene manuelle UI-Verifikationen (Stakeholder-Handoff)

App läuft auf http://localhost:8501 (Arbeitsbaum, Hot-Reload — Stand nach den S155-Commits).
Neue Ablaufregel S155: alle offenen UI-Verifikationen stehen immer hier im Handoff,
damit du sie unabhängig von der Session-Arbeit durchführen kannst.

## 1. Counter-Offensive-Timing + neuer Hinweistext (E1/B-087, Commit S155)

1. Fight Phase erreichen, je eine Einheit pro Seite im Nahkampf.
2. Erste Einheit (eigene Seite, am Zug) den Kampf komplett durchklicken.
3. **Erwartung:** In der Spalte der Gegenseite erscheint statt der Counter-Offensive-Box
   der Hinweis „Counter-Offensive becomes available once an enemy unit has fought."
   (regelkonform — Trigger ist explizit ein *gegnerischer* Fight, core_rules.txt:3256).
4. Danach die gegnerische Einheit fechten lassen.
5. **Erwartung:** Nach deren Fight erscheint die Counter-Offensive-Box bei der zuerst
   fechtenden Seite — sofern diese noch eine fecht-fähige Einheit hat.
   Hinweis: In einfachen 1-gegen-1-Sequenzen springt der Zug oft sofort zurück, dann
   bleibt die Box unsichtbar — bekannter Zusatzbefund, als eigenes Backlog-Item erfasst.

## 2. „used on ⟨Einheit⟩"-Suffix Advance-Reroll (B-027, Commit S155)

1. Movement Phase → Einheit wählen → „Advance".
2. Command-Re-Roll-GO-Karte nutzen.
3. **Erwartung:** Karte zeigt danach „Used" **mit** Suffix „used on ⟨Einheiten-Name⟩" (vorher leer).

## 3. „used on ⟨Einheit⟩"-Suffix Fire Overwatch (B-027, Commit S155)

1. Charge Phase → gegnerische Einheit als Charge-Ziel deklarieren.
2. Fire-Overwatch-GO-Box beim Verteidiger nutzen.
3. **Erwartung:** gleicher „used on"-Suffix bei der reagierenden Einheit.

## 4. Übernommen aus S154 (weiter offen)

- **Silent-King-Attacken-Defaults:** Fight Phase mit Silent King — Staff of Stars muss
  mit 3 Attacken, Scythes of Dust mit 4 Attacken vorbelegt sein (Weapon-Maximum).
- **PSI-Flow:** Testpaar `orks.yaml` (mit Psyker) vs. `necrons_test.yaml` (ohne) —
  Psychic Phase erscheint nur bei Roster mit Psyker; Details siehe
  `docs/handoff/S154_offene_entscheide.md` (Anleitung dort, Datei bleibt bis dahin liegen).
- **Weiter blockiert (unverändert):** Spend-Guard tisch-aufgelöstes Stratagem ohne
  Einheit → wartet auf Roster-Builder (B-067); B12b-Rest (Movement-Advance-Reroll-
  Randfall) → durch B-027 abgedeckt, Prüfung = Punkt 2.

Lifecycle: Wenn alle Punkte geprüft sind, Ergebnis hier eintragen → Marker auf ANSWERED;
Befunde wandern in `Stakeholder_Beobachtungen.md`/Backlog, Datei danach löschbar (DONE).
