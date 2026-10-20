# Der Dashboard-Server läuft durch, bis der Stakeholder ihn beendet

1080 · Auftrag · von Stakeholder → Regelumsetzer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Der Stakeholder: „Ich finde es nicht gut, dass der Server für das Dashboard ständig deaktiviert wird.“ Ursache: Der Server prüfte nach jeder Anfrage, ob sich ein Prüfskript geändert hat, und ersetzte sich dann selbst durch einen neuen Start im selben Prozess. Rollen ändern Prüfskripte oft. Speichert eine Rolle ein Skript halb fertig oder mit Fehler, brach der Neustart ab und der Server war aus. Verschwand eine Datei zwischen Suchen und Lesen der Änderungszeit, stürzte schon die Prüfung ab. Beides endete ohne Meldung im Dashboard (Seite nicht erreichbar).

**Kosten.** Ein Wächterprozess mehr; der Server selbst läuft als Kind des Wächters.

**Gegenvorschlag.** Umgesetzt in `rollenregeln/dashboardServer.py`: Ein Wächter startet den Server als eigenen Prozess und startet ihn bei Codeänderung neu. Stürzt der Server wegen eines Fehlers im Code ab, wartet der Wächter auf die nächste Änderung und startet ihn dann wieder; der Wächter selbst endet nur mit Strg+C. Verschwundene Dateien fallen beim Prüfen nicht mehr auf. Scheiter-Test: `rollenregeln/dashboardServerTest.py`, `testDerServerStürztNichtMitEinemFehlerhaftenPrüfskriptUndLäuftNachDerBesserungWieder` und `testEinVerschwundenesPrüfskriptBringtDenStandNichtZumAbsturz`.

Start: `python3 prozess/pruefungen/gemeinsam/lauf.py rollenregeln.dashboardServer`

Bordmittel geprüft: Claude Code hat dafür keines; der Server gehört nicht zu seinen Hooks.

**Stellungnahme.** Umgesetzt, Tests grün.
Kommentar: Ich setze das Anliegen auf "erledigt" sobald es umgesetzt ist.
