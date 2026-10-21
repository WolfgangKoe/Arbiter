# Tests zu Item 2: Rest aus 1215, gezogenes Modell und Millionstel

1340 · Kritik · von Architekt → Testautor · Runde 1/3 · erledigt

## Runde 1
**Befund.** Nachprüfung von Anliegen 1215
und Anliegen 1216 an den Tests zu Item
[einheitVerschieben](../../domaene/items/einheitVerschieben.md): Beide sind erfüllt. Kein Test
zu AUF-20, 21, 24.2, 25 und 26.1 liest `gesperrt(…)`, `gründeDesGesperrten` oder
`gründeDerGesperrten`, keiner schneidet mit `[:` aus, alle Seitentests nehmen
`mitMausUndFinger` und `seiteMitEingabe`; `stelleImSpielstand` ist der eine Name für die
*Stelle* im Spielstand. `ruff check`, `ruff format --check` und `prozess/pruefungen`
(740) sind grün; die roten Tests scheitern an fehlendem Code (`ebeneWählen`, `ebene`, der
Weg `…/ebene`, das Hineinrücken), keiner an einem Feld, das V10 streicht. Das grep aus 1216
findet noch `float(stelle.x)` in `setzenPerKlickTest.py:166`; dort vergleicht der Test die
Anfrage eines Klicks je Achse mit Toleranz, nicht den Spielstand, das ist richtig so.

Was bleibt, wartet nach [Ich 3](../../prozess/praemissen/ich.md) (Ablage von Hilfen, keine
Prüfung rot):
1. `testAuf24_2KeinModellDesBlocksIstWegenEinesModellsDerselbenEinheitGesperrt`
   ([blockAlsGanzesTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/blockAlsGanzesTest.py))
   wählt das gezogene *Modell* von Hand
   (`(zweites, stelleZweites) if zweitesGezogen else (erstes, stelleErstes)`), die zwei
   anderen Tests zu 24.2 über `gezogenesUndRest(list(zip(…)))`. Grund: `modelleAnStellenSetzen`
   gibt nichts zurück, `modelleSetzen` gibt die Paare aus *Modell* und *Stelle*.
2. Die Tests zu 26.1 in
   [anhaltenAnEinerBaseTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/anhaltenAnEinerBaseTest.py)
   nehmen das eigene `millionstel` der Datei statt des aus `handgriffe.py` (1215, Punkt 3;
   in der Stellungnahme dem Testautor zu anhaltenAnBases zugewiesen).
3. `endstellen` ([einheitVerschiebenTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/einheitVerschiebenTest.py))
   und `erwarteteStelle` (anhaltenAnEinerBaseTest.py) rechnen beide `(Zoll, Radien)` mit
   `inZoll` in eine *Stelle* der *Aufstellungszone* um.

**Kosten.** Klein: Der Leser findet für „welches *Modell* wird gezogen“ zwei Formen in
einer Datei und für ein Millionstel Zoll zwei Konstanten. Ändert sich das Maß (Zoll und
Radien), sind es zwei Stellen.

**Gegenvorschlag.**
1. `modelleAnStellenSetzen` gibt wie `modelleSetzen` die Paare zurück; die drei Tests zu
   24.2 schreiben dann `(gezogenes, davor), _ = gezogenesUndRest(modelleAnStellenSetzen(…),
   zweitesGezogen=zweitesGezogen)`, ohne `zip` und ohne Wahl von Hand.
2. `millionstel` aus `handgriffe.py` importieren, die eigene Zeile entfällt. Ändert das
   schon die Kritik zu anhaltenAnBases, ist dieser Punkt damit erledigt.
3. `erwarteteStelle` nach `handgriffe.py` neben `inZoll`; `endstellen` ruft sie für das
   erste *Modell* und rückt das zweite um `2 * radius`.

Erledigt, wenn in `blockAlsGanzesTest.py` kein `zip(` und kein `if zweitesGezogen else`
steht, `anhaltenAnEinerBaseTest.py` kein `Fraction(1, 1_000_000)` enthält, `def erwarteteStelle` nur in `handgriffe.py` steht und `ruff check technik/tests`
sowie `python3 -m pytest prozess/pruefungen` grün bleiben.

**Stellungnahme.** Angenommen, Punkte 1 bis 3 umgesetzt.
1. `modelleAnStellenSetzen` gibt die Paare zurück, `blockVorEinerFremdenBase` und die drei
   Tests zu 24.2 in `blockAlsGanzesTest.py` nutzen sie mit `gezogenesUndRest`; dort steht
   weder `zip(` noch `if zweitesGezogen else`.
2. `anhaltenAnEinerBaseTest.py` importiert `millionstel` aus `handgriffe.py`.
3. `erwarteteStelle` steht in `handgriffe.py`; `endstellen` ruft sie für das erste *Modell*
   und rückt das zweite um `2 * radius`.
`ruff check`, `ruff format --check` und `prozess/pruefungen` sind grün.
