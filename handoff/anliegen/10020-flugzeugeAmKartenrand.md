# Flugzeuge am Kartenrand

Form: Fragen
Von: Anforderungsautor
An: Stakeholder
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Deine Antwort auf Anliegen 9760 F1
verlangt eine Regelrecherche zu Flugzeugen am Kartenrand. Ergebnis:
- Kein *Modell* fährt über die Kante; Arbiter hält es dort an (`core_rules.txt:729`,
  [BEW-20.1](../../domaene/anforderungen/phasen/bewegung/loslassenNebenDerKarte.md)).
- Ein Flugzeug (AIRCRAFT) muss in der *Bewegungsphase* eine Mindeststrecke ziehen. Ginge sie
  über die Kante, wird es entfernt und zählt als zerstört, außer ihr spielt mit Strategic
  Reserves (`core_rules.txt:1073`).
- Bei einer Battle-forged-Armee darf ein Flugzeug in der *Bewegungsphase* über die Kante
  ziehen, wenn seine Bewegung reicht, sie zu berühren; dann kommt es in die Strategic
  Reserves, ebenso bei zu kurzer Mindeststrecke, ohne Kosten, und kehrt im nächsten Zug
  zurück (`core_rules.txt:3409`, `:3415`). In Matched Play beginnt jedes Flugzeug dort
  (`matched_play.txt:225`).
- Arbiter kennt bisher kein Flugzeug: Die *Datenblätter* der Orks und Necrons enthalten keins
  (`domaene/daten/katalog/`), es gibt keine Reserve und keine Mindeststrecke. Keine Etappe
  nennt Flugzeuge.

**Kosten.** A: eine Anforderung ohne Etappe, drei neue Begriffe (Vorschlag: *Flugzeug*
für AIRCRAFT, *Strategische Reserve* für Strategic Reserves, *Mindeststrecke* für minimum
Move), Tests erst, wenn der Planer sie einplant. B: nichts jetzt; die Recherche steht hier,
bis git sie archiviert.

**Gegenvorschlag.** Siehe Frage. Du musst nur den Buchstaben eintragen.

**Stellungnahme.**

**F1 · Wann beschreibe ich, was mit einem Flugzeug am Kartenrand geschieht?**
A: Jetzt, als Anforderung ohne Etappe mit den drei Begriffen; der Planer plant sie ein (Anliegen 9760 F1).
B: Erst wenn der Planer ein Flugzeug in eine Etappe nimmt, etwa mit dem Armeebau (Etappe 9) (Absicht 3).
Empfehlung: B, denn Orks gegen Necrons läuft bisher ohne Flugzeug, und erst die wesentlichen Funktionen entlang der *Phasen* (Absicht 3).
Antwort: C: Wir packen es in Etappe 3, wo wir einerseits ein passendes Flugzeug mit ovaler Base und zusätzlich die nötige Logik für die Bewegungsphase ergänzen.
