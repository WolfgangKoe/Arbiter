# Backlog · Prozess

Zurückgestellt, bis ein Befund es auslöst. Was ausgelöst ist, wird ein Prozess-Item der Retro.
Ein Mechanismus entsteht erst bei beobachtetem Bedarf (Retro 3).

- Belegte Kriterien je Etappe zählen ([Kennzahlen](kennzahlen.md)): Kein Kriterium nennt
  seine Etappe; Frage an Planer und Anforderungsautor (Anliegen 691). Auslöser: Etappe 1
  ist erreicht, dann zählen alle Kriterien nicht mehr nur die laufende.
- `prozess/regeln.md` für den Regelumsetzer von der Sperre außerhalb der Prozessphase
  ausnehmen (Empfehlung in Anliegen 731). Auslöser: Ein Anliegen, das aufhält, braucht dort
  eine Zeile, und die Schreibgrenze sperrt sie.
- Ablauf, Fortschritt nach Anliegen 982 nachziehen: Abschnitt steht ab dem Schreiben der
  Datei, vor der Freigabe, alle Zeilen offen bis zum Beginn der Phase; Vertragszeile je Item
  in der Tabelle; dazu die Zeile in `prozess/regeln.md` (Mechanismus `standregeln/fortschritt.py`,
  `nächsteLage`, `alleOffen`; Tests in `standregeln/fortschrittTest.py`:
  `testDerPlanTrägtVorDerFreigabeDieTechnikzeilenAlleOffen`,
  `testDasReviewTrägtVorDerFreigabeDieDomänenzeilenDesFolgezyklusOffen`,
  `testJedesItemHatVorDenTestsDieVertragszeileDesArchitekten`; in der Zeile zu 490, Teil 1,
  entfällt „in Zyklus 1 keiner“, der Plan trägt ihn). Auslöser: `Freigabe Retro 6`, die
  Schreibgrenze sperrt bis dahin. Ausgelöst ist damit auch der Punkt davor (982).
- Hilfsmodule der Akzeptanztests: Jedes neue braucht ein Anliegen für die Liste
  `akzeptanzHilfsmodule` in `formregeln/benennung.py` (257, 336, 465, 580, 1240, 1290); die
  Zeile Benennung in `prozess/regeln.md` zählt sie ein zweites Mal auf (Wir 3). Vorschlag:
  Hilfsmodul ist jede Datei direkt im Akzeptanzordner ohne Testfunktion, die Aufzählung in
  `prozess/regeln.md` entfällt; Kritik vom Architekten (Architektur, T1). Auslöser:
  `Freigabe Retro 6`, die Schreibgrenze sperrt `prozess/regeln.md` bis dahin.

Mechanismus: nur Text, Höchstmaß `prozess/kennzahlen.md` (Backlog je Perspektive).
