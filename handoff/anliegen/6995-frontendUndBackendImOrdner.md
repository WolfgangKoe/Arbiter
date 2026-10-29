# Wie das Frontend gebaut ist und ob die Ordner den Schnitt zeigen

Form: Fragen
Von: Architekt
An: Stakeholder
Runde: 1/3
Status: offen

## Runde 1
**Befund.** Deine Frage: Baut Python die Oberfläche, liegen Dateien des Frontends im Backend,
passt die Ordnerstruktur? Python baut keine Oberfläche. Das Frontend ist
[`technik/frontend/`](../../technik/frontend/): eine HTML-Seite mit Vorlagen, ein Stylesheet,
vier JavaScript-Module (Einstieg, Bedienung, Anfragen, Zeichnen), ohne Framework und
Build-Schritt. Das Backend ist [`technik/arbiter/`](../../technik/arbiter/), das Python-Paket:
Es liefert diese Dateien unverändert aus und beantwortet Anfragen unter `/api/` mit dem
Spielstand als JSON; HTML erzeugt es nicht ([W1](../../technik/architektur/web.md)). Anders
ArbiterMap: Dort setzt Python die Seite aus Vorlagen zusammen.

Datei für Datei: Im Frontend steht nichts vom Backend, im Backend keine Datei nur fürs
Frontend. `web/` ist die Backend-Seite der Schnittstelle: Server, Pfade, Spielstand als JSON,
Nummern für *Spieler* und *Einheiten*. *Auswahl*, *Ebene* und Anklicken in der Domäne klingen
nach Oberfläche, sind aber Anforderungen (AUF-5, AUF-20, AUF-25) und bestimmen, was Ziehen
bewegt; sie gehören dorthin. Drei Befunde:
1. Der Name zeigt den Schnitt nicht: `arbiter/` ist das Backend, du hast es fürs Frontend
   gehalten. Darin klingt `web/` nach Oberfläche und ist der Anschluss für HTTP.
2. [`web/anwendung.py`](../../technik/arbiter/web/anwendung.py) enthält Ablauf, der in die
   geplante Schicht `anwendung/` gehört: wann die *Schlacht* beginnt, ob „Phase beenden“ die
   laufende *Phase* meint. Der Umzug ist beschlossen
   ([Anwendung, Umbau](../../technik/architektur/anwendung.md)), die Datei heißt dann
   `routen.py`.
3. Eine Regel steht nur dort: *Ebene* wird nur ein *gesetztes* *Modell*. Die Domäne
   (`Aufstellung.ebeneWählen`) nimmt jedes *Modell* der *ausgewählten* *Einheit*; die Seite
   bekommt heute trotzdem die richtige Antwort.

**Kosten.** Am Bildschirm ändert keine Option etwas. Umbenennen berührt 32 Dateien mit 75
Pfaden, 15 davon in Prüfungen und Agentendefinitionen, dazu drei Zeilen in `pyproject.toml`;
der Regelumsetzer baut gerade den Reiter Architektur (Anliegen 4140), der die Ordner liest.
Token: ein mittlerer Auftrag, je ein Zug von Regelumsetzer und Architekt.

**Gegenvorschlag.** Den Schnitt im Ordnernamen zeigen, zusammen mit dem Umbau zu
`anwendung/` (Anliegen 692) in einer Technikphase.

**Stellungnahme.**

**F1 · Sollen die Ordner Frontend und Backend heißen?**
A: `technik/arbiter/` wird `technik/backend/arbiter/`, neben `technik/frontend/`, wie
`backend/` und `frontend/` in ArbiterMap (ArbiterMap). Befehl und Paketname `arbiter`
bleiben. Nachteil: Kosten oben. Rückweg: zurückschieben. Nicht an einer Kopie erprobt.
B: Bleibt; die [Architektur](../../technik/architektur.md) nennt `arbiter/` ausdrücklich das
Backend (Architektur W1). Eine Zeile, der Name bleibt missverständlich.
C: Das Frontend ins Paket (`arbiter/web/static/`), wie Flask es anbietet (neu). Verwischt die
Trennung von Frontend und Backend aus dem Technik-Rahmen.
Empfehlung: A, nach Anliegen 4140. Hast du den Ordner missverstanden, tut es jeder neue Leser.
Antwort: .

**F2 · Wann kommt die Regel aus Befund 3 in die Domäne?**
A: Mit dem Umbau zu `anwendung/` (Anwendung, Umbau): Erst dann ruft ein zweiter Weg die
Domäne, das Wiederholen gespeicherter Handlungen (Speicher, P2). Ein Einheitstest, wenige
Zeilen.
B: Jetzt als eigenes Item in der nächsten Technikphase (neu, Grund: Ziel,
Regelkonformität). Gleich viel Arbeit, früher sicher.
Empfehlung: A, heute fängt `web/` den Fall ab.
Antwort: .
