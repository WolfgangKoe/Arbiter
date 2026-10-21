# Eine Zeile, die ein Fakt abhakt, ist im Dashboard auch offen gesperrt

Form: Kritik
Von: Organisationsentwickler
An: Regelumsetzer
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Nachprüfung von [2060](2060-boardOhneKommentarfelderFortschrittDaneben.md),
Punkt 3 „was ein Fakt abhakt, bleibt gesperrt“: `rollenregeln/dashboardFortschritt.py`
sperrt eine Zeile nur, wenn ihr Fakt schon gilt (`vonFakt=zeile.fakt is True`). Zeilen, deren
Fakt noch fehlt (`fakt` ist `False`), lassen sich anklicken; in der laufenden Retro 6 sind das
„Regelumsetzer: P3“, „Regelumsetzer: P5“ und „Koordinator: nach dev gepusht“, in anderen
Phasen etwa „Stakeholder: Freigabe Plan“. Auch `standregeln/zeilenZug.py`
(`zeilenzugÜbernehmen`) nimmt den Haken für jede Zeile an, und `abschnittBauen` behält ihn.
Einordnung nach Ich 3: abseits des Happy Path, die Phase seiner Perspektive läuft; darum ohne
`Wartet auf:`.

**Kosten.** Seit ein Haken nicht mehr entfernbar ist (Kommentar des Stakeholders in 2060),
setzt ein Fehlklick auf eine solche Zeile sie dauerhaft auf erledigt, ohne Commit oder Push;
der Fortschritt und der nächste Schritt im Stand stimmen dann nicht mehr, zurück geht es nur
von Hand in der Datei.

**Gegenvorschlag.** Bestehende Regel (Ich 4): [Ablauf, Fortschritt](../../prozess/ablauf.md#fortschritt),
Spalte „abgehakt durch“ und Absatz Dashboard, dort schon so gefasst; deine Zeile zu Anliegen
490 in `prozess/regeln.md` ziehst du nach.
1. Gesperrt ist jede Zeile mit Fakt (`zeile.fakt is not None`), gesetzt oder offen.
2. Der Server weist einen Haken auf eine solche Zeile ab, wie einen leeren Kommentar.

Erledigt, wenn Scheiter-Tests zeigen: Eine Zeile mit noch fehlendem Fakt erscheint mit
`disabled`, und ein Haken dafür über `/fortschritt` ändert die Datei nicht.

Bordmittel geprüft: keine; das Dashboard ist eigener Code.

**Stellungnahme.** Angenommen und umgesetzt: Jede Zeile mit Fakt (`fakt is not None`) ist im
Dashboard gesperrt, und `zeilenzugÜbernehmen` weist den Haken darauf ab. Scheiter-Tests:
`rollenregeln/dashboardFortschrittTest.py` (`testEineZeileMitNochFehlendemFakt…`),
`standregeln/zeilenZugTest.py` (`testDerHakenAufEineZeileMitFaktWirdAbgewiesen`).
