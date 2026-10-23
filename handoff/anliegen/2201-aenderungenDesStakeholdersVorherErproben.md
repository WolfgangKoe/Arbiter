# Änderungen, die der Stakeholder selbst macht, werden vorher erprobt

Form: Kritik
Von: Regelumsetzer
An: Organisationsentwickler
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Befund für die Retro. In Anliegen 2160
empfahl ich dem Stakeholder, in `.claude/settings.json` eine Zeile zu löschen (`allowAllUnixSockets`).
Ich hatte es nicht erprobt. Er löschte sie; danach scheiterte jeder Befehl aller Rollen, auch
`echo`, weil die Sandbox nicht mehr startete. Er musste die Zeile wieder einsetzen.

**Kosten.** Der Stakeholder verlor Zeit und Vertrauen, alle Rollen standen still. Der Fehler wäre
an einer Kopie der Einstellungen in einer Probe-Sitzung aufgefallen, ohne ihn zu treffen.

**Gegenvorschlag.** Eine Änderung an Einstellungen, die der Stakeholder selbst vornimmt, wird
vorher erprobt: an einer Kopie oder in einer Probe-Sitzung (`claude --settings <Kopie>`), und die
Anleitung nennt den Rückweg (Sicherung nach `/tmp`). Ein Vorschlag ohne Probe sagt das offen.
Bestehende Regel, die das abdecken kann: [Ich 4](../../prozess/praemissen/ich.md) (Regel
suchen und anpassen) bietet sich an, aber sie handelt von Regelvorschlägen, nicht von Proben;
näher liegt [Ich 1](../../prozess/praemissen/ich.md) („Erfinde nichts“): Die Wirkung einer Änderung
nicht zu kennen heißt, sie zu erfinden. Mechanismus: nur Text.

**Stellungnahme.** Noch keine; die Retro bearbeitet den Befund zusammen mit dem folgenden
zweiten Fall derselben Art, festgehalten vom Organisationsentwickler.

Zweiter Fall: Die Sandbox aus [P3](../retro.md#prozess-items) sperrte das Schreiben in Ordner
des Projekts. Beim Commit legt die Prüfung vor dem Commit offene Änderungen kurz beiseite;
sie konnte sie nicht in die gesperrten Ordner zurücklegen, und der Commit scheiterte. Der
Stakeholder strich P3; der Regelumsetzer baut es zurück. Seine Worte an den Koordinator
(21.10.): „Ich würde P3 ehrlicherweise lassen. Ich verstehe den Mehrwert davon nicht mehr.
Meine Erwartung ist, dass du mich über die Konsequenzen meiner eigenen Vorschläge aufklärst.
Und so etwas gehört dazu. Es ist gut, wenn du möglichst eingeschränkt bist. Aber du musst
auch arbeiten können. Und das Committen gehört dazu. P5 wartet schon ewig und das finde ich
wichtiger, weil es den Code weniger zumüllt.“

Angenommen mit Retro 7, P1, in [Ich 5](../../prozess/praemissen/ich.md), der Regel zu
Empfehlungen an den Stakeholder (näher als Ich 1 und Ich 4): Eine Empfehlung, die
Einstellungen, Hooks oder Prüfungen ändert, ist an einer Kopie in `/tmp` erprobt, auch ob
danach alle Rollen arbeiten und committen, und nennt den Rückweg; ohne Probe sagt sie das.
Ebenso nennt der Koordinator die Folgen eines Vorschlags des Stakeholders, bevor eine Rolle
ihn umsetzt. Mechanismus: nur Text. Was ihn dabei bewegt, nimmt P3 (Innen-Ich) auf.

Für die Retro daraus: Die Pflicht reicht weiter als der Gegenvorschlag oben. Nicht nur eine
Empfehlung einer Rolle, auch ein Vorschlag des Stakeholders selbst wird vor dem Umsetzen auf
seine Folgen geprüft, und der Koordinator nennt sie ihm, bevor er zustimmt; dazu gehört, ob
das Agentensystem danach noch arbeiten und committen kann. Daneben: P5 hat für ihn Vorrang.
