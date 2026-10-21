# Die arabisch-indische Ziffer prüft re.ASCII nicht

1656 · Kritik · von Architekt → Implementierer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Kritik am Code zu [1630](1630-sonarlintRotInAnwendung.md). Die Architektur hält:
`_jsonZahlText` liegt in der Webschicht, die Domäne bleibt unberührt. Aber die neue Zeile
`{"x": "٣", "y": 2}` in `testEineAbfrageDerStelleBeimLoslassenOhneZahlenFürXUndYIstEineFehlerhafteAnfrage`
([anwendungTest.py](../../technik/tests/einheit/web/anwendungTest.py)) belegt nicht, was die
Stellungnahme in 1630 ihr zuschreibt:

- Die erste Ziffer prüft das Muster mit `[1-9]` bzw. `0`, das ist auch ohne `re.ASCII` nur
  ASCII. „٣“ scheitert dort, `\d` wird gar nicht erreicht.
- Ohne `re.ASCII` lehnt `json.loads` jede nicht-ASCII-Ziffer ab (`ValueError`, abgefangen),
  also bleibt es bei 400, auch für `"1٣"`.

Gegenprobe in `/tmp`: Muster ohne `re.ASCII` eingesetzt, alle 12 Fälle des Tests bleiben grün.
Die Mutante „`re.ASCII` entfernen“ überlebt also jede Eingabe; sie ist gleichwertig, solange
`json.loads` dahinter steht.

Nach [Ich 3](../../prozess/praemissen/ich.md) wartet es auf die nächste Technikphase: Keine
Prüfung ist rot, das Verhalten (V5) stimmt. Die Testzeile führt nur den Leser in die Irre.

**Kosten.** Eine Testzeile, kein Produktcode. Der Mutationslauf des Reviewers meldet die
Mutante womöglich als überlebend; dann ist dieser Befund die Erklärung.

**Gegenvorschlag.** Die Zeile auf `{"x": "1٣", "y": 2}` ändern: Sie läuft dann durch `\d` und
belegt, dass eine nicht-ASCII-Ziffer hinter der ersten 400 ergibt, mit oder ohne `re.ASCII`.
Dass `re.ASCII` allein nichts am Ergebnis ändert, nimmt man hin: Es hält das Muster ehrlich
(V5 im Muster, nicht erst in `json.loads`) und stillt SonarLint (S6353).

**Stellungnahme.**
Angenommen. Die Testzeile heißt jetzt `{"x": "1٣", "y": 2}` und läuft durch `\d`.
