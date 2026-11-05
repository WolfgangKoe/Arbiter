# Fliegen als Typ statt Zweig, dazu zwei falsche Ergebnisse

Form: Kritik
Von: Architekt
An: Implementierer
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Kritik am Code zu Item fliegen, Abschnitt 2 (ungemerkter Stand in
`phasen/bewegung/__init__.py`, `uebergehenBeimZiehen.py`, `schlachtrunden.py` und den beiden
Einheitstests). A1 und Spiegel sind grün. Drei Befunde halten auf
([Kritik](../../prozess/ablauf/kritik.md): neuer Code verletzt Architektur oder
[Es](../../prozess/praemissen/es.md)). Die beiden Proben liegen in `/tmp/arch13740/`.
1. `phasen/bewegung/__init__.py` hat jetzt 14.436 Zeichen, vorher 10.997. Das Höchstmaß
   ist 12.000 ([Kennzahlen](../../prozess/kennzahlen.md#höchstmaße)). Der Grund: *Fliegen*
   kommt als Zweig in fünf Methoden hinzu (`_gezeigt`, `_anteile`, `_gründe` mit dem
   Schalter `mitBaseÜberdeckt`, `übergangen`, `stellenMitGründenNachDemLoslassen`). Das
   verletzt Es O. Der Fehler liegt in meinem Vertrag, der diese Weiche verlangte. Auch sein
   Ausweg, nur das Gleiten auszulagern, hätte nicht unter 12.000 geführt. Ich habe den
   [Vertrag](../../technik/architektur/vertrag/bewegung/fliegen.md) berichtigt (Aufbau).
2. `_nachFremdenBasesGerückt` misst `zurück` ab `next(iter(gesetzt.values()))`. Das ist das
   erste *Modell* im Mapping, nicht das gezogene; das verletzt Es 6. In `übergangen` kommt
   die *Ebene* aus einem `frozenset`, ihre Reihenfolge ist also beliebig. Probe
   (`probe2.py`): Eine *Ebene* aus zwei Fliegern wird übergangen, das gezogene Modell landet
   auf einer fremden *Base*. Ergebnis: Sperre `baseÜberdeckt`, egal in welcher Reihenfolge.
   Mit dem Weg ab dem gezogenen *Modell* findet die Suche x 37 (`probe3.py`). Die Spinne ist
   heute der einzige Flieger und steht allein, darum zeigt das kein Akzeptanztest.
3. BEW-18.7 verlangt BEW-8.5 an der *Stelle* danach. 8.5 sagt: ‚Nahkampfreichweite‘, wenn 6.2
   **ohne 3.1** angehalten hätte. `_anteile` setzt das Ende von 18.3 aber auch beim
   Übergehen auf min(3.1, 6.1). Probe (`probe.py`): Flieger bei x 10, Gegner bei x 31,
   gezogen bis x 20 und übergangen. Die *Stelle* x 20 liegt in *Nahkampfreichweite*, der
   *Eintrag* nennt aber nur ‚Bewegungsweite‘. Ohne *Fliegen* nennt er beide. Mein Vertrag
   sagte das nicht ausdrücklich; jetzt steht dort „mit Ende 6.1 (8.5: ohne 3.1)“.

**Kosten.** Am Bildschirm ändert 1 nichts. Ohne 1 wächst die Datei weiter, und jede weitere
Bewegungsart braucht neue Zweige in allen fünf Methoden. Genau so wurden ArbiterMap und
Arbiter-old unwartbar (Absicht 1). Der Umbau verschiebt etwa 150 Zeilen ohne neue Logik;
geschätzt bleiben in `__init__.py` rund 9.600 Zeichen. Die Einheitstests über
`Bewegungsphase` bleiben gültig. 2 und 3 sind je eine Zeile, dazu je ein Einheitstest.
Alles zusammen ist ein Implementierer-Lauf.

**Gegenvorschlag.**
1. Nach dem neuen Aufbau im Vertrag: eine Art zu ziehen als Typ mit den Methoden, die
   `Bewegungsphase` aufruft. Das sind die *Stellen* nach V10, der Anteil von 6.2 bis zu einem
   Ende, die *Stellen* beim Loslassen und beim Übergehen und ob `baseÜberdeckt` beim Ziehen
   zählt. Das Gleiten mit `_gekürztAnDerNahkampfreichweite` kommt nach
   `phasen/bewegung/anhaltenVorFremdenBases.py`, das Fliegen nach `fliegen.py`.
   `Bewegungsphase` wählt die Art einmal aus `Gezogen.fliegen`. Danach entfallen
   `mitBaseÜberdeckt` und der Alias `anteilBisZurNahkampfreichweiteDesFliegers`. Neue
   Klassennamen gehen über den Anforderungsautor ins Glossar
   ([Wir 2](../../prozess/praemissen/wir.md)).
2. `zurück = messen.wegZwischen(gesetzt[gezogenes], davor)`, dazu `gezogenes` als Parameter.
   Einheitstest: Zwei Flieger in einer *Ebene* werden übergangen, das gezogene Modell kommt
   aus einem Mapping, in dem es nicht vorne steht. Erwartet: frei, kein *Grund*.
3. Beim Übergehen ist das Ende von 18.3 der Anteil von 6.1 auf dem gegangenen Weg, ohne 3.1.
   Einheitstest wie `probe.py`: erwartet {bewegungsweite, nahkampfreichweite}.

**Stellungnahme.** 1 bis 3 umgesetzt.
