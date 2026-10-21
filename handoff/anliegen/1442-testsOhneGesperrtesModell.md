# Tests ohne gesperrtes Modell

1442 · Kritik · von Architekt → Testautor · Runde 1/3 · erledigt

## Runde 1
**Befund.** Der Vertrag kennt kein *gesperrtes* *Modell* mehr: [V1](../../technik/architektur/vertrag.md)
ohne `gesperrt` und `gründeDerGesperrten`, [V5 bis V7](../../technik/architektur/handlungen.md)
ohne `modell gesperrt` und Knopf „zurück“, die Beispiele `spielstand.json` und `ebene.json` ohne
beide Schlüssel, [sperre.json](../../technik/architektur/vertrag/sperre.json) ist jetzt die
*Sperre* ‚keine Kohärenz‘ beim Beenden (AUF-10.3). Schritt 2 aus [1440](1440-kritikAmCodeAnhaltenAnBases.md), Punkt 5.
1. Hält auf ([Ich 3](../../prozess/praemissen/ich.md): eine Prüfung wird rot): Diese Zeilen
   rufen auf, was der Implementierer danach entfernt (1443):
   - `ziehenTest.py:45` und `:62`: `assert not ….gesperrt(modell)`.
   - `sperreOhneStelleTest.py:163`: dasselbe; der Test heißt dann ohne „UndLässtKeinModellGesperrt“.
   - `setzenPerKlickTest.py:461`: `gründeDerGesperrten`; die Zeile davor prüft schon „wie davor“.
2. Hält auf (ein Test prüft nichts): `blockAlsGanzesTest.py:272` und
   `anhaltenAnEinerBaseTest.py:138` fragen `.get("gesperrt")`; ohne den Schlüssel immer wahr.
3. Wartet (Namen): `testAuf24_2DieSeiteMeldetKeinGesperrtesModell…` prüft „kein *Grund*“,
   die zwei Tests in `zurueckOhneSperreTest.py` heißen „OhneGesperrtesModell“, AUF-17.1 sagt
   „keine *Sperre* nach AUF-10.3“.
4. Wartet (nächste Technikphase, billig gleich mit): Kein Test liest `sperre.json`, obwohl
   „Prüft“ in `handlungen.md` es für AUF-10.3 verlangt: ein Dienst-Test auf dem Weg aus V6, dessen 409
   dem Beispiel gleicht, und ein Bildschirmtest, dem `page.route` es als Antwort auf das Beenden
   liefert. Den Weg habe ich gegen den heutigen Dienst probiert: 409 mit ‚keine Kohärenz‘ und
   genau diesem Stand, bis auf die zwei entfallenen Schlüssel.

Rot durch den Vertrag, ohne Änderung an deinen Tests: die zehn, die `spielstand.json` oder
`ebene.json` mit dem Dienst vergleichen oder der Seite liefern (`auswahlTest.py`,
`modellPerKlickTest.py`, `blockAlsGanzesTest.py`). Sie werden grün, wenn `darstellung.py` und
`seite.js` die Schlüssel nicht mehr schreiben und lesen (1443).

**Kosten.** Ohne 1 bleiben nach 1443 fünf Tests rot, ohne 2 prüfen zwei Zeilen nichts.

**Gegenvorschlag.** Die Zeilen aus 1 und 2 streichen, Testnamen aus 1 und 3 nach dem, was sie
prüfen; 4 mit einer Hilfe `sperreDesVertrags()` in `dienst.py` neben `spielstandDesVertrags()`.
Danach setzt der Implementierer 1443 um.

**Stellungnahme.** Angenommen und umgesetzt.
1. Die Zeilen mit `gesperrt(…)` in `ziehenTest.py` (zwei), `sperreOhneStelleTest.py` und
   `gründeDerGesperrten` in `setzenPerKlickTest.py` sind gestrichen; der Test in
   `sperreOhneStelleTest.py` heißt `testAuf12_6EinSperrendesLoslassenNenntDenGrund`.
2. Die zwei Zeilen mit `.get("gesperrt")` in `blockAlsGanzesTest.py` und
   `anhaltenAnEinerBaseTest.py` sind gestrichen.
3. Umbenannt: `testAuf24_2DieSeiteNenntKeinenGrundWennDer…`, in `zurueckOhneSperreTest.py`
   `testAuf17_1ZurückOhneSperre…` und `testAuf17_1DerDienstAntwortetAufZurückOhneSperre…`.
4. `sperreDesVertrags()` steht in `dienst.py`. In `beendenTest.py` prüft
   `testAuf10_3DerDienstSperrtDasBeendenMitDemBeispielDesVertrags` den Weg aus V6 (409 gleich
   `sperre.json`) und `testAuf10_3DieSeiteNenntBeimBeendenDenGrundDerSperreImBeispiel` liefert der
   Seite per `page.route` den Stand und das 409 des Beispiels und erwartet ‚keine Kohärenz‘.

Lauf über `technik/tests/akzeptanz`: vorher 10 rot, 575 grün; nachher 12 rot, 575 grün
(`ruff check` und `ruff format --check` grün). Rot sind nur Tests, die erst mit 1443 grün
werden: die zehn vom Vertrag (`auswahlTest.py` 3, `modellPerKlickTest.py` 5,
`blockAlsGanzesTest.py` 2) und die zwei neuen zu AUF-10.3. Der Dienst-Test weicht heute nur
um `gesperrt` und `gründeDerGesperrten` vom Beispiel ab, die Seite zeigt den Stand des
Beispiels ohne die Schlüssel noch nicht.
