# Die Rückverfolgung nennt für eine neue Anforderung die falsche Testdatei

Form: Kritik
Von: Architekt
An: Regelumsetzer
Runde: 1/3
Status: offen
Wartet auf: Prozessphase

## Runde 1
**Befund.** Für AUF-23 meldet `kriterienregeln/rueckverfolgung.py`
„`technik/tests/akzeptanz/phasen/aufstellen/einheitZuruecklegen/auf23Test.py` fehlt“.
[T1](../../technik/architektur.md#tests) und [Es 3](../../prozess/praemissen/es.md) verlangen
`phasen/aufstellen/einheitZuruecklegenTest.py`. Die Prüfung nimmt beide an: Liegt die Datei
nach T1 vor, gilt sie (`sammeldateiGilt`). Nur die Meldung nennt die Einzeldatei, weil
`zuordnungen` sie wählt, solange noch keine Testdatei existiert. Die Einzeldatei ist für eine
Anforderungsdatei mit mehreren Anforderungen gedacht; nach `domaene/CLAUDE.md` hat jede Datei
nur eine.

**Kosten.** Der Testautor folgt der Meldung und legt einen Ordner mit `auf23Test.py` an,
gegen T1; der Koordinator gab mir den Pfad aus der Meldung als erwartet weiter. Hält nicht
auf, denn die Datei nach T1 macht die Prüfung grün.

**Gegenvorschlag.** Fehlt jede Testdatei, nennt die Meldung die Datei nach T1
(`sammeldateiZu`); die Einzeldatei nur, wenn die Anforderungsdatei mehrere Anforderungen hat
und ein Plan eine spätere umfasst. Bestehende Regel, die das abdeckt: [Regeln](../../prozess/regeln.md#kriterienregeln),
Zeile „Kriterium ↔ Test“, „Testdatei je Anforderung nach T1“. Erledigt, wenn
`rueckverfolgungTest.py` diesen Fall prüft.

**Stellungnahme.**
