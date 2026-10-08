# Stand behalten braucht keine Datenbank

319 · Kritik · von Architekt (Technik) → Planer · Runde 1/3 · angenommen

## Runde 1
**Befund.** Item 3 ([Stand behalten](../../domaene/items/standBehalten.md)) begründet sich
mit „Bringt den Speicher, den jede weitere Handlung braucht“. Der [Plan](../plan.md) nennt es
„Neuland“, lässt es als Erstes fallen, wenn der Zyklus nicht reicht, und gibt mir vor dem
Testautor einen Wegwerf-Versuch zum Wiederholen der Handlungen auf. Die Kriterien des Items
verlangen keine Datenbank:
- QUE-3.2 (neu laden zeigt dasselbe) erfüllt schon der laufende Server. Er hält eine einzige
  `Aufstellung` im Speicher des Prozesses, solange Arbiter läuft (`serverStarten`, W2 in
  [web.md](../../technik/architektur/web.md)). Beispiel: Setzt ein Test heute ein Modell und
  lädt die Seite zweimal, zeigt sie es beide Male. QUE-3.2 legt nur fest, dass die Auswahl
  aus Item 2 im Server liegt und nicht im Browser.
- QUE-3.3 (Neustart zeigt die Ausgangslage) gilt von selbst: Ein neuer Prozess lädt die
  Ausgangslage neu (W5). Der Stakeholder hat in 309 F2 (git) gegen B gewählt, die letzte
  Partie wiederherzustellen. Eine Datenbank speicherte also nur, was niemand mehr liest.
- Die Auswahl ist nach AUF-5 (Zweck) und Glossar keine Handlung. Die Folge der Handlungen
  ([speicher.md](../../technik/architektur/speicher.md), P2) enthielte sie gar nicht.

Der Fehler liegt bei mir: speicher.md legt die Datenbank auf „die erste Handlung über HTTP“.
Das ziehe ich in der Technikphase nach. Die Datenbank kommt dann mit dem ersten Kriterium,
das den Stand über einen Neustart hinaus verlangt, oder mit „zurück“ (Plan 6), falls dort das
Wiederholen der Handlungen gewählt wird.

**Kosten.** So wie der Plan steht, kosten Kriterien ohne Bedarf: ein Wegwerf-Versuch
(SQLite, Handlungen wiederholen), das Paket `speicher/` mit den Auslösern P1 und A3, also
Läufe des Regelumsetzers für den Importvertrag, dazu ein Akzeptanztest „wiederholt ergibt
denselben Spielstand“ ohne Kriterium. Die Bildschirmtests müssten ihren Zustand über die
Folge der Handlungen übergeben statt als `Aufstellung` (speicher.md, Neuland). Der
Stakeholder liest außerdem ein falsches Risiko: Item 3 ist das billigste der drei, nicht das
unsicherste. Der Satz „Reicht der Zyklus nicht, fällt Item 3“ verspricht eine Einsparung, die
es nicht gibt.

**Gegenvorschlag.**
1. Item 3, „Warum jetzt“: „Legt fest, dass Arbiter den Stand im laufenden Server hält, nicht
   im Browser (QUE-3.2), und beim Neustart verwirft (QUE-3.3); ohne Datenbank (319).“
   Umfang und Abhängigkeit bleiben. In Item 2 ist kein Platz für die beiden Kriterien
   (399 von 400 Zeichen), darum bleibt Item 3 eigenständig.
2. Plan: „der Speicher dazu (Neuland, speicher.md)“ wird zu „prüft, dass die Auswahl im
   Server liegt“. Die Ausfallregel „fällt Item 3“ entfällt oder trifft Item 2. Im Auftrag an
   mich vor dem Testautor bleibt nur der Vertrag für den Klick in web.md; der Wegwerf-Versuch
   entfällt.
3. Wo der Plan die Auswahl beschreibt, darf er nicht „Speicher“ sagen, solange speicher.md
   die Datenbank meint.

Erledigt, wenn Item 3 und der Plan keinen Speicher und kein Neuland mehr für QUE-3.2 und
QUE-3.3 nennen.

**Stellungnahme.** Angenommen, alle drei Punkte.
1. [Stand behalten](../../domaene/items/standBehalten.md), „Warum jetzt“: Arbiter zeigt beim
   Neuladen den Stand samt Auswahl (QUE-3.2) und verwirft ihn beim Neustart (QUE-3.3), ohne
   Datenbank. Ich formuliere es ohne „Server“, weil das Item fachlich bleibt; Umfang und
   Abhängigkeit sind unverändert.
2. [Plan](../plan.md): Item 3 „prüft, dass Arbiter die Auswahl beim Neuladen behält und beim
   Neustart verwirft“. Die Ausfallregel „fällt Item 3“ ist gestrichen, ohne Ersatz. Item 2
   ist der Kern des Zyklus und kann nicht ausfallen. Vor dem Testautor bleibt für dich nur
   der Vertrag für den Klick in web.md.
3. „Speicher“ steht im Plan nur noch unter „Grundlage“, mit der Begründung, warum Plan 4 vom
   Zyklusziel aus Review 3 („mit Speicher“) abweicht und ihn nicht braucht (Verweis auf 319).
   Neuland steht nicht mehr im Plan.
