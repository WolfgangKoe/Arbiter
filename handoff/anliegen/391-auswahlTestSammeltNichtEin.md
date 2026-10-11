# auswahlTest sammelt nicht ein: Klasse zwischen den Parametrierungen

391 · Kritik · von Implementierer (Technik) → Testautor (Technik) · Runde 1/3 · erledigt

## Runde 1
**Befund.** `technik/tests/akzeptanz/phasen/aufstellen/auswahlTest.py` scheitert beim
Einsammeln mit „function uses no argument 'fall'“. Zwischen den `@pytest.mark.parametrize`
für `spielername` und `einheitenname` (um Zeile 60 bis 70) und der Funktion
`testAuf5_3EinKlickAufEineNichtAusgewählteEinheitMachtSieAusgewählt` steht die Klasse
`Auswahlfall`. Die Dekoratoren davor hängen an der Klasse; die Parametrierung `fall`
(Zeile 77) landet an Test AUF-5.3, der kein `fall` hat. `testAuf5_8DerDienstÄndertBei…`
(Zeile 470) nimmt `fall`, hat aber keine Parametrierung.

**Kosten.** Die ganze Datei, alle Tests zu AUF-5, läuft nicht. Ich lasse sie aus, bis der
Fehler behoben ist (Ablauf, Technikphase Schritt 2).

**Gegenvorschlag.** `class Auswahlfall` vor alle Dekoratoren stellen; die Parametrierung
`fall` an `testAuf5_8…` hängen. Erledigt, wenn `python3 -m pytest
technik/tests/akzeptanz/phasen/aufstellen/auswahlTest.py` einsammelt.

**Stellungnahme.** Angenommen und umgesetzt. `Auswahlfall` steht vor allen Dekoratoren,
`fall` hängt an `testAuf5_8DerDienstÄndert…`. Auch die vier übrigen Parametrierungen
hingen an der Klasse; ich habe sie den Tests mit den passenden Parametern zugeordnet:
AUF-5.3 (Klick und Dienst), AUF-5.4 (Klick und Dienst), AUF-5.6 (Ablage).
