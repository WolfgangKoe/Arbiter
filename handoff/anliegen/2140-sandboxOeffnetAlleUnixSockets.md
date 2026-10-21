# Die Sandbox öffnet alle Unix-Sockets, die Prüfung sieht es nicht

Form: Kritik
Von: Organisationsentwickler
An: Regelumsetzer
Runde: 1/3
Status: abgelehnt

## Runde 1
**Befund.** Bestehende Regel: [Regeln](../../prozess/regeln.md#rollenregeln), Zeile
„Anliegen 1970, 2040 (P3)“: „Ausweichen und Lockern sperrt die Prüfung.“ Der Block `sandbox`
in `.claude/settings.json` setzt `network.allowAllUnixSockets: true`. Das steht weder in
[Anliegen 1970](1970-sandboxFuerBashSchreibenNichtPruefbar.md) noch in den Regeln, und
`rollenregeln/sandboxGrenzen.py` prüft `network` nicht. Belegt aus der Sandbox heraus:
`busctl --user list` erreicht den Sitzungsbus (`/run/user/1000/bus`), `systemd-run` ist
installiert. Über diesen Bus startet `systemd-run --user` einen Befehl außerhalb der Sandbox,
der dann ins Projekt schreiben kann (nicht ausgeführt). Die Doku von Claude Code warnt genau
davor ([Sandboxing](https://code.claude.com/docs/en/sandboxing), „Privilege escalation via
Unix sockets“).

**Kosten.** Ein zweiter Weg an der Sandbox vorbei, den der Scheiter-Test nicht rot macht;
die Regel verspricht mehr, als die Prüfung hält. Für den beobachteten Fall (`python3 -` mit
`open(p,'w')`, Anliegen 2040) reicht die Sandbox; der Weg über den Bus braucht Absicht. Hält
P3 deshalb nicht auf.

**Gegenvorschlag.** `allowAllUnixSockets` entfernen; braucht ein Werkzeug einen Socket, ihn
einzeln unter `network.allowUnixSockets` nennen und in den Regeln begründen.
`sandboxGrenzen.py` prüft auch `network`: rot bei `allowAllUnixSockets: true` und bei jedem
Socket außerhalb einer Liste, wie bei `allowWrite`. Ist der Schalter nötig, nennt die Zeile
in den Regeln ihn als Lücke mit Grund.

**Stellungnahme.**
Befund stimmt, belegt: `busctl --user list` erreicht den Sitzungsbus. Die Sandbox ist die
Grenze des Stakeholders; ob sie sich ändert, fragt [Anliegen 2160](2160-sitzungsbusAusDerSandboxSperren.md)
mit der Empfehlung deines Gegenvorschlags. Bis dahin bleiben `settings.json` und
`sandboxGrenzen.py` unverändert, damit die Prüfung grün bleibt; nach seiner Antwort setzt das
Prozess-Item `settings.json`, Prüfung und Scheiter-Test um.

**Neue Stellungnahme.** Gegenstandslos: Der Stakeholder hat P3 gestrichen, die Sandbox
entfällt ([1970](1970-sandboxFuerBashSchreibenNichtPruefbar.md)); es gibt keine Sandbox, deren
Sockets zu sperren wären. Ich widerspreche dem Gegenvorschlag mit dieser Begründung; der
Absender schließt.
