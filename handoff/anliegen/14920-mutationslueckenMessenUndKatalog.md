# Mutationslücken in messen und im Katalog

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: erledigt
Wartet auf: Technikphase 10

## Runde 1
**Befund.** Neu an dich aus Anliegen 8971 (Unit-Tests gehören dir). Der Mutationslauf von
Zyklus 9 lag unter der Schwelle; nach der [DoD](../../prozess/ablauf/dod.md) wird darunter
jeder Überlebende angegangen. Am heutigen Code nachgeprüft bleiben vier Lücken in den Tests;
die Befunde 4 und 5 aus 8971 sind erledigt, seit `abbildungLesen` die leere und die falsch
geformte Abbildung prüft und
[eintragLesenTest.py](../../technik/tests/einheit/katalog/eintragLesenTest.py) beides fängt.
1. [messen.py, Zeile 160](../../technik/arbiter/domaene/messen.py#L160), `schritte == 0`
   wird `schritte == 1`: Bei einem Weg von genau einem Rasterschritt (1/100 Zoll), der schon
   trifft, gibt das Original den Anteil 0, der Mutant 1; das *Modell* stünde 1/100 Zoll über
   der *Spielfeldkante* oder der *Bewegungsweite*. Kein Unit-Test ruft
   `anteilVorDemErstenSchrittMit` auf. Fangen müsste ihn ein Test in
   [messenTest.py](../../technik/tests/einheit/domaene/messenTest.py) mit dem Weg
   `(Fraction(1, 100), Fraction(0))` und einer Prüfung, die ab jedem Anteil über 0 trifft:
   Anteil 0.
2. [messen.py, Zeile 186](../../technik/arbiter/domaene/messen.py#L186), `return Fraction(1)`
   wird `Fraction(2)`: Ohne Berührung auf dem Weg liefert `anteilBisZurBerührungAufDemWeg` 2.
   Am Bildschirm deckt es heute das Minimum in `stellenMitGründenNachDemZiehen` zu; die
   Funktion selbst hält ihren Vertrag nicht. Der einzige Test mit Anteil 1 hat einen Weg der
   Länge 0 und endet schon in Zeile 178. Fangen müsste ihn ein Test neben
   `testAufDemWegHältDerAnteilVorEinerBaseAnDieDasEndeSchonÜberquertHat`: ein Hindernis
   abseits des Wegs, Anteil 1.
3. [katalog/ausgangslage.py, Zeile 24](../../technik/arbiter/katalog/ausgangslage.py#L24),
   `raise` entfällt in `_textLesen`: Kein Fall mit einem Namen, der kein Text ist. Ein Fall
   `{"fraktion": 5, …}` in `testEinFehlerhafterEintragEinerEinheitIstEinFehlerBeimLaden`
   ([ausgangslageTest.py](../../technik/tests/einheit/katalog/ausgangslageTest.py)) allein
   genügt nicht: `datenblätterVon` im Test wirft für eine unbekannte *Fraktion* ebenfalls
   einen `ValueError`. Er braucht `match="Ein Name muss Text sein"`.
4. [katalog/datenblaetter.py, Zeile 67](../../technik/arbiter/katalog/datenblaetter.py#L67),
   `raise` entfällt: Der Fall `"../orks"` in `testEineFraktionOhneOrdnerIstEinFehler` endet
   ohne die Prüfung im `FileNotFoundError` und damit im selben `ValueError`. Fangen müsste
   ihn eine *Fraktion*, die nicht nur aus Buchstaben besteht, deren Ordner es aber gibt:
   `"./orks"`.

**Kosten.** Am Bildschirm: nichts. Im Code: Diese Tests bleiben grün, auch wenn die Prüfung
fehlt, die sie zu prüfen scheinen (Absicht 1, Anliegen 692). Token: zwei Tests, zwei Fälle.

**Gegenvorschlag.** Die Tests und Fälle aus 1 bis 4; Produktcode ändert sich dafür nicht.

**Stellungnahme.** Angenommen, alle vier umgesetzt, Produktcode unverändert:
1. `testEinWegVonEinemRasterschrittDerSchonTrifftHatDenAnteilNull` in messenTest.py.
2. `testEineBaseAbseitsDesWegsBerührtNieUndDerAnteilIstEins` in messenTest.py.
3. `testEinNameDerKeinTextIstIstEinFehlerBeimLaden` mit `match="Ein Name muss Text sein"` in ausgangslageTest.py.
4. Fall `"./orks"` in `testEineFraktionOhneOrdnerIstEinFehler` in datenblaetterTest.py.
Alle Einheitstests grün (282).
