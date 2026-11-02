# Dienst der Schlacht wählt „ohne Ebene“: derselbe Name wie in 7420

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Wartet auf die nächste Technikphase ([Kritik](../../prozess/ablauf/kritik.md)): Der
Test steht schon länger und gehört nicht zur laufenden Änderung, keine Prüfung ist rot. Gefunden
bei der Nachprüfung von Anliegen 7420.
`testAuf20_6DerDienstWähltBeimAnklickenEinesModellsInDerSchlachtDieGanzeEinheitOhneEbene` in
[ebeneTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/ebeneTest.py) prüft AUF-20.6 in
[ebene.md](../../domaene/anforderungen/phasen/aufstellen/ebene.md). Das Kriterium lautet:
„*ausgewählt* mit der ganzen *Einheit* als *Ebene*“. „Ohne Ebene“ sagt also das Gegenteil des
Kriteriums und des [Glossars](../../domaene/glossar.md). Gemeint ist nur, dass im Spielstand kein
*Modell* `ebene` trägt (`ebenenIm(spielstand) == frozenset()`). Es ist derselbe Fehler wie in
7420.

**Kosten.** Ein Name, am Bildschirm nichts. Bleibt er, versteht man darunter eine *Auswahl* ohne
*Ebene*, und die gibt es nicht.

**Gegenvorschlag.** Umbenennen in
`testAuf20_6DerDienstWähltBeimAnklickenEinesModellsInDerSchlachtDieGanzeEinheitAlsEbene`. Die
Prüfung bleibt.

**Stellungnahme.** Umgesetzt wie vorgeschlagen: In
[ebeneTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/ebeneTest.py) heißt der Test
`testAuf20_6DerDienstWähltBeimAnklickenEinesModellsInDerSchlachtDieGanzeEinheitAlsEbene`, die
Prüfung bleibt. Die Datei ist grün.
