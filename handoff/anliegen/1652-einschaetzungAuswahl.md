# Einschätzung: Ist auswahl.py im Sinne der Kritik lesbar?

1652 · Fragen · von Architekt → Stakeholder · Runde 1/3 · erledigt

## Runde 1
**Befund.** Deine Einschätzung: „auf den ersten Blick recht gut lesbar“, aber vielleicht nicht im
Sinne von [kritik-entwickler.md](../kritik-entwickler.md), Abschnitt 1. Ich habe
[auswahl.py](../../technik/arbiter/domaene/phasen/aufstellen/auswahl.py) und die Module daneben
gelesen, ohne die Kommentare `# Regel:`. Kurz: Dein Eindruck stimmt. Die Kritik an Namen,
Verzweigungen und Messbarkeit ist erfüllt. Die Kritik „Domänenmodell zu implizit“ trifft noch an
drei Stellen.

Erfüllt:
- **Namen.** Kein Name ist kürzer als drei Zeichen, alle sind deutsch und sprechen: `auswählen`,
  `ebeneWählen`, `_prüfenDassZurAusgewähltenEinheit`. Eine Prüfung erzwingt das.
- **Verzweigungen.** Jede Methode hat höchstens zwei `if`, meist mit frühem `return`. Wo viele
  Gründe gelten, stehen sie als Tabelle (`beenden.py`). Komplexität und Zahl der Zweige misst
  eine Prüfung.
- **Messbar.** Namen, Komplexität, Zweige, Mutationstests und SonarLint laufen als Prüfungen.
- **Begriffe.** *Auswahl* und *Ebene* stehen im Glossar und heißen im Code genauso.
  *Auswahl* ist eine eigene Klasse mit einer Aufgabe.

Noch implizit (Befunde an den Implementierer: [1651](1651-auswahlUndAufstellungImplizit.md)):
1. Die *Auswahl* schaut heimlich in den Zustand der *Aufstellung*. Sie bekommt deren Liste der
   aufgestellten *Einheiten* und liest mit, wenn diese wächst. Wer nur auswahl.py liest, hält die
   Liste für fest.
2. Ob Ziehen die ganze *Einheit* oder nur ein *Modell* bewegt (AUF-21.1 gegen 20.4), steckt in
   einem Vergleich: `ebene(einheit) is not einheit`. Die Frage hat keinen Namen.
3. `spieler` heißt mal ein *Spieler*, mal beide. Das Deutsche unterscheidet hier Ein- und
   Mehrzahl nicht, der Leser muss auf den Typ schauen.

Gilt das Muster auch in anderen Modulen? Ja, in `reihenfolge.py` (Punkt 3) und in `Aufstellung`.
Diese Klasse reicht sieben Aufrufe an die *Auswahl* durch, verteilt auf zwei Stellen. Der Rest der
Phase ist sauber: Hilfsfunktionen bekommen ihren Zustand offen als Angaben, nicht heimlich, etwa
`prüfenDassWählbar(einheit, aufgestellt, anDerReihe, einheitInAufstellung)`. Ein Kunstgriff
fällt noch auf: Aufrunden als `-(-a // b)` in `setzenPerKlick.py`.

Mein eigener Anteil: Die Architektur sagt nicht, wann der Code eine *Sperre* meldet (Regelverstoß,
die Seite zeigt den *Grund*) und wann einen Programmfehler (`ValueError`, ein Aufruf, den die
Seite nie schickt). Das ist implizit wie 1 bis 3. Ich schreibe es in der nächsten
Technikphase in die Architektur.

**Kosten.** Keiner der Punkte macht heute einen Fehler. Punkt 1 ist der teuerste: Ändert jemand
die Liste der *Aufstellung*, bricht die *Auswahl* unbemerkt. Die Punkte 2 und 3 kosten
Lesezeit, Punkt 2 mit jeder neuen Anforderung zur *Ebene* mehr. Zusammen etwa ein halbes Item,
das Verhalten bleibt gleich.

**Gegenvorschlag.**

**F1 · Wann soll der Implementierer 1651 umsetzen?** Empfehlung: in der nächsten Technikphase
als eigenes Item vor dem nächsten fachlichen Item der Aufstellung. Das laufende Item steht kurz
vor der Abnahme. Nichts davon ist rot.
Antwort: .

**Stellungnahme.**
