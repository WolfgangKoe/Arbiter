# Karte und Ebene klarer benennen

Form: Fragen
Von: Anforderungsautor
An: Stakeholder
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Dein Auftrag: *Karte* meint auch armeeKarte und einheitenKarte, *Ebene* stört.
Nachtrag: „Die Umbenennung muss nicht ‚sofort‘ erfolgen. Lege ein Anliegen an und wir planen
es bewusst an eine passende Stelle.“ Es wartet daher, bis es eingeplant ist (F3).
- *Karte* ist im [Glossar](../../domaene/glossar.md) das Abbild des *Spielfelds* (ArbiterMap,
  [Ziel](../../domaene/ziel.md)). Die Doppelung kommt aus dem Englischen: map und card heißen
  beide Karte. armeeKarte und einheitenKarte sind Klassen des Design-Systems, keine
  Glossarbegriffe; fachlich heißt die Spalte *Armeeliste*.
- *Ebene* kommt aus ArbiterMap: „Auswahl auf Einheiten-Ebene / Modell-Ebene“
  (`interaction_map.md:376`). Bei uns ist es ein Hauptwort, das „ein *Modell* ist“.
- Der Regeltext kennt beide nicht; battlefield heißt *Spielfeld* (`core_rules.txt:452`).

**Kosten.** Am Bildschirm nichts Sichtbares; du liest die neuen Wörter in Anforderungen,
Plan und Review. Stellen per grep:
- Karte: Anforderungen 64 in 28 Dateien (QUE-2 heißt `karte.md`), Glossar 7 Zeilen, Ziel 2
  (ändert nur du), Items 2 Dateien, Frontend 34, Tests 112 (davon 49 Testnamen), Architektur
  18. armeeKarte und einheitenKarte bleiben.
- Ebene: Anforderungen 29 in 11 Dateien (AUF-20 heißt `ebene.md`), Glossar 5, Domäne im Code
  62 in 6 Dateien, Frontend 9, Tests 309 in 24 Dateien (davon 37 Testnamen), Architektur 33.
- Keine Prüfung wird zwischen den Phasen rot. Token: Domäne gering, Technik mittel
  (mechanisch).

**Gegenvorschlag.**
**F1 · Wie heißt das Abbild des Spielfelds?**
- A *Spielfeld* (Regeltext; ArbiterMap sagt „Feld“, „Feldkante“, `interaction_map.md:387`):
  *Karte* entfällt, die Zeile *Spielfeld* erhält „maßstäblich in Zoll, bildet den Spielstand
  ab, nicht den exakten Tisch“. Vorteil: Wort des Spielers, ein Begriff weniger, dein „Feld“
  steckt darin. Nachteil: QUE-2.2, 2.3, 2.5 („die *Karte* zeigt das *Spielfeld*“) werden
  umformuliert; du änderst das Ziel. **Empfehlung.**
- B *Feld* (dein Vorschlag, neu): kurz. Nachteil: zwei Begriffe für fast dasselbe (Feld,
  Spielfeld, Spielfeldkante); „Feld“ heißt bei uns auch Eingabefeld im Dashboard und Feld
  einer *Stelle* (Es 5).
- C bleibt *Karte* (ArbiterMap, Ziel): keine Kosten, die Doppelung bleibt.

Mit A oder B ist „Karte“ frei für die Komponenten, ins Glossar erst, wenn eine Anforderung
es braucht (Absicht 3).
Antwort: A

**F2 · Wie heißt, was Ziehen bewegt (bisher *Ebene*)?**
- A *ausgewähltes Modell* (ArbiterMap `model_selection.js`; Glossar *ausgewählt*, Anliegen
  980): *Ebene* entfällt. „deren *Ebene* ein *Modell* ist“ wird „mit einem *ausgewählten*
  *Modell*“, „die *Ebene* ist die ganze *Einheit*“ wird „ohne *ausgewähltes* *Modell*“, „macht
  es zur *Ebene*“ wird „wählt es aus“. Vorteil: Das siehst du am Bildschirm (nur dieses
  *Modell* gekennzeichnet, AUF-25.4), kein neuer Begriff. Nachteil: Die ganze *Einheit* steht
  als Verneinung. **Empfehlung.**
- B *Einheitenebene* und *Modellebene* (ArbiterMap `interaction_map.md:376`): nah am
  Vorbild, „Ebene“ bleibt.
- C bleibt *Ebene* (Anliegen 980): keine Kosten.
Antwort: B, "Ebene" wäre dann eine Klasse und Einheitenebene und Modellebene wären dann vielleicht UNterklasse? Naja, ich will dir da nicht viel hineinreden. Aber ich würde an irgendeiner Stelle zwishcen Einheit und Modell unterscheiden und da scheint mir hier die Unterscheidung in der Begrifflichkeit sinnvoll, ohne dass ich das Konzept der "Ebene" wie wir es verwenden, verwerfen möchte.  

**F3 · Wann?**
- A Domänenphase 10 (Ablauf, Domänenphase): Ich ändere Glossar und Anforderungen, Kennungen
  bleiben, da sich kein Sinn ändert; du das Ziel. Technikphase 10 benennt Code und Tests in
  einem Item um, mit Anliegen 7701 und 7601, die die *Auswahl* ohnehin ändern. Vorteil: Der
  Code wird einmal angefasst, die Stellen wachsen nicht weiter. **Empfehlung.**
- B nach Etappe 2 (Etappe 2): ungestört, aber mehr Stellen.
- C laufende Technikphase 9 (Plan 9): stößt mit vier parallel arbeitenden Rollen zusammen.

Annahme: Bis dahin bleiben *Karte* und *Ebene*; neue Kriterien schreibe ich mit ihnen.
Antwort: Am Ende der Technikphase 9 als Refactoring-Task. Wir unterbrechen die laufende Arbeit nicht, aber es kommt noch vor dem nächsten Zyklus.

**Stellungnahme.**
