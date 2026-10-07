# Die Prüfskripte sind nicht ordentlich strukturiert abgelegt

107 · Kritik · von Stakeholder → Organisationsentwickler (Prozess) · Runde 1/3 · angenommen

Legende: Status im Kopf · als Empfänger angenommen, rückfrage, abgelehnt · als Absender erledigt, offen (neue Runde) · unter einer Frage `Antwort: .` (Empfehlung), `Antwort: B` oder `Antwort: <Text>`

Kritik: Ich möchte mir die Prüfskripte gerne anschauen können. Je mehr dazukommen, desto unübersichtlicher wird der Inhalt des Ordners. Des Weiteren scheinen mir die Prüfskripte nicht den Kriterien für lesbaren Code zu entsprechen.

**Stellungnahme (Organisationsentwickler):** Angenommen; die früheren Stellungnahmen im
Wortlaut: `git show 9edb97e:handoff/anliegen/107-kritikAnDenPruefungen.md`. Die Ordnung in
Themenordnern und der Rückstand sind mit Anliegen 113 und 114 umgesetzt; SOLID und
Lesbarkeit führt Anliegen 253 beim Regelumsetzer.

Weitere Kritik: Was ist mit dieser Datei? /home/wolfgang/Dokumente/Arbiter_Structure/prozess/pruefungen/benennungRueckstand.txt

Nachprüfung: Der Koordinator hat mich gebeten, dieses Anliegen nachzuprüfen. Die Datei "benennungRueckstand.txt" finde ich nicht mehr und ist daher wohl gelöscht. Der Teil des Anliegens ist erledigt. 107 ist voraussichtlich mit 114 abgeschlossen, bitte nach Abschluss von 114 dieses Anliegen hier nochmal zur Prüfung vorlegen.

Antwort: Hier scheint noch keine Reaktion vom @organisationsentwickler gekommen zu sein. 

**Stellungnahme (Stakeholder):** Verstehe ich es richtig, dass wir hier eine Art Zyklus haben, der im schlimmsten Fall immer weiter wächst, aber keinen echten Mehrwert liefert? Falls ja, wie können wir das sinnvoll eindämmen. Ich bin ein Fan von Regeln, die uns helfen, diese sollte aber möglichst schlank sein. Bevor wir eine neue Regel einführen, sollte geprüft werden, ob es die schon gibt bzw., ob eine bestehende diese schon abdeckt. GGf. muss diese auch einfach nur angepasst werden. 

**Stellungnahme (Organisationsentwickler):** Ja, der Kreis ist messbar: Jede Regel will einen
Mechanismus, jeder Mechanismus ist Code, jeder Code bekommt Kritik, jede Kritik wird ein
Anliegen an den Regelumsetzer. Seit `Freigabe Retro 2` gingen 71 von 107 neuen Anliegen an
ihn oder mich (66 %, Schwelle der [Prozesslast](../../prozess/kennzahlen.md) ein Drittel);
die Prüfskripte samt Tests wuchsen von 183.000 auf 322.600 Zeichen, der Produktcode von
13.000 auf 18.300. Die Bremse der Kennzahl, erst löschen, dann neu, ist nur Text und griff nie.
Schlank eindämmen:
1. Erst suchen, dann regeln: [ich.md](../../prozess/praemissen/ich.md) 4, seit 255 in Kraft.
2. Der Stand rechnet die Prozesslast; darüber beauftragt der Koordinator keinen neuen
   Mechanismus, der nicht von dir kommt, bevor ein alter gelöscht ist.
3. Ein Gesamtmaß für `prozess/pruefungen/`: Was hinzukommt, nimmt anderswo weg.
2 und 3 lege ich dir in Retro 3 als Prozess-Items vor ([Backlog](../../prozess/backlog.md));
dort sortiere ich auch die 26 offenen Anliegen an den Regelumsetzer in behalten,
zurückstellen, schließen. Wartet auf 253.

**Stellungnahme (Organisationsentwickler):** 253 ist erledigt, die Prüfskripte sind
gegliedert und nach [es.md](../../prozess/praemissen/es.md) überarbeitet. Zum Eindämmen
schlage ich statt 2 schlankere Anpassungen bestehender Regeln vor: Deckel, Backlog und Kritik
nur bei Fehlverhalten, Fragen in [296](296-prozesslastEindaemmen.md), aufgenommen in
[Retro 3](../retro.md). Punkt 3 bleibt im Backlog. Bitte nachprüfen.