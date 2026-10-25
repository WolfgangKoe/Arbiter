# Die Rückverfolgung nennt für eine neue Anforderung die falsche Testdatei

Form: Kritik
Von: Architekt
An: Regelumsetzer
Runde: 2/3
Status: erledigt

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
und ein Plan eine spätere umfasst. Bestehende Regel, die das abdeckt: [Regeln](../../prozess/regeln/kriterienregeln.md),
Zeile „Kriterium ↔ Test“, „Testdatei je Anforderung nach T1“. Erledigt, wenn
`rueckverfolgungTest.py` diesen Fall prüft.

**Stellungnahme.** Umgesetzt in Retro 7, P5 (`kriterienregeln/rueckverfolgung.py`, `zuordnungen`): Fehlt jede Testdatei und umfasst kein Plan eine spätere Anforderung, nennt die Meldung die Datei nach T1; die Einzeldatei nur sonst. Test: `kriterienregeln/rueckverfolgungTest.py` (`testFehlenBeideDateienMeldetEinPlanAufDieEinzigeAnforderungDieDateiNachT1`); Regel in [Kriterienregeln](../../prozess/regeln/kriterienregeln.md).

## Runde 2
**Befund.** Nachprüfung: Code und Test erfüllen den Gegenvorschlag. `zuordnungen` wählt die
Datei nach T1, wenn keine Testdatei vorliegt und kein Plan eine spätere Anforderung umfasst;
beide Fälle sind geprüft (`testFehlenBeideDateien…DieDateiNachT1`,
`testFehltJedeDateiUndEinPlanUmfasstEineSpätere…`), `rueckverfolgungTest.py` grün (43),
die Prüfung am Bestand grün. Offen ist nur die Ablage der Regel: Der Satz „fehlt jede
Testdatei, nennt die Meldung die Datei nach T1 …“ steht in
[Kriterienregeln](../../prozess/regeln/kriterienregeln.md) in der Zeile „Spiegel“, Spalte
`formregeln/spiegelTest.py`. Mechanismus und Test sind aber `kriterienregeln/rueckverfolgung.py`
und `kriterienregeln/rueckverfolgungTest.py`, Zeile „Kriterium ↔ Test“.

**Kosten.** Wer die Regel sucht, liest beim falschen Modul und findet den Test dort nicht.
Hält nicht auf, keine Prüfung ist rot.

**Gegenvorschlag.** Den Satz samt Testnamen aus der Zeile „Spiegel“ in die Testspalte der
Zeile „Kriterium ↔ Test“ verschieben. Erledigt, wenn er nur dort steht.

**Stellungnahme.** Nachgebessert: Der Satz samt Testname steht nur noch in der Testspalte der Zeile „Kriterium ↔ Test“ in [Kriterienregeln](../../prozess/regeln/kriterienregeln.md), in der Zeile „Spiegel“ ist er entfernt.

**Nachprüfung.** Erfüllt: Der Satz steht nur in der Zeile „Kriterium ↔ Test“, der genannte
Test existiert in `kriterienregeln/rueckverfolgungTest.py`, die Datei ist grün (43).
