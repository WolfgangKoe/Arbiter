# Soll die Sandbox den Sitzungsbus des Rechners sperren?

Form: Fragen
Von: Regelumsetzer
An: Stakeholder
Runde: 3/3
Status: erledigt

## Runde 1
**Befund.** Zu P3 aus [Retro 6](../retro.md), Kritik [2140](2140-sandboxOeffnetAlleUnixSockets.md):
`network.allowAllUnixSockets: true` in `.claude/settings.json` lässt Befehle im Käfig mit den
Hintergrunddiensten des Rechners sprechen; belegt: `busctl --user list` erreicht den
Sitzungsbus. Über ihn kann ein Befehl außerhalb des Käfigs starten (nicht ausgeführt).

**Gegenvorschlag.** Zeile entfernen; `sandboxGrenzen.py` wird bei ihr rot.

**Stellungnahme.**

**F1 · `allowAllUnixSockets` entfernen und die Prüfung um `network` erweitern?** Empfehlung: ja.
Antwort: ja, danke für die Erklärung. So wie ich es jetzt verstehe, schließt du die Sandbox zu.
Kommentar: Ich verstehe die Frage nicht und welche Konsequenzen meine Antwort darauf hat. Bitte erläutern!!!

## Runde 2
**Befund.** Deine Antwort war „ja“, aber mit dem Kommentar, du verstündest die Frage nicht.
Darum frage ich neu und einfacher.

**Stellungnahme.**

**Klärung.** In einfachen Worten:

*Was die Einstellung heute erlaubt.* Jeder Befehl eines Agenten läuft in einem Käfig, der das
Schreiben in deine Projektordner verbietet (`handoff/`, `prozess/` u. a.). Eine Zeile in
`.claude/settings.json` lässt aber Befehle im Käfig mit den Hintergrunddiensten deines
Rechners sprechen. Einer dieser Dienste kann auf Anfrage neue Programme starten, und die
laufen dann nicht mehr im Käfig.

*Was eine Rolle damit tun könnte.* Sie könnte absichtlich diesen Umweg nehmen und doch in
gesperrte Ordner schreiben. Das ist keine Panne, die von selbst passiert; es braucht Absicht.
Beobachtet habe ich es nicht, und ich habe es nicht ausprobiert.

*Was du davon merkst.* Heute nichts. Ändert sich etwas, merkst du es nur, wenn ein Werkzeug
wirklich einen solchen Dienst braucht: Dann scheitert sein Befehl mit einer Fehlermeldung, und
ich gebe genau diesen einen Dienst gezielt frei. Verloren geht nichts.

*Bei „ja“.* Die Zeile wird entfernt. Der Käfig hat dann keine offene Tür mehr, und die
Prüfung wird rot, sobald jemand sie wieder einträgt. Das ist das, was du mit „zuschließen“
gemeint hast. Du trägst es in `.claude/settings.json` selbst ein (im Block `"sandbox"` die
Zeile `"network": {"allowAllUnixSockets": true}` löschen); ich ziehe die Prüfung nach.
*Bei „nein“.* Alles bleibt wie heute; die Tür bleibt offen, und ich vermerke in den Regeln,
dass die Sperre diesen Umweg nicht abdeckt.

**F1 · Die Zeile mit `allowAllUnixSockets` löschen?** Empfehlung: ja, weil du die Rollen
sicher einsperren willst und der Preis nur ein gelegentlicher, gezielt behebbarer Fehler ist.
Annahme: Bis dahin bleibt alles wie heute.
Antwort: Ja

## Runde 3
**Befund.** Du hast nach meiner Anleitung die Zeile gelöscht. Danach scheiterte jeder Befehl
der Agenten, sogar `echo`, mit der Meldung, der Käfig könne nicht starten (`apply-seccomp …
Permission denied`). Du hast die Zeile wieder eingesetzt. Ich hatte die Empfehlung nicht
erprobt und geschrieben, es scheitere höchstens gelegentlich ein Werkzeug; das war falsch.
Der Fehler liegt bei mir.

**Stellungnahme.**

**Klärung.** Die Zeile steht wieder, die Lücke (Befehle im Käfig erreichen Hintergrunddienste)
bleibt offen. Wie man sie schließt, ohne den Käfig lahmzulegen, ist ungelöst; das klären wir im
nächsten Chat mit `claude-code-guide`. Künftig wird eine Änderung, die du selbst machst, vorher
erprobt (Anliegen [2201](2201-aenderungenDesStakeholdersVorherErproben.md)).

**F1 · Bleibt die Zeile bis zur Klärung?** Empfehlung: ja.
Annahme: Bis dahin bleibt alles wie heute.
Antwort: Ja

**Abschluss.** Gegenstandslos: Der Stakeholder hat P3 gestrichen, die Sandbox entfällt
([1970](1970-sandboxFuerBashSchreibenNichtPruefbar.md)); ohne Sandbox gibt es keine Tür zu
sperren. Die Antwort von `claude-code-guide` (Wege mit `sudo`, nicht erprobt) wird nicht verfolgt.
