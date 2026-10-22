# Regelkommentare entbehrlich

Form: Auftrag
Von: Stakeholder
An: Organisationsentwickler
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Wortlaut des Stakeholders: „Ich finde noch diverse Kommentare wie ‚# Regel:
AUF-5.11 (keine andere ausgewählt), AUF-20.2 (die Ebene ist die Einheit)‘. Die sollte es
eigentlich nicht brauchen. So etwas finde ich in vielen Dateien (auch in den
Akzeptanztests). In den Definitionen der Tests gibt es ja eine Referenz zu den
Akzeptanzkriterien. Das ist eine Art ‚#tag‘, so dass klar wird, welcher Test welches
Akzeptanzkriterium sicherstellen soll. Über die Mutationstests finden wir toten Code. Die
Architektur stellt (hoffentlich) sicher, dass alles gut zusammen funktioniert und wir eine
hexagonale Architektur haben. Im Zuge der DoD sollten solche Dinge immer über Skripte
geprüft und entsprechend reagiert werden.“

Dazu: „Beim Setzen der Kommentare scheint es kein Einlenken zu geben. Im Sinne von SOLID und
Clean Code sollten Kommentare an sich nicht nötig sein. Ausnahme wäre, dass hier etwas zu tun
ist im Sinne eines ‚TODO‘. Dieses muss dann aber in der nächsten Technikphase angegangen
werden, und die Anzahl der TODOs muss gedeckelt sein. Am Ende einer Technikphase müssen alle
TODOs gelöst sein, die vorher da waren. TODOs dürfen danach nur bleiben, wenn sie in der
gerade durchgeführten Technikphase entstanden sind.“

Beispiel: `technik/arbiter/domaene/phasen/aufstellen/auswahl.py`, Zeile 25. Heute stehen
32 Kommentare `# Regel:` in 18 Dateien unter `technik/` (8 davon in Tests), 7 `// Regel:`
im Frontend und 15 in `prozess/pruefungen/`.

Bestehende Regeln, die das berühren ([Ich 4](../../prozess/praemissen/ich.md)):
- [Es 8](../../prozess/praemissen/es.md) erlaubt `# Regel: <Fundstelle>` und `# Warum:`
  ausdrücklich und verbietet TODO und FIXME.
- `prozess/pruefungen/formregeln/kommentare.py` (`erlaubterKommentar`) und
  `prozess/pruefungen/frontendregeln/eslintKommentare.mjs` lassen ihn durch
  ([Regeln, Formregeln](../../prozess/regeln.md#formregeln)); beide laufen in der
  [DoD 2](../../prozess/ablauf.md#dod-item-fertig).
- [Architektur, T2](../../technik/architektur.md): Der Weg vom Kriterium zum Test steht nur im
  Namen (`testAuf7_3…`), geprüft von `kriterienregeln/rueckverfolgung.py`; ein
  Kriterium im Kommentar des Produktcodes wiederholt das ([Wir 3](../../prozess/praemissen/wir.md)).
- Toten Code finden vulture (DoD 2) und die Mutationstests
  (Anliegen 1570); die Schichten prüft
  `formregeln/importvertrag.py`.

**Kosten.** Ein Kommentar mit Kennung veraltet, sobald sich Kriterium oder Nummer ändert,
und kein Skript merkt es. Er ersetzt einen sprechenden Namen und wiederholt, was Testname
und Prüfungen schon sichern.

**Gegenvorschlag.** Fragen an die Prozessphase; den Mechanismus baut der Regelumsetzer:
1. Bleiben nach Es 8 nur Werkzeugkommentare und `TODO`, und sperren `kommentare.py` und
   `eslintKommentare.mjs` alles andere in Produkt, Tests und Prüfcode, auch `# Warum:`?
2. Wie hoch ist der Deckel für TODOs, und woran erkennt das Skript, ob ein TODO aus der
   laufenden Technikphase stammt (etwa `git blame` gegen „Freigabe Plan <n>“)?
3. Was bleibt für eine Fundstelle außerhalb der Kriterien (Glossar, Architektur S3,
   Regelbuch der 9. Edition): ein Name, der sie trägt, oder nichts?
4. Wer entfernt die bestehenden Kommentare: Zählen sie als TODOs von vor der Technikphase 7?
5. Welche Prüfung der DoD fehlt noch, damit Kriteriumsbezug, toter Code und Architektur
   nur über Skripte belegt sind, nicht über Kommentare?

**Stellungnahme.** Angenommen (Anliegen 1860), [Es 8](../../prozess/praemissen/es.md) neu:
1 und 3 nur Werkzeugkommentare mit Regelcode und `TODO`, der Name trägt die Fundstelle; 2
höchstens drei, ein altes TODO macht die DoD rot; 4 Technikphase 7; 5 Regelumsetzer, P5.
Kommentar: Woran erkenne ich an diesem Anliegen, dass ich es auf "erledigt" setzen kann?
Stellungnahme: Wenn in der [Retro 6](../retro.md) „Regelumsetzer: P5“ abgehakt ist; die alten Kommentare sind nach Technikphase 7 weg, sonst ist deren DoD rot.
