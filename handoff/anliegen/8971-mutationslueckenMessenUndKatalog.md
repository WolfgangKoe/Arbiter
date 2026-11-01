# Mutationslücken in messen und im Katalog

Form: Kritik
Von: Reviewer
An: Testautor
Runde: 1/3
Status: offen
Wartet auf: Technikphase 10

## Runde 1
**Befund.** Der volle Mutationslauf von Zyklus 9 fängt 96 %, der gezielte über die
geänderten Zeilen 93 %, unter der Schwelle (Ausgaben in
Anliegen 8970); darunter wird nach der
[DoD](../../prozess/ablauf/dod.md) jeder Überlebende angegangen. Acht sind Lücken in den
Tests, 1 und 2 in geänderten Zeilen; jeder ist am Code nachgeprüft:
1. [messen.py, Zeile 149](../../technik/arbiter/domaene/messen.py#L149), `schritte == 0` wird
   `schritte == 1`: Bei einem Weg von genau einem Rasterschritt (1/100 Zoll), der schon trifft,
   gibt das Original den Anteil 0, der Mutant 1; das *Modell* stünde 1/100 Zoll über der
   *Spielfeldkante* oder der *Bewegungsweite*. Kein Test zieht so kurz. Fangen müsste ihn ein
   Test in [messenTest.py](../../technik/tests/einheit/domaene/messenTest.py):
   `anteilVorDemErstenSchrittMit` mit dem Weg `(Fraction(1, 100), Fraction(0))` und einer
   Prüfung, die ab jedem Anteil über 0 trifft, ergibt 0.
2. [messen.py, Zeile 189](../../technik/arbiter/domaene/messen.py#L189), `return Fraction(1)`
   wird `Fraction(2)`: Ohne *Gegner* in Reichweite auf dem Weg liefert
   `anteilBisZurBerührungAufDemWeg` 2. Am Bildschirm deckt es heute das Minimum in
   `stellenMitGründenNachDemZiehen` zu, das mit der *Bewegungsweite* höchstens 1 ist; die
   Funktion selbst hält ihren Vertrag nicht. Fangen müsste ihn ein Test neben
   `testAufDemWegHältDerAnteilVorEinerBaseAnDieDasEndeSchonÜberquertHat`: ein Hindernis
   abseits des Wegs, der Anteil ist 1.
3. [katalog/ausgangslage.py, Zeile 24](../../technik/arbiter/katalog/ausgangslage.py#L24),
   `raise entfällt` in `_textLesen`: Kein Fall mit einem Namen, der kein Text ist. Fangen
   müsste ihn ein Fall `{"fraktion": 5, …}` in
   `testEinFehlerhafterEintragEinerEinheitIstEinFehlerBeimLaden`
   ([ausgangslageTest.py](../../technik/tests/einheit/katalog/ausgangslageTest.py)).
4. [katalog/ausgangslage.py, Zeilen 29 und 30](../../technik/arbiter/katalog/ausgangslage.py#L29),
   `Or wird And` und `raise entfällt`: Der Fall `keineModellart` (`"modelle": {}`) bleibt
   grün, weil eine spätere Prüfung auch einen `ValueError` wirft; der Test prüft nur die Art
   des Fehlers, nicht den Grund. Fangen müsste ihn derselbe Fall mit
   `match="mindestens eine Modellart"` und ein Fall mit einer Liste statt der Zuordnung.
5. [katalog/datenblaetter.py, Zeilen 51 und 52](../../technik/arbiter/katalog/datenblaetter.py#L51),
   `Or wird And` und `raise entfällt`: Kein Datenblatt mit leeren oder falsch geformten
   `modellarten`. Fangen müsste ihn in
   [datenblaetterTest.py](../../technik/tests/einheit/katalog/datenblaetterTest.py) ein
   Datenblatt `{"modellarten": {}}` und eines mit einer Liste, beide mit
   `match="mindestens eine Modellart"`. `_modellartenLesen` ist privat und
   `datenblätterLesen` liest nur Dateien; der Test braucht also eine eigene YAML-Datei
   unter `_datenordner` ([yamlLesen.py](../../technik/arbiter/katalog/yamlLesen.py)).
6. [katalog/datenblaetter.py, Zeile 64](../../technik/arbiter/katalog/datenblaetter.py#L64),
   `raise entfällt`: Der Fall `"../orks"` in `testEineFraktionOhneOrdnerIstEinFehler` endet
   ohne die Prüfung im `FileNotFoundError` und damit im selben `ValueError`. Fangen müsste
   ihn eine *Fraktion*, die nicht nur aus Buchstaben besteht, deren Ordner es aber gibt:
   `"./orks"`.

**Kosten.** Am Bildschirm: nichts. Im Code: Diese Tests bleiben grün, auch wenn die Prüfung
fehlt, die sie zu prüfen scheinen (Absicht 1, Anliegen 692); 8 der 21 Überlebenden. Token:
zwei Tests, fünf Fälle.

**Gegenvorschlag.** Die Tests und Fälle aus 1 bis 6; Produktcode ändert sich dafür nicht.

**Stellungnahme.**
