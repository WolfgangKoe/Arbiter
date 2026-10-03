# Erste Oberfläche im Browser: Plan 3, ArbiterMap als Vorbild

145 · Fragen · von Planer (Domäne) → Stakeholder · Runde 1/3 · offen

## Runde 1
**Befund.** Dein Wunsch: ein Frontend, in dem du die Funktionalität im Browserfenster
siehst, ähnlich wie ArbiterMap. Er gehört zu [Etappe 1](../../domaene/etappen/01-aufstellen.md):
Sie ist erst erreicht, wenn die Spieler Modelle aus der Ablage setzen und auf der Karte
loslassen, und der Technik-Rahmen (Flask, Frontend getrennt) heißt Browser. Im
[Plan](../plan.md) steht die erste Oberfläche unter „Danach“ an erster Stelle. Nach Zyklus 2
rechnet Arbiter Reihenfolge und Sperren beim Setzen; sehen kannst du davon noch nichts.

Mein Vorschlag für Plan 3: Du startest Arbiter mit einem Befehl, öffnest die genannte Adresse
und siehst das Spielfeld 44″×60″, beide Aufstellungszonen und je Spieler die Ablage mit den
Modellen der Ausgangslage. Du ziehst ein Modell mit Maus oder Finger auf die Karte; ist das
Setzen gesperrt, zeigt Arbiter den Grund, und das Modell bleibt, wo es war. „Zurück“,
„gemeinsam übergehen“, Protokoll und das Beenden der Einheit folgen in späteren Zyklen.

**Kosten.** Die erste Oberfläche bringt viel Neues auf einmal: Start, Karte, Ziehen mit Maus
und Touch, Mockup (neue Rolle UX), Komponentenseite und Bildschirmtest
([Architektur, Oberfläche](../../technik/architektur.md)). In ArbiterMap hat allein das
Ziehen 85.402 Zeichen JavaScript (`frontend/static/js/model_drag.js`). Vermutlich werden es
zwei Items, erst Anzeige, dann Ziehen; den Schnitt prüft der Architekt in
[146](146-schnittDerErstenOberflaeche.md). Was „ähnlich wie ArbiterMap“ heißt, bestimmt das
Mockup.

**F1 · Was übernehmen wir von ArbiterMap?**
- A: Den Aufbau als Vorbild: Karte in der Mitte, je Spieler eine Seitenleiste mit der Ablage
  („Noch nicht aufgestellt“), Start mit einem Befehl, der die Adresse nennt. Das Aussehen
  (Farben, Schrift) schlägt UX im Mockup vor, angelehnt an ArbiterMap; du siehst das Mockup
  vor der Freigabe des Plans, der es baut.
- B: Aufbau und Aussehen so nah wie möglich übernehmen (Farben, Klassen, Bedienelemente).
- C: Nur der Browser; Aufbau und Aussehen frei.

Empfehlung: A. Der Aufbau von ArbiterMap folgt deinen Skizzen (`ArbiterMap/docs/spec/design_system.md`,
dort „[Beleg]“); die Farben waren dort nur Vorschlag. Übernommen wird das Bild, kein Code:
Der Altbestand dient als Beispiel, nicht als Vorlage.

Antwort: .

**F2 · Kommt die Oberfläche vor den übrigen Regeln von Etappe 1?**
- A: Ja. Plan 3 beginnt mit der Oberfläche; „zurück“, „gemeinsam übergehen“, Protokoll und
  Beenden danach.
- B: Nein. Erst die übrigen Regeln ohne Oberfläche, die Oberfläche zum Schluss von Etappe 1.

Empfehlung: A. Du siehst früh, was gebaut ist, und kannst es am Tisch ausprobieren. „Zurück“
und „gemeinsam übergehen“ sind Knöpfe neben einem stehengebliebenen Modell und brauchen die
Karte ohnehin. Das Ziel verlangt Abstände, die man auf der Karte zieht; die Oberfläche ist
also kein Komfort, der hinter der Regelkonformität zurückstehen müsste.

Antwort: .
