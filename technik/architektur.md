# Architektur

Wie Arbiter gebaut ist: welcher Teil was tut und welche Regeln dort gelten. Jede Regel steht
genau einmal und nennt, was sie prüft; „nur Text“ heißt ohne Mechanismus, ein Auslöser dabei:
Danach baut ihn der Regelumsetzer auf Anliegen des Architekten.

## Schichten
Ein Klick auf der Seite wird eine Anfrage an das Backend; die Domäne prüft die Regeln und
ändert den Zustand; die Antwort ist der Spielstand, die Seite zeichnet ihn. Hexagonal: Die
Domäne kennt keine Technik, Adapter stecken an den Ports von `anwendung/`.

Unter `technik/` | Aufgabe | Regeln
---|---|---
`frontend/` | Frontend: Seite, Stil, Komponenten; spricht nur über HTTP mit `web/` | [Frontend](architektur/frontend.md): O1 bis O5
`arbiter/` | Backend, das Python-Paket mit den Ordnern darunter | A1, A2, A4 (unten)
`arbiter/web/`, `__main__.py` | Flask: Anfrage → Befehl, Spielstand → JSON, *Sperre* → 409; der Start | [Web](architektur/web.md): W1 bis W5
`arbiter/anwendung/` | je Handlung ein Dienst; Ports, Befehle, Spielstand | [Anwendung](architektur/anwendung.md)
`arbiter/katalog/` | Port Katalog: Datenblätter und Ausgangslage aus `domaene/daten/` | [Katalog](architektur/katalog.md): A3, K1 bis K7
`arbiter/speicher/` | Port Partien: die Folge der Befehle | [Speicher](architektur/speicher.md): P1, P2
`arbiter/domaene/` | Fachlogik: Regeln, *Sperren*, Messen | [Domäne](architektur/domaene.md): S1 bis S3, D1 bis D4, M1
`tests/` | `akzeptanz/` je Anforderung, `einheit/` je Modul | [Tests](architektur/tests.md): T1, T2, B1 bis B5

Ein Ordner entsteht mit dem ersten Item, das ihn braucht. Den Vertrag zwischen `web/` und
`frontend/`, Pfade und JSON, hält je Phase eine Datei oder ein Ordner mit je Abschnitt einer
Datei: [Querschnitt](architektur/vertrag/querschnitt.md) für alle Phasen (V1, V4 bis V8),
[Aufstellen](architektur/vertrag/aufstellen/) (V2, V3, V9, V10),
[Schlacht](architektur/vertrag/schlacht/) und [Bewegung](architektur/vertrag/bewegung/)
(V11 bis V21). Höchstmaße: [Kennzahlen](../prozess/kennzahlen.md#höchstmaße).

## Abhängigkeiten zeigen nach innen
- **A1** `arbiter.domaene` importiert nur die Standardbibliothek und sich selbst. Prüft:
  `formregeln/importvertrag.py`, auch relative Importe.
- **A2** Außen kennt innen, nie umgekehrt: `anwendung/` und `katalog/` kennen die Domäne,
  `speicher/` von `arbiter` nur `anwendung/`; `katalog/` und `speicher/` kennt nur
  `__main__.py`. Prüft: wie A1; `speicher/` ab seinem ersten Modul (Auslöser), der Rest nur
  Text.
- **A4** `web/` kennt von `arbiter` nur `anwendung/`; `anwendung/` nur die Domäne und die
  Standardbibliothek. Prüft: nur Text; Auslöser: Freigabe des Plans mit dem ersten Item zum
  Speicher, dann `formregeln/importvertrag.py` vor dem [Umbau](architektur/anwendung.md#umbau).
