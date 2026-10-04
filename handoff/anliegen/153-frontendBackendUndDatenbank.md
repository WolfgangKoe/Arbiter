# Frontend, Backend und Datenbank fehlen in der Technik

153 · Kritik · von Stakeholder → Architekt · Runde 1/3 · angenommen

## Runde 1
**Befund (Stakeholder).** „Ich vermisse in der Technik die Frontend Backend Struktur sowie
die Anlage der Datenbank.“

**Stellungnahme (Architekt).** Berechtigt. [architektur.md](../../technik/architektur.md)
nennt `web/`, `speicher/` und `frontend/` nur als Ordner; wie sie zusammenspielen, fehlt, und
für die Datenbank steht nur der Auslöser (A3). Der Aufbau unten geht in die Technik, sobald
dort Platz ist: architektur.md hat 5.985 von 6.000 Zeichen
(Anliegen 155). Er beantwortet zugleich die Fragen 1 bis 3
in Anliegen 146.

*Frontend und Backend*
- Ein Befehl startet Flask (`web/`) und nennt die Adresse. `web/` liefert die Dateien aus
  `frontend/` unverändert aus und beantwortet unter `/api/` Anfragen mit JSON. Getrennt
  heißt: `web/` erzeugt kein HTML, das Frontend kennt nur diese Adressen. Gegenbeispiel
  ArbiterMap: Das Backend füllt Jinja-Vorlagen aus `frontend/templates/`,
  `routes/map.py` hat 40.000 Zeichen.
- `web/` ist dünn: Anfrage lesen, eine Handlung der Domäne aufrufen, Antwort schreiben. Eine
  Anfrage je Handlung (Anliegen 03, in git); eine Sperre wird HTTP 409 mit der Liste ihrer
  Gründe (`Sperre.gründe`, Text aus `Grund`). Regeln stehen nur in der Domäne.
- Spielobjekte haben in der Domäne keine Kennung, sie sind über `is` gleich (D1). `web/`
  vergibt sie aus der Reihenfolge der Ausgangslage: Spieler, Einheit, Modell.
- Frontend: HTML, CSS mit Variablen und JavaScript-Module; kein Framework, kein
  Build-Schritt, kein Tailwind. Die Karte ist ein SVG in Zoll, der Browser skaliert. eslint
  und stylelint prüfen.

*Datenbank*
- SQLite über `sqlite3` aus der Standardbibliothek, ohne ORM; eine Datei außerhalb von git.
- Gespeichert wird nicht der Zustand, sondern die Folge der Handlungen einer Partie: Tabelle
  `partie` (Kennung, Beginn) und `handlung` (Partie, Nummer, Art, Angaben als JSON,
  übergangene Sperre). Den Spielstand stellt `web/` her, indem es die Handlungen auf der
  Ausgangslage wiederholt.
- Warum: Die Domäne bleibt die einzige Prüfinstanz und braucht keine Schnittstelle zur
  Datenbank (A2). „Zurück“ heißt, die letzte Handlung weglassen; das Protokoll des Übergehens
  ist dieselbe Tabelle. Das Schema wächst nicht mit jedem Spielobjekt; ArbiterMap hält den
  Zustand in eigenen Tabellen für Einheiten und Modelle, `schema.sql` hat 10.000 Zeichen.
- Katalogdaten bleiben YAML (A3); der dort geplante Import in die Datenbank entfällt.
- Neuland ist das Wiederholen der Handlungen: vorher ein Wegwerf-Versuch.

**F1 · Wann wird die Datenbank angelegt?**
- A: Mit der ersten Handlung über HTTP (Wählen oder Setzen); die reine Anzeige der
  Ausgangslage braucht keine.
- B: Schon mit der ersten Oberfläche, auch wenn sie nur anzeigt.

Empfehlung: A. Vor der ersten Handlung gibt es nichts zu speichern, was nicht schon im YAML
steht; B brächte `speicher/`, Schema und Tests in den Zyklus, der ohnehin Start, Karte,
Komponentenseite und Bildschirmtest bringt.

Antwort: .

**Nachtrag (Architekt).** Die Technik hat Platz (Anliegen 159, C;
Anliegen 155 erledigt). Eingetragen wird der Aufbau oben
als erster Schritt der Technikphase von Zyklus 3, vor dem Testautor ([Plan 3](../plan.md)):
Frontend und Backend in `technik/architektur/web.md`, die Datenbank in `speicher.md`,
`architektur.md` verlinkt beide. F1 beantwortet die Freigabe von Plan 3.
Deine Nachprüfung jetzt gilt dem Aufbau oben, bevor er in die Technik geht. Passt etwas
nicht, schreib es als Runde 2 mit Status `offen`, dann ändere ich ihn vorher. `erledigt`
setze bitte erst, wenn er in der Technik steht; das trage ich hier ein.
