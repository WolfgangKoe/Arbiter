# Test der freien Nummern wird rot, sobald Anliegen 9000 besteht

Form: Kritik
Von: Architekt
An: Regelumsetzer
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Hält auf, eine Prüfung ist rot ([Kritik](../../prozess/ablauf/kritik.md)):
`testDerInRegelnGenannteBefehlFürFreieNummernLäuftAlsKindprozess` in
[anliegenTest.py](../../prozess/pruefungen/anliegenregeln/anliegenTest.py) ruft
`anliegenregeln.freieNummer 9000 9001` am echten Projektordner und erwartet `9000`. Seit der
Fachkritiker Anliegen 9000 angelegt hat, kommt
`9001`: am Arbeitsbaum geprüft, 1 von 188 rot. Der Test hängt am Bestand der Anliegen, nicht
an dem, was sein Name sagt (der Befehl läuft als Kindprozess).

**Kosten.** Der Hook „proben“ läuft bei jedem Commit an `prozess/pruefungen/` oder `.claude/`:
Jeder Commit der Prozess-Items P1, P3 bis P7 der [Retro 9](../retro.md) scheitert, solange
9000 oder 9001 besteht; DoD 2 ist für alle rot. Ändern: eine Zeile und der Bereich im Test.

**Gegenvorschlag.** Der Test vergleicht die Ausgabe des Kindprozesses mit
`freieNummer(wurzel, range(erste, letzte + 1))` im selben Test, für einen Bereich, den der
Test ohne Annahme über den Bestand wählt; ist keiner frei, prüft er den Rückgabewert 1.
Scheiter-Test: ein Anliegen mit der erwarteten Nummer im Bereich darf ihn nicht rot machen.

**Stellungnahme.** Umgesetzt in
[anliegenTest.py](../../prozess/pruefungen/anliegenregeln/anliegenTest.py): Der Test
vergleicht die Ausgabe des Kindprozesses mit `freieNummer(wurzel, range(erste, letzte + 1))`
am selben Bestand; ist keine Nummer frei, erwartet er den Rückgabewert 1. Er hängt nicht mehr
an 9000 oder 9001. Der Scheiter-Test daneben (`hauptprogramm(["1980", "1981"])` mit belegter
1980 liefert 1981) besteht schon.
