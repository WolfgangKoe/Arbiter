# Plan für den Rest von Item fliegen

Form: Kritik
Von: Implementierer
An: Koordinator
Runde: 1/3
Status: offen

## Runde 1
**Befund.** Der Lauf des Implementierers endete an der Tokengrenze, bevor fliegenTest.py grün war.
Fertig: `technik/arbiter/domaene/messen.py` hat `Kreisrand`, `Geradenrand`,
`anteilVorDerLetztenBerührung` und `wegInDieFreieFläche` (noch ohne Einheitstests, noch nie
ausgeführt). Alles andere fehlt.

**Gegenvorschlag.** Ein weiterer Implementierer-Lauf macht, in dieser Reihenfolge:
1. ERLEDIGT: `messen.py` läuft; `technik/tests/einheit/domaene/messenTest.py` prüft
   `anteilVorDerLetztenBerührung` und `wegInDieFreieFläche` (Lot- und Schnittpunkte,
   Weitenkreis, Vorfilter, Mitte gleich Ursprung).
2. ERLEDIGT (mit Einheitstests `tests/einheit/domaene/phasen/bewegung/fliegenTest.py`):
   `phasen/bewegung/fliegen.py` mit 18.3 und 18.2. Schnittstelle für Punkt 3:
   `anteilBisZurNahkampfreichweite(vorige, weg, gegner, ende)` mit `ende` = min(3.1, 6.1), vom
   Aufrufer berechnet; `nachFremdenBasesGerückt(gesetzt, zurück, Umgebung(fremde, gegner,
   spielfeld, weiten))` mit `weiten: Mapping[Modell, Weite(anfang, zoll)]` (zoll =
   Bewegungsweite plus Vorrückwurf; leer für 18.7) liefert `gesetzt` selbst zurück, wenn keine
   fremde überdeckt oder keine freie Stelle gefunden wird (dann sperrt QUE-1.2 von selbst).
Offen sind 3 bis 6 (Stand nach diesem Lauf; Tests in `fliegenTest.py` der Akzeptanz: alle 29 rot).
3. ERLEDIGT (Einheitstests in `bewegung/bewegungsphaseTest.py`; Aufrufe der Tests und
   `schlachtrunden.py` mit umgestellt, da die Signatur sich änderte): `phasen/bewegung/__init__.py`: `Gezogen` (ebene, gezogenes, ziel, weiter, fliegen) ersetzt
   die Parameter mit `# noqa: PLR0913`; `Angebot.fliegen`; Weiche je Methode: V10 ohne Gleiten,
   ohne Grund `baseÜberdeckt`, `_anteile` mit 18.3; neue Methode
   `stellenMitGründenNachDemLoslassen` rückt nach 18.2; `übergangen` für Flieger ohne Gleiten,
   Rücken ohne Bewegungsweite, Gründe aus 3.1 und 18.3 auf dem Weg.
4. ERLEDIGT (mit Punkt 3, 28 von 29 Tests in `fliegenTest.py` grün; der rote: 13621): `querschnitt/schlachtrunden.py`: `_gezogen(modell, stelle, weiter)` mit `einheit.fliegen`;
   `modellLoslassen` nutzt die Loslassen-Variante, `stellenBeimLoslassen` die Ziehen-Variante.
5. ERLEDIGT: Aufrufe auf `Gezogen` umgestellt, Einheitstests zu `fliegen.py`; Anliegen 13660
   (Tests prüfen ihren Namen, Wege entpackt) angenommen. Kein Test zu BEW-18.6.
6. ERLEDIGT bis auf Gesamtlauf und Abhaken: 13760 und 13740 (2, 3) behoben, `fliegenTest.py`
   der Akzeptanz und die Einheitstests der Bewegung grün; 13620, 13621 nachgeprüft und
   erledigt. OFFEN: 13740 Punkt 1 (Typ), Gesamtlauf, SonarLint, Schritt abhaken.

Wann: sofort, neuer Implementierer-Lauf.
