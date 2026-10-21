# Vier Tests zu Item anhaltenAnBases verlangen, was keine Umsetzung liefern kann

1460 · Kritik · von Implementierer → Testautor · Runde 1/3 · erledigt

## Runde 1
**Befund.** Einordnung nach Ich 3: hält auf, vier Tests bleiben rot, alle übrigen des Items sind grün.
1. `testAuf24_1DerDienstNenntDieStellenDesBlocksWieDasBeispielImVertrag`: Die Fixture
   `aufstellungDesBeispiels` wählt die *Einheit* nicht aus, das Beispiel `stelleBeimLoslassen.json`
   gilt für den Stand mit *ausgewählter* *Einheit* (V1). Ohne *Auswahl* nennt der Dienst nach
   AUF-20.4 nur das eine *Modell*. Die Tests in `modellPerKlickTest.py` rufen dazu `auswählen` auf.
2. `testAuf26_3DerDienstKürztDenWegDerEinheitVorDerBaseEinerAnderenOhneGrund`: Der Dienst liest
   `y = 100/127` als Dezimalzahl wie gesendet (S2), der Weg liegt dann um 1e-17 neben dem Weg des
   Tests; `liegtAufDerStrecke` verlangt exakt kollinear.
3. und 4. `testAuf26_2DieSeiteSetztDasModellAnDieBaseAnOhneGrund[maus|finger]`: Die Seite sendet den
   Pixel des Zeigers (B5, auf einen Pixel genau), der Weg liegt daneben; dieselbe exakte Prüfung.

**Kosten.** Die Tests prüfen ihr Kriterium nicht, sondern die Rundung der Eingabe.

**Gegenvorschlag.**
1. In der Fixture oder im Test die *Einheit* auswählen.
2. und 3. und 4. Den Weg des Dienstes und der Seite aus der gesendeten Zahl rechnen (die
   Streckenprüfung mit dem gesendeten Ziel) oder eine Toleranz von `zollJePixel` wie bei
   `liegtEinPixelGenauAn`; ‚keine *Base* überdeckt‘ und `stößtAn` bleiben exakt.

**Stellungnahme.** Angenommen und umgesetzt.
1. `testAuf24_1DerDienstNenntDieStellenDesBlocksWieDasBeispielImVertrag` wählt vorher
   „Necron Warriors“ aus, wie `modellPerKlickTest.py`.
2. `testAuf26_3DerDienstKürztDenWegDerEinheitVorDerBaseEinerAnderenOhneGrund` prüft den Weg
   mit der neuen Hilfe `liegtNahAnDerStrecke` (`anhalten.py`) und der Toleranz `dezimalFehler`
   (1e-9 Zoll, die Rundung der Dezimalzahl, S2).
3. und 4. `testAuf26_2DieSeiteSetztDasModellAnDieBaseAnOhneGrund[maus|finger]` prüfen mit
   `liegtNahAnDerStrecke` und `zollJePixel(seite)` (B5).
Die Prüfungen ‚keine *Base* überdeckt‘ und `stößtAn` sind unverändert exakt; alle Fälle
der Domäne prüfen die Strecke weiter exakt. Lauf vor und nach über `anhaltenAnEinerBaseTest.py`
und `blockAlsGanzesTest.py`: vorher genau diese vier rot, nachher alle 160 grün.
`ruff check` und `ruff format --check` sind grün.
