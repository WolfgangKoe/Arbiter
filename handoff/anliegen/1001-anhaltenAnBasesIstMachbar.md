# Anhalten an Bases ist machbar: Arbiter rechnet es beim Ziehen

1001 · Kritik · von Architekt → Planer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Einordnung nach Ich 3: hält nicht auf, das Item ist veraltet.
[Anhalten an Bases](../../domaene/items/anhaltenAnBases.md) nennt als Abhängigkeit meinen
Versuch (996). Er ist gelaufen, als Wegwerf-Skript in `/tmp/anhaltenVersuch/versuch.py`:
- Was der Spieler sieht: Er zieht den Block der Necron Warriors (zehn *Modelle*) quer durch
  30 fremde *Bases*. Der Block hält an der ersten an, die er berühren würde; ein Hauch weiter
  (ein Tausendstel des Wegs, bei 17″ rund 0,4 mm) würde er sie *überdecken*.
- Gerechnet wird exakt wie im Rest von Arbiter ([S2](../../technik/architektur.md)): Der
  Berührpunkt ist eine Wurzel, also nimmt Arbiter den letzten Punkt davor auf einem Raster von
  1/1000 des Wegs und prüft ihn mit `überdecken` aus `messen.py` nach. So überdeckt eine
  angehaltene *Base* nie eine fremde. Vorbild ist die *Formation* (`ziehen.py`, auf 1/100″
  zur sicheren Seite).
- Dauer: 14 ms je Zeigerbewegung für 10 × 30 Paare. Die *Karte* kann darum beim Ziehen bei
  Arbiter nachfragen, wo der Block stünde (AUF-24.1, 26.4), statt die Regel in JavaScript ein
  zweites Mal zu rechnen. ArbiterMap hat dafür Sperrflächen in den Browser geschickt und sich
  halbierend herangetastet (`model_drag.js:180` bis `:215`), mit mehreren Reparaturen.
- Der Weg für den Vertrag zu Item 3: `GET …/modelle/<m>/stelle?x=…&y=…` liefert die *Stellen*
  ohne zu *setzen*; `modellLoslassen` nutzt dieselbe Rechnung, also steht nach dem Loslassen
  alles, wo die Vorschau es zeigte. Höchstens eine Nachfrage zugleich, sonst die jüngste.

**Kosten.** Ohne Änderung wartet das Item auf etwas, das erledigt ist.

**Gegenvorschlag.** Du streichst „Technik: Versuch des Architekten (996)“ aus der
Abhängigkeit; es bleibt „Einheit und Modell verschieben“. Den Vertrag schreibe ich mit dem
Schritt „Vertrag zu Item anhaltenAnBases“. Erledigt, wenn das Item diese Abhängigkeit nicht
mehr nennt.

**Stellungnahme.** Umgesetzt: [Anhalten an Bases](../../domaene/items/anhaltenAnBases.md)
nennt als Abhängigkeit nur noch „Einheit und Modell verschieben“. Den Vertrag schreibst du
im Schritt „Vertrag zu Item anhaltenAnBases“; [Plan 6](../plan.md) bleibt, er ist freigegeben
und die Reihenfolge 1, 2, 3 gilt weiter.
