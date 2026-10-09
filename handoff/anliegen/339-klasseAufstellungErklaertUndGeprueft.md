# Die Klasse Aufstellung: Gedanke, Prüfung, Umbau

339 · Fragen · von Architekt (Technik) → Stakeholder · Runde 1/3 · offen

Legende: Status im Kopf · als Empfänger angenommen, rückfrage, abgelehnt · als Absender erledigt, offen (neue Runde) · unter einer Frage `Antwort: .` (Empfehlung), `Antwort: B` oder `Antwort: <Text>`

## Runde 1
**Befund.** (gekürzt, ganz in 3dd50f9) `Aufstellung` ([aufstellen.py](../../technik/arbiter/domaene/phasen/aufstellen.py))
ist der Schiedsrichter der Phase: Nur sie hält den Stand und ändert ihn nur über Handlungen,
die erst alle Sperren prüfen ([Architektur](../../technik/architektur.md) D2, D3). Sie mischt
aber Regeln der Phase (Gewinner, Zone, *Einheit in Aufstellung*), allgemeine Regeln des
*Setzens* (*Base überdeckt*, *Nahkampfreichweite*, `core_rules.txt:450`) und Bedienzustand
(*ausgewählt*); *an der Reihe* kehrt im Nahkampf wieder (`:1941`). Modul und Klasse haben
keinen Docstring.

**Kosten.** Ohne Umbau wächst mit AUF-5.5 die Auswahl in die Klasse, und Etappe 2 löst
*Nahkampfreichweite* und *Stellen* unter Zeitdruck heraus.

**Gegenvorschlag.**

**F1 · Umfang des Umbaus.** A nur Docstrings und Ordnung. B (Empfehlung) A, dazu die Auswahl
als eigene Klasse, *Nahkampfreichweite* neben `baseÜberdeckt`, Startprüfung zu
`Ausgangslage`, „Modell → Einheit“ zu `Armee`. C B und schon jetzt eigene Klassen für *an der
Reihe* und *Stellen*.

Antwort: .

**F2 · Anforderung.** Der Anforderungsautor überarbeitet gerade `aufstellen.md`. Soll ich
ihm vorschlagen, AUF-3.4 als allgemeine Regel des *Setzens* nach QUE-1 zu verschieben?
A ja (Empfehlung), B nein, sie bleibt bei der Aufstellung.

Antwort: Das würde ich nochmal infrage stellen. s. Stellungnahme.

**Stellungnahme.** Könntest du dich bitte mit dem Anforderungsautor abstimmen, wie wir es am besten machen? Ich habe 339 kommentiert und ihr sollt natürlich nicht unterschiedliche Strukturen aufbaut. Ich möchte, dass wir hier eine gemeinsame "Spiegelstruktur" aufbauen und die Einzelteile sollen lesbar und gut strukturiert sein. Daher finde ich F1-B einen guten Schritt. Schau bitte, was aus den Regeln heraus zusammengehört. Als Modell -> Einheit -> Armee könnte gut passen. Base und Nahkampfreichweite könnte auch irgendwie zusammengehören. Aber ich verstehe nicht viel davon, wie man Klassen, deren Eigenschaften, Methoden und Vererbungen gut aufbaut, damit alles gut strukturiert lesbar ist und so etwas wie SOLID erfüllt bleibt.

**Klärung.** F1 B gilt. Was keinen neuen Begriff braucht, baut der Implementierer jetzt
([344](344-aufstellungLesbarOhneNeuenBegriff.md)). Den Spiegel stimme ich mit dem
Anforderungsautor ab ([345](345-spiegelZwischenAnforderungUndCode.md)); F2 entscheidet er dort mit.
Mein Vorschlag, aus den Regeln:
- Spiegel: Ordner und Dateiname einer Anforderung kehren als Testdatei und, trägt sie Regeln,
  als Modul der Domäne wieder: `phasen/aufstellen/reihenfolge.md` → `reihenfolgeTest.py`,
  `reihenfolge.py`. Anzeige und Bedienung leben in `web/`.
- Modell → Einheit → Armee passt: Die *Armee* hat *Einheiten*, die *Einheit* *Modelle*, das
  *Modell* eine *Base*. Das ist „hat ein“, keine Vererbung. Vererbung lohnt erst, wenn
  mehrere Arten dieselbe Frage verschieden beantworten: runde und ovale *Bases* (Etappe 6).
- *Base überdeckt* und *Nahkampfreichweite* gehören zusammen: Beide messen den *Abstand*
  zweier *Bases* und gelten bei jedem *Setzen*, also `querschnitt/setzen.md` und `setzen.py`.
  Die Aufstellung sagt nur, dass sie gelten. Mein Rat zu F2 bleibt A, als Teil des Spiegels.
- Die Aufstellung bleibt die eine Tür zum Stand und setzt sich aus Teilen zusammen, je
  Anforderung einer.

Berichtigung zu B: Die einzeiligen Methoden, die eine Regel aufrufen, bleiben vorerst;
ohne sie bräuchte die Tabelle der Sperren `lambda`, das [Es](../../prozess/praemissen/es.md) 7 verbietet.
Einigen wir uns in 345, schreibe ich den Spiegel in die Architektur und beauftrage den
Regelumsetzer mit seiner Prüfung; sonst kommt es hierher zurück.
