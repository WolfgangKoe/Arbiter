# Zweite Technikdatei für den Architekten

159 · Fragen · von Organisationsentwickler (Prozess) → Stakeholder · Runde 2/3 · beantwortet

## Runde 1
**Befund.** `technik/architektur.md` ist mit 5.985 Zeichen am Höchstmaß 6.000
([Kennzahlen](../../prozess/kennzahlen.md)). Dein Anliegen
[153](153-frontendBackendUndDatenbank.md) (Frontend, Backend, Datenbank) und Regel D4 aus
Anliegen 152 brauchen rund 2.500 Zeichen mehr. Kürzen heißt aufteilen, der
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

Antwort: Ich brauche hier mehr Kontext und wie bereits in einem anderen Anliegen die Vor- und Nachteile der hier vorgestellten Optionen. Wenn ich es richtig verstehe, kommen wir genau an dem Punkt mit dem Zeichenlimit, der das gewünschte Verhalten mit sich bringt. Wir bauen die Archtiktur aus. Doch hier legen wir möglicherweise einen Grundstein für das, was noch kommt. Dies lässt sich an ArbiterMap und an Arbiter-old ein stückweit einschätzen. Argumentiere im Blick auf den zu erwartenden Scope, welche deiner Entscheidungen dies am ehesten berücksichtigt. Vielleicht kommst du dabei noch auf eine bessere Idee.

## Runde 2
**Befund.** Zu erwartender Umfang: ArbiterMap hat für die Technik vier Dateien mit zusammen
rund 75.000 Zeichen (`docs/spec/architecture.md`, `architecture_invariants.md`,
`design_system.md`, `design_colors.md`), Arbiter-old allein für das Design-System 69.000.
Arbiter kommt bis zum Ziel mindestens dazu: Web und HTTP, Speicher mit Datenbank,
Oberfläche mit Komponentenseite und Bildschirmtest, später Bewegung und Kampf in der Domäne.
Ein Schreibpfad für eine Datei reicht also für ein Thema, nicht für den Scope.

**Stellungnahme.**
- A, eine Datei `webUndSpeicher.md`. Vorteil: eng, jede weitere Datei entscheidest du.
  Nachteil: Mit der Oberfläche ist sie wieder voll; je Thema ein neues Anliegen an dich, und
  Web, Speicher und Oberfläche teilen sich 6.000 Zeichen.
- B, `technik/*.md`. Vorteil: Der Architekt teilt frei. Nachteil: Das Muster trifft auch
  `technik/CLAUDE.md` (Prozess) und jede `.md` in Unterordnern; kein Gesamtmaß, die Technik
  kann wachsen wie in ArbiterMap.
- C, neu: `technik/architektur.md` bleibt die Übersicht (Schichten, Abhängigkeiten, Tests)
  und verlinkt je Thema eine Datei im Ordner `technik/architektur/` (`domaene.md`, `web.md`,
  `speicher.md`, `oberflaeche.md`). Schreibpfad: die Übersicht und der Ordner. Höchstmaß
  6.000 je Datei, dazu ein Gesamtmaß von 24.000 Zeichen für alle.
  Vorteil: wächst mit dem Scope ohne neues Anliegen; ein Ordner greift nicht über Ordner
  hinweg; eine Rolle liest nur das Thema, das sie braucht (der Implementierer der Oberfläche
  nur `oberflaeche.md`), das spart Token; das Gesamtmaß verhindert ArbiterMap. Links auf
  `architektur.md` bleiben gültig.
  Nachteil: Mehr Dateien, in denen eine Aussage doppelt stehen kann (Architekt, Kritik am
  Code); Gesamtmaß und Höchstmaß prüft erst eine Prüfung, bis dahin nur Text.

**F2 · Welcher Schreibpfad?**
- A: Die eine Datei `technik/webUndSpeicher.md`.
- B: `technik/*.md`.
- C: Übersicht `technik/architektur.md` und Ordner `technik/architektur/`, je Datei 6.000,
  zusammen 24.000 Zeichen.
Empfehlung: C.

Antwort: C
