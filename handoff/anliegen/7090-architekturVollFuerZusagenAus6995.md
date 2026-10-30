# Die Architektur ist voll für die Zusagen aus 6995

Form: Fragen
Von: Architekt
An: Stakeholder
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** In [Anliegen 6995](6995-frontendUndBackendImOrdner.md) habe ich dir für die
Technikphase 9 drei Sätze in der [Architektur](../../technik/architektur.md) zugesagt:
1. `arbiter/` ist das Backend (F1 B).
2. In [W2](../../technik/architektur/web.md#aufbau): „`web/` liefert Formen und *Abstände*
   in *Zoll*, keine Zeichnung“.
3. In [O5](../../technik/architektur/frontend.md): der Ordner `frontend/komponenten/`, je
   Komponente ein Modul, das ihre Vorlage füllt und keine Regel kennt (F3 A). Item 4
   (*Grenzkreise*) baut darin `grenze.js`; ohne den Satz verstößt es gegen O5, das heute nur
   `zeichnen.js` als Ziel der Importe nennt.

Zusammen sind das rund 300 Zeichen. Die Regeln der Architektur dürfen zusammen 24.000
Zeichen haben ([Kennzahlen](../../prozess/kennzahlen.md#höchstmaße), Anliegen 159, 211),
damit man sie auf einmal lesen kann. Heute haben sie 24.000; es passt kein Zeichen mehr.

Platz ist da, wo die Architektur wiederholt, was der Code schon sagt:
- W2 beschreibt `server.py` bis auf Parameter und Socket (`serverStarten(aufstellung,
  port=0)`, `make_server`, `socket.create_server`, `errno.EADDRINUSE`). Für die Architektur
  genügt: eigener Thread, eine Anfrage nach der anderen, eine belegte Adresse wird `AdresseBelegt`. Frei:
  rund 270 Zeichen.
- W5 nennt die Meldung bei belegter Adresse wörtlich; sie steht genauso in
  `arbiter/__main__.py`, die Anforderung QUE-8.2 verlangt nur „meldet die Adresse als
  belegt“. Frei: rund 140 Zeichen.

Kürzen liegt in meinen Schreibpfaden. Ich frage dich, weil die Summe deine Regel ist und
Option B sie ändert.

**Kosten.** Am Bildschirm ändert keine Option etwas.
- A: ein kurzer Lauf von mir, zwei Absätze in [Web](../../technik/architektur/web.md).
  Verloren geht nichts, was nicht im Code steht. Die nächste Zusage dieser Größe stößt
  wieder an die Summe; dann frage ich erneut.
- B: Der Organisationsentwickler ändert einen Satz in den Kennzahlen. Die Architektur darf
  danach wachsen, wer sie ganz liest (Architekt, Reviewer), liest mit jeder Etappe mehr;
  die übrigen Rollen lesen ohnehin nur die Datei ihres Ordners.
- C: wie B, nur später voll.

**Gegenvorschlag.** Siehe F1.

**Stellungnahme.**

**F1 · Wie kommen die drei Zusagen aus 6995 in die Architektur?**
A: Ich kürze W2 und W5 um das, was der Code schon sagt, und schreibe die Zusagen in den
frei gewordenen Platz; die Summe bleibt 24.000 (Kennzahlen, Wir 3).
B: Die Summe fällt, je Datei bleiben 6.000 Zeichen, wie beim Vertrag (Anliegen 7022).
C: Die Summe steigt auf 30.000 (neu).
Empfehlung: A. Die Summe wirkt, wie sie soll: Sie zwingt mich, Wiederholungen zu
streichen, und es gibt sie. Für B spräche erst eine Architektur ohne Wiederholungen.
Annahme: Ohne Antwort kürze ich nach A, sobald der laufende Umbau des Vertrags (Anliegen
7022) fertig ist, und vor Item 4 (*Grenzkreise*).
Antwort: Wir machen erst A und dann B. Ich möchte dass Redundanzen reduziert werden. Wir brauchen eine smarte Struktur, die auch für mich als Stakeholder verständlich sein muss.
