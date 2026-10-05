# Frontend, Backend und Datenbank fehlen in der Technik

153 · Kritik · von Stakeholder → Architekt · Runde 1/3 · erledigt

## Runde 1
**Befund (Stakeholder).** „Ich vermisse in der Technik die Frontend Backend Struktur sowie
die Anlage der Datenbank.“

**Stellungnahme (Architekt).** Berechtigt. Der Aufbau steht jetzt in der Technik:
Frontend und Backend in [Web](../../technik/architektur/web.md), die Datenbank in
[Speicher](../../technik/architektur/speicher.md); [Architektur](../../technik/architektur.md)
verlinkt beide, A2 und A3 sind angepasst. Er beantwortet zugleich die Fragen 1 bis 3 in
Anliegen 146 (git).

**F1 · Wann wird die Datenbank angelegt?**
- A: Mit der ersten Handlung über HTTP (Wählen oder Setzen); die reine Anzeige der
  Ausgangslage braucht keine.
- B: Schon mit der ersten Oberfläche, auch wenn sie nur anzeigt.

Empfehlung: A. Vor der ersten Handlung gibt es nichts zu speichern, was nicht schon im YAML
steht.

Antwort: .

Beantwortet mit der Freigabe von Plan 3: A, eingetragen in Speicher (erster Absatz).

Rückfrage: Betrachtest du dieses Anliegen als erledigt? Bitte begründen.

**Antwort (Architekt).** Ja, dein Befund ist behoben. Begründung:
1. *Frontend und Backend* stehen in Web: getrennt (W1), ein dünnes `web/` mit drei Modulen,
   je eins für Server, Anfragen und Übersetzung des Spielstands (W2), ein Befehl mit Adresse
   (W5), Oberfläche ohne Framework (O1 bis O3). Der Code folgt dem: `web/anwendung.py`
   liefert `technik/frontend/` unverändert aus und antwortet mit JSON (`jsonify`). Ein
   `render_template` wie in `ArbiterMap/backend/app/routes/map.py` gibt es nicht.
2. *Datenbank* steht in Speicher: SQLite ohne ORM, Tabellen `partie` und `handlung`, der
   Spielstand entsteht durch Wiederholen der Handlungen (P1 bis P3). Eine Datei gibt es noch
   nicht; das ist deine Antwort F1 A. Sie entsteht mit „Wählen per Klick mit Speicher“
   ([Plan 3](../plan.md), Danach).
3. Was offen ist, gehört nicht zu diesem Befund und hat schon einen eigenen Ort:
   - der Vertrag (Pfade, JSON): [Ablauf, Technikphase](../../prozess/ablauf.md#technikphase),
     Schritt 1, fällig mit dem ersten Item mit beiden Hälften;
   - zwei Fragen zum Wiederholen: [Speicher, Neuland](../../technik/architektur/speicher.md#neuland),
     Wegwerf-Versuch mit der ersten Handlung über HTTP;
   - Prüfungen zu W1, W2 und D3: [265](265-ausgeloestePruefungenZuWeb.md), beim
     Regelumsetzer.
   Hielte 153 sie fest, stünden sie zweimal.

Zusichern kann ich nicht, dass P2 trägt; das zeigt erst der Wegwerf-Versuch. Ändert er den
Aufbau, wird das ein neues Anliegen. Empfehlung: Setze `erledigt`; das darf nur der Absender.
