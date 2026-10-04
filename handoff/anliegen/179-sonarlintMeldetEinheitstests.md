# SonarLint meldet S5778 in den Einheitstests

179 · Anliegen · von Regelumsetzer (Prozess) → Implementierer (Technik) · Runde 1/3 · angenommen

## Runde 1
**Befund.** Der Wegwerf-Versuch aus P2 (Retro 2, [150](150-sonarlintAbdeckungUndToterCode.md))
läuft: `python3 prozess/pruefungen/sonarlint.py` ruft den Analysator der Erweiterung ohne
VS Code und meldet das Standardprofil. Acht Funde bleiben, alle in Einheitstests
(Regel S5778: in `pytest.raises` nur ein Aufruf, der werfen kann):
- `technik/tests/einheit/domaene/phasen/aufstellenTest.py`: Zeilen 36, 45, 63, 71, 84
- `technik/tests/einheit/katalog/ausgangslageTest.py`: Zeilen 18, 25, 37

Das sind dieselben Meldungen, die der Stakeholder in VS Code sieht.

**Gegenvorschlag.** Den Aufruf, der nicht werfen soll (Aufbau von Argumenten, Verschachtelung),
vor den Block `with pytest.raises(...)` ziehen; im Block bleibt nur der eine werfende Aufruf.

**Kosten.** Acht kleine Umbauten, kein neues Verhalten.

**Folge.** Bis dahin prüft die Sperre `technik/tests/einheit` nicht
(`geprüfteOrdner` in `prozess/pruefungen/sonarlint.py`). Sind die Funde weg, nimmt der
Regelumsetzer den Ordner auf; die Prüfung ist dann dort rot, nicht mehr nur die Meldung.

**Stellungnahme (Implementierer).** Angenommen und umgesetzt. In allen acht Tests steht der
nicht werfende Aufbau vor `pytest.raises`. `sonarlint.py`: keine Funde; `pytest technik/tests`: 153 grün.
