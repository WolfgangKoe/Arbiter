# Ein verschobener Block sperrt sich an seinen eigenen vorigen Stellen

920 · Kritik · von Architekt → Anforderungsautor · Runde 1/3 · erledigt

## Runde 1
**Befund.** [AUF-21.1](../../domaene/anforderungen/phasen/aufstellen/einheitVerschieben.md)
*setzt* jedes *gesetzte* *Modell* der *Einheit* um denselben Weg, AUF-21.3 und AUF-3.7 prüfen
dann jede neue *Stelle* nach QUE-1.2: Überdeckt die *Base* „die eines anderen *gesetzten*
*Modells*“? Kein Kriterium sagt, wo dabei die anderen *Modelle* derselben *Einheit* stehen,
an ihrer vorigen oder ihrer neuen *Stelle*. Schiebt ein *Spieler* seine Boyz um einen halben
*Zoll* entlang einer Reihe, überdeckt jede neue *Base* die vorige ihres Nachbarn. Der Code
prüft heute jedes *Modell* einzeln gegen den Stand davor (`_loslassen` in
`technik/arbiter/domaene/phasen/aufstellen/__init__.py`); so gebaut, wäre jeder kleine Zug
*gesperrt* mit ‚Base überdeckt‘. ArbiterMap nimmt die eigene *Einheit* deshalb aus der Prüfung
(`ArbiterMap/backend/app/services/movement_service.py:450`, „die eigene Einheit bewegt sich
mit“).

Einordnung nach Ich 3: hält auf. Nachrücken um wenig ist der häufigste Zug nach dem Klick
(AUF-20.2: „Ganze Einheit“), und eine *Sperre* griffe zu Unrecht; ein Test mit einem langen
Weg fände das nicht.

**Kosten.** Ohne Satz wählt der Testautor den Weg frei, und der Implementierer entscheidet
eine Regel, die keiner geprüft hat. Mit dem Satz: ein Test mehr, im Code eine Ausnahme beim
Prüfen der *Stelle*.

**Gegenvorschlag.** In AUF-21.3 oder als AUF-21.6: QUE-1.2 prüft gegen die *Stellen* nach dem
Verschieben, eine *Base* sperrt nicht an der vorigen *Stelle* eines *Modells* derselben
*Einheit*. Bestehende Regel nach Ich 4: AUF-3.7 („wie bei jedem *Setzen*“), die das offen
lässt. AUF-21 hat nur noch wenige Zeichen frei; kürzen oder eine eigene Kennung. Erledigt,
wenn ein Kriterium den Fall regelt, oder du begründest, warum der Block sich sperren soll.

**Stellungnahme.** Angenommen, als eigene Kennung, weil AUF-21 voll ist:
[AUF-24.2](../../domaene/anforderungen/phasen/aufstellen/blockAlsGanzes.md). Ich folge dem
Vorbild (`movement_service.py:450`), nicht ganz dem Gegenvorschlag: Die *Modelle* derselben
*Einheit* zählen für QUE-1.2 gar nicht, weder an voriger noch an neuer *Stelle*. Beim starren
Verschieben ist das dasselbe, außer zwei *Modelle* überdeckten sich schon vorher (nach
*gemeinsam übergehen*); dann sperrte sich der Block sonst bei jedem Zug erneut. AUF-21.3 bleibt
ohne neuen Inhalt; Item 2 zieht der Planer nach ([932](932-plan6NachZuruecklegenUndBlock.md)).
