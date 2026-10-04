# Plan 3: was sichtbar wird, was geprüft wird, und 153 als Abhängigkeit

198 · Kritik · von Architekt (Technik) → Planer (Domäne) · Runde 1/3 · offen

## Runde 1
**Befund 1 · Die Empfehlung verspricht mehr, als zu sehen ist.** „siehst … wer an der Reihe
ist“: In der Ausgangslage ist keiner an der Reihe (AUF-1.3), und ohne Handlung bleibt es so.
Ebenso zeigt die Karte kein Modell (AUF-2.5) und keine Zone farbig (AUF-4.6). Sechs der zwölf
Kriterien zeigen im Review nur ihren leeren Fall: QUE-2.4, QUE-2.6 und AUF-4.5 ganz, AUF-4.4
und AUF-4.6 ohne die Hälfte mit Spieler, QUE-2.5 ohne die Bases. Anliegen 195 nennt drei
davon, der Plan zieht keinen Schluss.

**Kosten.** Der Stakeholder erwartet im Review „wer an der Reihe ist“ und findet nichts. Die
Prüfung selbst ist billig: Die Akzeptanztests bauen den Spielstand mit den Handlungen der
Domäne (`aufstellung.einheitInAufstellungWählen(…)`, `modellSetzen(…)`) und starten die
Oberfläche damit. `web/` bekommt den Spielstand beim Erzeugen übergeben, im Betrieb die
Ausgangslage. Das ist das übliche App-Factory-Muster von Flask, keine Hintertür: Keine
Handlung läuft über HTTP, und es braucht keinen Speicher (153 F1). So sind alle zwölf
Kriterien voll geprüft, nicht nur ihr Anfang.

**Gegenvorschlag.**
- A: Beide Items wie geschnitten. Die Empfehlung sagt: Du siehst Spielfeld, Zonen ohne
  Farbe, beide Ablagen, keinen an der Reihe; Zustände mit Spieler an der Reihe, gesetzten
  Modellen und farbigen Zonen zeigen die Bilder des Bildschirmtests im Review.
- B: QUE-2.4, QUE-2.6 und AUF-4.5 wandern ins Item „Wählen per Klick“, wo man sie auch
  bedient. Der Zyklus wird kleiner, aber AUF-4.4, AUF-4.6 und QUE-2.5 müsste der
  Anforderungsautor teilen, damit ein Item nicht halbe Kriterien trägt.

Empfehlung A: Kreise und Farben kosten im Frontend wenig, die Naht für den Test entsteht
ohnehin, und das Item „Wählen per Klick“ bleibt bei den Handlungen.

**Befund 2 · 153 als Abhängigkeit von Item 1 widerspricht DoR 4.** DoR 4 verlangt erledigte
Abhängigkeiten vor der Freigabe. Den Aufbau aus 153 schreibe ich aber erst in der
Technikphase in die Technik (Plan, „Vor dem Testautor“); in der Domänenphase arbeite ich
nicht in `technik/`. Dazu wartet 153 auf 155 und 159, und zu 159 hat der Stakeholder eine
Rückfrage gestellt statt zu entscheiden. Nach DoR wird Item 1 so nie bereit.

**Kosten.** Die Freigabe hinge an einer Kette aus drei Anliegen, die der Plan selbst erst
nach der Freigabe abarbeiten will.

**Gegenvorschlag.** In beiden Items steht als Abhängigkeit nur, was vor der Freigabe fertig
sein muss: Mockup (151), Antworten zu 195, für Item 2 zusätzlich Item 1. 153 steht nur
unter „Vor dem Testautor“, wie schon im Plan, mit 159 als Voraussetzung.

**Stellungnahme (Planer).**
