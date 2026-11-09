# Ein Mutationslauf je Zyklus

Form: Kritik
Von: Stakeholder
An: Organisationsentwickler
Runde: 1/3
Status: offen
Wartet auf: Prozessphase

## Runde 1
**Befund.** Wortlaut des Stakeholders:
„Ehrlich, ein Mutationstest pro Zyklus reicht! Wenn wir ihn jetzt starten, hätten wir es
vorher nicht machen müssen!“
Anlass: Nach dem Lauf des Zyklus (`/tmp/mutation10b.log`, 96 min, 374 Mutanten, 82 %, gleich
wie `/tmp/mutation10.log`) startete der Reviewer zur Nachprüfung von
Anliegen 15462 einen weiteren; er ist abgebrochen
(`/tmp/mutation10c.log`, exit 143).
Bestehende Regeln, die mehrere Läufe je Zyklus verlangen (Ich 4):
- [Mutationsregeln](../../prozess/regeln/mutationsregeln.md): „der Lauf geschieht je Item vor
  dem Review“; ein Ergebnis gilt nur, solange `technik/` gleich ist. Jeder neue Test ändert
  `technik/`, also verfällt der Merkzettel und die Nachprüfung läuft alles neu.
- [DoD](../../prozess/ablauf/dod.md), voller Lauf: „ändert sich `technik/` danach, startet er
  ihn neu“ (Anliegen 8961). Mechanismus: nur Text.
- 15462, Gegenvorschlag: „Erledigt, wenn … mutationsregeln.mutation 95 % meldet“, also ein
  ganzer Lauf als Nachprüfung.

**Kosten.** Je Lauf über eine Stunde, alle Kerne belegt; Commits und Bildschirmtests der
anderen Rollen werden langsam. Wenige Token, aber Wartezeit für dich und den Koordinator.

**Gegenvorschlag (Organisationsentwickler).** Ein Mutationslauf je Zyklus, einmal, im
Hintergrund, sobald die DoD über das Inkrement sonst grün ist. Danach kein Neustart, wenn
sich `technik/` ändert. Die Überlebenden prüft der Testautor einzeln nach, nur ihre Zeilen
(`mutationsregeln.mutation <Modul>:<von>-<bis>`, gibt es schon); das genügt auch dem Absender
zum Abschluss. Was im Zyklus nicht gefangen ist, steht im nächsten Lauf wieder da.
Ändern: der Absatz in der DoD und „je Item vor dem Review“ in den Mutationsregeln, nach
`Freigabe Retro 10` als Prozess-Item in der [Retro 10](../retro.md). Mechanismus: nur Text;
`mutation.py` bleibt, wie es ist. Rückweg: Commit `P<k>:` zurücknehmen.

**Stellungnahme.**

**F1 · Welcher Lauf ist der eine je Zyklus?**
A: Der gezielte über die geänderten Zeilen; im Zyklus, dessen Plan die Etappe abschließen soll, an seiner Stelle der volle (DoD, Anliegen 8961)
B: In jedem Zyklus der volle über alle Module, auch `web/` (DoD, Anliegen 8961)
C: Wie bisher, gezielt je Item und der volle mit Neustart (Mutationsregeln, DoD)
Empfehlung: A, die Schwelle von 95 % gilt den geänderten Zeilen; der volle prüft auch
Unverändertes und dauert länger, er lohnt sich nur zum Abschluss einer Etappe.
Antwort: .
