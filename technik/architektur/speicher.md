# Speicher: die Datenbank

Übersicht und Schichten: [Architektur](../architektur.md). Angelegt wird die Datenbank mit der
ersten Handlung über HTTP (Wählen oder Setzen); die Anzeige der Ausgangslage braucht keine.

## Aufbau
- **P1** SQLite über `sqlite3` aus der Standardbibliothek, ohne ORM; eine Datei außerhalb von
  git. Prüft: nur Text; Auslöser: erstes Modul in `speicher/`, dann der Importvertrag
  „`speicher/` importiert weder `flask` noch `arbiter.web`“.
- **P2** Gespeichert wird nicht der Zustand, sondern die Folge der Handlungen einer Partie:
  - `partie`: Kennung, Beginn.
  - `handlung`: Partie, Nummer, Art, Angaben als JSON, übergangene Sperre.
  Den Spielstand stellt `web/` her, indem es die Handlungen auf der Ausgangslage wiederholt.
  Prüft: nur Text; Auslöser: wie P1, dann ein Akzeptanztest „wiederholt ergibt denselben
  Spielstand“.
- **P3** Katalogdaten bleiben YAML in `domaene/daten/` (A3); in die Datenbank kommen sie nicht.

## Warum so
- Die Domäne bleibt die einzige Prüfinstanz: Jede wiederholte Handlung läuft durch dieselben
  Sperren. Sie braucht keine Schnittstelle zur Datenbank (A2); `speicher/` kennt nur Art und
  Angaben, die Übersetzung in Handlungen der Domäne macht `web/`.
- „Zurück“ heißt, die letzte Handlung weglassen; das Protokoll des Übergehens ist dieselbe
  Tabelle.
- Das Schema wächst nicht mit jedem Spielobjekt. Gegenbeispiel ArbiterMap: eigene Tabellen
  für Einheiten und Modelle, `ArbiterMap/backend/app/repository/schema.sql` hat 10.000
  Zeichen.

## Neuland
Das Wiederholen der Handlungen: vorher ein Wegwerf-Versuch, mit der ersten Handlung über
HTTP. Offen bis dahin: wie eine übergangene Sperre beim Wiederholen übersprungen wird (D2), und
wie ein Bildschirmtest seinen Zustand übergibt: Heute bekommt `serverStarten` die
`Aufstellung` (W2, B1), mit dem Speicher wäre es die Folge der Handlungen.
