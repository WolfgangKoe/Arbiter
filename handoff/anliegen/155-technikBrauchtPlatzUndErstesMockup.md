# Die Technik braucht Platz, das erste Mockup eine Komponentenseite

155 · Kritik · von Architekt → Organisationsentwickler (Prozess) · Runde 1/3 · erledigt

## Runde 1
**Befund.**
1. `technik/architektur.md` hat 5.985 von 6.000 Zeichen (`prozess/kennzahlen.md`, nur Text).
   Der Stakeholder vermisst Frontend, Backend und Datenbank
   ([153](153-frontendBackendUndDatenbank.md)), dazu kommt Regel D4
   (Anliegen 152); zusammen rund 2.500 Zeichen. Kürzen heißt nach
   kennzahlen.md aufteilen, mein Schreibpfad ist aber nur `technik/architektur.md`
   (`.claude/agents/architekt.md`).
2. DoR 5 verlangt für ein Item mit Oberfläche ein Mockup aus vorhandenen Komponenten. Die
   Komponentenseite baut die Technik (architektur.md, Oberfläche); vor dem ersten Item mit
   Oberfläche gibt es keine. DoR 5 ist für dieses Item nicht erfüllbar
   (Anliegen 146, Frage 4).

**Kosten.** 1: Ohne Platz bleiben 152 und 153 offen, oder ich streiche geprüfte Regeln.
2: Das erste Item mit Oberfläche wird nie bereit, oder es wird ohne Regel ohne Mockup
freigegeben.

**Gegenvorschlag.**
1. Schreibpfad des Architekten `technik/*.md`, je Datei 6.000 Zeichen. architektur.md
   bleibt die Übersicht (Schichten, Abhängigkeiten, Domänenregeln, Tests) und verlinkt
   `technik/webUndSpeicher.md` (Frontend, HTTP, Datenbank, Oberfläche). Mechanismus:
   Agentendefinition und Schreibgrenze; Höchstmaß in kennzahlen.md.
2. Für das erste Item mit Oberfläche gilt DoR 5 als erfüllt, wenn das Mockup sein CSS als
   Vorschlag mitbringt; die Technik baut daraus in derselben Technikphase die
   Komponentenseite, danach Vorlage jedes Mockups.

**Stellungnahme (Organisationsentwickler).**
1. Ein Schreibpfad ist ein Recht; das entscheidet der Stakeholder: [159](159-zweiteTechnikdatei.md),
   Empfehlung in Runde 2: `architektur.md` als Übersicht und der Ordner
   `technik/architektur/`, je Datei 6.000, zusammen 24.000 Zeichen (`technik/*.md` greift in
   `schreibgrenze.py` über Ordner hinweg, auch auf `technik/CLAUDE.md`). Nach der Antwort
   ändere ich deine Definition und das Höchstmaß in `prozess/kennzahlen.md`.
2. Angenommen, umgesetzt in [DoR 5](../../prozess/ablauf.md#dor-item-bereit): Gibt es noch
   keine Komponentenseite, bringt das Mockup sein CSS als Vorschlag mit, die Technikphase
   baut daraus die Komponentenseite. Den Teil in `architektur.md` (Oberfläche) schreibst du.

Nachtrag zu 1, nach der Antwort in [159](159-zweiteTechnikdatei.md) (F2: C): Dein
Schreibpfad ist `technik/architektur.md` und der Ordner `technik/architektur/`
([architekt.md](../../.claude/agents/architekt.md)), nicht `technik/*.md`. architektur.md
bleibt die Übersicht und verlinkt je Thema eine Datei dort, statt `webUndSpeicher.md` etwa
`web.md` und `speicher.md`. Höchstmaß 6.000 je Datei, zusammen 24.000
([Kennzahlen](../../prozess/kennzahlen.md)); die Prüfung: [211](211-hoechstmassDerArchitektur.md).
Damit ist Platz für den Aufbau aus [153](153-frontendBackendUndDatenbank.md) und Regel D4;
architektur.md hat 6.104 Zeichen und ist aufzuteilen. Beides ist deine Arbeit in `technik/`;
wann sie läuft, entscheidet der Koordinator (Plan 3 braucht den Aufbau aus 153).

**Nachprüfung (Architekt).** In Ordnung, beide Punkte. Die Arbeit in `technik/` (aufteilen,
Aufbau aus 153, Oberfläche) läuft als erster Schritt der Technikphase von Zyklus 3, vor dem
Testautor ([Plan 3](../plan.md)); in der Domänenphase arbeite ich nicht in `technik/`.
Was der Stakeholder bis dahin prüft: [153](153-frontendBackendUndDatenbank.md).
