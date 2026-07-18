STATUS: REVIEW

# S166 — DoD-Review vor Abschluss-Commit

**Verdikt: GO.** Alle harten Gates grün, jede uncommittete Änderung ist durch die
Session-Inhalte (Retro-Überführung S165, B-122-Fix, B-123-Diagnose, Explodes-Mockup)
erklärt, keine unerklärten oder versehentlichen Änderungen, kein Regelverstoß, `src/`
diese Session unangetastet. Die offenen Punkte unten sind reguläre Abschluss-Nachzüge
(nach dem Review), kein NO-GO-Grund.

---

## Messwerte

- **pytest (voll, inkl. Coverage-Gate):** `2018 passed in 317.73s` · **Coverage 99.14 %**
  (Gate 99.0 % erreicht).
- **Architektur-Gate** (`tests/architecture/ --no-cov -q`): **8 passed**. INV-4b-Ratchet
  unverändert (6 Tokens / 16 Fundstellen / 3 Dateien) — kann nicht gestiegen sein, da `src/`
  nicht angefasst wurde.
- **Doku-/Akzeptanz-Gate** (`tests/docs/ tests/acceptance/ --no-cov -q`): **25 passed**.
  Regel-Ledger (impl. ohne Test) = 0, alle getestet-Refs existieren.

---

## Befunde

1. **Datenänderung konsistent (B-122).** `units.yaml:1106` Menhir-`wounds` 7→5, Erklärkommentar
   (Z. 1099) mitgezogen. Der direkt betroffene Test
   `tests/uiLayout/test_group_flow.py::test_front_group_hp_menhirs_then_szarekh` wurde von den
   alten Fixture-Zahlen (14/7/9) auf die neuen (10/5/7) nachgezogen — erwarteter Rot→Grün-Fix,
   kein stiller Verhaltensbruch (die Erwartungswerte folgen sauber aus 2×5 statt 2×7).
   **Empfehlung:** keine — sauber.

2. **Regelkonformität B-122 plausibel dokumentiert.** `S166_B122_VERIFIKATION.md` belegt den
   Wert 5 über drei unabhängige Quellen (wahapedia.ru, 40k.app, twinnedminiatures) und legt
   die Scraper-Lücke (lokaler Dump enthält nur Szarekhs Statszeile) offen. Nur der in allen
   drei Quellen übereinstimmende Wounds-Wert wurde übernommen; widersprüchliche Fetch-Werte
   (WS/BS/T/Save) bewusst NICHT angetastet — Scope-Disziplin korrekt. **Empfehlung:** keine.

3. **UI-Verifikation B-122 erfüllt DoD-Punkt 6 (für die YAML-Änderung).** Der Stakeholder hat
   in `S166_B122_VERIFIKATION.md` (Testfall 1+2 Befund) bestätigt, dass die Anzeige jetzt
   korrekt 26 gesamt bzw. 2/5 Frontmodell zeigt. Die zusätzlich beobachtete Fehlfunktion
   („26 Schaden zerstört die Einheit nicht, nur eine Subgruppe") betrifft NICHT den B-122-Wert,
   sondern den Schadenszuweisungs-Pfad = B-123. Damit ist die Statwert-Korrektur manuell
   verifiziert. **Empfehlung:** siehe Befund 6 (Marker/Status-Nachzug).

4. **Generisch-Constraint automatisch erfüllt.** `git diff --stat -- src/` ist leer — diese
   Session hat `src/` nicht berührt. Keine neuen Fraktions-Strings/-Checks möglich. **Empfehlung:** keine.

5. **B-123 ist reine Diagnose, kein Code-Fix — korrekt so abgegrenzt.** `S166_B123_DIAGNOSE.md`
   + `S166_B123_NACHDIAGNOSE.md` liegen als NEEDS-DECISION-Artefakte vor; die Nachdiagnose weist
   einen echten Fachlogik-Bug in `apply_damage` (Überschuss-Verwurf an Subgruppengrenzen, vom
   UI-`directed group`-Zweig für Mehrgruppen-Einheiten praktisch erzwungen) nach. Umsetzung ist
   S167-Stoff, die Stakeholder-Richtung (Subgruppen-Logik vereinheitlichen) ist notiert.
   **Empfehlung:** als S167-Task mit der vorgegebenen Richtung in den Backlog/Planner geben.

6. **Offener Abschluss-Nachzug — B-122-Status/Marker.** `backlog.md`/`backlog_details.md` führen
   B-122 auf `UI-Verifikation` (wartet auf Sichtprüfung), doch die Sichtprüfung ist laut
   `S166_B122_VERIFIKATION.md` bereits durch den Stakeholder erfolgt und bestätigt. Der
   Verifikations-Marker steht noch auf `STATUS: AWAITING-VERIFICATION`. **Empfehlung (Abschluss,
   nach Review):** B-122 (Anzeige-Anteil) auf erledigt setzen und ins `backlog_archive.md`
   überführen bzw. den Marker auf DONE ziehen; den separat gefundenen Zuweisungs-Bug einzig über
   B-123 weiterführen (ist bereits so erfasst). Kein NO-GO — klarer Abschluss-Punkt.

7. **Offener Abschluss-Nachzug — briefing.md.** `briefing.md` ist teilweise aktualisiert
   (Memory-Ergänzung `feedback_test_mandate` als vom Stakeholder abgelehnt geschlossen;
   S165_RETRO-Löschung dokumentiert), trägt aber noch keinen S166-Sessionstand/nächsten Schritt.
   **Empfehlung (Abschluss):** Stand (B-122 erledigt, B-123 Diagnose→S167, Explodes-Mockup V3
   offen mit 7 Korrekturwünschen) + nächster Schritt eintragen.

8. **Untracked Handoff-Artefakte.** 6 Screenshots (`Bildschirmfoto …png`) + `S166_MOCKUP_EXPLODES_V2.html`
   + die S166-Handoff-Markdowns liegen unversioniert in `docs/handoff/`. Sie sind gültige
   S166-Arbeitsprodukte (Mockup-Runde, Diagnosen). **Empfehlung (Abschluss):** bewusst
   entscheiden, ob die PNG-Screenshots mitcommittet werden (Binär-Ballast) oder nur die
   Markdown-/HTML-Artefakte — kein Review-Blocker.

---

## Für Retro relevant

- **Erstdiagnose B-123 nutzte einen UI-unerreichbaren Testpfad als Beweis.**
  `S166_B123_DIAGNOSE.md` schloss auf „(c) Mischfall / UI-Verwechslung, Pfad A ist bereits
  regelkonform — durch Tests belegt". Die `S166_B123_NACHDIAGNOSE.md` widerlegte das: Die
  Belegtests simulieren einen Zustand (`resolved=True` ohne `directed group`-Zwang), den die
  echte UI für Mehrgruppen-Einheiten wie den Silent King nie erreicht — es liegt ein echter
  Code-Bug in `apply_damage` vor. Prozess-Signal: Eine Diagnose, die „durch Tests belegt"
  argumentiert, muss zuerst prüfen, ob der getestete Pfad über die reale UI überhaupt erreichbar
  ist, bevor sie eine Fach-Schlussfolgerung („kein Bug") zieht. Kandidat für eine Retro-Maßnahme
  (z. B. Diagnose-Auftrag verpflichtet zur UI-Erreichbarkeitsprüfung des Beweispfads).
- **Budget-Kalibrierung greift.** Die diese Session in `agent_scopes.md`/`backlog.md` verankerte
  neue Effort-Skala (XS≈50k … M≈190k) ist der direkte Lerneffekt aus den S165-Fehlschätzungen —
  konsistent überführt, keine zweite Konvention entstanden.
