# Speicher: die Datenbank

[Übersicht](../architektur.md). Angelegt wird die Datenbank mit dem ersten Item zum Speicher
([Umbau](anwendung.md#umbau)).

## Aufbau
- **P1** SQLite über `sqlite3` aus der Standardbibliothek, ohne ORM; eine Datei außerhalb von
  git. Importe nach A2. Prüft: nur Text.
- **P2** Gespeichert wird nicht der Zustand, sondern die Folge der Handlungen einer Partie:
  - `partie`: Kennung, Beginn.
  - `handlung`: Partie, Nummer, Art, Angaben als JSON, übergangene Sperre.
  Den Spielstand stellt ein Dienst in `anwendung/` her, indem er die Handlungen auf der
  Ausgangslage wiederholt. Katalogdaten kommen nicht hinein ([A3](katalog.md)).
  Prüft: nur Text; Auslöser: erstes Modul in `speicher/`, dann ein Akzeptanztest „wiederholt
  ergibt denselben Spielstand“.

Warum so: Jede wiederholte Handlung läuft durch dieselben Sperren der Domäne, die keine
Datenbank kennt (A2); das *Protokoll* des Übergehens ist dieselbe Tabelle; das Schema wächst
nicht mit jedem Spielobjekt (Gegenbeispiel `ArbiterMap/backend/app/repository/schema.sql`,
10.000 Zeichen). Neuland: das Wiederholen, auch einer übergangenen Sperre (D2); vorher ein
Wegwerf-Versuch.
