# Architekturbild: Fachregeln in der Mitte, Technik steckt außen an

692 · Fragen · von Architekt → Stakeholder · Runde 1/3 · erledigt

## Runde 1
**Befund.** Hexagonal (Cockburn 2005, „Ports und Adapter“): Der Kern kennt keine Technik.
Er hat Anschlüsse (Ports) wie Steckdosen; Technik steckt als Adapter daran, wie ein
Stecker. Treibend: was den Kern aufruft (Bildschirm, Tests). Getrieben: was er aufruft
(Katalog, Speicher). Pfeile heißen „kennt“, alle zeigen nach innen. Bild und Schichten:
[Architektur](../../technik/architektur.md#schichten), [Anwendung](../../technik/architektur/anwendung.md).

Abstand heute: klein. Die Domäne ist rein, `web/` getrennt (A1, A2,
[W1](../../technik/architektur/web.md)). Es fehlen die Dienste: `web/anwendung.py` ruft die
`Aufstellung` direkt, und nach P2 müsste `web/` die Handlungen wiederholen. Kennungen
(W4) und Spielstand (`darstellung.py`) liegen in `web/`, der Speicher braucht beide.
Vorbild: ArbiterMap trennt Regeln ebenso (`domain/rule_checks.py`).

**Kosten.** Ohne Dienste wächst `web/` mit dem Speicher zur dicken Schicht, wie
`ArbiterMap/backend/app/routes/map.py` (40.000 Zeichen). Der Umbau: `anwendung/` neu, etwa
150 Zeilen; `kennungen.py` und `darstellung.py` ziehen um (130 Zeilen); `web/anwendung.py`
schrumpft. Akzeptanztests bleiben bis auf den Serverstart der Bildschirmtests (B1). Neu ist A4 im
Importvertrag (`web/` kennt `anwendung/`, nicht `domaene/`). Am billigsten mit dem ersten
Item zum Speicher, das die Dienste ohnehin braucht.

**Gegenvorschlag.** Bestehende Regeln (Ich 4): A1, A2, W1, W2, P1, P2,
`formregeln/importvertrag.py`, [Es, D](../../prozess/praemissen/es.md). Nach deinen Antworten
schreibe ich das Bild in [Architektur](../../technik/architektur.md) (Schichten, A4) und
beauftrage den Regelumsetzer mit A4. Quellen:
[Cockburn](https://alistair.cockburn.us/hexagonal-architecture/), Percival und Gregory,
„Architecture Patterns with Python“ ([Kapitel 4, Dienste mit Flask](https://www.oreilly.com/library/view/architecture-patterns-with/9781492052197/ch04.html)).

**F1 · Gilt dieses Bild als Zielbild?**
A: Ja, hexagonal mit `anwendung/` (Dienste, Ports, DTOs) zwischen `web/` und `domaene/`.
B: Nein, wie heute: Domäne und dünnes `web/`; Ports erst, wenn der Speicher kommt.
Empfehlung: A. Der Speicher braucht die Dienste; ich prüfe künftig jeden Code daran.
Antwort: A

**F2 · Wann wird umgebaut?**
A: Mit dem ersten Item zum Speicher, im selben Zyklus.
B: Sofort als eigenes Item vor dem nächsten Fach-Item.
Empfehlung: A. Vorher hat der Umbau nur einen Nutzer (`web/`) und kostet einen Zyklus ohne
neues Verhalten am Bildschirm.
Antwort: A

**Stellungnahme.**
Kommentar: Für mich klingt das schlüssig. Ich hoffe, du weißt, was du tust ;-). Eine Sache, die mir noch bei den Akzeptanztests aufgefallen ist. Kann es sein, dass es dort ein paar "triviale Tests" gibt, die quasi immer grün sind? Ich bin mir da nicht sicher, ob jeder einzelne Test dann auch Methoden aufruft, die im Produktivcode stehen. Ich frage das nur, weil ich die Sorge habe, dass wir viele frohe und vor allem grüne Tests haben, die am Ende gar nichts testen.

**Klärung.** Umgesetzt: Bild oben verlinkt, A4 beim Regelumsetzer
(Anliegen 694). Zu den Tests: Ja, solche gibt es. Jeder ruft Produktcode
auf, doch die Abdeckung zeigt nur, dass jede Zeile läuft, nicht, dass ein Test einen Fehler
bemerkt. Zwei Arten: Tests, die vor allem die Katalogdaten prüfen (OBJ-1.1, „jeder *Spieler*
führt eine *Armee* mit *Einheiten*“), und Tests auf „ändert nichts“ (AUF-17.1, „zurück“ ohne
*gesperrtes* *Modell*): Sie blieben grün, wenn „zurück“ gar nichts täte, und zählen nur mit
ihrem Gegenstück (AUF-9.3). Wie viele nichts fangen, misst ein Mutationstest: Er baut Fehler
ein und zählt, welche kein Test bemerkt. Von Hand fand die Probe des Reviewers zwei Lücken;
das Werkzeug steht im Backlog, spätestens zu Etappe 2. Empfehlung: jetzt auslösen, als
Kommentar zur Retro 5.
