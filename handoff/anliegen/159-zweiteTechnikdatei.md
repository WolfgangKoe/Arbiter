# Zweite Technikdatei für den Architekten

159 · Fragen · von Organisationsentwickler (Prozess) → Stakeholder · Runde 1/3 · offen

## Runde 1
**Befund.** `technik/architektur.md` ist mit 5.985 Zeichen am Höchstmaß 6.000
([Kennzahlen](../../prozess/kennzahlen.md)). Dein Anliegen
[153](153-frontendBackendUndDatenbank.md) (Frontend, Backend, Datenbank) und Regel D4 aus
[152](152-solidUndVieleIf.md) brauchen rund 2.500 Zeichen mehr. Kürzen heißt aufteilen, der
Architekt darf aber nur `architektur.md` schreiben ([155](155-technikBrauchtPlatzUndErstesMockup.md),
Punkt 1). Ein Schreibpfad ist ein Recht; das entscheidest du.

**Kosten.** Ohne zweite Datei bleiben 152 und 153 offen, oder der Architekt streicht geprüfte
Regeln. Plan 3 braucht den Aufbau aus 153 für die erste Oberfläche.

**Gegenvorschlag.** Der Architekt bekommt den Schreibpfad `technik/webUndSpeicher.md`
(Frontend, HTTP, Datenbank, Oberfläche); `architektur.md` bleibt die Übersicht und verlinkt
sie. Höchstmaß je Datei 6.000. Mechanismus: Agentendefinition (`schreibpfade:`) und
`schreibgrenze.py`; das Höchstmaß bleibt nur Text.

**F1 · Welcher Schreibpfad?**
- A: Die eine Datei `technik/webUndSpeicher.md`. Jede weitere Datei ist ein neues Anliegen.
- B: `technik/*.md`, wie der Architekt vorschlägt.
Empfehlung: A. Das Muster `*` greift in `schreibgrenze.py` auch über Ordner hinweg, B
erlaubte also jede `.md` unter `technik/`, auch `technik/CLAUDE.md`, die dem Prozess gehört.

Antwort: .
