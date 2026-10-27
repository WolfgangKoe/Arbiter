# Anwendung: Dienste und Ports

Schichten: [Architektur](../architektur.md). Vorbild: Cockburn,
[Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/); Percival und
Gregory, „Architecture Patterns with Python“, Kapitel 4.

## Aufbau
- Je Handlung ein Dienst: Partie holen (P2), Befehl an die Domäne, ablegen, Spielstand
  zurück, bei einer *Sperre* mit den Texten ihrer Gründe (W3).
- Ports sind `typing.Protocol`: `Katalog` lädt die Ausgangslage, `Partien` liest und hängt
  Befehle an. Ein Adapter erfüllt sie, ohne sie zu importieren. Die Domäne braucht keine.
- Befehle und Spielstand sind unveränderliche `dataclass` mit Kennungen (W4) statt Objekten
  der Domäne, etwa `ModellLoslassen(spieler, einheit, modell, x, y)`; der Befehl ist die
  Handlung, die `speicher/` ablegt.

Prüft: nur Text; Auslöser: erstes Modul in `anwendung/`.

## Umbau
Heute fehlt `anwendung/`, `web/` ruft die `Aufstellung` (W2). Mit dem ersten Item zum
Speicher (Anliegen 692) ziehen `kennungen.py` und `darstellung.py` nach `anwendung/`,
`web/anwendung.py` heißt `routen.py`, und Bildschirmtests geben `serverStarten` Dienste mit
einem Speicher im Arbeitsspeicher ([B1](tests.md#bildschirmtests)).
