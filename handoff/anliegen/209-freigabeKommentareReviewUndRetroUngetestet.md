# Kommentare und Freigabe: Review und Retro ungetestet

209 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
**Befund.** Kritik am Code von e90d6ad (Anliegen 167, Teil 2). Erkennung der Kommentare,
Stellungnahme als nächste nicht leere Zeile, `Kommentar: .` und `Freigabe: ja` ohne Commit
stimmen mit dem Gegenvorschlag in 167; `python3 -m pytest prozess/pruefungen` grün (564),
Abdeckung 98,5 % / 96,9 %.

Die drei neuen Tests in `standTest.py` nutzen nur `handoff/plan.md`. Die Zeilen für Review
und Retro in `freigabeKommentare.artefakte` (Autor `Reviewer` und `Organisationsentwickler`,
Gegenstand `Review` und `Retro`) prüft kein Test.

Nebenbei, aus Vereinfachung und Effizienz:
- `plan.planDatei` gibt es schon; `freigabeKommentare` setzt den Pfad `handoff/plan.md` noch
  einmal selbst zusammen.
- `freigabeZuCommitten` liest jede Datei zweimal (`zyklus`, `zeilenDer`) und ruft je Artefakt
  `freigabeCommit` auf, also bis zu drei weitere `git log` je Stand. Der Stand läuft nach
  jedem Agent-Lauf.
- `dranAlsText(wurzel, kommentare=None)` mit `or {}`: Der einzige Aufrufer (`stand.py`) gibt
  `kommentare` immer mit. Der Parameter kann Pflicht sein.

**Kosten.** Ein Tippfehler im Rollennamen oder im Gegenstand fällt nicht auf. Dann meldet der
Stand eine Rolle, die es nicht gibt, oder einen Freigabe-Betreff, den `phasenfolge` nicht
erkennt, und die Retro wartet nach dem Commit weiter auf ihre Freigabe. Die Nebenpunkte
kosten wenig, wachsen aber mit Teil 3, der dieselben Dateien noch einmal liest.

**Gegenvorschlag.** Zwei Scheiter-Tests in `standTest.py`, beide mit fest ausgeschriebener
Erwartung, nicht aus `artefakte` abgeleitet: Ein Kommentar ohne Stellungnahme in `review.md`
ergibt „Dran: Reviewer (review.md)“. `Freigabe: ja` in `retro.md` ohne Commit ergibt
„Koordinator: Freigabe Retro 1 committen“, nach `repo.freigabe("Retro", 1)` nicht mehr. Die
Nebenpunkte nimmst du mit, wenn du Teil 3 baust, oder du lehnst sie mit Grund ab.

Erledigt, wenn beide Tests grün sind, `python3 -m pytest prozess/pruefungen` grün ist und der
Reviewer den Commit geprüft hat.
